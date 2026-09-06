"""Datenaufbereitung fuer die Wissensuebersicht (/dashboard).

Ein Aufruf, ein Datenpaket: `build_overview(user, modus)` liefert alles, was die
Seite zeigt - Graph, Abteilungsstatistik, Wortwolke, Artikeltabelle, Scans und
Projektantraege.

Sicherheitsregel wie ueberall (docs/berechtigungen-stufe-2-admin-und-ablage.md):
Jede Zahl, jedes Wort und jede Zeile stammt aus den GEFILTERTEN Quellen
`wiki.list_pages(user)` und `proposals.list_proposals(user)`. Die einzige
Ausnahme ist der anonymisierte Graphteil, und die liegt gebuendelt in
`graph._hidden_documents` - hier wird sie nur durchgereicht, nie erweitert:
verborgene Dokumente erscheinen ausschliesslich als Anzahl je Abteilung, nie in
der Tabelle und nie in der Wortwolke.
"""
from __future__ import annotations

from typing import Any

from . import access, graph as graph_mod, proposals, stats as stats_mod, scans, usage, wiki

WORDCLOUD_SIZE = 40
WORDCLOUD_MIN_PX = 13
WORDCLOUD_MAX_PX = 32
MAX_SIMILAR_SHOWN = 3


# ---------------------------------------------------------------------------
# Bearbeitungen: Git-Historie und Frontmatter zusammenfuehren
# ---------------------------------------------------------------------------


def _merge_edits(page: wiki.Page) -> list[dict[str, str]]:
    """Alle bekannten Bearbeitungen einer Seite, neueste zuerst.

    Zwei Quellen, weil keine allein reicht: Git kennt jede Aenderung, aber nur
    fuer committete Dateien (frisch hochgeladene Seiten fehlen komplett). Das
    Frontmatter kennt Anlage und letzte Aenderung, aber nichts dazwischen.
    Zusammengefuehrt und dedupliziert ueber (Person, Minute) - derselbe
    Speichervorgang taucht sonst zweimal auf.

    Nutzer-IDs werden ueber `access.user_name` zu Anzeigenamen; Git-Autoren
    stehen ohnehin schon als Name in der Historie.
    """
    roh: list[tuple[str, str]] = []
    for autor, zeit in stats_mod._git_history(page):
        roh.append((autor, zeit))
    meta = page.meta
    if meta.erstellt_von and meta.erstellt_von != access.UNKNOWN_CREATOR:
        roh.append((access.user_name(meta.erstellt_von), meta.erstellt_am))
    if meta.geaendert_von:
        roh.append((access.user_name(meta.geaendert_von), meta.geaendert_am))

    gesehen: set[tuple[str, str]] = set()
    out: list[dict[str, str]] = []
    for person, zeit in roh:
        person = (person or "").strip()
        if not person:
            continue
        schluessel = (person.lower(), (zeit or "")[:16])
        if schluessel in gesehen:
            continue
        gesehen.add(schluessel)
        out.append({"person": person, "zeit": zeit or ""})
    out.sort(key=lambda e: e["zeit"], reverse=True)
    return out


# ---------------------------------------------------------------------------
# Anlagen und Links aus dem (bereits gefilterten) Graphen
# ---------------------------------------------------------------------------


def _attachment_index(data: dict[str, Any]) -> dict[str, dict[str, list]]:
    """Je Knoten die Nachbarn nach Kantenart - nur sichtbare Dokumentknoten.

    Verborgene Platzhalter (`type: hidden`) tragen ohnehin nur die Kante zum
    Domaenen-Hub; sie werden hier zusaetzlich hart ausgeschlossen, damit ein
    kuenftiger Umbau am Graphen sie nicht versehentlich in die Tabelle spuelt.
    """
    knoten = {n["id"]: n for n in data["nodes"]}
    index: dict[str, dict[str, list]] = {}
    for link in data["links"]:
        if link["kind"] not in (graph_mod.KIND_LINK, graph_mod.KIND_SIMILAR):
            continue
        for a, b in ((link["source"], link["target"]), (link["target"], link["source"])):
            ziel = knoten.get(b)
            if not ziel or ziel["type"] not in ("page", "proposal"):
                continue
            eintrag = index.setdefault(a, {graph_mod.KIND_LINK: [], graph_mod.KIND_SIMILAR: []})
            eintrag[link["kind"]].append({
                "titel": ziel["label"],
                "url": ziel.get("url", ""),
                "gewicht": link.get("weight", 0),
            })
    return index


