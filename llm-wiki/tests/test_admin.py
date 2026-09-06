"""Stufe 2, US-13 bis US-16: Admin-Dashboard, Protokoll, Gewaltenteilung."""
from __future__ import annotations

import pytest

from tests.conftest import as_user

POSTS = [
    ("/admin/users/save", {"user_id": "mitarbeiter", "name": "Mitarbeiter", "gruppen": ["alle", "finance"]}),
    ("/admin/users/new", {"user_id": "neu", "name": "Neu", "gruppen": ["alle"]}),
    ("/admin/users/delete", {"user_id": "mitarbeiter"}),
    ("/admin/domains/save", {"domaene": "finance", "lesen": ["alle"]}),
    ("/admin/domains/new", {"domaene": "qm", "lesen": ["alle"]}),
    ("/admin/domains/delete", {"domaene": "mail"}),
    ("/admin/groups/new", {"gruppe": "qm"}),
]


def _changelog():
    import app.access as access
    return access.read_changelog(50)


@pytest.mark.security
def test_nicht_admin_bekommt_404_ueberall(client):
    import app.access as access

    for user in ("mitarbeiter", "cfo", "ceo", "gast"):
        c = as_user(user)
        r = client.get("/admin", cookies=c)
        assert r.status_code == 404
        assert r.text == client.get("/wiki/gibt-es-nicht", cookies=c).text
        for path, data in POSTS:
            assert client.post(path, cookies=c, data=data).status_code == 404, (user, path)
        # Link nur fuer Admins sichtbar
        assert 'href="/admin"' not in client.get("/wiki/oeffentlich", cookies=c).text
    # nichts wurde geschrieben
    assert access.user_groups("mitarbeiter") == ["alle"]
    assert _changelog() == []


def test_admin_sieht_dashboard(client):
    r = client.get("/admin", cookies=as_user("admin"))
    assert r.status_code == 200
    assert "Admin-Dashboard" in r.text
    for uid in ("gast", "mitarbeiter", "cfo", "admin"):
        assert f"<code>{uid}</code>" in r.text
    for dom in ("allgemein", "finance", "br"):
        assert f"<code>{dom}</code>" in r.text
    assert 'href="/admin"' in client.get("/wiki/oeffentlich", cookies=as_user("admin")).text


@pytest.mark.security
def test_admin_liest_keine_finance_seite(client):
    """Gewaltenteilung: admin verwaltet Rechte, liest aber nicht mehr als 'alle'."""
    import app.access as access
    from app.access import PageMeta

    assert access.decide("admin", PageMeta(vertraulichkeit="intern", domaene="finance")) == "DENY"
    assert access.decide("admin", PageMeta(vertraulichkeit="intern", domaene="br")) == "DENY"
    assert access.decide("admin", PageMeta(vertraulichkeit="intern", domaene="allgemein")) == "ALLOW"
    assert client.get("/wiki/budget-finance", cookies=as_user("admin")).status_code == 404
    assert client.get("/wiki/br-protokoll", cookies=as_user("admin")).status_code == 404
    assert client.get("/wiki/altbestand", cookies=as_user("admin")).status_code == 200


