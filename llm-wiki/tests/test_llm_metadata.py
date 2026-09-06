"""Modellantworten fuer den Dokumentkopf: Code-Zaeune, Frontmatter-Schnitt, Fallback mit Log."""
from __future__ import annotations

import logging

from app import llm_metadata

FENCED_RESPONSE = """Hier ist der Dokumentkopf:

```yaml
---
doc_id: "LTT-2026-0906-PMO-001"
titel: "Project Charter HARBOR: Logistik-Plattform"
dokumenttyp: "Projektsteckbrief"
datum: "2026-09-01"
verfasser: "Maria Muster"
rolle: "Projektleitung"
organisationseinheit: "PMO"
empfaenger: []
projekt: "HARBOR"
geschaeftsbereich: "Logistics"
vertraulichkeit: "C-Level"
informationsdomaene: [projekt]
ablageort: "projektlaufwerk"
erstellt_von: "irgendwer"
erstellt_am: "2000-01-01T00:00:00"
quelle: "upload"
original_datei: "x.docx"
---
# Project Charter HARBOR: Logistik-Plattform

**Lahnberg Thermotechnik GmbH & Co. KG** - PMO
```
"""


def test_strip_code_fences_keeps_content_in_order():
    out = llm_metadata.strip_code_fences("vorher\n```yaml\n---\na: 1\n---\n```\nnachher")
    assert "```" not in out
    assert out.splitlines()[0] == "vorher" and out.splitlines()[-1] == "nachher"
    assert "---\na: 1\n---" in out


def test_extract_frontmatter_cuts_between_first_two_delimiters():
    fm, rest = llm_metadata.extract_frontmatter("intro\n---\ntitel: x\n---\n# X\n---\nmehr")
    assert fm == "titel: x"
    assert rest.startswith("# X")
    assert llm_metadata.extract_frontmatter("kein frontmatter ---") is None


def test_generate_header_parses_fenced_yaml(monkeypatch):
    monkeypatch.setattr(llm_metadata, "is_configured", lambda: True)
    monkeypatch.setattr(llm_metadata, "llm_chat", lambda *a, **k: FENCED_RESPONSE)

    header, meta, title = llm_metadata.generate_header("Projektsteckbrief HARBOR ...", "x.docx", "cfo")

    assert title == "Project Charter HARBOR: Logistik-Plattform"
    assert meta.dokumenttyp == "Projektsteckbrief"
    assert meta.verfasser == "Maria Muster"
    # Systemfelder werden ueberschrieben, Korpus-Stufe wird uebersetzt
    assert meta.erstellt_von == "cfo"
    assert meta.vertraulichkeit == "vertraulich"
    assert meta.empfaenger == ["gf", "finance"]
    assert "```" not in header and header.startswith("---")


def test_generate_header_logs_and_falls_back_on_garbage(monkeypatch, caplog):
    monkeypatch.setattr(llm_metadata, "is_configured", lambda: True)
    monkeypatch.setattr(llm_metadata, "llm_chat", lambda *a, **k: "Sorry, kann ich nicht.")

    with caplog.at_level(logging.WARNING, logger="app.llm_metadata"):
        _, meta, title = llm_metadata.generate_header("Text", "Mein_Dokument.pdf", "cfo")

    assert title == "Mein Dokument"  # Fallback aus dem Dateinamen
    assert meta.dokumenttyp == "Dokument"
    assert any("Fallback" in r.getMessage() and "Sorry" in r.getMessage() for r in caplog.records)


def test_generate_header_logs_when_llm_raises(monkeypatch, caplog):
    def boom(*a, **k):
        raise RuntimeError("Timeout")

    monkeypatch.setattr(llm_metadata, "is_configured", lambda: True)
    monkeypatch.setattr(llm_metadata, "llm_chat", boom)
    with caplog.at_level(logging.WARNING, logger="app.llm_metadata"):
        _, _, title = llm_metadata.generate_header("Text", "Notiz.txt", "cfo")
    assert title == "Notiz"
    assert any("Timeout" in r.getMessage() for r in caplog.records)
