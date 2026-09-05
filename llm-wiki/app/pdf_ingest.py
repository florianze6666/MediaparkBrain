"""PDF-Einlesen (Arbeitspaket 8).

Holt den Textlayer aus einem PDF und giesst ihn so in Markdown, dass die
Wortsuche in `wiki.search_snippets` damit etwas anfangen kann.

Bewusst **kein OCR**: Digital erzeugte PDFs - Exporte aus Word, Excel oder
PowerPoint, also praktisch alle Projektunterlagen - enthalten den Text bereits
exakt. OCR wuerde diese Seiten rastern und den Text neu raten, also exakte
Daten durch eine Schaetzung ersetzen. Bei Betraegen im Business Case ist das
schaedlich ("450 T€" wird zu "45O TE"). Fehlt der Textlayer, wird die Datei
deshalb abgelehnt und die Luecke benannt, statt sie zu ueberspielen
(PLAN.md §7, Phase 5).

Zwei PDF-Bauformen werden unterschieden, siehe docs/FUNKTIONSWEISE.md §6:

* ``folien``     - aus Praesentationsfolien exportiert. Eine Seite wird ein
                   Abschnitt, die Ueberschrift bleibt beim Text.
* ``fliesstext`` - Bericht, Angebot, Charter. Seitenumbraucke werden wieder
                   zusammengefuegt, Kopf- und Fusszeilen entfernt.
"""
from __future__ import annotations

import io
import re
from dataclasses import dataclass, field

import pdfplumber

# Die Leerpruefung fragt "gibt es ueberhaupt einen Textlayer?", nicht "ist es
# viel Text?". Folien tragen absichtlich wenig Text - eine Mengenschwelle
# wuerde einen voellig brauchbaren Foliensatz abweisen.
MIN_CHARS_TOTAL = 40
# Ein Scan liefert auf praktisch keiner Seite Text. Liegt der Anteil der
# Seiten mit Text darunter, ist es ein Bild-PDF (ggf. mit Textdeckblatt).
MIN_PAGES_WITH_TEXT = 0.3

# Ab wie vielen Woertern je Seite wir von Fliesstext statt von Folien ausgehen.
FLOW_WORDS_PER_PAGE = 120

# Eine Zeile gilt als Kopf-/Fusszeile, wenn sie auf mindestens so vielen
# Seiten identisch auftaucht (nur ab 3 Seiten sinnvoll pruefbar).
REPEAT_RATIO = 0.6
# ... und nur, wenn sie im oberen bzw. unteren Rand der Seite steht. Ohne
# diese Bedingung loescht die Wiederholungsregel echten Inhalt, sobald ein
# Satz im Dokument mehrfach identisch vorkommt.
MARGIN_BAND = 0.12

SENTENCE_END = re.compile(r"[.!?:;)\]]\s*$")


@dataclass
class PdfPage:
    """Eine Seite des PDFs, bereits aufgeraeumt.

    `entries` haelt zu jeder Zeile ihre vertikale Position, damit sich
    Kopf- und Fusszeilen am Seitenrand von Inhalt unterscheiden lassen.
    """

    number: int
    heading: str = ""
    lines: list[str] = field(default_factory=list)
    tables: list[list[list[str]]] = field(default_factory=list)
    entries: list[tuple[str, float]] = field(default_factory=list)
    height: float = 0.0

    @property
    def text(self) -> str:
        return "\n".join(self.lines)

    def in_margin(self, top: float) -> bool:
        if self.height <= 0:
            return False
        band = self.height * MARGIN_BAND
        return top <= band or top >= self.height - band


@dataclass
class PdfExtract:
    """Ergebnis des Einlesens."""

    title: str
    markdown: str
    pages: list[PdfPage]
    layout: str  # "folien" | "fliesstext" | "leer"
    char_count: int
    ok: bool
    reason: str = ""

    @property
    def page_count(self) -> int:
        return len(self.pages)


# ---------------------------------------------------------------------------
# Lesen
# ---------------------------------------------------------------------------


