"""Wissensuebersicht (/dashboard, app/overview.py, app/usage.py, app/scans.py).

Kernfrage: Fasst die Seite Wissen zusammen, ohne dabei etwas zu verraten?
Eine Uebersicht ist gefaehrlicher als eine Einzelseite - sie zaehlt, sortiert
und verdichtet, und jede dieser Operationen kann Wissen ueber Dokumente
durchlassen, die der Nutzer nicht lesen darf. Die security-Tests pruefen
deshalb Tabelle, Wortwolke, Zugriffsprotokoll, Teilen und den anonymisierten
Graphmodus einzeln.
"""
from __future__ import annotations

import pytest

from tests.conftest import as_user

# Kunstwort, das es nur in einer Finance-Seite gibt: taucht es irgendwo in der
# Sicht des Mitarbeiters auf, leckt die Uebersicht.
KUNSTWORT = "zwirbelfink"


def _overview(user, modus="eigen"):
    import app.overview as overview

    return overview.build_overview(user, modus)


def _save(slug, title, text, **meta_kwargs):
    import app.wiki as wiki
    from app.access import PageMeta

    meta_kwargs.setdefault("erstellt_von", "projektmanager")
    meta_kwargs.setdefault("vertraulichkeit", "intern")
    meta_kwargs.setdefault("domaene", "allgemein")
    return wiki.save_page(slug, title, text, PageMeta(**meta_kwargs))


# ---------------------------------------------------------------------------
# (a) Tabelle folgt den Leserechten
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_tabelle_zeigt_finance_nur_dem_cfo(pages_env):
    mitarbeiter = {a["slug"] for a in _overview("mitarbeiter")["artikel"]}
    cfo = {a["slug"] for a in _overview("cfo")["artikel"]}
    assert "budget-finance" not in mitarbeiter
    assert "budget-finance" in cfo
    # Der CFO liest die BR-Ablage trotzdem nicht
    assert "br-protokoll" not in cfo


@pytest.mark.security
def test_dashboard_route_zeigt_keine_fremden_titel(client):
    r = client.get("/dashboard", cookies=as_user("mitarbeiter"))
    assert r.status_code == 200
    assert "Budget Finance" not in r.text
    assert "BR Protokoll" not in r.text

    r_cfo = client.get("/dashboard", cookies=as_user("cfo"))
    assert "Budget Finance" in r_cfo.text


# ---------------------------------------------------------------------------
# (b) Anonymisierter Modus: eine Berechtigung, serverseitig durchgesetzt
# ---------------------------------------------------------------------------


def _hidden(data):
    return [n for n in data["graph"]["nodes"] if n["type"] == "hidden"]


@pytest.mark.security
def test_mitarbeiter_bekommt_trotz_modus_keine_verborgenen_knoten(pages_env):
    """`mitarbeiter` ist nicht in `leitung` - der Parameter allein reicht nicht."""
    import app.access as access

    assert access.can_see_anonymized("mitarbeiter") is False
    data = _overview("mitarbeiter", "anonymisiert")
    assert _hidden(data) == []
    assert data["graph"]["stats"]["hidden"] == 0
    assert data["graph"]["stats"]["modus"] == "eigen"
    assert data["darf_anonymisiert"] is False


@pytest.mark.security
def test_api_graph_erzwingt_die_berechtigung_serverseitig(client):
    ohne_recht = client.get("/api/graph?modus=anonymisiert",
                            cookies=as_user("mitarbeiter")).json()
    normal = client.get("/api/graph", cookies=as_user("mitarbeiter")).json()
    # Byte fuer Byte dasselbe: der Modus existiert fuer ihn schlicht nicht.
    assert ohne_recht == normal

    mit_recht = client.get("/api/graph?modus=anonymisiert",
                           cookies=as_user("pmo-leitung")).json()
    assert [n for n in mit_recht["nodes"] if n["type"] == "hidden"]


