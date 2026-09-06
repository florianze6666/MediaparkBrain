"""Wissensgraph (app/graph.py, /graph, /api/graph).

Kernfrage dieser Tests: Zeigt der Graph jedem Nutzer nur, was er sehen darf?
Ein Graph ist dabei gefaehrlicher als eine Liste - er verraet Zusammenhaenge
auch dann, wenn der Inhalt verborgen bleibt. Deshalb pruefen die
security-Tests nicht nur, dass verbotene Seiten fehlen, sondern auch, dass
weder Domaenen-Hub noch Kante ihre Existenz verraten.
"""
from __future__ import annotations

import pytest

from tests.conftest import as_user


def _graph(user):
    import app.graph as graph

    return graph.build_graph(user)


def _ids(data, typ=None):
    return {n["id"] for n in data["nodes"] if typ is None or n["type"] == typ}


def _kinds(data, kind):
    return [l for l in data["links"] if l["kind"] == kind]


def _save(slug, title, text, **meta_kwargs):
    import app.wiki as wiki
    from app.access import PageMeta

    meta_kwargs.setdefault("erstellt_von", "projektmanager")
    meta_kwargs.setdefault("vertraulichkeit", "intern")
    meta_kwargs.setdefault("domaene", "allgemein")
    wiki.save_page(slug, title, text, PageMeta(**meta_kwargs))


# ---------------------------------------------------------------------------
# (a) Rechte: finance ist fuer den Mitarbeiter unsichtbar, fuer den CFO nicht
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_mitarbeiter_sieht_keine_finance_seite_und_keinen_finance_hub(pages_env):
    data = _graph("mitarbeiter")
    ids = _ids(data)
    assert "page:budget-finance" not in ids
    assert "domain:finance" not in ids
    # Auch keine Kante darf die Seite erwaehnen
    for link in data["links"]:
        assert "budget-finance" not in link["source"]
        assert "budget-finance" not in link["target"]
        assert link["source"] != "domain:finance" and link["target"] != "domain:finance"


@pytest.mark.security
def test_cfo_sieht_finance_seite_und_hub(pages_env):
    data = _graph("cfo")
    ids = _ids(data)
    assert "page:budget-finance" in ids
    assert "domain:finance" in ids
    assert {"source": "page:budget-finance", "target": "domain:finance",
            "kind": "domain", "weight": 1} in data["links"]
    # Der CFO liest die BR-Ablage trotzdem nicht (br: lesen [br])
    assert "page:br-protokoll" not in ids
    assert "domain:br" not in ids


# ---------------------------------------------------------------------------
# (b) Gast: nur oeffentliche Seiten aus der Lobby
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_gast_sieht_nur_oeffentliche_lobby_seiten(pages_env):
    data = _graph("gast")
    assert _ids(data, "page") == {"page:oeffentlich"}
    assert _ids(data, "proposal") == set()
    assert _ids(data, "domain") == {"domain:allgemein"}
    # Der interne Altbestand in derselben Domaene bleibt unsichtbar
    assert "page:altbestand" not in _ids(data)
    assert data["stats"]["seiten"] == 1


# ---------------------------------------------------------------------------
# (c) Wikilink nur, wenn das Ziel sichtbar ist
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_wikilink_auf_verbotene_seite_erzeugt_keine_kante(pages_env):
    _save("quelle-mit-link", "Quelle mit Link",
          "Verweis auf [[budget-finance]] und auf [[Oeffentliche Testseite]].")

    data = _graph("mitarbeiter")
    ids = _ids(data)
    assert "page:quelle-mit-link" in ids
    assert "page:budget-finance" not in ids
    link_pairs = {(l["source"], l["target"]) for l in _kinds(data, "link")}
    assert all("budget-finance" not in a and "budget-finance" not in b
               for a, b in link_pairs)
    # Das sichtbare Ziel wird dagegen verbunden (Titel-Schreibweise)
    assert ("page:quelle-mit-link", "page:oeffentlich") in link_pairs


def test_wikilink_auf_sichtbare_seite_erzeugt_kante(pages_env):
    _save("quelle-mit-link", "Quelle mit Link",
          "Verweis auf [[budget-finance]].", erstellt_von="cfo")

    data = _graph("cfo")
    kanten = _kinds(data, "link")
    assert len(kanten) == 1
    assert kanten[0]["weight"] == 3
    assert {kanten[0]["source"], kanten[0]["target"]} == {
        "page:quelle-mit-link", "page:budget-finance"}


