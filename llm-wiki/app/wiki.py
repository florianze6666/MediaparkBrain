from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .access import PageMeta, decide, normalize_domaene, ALLOW

# Standard-Ablage der Seiten; per Env MPB_PAGES_DIR ueberschreibbar (Tests).
PAGES_DIR = Path(__file__).resolve().parent.parent / "pages"
SLUG_RE = re.compile(r"[^a-z0-9-]+")
# Genau das, was slugify erzeugen kann - alles andere ist kein Slug.
SLUG_OK = re.compile(r"[a-z0-9-]+")
# Ein automatisch gesetzter Ablageort, erkennbar an <domaene>/<slug>.md.
AUTO_ABLAGEORT = re.compile(r"[a-z0-9-]+/[a-z0-9-]+\.md")
WORD_RE = re.compile(r"[a-zA-ZäöüÄÖÜß0-9]+")
FRONTMATTER_DELIM = "---"


def pages_dir() -> Path:
    env = os.environ.get("MPB_PAGES_DIR")
    return Path(env) if env else PAGES_DIR


def slugify(title: str) -> str:
    slug = title.strip().lower().replace(" ", "-")
    slug = SLUG_RE.sub("", slug)
    return slug or "seite"


@dataclass
class Page:
    slug: str
    title: str
    content: str  # raw markdown, without frontmatter and title heading
    meta: PageMeta = field(default_factory=PageMeta)

    @property
    def path(self) -> Path:
        # normalize_domaene haelt den Wert in der Liste aus permissions.yaml;
        # ohne diese Pruefung koennte ein Formularwert wie "../../ausserhalb"
        # eine Datei ausserhalb des Seitenverzeichnisses anlegen.
        return pages_dir() / normalize_domaene(self.meta.domaene) / f"{self.slug}.md"


# ---------------------------------------------------------------------------
# Dateiformat: optionales YAML-Frontmatter, dann "# Titel", dann Inhalt
# ---------------------------------------------------------------------------


def _split_frontmatter(raw: str) -> tuple[PageMeta, str]:
    """Trennt YAML-Frontmatter (zwischen ---‑Zeilen am Dateianfang) vom Rest.

    Seiten ohne Frontmatter (Altbestand) bekommen die Defaults aus PageMeta:
    erstellt_von "unbekannt", intern, allgemein.
    """
    lines = raw.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_DELIM:
        return PageMeta(), raw
    for i in range(1, len(lines)):
        if lines[i].strip() == FRONTMATTER_DELIM:
            block = "\n".join(lines[1:i])
            try:
                data = yaml.safe_load(block) or {}
            except yaml.YAMLError:
                data = {}
            if not isinstance(data, dict):
                data = {}
            rest = "\n".join(lines[i + 1 :]).lstrip("\n")
            return PageMeta.from_dict(data), rest
    # Kein schliessendes --- gefunden: als normalen Inhalt behandeln
    return PageMeta(), raw


def _split_title(raw: str) -> tuple[str, str]:
    lines = raw.splitlines()
    if lines and lines[0].startswith("# "):
        return lines[0][2:].strip(), "\n".join(lines[1:]).lstrip("\n")
    return "Unbenannt", raw


def _parse(slug: str, raw: str) -> Page:
    meta, rest = _split_frontmatter(raw)
    title, content = _split_title(rest)
    return Page(slug=slug, title=title, content=content, meta=meta)


def _render_frontmatter(meta: PageMeta) -> str:
    body = yaml.safe_dump(
        meta.to_dict(), sort_keys=False, allow_unicode=True, default_flow_style=False
    ).rstrip("\n")
    return f"{FRONTMATTER_DELIM}\n{body}\n{FRONTMATTER_DELIM}\n"


# ---------------------------------------------------------------------------
# Lesen / Schreiben
# ---------------------------------------------------------------------------


def list_pages(user: str | None = None) -> list[Page]:
    """Alle Seiten; mit `user` nur die, die `decide` erlaubt.

    Ohne Argument ungefiltert (Rohzugriff, z. B. Paket 6 Statistik).
    """
    d = pages_dir()
    d.mkdir(parents=True, exist_ok=True)
    pages = []
    for f in sorted(d.rglob("*.md")):
        page = _parse(f.stem, f.read_text(encoding="utf-8"))
        if user is not None and decide(user, page.meta) != ALLOW:
            continue
        pages.append(page)
    return sorted(pages, key=lambda p: p.title.lower())


def _find_page_file(slug: str) -> Path | None:
    """Sucht die Datei zu `slug` unabhaengig davon, in welchem Domaenen-Ordner sie liegt.

    Der Slug kommt roh aus dem Pfadparameter der Routen und wird an `rglob`
    als *Muster* weitergereicht. Ohne die Pruefung wuerde "*" auf eine
    beliebige fremde Seite passen - `/wiki/*/delete` haette dann eine Seite
    geloescht, die niemand benannt hat. Erlaubt ist genau das Alphabet, das
    `slugify` erzeugen kann.
    """
    if not SLUG_OK.fullmatch(slug):
        return None
    return next(iter(sorted(pages_dir().rglob(f"{slug}.md"))), None)


