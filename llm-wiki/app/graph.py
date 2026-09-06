"""Wissensgraph: Knoten und Kanten fuer die Graphansicht (/graph, /api/graph).

Sicherheitsregel (derselbe eine Zugriffsweg wie ueberall, siehe
docs/berechtigungen-stufe-2-admin-und-ablage.md, Abschnitt Sicherheitsbetrachtung):
Der Graph wird AUSSCHLIESSLICH aus `wiki.list_pages(user)` und
`proposals.list_proposals(user)` gebaut - also aus den bereits gefilterten
Listen (Ordner-Schranke + `decide` pro Dokument). Die ungefilterten Varianten
(`list_pages()` ohne Nutzer, `get_page`, `get_proposal`) werden hier nie
benutzt. Alles Weitere - Domaenen, Rollen, Kanten, Aehnlichkeiten - wird nur
aus diesen sichtbaren Dokumenten abgeleitet:

* ein Domaenen- oder Rollenknoten existiert nur, wenn mindestens ein sichtbares
  Dokument daran haengt (kein Knoten verraet die blosse Existenz einer Domaene,
  in die der Nutzer nicht schauen darf),
* eine Wikilink-Kante entsteht nur, wenn das Ziel im sichtbaren Set liegt
  (ein Link auf eine verbotene Seite ist im Graphen unsichtbar, nicht "grau"),
* Aehnlichkeit wird nur zwischen sichtbaren Dokumenten gerechnet.

Damit aendert sich der Graph beim Rollenwechsel in der Seitenleiste - das ist
der Demo-Punkt und zugleich die Probe aufs Exempel.
"""
from __future__ import annotations

import re
from typing import Any, Iterable

from . import access, proposals, wiki

# Kantenarten
KIND_DOMAIN = "domain"
KIND_HERKUNFT = "herkunft"
KIND_LINK = "link"
KIND_SIMILAR = "similar"

WEIGHT_DOMAIN = 1
WEIGHT_HERKUNFT = 1
WEIGHT_LINK = 3

# Aehnlichkeit: darunter ist es Rauschen, und pro Knoten bleiben nur die
# staerksten Kanten - sonst wird der Graph ein Filz statt einer Karte.
SIMILARITY_THRESHOLD = 0.08
MAX_SIMILAR_PER_NODE = 4
MIN_TOKEN_LENGTH = 4

WIKILINK_RE = re.compile(r"\[\[([^\]\[]{1,200})\]\]")
MDLINK_RE = re.compile(r"\]\(\s*/wiki/([a-z0-9-]+)\s*\)")

# Kleine deutsche Stoppwortliste. Kuerzere Woerter (< 4 Zeichen) fallen ohnehin
# weg, deshalb stehen hier fast nur laengere Fuellwoerter.
STOPWORDS = {
    "aber", "alle", "allem", "allen", "aller", "alles", "also", "andere",
    "anderen", "auch", "auf", "aus", "bei", "beim", "bereits", "bis", "dabei",
    "dafuer", "dafür", "daher", "damit", "dann", "darauf", "dass", "dazu",
    "denn", "deren", "dessen", "diese", "diesem", "diesen", "dieser", "dieses",
    "doch", "durch", "eben", "eine", "einem", "einen", "einer", "eines",
    "einige", "etwa", "etwas", "fuer", "für", "gegen", "haben", "hatte",
    "hier", "immer", "jede", "jeden", "jeder", "jedoch", "kann", "keine",
    "keinen", "koennen", "können", "mehr", "muss", "muessen", "müssen",
    "nach", "nicht", "noch", "oder", "ohne", "schon", "sein", "seine", "sich",
    "sind", "soll", "sollen", "sondern", "sowie", "ueber", "über", "unter",
    "viele", "vom", "von", "waehrend", "während", "weil", "weitere", "wenn",
    "werden", "wieder", "wird", "wurde", "wurden", "zudem", "zum", "zur",
    "zwar", "zwischen",
}


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------


def page_id(slug: str) -> str:
    return f"page:{slug}"


def proposal_id(slug: str) -> str:
    return f"proposal:{slug}"


def domain_id(name: str) -> str:
    return f"domain:{name}"


def role_id(user_id: str) -> str:
    return f"role:{user_id}"