@pytest.mark.security
def test_pmo_leitung_sieht_verborgene_ohne_jede_identitaet(pages_env):
    import app.access as access
    import app.proposals as proposals
    import app.wiki as wiki

    assert access.can_see_anonymized("pmo-leitung") is True
    data = _overview("pmo-leitung", "anonymisiert")
    verborgen = _hidden(data)

    # Anzahl stimmt mit den tatsaechlich verborgenen Dokumenten ueberein
    sichtbar = {p.slug for p in wiki.list_pages("pmo-leitung")}
    alle = {p.slug for p in wiki.list_pages()}
    sichtbar_props = {p.slug for p in proposals.list_proposals("pmo-leitung")}
    alle_props = {p.slug for p in proposals.list_proposals()}
    erwartet = len(alle - sichtbar) + len(alle_props - sichtbar_props)
    assert erwartet > 0, "Testaufbau: es muss verborgene Dokumente geben"
    assert len(verborgen) == erwartet
    assert data["graph"]["stats"]["hidden"] == erwartet

    verbotene_slugs = (alle - sichtbar) | (alle_props - sichtbar_props)
    verbotene_titel = {p.title for p in wiki.list_pages() if p.slug not in sichtbar}

    for node in verborgen:
        # Nur diese Felder, sonst nichts
        assert set(node) == {"id", "type", "label", "domaene", "vertraulichkeit"}
        assert node["label"] == "Verborgen"
        assert "url" not in node and "slug" not in node and "erstellt_von" not in node
        # Die Kennung ist ein Hash, nicht der Slug
        assert node["id"].startswith("hidden:")
        for slug in verbotene_slugs:
            assert slug not in node["id"]
        for titel in verbotene_titel:
            assert titel.lower() not in node["id"].lower()

    # Keine Kante ausser der zum Domaenen-Hub
    ids = {n["id"] for n in verborgen}
    hubs = {n["id"] for n in data["graph"]["nodes"] if n["type"] == "domain"}
    for link in data["graph"]["links"]:
        enden = {link["source"], link["target"]}
        if not (enden & ids):
            continue
        assert link["kind"] == "domain"
        assert len(enden & ids) == 1
        assert (enden - ids).pop() in hubs


@pytest.mark.security
def test_verborgene_dokumente_erscheinen_nie_in_tabelle_oder_wolke(pages_env):
    # br liest ausser dem Betriebsrat niemand - auch die Leitung nicht.
    _save("br-kunstwort", "BR Kunstwort",
          f"Das {KUNSTWORT} steht nur in dieser BR-Seite.",
          erstellt_von="betriebsrat", domaene="br")

    data = _overview("pmo-leitung", "anonymisiert")
    assert _hidden(data), "Testaufbau: es muss verborgene Dokumente geben"
    slugs = {a["slug"] for a in data["artikel"]}
    assert "br-kunstwort" not in slugs
    assert all(a["titel"] != "Verborgen" for a in data["artikel"])
    assert KUNSTWORT not in {w["wort"] for w in data["wortwolke"]}


def test_standardmodus_bleibt_unveraendert(pages_env):
    """`build_graph(user)` ohne Modus muss sich exakt wie bisher verhalten."""
    import app.graph as graph

    for user in ("gast", "mitarbeiter", "cfo", "pmo-leitung"):
        ohne = graph.build_graph(user)
        mit = graph.build_graph(user, graph.MODE_EIGEN)
        assert ohne["nodes"] == mit["nodes"]
        assert ohne["links"] == mit["links"]
        assert not [n for n in ohne["nodes"] if n["type"] == "hidden"]
        assert ohne["stats"]["hidden"] == 0


# ---------------------------------------------------------------------------
# (c) Zugriffsprotokoll
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_verbotener_aufruf_wird_nicht_gezaehlt(client):
    import app.usage as usage

    # 404 (existiert, aber verboten) und 404 (existiert gar nicht)
    assert client.get("/wiki/budget-finance", cookies=as_user("mitarbeiter")).status_code == 404
    assert client.get("/wiki/gibt-es-nicht", cookies=as_user("mitarbeiter")).status_code == 404

    zahlen = usage.stats_for(["budget-finance", "gibt-es-nicht"])
    assert zahlen["budget-finance"]["views"] == 0
    assert zahlen["gibt-es-nicht"]["views"] == 0


def test_erlaubter_aufruf_zaehlt_und_merkt_den_leser(client):
    import app.usage as usage

    assert client.get("/wiki/budget-finance", cookies=as_user("cfo")).status_code == 200
    assert client.get("/wiki/budget-finance", cookies=as_user("ceo")).status_code == 200

    zahlen = usage.stats_for(["budget-finance"])["budget-finance"]
    assert zahlen["views"] == 2
    assert zahlen["last_viewer"] == "ceo"
    assert zahlen["last_view"]