def _page_heading(page) -> str:
    """Groesste Schrift der Seite = Ueberschrift.

    Bei Folien traegt die Ueberschrift die Woerter, an denen die Wortsuche
    ueberhaupt greifen kann - Stichpunkte wie "ROI 3,16" tun das nicht.
    """
    try:
        words = page.extract_words(extra_attrs=["size"])
    except Exception:
        return ""
    if not words:
        return ""
    sizes = [w.get("size") or 0 for w in words]
    top_size = max(sizes)
    if top_size <= 0:
        return ""
    # Alles, was nah an der groessten Schrift liegt, gehoert zur Ueberschrift.
    head = [
        w["text"]
        for w in words
        if (w.get("size") or 0) >= top_size - 0.5 and w["top"] < page.height / 2
    ]
    heading = " ".join(head).strip()
    # Eine "Ueberschrift", die die halbe Seite umfasst, ist keine.
    return heading if 0 < len(heading) <= 120 else ""


def _read_pages(data: bytes) -> list[PdfPage]:
    pages: list[PdfPage] = []
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            entries: list[tuple[str, float]] = []
            try:
                for line in page.extract_text_lines() or []:
                    text = (line.get("text") or "").strip()
                    if text:
                        entries.append((text, float(line.get("top") or 0.0)))
            except Exception:
                # Aeltere/kaputte Seiten: ohne Positionen weitermachen.
                raw = page.extract_text() or ""
                entries = [(ln.strip(), 0.0) for ln in raw.splitlines() if ln.strip()]
            try:
                tables = [t for t in (page.extract_tables() or []) if t]
            except Exception:
                tables = []
            pages.append(
                PdfPage(
                    number=i,
                    heading=_page_heading(page),
                    lines=[t for t, _ in entries],
                    tables=tables,
                    entries=entries,
                    height=float(page.height or 0.0),
                )
            )
    return pages


def _drop_repeating_lines(pages: list[PdfPage]) -> None:
    """Kopf- und Fusszeilen entfernen.

    Sie wiederholen sich auf jeder Seite und wuerden sonst jedem Absatz
    denselben Firmennamen anhaengen - das verwaessert die Wortsuche, weil
    dann jede Seite auf jede Frage ein bisschen passt.
    """
    if len(pages) < 3:
        return
    # Nur Zeilen am oberen/unteren Seitenrand kommen ueberhaupt in Frage.
    counts: dict[str, int] = {}
    for p in pages:
        randzeilen = {t for t, top in p.entries if p.in_margin(top)}
        for line in randzeilen:
            counts[line] = counts.get(line, 0) + 1
    threshold = max(2, int(len(pages) * REPEAT_RATIO))
    repeating = {
        line
        for line, n in counts.items()
        # Lange Zeilen sind eher echter Inhalt als eine Fusszeile.
        if n >= threshold and len(line) <= 80
    }
    if not repeating:
        return
    for p in pages:
        p.entries = [
            (t, top)
            for t, top in p.entries
            if not (t in repeating and p.in_margin(top))
        ]
        p.lines = [t for t, _ in p.entries]


def _detect_layout(pages: list[PdfPage]) -> str:
    words = sum(len(p.text.split()) for p in pages)
    if not pages or not words:
        return "leer"
    return "fliesstext" if words / len(pages) >= FLOW_WORDS_PER_PAGE else "folien"


# ---------------------------------------------------------------------------
# Markdown erzeugen
# ---------------------------------------------------------------------------


def _table_to_markdown(table: list[list[str]]) -> str:
    rows = [[(c or "").replace("\n", " ").strip() for c in row] for row in table]
    rows = [r for r in rows if any(r)]
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    head, *body = rows
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * width]
    out += ["| " + " | ".join(r) + " |" for r in body]
    return "\n".join(out)


def _body_lines(page: PdfPage) -> list[str]:
    """Die Zeilen der Seite ohne die Ueberschrift.

    Die Ueberschrift steckt auch in `lines` und kann sich ueber mehrere
    extrahierte Zeilen ziehen; hier wird genau dieser Vorspann entfernt.
    """
    if not page.heading:
        return list(page.lines)
    acc = ""
    n = 0
    for line in page.lines:
        cand = f"{acc} {line}".strip() if acc else line
        if not page.heading.startswith(cand):
            break
        acc, n = cand, n + 1
        if acc == page.heading:
            break
    return page.lines[n:] if acc == page.heading else list(page.lines)


