"""Ein Zugriffsweg ueber HTTP: Liste, 404 auf verbotene URLs, Gast-Sperre."""
from __future__ import annotations

import re

import pytest

from tests.conftest import as_user

pytestmark = pytest.mark.security


def sidebar_slugs(html: str) -> set[str]:
    return set(re.findall(r'href="/wiki/([a-z0-9-]+)"', html))


def test_mitarbeiter_sieht_finance_nicht(client):
    c = as_user("mitarbeiter")
    r = client.get("/", cookies=c)
    assert r.status_code == 200
    assert "budget-finance" not in sidebar_slugs(r.text)
    assert "Budget Finance" not in r.text
    assert client.get("/wiki/budget-finance", cookies=c).status_code == 404
    assert client.get("/wiki/budget-finance/edit", cookies=c).status_code == 404
    assert client.post(
        "/wiki/budget-finance/edit", cookies=c,
        data={"title": "x", "content": "y"},
    ).status_code == 404
    assert client.post("/wiki/budget-finance/delete", cookies=c).status_code == 404


def test_verbotene_und_fehlende_seite_nicht_unterscheidbar(client):
    c = as_user("mitarbeiter")
    r1 = client.get("/wiki/budget-finance", cookies=c)
    r2 = client.get("/wiki/gibt-es-nicht", cookies=c)
    assert r1.status_code == r2.status_code == 404
    assert r1.text == r2.text


def test_cfo_sieht_finance(client):
    c = as_user("cfo")
    r = client.get("/", cookies=c)
    assert "budget-finance" in sidebar_slugs(r.text)
    r = client.get("/wiki/budget-finance", cookies=c)
    assert r.status_code == 200
    # US-10 (Stufe 2): Herkunftsbox ersetzt "Angelegt von" durch "Eingebracht von"
    assert "Eingebracht von" in r.text
    assert "CFO / Controlling" in r.text
    assert "01.09.2026 10:00" in r.text
    assert client.get("/wiki/budget-finance/edit", cookies=c).status_code == 200


def test_ceo_liest_br_nicht(client):
    c = as_user("ceo")
    r = client.get("/", cookies=c)
    assert "br-protokoll" not in sidebar_slugs(r.text)
    assert client.get("/wiki/br-protokoll", cookies=c).status_code == 404
    # Betriebsrat schon
    assert client.get("/wiki/br-protokoll", cookies=as_user("betriebsrat")).status_code == 200


def test_gast_sieht_nur_oeffentlich_und_darf_nicht_anlegen(client):
    r = client.get("/")  # kein Cookie -> Gast
    assert r.status_code == 200
    assert "Gast (nicht angemeldet)" in r.text
    slugs = sidebar_slugs(r.text)
    assert slugs == {"oeffentlich"}
    assert client.get("/wiki/oeffentlich").status_code == 200
    assert client.get("/wiki/altbestand").status_code == 404

    r = client.get("/new")
    assert r.status_code == 403
    assert "Bitte erst Nutzer wählen" in r.text
    r = client.post("/new", data={"title": "Neu", "content": "x"})
    assert r.status_code == 403
    # Gast darf auch oeffentliche Seiten nicht bearbeiten/loeschen
    assert client.get("/wiki/oeffentlich/edit").status_code == 403
    assert client.post("/wiki/oeffentlich/delete").status_code == 403


def test_unbekannter_cookie_ist_gast(client):
    r = client.get("/", cookies=as_user("hacker"))
    assert sidebar_slugs(r.text) == {"oeffentlich"}


def test_altbestand_sichtbar_mit_hinweis(client):
    c = as_user("mitarbeiter")
    r = client.get("/", cookies=c)
    assert "altbestand" in sidebar_slugs(r.text)
    r = client.get("/wiki/altbestand", cookies=c)
    assert r.status_code == 200
    assert "Altbestand" in r.text
    assert "Herkunft unbekannt (Altbestand)" in r.text


def test_vertraulich_nur_ersteller_und_empfaenger(client):
    assert client.get("/wiki/vertraulich-projekt", cookies=as_user("projektmanager")).status_code == 200
    assert client.get("/wiki/vertraulich-projekt", cookies=as_user("pmo-leitung")).status_code == 200
    assert client.get("/wiki/vertraulich-projekt", cookies=as_user("mitarbeiter")).status_code == 404
    assert client.get("/wiki/vertraulich-projekt", cookies=as_user("ceo")).status_code == 404


def test_login_setzt_cookie_und_leitet_zurueck(client):
    import app.access as access

    r = client.post("/login", data={"user": "cfo", "next": "/wiki/budget-finance"})
    assert r.status_code == 303
    assert r.headers["location"] == "/wiki/budget-finance"
    # Cookie ist signiert (<uid>.<hmac>), nicht der rohe Nutzername
    assert r.cookies.get("mpb_user") != "cfo"
    assert access.verify_user(r.cookies.get("mpb_user")) == "cfo"
    # Open-Redirect-Schutz
    r = client.post("/login", data={"user": "cfo", "next": "https://evil.example/"})
    assert r.headers["location"] == "/"
    # unbekannter Nutzer -> gast
    r = client.post("/login", data={"user": "root"})
    assert access.verify_user(r.cookies.get("mpb_user")) == "gast"
    r = client.post("/logout")
    assert r.status_code == 303


def test_neue_seite_traegt_aktuellen_nutzer(client):
    import app.wiki as wiki
    c = as_user("projektmanager")
    r = client.post("/new", cookies=c, data={
        "title": "Meine Notiz", "content": "Inhalt",
        "vertraulichkeit": "vertraulich", "domaene": "projekt",
        "empfaenger": "pmo-leitung, finance",
    })
    assert r.status_code == 303
    page = wiki.get_page("meine-notiz")
    assert page.meta.erstellt_von == "projektmanager"
    assert page.meta.erstellt_am and "." not in page.meta.erstellt_am  # keine Mikrosekunden
    assert page.meta.vertraulichkeit == "vertraulich"
    assert page.meta.domaene == "projekt"
    assert page.meta.empfaenger == ["pmo-leitung", "finance"]
    assert page.meta.geaendert_von == ""
    # Nutzerauswahl zeigt alle Nutzer aus permissions.yaml
    r = client.get("/wiki/meine-notiz", cookies=c)
    assert '<select name="user"' in r.text
    for uid in ("gast", "mitarbeiter", "cfo", "betriebsrat", "ceo", "orchestrator"):
        assert f'value="{uid}"' in r.text
