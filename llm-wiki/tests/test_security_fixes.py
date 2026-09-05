"""Security-Review nach Paket 8 - drei Luecken, drei Fixes:

1. Write ⊆ Read: Schreiben nur in Domaenen, die man lesen darf (access.can_write).
2. Signierter Identitaets-Cookie (HMAC-SHA256, MPB_SECRET): roh oder manipuliert = Gast.
3. Ordner ist die einzige Wahrheit, `allgemein` ist die Lobby: Das Label oeffentlich
   erweitert nie die Ordnerrechte.
Dazu: Admin kann sich die Gruppe admin nicht selbst entziehen; Slugs nur ^[a-z0-9-]+$.
"""
from __future__ import annotations

import importlib
import re

import pytest

from tests.conftest import as_user

pytestmark = pytest.mark.security

WRITE_403 = "Du darfst in dieser Domäne nichts anlegen"


def sidebar_slugs(html: str) -> set[str]:
    return set(re.findall(r'href="/wiki/([a-z0-9-]+)"', html))


def _page_form(title: str, domaene: str, vertraulichkeit: str = "intern", empfaenger: str = "",
               content: str = "Inhalt") -> dict:
    return {"title": title, "content": content, "vertraulichkeit": vertraulichkeit,
            "domaene": domaene, "empfaenger": empfaenger}


# ---------------------------------------------------------------------------
# Fix 1: Write ⊆ Read
# ---------------------------------------------------------------------------


def test_new_in_fremder_domaene_403_und_keine_datei(client):
    import app.wiki as wiki

    r = client.post("/new", cookies=as_user("mitarbeiter"), data=_page_form("Schmuggel", "finance"))
    assert r.status_code == 403
    assert WRITE_403 in r.text
    assert not (wiki.pages_dir() / "finance" / "schmuggel.md").exists()
    assert wiki.get_page("schmuggel") is None
    assert not list(wiki.pages_dir().rglob("schmuggel.md"))

    # cfo liest finance -> darf dort anlegen
    r = client.post("/new", cookies=as_user("cfo"), data=_page_form("Schmuggel", "finance"))
    assert r.status_code == 303
    assert (wiki.pages_dir() / "finance" / "schmuggel.md").exists()
    assert wiki.get_page("schmuggel").meta.erstellt_von == "cfo"


def test_edit_verschieben_in_fremde_domaene_403(client):
    import app.wiki as wiki
    from tests.conftest import LEGACY_TEXT

    src = wiki.pages_dir() / "allgemein" / "altbestand.md"
    before = src.read_text(encoding="utf-8")
    r = client.post("/wiki/altbestand/edit", cookies=as_user("mitarbeiter"),
                    data=_page_form("Altbestand", "finance", content="verschoben?"))
    assert r.status_code == 403
    assert WRITE_403 in r.text
    assert src.exists() and src.read_text(encoding="utf-8") == before
    assert not (wiki.pages_dir() / "finance" / "altbestand.md").exists()
    assert LEGACY_TEXT in wiki.get_page("altbestand").content

    # Umbenennen + Verschieben in einem Schritt: nichts wird geloescht
    r = client.post("/wiki/altbestand/edit", cookies=as_user("mitarbeiter"),
                    data=_page_form("Neuer Name", "finance"))
    assert r.status_code == 403
    assert src.exists()
    assert not list(wiki.pages_dir().rglob("neuer-name.md"))

    # in der eigenen Domaene bleibt Bearbeiten erlaubt
    r = client.post("/wiki/altbestand/edit", cookies=as_user("mitarbeiter"),
                    data=_page_form("Altbestand", "allgemein", content="ok"))
    assert r.status_code == 303


def test_edit_vertraulich_empfaenger_darf_sich_nicht_selbst_aussperren(client):
    """Write ⊆ Read auf Seitenebene: Ein Empfaenger darf die Empfaengerliste nicht
    so aendern, dass er die Seite danach selbst nicht mehr sieht."""
    import app.wiki as wiki

    # Titel "Vertraulich Projekt" -> Slug bleibt vertraulich-projekt (kein Umbenennen)
    r = client.post("/wiki/vertraulich-projekt/edit", cookies=as_user("pmo-leitung"),
                    data=_page_form("Vertraulich Projekt", "projekt",
                                    vertraulichkeit="vertraulich", empfaenger=""))
    assert r.status_code == 403
    assert wiki.get_page("vertraulich-projekt").meta.empfaenger == ["pmo-leitung"]
    # der Ersteller sieht sich immer selbst -> darf die Liste leeren
    r = client.post("/wiki/vertraulich-projekt/edit", cookies=as_user("projektmanager"),
                    data=_page_form("Vertraulich Projekt", "projekt",
                                    vertraulichkeit="vertraulich", empfaenger=""))
    assert r.status_code == 303
    assert wiki.get_page("vertraulich-projekt").meta.empfaenger == []