def _anlagen(page: wiki.Page, index: dict[str, dict[str, list]]) -> dict[str, Any]:
    eintrag = index.get(graph_mod.page_id(page.slug), {})
    verlinkt = sorted(eintrag.get(graph_mod.KIND_LINK, []), key=lambda e: e["titel"].lower())
    aehnlich = sorted(
        eintrag.get(graph_mod.KIND_SIMILAR, []),
        key=lambda e: (-e["gewicht"], e["titel"].lower()),
    )[:MAX_SIMILAR_SHOWN]
    datei = page.meta.original_datei
    return {
        "verlinkt": verlinkt,
        "aehnlich": aehnlich,
        "original_datei": datei,
        "anzahl": len(verlinkt) + len(aehnlich) + (1 if datei else 0),
    }


# ---------------------------------------------------------------------------
# Wortwolke
# ---------------------------------------------------------------------------


def build_wordcloud(pages: list[wiki.Page]) -> list[dict[str, Any]]:
    """Haeufigste Woerter der SICHTBAREN Seiten.

    Gezaehlt wird je Seite einmal (Dokumenthaeufigkeit, `wiki._tokenize`
    liefert ohnehin eine Menge) - ein Wort, das in einer einzigen Seite hundert
    Mal steht, dominiert die Wolke dadurch nicht. Stoppwoerter und kurze
    Woerter kommen aus `graph.py`, damit Graph und Wolke dieselbe Sprache
    sprechen.
    """
    zaehler: dict[str, int] = {}
    for page in pages:
        for token in wiki._tokenize(f"{page.title} {page.content}"):
            if len(token) < graph_mod.MIN_TOKEN_LENGTH or token in graph_mod.STOPWORDS:
                continue
            if token.isdigit():
                continue
            zaehler[token] = zaehler.get(token, 0) + 1
    top = sorted(zaehler.items(), key=lambda kv: (-kv[1], kv[0]))[:WORDCLOUD_SIZE]
    if not top:
        return []
    hoechste = top[0][1]
    niedrigste = top[-1][1]
    spanne = max(1, hoechste - niedrigste)
    return [
        {
            "wort": wort,
            "anzahl": anzahl,
            "groesse": round(
                WORDCLOUD_MIN_PX
                + (WORDCLOUD_MAX_PX - WORDCLOUD_MIN_PX) * ((anzahl - niedrigste) / spanne),
                1,
            ),
        }
        for wort, anzahl in top
    ]


# ---------------------------------------------------------------------------
# Abteilungen (= Domaenen)
# ---------------------------------------------------------------------------


