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
