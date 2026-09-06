"""Die Kompass-Suchleiste ist zugleich "Frag das Wiki".

Vor dieser Aenderung lieferte /search nur eine Trefferliste: keine Antwort,
kein Zitat. Die Tests halten fest, dass aus derselben Leiste jetzt eine
belegte Antwort kommt - und dass der Rechte-Filter dabei wirksam bleibt.
"""
from __future__ import annotations

import json

import pytest

from app import llm
from tests.conftest import as_user


@pytest.fixture
def mit_key(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "test-key")


def _antwort_des_modells(monkeypatch, fakten: list[dict]) -> None:
    """Ersetzt den einzigen Aufruf nach aussen."""
    text = json.dumps({"fakten": fakten}, ensure_ascii=False)
    monkeypatch.setattr(llm, "_modell_fragen", lambda frage, kontext: text)


# ---------------------------------------------------------------------------
# Die Leiste beantwortet, statt nur zu listen
# ---------------------------------------------------------------------------


def test_suche_liefert_eine_antwort_mit_zitat(client, mit_key, monkeypatch):
    _antwort_des_modells(monkeypatch, [
        {"aussage": "Die Lizenzen kosten 48.000 EUR.",
         "zitat": "Budgetantrag KI-Wissensassistent: Lizenzen 48.000 EUR"},
    ])

    r = client.get("/search", params={"q": "Lizenzen Kostenstelle"}, cookies=as_user("cfo"))

    assert r.status_code == 200
    assert "Die Lizenzen kosten 48.000 EUR." in r.text
    assert "kp-zitat" in r.text, "die Zitatbox fehlt"
    assert "Lizenzen 48.000 EUR" in r.text


def test_zitat_verlinkt_die_quellseite(client, mit_key, monkeypatch):
    _antwort_des_modells(monkeypatch, [
        {"aussage": "Die Lizenzen kosten 48.000 EUR.",
         "zitat": "Budgetantrag KI-Wissensassistent: Lizenzen 48.000 EUR"},
    ])

    r = client.get("/search", params={"q": "Lizenzen Kostenstelle"}, cookies=as_user("cfo"))

    assert '/knowledge/budget-finance' in r.text


def test_unbelegte_aussage_wird_als_solche_gekennzeichnet(client, mit_key, monkeypatch):
    """Eine huebsche Box um eine Halluzination waere schlimmer als keine Box."""
    _antwort_des_modells(monkeypatch, [
        {"aussage": "Der Vorstand hat das Projekt freigegeben.",
         "zitat": "Der Vorstand hat am 12. Maerz zugestimmt."},
    ])

    r = client.get("/search", params={"q": "Lizenzen Kostenstelle"}, cookies=as_user("cfo"))

    assert "Ohne Beleg" in r.text
    assert "Der Vorstand hat am 12. Maerz zugestimmt." not in r.text


def test_ohne_suchbegriff_keine_antwort(client, mit_key, monkeypatch):
    monkeypatch.setattr(llm, "_modell_fragen", lambda frage, kontext: pytest.fail(
        "ohne Suchbegriff darf das Modell nicht gefragt werden"))

    r = client.get("/search", cookies=as_user("cfo"))

    assert r.status_code == 200
    assert "kp-zitat" not in r.text


def test_ohne_treffer_gibt_es_einen_hinweis(client, mit_key, monkeypatch):
    _antwort_des_modells(monkeypatch, [])

    r = client.get("/search", params={"q": "einhornzuechterei"}, cookies=as_user("cfo"))

    assert "nichts im Wiki" in r.text


def test_ohne_api_key_bleiben_die_belegstellen(client, monkeypatch):
    """Die Seite bleibt nutzbar: Belege ja, formulierte Antwort nein."""
    monkeypatch.delenv("LLM_API_KEY", raising=False)

    r = client.get("/search", params={"q": "Lizenzen Kostenstelle"}, cookies=as_user("cfo"))

    assert r.status_code == 200
    assert "LLM_API_KEY" in r.text
    assert "Lizenzen 48.000 EUR" in r.text


# ---------------------------------------------------------------------------
# Rechte bleiben wirksam - auch fuer die Zitattexte
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_mitarbeiter_bekommt_kein_zitat_aus_finance(client, mit_key, monkeypatch):
    """Belegt wird nur gegen die Treffer, und die sind bereits gefiltert."""
    _antwort_des_modells(monkeypatch, [
        {"aussage": "Die Lizenzen kosten 48.000 EUR.",
         "zitat": "Budgetantrag KI-Wissensassistent: Lizenzen 48.000 EUR"},
    ])

    r = client.get("/search", params={"q": "Lizenzen Kostenstelle"},
                   cookies=as_user("mitarbeiter"))

    assert r.status_code == 200
    assert "48.000 EUR" not in r.text
    assert "budget-finance" not in r.text


@pytest.mark.security
def test_gast_bekommt_kein_zitat_aus_dem_betriebsrat(client, mit_key, monkeypatch):
    _antwort_des_modells(monkeypatch, [
        {"aussage": "Es gibt eine Loeschfrist.",
         "zitat": "Betriebsratssitzung: Leistungskontrolle nach BetrVG, Loeschfrist 30 Tage"},
    ])

    r = client.get("/search", params={"q": "Loeschfrist Leistungskontrolle"},
                   cookies=as_user("gast"))

    assert "Loeschfrist 30 Tage" not in r.text