def build_departments(
    pages: list[wiki.Page],
    props: list[Any],
    graph_data: dict[str, Any],
) -> list[dict[str, Any]]:
    zeilen: dict[str, dict[str, Any]] = {}

    def zeile(dom: str) -> dict[str, Any]:
        return zeilen.setdefault(
            dom, {"domaene": dom, "seiten": 0, "vorschlaege": 0, "verborgen": 0}
        )

    for page in pages:
        zeile(page.meta.domaene or access.LOBBY_DOMAIN)["seiten"] += 1
    for p in props:
        zeile(p.meta.domaene or access.LOBBY_DOMAIN)["vorschlaege"] += 1
    # Verborgene Dokumente: nur die Anzahl je Abteilung, mehr steht im Graphen
    # gar nicht drin (siehe graph._hidden_documents).
    for node in graph_data["nodes"]:
        if node["type"] == "hidden":
            zeile(node.get("domaene") or access.LOBBY_DOMAIN)["verborgen"] += 1

    out = list(zeilen.values())
    for z in out:
        z["sichtbar"] = z["seiten"] + z["vorschlaege"]
        z["gesamt"] = z["sichtbar"] + z["verborgen"]
    out.sort(key=lambda z: (-z["gesamt"], z["domaene"]))
    hoechste = max((z["gesamt"] for z in out), default=0) or 1
    for z in out:
        z["anteil_sichtbar"] = round(100 * z["sichtbar"] / hoechste, 1)
        z["anteil_verborgen"] = round(100 * z["verborgen"] / hoechste, 1)
    return out


# ---------------------------------------------------------------------------
# Artikeltabelle
# ---------------------------------------------------------------------------


def _recipient_labels(empfaenger: list[str]) -> list[str]:
    """Nutzer-IDs als Anzeigename, Gruppen unveraendert (die heissen so)."""
    bekannt = {u["id"] for u in access.list_users()}
    return [access.user_name(e) if e in bekannt else e for e in empfaenger]


def build_articles(user: str | None, pages: list[wiki.Page], graph_data: dict[str, Any]) -> list[dict[str, Any]]:
    index = _attachment_index(graph_data)
    zugriffe = usage.stats_for([p.slug for p in pages])
    artikel = []
    for page in pages:
        historie = _merge_edits(page)
        z = zugriffe.get(page.slug, {"views": 0, "last_view": "", "last_viewer": ""})
        artikel.append({
            "slug": page.slug,
            "titel": page.title,
            "url": f"/wiki/{page.slug}",
            "domaene": page.meta.domaene,
            "vertraulichkeit": page.meta.vertraulichkeit,
            "empfaenger": _recipient_labels(page.meta.empfaenger),
            "zugriffe": z["views"],
            "letzter_zugriff": z["last_view"],
            "letzter_zugriff_von": access.user_name(z["last_viewer"]) if z["last_viewer"] else "",
            "bearbeitungen": len(historie),
            "bearbeiter": len({e["person"].lower() for e in historie}),
            "letzte_bearbeitung": historie[0]["zeit"] if historie else "",
            "letzter_bearbeiter": historie[0]["person"] if historie else "",
            "anlagen": _anlagen(page, index),
            "erstellt_von": page.meta.erstellt_von,
            "ist_ersteller": bool(user) and page.meta.erstellt_von == user,
        })
    artikel.sort(key=lambda a: a["titel"].lower())
    return artikel


# ---------------------------------------------------------------------------
# Alles zusammen
# ---------------------------------------------------------------------------


def build_overview(user: str | None, modus: str = graph_mod.MODE_EIGEN) -> dict[str, Any]:
    """Das komplette Datenpaket der Wissensuebersicht aus Sicht von `user`.

    `modus` wird unveraendert an `graph.build_graph` gereicht - dort (und nur
    dort) wird geprueft, ob der Nutzer den anonymisierten Modus ueberhaupt
    sehen darf. Faellt die Pruefung negativ aus, kommt der Standardgraph
    zurueck, und alles Weitere hier arbeitet automatisch ohne verborgene Anteile.
    """
    pages = wiki.list_pages(user)
    props = proposals.list_proposals(user)
    graph_data = graph_mod.build_graph(user, modus)
    return {
        "graph": graph_data,
        "modus": graph_data["stats"]["modus"],
        "darf_anonymisiert": access.can_see_anonymized(user),
        "abteilungen": build_departments(pages, props, graph_data),
        "wortwolke": build_wordcloud(pages),
        "artikel": build_articles(user, pages, graph_data),
        "scans": scans.recent_scans(user),
        "proposals": stats_mod.get_proposal_stats(user or access.GUEST),
    }