def content_tokens(*parts: str) -> set[str]:
    """Tokens fuer den Aehnlichkeitsvergleich: `wiki._tokenize` (derselbe
    Tokenizer wie die Suche) minus Stoppwoerter und minus kurze Woerter."""
    text = " ".join(p for p in parts if p)
    return {
        t for t in wiki._tokenize(text)
        if len(t) >= MIN_TOKEN_LENGTH and t not in STOPWORDS
    }


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    union = len(a | b)
    if not union:
        return 0.0
    return len(a & b) / union


def _pair(a: str, b: str) -> tuple[str, str]:
    return (a, b) if a <= b else (b, a)


def _resolve_link_target(raw: str, by_slug: dict[str, str], by_title: dict[str, str]) -> str | None:
    """`[[slug]]` oder `[[Titel]]` -> Knoten-ID einer SICHTBAREN Seite, sonst None."""
    target = raw.strip()
    if not target:
        return None
    # `[[Titel|Anzeigetext]]` und `[[slug#Abschnitt]]` mitnehmen
    target = target.split("|", 1)[0].split("#", 1)[0].strip()
    if not target:
        return None
    if target in by_slug:
        return by_slug[target]
    return by_title.get(target.lower())


# ---------------------------------------------------------------------------
# Graph bauen
# ---------------------------------------------------------------------------


