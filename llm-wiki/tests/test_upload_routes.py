from pathlib import Path
import pytest
from app import wiki
from tests.conftest import as_user

TEST_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "test project data"


def test_upload_form_get(client):
    res = client.get("/upload", cookies=as_user("projektmanager"))
    assert res.status_code == 200
    assert "Datei hochladen" in res.text
    assert "Unterstützte Formate" in res.text


def test_upload_docx_and_search(client, pages_env):
    docx_file = TEST_DATA_DIR / "__Project_Charter_M-Companion_anonymisiert 1.docx"
    assert docx_file.exists()

    with open(docx_file, "rb") as f:
        file_bytes = f.read()

    res = client.post(
        "/upload",
        files={"file": ("Project_Charter_M_Companion.docx", file_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
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
    snippets = wiki.search_snippets("Companion", user="projektmanager")
    assert len(snippets) > 0
    assert any("Companion" in s.page.title or "Companion" in s.paragraph for s in snippets)


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
    docx_file = TEST_DATA_DIR / "__Project_Charter_M-Companion_anonymisiert 1.docx"
    assert docx_file.exists()

    with open(docx_file, "rb") as f:
        file_bytes = f.read()

    res = client.post(
        "/api/extract-document",
        files={"file": ("Project_Charter_M_Companion.docx", file_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        cookies=as_user("projektmanager"),
    )
    assert res.status_code == 200
    data = res.json()
    assert "title" in data
    assert "content" in data
    assert "vertraulichkeit" in data
    assert "domaene" in data
    assert len(data["content"]) > 50

