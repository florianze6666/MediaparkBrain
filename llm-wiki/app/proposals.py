"""Projektvorschlaege in project_proposals/<slug>.md.

Stufe 2 (docs/berechtigungen-stufe-2-admin-und-ablage.md): Jeder Vorschlag traegt
einen YAML-Kopf mit eingereicht_von, rolle (Snapshot des Anzeigenamens),
eingereicht_am, vertraulichkeit, domaene, empfaenger. Rechte laufen ueber
denselben Weg wie bei Wiki-Seiten: access.can_read(user, meta) - Ordner-Schranke
(readable_domains) plus decide; das Label oeffentlich oeffnet keine fremde Domaene.
Altbestand ohne (oder mit fremdem) Kopf: eingereicht_von unbekannt, projekt, intern.
"""
from __future__ import annotations

import hashlib
import os
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from . import access
from .access import PageMeta, UNKNOWN_CREATOR
from .wiki import slugify, is_valid_slug, split_frontmatter_raw, FRONTMATTER_DELIM

# Standardablage; per Env MPB_PROPOSALS_DIR ueberschreibbar (Tests).
PROPOSALS_DIR = Path(__file__).resolve().parent.parent.parent / "project_proposals"
DEFAULT_DOMAIN = "projekt"
SOURCE = "proposal"


def proposals_dir() -> Path:
    env = os.environ.get("MPB_PROPOSALS_DIR")
    return Path(env) if env else PROPOSALS_DIR


def uploads_dir() -> Path:
    return proposals_dir() / "uploads"


DEFAULT_STATUS = "Eingereicht"

# Die 15 Pflichtfelder aus PLAN.md Sec. 2. Reihenfolge = Reihenfolge im Plan.
PFLICHTFELDER = (
    "projektname", "beschreibung", "zielsetzung", "nutzen", "geschaeftsprozesse",
    "organisationseinheiten", "business_case", "kosten", "wirtschaftlicher_nutzen",
    "laufzeit", "technische_abhaengigkeiten", "organisatorische_abhaengigkeiten",
    "risikoanalyse", "begruendung", "anbieterinformationen",
)

# Entschiedene Zustaende (POST /proposals/{slug}/decide setzt sie).
DECIDED_STATUS = ("freigegeben", "zurueckgestellt", "abgelehnt")


@dataclass
class Proposal:
    slug: str
    project_name: str
    description: str
    submitted_at: str
    submitted_by: str = "unbekannt"
    status: str = DEFAULT_STATUS
    files: list[str] = field(default_factory=list)
    meta: PageMeta = field(default_factory=lambda: _default_meta())
    rolle: str = UNKNOWN_CREATOR
    # Pflichtfelder aus PLAN.md Sec. 2, im Kopf abgelegt (Kompass-Umbau).
    # Optional: Altbestand und Vorschlaege von Marc haben sie nicht.
    felder: dict[str, str] = field(default_factory=dict)
    # Dialogeintraege [{author, kind, text, zeit}] - Rueckfragen, Vermerke, Entscheidungen.
    dialog: list[dict[str, str]] = field(default_factory=list)

    @property
    def path(self) -> Path:
        return proposals_dir() / f"{self.slug}.md"

    @property
    def upload_dir(self) -> Path:
        return uploads_dir() / self.slug


def _default_meta() -> PageMeta:
    return PageMeta(erstellt_von=UNKNOWN_CREATOR, vertraulichkeit="intern",
                    domaene=DEFAULT_DOMAIN, quelle=SOURCE)


def _meta_from_head(head: dict[str, Any] | None) -> tuple[PageMeta, str]:
    """Kopf -> (PageMeta, rolle). Fremde Koepfe (Altbestand von Marc) haben keine
    unserer Felder und landen bei den Defaults."""
    meta = _default_meta()
    rolle = UNKNOWN_CREATOR
    if not head:
        return meta, rolle
    mapped = PageMeta.from_dict({
        "erstellt_von": head.get("eingereicht_von"),
        "erstellt_am": head.get("eingereicht_am"),
        "vertraulichkeit": head.get("vertraulichkeit"),
        "domaene": head.get("domaene"),
        "empfaenger": head.get("empfaenger"),
    })
    if head.get("eingereicht_von"):
        meta.erstellt_von = mapped.erstellt_von
        meta.erstellt_am = mapped.erstellt_am
        meta.vertraulichkeit = mapped.vertraulichkeit
        meta.domaene = mapped.domaene or DEFAULT_DOMAIN
        meta.empfaenger = mapped.empfaenger
        rolle = str(head.get("rolle") or "").strip() or access.user_name(meta.erstellt_von)
    return meta, rolle


