"""Ergebnis-Cache der Experten-Bewertung (data/evaluations/<slug>.json).

Warum ein Cache: `evaluation.evaluate_proposal` ruft das LLM und braucht bis zu
einer Minute. Dashboard und Antragsdetail zeigen aber bei jedem Aufruf Scores.
Ohne Cache waere jede Seitenansicht ein LLM-Lauf - langsam, teuer und bei jedem
Aufruf ein anderes Ergebnis. Der Cache ist die einzige Quelle fuer angezeigte
Scores: steht dort nichts, zeigt die Oberflaeche "kein Score" (state 'none') und
nicht etwa einen geschaetzten Wert.

Ablage unter `data/evaluations/`, per Env MPB_DATA_DIR ueberschreibbar (Tests).
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from .wiki import is_valid_slug

log = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def data_dir() -> Path:
    env = os.environ.get("MPB_DATA_DIR")
    return Path(env) if env else DATA_DIR


def evaluations_dir() -> Path:
    d = data_dir() / "evaluations"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _path(slug: str) -> Path | None:
    # Kein Pfad aus fremden Zeichen (../ etc.) - gleiche Regel wie bei Seiten.
    if not is_valid_slug(slug):
        return None
    return evaluations_dir() / f"{slug}.json"


def load(slug: str) -> dict | None:
    """Gespeichertes Bewertungsergebnis oder None (nie ein Ersatzwert)."""
    path = _path(slug)
    if path is None or not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("Bewertungs-Cache %s unlesbar: %s", slug, exc)
        return None
    return data if isinstance(data, dict) else None


def store(slug: str, data: dict) -> Path | None:
    path = _path(slug)
    if path is None:
        return None
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def all() -> dict[str, dict]:
    """Alle gespeicherten Bewertungen als {slug: daten}."""
    out: dict[str, dict] = {}
    for f in sorted(evaluations_dir().glob("*.json")):
        data = load(f.stem)
        if data is not None:
            out[f.stem] = data
    return out
