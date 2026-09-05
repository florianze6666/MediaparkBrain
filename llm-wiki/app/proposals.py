from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .wiki import slugify

PROPOSALS_DIR = Path(__file__).resolve().parent.parent.parent / "project_proposals"
UPLOADS_DIR = PROPOSALS_DIR / "uploads"


DEFAULT_STATUS = "Eingereicht"


@dataclass
class Proposal:
    slug: str
    project_name: str
    description: str
    submitted_at: str
    submitted_by: str = "unbekannt"
    status: str = DEFAULT_STATUS
    files: list[str] = field(default_factory=list)

    @property
    def path(self) -> Path:
        return PROPOSALS_DIR / f"{self.slug}.md"

    @property
    def upload_dir(self) -> Path:
        return UPLOADS_DIR / self.slug


def _parse(raw: str, slug: str) -> Proposal:
    lines = raw.splitlines()
    project_name = lines[0][2:].strip() if lines and lines[0].startswith("# ") else slug
    submitted_at = ""
    submitted_by = "unbekannt"
    status = DEFAULT_STATUS
    files: list[str] = []
    description_lines: list[str] = []
    section = None
    for line in lines[1:]:
        if line.startswith("Eingereicht am:"):
            submitted_at = line.split(":", 1)[1].strip()
        elif line.startswith("Eingereicht von:"):
            submitted_by = line.split(":", 1)[1].strip() or "unbekannt"
        elif line.startswith("Status:"):
            status = line.split(":", 1)[1].strip() or DEFAULT_STATUS
        elif line.strip() == "## Beschreibung":
            section = "description"
        elif line.strip() == "## Hochgeladene Dateien":
            section = "files"
        elif section == "description":
            description_lines.append(line)
        elif section == "files" and line.strip().startswith("- "):
            files.append(line.strip()[2:].strip())
    return Proposal(
        slug=slug,
        project_name=project_name,
        description="\n".join(description_lines).strip(),
        submitted_at=submitted_at,
        submitted_by=submitted_by,
        status=status,
        files=files,
    )


def list_proposals() -> list[Proposal]:
    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    proposals = [
        _parse(f.read_text(encoding="utf-8"), f.stem)
        for f in sorted(PROPOSALS_DIR.glob("*.md"))
    ]
    return sorted(proposals, key=lambda p: p.submitted_at, reverse=True)


def get_proposal(slug: str) -> Proposal | None:
    f = PROPOSALS_DIR / f"{slug}.md"
    if not f.exists():
        return None
    return _parse(f.read_text(encoding="utf-8"), slug)


def already_submitted(project_name: str) -> bool:
    """Prueft, ob unter diesem Projektnamen bereits ein Vorschlag eingereicht wurde."""
    return (PROPOSALS_DIR / f"{slugify(project_name)}.md").exists()


def save_proposal(
    project_name: str,
    description: str,
    uploaded_files: list[tuple[str, bytes]],
    submitted_by: str = "unbekannt",
) -> Proposal:
    """Speichert einen neuen Projektvorschlag. Ruft VOR dem Aufruf already_submitted()
    auf, um Duplikate abzulehnen - diese Funktion selbst prueft das nicht erneut."""
    slug = slugify(project_name)
    submitted_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    proposal = Proposal(
        slug=slug,
        project_name=project_name,
        description=description.strip(),
        submitted_at=submitted_at,
        submitted_by=submitted_by,
        files=[name for name, _ in uploaded_files if name],
    )

    if proposal.files:
        proposal.upload_dir.mkdir(parents=True, exist_ok=True)
        for name, data in uploaded_files:
            if not name:
                continue
            safe_name = Path(name).name  # keine Pfad-Traversal ueber Dateinamen
            (proposal.upload_dir / safe_name).write_bytes(data)

    files_section = (
        "\n".join(f"- {name}" for name in proposal.files)
        if proposal.files
        else "*(keine Dateien hochgeladen)*"
    )
    proposal.path.write_text(
        f"# {project_name}\n\n"
        f"Eingereicht am: {submitted_at}\n"
        f"Eingereicht von: {submitted_by}\n"
        f"Status: {proposal.status}\n\n"
        f"## Beschreibung\n\n{proposal.description}\n\n"
        f"## Hochgeladene Dateien\n\n{files_section}\n",
        encoding="utf-8",
    )
    return proposal


def delete_proposal(slug: str) -> None:
    f = PROPOSALS_DIR / f"{slug}.md"
    if f.exists():
        f.unlink()
    upload_dir = UPLOADS_DIR / slug
    if upload_dir.exists():
        shutil.rmtree(upload_dir)
