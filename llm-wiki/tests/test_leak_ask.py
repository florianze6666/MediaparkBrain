"""US-7: Kein verbotener Text landet im LLM-Kontext oder in der Antwort."""
from __future__ import annotations

import pytest

from tests.conftest import FINANCE_TEXT, as_user

pytestmark = pytest.mark.security

# Charakteristische Woerter/Zahlen aus dem Finance-Text
FINANCE_MARKERS = ["48.000", "95.000", "220.000", "4711", "P-2026-031",
                   "Budgetantrag", "Budget Finance"]
QUESTION = "Wie hoch ist der Budgetantrag fuer den KI-Wissensassistent, Lizenzen Entwicklung Gesamt Kostenstelle?"


@pytest.fixture(autouse=True)
def no_api_key(monkeypatch):
    # Ohne Key gibt ask_llm den Kontext roh zurueck -> Leak waere im HTML sichtbar.
    # Leerer String statt delenv: load_dotenv() beim Import von app.main setzt
    # nur fehlende Variablen, ueberschreibt aber keine vorhandenen.
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")
    monkeypatch.delenv("ANTHROPIC_MODEL", raising=False)


def after_form(html: str) -> str:
    """Antwort + Quellen: alles nach dem Frage-Formular (die Frage selbst wird
    ins Eingabefeld zurueckgespiegelt und darf nicht als Leak zaehlen)."""
    return html.split('class="ask-form"', 1)[1].split("</form>", 1)[1]


def test_mitarbeiter_bekommt_nichts_aus_finance(client):
    r = client.post("/ask", cookies=as_user("mitarbeiter"), data={"question": QUESTION})
    assert r.status_code == 200
    assert "Suche als" in r.text and "Mitarbeiter" in r.text
    assert "Kein ANTHROPIC_API_KEY gesetzt" in r.text  # wirklich Roh-Kontext, kein LLM
    body = after_form(r.text)
    for marker in FINANCE_MARKERS:
        assert marker not in body, f"Leak: {marker!r} in Antwort fuer mitarbeiter"
    assert "budget-finance" not in r.text


def test_cfo_bekommt_finance(client):
    r = client.post("/ask", cookies=as_user("cfo"), data={"question": QUESTION})
    assert r.status_code == 200
    body = after_form(r.text)
    assert "Budget Finance" in body
    assert "220.000" in body and "4711" in body


def test_gast_bekommt_nur_oeffentliches(client):
    r = client.post("/ask", data={"question": "Wiki Gast lesen Budgetantrag Betriebsratssitzung Altbestand"})
    assert r.status_code == 200
    body = after_form(r.text)
    assert "Oeffentliche Testseite" in body
    for marker in FINANCE_MARKERS + ["Betriebsratssitzung", "Altbestand ohne Frontmatter"]:
        assert marker not in body


def test_search_snippets_filtert_vor_scoring(pages_env):
    import app.wiki as wiki

    # Frage ist wortwoertlich der Finance-Text -> Score waere 1.0, trotzdem kein Treffer
    snippets = wiki.search_snippets(FINANCE_TEXT, "mitarbeiter", top_k=50)
    assert all(s.page.slug != "budget-finance" for s in snippets)
    assert all(s.page.meta.domaene != "finance" for s in snippets)

    snippets = wiki.search_snippets(FINANCE_TEXT, "cfo", top_k=50)
    assert any(s.page.slug == "budget-finance" for s in snippets)

    # user ist Pflicht
    with pytest.raises(TypeError):
        wiki.search_snippets(FINANCE_TEXT)  # type: ignore[call-arg]


def test_ceo_findet_br_nicht(pages_env):
    import app.wiki as wiki

    snippets = wiki.search_snippets("Leistungskontrolle BetrVG Betriebsvereinbarung", "ceo", top_k=50)
    assert all(s.page.slug != "br-protokoll" for s in snippets)
    snippets = wiki.search_snippets("Leistungskontrolle BetrVG Betriebsvereinbarung", "betriebsrat", top_k=50)
    assert any(s.page.slug == "br-protokoll" for s in snippets)
