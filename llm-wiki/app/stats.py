from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

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


# ---------------------------------------------------------------------------
# Git-Historie: EIN `git log` ueber das ganze Seitenverzeichnis (Phase 0.1).
#
# Vorher lief je Seite ein eigener Subprozess (zwei, wenn die Seite verschoben
# war). Unter Windows kostet allein der Prozessstart rund 50 ms, bei 218 Seiten
# waeren das rund 20 Sekunden je Dashboard-Aufruf. Jetzt: ein Aufruf, dessen
# Ausgabe einmal nach Pfad gruppiert wird, unabhaengig von der Seitenzahl.
#
# Dazu ein Cache, der am aktuellen Commit haengt: die Historie unter pages/
# aendert sich nur mit HEAD. Die Commit-Kennung wird aus den .git-Dateien
# gelesen, ohne Subprozess; ist sie unveraendert, entfaellt auch der eine Aufruf.
# ---------------------------------------------------------------------------

History = dict[str, list[tuple[str, str]]]  # relpath -> [(autor, iso-datum)], neuester zuerst

_history_cache: dict[str, object] = {"root": None, "head": None, "history": None}


def clear_history_cache() -> None:
    _history_cache["root"] = None
    _history_cache["head"] = None
    _history_cache["history"] = None


def _git_log(cwd, rel_path: str) -> list[tuple[str, str]]:
    """Commits einer EINZELNEN Datei, neuester zuerst.

    Die Seitenhistorie laeuft seit Phase 0 gebuendelt ueber _git_history_all;
    fuer Einzeldateien ausserhalb des Seitenverzeichnisses (Projektantraege,
    Versionsliste im Antragsdetail) bleibt der gezielte Aufruf der richtige Weg.
    """
    try:
        result = subprocess.run(
            ["git", "log", "--follow", "--format=%an|%aI", "--", rel_path],
            cwd=cwd, capture_output=True, text=True,
        )
    except OSError:
        return []
    if result.returncode != 0:
        return []
    entries = []
    for line in result.stdout.strip().splitlines():
        if "|" in line:
            author, date = line.split("|", 1)
            entries.append((author, date))
    return entries


def _git_dir(root: Path) -> Path | None:
    """Das .git des Repos, zu dem `root` gehoert (aufwaerts gesucht). None ohne Repo."""
    for d in (root, *root.parents):
        g = d / ".git"
        if g.is_dir():
            return g
        if g.is_file():  # Worktree: ".git" ist eine Datei mit "gitdir: <pfad>"
            try:
                line = g.read_text(encoding="utf-8").strip()
            except OSError:
                return None
            if line.startswith("gitdir:"):
                p = Path(line[len("gitdir:"):].strip())
                return p if p.is_absolute() else (d / p).resolve()
            return None
    return None


def _head_marker(root: Path) -> str | None:
    """Kennung des aktuellen Commits ohne Subprozess: Inhalt von HEAD, aufgeloest
    ueber die Ref-Datei oder packed-refs. None, wenn nicht bestimmbar; dann wird
    nicht gecacht, sondern bei jedem Aufruf frisch gelesen."""
    git = _git_dir(root)
    if git is None:
        return None
    try:
        head = (git / "HEAD").read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not head.startswith("ref:"):
        return head  # detached HEAD: Commit-Hash steht direkt drin
    ref = head[len("ref:"):].strip()
    try:
        return (git / ref).read_text(encoding="utf-8").strip()
    except OSError:
        pass
    try:
        for line in (git / "packed-refs").read_text(encoding="utf-8").splitlines():
            if line.endswith(" " + ref):
                return line.split(" ", 1)[0]
    except OSError:
        pass
    return None


def _git_history_all(root: Path) -> History:
    """Autor + ISO-Datum je Commit fuer JEDE Datei unter `root`, aus einem Aufruf.

    Pfade relativ zu `root` (--relative), Reihenfolge je Datei wie `git log`,
    also neuester Commit zuerst. Kein Repo, kein git, Fehler: leeres dict,
    dann gibt es keine Historie, aber auch keinen Absturz.
    """
    try:
        result = subprocess.run(
            ["git", "-c", "core.quotepath=false", "log", "--relative",
             "--name-only", "--format=%x00%an|%aI", "--", "."],
            cwd=root, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )
    except OSError:
        return {}
    if result.returncode != 0:
        return {}
    history: History = {}
    current: tuple[str, str] | None = None
    for line in result.stdout.splitlines():
        if line.startswith("\x00"):
            author, _, date = line[1:].partition("|")
            current = (author, date) if date else None
            continue
        rel = line.strip()
        if not rel or current is None:
            continue
        history.setdefault(rel, []).append(current)
    return history


def _history_for_root(root: Path) -> History:
    """Historie aus dem Cache, solange HEAD unveraendert ist; sonst neu lesen."""
    head = _head_marker(root)
    if (head is not None and _history_cache["history"] is not None
            and _history_cache["root"] == str(root) and _history_cache["head"] == head):
        return _history_cache["history"]  # type: ignore[return-value]
    history = _git_history_all(root)
    if head is not None:
        _history_cache["root"] = str(root)
        _history_cache["head"] = head
        _history_cache["history"] = history
    return history


def _commit_time(entry: tuple[str, str]) -> datetime:
    try:
        return datetime.fromisoformat(entry[1])
    except ValueError:
        return _MIN_DATETIME


def _git_history(page: wiki.Page, history: History) -> list[tuple[str, str]]:
    """Autor + ISO-Datum je Commit, der die Seite betrifft. Neuester zuerst.

    Eine in den Domaenenordner verschobene Seite (Stufe 2) traegt die Historie
    ihres flachen Altpfads `<slug>.md` weiter; das ersetzt das fruehere
    `--follow` je Datei. Solange die Verschiebung nicht committet ist, kennt git
    nur den alten Pfad, auch dann greift derselbe Rueckgriff.
    """
    root = wiki.pages_dir()
    try:
        rel = page.path.relative_to(root).as_posix()
    except ValueError:
        return []  # Seite ausserhalb des Seitenverzeichnisses: keine Historie
    entries = list(history.get(rel, ()))
    if "/" in rel:
        for e in history.get(f"{page.slug}.md", ()):
            if e not in entries:
                entries.append(e)
        entries.sort(key=_commit_time, reverse=True)
    return entries


def _activity_for(page: wiki.Page, history: History) -> DocumentActivity:
    commits = _git_history(page, history)
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
    history = _history_for_root(wiki.pages_dir()) if pages else {}
    activities = [_activity_for(p, history) for p in pages]
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