def test_markdown_link_erzeugt_kante(pages_env):
    _save("md-quelle", "MD Quelle", "Siehe [Oeffentlich](/wiki/oeffentlich) im Wiki.")
    data = _graph("mitarbeiter")
    pairs = {frozenset((l["source"], l["target"])) for l in _kinds(data, "link")}
    assert frozenset(("page:md-quelle", "page:oeffentlich")) in pairs


# ---------------------------------------------------------------------------
# (d) Aehnlichkeit
# ---------------------------------------------------------------------------

AEHNLICH_A = (
    "Migration der Serverlandschaft auf Kubernetes. Container werden "
    "orchestriert, Deployment erfolgt automatisiert ueber Pipelines. "
    "Monitoring und Logging bleiben zentral."
)
AEHNLICH_B = (
    "Kubernetes Migration der Serverlandschaft: Container werden automatisiert "
    "deployed, Pipelines uebernehmen Deployment, Monitoring und Logging "
    "zentral orchestriert."
)
UNAEHNLICH = (
    "Kantinenordnung: Mittagessen zwischen zwoelf und vierzehn Uhr, Nachtisch "
    "freitags, Geschirr bitte zurueckbringen, Pfandbecher Rueckgabe am Tresen."
)


def test_aehnliche_seiten_bekommen_similar_kante(pages_env):
    _save("kubernetes-a", "Kubernetes A", AEHNLICH_A)
    _save("kubernetes-b", "Kubernetes B", AEHNLICH_B)
    _save("kantine", "Kantine", UNAEHNLICH)

    data = _graph("mitarbeiter")
    similar = {frozenset((l["source"], l["target"])) for l in _kinds(data, "similar")}
    assert frozenset(("page:kubernetes-a", "page:kubernetes-b")) in similar
    for anderes in ("page:kubernetes-a", "page:kubernetes-b"):
        assert frozenset(("page:kantine", anderes)) not in similar


def test_similar_kanten_haben_gewicht_und_grenzen(pages_env):
    import app.graph as graph

    _save("kubernetes-a", "Kubernetes A", AEHNLICH_A)
    _save("kubernetes-b", "Kubernetes B", AEHNLICH_B)

    data = _graph("mitarbeiter")
    zaehler: dict[str, int] = {}
    for link in _kinds(data, "similar"):
        assert link["weight"] >= graph.SIMILARITY_THRESHOLD
        for end in (link["source"], link["target"]):
            zaehler[end] = zaehler.get(end, 0) + 1
    assert all(v <= graph.MAX_SIMILAR_PER_NODE for v in zaehler.values())


# ---------------------------------------------------------------------------
# (e) Invariante: jede Kante zeigt auf existierende Knoten
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("user", ["gast", "mitarbeiter", "cfo", "betriebsrat",
                                  "pmo-leitung", "ceo", "admin"])
def test_alle_kanten_zeigen_auf_existierende_knoten(pages_env, user):
    import app.graph as graph

    data = _graph(user)
    ids = {n["id"] for n in data["nodes"]}
    for link in data["links"]:
        assert link["source"] in ids
        assert link["target"] in ids
        assert link["source"] != link["target"]
    assert graph.validate(data) is True


def test_stats_zaehlen_knoten_und_kanten(pages_env):
    data = _graph("mitarbeiter")
    stats = data["stats"]
    assert stats["seiten"] == len([n for n in data["nodes"] if n["type"] == "page"])
    assert stats["vorschlaege"] == len([n for n in data["nodes"] if n["type"] == "proposal"])
    assert stats["domaenen"] == len([n for n in data["nodes"] if n["type"] == "domain"])
    assert stats["kanten"] == len(data["links"])
    assert sum(stats["kanten_je_kind"].values()) == len(data["links"])


# ---------------------------------------------------------------------------
# (f) Routen
# ---------------------------------------------------------------------------


def test_graph_seite_liefert_button_und_skript(client):
    r = client.get("/graph")
    assert r.status_code == 200
    html = r.text
    assert "Wissensgraph" in html
    assert 'class="btn btn-graph"' in html
    assert "cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js" in html
    assert "/static/graph.js" in html
    assert "Sichtbar als" in html


def test_graph_button_steht_in_jeder_seitenleiste(client):
    r = client.get("/")
    assert r.status_code == 200
    assert 'href="/graph"' in r.text


def test_api_graph_liefert_json_mit_stats(client):
    r = client.get("/api/graph")
    assert r.status_code == 200
    data = r.json()
    assert set(data) == {"nodes", "links", "stats"}
    assert "kanten_je_kind" in data["stats"]


