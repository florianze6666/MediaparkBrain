from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone

from . import proposals, wiki

_MIN_DATETIME = datetime.min.replace(tzinfo=timezone.utc)


@dataclass
class DocumentActivity:
    title: str
    slug: str
    uploaded_at: datetime | None
    uploaded_by: str
    is_update: bool


@dataclass
class DashboardStats:
    total_files: int
    total_folders: int
    recent_documents: list[DocumentActivity]


@dataclass
class ProposalActivity:
    title: str
    slug: str
    document_count: int
    submitted_by: str
    submitted_at: str
    status: str


def _git_history(page: wiki.Page) -> list[tuple[str, str]]:
    """Autor + ISO-Datum je Commit, der die Seite betrifft. Neuester zuerst.

    Nutzt --follow, damit auch Umbenennungen (Titel-/Slug-Aenderung) als
    Fortsetzung derselben Seite erkannt werden.
    """
    result = subprocess.run(
        ["git", "log", "--follow", "--format=%an|%aI", "--", page.path.name],
        cwd=page.path.parent,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    entries = []
    for line in result.stdout.strip().splitlines():
        if "|" not in line:
            continue
        author, date = line.split("|", 1)
        entries.append((author, date))
    return entries


def _activity_for(page: wiki.Page) -> DocumentActivity:
    commits = _git_history(page)
    if commits:
        author, date_str = commits[0]
        uploaded_at = datetime.fromisoformat(date_str)
        is_update = len(commits) > 1
    else:
        uploaded_at = None
        author = "Unbekannt (noch nicht committet)"
        is_update = False
    return DocumentActivity(
        title=page.title,
        slug=page.slug,
        uploaded_at=uploaded_at,
        uploaded_by=author,
        is_update=is_update,
    )


def get_dashboard_stats(user: str, limit: int = 10) -> DashboardStats:
    """Statistik aus Sicht von `user` - zeigt nur Seiten, die er lesen darf.

    Verhindert, dass Titel/Autor vertraulicher Dokumente ueber das Dashboard
    an Nutzer ohne Zugriff durchsickern (siehe access.decide).
    """
    pages = wiki.list_pages(user)
    activities = [_activity_for(p) for p in pages]
    activities.sort(key=lambda a: a.uploaded_at or _MIN_DATETIME, reverse=True)
    return DashboardStats(
        total_files=len(pages),
        total_folders=1 if pages else 0,
        recent_documents=activities[:limit],
    )


def get_proposal_stats() -> list[ProposalActivity]:
    """Alle eingereichten Projektantraege, neuester zuerst (wie proposals.list_proposals)."""
    return [
        ProposalActivity(
            title=p.project_name,
            slug=p.slug,
            document_count=len(p.files),
            submitted_by=p.submitted_by,
            submitted_at=p.submitted_at,
            status=p.status,
        )
        for p in proposals.list_proposals()
    ]