def _render_head(
    meta: PageMeta,
    rolle: str,
    felder: dict[str, str] | None = None,
    dialog: list[dict[str, str]] | None = None,
) -> str:
    """Kopf eines Vorschlags. Pflichtfelder und Dialog werden nur geschrieben,
    wenn es sie gibt - der Kopf eines alten Vorschlags bleibt damit unveraendert."""
    head: dict[str, Any] = {
        "eingereicht_von": meta.erstellt_von,
        "rolle": rolle,
        "eingereicht_am": meta.erstellt_am,
        "vertraulichkeit": meta.vertraulichkeit,
        "domaene": meta.domaene,
        "empfaenger": list(meta.empfaenger),
    }
    for key in PFLICHTFELDER:
        value = (felder or {}).get(key)
        if value:
            head[key] = value
    if dialog:
        head["dialog"] = [dict(entry) for entry in dialog]
    body = yaml.safe_dump(
        head, sort_keys=False, allow_unicode=True, default_flow_style=False,
    ).rstrip("\n")
    return f"{FRONTMATTER_DELIM}\n{body}\n{FRONTMATTER_DELIM}\n"


def _parse(raw: str, slug: str) -> Proposal:
    head, body = split_frontmatter_raw(raw)
    meta, rolle = _meta_from_head(head)
    lines = body.splitlines()
    is_legacy = bool(head and head.get("project_name"))
    if is_legacy:
        # Altbestand mit fremdem Kopf (Marcs Format): dort steht der echte Name,
        # die Ueberschrift lautet generisch "Projektvorschlag".
        project_name = str(head["project_name"])
    elif lines and lines[0].startswith("# "):
        project_name = lines[0][2:].strip()
    else:
        project_name = slug
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
    if not files and head and head.get("source_documents"):
        # Altbestand mit fremdem Kopf (Marcs Format): Dateien stehen unter
        # source_documents als Pfade, nicht im "## Hochgeladene Dateien"-Abschnitt.
        files = [Path(str(s)).name for s in head["source_documents"] if str(s).strip()]
    if is_legacy and not description_lines:
        # Marcs Format hat keinen "## Beschreibung"-Unterabschnitt - die
        # komplette PLAN.md-Sec.-2-Struktur (Zielsetzung, Business Case,
        # Risikoanalyse, ...) steht direkt im Body. Das ganze Dokument
        # (ohne die generische Titelzeile "# Projektvorschlag") ist die
        # vollstaendige Projektcharter.
        body_lines = lines[1:] if lines and lines[0].startswith("# ") else lines
        description = "\n".join(body_lines).strip()
    else:
        description = "\n".join(description_lines).strip()
    felder = {
        key: str(head[key]).strip()
        for key in PFLICHTFELDER
        if head and head.get(key) not in (None, "")
    }
    dialog = []
    for entry in (head or {}).get("dialog") or []:
        if isinstance(entry, dict):
            dialog.append({k: str(v) for k, v in entry.items()})
    return Proposal(
        slug=slug,
        project_name=project_name,
        description=description,
        submitted_at=submitted_at,
        submitted_by=submitted_by,
        status=status,
        files=files,
        meta=meta,
        rolle=rolle,
        felder=felder,
        dialog=dialog,
    )


def list_proposals(user: str | None = None) -> list[Proposal]:
    """Alle Vorschlaege; mit `user` nur die, die `decide` erlaubt (US-12).
    Ohne Argument ungefiltert (Rohzugriff)."""
    d = proposals_dir()
    d.mkdir(parents=True, exist_ok=True)
    proposals = []
    for f in sorted(d.glob("*.md")):
        p = _parse(f.read_text(encoding="utf-8"), f.stem)
        if user is not None and not access.can_read(user, p.meta):
            continue
        proposals.append(p)
    return sorted(proposals, key=lambda p: p.submitted_at, reverse=True)


def get_proposal(slug: str) -> Proposal | None:
    """Ungefilterter Rohzugriff. Fuer Nutzer-Sicht `get_proposal_for` verwenden."""
    if not is_valid_slug(slug):
        return None  # kein Pfad aus fremden Zeichen (../ etc.) bauen
    f = proposals_dir() / f"{slug}.md"
    if not f.exists():
        return None
    return _parse(f.read_text(encoding="utf-8"), slug)


def get_proposal_for(slug: str, user: str) -> Proposal | None:
    """Vorschlag aus Sicht eines Nutzers: None, wenn er fehlt ODER verboten ist."""
    p = get_proposal(slug)
    if p is None or not access.can_read(user, p.meta):
        return None
    return p


