"""Projektbewertung (/proposals/evaluate): Rechte-Filter und robuste Fehlerbehandlung.

Vorher brach die Seite mit HTTP 500 ab, sobald der LLM-Aufruf scheiterte
(ungueltiger Key, unbekanntes Modell, Netzfehler), und bewertete ungefiltert
auch Vorschlaege, die der Nutzer gar nicht lesen darf.
"""
from __future__ import annotations

import json

import httpx
import pytest

from tests.conftest import as_user

pytestmark = pytest.mark.security


def _submit(client, user, name, vertraulichkeit="intern", empfaenger=""):
    return client.post("/proposals/new", cookies=as_user(user), data={
        "project_name": name, "description": "Beschreibung von " + name,
        "domaene": "projekt", "vertraulichkeit": vertraulichkeit, "empfaenger": empfaenger,
    })


def _fake_evaluation():
    ok = {"status": "BEWERTET", "score": 8, "begruendung": "passt", "fehlende_informationen": []}
    return {"betriebsrat": ok, "cfo": ok, "it": ok, "ceo": ok}


def _api_error(status: int) -> Exception:
    """Erzeugt die passende anthropic-Exception fuer einen HTTP-Status."""
    import anthropic

    request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    response = httpx.Response(status, request=request, json={"error": {"message": "x"}})
    klasse = {
        401: anthropic.AuthenticationError,
        404: anthropic.NotFoundError,
        429: anthropic.RateLimitError,
    }[status]
    return klasse(message="x", response=response, body=None)


def _raise(err: Exception):
    def fake_ask(model, proposal):
        raise err
    return fake_ask


def test_seite_ohne_api_key_zeigt_hinweis_statt_500(client, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert _submit(client, "projektmanager", "Portal").status_code == 303
    r = client.get("/proposals/evaluate", cookies=as_user("projektmanager"))
    assert r.status_code == 200
    assert "Kein ANTHROPIC_API_KEY gesetzt" in r.text
    assert "Bewertung nicht möglich" in r.text


@pytest.mark.parametrize("status, erwartet", [
    (401, "ANTHROPIC_API_KEY wird vom Anbieter abgelehnt"),
    (404, "nicht verfuegbar"),
    (429, "Rate-Limit"),
])
def test_api_fehler_landet_auf_der_seite_statt_500(client, monkeypatch, status, erwartet):
    import app.evaluation as evaluation

    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setattr(evaluation, "_ask_model", _raise(_api_error(status)))
    assert _submit(client, "projektmanager", "Portal").status_code == 303
    r = client.get("/proposals/evaluate", cookies=as_user("projektmanager"))
    assert r.status_code == 200
    assert erwartet in r.text
    assert "Portal" in r.text  # Vorschlag wird trotzdem gelistet


def test_verbindungsfehler_landet_auf_der_seite(client, monkeypatch):
    import anthropic
    import app.evaluation as evaluation

    request = httpx.Request("POST", "http://127.0.0.1:9/v1/messages")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setattr(evaluation, "_ask_model", _raise(anthropic.APIConnectionError(request=request)))
    assert _submit(client, "projektmanager", "Portal").status_code == 303
    r = client.get("/proposals/evaluate", cookies=as_user("projektmanager"))
    assert r.status_code == 200
    assert "Keine Verbindung zum LLM-Anbieter" in r.text


def test_ein_fehlschlag_bricht_die_anderen_bewertungen_nicht_ab(client, monkeypatch):
    import app.evaluation as evaluation

    def fake_ask(model, p):
        if p.slug == "kaputt":
            raise _api_error(429)
        return json.dumps(_fake_evaluation())

    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setattr(evaluation, "_ask_model", fake_ask)
    assert _submit(client, "projektmanager", "Kaputt").status_code == 303
    assert _submit(client, "projektmanager", "Heil").status_code == 303
    r = client.get("/proposals/evaluate", cookies=as_user("projektmanager"))
    assert r.status_code == 200
    assert "Rate-Limit" in r.text
    assert "Gesamtscore: 8.0" in r.text


def test_unerwartete_json_struktur_wird_abgefangen(client, monkeypatch):
    import app.evaluation as evaluation

    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setattr(evaluation, "_ask_model", lambda model, p: "[1, 2, 3]")
    assert _submit(client, "projektmanager", "Portal").status_code == 303
    r = client.get("/proposals/evaluate", cookies=as_user("projektmanager"))
    assert r.status_code == 200
    assert "nicht die erwartete Struktur" in r.text


def test_bewertung_folgt_decide_gast_sieht_keine_internen_vorschlaege(client, monkeypatch):
    """US-12: Die Bewertungsseite darf nicht mehr zeigen als die Vorschlagsliste."""
    import app.evaluation as evaluation

    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setattr(evaluation, "_ask_model", lambda model, p: json.dumps(_fake_evaluation()))
    assert _submit(client, "projektmanager", "Internes Projekt").status_code == 303
    assert _submit(client, "projektmanager", "Geheimes Projekt", "vertraulich").status_code == 303

    gast = client.get("/proposals/evaluate")
    assert gast.status_code == 200
    assert "Internes Projekt" not in gast.text
    assert "Geheimes Projekt" not in gast.text
    assert "Noch keine Projektvorschläge" in gast.text

    einreicher = client.get("/proposals/evaluate", cookies=as_user("projektmanager"))
    assert "Internes Projekt" in einreicher.text
    assert "Geheimes Projekt" in einreicher.text


def test_bewertung_ruft_das_modell_nur_fuer_sichtbare_vorschlaege(client, monkeypatch):
    """Vertrauliche Inhalte duerfen fuer Fremde nicht einmal an das Modell gehen."""
    import app.evaluation as evaluation

    gesehen: list[str] = []

    def fake_ask(model, p):
        gesehen.append(p.slug)
        return json.dumps(_fake_evaluation())

    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setattr(evaluation, "_ask_model", fake_ask)
    assert _submit(client, "projektmanager", "Geheimes Projekt", "vertraulich").status_code == 303
    client.get("/proposals/evaluate")  # Gast
    assert gesehen == []
    client.get("/proposals/evaluate", cookies=as_user("projektmanager"))
    assert gesehen == ["geheimes-projekt"]
