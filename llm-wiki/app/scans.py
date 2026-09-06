"""Block "Zuletzt gescannt" der Wissensuebersicht.

Zwei Quellen, klar getrennt:

1. **Pseudodaten** aus `<MPB_DATA_DIR>/scans.json`. Die Datei wird beim ersten
   Aufruf angelegt, jeder Eintrag traegt `demo: true` und wird in der Anzeige
   als "Demo" ausgezeichnet. Sie steht fuer die Ablageorte des Korpus
   (SharePoint, Projektlaufwerk, ...), die ein echter Konnektor spaeter
   wirklich scannen wuerde. Nichts daran ist gemessen.
2. **Echte Uploads** aus `uploads/<domaene>/` - die letzten fuenf nach mtime,
   und ausschliesslich aus Domaenen, die der Nutzer lesen darf. Ein Dateiname
   verraet oft den Inhalt; deshalb gilt hier dieselbe Ordner-Schranke wie
   ueberall (`access.readable_domains`).
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from . import access, wiki
from .usage import data_dir

log = logging.getLogger(__name__)

SCANS_NAME = "scans.json"
MAX_UPLOADS = 5

# Vier Ablageorte aus dem Korpus - siehe Kommentarspalte in permissions.yaml.
DEMO_SOURCES = [
    ("SharePoint / sharepoint_finance", 20, "gescannt, 3 neu"),
    ("Projektlaufwerk / projektlaufwerk", 34, "gescannt, 1 neu"),
    ("SharePoint / sharepoint_hr", 12, "gescannt, keine Änderung"),
    ("IT-Dokumentation / it_doku", 27, "gescannt, 2 neu"),
]


def scans_path() -> Path:
    return data_dir() / SCANS_NAME


def _demo_entries() -> list[dict[str, Any]]:
    stamp = datetime.now().replace(microsecond=0).isoformat()
    return [
        {"quelle": quelle, "anzahl": anzahl, "zeit": stamp, "status": status, "demo": True}
        for quelle, anzahl, status in DEMO_SOURCES
    ]


def load_demo_scans() -> list[dict[str, Any]]:
    """Liest scans.json; legt sie beim ersten Aufruf mit Pseudodaten an."""
    path = scans_path()
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            log.warning("scans.json nicht lesbar (%s) - Pseudodaten werden verwendet", e)
            return _demo_entries()
        if isinstance(data, list):
            # `demo` nie aus der Datei uebernehmen, ohne es zu erzwingen: was
            # hier steht, ist per Definition nicht gemessen.
            return [{**e, "demo": bool(e.get("demo", True))} for e in data if isinstance(e, dict)]
        return _demo_entries()
    entries = _demo_entries()
    try:
        path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as e:
        log.warning("scans.json nicht schreibbar: %s", e)
    return entries


def _upload_entries(user: str | None) -> list[dict[str, Any]]:
    """Die letzten Uploads - nur aus Domaenenordnern, die `user` lesen darf."""
    root = wiki.uploads_dir()
    erlaubt = set(access.readable_domains(user))
    gefunden: list[tuple[float, dict[str, Any]]] = []
    for sub in sorted(root.iterdir()) if root.is_dir() else []:
        if not sub.is_dir() or sub.name not in erlaubt:
            continue
        for f in sub.iterdir():
            if not f.is_file() or f.name.startswith("."):
                continue
            try:
                mtime = f.stat().st_mtime
            except OSError:
                continue
            gefunden.append((mtime, {
                "quelle": f"Upload / {sub.name}/{f.name}",
                "anzahl": 1,
                "zeit": datetime.fromtimestamp(mtime).replace(microsecond=0).isoformat(),
                "status": "übernommen",
                "demo": False,
            }))
    gefunden.sort(key=lambda x: x[0], reverse=True)
    return [entry for _, entry in gefunden[:MAX_UPLOADS]]


def recent_scans(user: str | None) -> list[dict[str, Any]]:
    """Echte Uploads zuerst (die sind aktuell), danach die Pseudodaten."""
    return _upload_entries(user) + load_demo_scans()