def test_zugriffszahlen_stehen_in_der_uebersicht(client):
    client.get("/wiki/budget-finance", cookies=as_user("cfo"))
    r = client.get("/dashboard", cookies=as_user("cfo"))
    assert r.status_code == 200

    daten = _overview("cfo")
    zeile = next(a for a in daten["artikel"] if a["slug"] == "budget-finance")
    assert zeile["zugriffe"] == 1
    assert zeile["letzter_zugriff_von"] == "CFO / Controlling"


# ---------------------------------------------------------------------------
# (d) Bearbeitungen aus dem Frontmatter, wenn Git nichts weiss
# ---------------------------------------------------------------------------


def test_bearbeitungszaehler_nutzt_frontmatter_ohne_git(pages_env):
    """Die Testseiten liegen in tmp_path, also ausserhalb jeder Git-Historie -
    gezaehlt werden muss trotzdem, sonst stuende die Tabelle voll auf Null."""
    import app.stats as stats

    daten = _overview("cfo")
    zeile = next(a for a in daten["artikel"] if a["slug"] == "budget-finance")
    seite = next(p for p in __import__("app.wiki", fromlist=["x"]).list_pages("cfo")
                 if p.slug == "budget-finance")
    assert stats._git_history(seite) == []          # wirklich keine Git-Historie
    assert zeile["bearbeitungen"] == 1
    assert zeile["bearbeiter"] == 1
    assert zeile["letzter_bearbeiter"] == "CFO / Controlling"
    assert zeile["letzte_bearbeitung"] == "2026-09-01T10:00:00"


def test_zweiter_bearbeiter_wird_mitgezaehlt(client):
    r = client.post("/wiki/budget-finance/edit", cookies=as_user("ceo"), data={
        "title": "Budget Finance", "content": "Neue Fassung.",
        "vertraulichkeit": "intern", "domaene": "finance", "empfaenger": "",
    })
    assert r.status_code == 303
    zeile = next(a for a in _overview("cfo")["artikel"] if a["slug"] == "budget-finance")
    assert zeile["bearbeitungen"] == 2
    assert zeile["bearbeiter"] == 2
    assert zeile["letzter_bearbeiter"] == "CEO / Strategie"


# ---------------------------------------------------------------------------
# (e) Teilen
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_nicht_ersteller_darf_nicht_teilen(client):
    """`oeffentlich` stammt von `system` - der Mitarbeiter darf sie lesen,
    aber nicht weiterreichen."""
    r = client.post("/wiki/oeffentlich/share", cookies=as_user("mitarbeiter"),
                    data={"empfaenger": "cfo"})
    assert r.status_code == 403

    import app.wiki as wiki
    assert wiki.get_page("oeffentlich").meta.empfaenger == []


@pytest.mark.security
def test_gast_darf_nicht_teilen(client):
    r = client.post("/wiki/oeffentlich/share", data={"empfaenger": "cfo"})
    assert r.status_code == 403


@pytest.mark.security
def test_teilen_auf_verbotene_seite_ist_404(client):
    r = client.post("/wiki/budget-finance/share", cookies=as_user("mitarbeiter"),
                    data={"empfaenger": "mitarbeiter"})
    assert r.status_code == 404


def test_ersteller_ergaenzt_empfaenger_und_empfaenger_sieht_die_seite(client):
    import app.wiki as wiki

    # Vorher: der Mitarbeiter sieht die vertrauliche Projektnotiz nicht
    assert client.get("/wiki/vertraulich-projekt",
                      cookies=as_user("mitarbeiter")).status_code == 404

    r = client.post("/wiki/vertraulich-projekt/share",
                    cookies=as_user("projektmanager"),
                    data={"empfaenger": "mitarbeiter"})
    assert r.status_code == 303
    assert "geteilt=" in r.headers["location"]

    meta = wiki.get_page("vertraulich-projekt").meta
    assert "pmo-leitung" in meta.empfaenger      # bestehender Empfaenger bleibt
    assert "mitarbeiter" in meta.empfaenger      # neuer kommt dazu
    assert meta.geaendert_von == "projektmanager"

    # Nachher sieht er sie
    assert client.get("/wiki/vertraulich-projekt",
                      cookies=as_user("mitarbeiter")).status_code == 200


def test_teilen_dedupliziert_empfaenger(client):
    import app.wiki as wiki

    for _ in range(2):
        client.post("/wiki/vertraulich-projekt/share",
                    cookies=as_user("projektmanager"),
                    data={"empfaenger": "mitarbeiter, pmo-leitung"})
    empf = wiki.get_page("vertraulich-projekt").meta.empfaenger
    assert empf.count("mitarbeiter") == 1
    assert empf.count("pmo-leitung") == 1