@pytest.mark.security
def test_api_graph_folgt_der_rolle(client):
    ohne = client.get("/api/graph").json()
    mitarbeiter = client.get("/api/graph", cookies=as_user("mitarbeiter")).json()
    cfo = client.get("/api/graph", cookies=as_user("cfo")).json()

    ids_gast = {n["id"] for n in ohne["nodes"]}
    ids_mitarbeiter = {n["id"] for n in mitarbeiter["nodes"]}
    ids_cfo = {n["id"] for n in cfo["nodes"]}

    assert "domain:finance" not in ids_gast
    assert "domain:finance" not in ids_mitarbeiter
    assert "domain:finance" in ids_cfo
    assert len(ids_gast) < len(ids_cfo)


# ---------------------------------------------------------------------------
# (g) Herkunft: `unbekannt` bekommt keinen Rollenknoten
# ---------------------------------------------------------------------------


def test_unbekannter_ersteller_bekommt_keinen_rollenknoten(pages_env):
    data = _graph("mitarbeiter")
    ids = _ids(data)
    assert "page:altbestand" in ids          # Altbestand ohne Frontmatter ist sichtbar
    assert "role:unbekannt" not in ids
    assert not [l for l in data["links"] if "unbekannt" in l["target"] or "unbekannt" in l["source"]]


def test_herkunft_kante_traegt_anzeigenamen(pages_env):
    data = _graph("cfo")
    rollen = {n["id"]: n["label"] for n in data["nodes"] if n["type"] == "role"}
    assert rollen.get("role:cfo") == "CFO / Controlling"
    herkunft = {(l["source"], l["target"]) for l in _kinds(data, "herkunft")}
    assert ("page:budget-finance", "role:cfo") in herkunft


@pytest.mark.security
def test_rollenknoten_nur_fuer_sichtbare_dokumente(pages_env):
    """Der Mitarbeiter sieht weder die BR- noch die Finance-Seite - also darf
    auch kein Rollenknoten verraten, dass Betriebsrat oder CFO etwas abgelegt haben."""
    data = _graph("mitarbeiter")
    ids = _ids(data, "role")
    assert "role:betriebsrat" not in ids
    assert "role:cfo" not in ids


def test_vorschlag_bekommt_eigenen_knoten_und_herkunft(client):
    r = client.post("/proposals/new", cookies=as_user("projektmanager"), data={
        "project_name": "Graph Demo", "description": "Ein Vorschlag fuer die Graphansicht.",
        "domaene": "projekt", "vertraulichkeit": "intern", "empfaenger": "",
    })
    assert r.status_code == 303

    data = client.get("/api/graph", cookies=as_user("projektmanager")).json()
    knoten = {n["id"]: n for n in data["nodes"]}
    assert "proposal:graph-demo" in knoten
    assert knoten["proposal:graph-demo"]["url"] == "/proposals/graph-demo"
    assert knoten["proposal:graph-demo"]["type"] == "proposal"
    herkunft = {(l["source"], l["target"]) for l in data["links"] if l["kind"] == "herkunft"}
    assert ("proposal:graph-demo", "role:projektmanager") in herkunft
    # Vorschlaege haengen ebenfalls an ihrem Domaenen-Hub, sonst schwimmen
    # Altbestands-Vorschlaege ohne Ersteller voellig frei im Bild.
    domain = {(l["source"], l["target"]) for l in data["links"] if l["kind"] == "domain"}
    assert ("proposal:graph-demo", "domain:projekt") in domain
    assert data["stats"]["vorschlaege"] >= 1


def test_kein_dokument_ohne_verbindung(client):
    """Jedes sichtbare Dokument haengt an mindestens einer Kante - ein Graph
    voller Einzelpunkte waere kein Graph."""
    data = client.get("/api/graph", cookies=as_user("projektmanager")).json()
    verbunden = set()
    for link in data["links"]:
        verbunden.add(link["source"])
        verbunden.add(link["target"])
    for node in data["nodes"]:
        if node["type"] in ("page", "proposal"):
            assert node["id"] in verbunden, node["id"]


@pytest.mark.security
def test_vorschlag_einer_fremden_domaene_fehlt_im_graph(client):
    r = client.post("/proposals/new", cookies=as_user("cfo"), data={
        "project_name": "Kostenprogramm", "description": "Nur fuer Finance.",
        "domaene": "finance", "vertraulichkeit": "intern", "empfaenger": "",
    })
    assert r.status_code == 303

    mitarbeiter = client.get("/api/graph", cookies=as_user("mitarbeiter")).json()
    assert not [n for n in mitarbeiter["nodes"] if n["id"] == "proposal:kostenprogramm"]
    cfo = client.get("/api/graph", cookies=as_user("cfo")).json()
    assert [n for n in cfo["nodes"] if n["id"] == "proposal:kostenprogramm"]
