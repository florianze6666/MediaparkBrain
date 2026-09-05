"""Wiki-Seiten: Markdown-Dateien mit Frontmatter, nach Domaene abgelegt.

Ablage (Stufe 2, docs/berechtigungen-stufe-2-admin-und-ablage.md):
    pages/<domaene>/<slug>.md                 intern / oeffentlich
    pages/<domaene>/vertraulich/<slug>.md     vertraulich
Der Ordner ist die einzige Wahrheit: Domaene und "vertraulich" kommen aus dem
Pfad und ueberschreiben den Dateikopf. Slugs sind global eindeutig.
Das Label oeffentlich erweitert nie die Ordnerrechte (Label verschaerft nur):
`allgemein` ist die Lobby, die jeder betritt - alle anderen Ordner nur, wer sie
laut permissions.yaml lesen darf.
"""
from __future__ import annotations

import logging
import os
import re
import secrets
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

import yaml

from . import access
from .access import PageMeta, decide, ALLOW, can_read

log = logging.getLogger(__name__)

# Standard-Ablage der Seiten; per Env MPB_PAGES_DIR ueberschreibbar (Tests).
PAGES_DIR = Path(__file__).resolve().parent.parent / "pages"
UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads"
SLUG_RE = re.compile(r"[^a-z0-9-]+")          # was slugify entfernt
VALID_SLUG_RE = re.compile(r"^[a-z0-9-]+$")    # was ein Slug sein darf (URL, Dateiname)

WORD_RE = re.compile(r"[a-zA-ZäöüÄÖÜß0-9]+")
FRONTMATTER_DELIM = "---"
VERTRAULICH_DIR = "vertraulich"
DEFAULT_DOMAIN = access.LOBBY_DOMAIN  # "allgemein"

# Ordner unter pages/, die keine Domaene sind: nur einmal warnen, nicht pro Request.
_warned_folders: set[str] = set()


def pages_dir() -> Path:
    env = os.environ.get("MPB_PAGES_DIR")
    return Path(env) if env else PAGES_DIR


def uploads_dir() -> Path:
    env = os.environ.get("MPB_UPLOADS_DIR")
    d = Path(env) if env else UPLOADS_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def sanitize_filename(filename: str) -> str:
    """Extrahiert den reinen Dateinamen und filtert unsichere Zeichen,
    um Path-Traversal (../, %2e%2e) sicher zu verhindern."""
    base = Path(filename).name
    clean = re.sub(r"[^A-Za-z0-9._-]", "_", base)
    clean = clean.lstrip(".")
    if not clean or clean in (".", ".."):
        clean = f"upload_{secrets.token_hex(4)}"
    return clean


def save_uploaded_file(filename: str, content_bytes: bytes, domaene: str = "") -> Path:
    safe_name = sanitize_filename(filename)
    d = uploads_dir()
    if domaene and is_valid_slug(domaene):
        d = d / domaene
    d.mkdir(parents=True, exist_ok=True)
    target = (d / safe_name).resolve()
    if not target.is_relative_to(uploads_dir().resolve()):
        raise ValueError("Ungültiger Dateiname / Pfadüberlauf")
    target.write_bytes(content_bytes)
    return target



def slugify(title: str) -> str:
    slug = title.strip().lower().replace(" ", "-")
    slug = SLUG_RE.sub("", slug)
    return slug or "seite"


def is_valid_slug(slug: str | None) -> bool:
    """Nur `^[a-z0-9-]+$` - alles andere (z. B. `..`, `%2e%2e`, Pfade) ist kein
    Slug und wird nie als Dateiname oder Suchschluessel verwendet."""
    return bool(slug) and bool(VALID_SLUG_RE.match(slug))


def page_path(slug: str, meta: PageMeta) -> Path:
    """Zielpfad einer Seite aus Domaene und Vertraulichkeit (US-17)."""
    d = pages_dir() / (meta.domaene or DEFAULT_DOMAIN)
    if meta.vertraulichkeit == "vertraulich":
        d = d / VERTRAULICH_DIR
    return d / f"{slug}.md"


