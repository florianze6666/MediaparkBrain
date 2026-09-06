"""Demo-Modus: Standardnutzer ohne Cookie (MPB_DEFAULT_USER).

Ohne die Env-Variable (conftest setzt sie explizit leer) bleibt alles wie bisher:
kein Cookie = Gast. Mit MPB_DEFAULT_USER=demo gilt der Demo-Nutzer fuer jeden
Request ohne gueltigen Cookie. Ein gueltiger Cookie gewinnt immer.
"""
from __future__ import annotations

import pytest

from app import wiki
from tests.conftest import as_user


def test_ohne_env_ist_gast(client, monkeypatch):
    monkeypatch.setenv("MPB_DEFAULT_USER", "")
    r = client.get("/")
    assert r.status_code == 200
    assert "Gast (nicht angemeldet)" in r.text
    assert "Standardnutzer (Demo)" not in r.text
    r = client.post(
        "/upload",
        files={"files": ("n.txt", b"x", "text/plain")},
        data={"target": "knowledge", "domaene": "allgemein"},
    )
    assert r.status_code == 403


def test_demo_standardnutzer_ohne_login(client, pages_env, monkeypatch):
    monkeypatch.setenv("MPB_DEFAULT_USER", "demo")
    monkeypatch.setenv("LLM_API_KEY", "")

    r = client.get("/")
    assert r.status_code == 200
    assert "Demo (alle Rechte)" in r.text
    assert "Standardnutzer (Demo)" in r.text

    # Einstellungen zeigen den Standardnutzer wie einen angemeldeten Nutzer
    r = client.get("/settings")
    assert 'value="demo" class="is-active"' in r.text

    # Upload ohne Login ueber den Kompass-Weg
    r = client.post(
        "/upload",
        files={"files": ("Notiz_Demo.txt", b"Demo-Notiz mit Inhalt.", "text/plain")},
        data={"target": "knowledge", "titel": "", "domaene": "projekt", "vertraulichkeit": "intern"},
    )
    assert r.status_code == 200
    assert 'href="/knowledge/notiz-demo"' in r.text
    page = wiki.get_page("notiz-demo")
    assert page is not None and page.meta.erstellt_von == "demo"
    assert client.get("/knowledge/notiz-demo").status_code == 200

    # demo ist auch admin
    assert client.get("/admin/permissions").status_code == 200


def test_unbekannter_wert_ist_gast(client, monkeypatch):
    monkeypatch.setenv("MPB_DEFAULT_USER", "gibt-es-nicht")
    r = client.get("/")
    assert "Gast (nicht angemeldet)" in r.text
    assert "Standardnutzer (Demo)" not in r.text
    assert client.get("/admin/permissions").status_code == 404


@pytest.mark.security
def test_gueltiger_cookie_gewinnt_ueber_standardnutzer(client, monkeypatch):
    monkeypatch.setenv("MPB_DEFAULT_USER", "demo")
    m = as_user("mitarbeiter")
    r = client.get("/", cookies=m)
    assert "Mitarbeiter" in r.text
    assert "Demo (alle Rechte)" not in r.text
    assert "Standardnutzer (Demo)" not in r.text
    # Rechte des Cookie-Nutzers, nicht die des Standardnutzers
    assert client.get("/admin/permissions", cookies=m).status_code == 404
    assert client.get("/knowledge/budget-finance", cookies=m).status_code == 404
