"""Bewertungslaeufe (Phase 4 des Dachplans: UC-04, UC-05, AE-04).

Das Wiki bewertet nicht selbst. Es startet fuer einen benannten Antrag den geskripteten
Orchestrator aus qmd/agenten/ als Subprozess, zeigt den Fortschritt (NFR-11) und rendert
das Ergebnis: je Rolle genau das Kapitel-17-Objekt, darueber die Kapitel-16-Aggregation.
Essay und Zitate kommen aus <rolle>.protokoll.json als aufklappbarer Beleg, nicht als
Felder (AE-04). Der fruehere Vorlaeufer app/evaluation.py (vier Rollen in einem
Haiku-Aufruf, ohne Wissensbasis) ist damit abgeloest.

Ablage je Lauf: <MPB_LAEUFE_DIR>/<lauf_id>/. Die Dateien dort schreibt der Orchestrator
(gate.json, informationsanforderung.json, vorbedingungen.json, <rolle>.jsonl,
<rolle>.protokoll.json, bewertungen.jsonl, zusammenfassung.json). Das Wiki fuehrt daneben
seine eigene Statusdatei wiki.json (Antrag, Nutzer, Start, Ende, Exit-Code) und
orchestrator.log; der Orchestrator selbst bleibt unveraendert.

Ein Lauf zugleich (Fit-Gap A-5, Regel Z1): der Reranker ist eine Instanz.

Umgebung (Vorgaben fuer den Betrieb; Tests unterschieben einen Stub):
  MPB_QMD_DIR           Arbeitsverzeichnis des Orchestrators      (<repo>/qmd)
  MPB_ORCHESTRATOR_CMD  Befehl, shell-artig zerlegt                (uv run python agenten/orchestrator.py)
  MPB_LAEUFE_DIR        Ablage der Laeufe                          (<repo>/qmd/laeufe)
"""
from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
import threading
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from . import proposals
from .wiki import split_frontmatter_raw

ROOT = Path(__file__).resolve().parent.parent.parent  # MediaparkBrain/
QMD_DIR = ROOT / "qmd"

# Kapitel 17.1: Reihenfolge der Rollen; Anzeigenamen aus PLAN.md Abschnitt 6.
ROLLEN: tuple[str, ...] = ("betriebsrat", "cfo", "it", "ceo")
ROLLEN_NAMEN: dict[str, str] = {
    "betriebsrat": "Betriebsrat / Employee Interests",
    "cfo": "CFO / Controlling",
    "it": "IT / Architektur / Cybersecurity",
    "ceo": "CEO / Strategie",
}

STATUS_LAEUFT = "laeuft"
STATUS_FERTIG = "fertig"
STATUS_GATE = "gate"
STATUS_VORBEDINGUNG = "vorbedingung"
STATUS_ABGEBROCHEN = "abgebrochen"

STATUS_TEXT = {
    STATUS_LAEUFT: "läuft",
    STATUS_FERTIG: "fertig",
    STATUS_GATE: "Rückfrage: Antrag unvollständig",
    STATUS_VORBEDINGUNG: "abgebrochen: Vorbedingung verletzt",
    STATUS_ABGEBROCHEN: "abgebrochen",
}

WIKI_STATUS = "wiki.json"
LOG = "orchestrator.log"

# Laufende Prozesse dieses Wiki-Prozesses: lauf_id -> Popen. Ein Lauf zugleich.
_PROZESSE: dict[str, subprocess.Popen] = {}
_SPERRE = threading.Lock()


class LaufAktiv(RuntimeError):
    """Es laeuft bereits ein Bewertungslauf (A-5, Z1)."""

    def __init__(self, lauf_id: str):
        super().__init__(f"Es läuft bereits der Bewertungslauf {lauf_id}")
        self.lauf_id = lauf_id


# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------


def qmd_dir() -> Path:
    env = os.environ.get("MPB_QMD_DIR")
    return Path(env) if env else QMD_DIR


def laeufe_dir() -> Path:
    env = os.environ.get("MPB_LAEUFE_DIR")
    return Path(env) if env else qmd_dir() / "laeufe"


def _uv() -> str:
    """uv wie in run.ps1: PATH, sonst der WinGet-Link."""
    found = shutil.which("uv")
    if found:
        return found
    local = os.environ.get("LOCALAPPDATA")
    if local:
        kandidat = Path(local) / "Microsoft" / "WinGet" / "Links" / "uv.exe"
        if kandidat.exists():
            return str(kandidat)
    return "uv"


