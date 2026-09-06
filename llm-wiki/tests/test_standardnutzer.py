"""Standardnutzer beim ersten Aufruf (MPB_DEFAULT_USER).

Wer die Seite ohne Cookie oeffnet, startet nicht mehr zwangslaeufig als Gast.
Die Vorgabe ist Konfiguration, kein fest verdrahteter Wert: ohne die Variable
bleibt es beim Gast, damit ein Vergessen nichts oeffnet.
"""
from __future__ import annotations

import pytest

from app import access
from tests.conftest import as_user


# ---------------------------------------------------------------------------
# Die Vorgabe selbst
# ---------------------------------------------------------------------------


def test_ohne_variable_bleibt_es_beim_gast(pages_env, monkeypatch):
    """Der sichere Ausgangszustand: nicht gesetzt heisst nicht offen."""
    monkeypatch.setenv("MPB_DEFAULT_USER", "")
    assert access.default_user() == access.GUEST


def test_gesetzter_standardnutzer_wird_uebernommen(pages_env, monkeypatch):
    monkeypatch.setenv("MPB_DEFAULT_USER", "ceo")
    assert access.default_user() == "ceo"


@pytest.mark.security
@pytest.mark.parametrize("murks", ["gibtsnicht", "CEO", "ce o", "../admin", "  "])
def test_unbekannte_id_faellt_auf_den_gast_zurueck(pages_env, monkeypatch, murks):
    """Ein Tippfehler in der .env darf keine Rechte verschieben."""
    monkeypatch.setenv("MPB_DEFAULT_USER", murks)
    assert access.default_user() == access.GUEST


# ---------------------------------------------------------------------------
# Wirkung auf die Anwendung
# ---------------------------------------------------------------------------


def test_besucher_ohne_cookie_startet_als_standardnutzer(client, monkeypatch):
    monkeypatch.setenv("MPB_DEFAULT_USER", "ceo")

    r = client.get("/knowledge")

    assert r.status_code == 200
    assert "CEO" in r.text, "der Standardnutzer wird nicht angezeigt"


def test_standardnutzer_sieht_finance(client, monkeypatch):
    """Der Sinn der Sache: ohne Anmeldung direkt etwas Brauchbares sehen."""
    monkeypatch.setenv("MPB_DEFAULT_USER", "ceo")

    r = client.get("/knowledge")

    assert "Budget Finance" in r.text


def test_ohne_variable_sieht_der_besucher_kein_finance(client, monkeypatch):
    monkeypatch.setenv("MPB_DEFAULT_USER", "")

    r = client.get("/knowledge")

    assert "Budget Finance" not in r.text


@pytest.mark.security
def test_ein_cookie_schlaegt_die_vorgabe(client, monkeypatch):
    """Wer sich bewusst als jemand anderes ausweist, bleibt das auch -
    die Vorgabe greift nur beim ersten Aufruf ohne Cookie."""
    monkeypatch.setenv("MPB_DEFAULT_USER", "ceo")

    r = client.get("/knowledge", cookies=as_user("mitarbeiter"))

    assert "Budget Finance" not in r.text


@pytest.mark.security
def test_standardnutzer_oeffnet_den_betriebsrat_nicht(client, monkeypatch):
    """`ceo` hat die meisten Rechte, aber nicht alle - br bleibt zu."""
    monkeypatch.setenv("MPB_DEFAULT_USER", "ceo")

    r = client.get("/knowledge")

    assert "BR Protokoll" not in r.text
    assert access.decide("ceo", access.PageMeta(domaene="br")) == access.DENY
