from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone

from . import access, proposals, wiki

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
    domaene: str


def _git_log(cwd, rel_path: str) -> list[tuple[str, str]]:
    result = subprocess.run(
        ["git", "log", "--follow", "--format=%an|%aI", "--", rel_path],
        cwd=cwd,
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


def _git_history(page: wiki.Page) -> list[tuple[str, str]]:
    """Autor + ISO-Datum je Commit, der die Seite betrifft. Neuester zuerst.

    Nutzt --follow, damit auch Umbenennungen und das Verschieben in den
    Domaenenordner (Stufe 2) als Fortsetzung derselben Seite erkannt werden.
    Solange die Verschiebung noch nicht committet ist, kennt git den neuen
    Pfad nicht - dann wird die Historie der alten flachen Datei genutzt.
    """
    root = wiki.pages_dir()
    try:
        rel = page.path.relative_to(root).as_posix()
    except ValueError:
        rel = page.path.name
        root = page.path.parent
    entries = _git_log(root, rel)
    if not entries and "/" in rel:
        entries = _git_log(root, f"{page.slug}.md")
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
        # Ordner = Domaenenordner, die der Nutzer lesen darf (Stufe 2, Paket 6)
        total_folders=len(access.readable_domains(user)),
        recent_documents=activities[:limit],
    )


def _submitted_by_for(p: proposals.Proposal) -> str:
    """`submitted_by`, mit Git-Commit-Autor als Fallback.

    Altbestand (Marcs PLAN.md-Format) hat kein eingereicht_von-Feld im Kopf -
    submitted_by bleibt dann "unbekannt". Zeigt stattdessen den Autor des
    Commits, der die Antragsdatei angelegt hat (wie beim Dateien-Dashboard).
    """
    if p.submitted_by and p.submitted_by != access.UNKNOWN_CREATOR:
        return p.submitted_by
    commits = _git_log(p.path.parent, p.path.name)
    return commits[0][0] if commits else p.submitted_by


def get_proposal_stats(user: str) -> list[ProposalActivity]:
    """Projektantraege aus Sicht von `user`, neuester zuerst.

    Nutzt denselben Rechtefilter wie /proposals (access.can_read ueber
    proposals.list_proposals(user)), damit vertrauliche Antraege hier nicht
    an Nutzer ohne Zugriff durchsickern.
    """
    return [
        ProposalActivity(
            title=p.project_name,
            slug=p.slug,
            document_count=len(p.files),
            submitted_by=_submitted_by_for(p),
            submitted_at=p.submitted_at,
            status=p.status,
            domaene=p.meta.domaene,
        )
        for p in proposals.list_proposals(user)
    ]