def test_proposal_in_fremder_domaene_403(client):
    import app.proposals as proposals

    r = client.post("/proposals/new", cookies=as_user("mitarbeiter"), data={
        "project_name": "Finanzplan", "description": "x",
        "domaene": "finance", "vertraulichkeit": "intern", "empfaenger": "",
    })
    assert r.status_code == 403
    assert WRITE_403 in r.text
    assert proposals.get_proposal("finanzplan") is None
    assert proposals.list_proposals() == []

    r = client.post("/proposals/new", cookies=as_user("cfo"), data={
        "project_name": "Finanzplan", "description": "x",
        "domaene": "finance", "vertraulichkeit": "intern", "empfaenger": "",
    })
    assert r.status_code == 303
    assert proposals.get_proposal("finanzplan").meta.domaene == "finance"


def test_domaenen_select_zeigt_nur_lesbare(client):
    m = as_user("mitarbeiter")
    for url in ("/new", "/proposals/new", "/wiki/altbestand/edit"):
        r = client.get(url, cookies=m)
        assert r.status_code == 200, url
        select = r.text.split('<select name="domaene">', 1)[1].split("</select>", 1)[0]
        assert 'value="finance"' not in select, url
        assert 'value="br"' not in select, url
        assert 'value="allgemein"' in select and 'value="projekt"' in select, url
    # cfo bekommt finance angeboten, br nicht
    select = client.get("/new", cookies=as_user("cfo")).text.split('<select name="domaene">', 1)[1].split("</select>", 1)[0]
    assert 'value="finance"' in select and 'value="br"' not in select


def test_can_write_ist_teilmenge_von_can_read(pages_env):
    import app.access as access
    from app.access import PageMeta

    # Ersteller sieht seine vertrauliche Seite immer -> darf sie anlegen
    assert access.can_write("cfo", PageMeta(erstellt_von="cfo", vertraulichkeit="vertraulich",
                                            domaene="finance", empfaenger=[]))
    # ceo liest finance, ist aber weder Ersteller noch Empfaenger -> nein
    assert not access.can_write("ceo", PageMeta(erstellt_von="cfo", vertraulichkeit="vertraulich",
                                                domaene="finance", empfaenger=[]))
    # Ordner nicht lesbar -> nein, auch als Ersteller, auch bei oeffentlich
    assert not access.can_write("mitarbeiter", PageMeta(erstellt_von="mitarbeiter", domaene="finance"))
    assert not access.can_write("mitarbeiter", PageMeta(erstellt_von="mitarbeiter",
                                                        vertraulichkeit="oeffentlich", domaene="finance"))
    # unbekannte Domaene -> nein
    assert not access.can_write("cfo", PageMeta(erstellt_von="cfo", domaene="gibt-es-nicht"))
    # Gast: intern nirgends
    assert not access.can_write("gast", PageMeta(domaene="allgemein"))
    # Was man schreiben darf, darf man auch lesen
    for uid in ("gast", "mitarbeiter", "cfo", "ceo", "betriebsrat", "admin"):
        for dom in access.list_domains():
            for v in access.VERTRAULICHKEITEN:
                meta = PageMeta(erstellt_von=uid, vertraulichkeit=v, domaene=dom)
                assert not access.can_write(uid, meta) or access.can_read(uid, meta)


# ---------------------------------------------------------------------------
# Fix 2: Signierter Identitaets-Cookie
# ---------------------------------------------------------------------------


def test_roher_cookie_ist_gast(client):
    raw = {"mpb_user": "admin"}
    assert client.get("/admin", cookies=raw).status_code == 404
    r = client.get("/", cookies=raw)
    assert r.status_code == 200
    assert "Angemeldet als: <strong>Gast (nicht angemeldet)</strong>" in r.text
    assert 'href="/admin"' not in r.text
    assert sidebar_slugs(r.text) == {"oeffentlich"}
    assert client.get("/wiki/budget-finance", cookies={"mpb_user": "cfo"}).status_code == 404
    assert client.post("/new", cookies={"mpb_user": "cfo"}, data=_page_form("X", "allgemein")).status_code == 403


def test_manipulierte_signatur_ist_gast(client):
    import app.access as access

    good = access.sign_user("cfo")
    uid, sig = good.rsplit(".", 1)
    assert uid == "cfo" and re.fullmatch(r"[0-9a-f]{64}", sig)
    flipped = ("0" if sig[0] != "0" else "1") + sig[1:]
    bad = f"{uid}.{flipped}"
    assert access.verify_user(bad) is None
    r = client.get("/wiki/budget-finance", cookies={"mpb_user": bad})
    assert r.status_code == 404
    assert "Gast (nicht angemeldet)" in client.get("/", cookies={"mpb_user": bad}).text

    # Signatur eines anderen Nutzers an "admin" haengen
    forged = f"admin.{sig}"
    assert access.verify_user(forged) is None
    assert client.get("/admin", cookies={"mpb_user": forged}).status_code == 404

    # Formfehler
    for value in (None, "", "admin", "admin.", ".abc", "admin.xyz", "Admin." + sig, "a" * 300):
        assert access.verify_user(value) is None, value


