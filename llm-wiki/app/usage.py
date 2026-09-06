"""Zugriffsprotokoll: wer hat wann welche Seite gelesen.

Bewusst schmal: eine Zeile JSON je erfolgreichem Aufruf, mehr nicht. Es wird
NUR protokolliert, was ein Nutzer auch sehen durfte - `main.view_page` ruft
`record_view` erst NACH `require_page` auf. Ein 404 (fehlend oder verboten)
hinterlaesst keine Spur; sonst waere das Protokoll selbst ein Kanal, aus dem
sich die Existenz verbotener Seiten ablesen liesse.

Ablage: `<MPB_DATA_DIR>/access-log.jsonl`, Standard `llm-wiki/data/`. Der
Ordner ist in .gitignore - Zugriffsdaten gehoeren nicht ins Repository.

Hinweis zur Betriebsvereinbarung (siehe Betriebsratsprotokoll im Korpus): Das
hier ist ein Demonstrator. Ein echter Betrieb braucht Loeschfristen und den
Verzicht auf personenbezogene Auswertung; beides ist hier NICHT umgesetzt.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from pathlib import Path

log = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LOG_NAME = "access-log.jsonl"


def data_dir() -> Path:
    env = os.environ.get("MPB_DATA_DIR")
    d = Path(env) if env else DATA_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def log_path() -> Path:
    return data_dir() / LOG_NAME


def record_view(slug: str, user: str) -> None:
    """Haengt eine Zeile an das Protokoll. Fehler beim Schreiben duerfen den
    Seitenaufruf nie kippen - das Protokoll ist Beiwerk, nicht die Funktion."""
    entry = {
        "ts": datetime.now().replace(microsecond=0).isoformat(),
        "slug": slug,
        "user": user,
    }
    try:
        with log_path().open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as e:
        log.warning("Zugriffsprotokoll nicht schreibbar: %s", e)


def _entries() -> list[dict]:
    path = log_path()
    if not path.exists():
        return []
    out: list[dict] = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue  # kaputte Zeile ueberspringen, nicht die ganze Datei verlieren
            if isinstance(data, dict) and data.get("slug"):
                out.append(data)
    except OSError as e:
        log.warning("Zugriffsprotokoll nicht lesbar: %s", e)
        return []
    return out


def stats_for(slugs: list[str] | set[str]) -> dict[str, dict]:
    """{slug: {views, last_view, last_viewer}} - nur fuer die uebergebenen Slugs.

    Der Aufrufer uebergibt die Slugs, die der Nutzer sehen darf; damit kann
    ueber diese Funktion nichts ueber fremde Seiten herauskommen.
    """
    wanted = set(slugs)
    out: dict[str, dict] = {
        s: {"views": 0, "last_view": "", "last_viewer": ""} for s in wanted
    }
    for entry in _entries():
        slug = entry.get("slug")
        if slug not in wanted:
            continue
        row = out[slug]
        row["views"] += 1
        ts = str(entry.get("ts") or "")
        if ts >= row["last_view"]:   # ISO-Zeitstempel sortieren als Text korrekt
            row["last_view"] = ts
            row["last_viewer"] = str(entry.get("user") or "")
    return out