@pytest.mark.security
def test_teilen_kann_keine_fremde_domaene_setzen(client):
    """Das Formular kennt kein Domaenenfeld - ein untergeschobenes wird
    ignoriert, die Seite bleibt, wo sie ist."""
    import app.wiki as wiki

    r = client.post("/wiki/vertraulich-projekt/share",
                    cookies=as_user("projektmanager"),
                    data={"empfaenger": "mitarbeiter", "domaene": "finance",
                          "vertraulichkeit": "oeffentlich"})
    assert r.status_code == 303
    meta = wiki.get_page("vertraulich-projekt").meta
    assert meta.domaene == "projekt"
    assert meta.vertraulichkeit == "vertraulich"


def test_teilen_kann_auf_vertraulich_hochstufen(client):
    import app.wiki as wiki

    seite = _save("meine-notiz", "Meine Notiz", "Nur eine Notiz.",
                  erstellt_von="projektmanager", domaene="projekt")
    assert seite.meta.vertraulichkeit == "intern"

    r = client.post("/wiki/meine-notiz/share", cookies=as_user("projektmanager"),
                    data={"empfaenger": "pmo-leitung", "vertraulich": "1"})
    assert r.status_code == 303
    meta = wiki.get_page("meine-notiz").meta
    assert meta.vertraulichkeit == "vertraulich"
    assert meta.empfaenger == ["pmo-leitung"]
    # Write ⊆ Read: der Ersteller sieht seine Seite danach weiterhin
    assert client.get("/wiki/meine-notiz",
                      cookies=as_user("projektmanager")).status_code == 200


# ---------------------------------------------------------------------------
# (f) Alte Dashboard-Adresse
# ---------------------------------------------------------------------------


def test_projektantraege_leiten_auf_die_uebersicht_um(client):
    r = client.get("/dashboard/projektantraege")
    assert r.status_code == 308
    assert r.headers["location"] == "/dashboard#projektantraege"


def test_projektantraege_stehen_als_abschnitt_in_der_uebersicht(client):
    r = client.post("/proposals/new", cookies=as_user("projektmanager"), data={
        "project_name": "Uebersicht Demo", "description": "Ein Antrag für die Tabelle.",
        "domaene": "projekt", "vertraulichkeit": "intern", "empfaenger": "",
    })
    assert r.status_code == 303
    d = client.get("/dashboard", cookies=as_user("projektmanager"))
    assert 'id="projektantraege"' in d.text
    assert "Uebersicht Demo" in d.text


# ---------------------------------------------------------------------------
# (g) Wortwolke leckt nichts
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_wortwolke_enthaelt_kein_wort_aus_verborgenen_seiten(pages_env):
    _save("finance-kunstwort", "Finance Kunstwort",
          f"Das {KUNSTWORT} kommt ausschliesslich in dieser Finance-Seite vor.",
          erstellt_von="cfo", domaene="finance")

    woerter_mitarbeiter = {w["wort"] for w in _overview("mitarbeiter")["wortwolke"]}
    assert KUNSTWORT not in woerter_mitarbeiter

    woerter_cfo = {w["wort"] for w in _overview("cfo")["wortwolke"]}
    assert KUNSTWORT in woerter_cfo


def test_wortwolke_verlinkt_auf_die_frage(client):
    r = client.get("/dashboard", cookies=as_user("mitarbeiter"))
    assert "/ask?q=" in r.text


def test_ask_uebernimmt_den_query_parameter(client):
    r = client.get("/ask?q=budget", cookies=as_user("mitarbeiter"))
    assert r.status_code == 200
    assert 'value="budget"' in r.text


# ---------------------------------------------------------------------------
# (h) Scans
# ---------------------------------------------------------------------------


def test_demo_eintraege_sind_als_demo_gekennzeichnet(pages_env):
    import app.scans as scans

    eintraege = scans.recent_scans("mitarbeiter")
    demo = [e for e in eintraege if e["demo"]]
    assert len(demo) == len(scans.DEMO_SOURCES)
    assert scans.scans_path().exists()          # beim ersten Aufruf angelegt
    for e in demo:
        assert e["demo"] is True
        assert e["quelle"] and e["anzahl"] and e["status"]