def test_korrekt_signiert_wird_erkannt(client):
    import app.access as access

    r = client.get("/", cookies=as_user("cfo"))
    assert "Angemeldet als: <strong>CFO / Controlling</strong>" in r.text
    assert "budget-finance" in sidebar_slugs(r.text)
    assert client.get("/admin", cookies=as_user("admin")).status_code == 200

    # Login -> signierter Cookie -> funktioniert im naechsten Request
    r = client.post("/login", data={"user": "cfo"})
    value = r.cookies.get("mpb_user")
    assert value != "cfo"
    assert re.fullmatch(r"cfo\.[0-9a-f]{64}", value)
    assert access.verify_user(value) == "cfo"
    set_cookie = r.headers["set-cookie"].lower()
    assert "httponly" in set_cookie and "samesite=lax" in set_cookie and "secure" not in set_cookie
    assert client.get("/wiki/budget-finance", cookies={"mpb_user": value}).status_code == 200


def test_secret_aus_env_und_warnung_ohne_secret(pages_env, monkeypatch, caplog):
    import app.access as access
    from tests.conftest import TEST_SECRET

    old = access.sign_user("cfo")
    # anderes Secret -> alte Signaturen ungueltig, neue gueltig
    monkeypatch.setenv("MPB_SECRET", "anderes-secret")
    importlib.reload(access)
    assert access.verify_user(old) is None
    assert access.verify_user(access.sign_user("cfo")) == "cfo"

    # kein Secret -> Warnung, zufaelliges Secret, Roundtrip funktioniert trotzdem
    monkeypatch.delenv("MPB_SECRET")
    with caplog.at_level("WARNING", logger="app.access"):
        importlib.reload(access)
    assert "MPB_SECRET nicht gesetzt" in caplog.text
    assert access.verify_user(access.sign_user("admin")) == "admin"
    assert access.verify_user(old) is None

    monkeypatch.setenv("MPB_SECRET", TEST_SECRET)
    importlib.reload(access)
    assert access.verify_user(old) == "cfo"


# ---------------------------------------------------------------------------
# Fix 3: Ordner ist die einzige Wahrheit, allgemein ist die Lobby
# ---------------------------------------------------------------------------


def test_oeffentlich_in_finance_sehen_nur_finance_leser(client):
    import app.access as access
    import app.wiki as wiki
    from app.access import PageMeta

    wiki.save_page("finance-faq", "Finance FAQ", "Zinsinfos Sonderwort Kalkulationsbasis",
                   PageMeta(erstellt_von="cfo", vertraulichkeit="oeffentlich", domaene="finance"))
    q = "Zinsinfos Sonderwort Kalkulationsbasis"

    for uid, cookies in (("gast", {}), ("mitarbeiter", as_user("mitarbeiter"))):
        assert "finance-faq" not in {p.slug for p in wiki.list_pages(uid)}, uid
        assert wiki.get_page_for("finance-faq", uid) is None, uid
        assert wiki.search_snippets(q, uid, top_k=50) == [], uid
        r = client.get("/", cookies=cookies)
        assert "finance-faq" not in sidebar_slugs(r.text) and "Finance FAQ" not in r.text, uid
        r404 = client.get("/wiki/finance-faq", cookies=cookies)
        assert r404.status_code == 404, uid
        assert r404.text == client.get("/wiki/gibt-es-nicht", cookies=cookies).text
        r = client.post("/ask", cookies=cookies, data={"question": q})
        assert "Finance FAQ" not in r.text.split("</form>", 1)[1], uid

    assert "finance-faq" in {p.slug for p in wiki.list_pages("cfo")}
    assert any(s.page.slug == "finance-faq" for s in wiki.search_snippets(q, "cfo", top_k=50))
    assert client.get("/wiki/finance-faq", cookies=as_user("cfo")).status_code == 200

    # Lobby: oeffentlich in allgemein sieht der Gast weiterhin, intern dort nicht
    assert client.get("/wiki/oeffentlich").status_code == 200
    assert sidebar_slugs(client.get("/").text) == {"oeffentlich"}
    assert client.get("/wiki/altbestand").status_code == 404
    assert access.readable_domains("gast") == ["allgemein"]
    assert access.readable_domains("mitarbeiter") == ["allgemein", "projekt"]
    assert access.readable_domains("cfo")[0] == "allgemein"
    # die alte Ausnahme (Kopf-Lesen in fremden Ordnern) ist weg
    assert not hasattr(wiki, "_header_is_public")