@dataclass
class Page:
    slug: str
    title: str
    content: str  # raw markdown, without frontmatter and title heading
    meta: PageMeta = field(default_factory=PageMeta)
    file: Path | None = None  # tatsaechlicher Speicherort, falls von Platte gelesen

    @property
    def path(self) -> Path:
        return self.file or page_path(self.slug, self.meta)


# ---------------------------------------------------------------------------
# Dateiformat: optionales YAML-Frontmatter, dann "# Titel", dann Inhalt
# ---------------------------------------------------------------------------


def split_frontmatter_raw(raw: str) -> tuple[dict[str, Any] | None, str]:
    """Trennt YAML-Frontmatter vom Rest. None, wenn keins vorhanden ist.

    Wird auch von proposals.py genutzt (andere Feldnamen im Kopf).
    """
    lines = raw.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_DELIM:
        return None, raw
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
            return data, rest
    # Kein schliessendes --- gefunden: als normalen Inhalt behandeln
    return None, raw


def _split_frontmatter(raw: str) -> tuple[PageMeta, str]:
    """Seiten ohne Frontmatter (Altbestand) bekommen die Defaults aus PageMeta:
    erstellt_von "unbekannt", intern, allgemein."""
    data, rest = split_frontmatter_raw(raw)
    if data is None:
        return PageMeta(), raw
    return PageMeta.from_dict(data), rest


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
# Ordner-Scan: Domaene und "vertraulich" kommen aus dem Pfad
# ---------------------------------------------------------------------------


def _scan(domains: list[str] | None = None) -> Iterator[tuple[str, bool, Path]]:
    """Liefert (domaene, vertraulich, datei) fuer alle Seiten in bekannten
    Domaenenordnern. Mit `domains` werden NUR diese Ordner betreten
    (Ordner-Schranke, US-18). Unbekannte Ordner werden ignoriert und gemeldet."""
    root = pages_dir()
    root.mkdir(parents=True, exist_ok=True)
    known = set(access.list_domains())
    wanted = None if domains is None else set(domains)
    for sub in sorted(root.iterdir()):
        if not sub.is_dir():
            continue
        dom = sub.name
        if dom not in known:
            if dom not in _warned_folders:
                _warned_folders.add(dom)
                log.warning(
                    "pages/%s ist keine Domaene aus permissions.yaml - Ordner wird ignoriert", dom
                )
            continue
        if wanted is not None and dom not in wanted:
            continue
        for f in sorted(sub.glob("*.md")):
            yield dom, False, f
        v = sub / VERTRAULICH_DIR
        if v.is_dir():
            for f in sorted(v.glob("*.md")):
                yield dom, True, f


def _load(dom: str, vertraulich: bool, f: Path) -> Page:
    page = _parse(f.stem, f.read_text(encoding="utf-8"))
    # Ordner = Wahrheit (US-17/18): Kopf wird beim naechsten Speichern korrigiert.
    page.meta.domaene = dom
    if vertraulich:
        page.meta.vertraulichkeit = "vertraulich"
    page.file = f
    return page


def _find_file(slug: str) -> tuple[str, bool, Path] | None:
    if not is_valid_slug(slug):
        return None
    for dom, vert, f in _scan():
        if f.stem == slug:
            return dom, vert, f
    return None


# ---------------------------------------------------------------------------
# Lesen / Schreiben
# ---------------------------------------------------------------------------


def list_pages(user: str | None = None) -> list[Page]:
    """Alle Seiten; mit `user` nur die, die der Nutzer sehen darf.

    Zwei Schranken, dieselbe Regel: Es werden AUSSCHLIESSLICH die Domaenenordner
    betreten, die der Nutzer laut permissions.yaml lesen darf
    (access.readable_domains - die Lobby `allgemein` ist immer dabei). Fremde
    Ordner werden nicht einmal geoeffnet. Innerhalb der betretenen Ordner
    entscheidet `decide` pro Seite (Vertraulichkeit, Empfaenger; der Gast sieht
    in allgemein nur oeffentlich).

    Das Label oeffentlich erweitert nie die Ordnerrechte (Label verschaerft nur).
    Ohne Argument ungefiltert (Rohzugriff, z. B. Paket 6 Statistik).
    """
    pages = []
    if user is None:
        for dom, vert, f in _scan():
            pages.append(_load(dom, vert, f))
        return sorted(pages, key=lambda p: p.title.lower())

    for dom, vert, f in _scan(access.readable_domains(user)):
        page = _load(dom, vert, f)
        if decide(user, page.meta) != ALLOW:
            continue
        pages.append(page)
    return sorted(pages, key=lambda p: p.title.lower())


