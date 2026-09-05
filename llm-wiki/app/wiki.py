from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .access import PageMeta, decide, ALLOW

# Standard-Ablage der Seiten; per Env MPB_PAGES_DIR ueberschreibbar (Tests).
PAGES_DIR = Path(__file__).resolve().parent.parent / "pages"
SLUG_RE = re.compile(r"[^a-z0-9-]+")
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
        return pages_dir() / f"{self.slug}.md"


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
    for f in sorted(d.glob("*.md")):
        page = _parse(f.stem, f.read_text(encoding="utf-8"))
        if user is not None and decide(user, page.meta) != ALLOW:
            continue
        pages.append(page)
    return sorted(pages, key=lambda p: p.title.lower())


def get_page(slug: str) -> Page | None:
    """Ungefilterter Rohzugriff. Fuer Nutzer-Sicht `get_page_for` verwenden."""
    f = pages_dir() / f"{slug}.md"
    if not f.exists():
        return None
    return _parse(slug, f.read_text(encoding="utf-8"))


def get_page_for(slug: str, user: str) -> Page | None:
    """Seite aus Sicht eines Nutzers: None, wenn sie fehlt ODER verboten ist."""
    page = get_page(slug)
    if page is None or decide(user, page.meta) != ALLOW:
        return None
    return page


def save_page(slug: str, title: str, content: str, meta: PageMeta | None = None) -> Page:
    d = pages_dir()
    d.mkdir(parents=True, exist_ok=True)
    page = Page(slug=slug, title=title, content=content, meta=meta or PageMeta())
    page.path.write_text(
        f"{_render_frontmatter(page.meta)}# {title}\n\n{content.strip()}\n",
        encoding="utf-8",
    )
    return page


def delete_page(slug: str) -> None:
    f = pages_dir() / f"{slug}.md"
    if f.exists():
        f.unlink()


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