@pytest.mark.security
def test_upload_eintraege_nur_aus_lesbaren_domaenen(pages_env):
    import app.scans as scans
    import app.wiki as wiki

    wiki.save_uploaded_file("kostenplan.xlsx", b"x", domaene="finance")
    wiki.save_uploaded_file("projektplan.docx", b"y", domaene="projekt")

    quellen_mitarbeiter = " ".join(
        e["quelle"] for e in scans.recent_scans("mitarbeiter") if not e["demo"]
    )
    assert "kostenplan.xlsx" not in quellen_mitarbeiter
    assert "projektplan.docx" in quellen_mitarbeiter

    quellen_cfo = " ".join(
        e["quelle"] for e in scans.recent_scans("cfo") if not e["demo"]
    )
    assert "kostenplan.xlsx" in quellen_cfo


def test_scans_stehen_auf_der_uebersicht(client):
    r = client.get("/dashboard", cookies=as_user("mitarbeiter"))
    assert "Zuletzt gescannt" in r.text
    assert "Demo" in r.text


# ---------------------------------------------------------------------------
# Abteilungen, Anlagen, Gast
# ---------------------------------------------------------------------------


def test_abteilungen_zaehlen_seiten_und_vorschlaege(pages_env):
    daten = _overview("cfo")
    nach_domaene = {a["domaene"]: a for a in daten["abteilungen"]}
    assert nach_domaene["finance"]["seiten"] == 1
    assert "br" not in nach_domaene          # nicht lesbar, also nicht gezaehlt
    for a in daten["abteilungen"]:
        assert a["verborgen"] == 0           # Standardmodus


def test_abteilungen_zeigen_verborgene_anzahl_im_anonymen_modus(pages_env):
    daten = _overview("pmo-leitung", "anonymisiert")
    verborgen_gesamt = sum(a["verborgen"] for a in daten["abteilungen"])
    assert verborgen_gesamt == daten["graph"]["stats"]["hidden"]
    br = next((a for a in daten["abteilungen"] if a["domaene"] == "br"), None)
    assert br is not None and br["verborgen"] >= 1
    assert br["sichtbar"] == 0               # nur die Anzahl, kein Inhalt


def test_anlagen_zeigen_verlinkte_und_aehnliche_seiten(pages_env):
    _save("quelle-mit-link", "Quelle mit Link",
          "Verweis auf [[Oeffentliche Testseite]].")
    zeile = next(a for a in _overview("mitarbeiter")["artikel"]
                 if a["slug"] == "quelle-mit-link")
    assert zeile["anlagen"]["anzahl"] >= 1
    assert any(l["titel"] == "Oeffentliche Testseite" for l in zeile["anlagen"]["verlinkt"])


@pytest.mark.security
def test_anlagen_verlinken_nie_auf_verbotene_seiten(pages_env):
    _save("quelle-mit-link", "Quelle mit Link",
          "Verweis auf [[budget-finance]] und [[Oeffentliche Testseite]].")
    zeile = next(a for a in _overview("mitarbeiter")["artikel"]
                 if a["slug"] == "quelle-mit-link")
    alle = zeile["anlagen"]["verlinkt"] + zeile["anlagen"]["aehnlich"]
    assert all("budget-finance" not in l["url"] for l in alle)
    assert all(l["titel"] != "Budget Finance" for l in alle)


def test_gast_sieht_die_uebersicht_ohne_aktionen(client):
    r = client.get("/dashboard")
    assert r.status_code == 200
    assert "Als Gast kannst du nur lesen" in r.text
    assert "dialog-teilen" not in r.text
    assert "Oeffentliche Testseite" in r.text     # die oeffentliche Seite schon
    assert "Budget Finance" not in r.text


# ---------------------------------------------------------------------------
# Die neue Berechtigung darf nicht durch eine Rechteaenderung verschwinden
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_admin_speichern_behaelt_den_graph_abschnitt(client):
    """`render_permissions` schrieb frueher nur gruppen/nutzer/domaenen - eine
    beliebige Rechteaenderung haette `graph.anonymisiert_sehen` (und die
    Vertraulichkeitsstufen) stillschweigend geloescht und damit allen das Recht
    entzogen."""
    import app.access as access

    assert access.can_see_anonymized("pmo-leitung") is True

    r = client.post("/admin/groups/new", cookies=as_user("admin"),
                    data={"gruppe": "revision"})
    assert r.status_code == 303

    access.clear_cache()
    daten = access.load_permissions()
    assert daten["graph"]["anonymisiert_sehen"] == ["leitung", "admin"]
    assert "vertraulichkeitsstufen" in daten
    assert access.can_see_anonymized("pmo-leitung") is True