def get_page(slug: str) -> Page | None:
    """Ungefilterter Rohzugriff ueber alle Ordner. Fuer Nutzer-Sicht `get_page_for`."""
    found = _find_file(slug)
    if found is None:
        return None
    return _load(*found)


def get_page_for(slug: str, user: str) -> Page | None:
    """Seite aus Sicht eines Nutzers: None, wenn sie fehlt ODER verboten ist.
    Dieselbe Schranke wie list_pages: Ordner lesbar UND decide erlaubt (can_read)."""
    page = get_page(slug)
    if page is None or not can_read(user, page.meta):
        return None
    return page


def slug_exists(slug: str) -> bool:
    return _find_file(slug) is not None


def slug_exists_elsewhere(slug: str, meta: PageMeta) -> bool:
    """Liegt der Slug bereits in einem anderen Ordner als dem Ziel aus `meta`?"""
    found = _find_file(slug)
    return found is not None and found[2] != page_path(slug, meta)


def save_page(slug: str, title: str, content: str, meta: PageMeta | None = None) -> Page:
    """Schreibt die Seite in den Ordner ihrer Domaene/Vertraulichkeit.
    Liegt der Slug bereits woanders, wird die alte Datei geloescht (= Verschieben)."""
    clean_content = content.strip()
    if clean_content.startswith(f"# {title}"):
        clean_content = clean_content[len(f"# {title}") :].lstrip("\n")
    page = Page(slug=slug, title=title, content=clean_content, meta=meta or PageMeta())
    target = page_path(slug, page.meta)
    found = _find_file(slug)
    if found is not None and found[2] != target:
        found[2].unlink()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        f"{_render_frontmatter(page.meta)}# {title}\n\n{clean_content}\n",
        encoding="utf-8",
    )
    page.file = target
    return page



def delete_page(slug: str) -> None:
    found = _find_file(slug)
    if found is not None:
        found[2].unlink()


# ---------------------------------------------------------------------------
# Migration flacher Dateien (US-19), idempotent, laeuft bei jedem Start
# ---------------------------------------------------------------------------


def migrate_flat_pages() -> int:
    """Sortiert `pages/*.md` auf oberster Ebene anhand ihres Kopfes ein.
    Ohne Kopf -> allgemein/ mit Default-Meta (erstellt_von unbekannt, intern).
    Unbekannte Domaene im Kopf -> allgemein (mit Warnung). Slug-Kollision mit
    einer bereits einsortierten Seite -> Datei bleibt liegen (mit Warnung)."""
    root = pages_dir()
    root.mkdir(parents=True, exist_ok=True)
    known = set(access.list_domains())
    moved = 0
    for f in sorted(root.glob("*.md")):
        page = _parse(f.stem, f.read_text(encoding="utf-8"))
        if page.meta.domaene not in known:
            log.warning(
                "Migration %s: Domaene %r unbekannt, wird nach %s/ einsortiert",
                f.name, page.meta.domaene, DEFAULT_DOMAIN,
            )
            page.meta.domaene = DEFAULT_DOMAIN
        if slug_exists(page.slug):
            log.warning(
                "Migration %s: Slug existiert bereits in einem Domaenenordner, Datei bleibt liegen",
                f.name,
            )
            continue
        save_page(page.slug, page.title, page.content, page.meta)
        f.unlink()
        moved += 1
        log.info("Migration: %s -> %s", f.name, page_path(page.slug, page.meta).relative_to(root))
    return moved


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
    verbotene Seiten werden gar nicht erst bewertet, fremde Ordner gar nicht
    erst geoeffnet (US-18). `user` ist Pflicht, damit niemand versehentlich
    ungefiltert sucht.
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
