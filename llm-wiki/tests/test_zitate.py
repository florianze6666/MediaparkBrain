"""Quellenzitat zu jeder Antwort (Paket 10).

Schwerpunkt ist die Zitatpruefung: Ein Zitat darf nur als Beleg erscheinen,
wenn es woertlich in der Wissensbasis steht. Alles andere waere eine huebsch
gerahmte Halluzination.
"""
from __future__ import annotations

import json

import pytest

from app import llm, wiki
from app.access import PageMeta

KONTEXT = (
    "Die einmaligen Kosten des Projekts CONI liegen bei 450 TEUR. "
    "Die laufenden Kosten betragen 90 TEUR pro Jahr."
)
PDF_ABSATZ = "*(Seite 7)* Total One-Off 450 TEUR · Avg Recurrent 90 TEUR"


def _snippet(slug: str, titel: str, absatz: str, score: float = 1.0) -> wiki.Snippet:
    seite = wiki.Page(slug=slug, title=titel, content=absatz, meta=PageMeta())
    return wiki.Snippet(page=seite, paragraph=absatz, score=score)


@pytest.fixture
def snippets() -> list[wiki.Snippet]:
    return [
        _snippet("business-case", "Business Case CONI", KONTEXT),
        _snippet("vorstellung", "Projektvorstellung CONI", PDF_ABSATZ),
    ]


@pytest.fixture
def mit_key(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "test-key")


def _antwort_des_modells(monkeypatch, fakten: list[dict], roh: str | None = None) -> None:
    """Ersetzt den einzigen Aufruf nach aussen."""
    text = roh if roh is not None else json.dumps({"fakten": fakten}, ensure_ascii=False)
    monkeypatch.setattr(llm, "_modell_fragen", lambda frage, kontext: text)


# ---------------------------------------------------------------------------
# Der Kern: woertlich oder gar nicht
# ---------------------------------------------------------------------------


def test_woertliches_zitat_wird_belegt(mit_key, monkeypatch, snippets):
    _antwort_des_modells(monkeypatch, [
        {"aussage": "Die einmaligen Kosten liegen bei 450 TEUR.",
         "zitat": "Die einmaligen Kosten des Projekts CONI liegen bei 450 TEUR."},
    ])

    antwort = llm.ask_llm("Was kostet CONI einmalig?", snippets)

    assert len(antwort.belegte) == 1
    fakt = antwort.belegte[0]
    assert fakt.quelle_titel == "Business Case CONI"
    assert fakt.quelle_slug == "business-case"


def test_umformuliertes_zitat_gilt_nicht_als_beleg(mit_key, monkeypatch, snippets):
    """Der wichtigste Test: nah dran ist nicht woertlich."""
    _antwort_des_modells(monkeypatch, [
        {"aussage": "Die einmaligen Kosten liegen bei 450 TEUR.",
         "zitat": "Die einmaligen Kosten von CONI belaufen sich auf 450 TEUR."},
    ])

    antwort = llm.ask_llm("Was kostet CONI?", snippets)

    assert antwort.belegte == []
    assert len(antwort.unbelegte) == 1
    # Die Aussage verschwindet nicht, sie wird nur nicht als belegt ausgegeben
    assert antwort.unbelegte[0].aussage == "Die einmaligen Kosten liegen bei 450 TEUR."
    assert antwort.unbelegte[0].zitat == ""
    assert "nicht mit einem woertlichen Zitat" in antwort.hinweis


def test_frei_erfundenes_zitat_gilt_nicht_als_beleg(mit_key, monkeypatch, snippets):
    _antwort_des_modells(monkeypatch, [
        {"aussage": "Das Projekt wurde vom Vorstand freigegeben.",
         "zitat": "Der Vorstand hat das Projekt am 12. Maerz freigegeben."},
    ])

    antwort = llm.ask_llm("Wurde CONI freigegeben?", snippets)

    assert antwort.belegte == []
    assert antwort.unbelegte[0].belegt is False


