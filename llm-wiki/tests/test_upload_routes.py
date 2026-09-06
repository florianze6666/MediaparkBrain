from pathlib import Path
import pytest
from app import wiki
from tests.conftest import as_user

TEST_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "test project data"


def test_upload_form_get(client):
    # /upload zeigt jetzt die Kompass-Maske; die alte Maske liegt unter ?classic=1
    res = client.get("/upload?classic=1", cookies=as_user("projektmanager"))
    assert res.status_code == 200
    assert "Datei hochladen" in res.text
    assert "Unterstützte Formate" in res.text


def test_upload_docx_and_search(client, pages_env):
    docx_file = TEST_DATA_DIR / "Project_Charter_HARBOR_Logistics.docx"
    assert docx_file.exists()

    with open(docx_file, "rb") as f:
        file_bytes = f.read()

    res = client.post(
        "/upload",
        files={"file": ("Project_Charter_HARBOR_Logistics.docx", file_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        data={"vertraulichkeit": "intern", "domaene": "projekt"},
        cookies=as_user("projektmanager"),
    )
    assert res.status_code == 303
    redirect_url = res.headers["location"]
    assert "uploaded=1" in redirect_url

    # Seite laden
    page_res = client.get(redirect_url, cookies=as_user("projektmanager"))
    assert page_res.status_code == 200
    assert "Quelle: Upload" in page_res.text

    # Pruefen, dass die Seite als Such-Snippet fuer 'Companion' gefunden wird
    snippets = wiki.search_snippets("HARBOR", user="projektmanager")
    assert len(snippets) > 0
    assert any("HARBOR" in s.page.title or "HARBOR" in s.paragraph for s in snippets)


def test_upload_c_level_confidentiality_isolation(client, pages_env):
    # CEO laedt C-Level Dokument hoch
    text_content = b"Geheimer M&A Bericht: Uebernahme von Rothenberg fuer 25 Mio EUR."
    res = client.post(
        "/upload",
        files={"file": ("c_level_bericht.txt", text_content, "text/plain")},
        data={"vertraulichkeit": "C-Level", "domaene": "finance"},
        cookies=as_user("ceo"),
    )
    assert res.status_code == 303
    redirect_url = res.headers["location"]

    # CEO darf es lesen
    res_ceo = client.get(redirect_url, cookies=as_user("ceo"))
    assert res_ceo.status_code == 200

    # CFO darf es ebenfalls lesen (Gruppe finance/leitung)
    res_cfo = client.get(redirect_url, cookies=as_user("cfo"))
    assert res_cfo.status_code == 200

    # Normaler Mitarbeiter erhaelt 404 (US-8)
    res_mitarbeiter = client.get(redirect_url, cookies=as_user("mitarbeiter"))
    assert res_mitarbeiter.status_code == 404

    # Suche: Mitarbeiter findet nichts, CEO findet es
    assert len(wiki.search_snippets("Rothenberg", user="mitarbeiter")) == 0
    assert len(wiki.search_snippets("Rothenberg", user="ceo")) > 0


def test_api_extract_document_prepopulate(client):
    docx_file = TEST_DATA_DIR / "Project_Charter_HARBOR_Logistics.docx"
    assert docx_file.exists()

    with open(docx_file, "rb") as f:
        file_bytes = f.read()

    res = client.post(
        "/api/extract-document",
        files={"file": ("Project_Charter_HARBOR_Logistics.docx", file_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        cookies=as_user("projektmanager"),
    )
    assert res.status_code == 200
    data = res.json()
    assert "title" in data
    assert "content" in data
    assert "vertraulichkeit" in data
    assert "domaene" in data
    assert len(data["content"]) > 50


def test_upload_path_traversal_prevention(client, pages_env):
    """Path-Traversal im Dateinamen (z.B. ../, %2e%2e) darf nicht aus uploads_dir ausbrechen."""
    payload = b"Inhalt fuer Traversal Test"
    res = client.post(
        "/upload",
        files={"file": ("../../traversal-test.txt", payload, "text/plain")},
        data={"vertraulichkeit": "intern", "domaene": "projekt"},
        cookies=as_user("projektmanager"),
    )
    assert res.status_code == 303
    # Datei darf keinesfalls im Root oder ausserhalb von uploads/ liegen
    uploads_dir = wiki.uploads_dir()
    assert (uploads_dir / "projekt" / "traversal-test.txt").exists() or (uploads_dir / "traversal-test.txt").exists()
    root_traversal = uploads_dir.parent / "traversal-test.txt"
    assert not root_traversal.exists()


def test_guest_cannot_upload_or_extract(client, pages_env):
    """Gast darf weder ueber /upload noch /api/extract-document hochladen (403)."""
    payload = b"Gast Upload Versuch"
    # Ohne Cookie (Gast)
    res_upload = client.post(
        "/upload",
        files={"file": ("test.txt", payload, "text/plain")},
        data={"vertraulichkeit": "intern", "domaene": "allgemein"},
    )
    assert res_upload.status_code == 403

    res_extract = client.post(
        "/api/extract-document",
        files={"file": ("test.txt", payload, "text/plain")},
    )
    assert res_extract.status_code == 403


def test_foreign_domain_write_forbidden(client, pages_env):
    """Mitarbeiter darf nicht in fremde Domaene (z.B. finance) hochladen (Write ⊆ Read)."""
    payload = b"Injektion in Finance"
    res = client.post(
        "/upload",
        files={"file": ("finance_inj.txt", payload, "text/plain")},
        data={"vertraulichkeit": "intern", "domaene": "finance"},
        cookies=as_user("mitarbeiter"),
    )
    assert res.status_code == 403


def test_betriebsrat_intern_normalization(client, pages_env):
    """Betriebsrat-intern wird zu vertraulich mit empfaenger=[br] normalisiert."""
    payload = b"Vertrauliche Notiz des Betriebsrats."
    res = client.post(
        "/upload",
        files={"file": ("br_notiz.txt", payload, "text/plain")},
        data={"vertraulichkeit": "Betriebsrat-intern", "domaene": "br"},
        cookies=as_user("betriebsrat"),
    )
    assert res.status_code == 303
    redirect_url = res.headers["location"]

    # Betriebsrat darf lesen
    assert client.get(redirect_url, cookies=as_user("betriebsrat")).status_code == 200
    # CEO darf BR-intern NICHT lesen (404)
    assert client.get(redirect_url, cookies=as_user("ceo")).status_code == 404




# ---------------------------------------------------------------------------
# Kompass-Upload (/api/prefill + POST /upload?target=knowledge)
# ---------------------------------------------------------------------------

import struct
import zlib

from app import main as app_main


def _png_bytes() -> bytes:
    """Kleinstes gueltiges PNG (1x1, RGBA)."""
    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
    idat = zlib.compress(b"\x00\x00\x00\x00\xff")
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


def test_api_prefill_sees_the_uploaded_file(client, monkeypatch):
    """request.form() liefert starlette-UploadFiles - die Datei darf nicht unter
    den Tisch fallen (frueher: Titel 'eingabe', Dokumenttyp 'Dokument')."""
    monkeypatch.setenv("LLM_API_KEY", "")  # kein Modell -> Fallback aus dem Dateinamen
    docx_file = TEST_DATA_DIR / "Project_Charter_HARBOR_Logistics.docx"
    res = client.post(
        "/api/prefill?target=knowledge",
        files={"files": (docx_file.name, docx_file.read_bytes(),
                         "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        cookies=as_user("cfo"),
    )
    assert res.status_code == 200
    fields = res.json()["fields"]
    assert fields["titel"] != "eingabe"
    assert "HARBOR" in fields["titel"]
    assert "empfaenger" in fields


def test_api_prefill_image_fields_from_filename(client, monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "")
    res = client.post(
        "/api/prefill?target=knowledge",
        files={"files": ("Messe_Stand-2026.png", _png_bytes(), "image/png")},
        cookies=as_user("cfo"),
    )
    assert res.status_code == 200
    fields = res.json()["fields"]
    assert fields["titel"] == "Messe Stand 2026"
    assert fields["dokumenttyp"] == "Bild"
    assert fields["datum"]


def test_parse_json_object_strips_fences_and_prose():
    raw = 'Klar:\n```json\n{"name": "X", "cost": null}\n```\nFertig.'
    assert app_main._parse_json_object(raw) == {"name": "X", "cost": None}
    with pytest.raises(ValueError):
        app_main._parse_json_object("kein json")


def test_kompass_upload_vertraulich_with_recipients(client, pages_env, monkeypatch):
    """Vorpruefung mit Ersteller + Empfaengern: cfo darf vertraulich in finance anlegen."""
    monkeypatch.setenv("LLM_API_KEY", "")
    res = client.post(
        "/upload",
        files={"files": ("Budget_2027.txt", b"Vertrauliches Budget 2027: 1,2 Mio EUR.", "text/plain")},
        data={"target": "knowledge", "titel": "Budget 2027", "domaene": "finance",
              "vertraulichkeit": "vertraulich", "empfaenger": "gf, finance",
              "dokumenttyp": "Business Case", "datum": "2026-09-06", "verfasser": "cfo"},
        cookies=as_user("cfo"),
    )
    assert res.status_code == 200
    assert "kp-burst" in res.text  # saved-Ansicht

    page_file = pages_env / "finance" / "vertraulich" / "budget-2027.md"
    assert page_file.is_file()
    page = wiki.get_page("budget-2027")
    assert page.meta.empfaenger == ["gf", "finance"]
    assert page.meta.erstellt_von == "cfo"
    assert page.meta.original_datei == "Budget_2027.txt"
    assert (wiki.uploads_dir() / "finance" / "Budget_2027.txt").is_file()

    assert client.get("/knowledge/budget-2027", cookies=as_user("cfo")).status_code == 200
    assert client.get("/knowledge/budget-2027", cookies=as_user("ceo")).status_code == 200  # gf
    assert client.get("/knowledge/budget-2027", cookies=as_user("mitarbeiter")).status_code == 404


def test_kompass_upload_png_creates_page_with_original(client, pages_env, monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "")
    res = client.post(
        "/upload",
        files={"files": ("Organigramm.png", _png_bytes(), "image/png")},
        data={"target": "knowledge", "titel": "Organigramm", "domaene": "finance",
              "vertraulichkeit": "intern", "dokumenttyp": "Bild"},
        cookies=as_user("cfo"),
    )
    assert res.status_code == 200
    page = wiki.get_page("organigramm")
    assert page is not None
    assert "![Organigramm](/knowledge/organigramm/original)" in page.content
    assert "Original: [Organigramm.png](/knowledge/organigramm/original)" in page.content
    assert "Kein Text extrahiert" in page.content  # kein OCR ohne Modell, Original haengt an
    assert page.meta.original_datei == "Organigramm.png"

    view = client.get("/knowledge/organigramm", cookies=as_user("cfo"))
    assert view.status_code == 200
    assert "/knowledge/organigramm/original" in view.text
    assert "Original öffnen" in view.text

    original = client.get("/knowledge/organigramm/original", cookies=as_user("cfo"))
    assert original.status_code == 200
    assert original.headers["content-type"].startswith("image/png")
    assert original.content == _png_bytes()

    # security: ohne Leserecht auf finance gibt es auch das Original nicht (404)
    assert client.get("/knowledge/organigramm/original", cookies=as_user("mitarbeiter")).status_code == 404
    assert client.get("/knowledge/organigramm/original").status_code == 404


def test_knowledge_original_traversal_name_is_404(client, pages_env):
    """Ein Pfad in original_datei darf nie aus uploads/ ausbrechen (security)."""
    from app.access import PageMeta

    secret = wiki.uploads_dir().parent / "secret.txt"
    secret.write_text("geheim", encoding="utf-8")
    wiki.save_page(
        "boese-seite", "Boese Seite", "x",
        PageMeta(erstellt_von="cfo", vertraulichkeit="intern", domaene="finance",
                 original_datei="../secret.txt"),
    )
    assert client.get("/knowledge/boese-seite/original", cookies=as_user("cfo")).status_code == 404
    # Seite ohne Original: ebenfalls 404
    assert client.get("/knowledge/budget-finance/original", cookies=as_user("cfo")).status_code == 404


# ---------------------------------------------------------------------------
# Demo-Modus: JPG ueber den Kompass-Weg, lesbare Fehler, Titel/Slug-Fallbacks
# ---------------------------------------------------------------------------


def _jpg_bytes(size=(300, 200)) -> bytes:
    import io

    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", size, (10, 120, 200)).save(buf, "JPEG")
    return buf.getvalue()


def test_kompass_upload_jpg_seite_und_original(client, pages_env, monkeypatch):
    """JPG ueber den Kompass-Weg: Seite in pages/<domaene>/, Original in uploads/<domaene>/,
    Original-Link oben im Inhalt, Original nur fuer Berechtigte (security)."""
    monkeypatch.setenv("LLM_API_KEY", "")
    res = client.post(
        "/upload",
        files={"files": ("Whiteboard_Foto.jpg", _jpg_bytes(), "image/jpeg")},
        data={"target": "knowledge", "titel": "Whiteboard", "domaene": "projekt",
              "vertraulichkeit": "intern"},
        cookies=as_user("projektmanager"),
    )
    assert res.status_code == 200
    assert 'href="/knowledge/whiteboard"' in res.text  # Link zur neuen Seite in der saved-Ansicht
    assert (pages_env / "projekt" / "whiteboard.md").is_file()
    assert (wiki.uploads_dir() / "projekt" / "Whiteboard_Foto.jpg").is_file()

    page = wiki.get_page("whiteboard")
    assert page.meta.original_datei == "Whiteboard_Foto.jpg"
    assert page.content.startswith("Original: [Whiteboard_Foto.jpg](/knowledge/whiteboard/original)")
    assert "300×200 px" in page.content

    # projekt liest jeder Angemeldete
    assert client.get("/knowledge/whiteboard", cookies=as_user("mitarbeiter")).status_code == 200
    orig = client.get("/knowledge/whiteboard/original", cookies=as_user("mitarbeiter"))
    assert orig.status_code == 200
    assert orig.headers["content-type"].startswith("image/jpeg")
    assert orig.content == _jpg_bytes()
    # security: Gast (keine Gruppen) sieht weder Seite noch Original
    assert client.get("/knowledge/whiteboard").status_code == 404
    assert client.get("/knowledge/whiteboard/original").status_code == 404


def test_kompass_upload_fehler_lesbar_titel_aus_dateiname_slug_frei(client, pages_env, monkeypatch):
    """Kompass-Weg: Fehler als Meldung in der Maske (Formular bleibt), nie nackte 403/500."""
    monkeypatch.setenv("LLM_API_KEY", "")
    # keine Datei
    r = client.post("/upload", data={"target": "knowledge"}, cookies=as_user("cfo"))
    assert r.status_code == 400
    assert "Bitte zuerst eine Datei ablegen" in r.text and 'id="kp-upload"' in r.text

    # fremde Domaene: Meldung in der Maske, Status 403, keine Datei geschrieben
    r = client.post(
        "/upload",
        files={"files": ("x.txt", b"abc", "text/plain")},
        data={"target": "knowledge", "domaene": "finance"},
        cookies=as_user("mitarbeiter"),
    )
    assert r.status_code == 403
    assert "kp-upload-error" in r.text and 'id="kp-upload"' in r.text
    assert not (wiki.uploads_dir() / "finance" / "x.txt").exists()

    # altes .doc: klare Meldung statt Traceback
    r = client.post(
        "/upload",
        files={"files": ("alt.doc", b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 64,
                         "application/msword")},
        data={"target": "knowledge", "domaene": "projekt"},
        cookies=as_user("cfo"),
    )
    assert r.status_code == 400 and "DOCX" in r.text and 'id="kp-upload"' in r.text

    # Titel leer -> aus dem Dateinamen; zweiter Upload -> Slug -2 statt Abbruch
    for _ in range(2):
        r = client.post(
            "/upload",
            files={"files": ("Protokoll_KW36.txt", b"Inhalt der Sitzung.", "text/plain")},
            data={"target": "knowledge", "titel": "", "domaene": "projekt"},
            cookies=as_user("cfo"),
        )
        assert r.status_code == 200
    assert wiki.get_page("protokoll-kw36").title == "Protokoll KW36"
    assert wiki.get_page("protokoll-kw36-2") is not None
    assert (pages_env / "projekt" / "protokoll-kw36.md").is_file()