def already_submitted(project_name: str) -> bool:
    """Prueft, ob unter diesem Projektnamen bereits ein Vorschlag eingereicht wurde."""
    return (proposals_dir() / f"{slugify(project_name)}.md").exists()


def file_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def find_duplicate_file(uploaded_files: list[tuple[str, bytes]]) -> Proposal | None:
    """Prueft anhand des Datei-Hashes, ob eine der hochgeladenen Projektdateien
    inhaltsgleich zu einer bereits eingereichten Projektdatei ist - auch wenn
    der Projektname diesmal ein anderer ist (z.B. erneute Einreichung desselben
    Business Case unter neuem Titel)."""
    if not uploaded_files or not uploads_dir().exists():
        return None

    new_hashes = {file_hash(data) for _, data in uploaded_files if data}
    if not new_hashes:
        return None

    for proposal in list_proposals():
        if not proposal.upload_dir.exists():
            continue
        for existing_file in proposal.upload_dir.iterdir():
            if not existing_file.is_file():
                continue
            if file_hash(existing_file.read_bytes()) in new_hashes:
                return proposal
    return None


def save_proposal(
    project_name: str,
    description: str,
    uploaded_files: list[tuple[str, bytes]],
    meta: PageMeta | None = None,
    rolle: str = "",
    felder: dict[str, str] | None = None,
    dialog: list[dict[str, str]] | None = None,
) -> Proposal:
    """Speichert einen neuen Projektvorschlag. Ruft VOR dem Aufruf already_submitted()
    auf, um Duplikate abzulehnen - diese Funktion selbst prueft das nicht erneut.

    `meta.erstellt_von` ist der Einreicher (US-11) und zugleich die einzige
    Quelle fuer `submitted_by` (Paket 6, Projektantraege-Dashboard) - kein
    zweites, separat uebergebenes Feld dafuer. `rolle` ist sein Anzeigename
    zum Zeitpunkt der Einreichung (Snapshot); fehlt sie, wird sie nachgeschlagen.
    """
    slug = slugify(project_name)
    submitted_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    meta = meta or _default_meta()
    meta.quelle = SOURCE
    meta.domaene = meta.domaene or DEFAULT_DOMAIN
    if not meta.erstellt_am:
        meta.erstellt_am = datetime.now().replace(microsecond=0).isoformat()
    rolle = rolle or access.user_name(meta.erstellt_von)
    submitted_by = meta.erstellt_von

    proposals_dir().mkdir(parents=True, exist_ok=True)
    proposal = Proposal(
        slug=slug,
        project_name=project_name,
        description=description.strip(),
        submitted_at=submitted_at,
        submitted_by=submitted_by,
        files=[name for name, _ in uploaded_files if name],
        meta=meta,
        rolle=rolle,
        felder=dict(felder or {}),
        dialog=[dict(e) for e in (dialog or [])],
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
        f"{_render_head(meta, rolle, proposal.felder, proposal.dialog)}"
        f"# {project_name}\n\n"
        f"Eingereicht am: {submitted_at}\n"
        f"Eingereicht von: {submitted_by}\n"
        f"Status: {proposal.status}\n\n"
        f"## Beschreibung\n\n{proposal.description}\n\n"
        f"## Hochgeladene Dateien\n\n{files_section}\n",
        encoding="utf-8",
    )
    return proposal


def write_proposal(proposal: Proposal) -> Proposal:
    """Schreibt einen bereits vorhandenen Vorschlag zurueck (Felder, Status, Dialog).

    Anders als `save_proposal` legt das nichts Neues an und ruehrt die
    hochgeladenen Dateien nicht an - Einreicher, Zeitpunkt und Rolle bleiben,
    wie sie beim Einreichen festgehalten wurden (US-11).
    """
    files_section = (
        "\n".join(f"- {name}" for name in proposal.files)
        if proposal.files
        else "*(keine Dateien hochgeladen)*"
    )
    proposal.path.parent.mkdir(parents=True, exist_ok=True)
    proposal.path.write_text(
        f"{_render_head(proposal.meta, proposal.rolle, proposal.felder, proposal.dialog)}"
        f"# {proposal.project_name}\n\n"
        f"Eingereicht am: {proposal.submitted_at}\n"
        f"Eingereicht von: {proposal.submitted_by}\n"
        f"Status: {proposal.status}\n\n"
        f"## Beschreibung\n\n{proposal.description}\n\n"
        f"## Hochgeladene Dateien\n\n{files_section}\n",
        encoding="utf-8",
    )
    return proposal


def delete_proposal(slug: str) -> None:
    f = proposals_dir() / f"{slug}.md"
    if f.exists():
        f.unlink()
    upload_dir = uploads_dir() / slug
    if upload_dir.exists():
        shutil.rmtree(upload_dir)