def build_graph(user: str | None) -> dict[str, Any]:
    """Knoten, Kanten und Statistik aus Sicht von `user`.

    Rueckgabe: {"nodes": [...], "links": [...], "stats": {...}}.
    Invariante (am Ende geprueft): jede Kante verweist auf existierende Knoten.
    """
    pages = wiki.list_pages(user)              # gefiltert - nie die Rohvariante
    props = proposals.list_proposals(user)     # gefiltert - nie die Rohvariante

    nodes: list[dict[str, Any]] = []
    node_ids: set[str] = set()
    links: list[dict[str, Any]] = []
    seen_edges: set[tuple[str, str, str]] = set()

    def add_node(node: dict[str, Any]) -> None:
        if node["id"] in node_ids:
            return
        node_ids.add(node["id"])
        nodes.append(node)

    def add_link(a: str, b: str, kind: str, weight: float) -> None:
        if a == b:
            return  # Selbstkanten nie
        s, t = _pair(a, b)
        key = (s, t, kind)
        if key in seen_edges:
            return  # keine Duplikate (ungerichtet)
        seen_edges.add(key)
        links.append({"source": a, "target": b, "kind": kind, "weight": weight})

    # --- Dokumentknoten ----------------------------------------------------
    for page in pages:
        add_node({
            "id": page_id(page.slug),
            "type": "page",
            "label": page.title,
            "slug": page.slug,
            "domaene": page.meta.domaene,
            "vertraulichkeit": page.meta.vertraulichkeit,
            "url": f"/wiki/{page.slug}",
            "erstellt_von": page.meta.erstellt_von,
        })

    for p in props:
        add_node({
            "id": proposal_id(p.slug),
            "type": "proposal",
            "label": p.project_name,
            "slug": p.slug,
            "domaene": p.meta.domaene,
            "vertraulichkeit": p.meta.vertraulichkeit,
            "url": f"/proposals/{p.slug}",
            "erstellt_von": p.meta.erstellt_von,
        })

    # --- Domaenen-Hubs: nur fuer sichtbare Dokumente -----------------------
    # Auch Vorschlaege haengen an ihrer Domaene. Ohne diese Kante haengen
    # Altbestands-Vorschlaege (erstellt_von "unbekannt", also ohne Rollenkante)
    # voellig frei im Bild - im echten Korpus sind das derzeit vier Knoten.
    def add_domain(doc_node_id: str, dom: str) -> None:
        if not dom:
            return
        did = domain_id(dom)
        add_node({"id": did, "type": "domain", "label": dom, "domaene": dom})
        add_link(doc_node_id, did, KIND_DOMAIN, WEIGHT_DOMAIN)

    for page in pages:
        add_domain(page_id(page.slug), page.meta.domaene)
    for p in props:
        add_domain(proposal_id(p.slug), p.meta.domaene)

    # --- Rollen-Hubs (Herkunft): `unbekannt` bekommt keinen Knoten ---------
    def add_origin(doc_node_id: str, creator: str) -> None:
        if not creator or creator == access.UNKNOWN_CREATOR:
            return
        rid = role_id(creator)
        add_node({
            "id": rid,
            "type": "role",
            "label": access.user_name(creator),
            "user_id": creator,
        })
        add_link(doc_node_id, rid, KIND_HERKUNFT, WEIGHT_HERKUNFT)

    for page in pages:
        add_origin(page_id(page.slug), page.meta.erstellt_von)
    for p in props:
        add_origin(proposal_id(p.slug), p.meta.erstellt_von)

    # --- Explizite Links zwischen sichtbaren Seiten ------------------------
    by_slug = {page.slug: page_id(page.slug) for page in pages}
    by_title: dict[str, str] = {}
    for page in pages:
        by_title.setdefault(page.title.strip().lower(), page_id(page.slug))

    explicit_pairs: set[tuple[str, str]] = set()
    for page in pages:
        src = page_id(page.slug)
        targets: set[str] = set()
        for raw in WIKILINK_RE.findall(page.content):
            hit = _resolve_link_target(raw, by_slug, by_title)
            if hit:
                targets.add(hit)
        for slug in MDLINK_RE.findall(page.content):
            # nur sichtbare Ziele - ein Link auf Verbotenes existiert im Graph nicht
            if slug in by_slug:
                targets.add(by_slug[slug])
        for target in targets:
            if target == src:
                continue
            explicit_pairs.add(_pair(src, target))
            add_link(src, target, KIND_LINK, WEIGHT_LINK)

    # --- Aehnlichkeit (page<->page, proposal<->page) -----------------------
    docs: list[tuple[str, str, set[str]]] = []
    for page in pages:
        docs.append((page_id(page.slug), "page", content_tokens(page.title, page.content)))
    for p in props:
        docs.append((proposal_id(p.slug), "proposal",
                     content_tokens(p.project_name, p.description)))

    candidates: list[tuple[float, str, str]] = []
    for i in range(len(docs)):
        id_a, type_a, tok_a = docs[i]
        for j in range(i + 1, len(docs)):
            id_b, type_b, tok_b = docs[j]
            if _pair(id_a, id_b) in explicit_pairs:
                continue  # expliziter Link ist die staerkere Aussage, keine Doppellinie
            score = jaccard(tok_a, tok_b)
            if score >= SIMILARITY_THRESHOLD:
                candidates.append((score, id_a, id_b))

    candidates.sort(key=lambda c: (-c[0], c[1], c[2]))
    used: dict[str, int] = {}
    for score, id_a, id_b in candidates:
        if used.get(id_a, 0) >= MAX_SIMILAR_PER_NODE:
            continue
        if used.get(id_b, 0) >= MAX_SIMILAR_PER_NODE:
            continue
        used[id_a] = used.get(id_a, 0) + 1
        used[id_b] = used.get(id_b, 0) + 1
        add_link(id_a, id_b, KIND_SIMILAR, round(score, 4))

    # --- Statistik ---------------------------------------------------------
    kanten_je_kind = {KIND_DOMAIN: 0, KIND_HERKUNFT: 0, KIND_LINK: 0, KIND_SIMILAR: 0}
    for link in links:
        kanten_je_kind[link["kind"]] = kanten_je_kind.get(link["kind"], 0) + 1

    stats = {
        "seiten": len(pages),
        "vorschlaege": len(props),
        "domaenen": sum(1 for n in nodes if n["type"] == "domain"),
        "rollen": sum(1 for n in nodes if n["type"] == "role"),
        "knoten": len(nodes),
        "kanten": sum(kanten_je_kind.values()),
        "kanten_je_kind": kanten_je_kind,
    }

    graph = {"nodes": nodes, "links": links, "stats": stats}
    validate(graph)
    return graph


def validate(graph: dict[str, Any]) -> bool:
    """Invariante: jede Kante verweist auf existierende Knoten, keine
    Selbstkanten, keine doppelte Kante gleicher Art. Wirft ValueError."""
    ids = {n["id"] for n in graph["nodes"]}
    seen: set[tuple[str, str, str]] = set()
    for link in graph["links"]:
        s, t = link["source"], link["target"]
        if s not in ids or t not in ids:
            raise ValueError(f"Kante zeigt auf unbekannten Knoten: {s} -> {t}")
        if s == t:
            raise ValueError(f"Selbstkante: {s}")
        key = (*_pair(s, t), link["kind"])
        if key in seen:
            raise ValueError(f"Doppelte Kante: {key}")
        seen.add(key)
    return True


def node_ids(nodes: Iterable[dict[str, Any]]) -> set[str]:
    return {n["id"] for n in nodes}
