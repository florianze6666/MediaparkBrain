"""Geometrie des Wissensgraphen (Wissen-Seite).

Der Graph ist ein sternfoermiges Netz: Wissensbasis in der Mitte, Domaenen auf
einem Ring, ihre Dokumente nach aussen aufgefaechert. Die Positionen sind
Prozentwerte, die Knoten haben aber feste Pixelgroessen - stimmt die Geometrie
nicht, ueberlappen die Beschriftungen oder werden am Rand abgeschnitten. Genau
das laesst sich hier ohne Browser pruefen.

Geprueft wird der dichte Fall (jede Domaene voll mit Dokumenten), nicht der
duenne Demo-Korpus: Am Bildschirm faellt eine Ueberlappung erst auf, wenn
jemand genug hochgeladen hat.
"""
from __future__ import annotations

import pytest

from app import kompass, wiki
from app.access import PageMeta


def _page(slug: str, titel: str, domaene: str) -> wiki.Page:
    return wiki.Page(slug=slug, title=titel, content="Text",
                     meta=PageMeta(domaene=domaene, geaendert_am="2026-01-01"))


def _dichter_korpus(pro_domaene: int = 9) -> list[wiki.Page]:
    """Jede Domaene voller als GRAPH_MAX_DOCS - erzwingt auch den "+N weitere"-Knoten."""
    seiten = []
    for dom in kompass.access.list_domains():
        for i in range(pro_domaene):
            seiten.append(_page(f"{dom}-{i}",
                                f"Dokument {i} mit einem langen Titel in {dom}", dom))
    return seiten


def _boxen(graph: dict) -> list[tuple[str, float, float, float, float]]:
    """Knoten als Rechtecke in Pixeln der gedachten Flaeche."""
    w = float(graph["min_px"])
    h = w / graph["ratio"]
    out = []
    for n in graph["nodes"]:
        bw, bh = kompass._node_box(n)
        cx, cy = n["x"] / 100 * w, n["y"] / 100 * h
        out.append((n["label"], cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2))
    return out


@pytest.fixture
def graph() -> dict:
    return kompass._graph("demo", _dichter_korpus())


def test_zentrum_und_alle_domaenen_sind_vertreten(graph: dict) -> None:
    arten = [n["kind"] for n in graph["nodes"]]
    assert arten.count("project") == 1, "genau ein Zentrum"
    domaenen = {n["id"] for n in graph["nodes"] if n["kind"] in ("dept", "dept-outline")}
    assert domaenen == set(kompass.access.list_domains())


def test_keine_knoten_ueberlappen_sich(graph: dict) -> None:
    boxen = _boxen(graph)
    kollisionen = [
        f"{a[0]!r} / {b[0]!r}"
        for i, a in enumerate(boxen)
        for b in boxen[i + 1:]
        if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]
    ]
    assert not kollisionen, "ueberlappende Knoten: " + ", ".join(kollisionen[:5])


def test_alle_knoten_liegen_in_der_flaeche(graph: dict) -> None:
    w = float(graph["min_px"])
    h = w / graph["ratio"]
    draussen = [
        b[0] for b in _boxen(graph)
        if b[1] < 0 or b[2] < 0 or b[3] > w or b[4] > h
    ]
    assert not draussen, "abgeschnittene Knoten: " + ", ".join(draussen[:5])


def test_jede_kante_endet_an_einem_knoten(graph: dict) -> None:
    punkte = {(n["x"], n["y"]) for n in graph["nodes"]}
    for e in graph["edges"]:
        assert (e["x1"], e["y1"]) in punkte, "Kante beginnt im Nichts"
        assert (e["x2"], e["y2"]) in punkte, "Kante endet im Nichts"


def test_gesperrte_domaene_zeigt_keine_dokumente() -> None:
    # betriebsrat sieht br, aber z.B. finance nicht.
    graph = kompass._graph("betriebsrat", _dichter_korpus())
    gesperrt = {n["dept"] for n in graph["nodes"] if n["kind"] == "dept-outline"}
    assert gesperrt, "Testnutzer muss mindestens eine gesperrte Domaene haben"
    dokument_domaenen = {n["dept"] for n in graph["nodes"] if n["kind"] == "doc"}
    assert not (dokument_domaenen & gesperrt)


def test_layout_ist_deterministisch() -> None:
    a = kompass._graph("demo", _dichter_korpus())
    b = kompass._graph("demo", _dichter_korpus())
    assert a == b