def get_page(slug: str) -> Page | None:
    """Ungefilterter Rohzugriff. Fuer Nutzer-Sicht `get_page_for` verwenden."""
    f = _find_page_file(slug)
    if f is None:
        return None
    return _parse(slug, f.read_text(encoding="utf-8"))


def get_page_for(slug: str, user: str) -> Page | None:
    """Seite aus Sicht eines Nutzers: None, wenn sie fehlt ODER verboten ist."""
    page = get_page(slug)
    if page is None or decide(user, page.meta) != ALLOW:
        return None
    return page


def save_page(slug: str, title: str, content: str, meta: PageMeta | None = None) -> Page:
    """Schreibt die Seite nach pages/<domaene>/<slug>.md.

    Liegt sie (z. B. nach einem Domaenen-Wechsel oder als Alt-Datei aus
    pages/<slug>.md) noch woanders, wird die alte Datei entfernt. `ablageort`
    wird nur befuellt, wenn der Aufrufer ihn nicht selbst gesetzt hat.
    """
    meta = meta or PageMeta()
    meta.domaene = normalize_domaene(meta.domaene)
    old = _find_page_file(slug)
    page = Page(slug=slug, title=title, content=content, meta=meta)
    if old is not None and old.resolve() != page.path.resolve():
        old.unlink()
    page.path.parent.mkdir(parents=True, exist_ok=True)
    # Nur den selbst gesetzten Wert fortschreiben. Ein vom Aufrufer
    # gepflegter echter Quellsystem-Pfad bleibt unangetastet; der zuvor
    # automatisch erzeugte wuerde sonst nach einem Domaenenwechsel dauerhaft
    # auf den alten Ordner zeigen und so in der Seitenansicht luegen.
    if not meta.ablageort or AUTO_ABLAGEORT.fullmatch(meta.ablageort):
        meta.ablageort = f"{meta.domaene}/{slug}.md"
    page.path.write_text(
        f"{_render_frontmatter(page.meta)}# {title}\n\n{content.strip()}\n",
        encoding="utf-8",
    )
    return page


def delete_page(slug: str) -> None:
    f = _find_page_file(slug)
    if f is not None:
        f.unlink()


def migrate_flat_pages() -> None:
    """Verschiebt Alt-Seiten aus pages/ (Wurzelebene) in ihren Domaenen-Ordner.

    Einmalig beim Start noetig, da Seiten frueher flach unter pages/*.md lagen.

    Die Datei wird **verschoben**, nicht ueber `save_page` neu geschrieben:
    Sonst haette `_find_page_file` bei gleichem Slug zuerst die bereits
    einsortierte Fassung gefunden und diese mit dem Inhalt der alten flachen
    Datei ueberschrieben - Datenverlust bei jedem Start, denn die flache Datei
    waere liegen geblieben und der Slug damit dauerhaft doppelt.

    Liegt am Zielort schon eine Seite mit diesem Slug, gewinnt sie. Die
    flache Alt-Datei wird dann auf `.md.alt` umbenannt: Der Inhalt bleibt
    erhalten, taucht aber nicht mehr als zweite Seite mit demselben Slug auf.
    """
    d = pages_dir()
    d.mkdir(parents=True, exist_ok=True)
    for f in sorted(d.glob("*.md")):
        page = _parse(f.stem, f.read_text(encoding="utf-8"))
        ziel = page.path
        if ziel.exists():
            beiseite = f.with_name(f.name + ".alt")
            if not beiseite.exists():
                f.rename(beiseite)
            continue
        ziel.parent.mkdir(parents=True, exist_ok=True)
        f.rename(ziel)


# ---------------------------------------------------------------------------
# Suche
# ---------------------------------------------------------------------------


def _tokenize(text: str) -> set[str]:
    return {w.lower() for w in WORD_RE.findall(text)}


@dataclass
class Snippet:
    page: Page
    paragraph: str
    score: float


def search_snippets(query: str, user: str, top_k: int = 5) -> list[Snippet]:
    """Volltextsuche aus Sicht von `user`.

    Der Rechte-Filter greift VOR dem Scoring und der Top-k-Auswahl (US-7):
    verbotene Seiten werden gar nicht erst bewertet. `user` ist Pflicht,
    damit niemand versehentlich ungefiltert sucht.
    """
    query_words = _tokenize(query)
    if not query_words:
        return []
    results: list[Snippet] = []
    for page in list_pages(user):
        title_words = _tokenize(page.title)
        paragraphs = [p.strip() for p in page.content.split("\n\n") if p.strip()]
        if not paragraphs:
            paragraphs = [page.title]
        for para in paragraphs:
            # Titelwoerter zaehlen mit, da relevanter Inhalt oft nur im Titel steht
            # (z.B. kurze Notizseiten wie "heute ist ein schoener Tag").
            para_words = _tokenize(para) | title_words
            if not para_words:
                continue
            overlap = query_words & para_words
            if not overlap:
                continue
            score = len(overlap) / len(query_words)
            results.append(Snippet(page=page, paragraph=para, score=score))
    results.sort(key=lambda s: s.score, reverse=True)
    return results[:top_k]