def test_zu_kurzes_zitat_belegt_nichts(mit_key, monkeypatch, snippets):
    """"450" steht in jedem Zahlenwerk und wuerde zufaellig irgendwo passen."""
    _antwort_des_modells(monkeypatch, [
        {"aussage": "Die Kosten liegen bei 450 TEUR.", "zitat": "450"},
    ])

    antwort = llm.ask_llm("Was kostet CONI?", snippets)

    assert antwort.belegte == []


@pytest.mark.parametrize("einzelwort", ["Betriebsrat", "CFO/Controlling", "Cybersecurity-Agent"])
def test_einzelnes_wort_belegt_keine_aussage(mit_key, monkeypatch, einzelwort):
    """Gemessen wird in Woertern, nicht in Zeichen.

    Eine Zeichengrenze trennt willkuerlich: "CFO/Controlling" haette sie
    bestanden, "CEO/Strategie" nicht - obwohl beide gleich wenig belegen.
    Erst der Satz, in dem das Wort steht, traegt die Aussage.
    """
    absatz = (
        "Das System nutzt vier Stakeholder-Agenten: Betriebsrat, CFO/Controlling, "
        "IT/Architektur/Cybersecurity und CEO/Strategie."
    )
    treffer = [_snippet("agenten", "Vier Experten-Agenten", absatz)]
    _antwort_des_modells(monkeypatch, [
        {"aussage": f"{einzelwort} ist einer der vier Agenten.", "zitat": einzelwort},
    ])

    assert llm.ask_llm("Welche Agenten?", treffer).belegte == []


def test_der_ganze_satz_belegt_die_aussage(mit_key, monkeypatch):
    """Die Gegenprobe: mit dem vollstaendigen Satz gilt derselbe Fakt als belegt."""
    absatz = (
        "Das System nutzt vier Stakeholder-Agenten: Betriebsrat, CFO/Controlling, "
        "IT/Architektur/Cybersecurity und CEO/Strategie."
    )
    treffer = [_snippet("agenten", "Vier Experten-Agenten", absatz)]
    _antwort_des_modells(monkeypatch, [
        {"aussage": "Der Betriebsrat ist einer der vier Agenten.", "zitat": absatz},
    ])

    assert len(llm.ask_llm("Welche Agenten?", treffer).belegte) == 1


def test_zeilenumbruch_entwertet_einen_beleg_nicht(mit_key, monkeypatch, snippets):
    """Nur Leerraum und Gross-/Kleinschreibung werden geglaettet."""
    _antwort_des_modells(monkeypatch, [
        {"aussage": "Einmalig 450 TEUR.",
         "zitat": "Die einmaligen Kosten des Projekts CONI\n   liegen bei 450 TEUR."},
    ])

    antwort = llm.ask_llm("Was kostet CONI?", snippets)

    assert len(antwort.belegte) == 1


# ---------------------------------------------------------------------------
# Belegstelle und Verlinkung
# ---------------------------------------------------------------------------


def test_seitenzahl_aus_pdf_wird_als_belegstelle_uebernommen(mit_key, monkeypatch, snippets):
    _antwort_des_modells(monkeypatch, [
        {"aussage": "Die laufenden Kosten betragen 90 TEUR.",
         "zitat": "Total One-Off 450 TEUR · Avg Recurrent 90 TEUR"},
    ])

    fakt = llm.ask_llm("Was sind die laufenden Kosten?", snippets).belegte[0]

    assert fakt.belegstelle == "Seite 7"
    assert fakt.quelle_slug == "vorstellung"


def test_ohne_pdf_herkunft_keine_belegstelle(mit_key, monkeypatch, snippets):
    _antwort_des_modells(monkeypatch, [
        {"aussage": "Einmalig 450 TEUR.",
         "zitat": "Die einmaligen Kosten des Projekts CONI liegen bei 450 TEUR."},
    ])

    assert llm.ask_llm("?", snippets).belegte[0].belegstelle == ""


# ---------------------------------------------------------------------------
# Rechte: belegt wird nur gegen die uebergebenen Snippets
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_zitat_aus_einer_nicht_uebergebenen_seite_wird_verworfen(mit_key, monkeypatch, snippets):
    """`search_snippets` filtert nach Rechten - hier darf nichts vorbeikommen."""
    verboten = "Der Betriebsrat lehnt die Leistungskontrolle ausdruecklich ab."
    _antwort_des_modells(monkeypatch, [
        {"aussage": "Der Betriebsrat ist dagegen.", "zitat": verboten},
    ])

    antwort = llm.ask_llm("Was sagt der Betriebsrat?", snippets)

    assert antwort.belegte == []
    assert verboten not in (antwort.unbelegte[0].zitat or "")