def test_gruppe_vergeben_gilt_sofort_und_wird_protokolliert(client):
    import app.access as access
    from app.access import PageMeta

    finance = PageMeta(vertraulichkeit="intern", domaene="finance")
    assert access.decide("mitarbeiter", finance) == "DENY"
    assert client.get("/wiki/budget-finance", cookies=as_user("mitarbeiter")).status_code == 404

    r = client.post("/admin/users/save", cookies=as_user("admin"), data={
        "user_id": "mitarbeiter", "name": "Mitarbeiter", "gruppen": ["alle", "finance"],
    })
    assert r.status_code == 303 and r.headers["location"] == "/admin?meldung=gespeichert"

    # ohne Neustart
    assert access.decide("mitarbeiter", finance) == "ALLOW"
    assert access.user_groups("mitarbeiter") == ["alle", "finance"]
    assert client.get("/wiki/budget-finance", cookies=as_user("mitarbeiter")).status_code == 200

    log = _changelog()
    assert len(log) == 1
    assert "· admin · Nutzer mitarbeiter: Gruppen [alle] → [alle, finance]" in log[0]
    assert (access.changelog_path()).exists()
    r = client.get("/admin", cookies=as_user("admin"))
    assert "Nutzer mitarbeiter: Gruppen [alle] → [alle, finance]" in r.text

    # Datei: Kopfkommentar und Reihenfolge bleiben erhalten
    raw = access.permissions_path().read_text(encoding="utf-8")
    assert raw.startswith("# Rechte-Datei des LLM-Wikis")
    assert "# sharepoint_finance" in raw  # Zeilenkommentar (Ablageort -> Domaene) bleibt
    ids = [u["id"] for u in access.list_users()]
    assert ids[:3] == ["gast", "mitarbeiter", "projektmanager"] and ids[-1] == "admin"

    # unveraendert speichern -> keine neue Protokollzeile
    r = client.post("/admin/users/save", cookies=as_user("admin"), data={
        "user_id": "mitarbeiter", "name": "Mitarbeiter", "gruppen": ["alle", "finance"],
    })
    assert r.headers["location"] == "/admin?meldung=unveraendert"
    assert len(_changelog()) == 1


def test_nutzer_anlegen_und_entfernen(client):
    import app.access as access

    r = client.post("/admin/users/new", cookies=as_user("admin"), data={
        "user_id": "einkauf-leitung", "name": "Einkaufsleitung", "gruppen": ["alle", "einkauf"],
    })
    assert r.headers["location"] == "/admin?meldung=gespeichert"
    assert access.get_user("einkauf-leitung")["gruppen"] == ["alle", "einkauf"]
    assert access.user_name("einkauf-leitung") == "Einkaufsleitung"
    # neuer Nutzer taucht in der Nutzerauswahl auf
    assert 'value="einkauf-leitung"' in client.get("/wiki/oeffentlich", cookies=as_user("admin")).text

    # ungueltige ID / Duplikat / unbekannte Gruppe
    r = client.post("/admin/users/new", cookies=as_user("admin"), data={"user_id": "Böse Id!", "name": "x"})
    assert r.headers["location"] == "/admin?meldung=ungueltige-id"
    r = client.post("/admin/users/new", cookies=as_user("admin"), data={"user_id": "cfo", "name": "x"})
    assert r.headers["location"] == "/admin?meldung=nutzer-existiert"
    r = client.post("/admin/users/new", cookies=as_user("admin"), data={"user_id": "xy", "gruppen": ["root"]})
    assert r.headers["location"] == "/admin?meldung=gruppe-unbekannt"

    r = client.post("/admin/users/delete", cookies=as_user("admin"), data={"user_id": "einkauf-leitung"})
    assert r.headers["location"] == "/admin?meldung=gespeichert"
    assert access.get_user("einkauf-leitung")["id"] == "gast"
    log = _changelog()
    assert "Nutzer einkauf-leitung entfernt (Name Einkaufsleitung, Gruppen [alle, einkauf])" in log[0]
    assert "Nutzer einkauf-leitung angelegt: Name Einkaufsleitung, Gruppen [alle, einkauf]" in log[1]


@pytest.mark.security
def test_gast_und_selbst_nicht_loeschbar(client):
    import app.access as access

    r = client.post("/admin/users/delete", cookies=as_user("admin"), data={"user_id": "gast"})
    assert r.headers["location"] == "/admin?meldung=gast-nicht-loeschbar"
    r = client.post("/admin/users/delete", cookies=as_user("admin"), data={"user_id": "admin"})
    assert r.headers["location"] == "/admin?meldung=selbst-nicht-loeschbar"
    r = client.post("/admin/users/save", cookies=as_user("admin"), data={"user_id": "admin", "gruppen": ["alle"]})
    assert r.headers["location"] == "/admin?meldung=admin-selbst"
    # Gast bleibt ohne Gruppen, auch wenn jemand welche schickt
    r = client.post("/admin/users/save", cookies=as_user("admin"), data={"user_id": "gast", "gruppen": ["alle", "finance"]})
    assert r.headers["location"] == "/admin?meldung=unveraendert"
    assert access.user_groups("gast") == []
    assert access.is_admin("admin")
    assert [u["id"] for u in access.list_users()][0] == "gast"
    assert _changelog() == []