def orchestrator_cmd() -> list[str]:
    env = os.environ.get("MPB_ORCHESTRATOR_CMD")
    if env:
        # posix=False laesst Windows-Pfade mit Backslash stehen; umschliessende
        # Anfuehrungszeichen (Pfade mit Leerzeichen) werden je Token entfernt.
        teile = shlex.split(env, posix=False)
        return [t[1:-1] if len(t) >= 2 and t[0] == t[-1] and t[0] in "\"'" else t for t in teile]
    return [_uv(), "run", "python", "agenten/orchestrator.py"]


def _jetzt() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


# ---------------------------------------------------------------------------
# Antragsdateien: die Projektklammer
# ---------------------------------------------------------------------------


def _project_id(pfad: Path) -> str:
    try:
        head, _ = split_frontmatter_raw(pfad.read_text(encoding="utf-8"))
    except OSError:
        return ""
    if not head:
        return ""
    return str(head.get("project_id") or "").strip()


def antrag_dateien(proposal: proposals.Proposal, user: str) -> list[Path]:
    """Alle Dateien, die zum Antrag gehoeren, in fester Reihenfolge.

    1. die Markdown-Datei des Antrags selbst,
    2. weitere Antraege mit derselben `project_id` im Kopf (Projektklammer: Steckbrief und
       Business Case liegen als zwei Dateien vor), sofern der Nutzer sie lesen darf,
    3. hochgeladene Markdown-Dateien unter uploads/<slug>/.
    """
    dateien: list[Path] = [proposal.path]
    pid = _project_id(proposal.path)
    if pid:
        for other in proposals.list_proposals(user):
            if other.slug == proposal.slug:
                continue
            if _project_id(other.path) == pid:
                dateien.append(other.path)
    if proposal.upload_dir.exists():
        for f in sorted(proposal.upload_dir.iterdir()):
            if f.is_file() and f.suffix.lower() == ".md":
                dateien.append(f)
    return dateien


# ---------------------------------------------------------------------------
# Lauf: starten, ueberwachen, lesen
# ---------------------------------------------------------------------------


@dataclass
class Lauf:
    lauf_id: str
    dir: Path
    slug: str = ""
    antraege: list[str] = field(default_factory=list)
    dateien: list[str] = field(default_factory=list)
    gestartet_von: str = ""
    gestartet_am: str = ""
    beendet_am: str | None = None
    exit_code: int | None = None
    status: str = STATUS_ABGEBROCHEN
    fortschritt: list[dict[str, str]] = field(default_factory=list)  # {rolle, name, zustand}
    aktuelle_rolle: str | None = None

    @property
    def status_text(self) -> str:
        return STATUS_TEXT.get(self.status, self.status)

    @property
    def laeuft(self) -> bool:
        return self.status == STATUS_LAEUFT

    @property
    def fertig(self) -> bool:
        return self.status == STATUS_FERTIG


