from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

PAGES_DIR = Path(__file__).resolve().parent.parent / "pages"
SLUG_RE = re.compile(r"[^a-z0-9-]+")
WORD_RE = re.compile(r"[a-zA-ZäöüÄÖÜß0-9]+")


def slugify(title: str) -> str:
    slug = title.strip().lower().replace(" ", "-")
    slug = SLUG_RE.sub("", slug)
    return slug or "seite"


@dataclass
class Page:
    slug: str
    title: str
    content: str  # raw markdown, without the title heading

    @property
    def path(self) -> Path:
        return PAGES_DIR / f"{self.slug}.md"


def _split_title(raw: str) -> tuple[str, str]:
    lines = raw.splitlines()
    if lines and lines[0].startswith("# "):
        return lines[0][2:].strip(), "\n".join(lines[1:]).lstrip("\n")
    return "Unbenannt", raw


def list_pages() -> list[Page]:
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    pages = []
    for f in sorted(PAGES_DIR.glob("*.md")):
        title, content = _split_title(f.read_text(encoding="utf-8"))
        pages.append(Page(slug=f.stem, title=title, content=content))
    return sorted(pages, key=lambda p: p.title.lower())


def get_page(slug: str) -> Page | None:
    f = PAGES_DIR / f"{slug}.md"
    if not f.exists():
        return None
    title, content = _split_title(f.read_text(encoding="utf-8"))
    return Page(slug=slug, title=title, content=content)


def save_page(slug: str, title: str, content: str) -> Page:
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    page = Page(slug=slug, title=title, content=content)
    page.path.write_text(f"# {title}\n\n{content.strip()}\n", encoding="utf-8")
    return page


def delete_page(slug: str) -> None:
    f = PAGES_DIR / f"{slug}.md"
    if f.exists():
        f.unlink()


def _tokenize(text: str) -> set[str]:
    return {w.lower() for w in WORD_RE.findall(text)}


@dataclass
class Snippet:
    page: Page
    paragraph: str
    score: float


def search_snippets(query: str, top_k: int = 5) -> list[Snippet]:
    query_words = _tokenize(query)
    if not query_words:
        return []
    results: list[Snippet] = []
    for page in list_pages():
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