def test_domaene_anlegen_pflegen_entfernen(client):
    import app.access as access
    import app.wiki as wiki
    from app.access import PageMeta

    r = client.post("/admin/domains/new", cookies=as_user("admin"), data={"domaene": "qm", "lesen": ["alle"]})
    assert r.headers["location"] == "/admin?meldung=gespeichert"
    assert (wiki.pages_dir() / "qm").is_dir()
    assert "qm" in access.list_domains()
    # erscheint im Editor
    assert '<option value="qm"' in client.get("/new", cookies=as_user("cfo")).text
    assert access.decide("mitarbeiter", PageMeta(domaene="qm")) == "ALLOW"

    # Lesegruppen aendern
    r = client.post("/admin/domains/save", cookies=as_user("admin"), data={"domaene": "qm", "lesen": ["leitung"]})
    assert r.headers["location"] == "/admin?meldung=gespeichert"
    assert access.decide("mitarbeiter", PageMeta(domaene="qm")) == "DENY"
    assert access.decide("cfo", PageMeta(domaene="qm")) == "ALLOW"
    assert "Domäne qm: Lesegruppen [alle] → [leitung]" in _changelog()[0]

    # mit Inhalt nicht loeschbar
    wiki.save_page("qm-handbuch", "QM Handbuch", "Inhalt", PageMeta(erstellt_von="cfo", domaene="qm"))
    r = client.post("/admin/domains/delete", cookies=as_user("admin"), data={"domaene": "qm"})
    assert r.headers["location"] == "/admin?meldung=domaene-nicht-leer"
    assert "qm" in access.list_domains()
    assert (wiki.pages_dir() / "qm" / "qm-handbuch.md").exists()

    # leer -> loeschbar, Ordner weg
    wiki.delete_page("qm-handbuch")
    r = client.post("/admin/domains/delete", cookies=as_user("admin"), data={"domaene": "qm"})
    assert r.headers["location"] == "/admin?meldung=gespeichert"
    assert "qm" not in access.list_domains()
    assert not (wiki.pages_dir() / "qm").exists()
    assert "Domäne qm entfernt (Lesegruppen [leitung])" in _changelog()[0]

    # Fixture-Domaene finance hat Seiten -> nicht loeschbar
    r = client.post("/admin/domains/delete", cookies=as_user("admin"), data={"domaene": "finance"})
    assert r.headers["location"] == "/admin?meldung=domaene-nicht-leer"
    assert "finance" in access.list_domains()


def test_gruppe_anlegen(client):
    import app.access as access

    r = client.post("/admin/groups/new", cookies=as_user("admin"), data={"gruppe": "qm"})
    assert r.headers["location"] == "/admin?meldung=gespeichert"
    assert "qm" in access.load_permissions()["gruppen"]
    assert "Gruppe qm angelegt" in _changelog()[0]
    r = client.post("/admin/groups/new", cookies=as_user("admin"), data={"gruppe": "qm"})
    assert r.headers["location"] == "/admin?meldung=gruppe-existiert"
    # neue Gruppe kann sofort vergeben werden
    r = client.post("/admin/users/save", cookies=as_user("admin"), data={
        "user_id": "mitarbeiter", "name": "Mitarbeiter", "gruppen": ["alle", "qm"],
    })
    assert r.headers["location"] == "/admin?meldung=gespeichert"
    assert access.user_groups("mitarbeiter") == ["alle", "qm"]


def test_save_permissions_roundtrip_und_changelog_format(pages_env):
    import app.access as access

    data = access.load_permissions()
    data["nutzer"]["cfo"]["name"] = 'CFO "Zahlen" / Controlling'
    access.save_permissions(data, "admin", "Nutzer cfo: Name CFO / Controlling → CFO \"Zahlen\" / Controlling")
    assert access.user_name("cfo") == 'CFO "Zahlen" / Controlling'
    lines = access.changelog_path().read_text(encoding="utf-8").splitlines()
    entry = [l for l in lines if l.startswith("- ")][-1]
    # - 2026-09-05T20:15 · admin · ...
    assert entry[2:18].count("T") == 1 and entry[18:].startswith(" · admin · Nutzer cfo:")
    assert access.read_changelog(1) == [entry[2:]]
