from pathlib import Path
import pytest
from app import extractors

TEST_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "test project data"


def test_extract_docx_real_project_charter():
    docx_file = TEST_DATA_DIR / "Project_Charter_HARBOR_Logistics.docx"
    assert docx_file.exists(), f"Testdatei nicht gefunden: {docx_file}"
    text = extractors.extract_docx(docx_file)
    assert text is not None
    assert len(text) > 100
    assert "HARBOR" in text
    # Pruefen, dass Tabellen oder Absaetze extrahiert wurden
    assert "\n" in text


def test_extract_xlsx_real_business_case():
    xlsx_file = TEST_DATA_DIR / "BC_2026_TANGENT_CorporateIT.xlsx"
    assert xlsx_file.exists(), f"Testdatei nicht gefunden: {xlsx_file}"
    text = extractors.extract_xlsx(xlsx_file)
    assert text is not None
    assert len(text) > 50
    assert "Tabellenblatt:" in text
    assert "|" in text  # Markdown Tabelle


def test_extract_text_file(tmp_path):
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("Das ist ein Testtext für MediaparkBrain.", encoding="utf-8")
    extracted = extractors.extract_text_from_file(txt_file, "test.txt")
    assert "Testtext für MediaparkBrain" in extracted


def test_extract_pdf_synthetic(tmp_path):
    from pypdf import PdfWriter

    pdf_path = tmp_path / "test.pdf"
    writer = PdfWriter()
    page = writer.add_blank_page(width=200, height=200)
    with open(pdf_path, "wb") as f:
        writer.write(f)

    # Sollte leer sein aber nicht abstuerzen
    extracted = extractors.extract_text_from_file(pdf_path, "test.pdf")
    assert isinstance(extracted, str)


def test_extract_image_without_llm_never_raises(tmp_path, monkeypatch):
    """Bilder werfen nie: ohne Sprachmodell (kein OCR) kommt ein Fallback-Text,
    der Upload laeuft trotzdem durch und haengt das Original an."""
    monkeypatch.setenv("LLM_API_KEY", "")
    img = tmp_path / "foto.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 32)  # kaputtes PNG: auch das darf nicht werfen
    text = extractors.extract_text_from_file(img, "foto.png")
    assert isinstance(text, str) and "foto.png" in text
    assert extractors.is_image("Bild.JPG") and not extractors.is_image("bild.heic")


# ---------------------------------------------------------------------------
# Bilder: Modellbeschreibung, Fallback mit Pillow-Massen, alte Office-Formate
# ---------------------------------------------------------------------------


def _testbild(tmp_path, name: str, size: tuple[int, int], color=(200, 30, 30)) -> Path:
    from PIL import Image

    path = tmp_path / name
    Image.new("RGB", size, color).save(path)
    return path


def test_extract_image_ohne_modell_fallback_mit_massen(tmp_path, monkeypatch):
    """Ohne Sprachmodell: Fallback-Text mit den Pillow-Massen, keine Exception."""
    monkeypatch.setenv("LLM_API_KEY", "")
    extractors._IMAGE_CACHE.clear()
    img = _testbild(tmp_path, "foto.png", (120, 80))
    text = extractors.extract_text_from_file(img, "foto.png")
    assert text == (
        "Bilddatei foto.png, 120×80 px. "
        "Kein Text extrahiert (Sprachmodell nicht erreichbar)."
    )


def test_extract_image_modellfehler_faellt_zurueck(tmp_path, monkeypatch):
    """Exception/Timeout im Modellaufruf: Fallback statt Traceback."""
    from app import llm

    monkeypatch.setenv("LLM_API_KEY", "test-key")
    extractors._IMAGE_CACHE.clear()

    def kaputt(data, mime, filename):
        raise TimeoutError("Request timed out")

    monkeypatch.setattr(llm, "describe_image", kaputt)
    img = _testbild(tmp_path, "scan.jpg", (64, 32), (10, 200, 10))
    text = extractors.extract_text_from_file(img, "scan.jpg")
    assert "Bilddatei scan.jpg, 64×32 px" in text
    assert "Kein Text extrahiert" in text


def test_extract_image_nutzt_modellbeschreibung_und_cache(tmp_path, monkeypatch):
    from app import llm

    monkeypatch.setenv("LLM_API_KEY", "test-key")
    extractors._IMAGE_CACHE.clear()
    aufrufe = []

    def beschreibe(data, mime, filename):
        aufrufe.append((mime, filename))
        return "Ein Organigramm mit drei Abteilungen."

    monkeypatch.setattr(llm, "describe_image", beschreibe)
    img = _testbild(tmp_path, "orga.webp", (40, 40), (0, 0, 250))
    assert extractors.extract_text_from_file(img, "orga.webp") == "Ein Organigramm mit drei Abteilungen."
    # zweiter Aufruf mit denselben Bytes (Prefill -> Upload): kein zweiter Modellaufruf
    assert extractors.extract_text_from_file(img, "orga.webp") == "Ein Organigramm mit drei Abteilungen."
    assert aufrufe == [("image/webp", "orga.webp")]


def test_alte_office_formate_geben_klare_meldung(tmp_path):
    """Echtes .doc/.xls koennen die Bibliotheken nicht lesen: Hinweis statt Traceback."""
    ole = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 64
    doc = tmp_path / "alt.doc"
    doc.write_bytes(ole)
    with pytest.raises(ValueError, match="DOCX"):
        extractors.extract_text_from_file(doc, "alt.doc")
    xls = tmp_path / "alt.xls"
    xls.write_bytes(ole)
    with pytest.raises(ValueError, match="XLSX"):
        extractors.extract_text_from_file(xls, "alt.xls")


def test_extract_image_modell_ohne_bild_faellt_zurueck(tmp_path, monkeypatch):
    """Proxy verschluckt das Bild, das Modell sagt "kein Bild uebermittelt": das ist
    keine Beschreibung, sondern der Fallback-Fall (Demo-Beobachtung hybridai.one)."""
    from app import llm

    monkeypatch.setenv("LLM_API_KEY", "test-key")
    extractors._IMAGE_CACHE.clear()
    antworten = [
        "Ich kann das Bild leider nicht sehen bzw. es wurde mir nicht übermittelt – mir liegt nur der Dateiname vor.",
        'Es tut mir leid, aber ich kann das Bild nicht sehen bzw. es wurde keine Bilddatei übermittelt.',
        "I'm sorry, I cannot see the image you are referring to.",
    ]
    for i, antwort in enumerate(antworten):
        monkeypatch.setattr(llm, "describe_image", lambda data, mime, filename, a=antwort: a)
        img = _testbild(tmp_path, f"tafel{i}.png", (50 + i, 20), (i * 40, 90, 10))
        text = extractors.extract_text_from_file(img, f"tafel{i}.png")
        assert text.startswith(f"Bilddatei tafel{i}.png, {50 + i}\u00d720 px"), text
    # echte Beschreibungen bleiben unangetastet
    assert not extractors.looks_like_no_image("Whiteboard mit der Ueberschrift 'Budget 2027: 1,2 Mio EUR'.")
    assert not extractors.looks_like_no_image("| Posten | Betrag |\n| --- | --- |\n| Lizenzen | 48.000 EUR |")