@pytest.mark.security
def test_ende_zu_ende_nur_erlaubte_seiten_werden_zitiert(pages_env, mit_key, monkeypatch):
    """Ein Mitarbeiter darf Finance nicht sehen - also auch nicht daraus zitieren."""
    treffer = wiki.search_snippets("Lizenzen Kostenstelle", "mitarbeiter")
    assert all(s.page.meta.domaene != "finance" for s in treffer)

    _antwort_des_modells(monkeypatch, [
        {"aussage": "Die Lizenzen kosten 48.000 EUR.",
         "zitat": "Lizenzen 48.000 EUR, externe Entwicklung 95.000 EUR"},
    ])
    antwort = llm.ask_llm("Was kosten die Lizenzen?", treffer)

    assert antwort.belegte == []


# ---------------------------------------------------------------------------
# Randfaelle
# ---------------------------------------------------------------------------


def test_ohne_treffer_gibt_es_einen_hinweis_statt_fakten(mit_key):
    antwort = llm.ask_llm("Gibt es Einhoerner?", [])
    assert antwort.fakten == []
    assert "nichts im Wiki" in antwort.hinweis


def test_ohne_api_key_gibt_es_belege_ohne_aussagen(monkeypatch, snippets):
    monkeypatch.delenv("LLM_API_KEY", raising=False)

    antwort = llm.ask_llm("Was kostet CONI?", snippets)

    assert len(antwort.fakten) == 2
    assert all(f.belegt for f in antwort.fakten)
    assert all(f.aussage == "" for f in antwort.fakten)
    assert "LLM_API_KEY" in antwort.hinweis


def test_json_im_codeblock_wird_gelesen(mit_key, monkeypatch, snippets):
    roh = (
        "Hier ist das Ergebnis:\n```json\n"
        + json.dumps({"fakten": [{
            "aussage": "Einmalig 450 TEUR.",
            "zitat": "Die einmaligen Kosten des Projekts CONI liegen bei 450 TEUR.",
        }]}, ensure_ascii=False)
        + "\n```"
    )
    _antwort_des_modells(monkeypatch, [], roh=roh)

    assert len(llm.ask_llm("?", snippets).belegte) == 1


def test_unlesbares_format_geht_nicht_verloren_gilt_aber_als_unbelegt(mit_key, monkeypatch, snippets):
    _antwort_des_modells(monkeypatch, [], roh="Das kostet 450 TEUR einmalig.")

    antwort = llm.ask_llm("?", snippets)

    assert antwort.belegte == []
    assert antwort.fakten[0].aussage == "Das kostet 450 TEUR einmalig."
    assert "unerwartetem Format" in antwort.hinweis


def test_fakten_ohne_aussage_werden_verworfen(mit_key, monkeypatch, snippets):
    _antwort_des_modells(monkeypatch, [
        {"aussage": "", "zitat": "Die einmaligen Kosten des Projekts CONI liegen bei 450 TEUR."},
        {"aussage": "Einmalig 450 TEUR.",
         "zitat": "Die einmaligen Kosten des Projekts CONI liegen bei 450 TEUR."},
    ])

    assert len(llm.ask_llm("?", snippets).fakten) == 1


def test_chatbot_id_nur_wenn_gesetzt(monkeypatch):
    """Das anbieterspezifische Feld darf nur mitgehen, wenn es konfiguriert ist -
    sonst wuerde ein reiner OpenAI-Endpoint ein unbekanntes Feld sehen."""
    monkeypatch.delenv("LLM_CHATBOT_ID", raising=False)
    assert llm._extra_body() == {}

    monkeypatch.setenv("LLM_CHATBOT_ID", "  cb-42  ")
    assert llm._extra_body() == {"chatbot_id": "cb-42"}

    monkeypatch.setenv("LLM_CHATBOT_ID", "   ")
    assert llm._extra_body() == {}