def _slides_to_markdown(pages: list[PdfPage]) -> str:
    """Eine Folie wird ein Abschnitt.

    Der Text einer Folie bleibt **ein** Absatz samt Ueberschrift: Stichpunkte
    sind einzeln zu wortarm, um gefunden zu werden. Zusammen mit der
    Ueberschrift tragen sie genug Woerter fuer einen Treffer.
    """
    blocks: list[str] = []
    for p in pages:
        body = " · ".join(_body_lines(p)).strip()
        heading = p.heading or f"Seite {p.number}"
        blocks.append(f"## {heading}\n\n*(Seite {p.number})* {body}".rstrip())
        for t in p.tables:
            md = _table_to_markdown(t)
            if md:
                blocks.append(md)
    return "\n\n".join(b for b in blocks if b.strip())


def _flow_to_markdown(pages: list[PdfPage]) -> str:
    """Fliesstext: Seitenumbrueche verschwinden wieder.

    Endet eine Seite mitten im Satz, gehoert die erste Zeile der naechsten
    Seite an denselben Absatz - sonst zerfaellt eine Aussage in zwei
    Halbsaetze, die einzeln nichts belegen.
    """
    paragraphs: list[str] = []
    tables: list[str] = []
    carry = ""

    def flush() -> None:
        nonlocal carry
        if carry.strip():
            paragraphs.append(carry.strip())
        carry = ""

    for p in pages:
        for t in p.tables:
            md = _table_to_markdown(t)
            if md:
                tables.append(md)
        # Eine Ueberschrift beginnt einen Abschnitt - sie darf nicht in den
        # laufenden Satz eingeschmolzen werden.
        if p.heading:
            flush()
            paragraphs.append(f"## {p.heading}")
        for line in p.lines if not p.heading else _body_lines(p):
            if carry and not SENTENCE_END.search(carry):
                carry = f"{carry} {line}"
            else:
                flush()
                carry = line
    flush()
    return "\n\n".join(paragraphs + tables)


def _title_from(pages: list[PdfPage], filename: str) -> str:
    for p in pages:
        if p.heading:
            return p.heading
        if p.lines:
            return p.lines[0][:120]
    return filename.rsplit(".", 1)[0]


# ---------------------------------------------------------------------------
# Oeffentliche Schnittstelle
# ---------------------------------------------------------------------------


def extract_pdf(data: bytes, filename: str = "dokument.pdf") -> PdfExtract:
    """Liest ein PDF ein.

    Kommt kein oder kaum Text heraus, ist `ok` False und `reason` nennt den
    Grund. Die Datei darf dann **nicht** als leere Seite gespeichert werden -
    das waere unsichtbarer Wissensverlust: die Frage bekaeme spaeter einfach
    keine Antwort, ohne dass irgendwo ein Fehler auftaucht.
    """
    try:
        pages = _read_pages(data)
    except Exception as exc:  # kaputtes oder passwortgeschuetztes PDF
        return PdfExtract(
            title=filename,
            markdown="",
            pages=[],
            layout="leer",
            char_count=0,
            ok=False,
            reason=f"PDF konnte nicht geoeffnet werden: {exc}",
        )

    if not pages:
        return PdfExtract(
            title=filename,
            markdown="",
            pages=[],
            layout="leer",
            char_count=0,
            ok=False,
            reason="Das PDF enthaelt keine Seiten.",
        )

    _drop_repeating_lines(pages)
    chars = sum(len(p.text) for p in pages)

    mit_text = sum(1 for p in pages if p.text.strip())
    if chars < MIN_CHARS_TOTAL or mit_text / len(pages) < MIN_PAGES_WITH_TEXT:
        return PdfExtract(
            title=_title_from(pages, filename),
            markdown="",
            pages=pages,
            layout="leer",
            char_count=chars,
            ok=False,
            reason=(
                f"Kein auswertbarer Textlayer gefunden ({chars} Zeichen, "
                f"{mit_text} von {len(pages)} Seiten mit Text). Vermutlich ein "
                "Scan oder ein als Bild exportiertes PDF. OCR ist nicht Teil "
                "dieses Systems - bitte eine Fassung mit Textlayer hochladen."
            ),
        )

    layout = _detect_layout(pages)
    markdown = (
        _flow_to_markdown(pages) if layout == "fliesstext" else _slides_to_markdown(pages)
    )
    return PdfExtract(
        title=_title_from(pages, filename),
        markdown=markdown,
        pages=pages,
        layout=layout,
        char_count=chars,
        ok=True,
    )