def _wiki_status_lesen(d: Path) -> dict[str, Any]:
    f = d / WIKI_STATUS
    if not f.exists():
        return {}
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _wiki_status_schreiben(d: Path, daten: dict[str, Any]) -> None:
    (d / WIKI_STATUS).write_text(json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")


def _json(d: Path, name: str) -> dict[str, Any] | None:
    f = d / name
    if not f.exists():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _prozess_laeuft(lauf_id: str) -> bool:
    p = _PROZESSE.get(lauf_id)
    return p is not None and p.poll() is None


def aktiver_lauf() -> str | None:
    """lauf_id des gerade laufenden Prozesses, sonst None."""
    with _SPERRE:
        for lauf_id, p in list(_PROZESSE.items()):
            if p.poll() is None:
                return lauf_id
    return None


def neue_lauf_id(slug: str) -> str:
    basis = f"{slug}-{datetime.now():%Y%m%d-%H%M%S}"
    lauf_id, n = basis, 1
    while (laeufe_dir() / lauf_id).exists():
        n += 1
        lauf_id = f"{basis}-{n}"
    return lauf_id


def _warte(lauf_id: str, proc: subprocess.Popen, d: Path, log) -> None:
    try:
        code = proc.wait()
    finally:
        try:
            log.close()
        except OSError:
            pass
    daten = _wiki_status_lesen(d)
    daten["beendet_am"] = _jetzt()
    daten["exit_code"] = code
    _wiki_status_schreiben(d, daten)


def starte_lauf(proposal: proposals.Proposal, user: str) -> Lauf:
    """Startet den Orchestrator fuer diesen Antrag. Ein Lauf zugleich, sonst LaufAktiv."""
    with _SPERRE:
        for lid, p in list(_PROZESSE.items()):
            if p.poll() is None:
                raise LaufAktiv(lid)
        dateien = antrag_dateien(proposal, user)
        lauf_id = neue_lauf_id(proposal.slug)
        d = laeufe_dir() / lauf_id
        d.mkdir(parents=True, exist_ok=True)
        cmd = orchestrator_cmd()
        for f in dateien:
            cmd += ["--antrag", str(f)]
        cmd += ["--lauf", lauf_id]
        antraege = [proposal.slug] + [
            p.slug for p in proposals.list_proposals(user)
            if p.slug != proposal.slug and p.path in dateien
        ]
        daten = {
            "lauf_id": lauf_id,
            "slug": proposal.slug,
            "antraege": antraege,
            "dateien": [str(f) for f in dateien],
            "gestartet_von": user,
            "gestartet_am": _jetzt(),
            "beendet_am": None,
            "exit_code": None,
            "cmd": cmd,
        }
        _wiki_status_schreiben(d, daten)
        env = dict(os.environ)
        env["MPB_LAEUFE_DIR"] = str(laeufe_dir())
        log = (d / LOG).open("ab")
        try:
            proc = subprocess.Popen(cmd, cwd=str(qmd_dir()), stdout=log, stderr=subprocess.STDOUT, env=env)
        except OSError as e:
            log.close()
            daten["beendet_am"] = _jetzt()
            daten["exit_code"] = -1
            daten["fehler"] = f"Orchestrator nicht startbar: {e}"
            _wiki_status_schreiben(d, daten)
            return lies_lauf(d)
        _PROZESSE[lauf_id] = proc
    threading.Thread(target=_warte, args=(lauf_id, proc, d, log), daemon=True).start()
    return lies_lauf(d)


def lies_lauf(d: Path) -> Lauf:
    """Zustand eines Laufs aus seinen Dateien: Status, Fortschritt je Rolle."""
    w = _wiki_status_lesen(d)
    lauf = Lauf(
        lauf_id=w.get("lauf_id") or d.name,
        dir=d,
        slug=str(w.get("slug") or ""),
        antraege=list(w.get("antraege") or []),
        dateien=list(w.get("dateien") or []),
        gestartet_von=str(w.get("gestartet_von") or ""),
        gestartet_am=str(w.get("gestartet_am") or ""),
        beendet_am=w.get("beendet_am"),
        exit_code=w.get("exit_code"),
    )
    if (d / "zusammenfassung.json").exists():
        lauf.status = STATUS_FERTIG
    elif (d / "informationsanforderung.json").exists():
        lauf.status = STATUS_GATE
    elif (d / "vorbedingungen.json").exists():
        lauf.status = STATUS_VORBEDINGUNG
    elif lauf.beendet_am or w.get("fehler"):
        lauf.status = STATUS_ABGEBROCHEN
    elif _prozess_laeuft(lauf.lauf_id):
        lauf.status = STATUS_LAEUFT
    else:
        # Kein Prozess mehr und kein Ergebnis: etwa nach einem Neustart des Wikis.
        lauf.status = STATUS_ABGEBROCHEN

    gate = _json(d, "gate.json")
    gate_ok = bool(gate and gate.get("bestanden"))
    laufend_gesetzt = False
    for rolle in ROLLEN:
        if (d / f"{rolle}.jsonl").exists():
            zustand = "fertig"
        elif (d / f"{rolle}.protokoll.json").exists():
            zustand = "fehler"
        elif lauf.status == STATUS_LAEUFT and gate_ok and not laufend_gesetzt:
            zustand = "laeuft"
            laufend_gesetzt = True
            lauf.aktuelle_rolle = rolle
        else:
            zustand = "offen"
        lauf.fortschritt.append({"rolle": rolle, "name": ROLLEN_NAMEN[rolle], "zustand": zustand})
    return lauf


def laeufe_fuer(slug: str) -> list[Lauf]:
    """Alle Laeufe, in denen dieser Antrag enthalten war, neuester zuerst."""
    basis = laeufe_dir()
    if not basis.exists():
        return []
    out: list[Lauf] = []
    for d in basis.iterdir():
        if not d.is_dir():
            continue
        w = _wiki_status_lesen(d)
        if not w:
            continue
        if w.get("slug") == slug or slug in (w.get("antraege") or []):
            out.append(lies_lauf(d))
    out.sort(key=lambda l: (l.gestartet_am, l.lauf_id), reverse=True)
    return out


def letzter_lauf(slug: str) -> Lauf | None:
    laeufe = laeufe_fuer(slug)
    return laeufe[0] if laeufe else None


def lauf_fuer(slug: str, lauf_id: str | None) -> Lauf | None:
    """Ein bestimmter Lauf, aber nur, wenn er zu diesem Antrag gehoert; sonst None."""
    if not lauf_id:
        return letzter_lauf(slug)
    if "/" in lauf_id or "\\" in lauf_id or ".." in lauf_id:
        return None
    d = laeufe_dir() / lauf_id
    if not d.is_dir():
        return None
    w = _wiki_status_lesen(d)
    if w.get("slug") != slug and slug not in (w.get("antraege") or []):
        return None
    return lies_lauf(d)


# ---------------------------------------------------------------------------
# Ergebnis: Kapitel 17 je Rolle, Kapitel 16 darueber, Beleg aus dem Protokoll
# ---------------------------------------------------------------------------


@dataclass
class Rollenkarte:
    rolle: str
    name: str
    zeile: dict[str, Any] | None = None       # Kapitel-17-Objekt (acht Felder)
    fehler: list[str] = field(default_factory=list)  # technische Fehler dieser Rolle
    protokoll: dict[str, Any] | None = None   # Beleg: Essay, Zitate, Abfragen, Zeiten


@dataclass
class Ergebnis:
    lauf: Lauf
    zusammenfassung: dict[str, Any] | None = None
    karten: list[Rollenkarte] = field(default_factory=list)
    informationsanforderung: dict[str, Any] | None = None
    vorbedingungen: dict[str, Any] | None = None
    gate: dict[str, Any] | None = None
    log_ende: str = ""


def _log_ende(d: Path, zeilen: int = 25) -> str:
    f = d / LOG
    if not f.exists():
        return ""
    try:
        text = f.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return "\n".join(text.splitlines()[-zeilen:])


def lade_ergebnis(lauf: Lauf) -> Ergebnis:
    d = lauf.dir
    erg = Ergebnis(lauf=lauf)
    erg.gate = _json(d, "gate.json")
    erg.informationsanforderung = _json(d, "informationsanforderung.json")
    erg.vorbedingungen = _json(d, "vorbedingungen.json")
    erg.zusammenfassung = _json(d, "zusammenfassung.json")
    if lauf.status == STATUS_ABGEBROCHEN:
        erg.log_ende = _log_ende(d)

    z = erg.zusammenfassung or {}
    zeilen = {r.get("rolle"): r for r in z.get("rollen") or [] if isinstance(r, dict)}
    fehler_je_rolle: dict[str, list[str]] = {r: [] for r in ROLLEN}
    for t in z.get("technische_fehler") or []:
        if isinstance(t, dict) and t.get("rolle") in fehler_je_rolle:
            fehler_je_rolle[t["rolle"]].append(str(t.get("fehler") or "technischer Fehler"))
    for zf in z.get("zeilenfehler") or []:
        if isinstance(zf, dict) and zf.get("rolle") in fehler_je_rolle:
            fehler_je_rolle[zf["rolle"]].append(f"17.5: {zf.get('fehler')}")

    for rolle in ROLLEN:
        karte = Rollenkarte(rolle=rolle, name=ROLLEN_NAMEN[rolle])
        karte.zeile = zeilen.get(rolle)
        karte.fehler = fehler_je_rolle[rolle]
        karte.protokoll = _json(d, f"{rolle}.protokoll.json")
        if karte.zeile is None and not karte.fehler and karte.protokoll:
            tf = karte.protokoll.get("technischer_fehler")
            if isinstance(tf, dict):
                karte.fehler.append(f"{tf.get('art')}: {tf.get('details')}")
        erg.karten.append(karte)
    return erg


def gesamt(lauf: Lauf) -> dict[str, Any] | None:
    """Gesamtscore und Gesamtstatus eines fertigen Laufs fuer Listen, sonst None."""
    z = _json(lauf.dir, "zusammenfassung.json")
    if not z:
        return None
    return {"gesamtscore": z.get("gesamtscore"), "gesamtstatus": z.get("gesamtstatus"),
            "anzahl_bewertet": z.get("anzahl_bewertet")}


def risk_class(score: float | int | None) -> str:
    """Ampel als Darstellung (nicht Teil der Bewertungslogik): 7 bis 10 gruen,
    4 bis 6 gelb, 0 bis 3 rot, ohne Score grau."""
    if score is None:
        return "risk-neutral"
    if score >= 7:
        return "risk-green"
    if score >= 4:
        return "risk-amber"
    return "risk-red"


def dezimal(wert: float | int | None) -> str:
    """Gesamtscore auf eine Dezimalstelle mit Komma (Kapitel 16.1); None wird KEIN SCORE."""
    if wert is None:
        return "KEIN SCORE"
    return f"{float(wert):.1f}".replace(".", ",")