def test_oeffentlicher_vorschlag_in_finance_nur_fuer_finance(client):
    """Dieselbe Regel fuer Vorschlaege: das Label oeffnet keine fremde Domaene."""
    import app.proposals as proposals

    r = client.post("/proposals/new", cookies=as_user("cfo"), data={
        "project_name": "Offenes Sparprogramm", "description": "Sparwort Geheimzahl",
        "domaene": "finance", "vertraulichkeit": "oeffentlich", "empfaenger": "",
    })
    assert r.status_code == 303
    slug = "offenes-sparprogramm"
    for cookies in ({}, as_user("mitarbeiter")):
        r = client.get("/proposals", cookies=cookies)
        assert "Offenes Sparprogramm" not in r.text and slug not in r.text
        assert client.get(f"/proposals/{slug}", cookies=cookies).status_code == 404
    assert [p.slug for p in proposals.list_proposals("gast")] == []
    assert [p.slug for p in proposals.list_proposals("cfo")] == [slug]
    assert client.get(f"/proposals/{slug}", cookies=as_user("cfo")).status_code == 200


# ---------------------------------------------------------------------------
# Klein: Admin-Aussperrung, Slug-Validierung
# ---------------------------------------------------------------------------


def test_admin_kann_sich_gruppe_admin_nicht_selbst_entziehen(client):
    import app.access as access

    r = client.post("/admin/users/save", cookies=as_user("admin"),
                    data={"user_id": "admin", "name": "Administrator", "gruppen": ["alle"]})
    assert r.status_code == 303
    assert r.headers["location"] == "/admin?meldung=admin-selbst"
    assert access.is_admin("admin")
    assert access.read_changelog() == []
    r = client.get("/admin?meldung=admin-selbst", cookies=as_user("admin"))
    assert "nicht selbst entziehen" in r.text
    # auch ohne Gruppen-Feld (leere Auswahl) bleibt admin admin
    r = client.post("/admin/users/save", cookies=as_user("admin"), data={"user_id": "admin"})
    assert r.headers["location"] == "/admin?meldung=admin-selbst"
    assert access.is_admin("admin")

    # einen ANDEREN Admin darf er entmachten (keine Aussperrung des Systems)
    r = client.post("/admin/users/new", cookies=as_user("admin"),
                    data={"user_id": "admin2", "name": "Zweiter", "gruppen": ["alle", "admin"]})
    assert r.headers["location"] == "/admin?meldung=gespeichert"
    r = client.post("/admin/users/save", cookies=as_user("admin"),
                    data={"user_id": "admin2", "name": "Zweiter", "gruppen": ["alle"]})
    assert r.headers["location"] == "/admin?meldung=gespeichert"
    assert not access.is_admin("admin2")


def test_ungueltige_slugs_sind_404(client, tmp_path):
    import app.proposals as proposals
    import app.wiki as wiki

    assert wiki.is_valid_slug("budget-finance")
    for bad in ("..", "../budget-finance", "Budget-Finance", "a b", "x.md", "", "..%2f", "budget_finance"):
        assert not wiki.is_valid_slug(bad), bad
        assert wiki.get_page(bad) is None, bad
        assert wiki.get_page_for(bad, "cfo") is None, bad
        assert not wiki.slug_exists(bad), bad
        assert proposals.get_proposal(bad) is None, bad

    # Traversal-Koeder ausserhalb der Ablagen: darf ueber keinen Slug erreichbar sein
    (tmp_path / "geheim.md").write_text("# Geheim\n\nAusserhalb\n", encoding="utf-8")
    assert proposals.get_proposal("../geheim") is None
    assert wiki.get_page("../geheim") is None

    # Ein rohes "/wiki/.." loest bereits der HTTP-Client zu "/" auf (RFC 3986) und
    # erreicht die Route nie; die kodierte Form %2e%2e kommt als ".." beim Slug an.
    # Serverseitig ist "/wiki/.." per `curl --path-as-is` ebenfalls 404 (Slug-Check).
    c = as_user("cfo")
    for slug in ("%2e%2e", "..%2F..%2Fpermissions", "%2e%2e%2Fgeheim", "Budget-Finance", "x.md"):
        for url in (f"/wiki/{slug}", f"/wiki/{slug}/edit", f"/proposals/{slug}"):
            r = client.get(url, cookies=c)
            assert r.status_code == 404, (url, r.status_code)
            assert "Geheim" not in r.text and "Ausserhalb" not in r.text
        assert client.post(f"/wiki/{slug}/delete", cookies=c).status_code == 404
        assert client.post(f"/proposals/{slug}/delete", cookies=c).status_code == 404
