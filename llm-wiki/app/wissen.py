"""Wissensmanagement erweitern und zuruecksetzen (Phase 5 des Dachplans: UC-01, UC-03).

UC-03: Ein angemeldeter Anwender laedt eine oder mehrere Dateien hoch. Jede wird mit
den vorhandenen Extraktoren nach Markdown gewandelt, bekommt den Dokumentkopf nach
vorlagen/Vorlage_dokument_kopfdaten.md (deutsche Schluessel, Vertraulichkeit als
Rohstufe aus der Rollenvorgabe, ablageort erweiterung) und landet unter
corpus/erweiterung/<slug>.md. Danach laeuft qmd/ingest/import.py als Subprozess und
zeigt den Fortschritt "n von N" (NFR-11).

UC-01: Der Admin setzt getrennt zurueck: Unternehmenswissen (qmd/ingest/reset.py wissen,
danach optional Neuimport des Korpus mit "n von 218") und Projektantraege (Antragsdateien,
Uploads, Laeufe loeschen, dann reset.py antraege). Beides verlangt das Wort RESET.

Ein Job zugleich: Import und Reset schreiben in denselben Index (Fit-Gap A-5).
Das Wiki fuehrt je Job ein Verzeichnis <MPB_JOBS_DIR>/<job_id>/ mit job.json und log.

Umgebung (Vorgabe in Klammern; Tests unterschieben Stubs und Temp-Verzeichnisse):
  MPB_QMD_DIR         Arbeitsverzeichnis der Ingest-Skripte   (<repo>/qmd)
  MPB_CORPUS_DIR      Korpus, darunter erweiterung/           (<repo>/corpus)
  MPB_JOBS_DIR        Ablage der Jobs                          (<repo>/qmd/jobs)
  MPB_IMPORT_CMD      Befehl, shell-artig zerlegt              (uv run python ingest/import.py)
  MPB_RESET_CMD       Befehl, shell-artig zerlegt              (uv run python ingest/reset.py)
  MPB_INDEX_ANTRAEGE  "0" schaltet den Antrags-Import nach dem Einreichen ab (Tests)
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import threading
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from . import access, bewertung, extractors, llm_metadata, proposals, wiki

ROOT = Path(__file__).resolve().parent.parent.parent  # MediaparkBrain/

ABLAGEORT = "erweiterung"
DOMAENE = "allgemein"  # Zieldomaene laut qmd/ingest/mapping.yaml
# Der Korpus kennt genau drei Rohstufen (vorlagen/Vorlage_dokument_kopfdaten.md).
ERLAUBTE_STUFEN = ("intern", "C-Level", "Betriebsrat-intern")

# Feldfolge des Frontmatters, verbindlich nach der Vorlage; danach Herkunft (NFR-07).
FELDER = ("doc_id", "titel", "dokumenttyp", "datum", "verfasser", "rolle", "organisationseinheit",
          "empfaenger", "projekt", "geschaeftsbereich", "vertraulichkeit", "informationsdomaene",
          "ablageort")
HERKUNFT = ("quelle", "erstellt_von", "erstellt_am", "original_datei")

JOB_STATUS = "job.json"
LOG = "log"
STATUS_LAEUFT = "laeuft"
STATUS_FERTIG = "fertig"
STATUS_FEHLER = "fehler"
STATUS_TEXT = {STATUS_LAEUFT: "läuft", STATUS_FERTIG: "fertig", STATUS_FEHLER: "abgebrochen"}

FORTSCHRITT_RE = re.compile(r"^(Sicht: \d+ von \d+|Einbettung: \d+ %|Index: .+|Reset: .+|Fertig: .+|"
                            r"Wissen: .+|Antraege: .+|FEHLER: .+|ABBRUCH: .+)")

_PROZESSE: dict[str, subprocess.Popen] = {}
_SPERRE = threading.Lock()


class JobAktiv(RuntimeError):
    def __init__(self, job_id: str):
        super().__init__(f"Es läuft bereits der Job {job_id}")
        self.job_id = job_id


class Uploadfehler(ValueError):
    pass


# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------


def qmd_dir() -> Path:
    return bewertung.qmd_dir()


def corpus_dir() -> Path:
    env = os.environ.get("MPB_CORPUS_DIR")
    return Path(env) if env else ROOT / "corpus"


def erweiterung_dir() -> Path:
    return corpus_dir() / ABLAGEORT


def jobs_dir() -> Path:
    env = os.environ.get("MPB_JOBS_DIR")
    return Path(env) if env else qmd_dir() / "jobs"


def _cmd(env_name: str, skript: str) -> list[str]:
    env = os.environ.get(env_name)
    if env:
        import shlex
        teile = shlex.split(env, posix=False)
        return [t[1:-1] if len(t) >= 2 and t[0] == t[-1] and t[0] in "\"'" else t for t in teile]
    return [bewertung._uv(), "run", "python", skript]


def import_cmd() -> list[str]:
    return _cmd("MPB_IMPORT_CMD", "ingest/import.py")


def reset_cmd() -> list[str]:
    return _cmd("MPB_RESET_CMD", "ingest/reset.py")


def antraege_index_aktiv() -> bool:
    return os.environ.get("MPB_INDEX_ANTRAEGE", "1") != "0"


def _jetzt() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def korpus_anzahl() -> int:
    """Markdown-Dokumente unter corpus/ (UC-02: "n von N")."""
    d = corpus_dir()
    return sum(1 for _ in d.rglob("*.md")) if d.is_dir() else 0


# ---------------------------------------------------------------------------
# UC-03: Dokument anlegen
# ---------------------------------------------------------------------------


def stufe_fuer(user: str) -> str:
    """Rohstufe aus der Rollenvorgabe in permissions.yaml; der Korpus kennt nur drei."""
    stufe = access.default_confidentiality_for_user(user)
    return stufe if stufe in ERLAUBTE_STUFEN else "intern"


def _yaml_wert(v: Any) -> str:
    if isinstance(v, list):
        return "[" + ", ".join(str(x) for x in v) + "]"
    s = str(v if v is not None else "-").strip() or "-"
    # Doppelpunkt, Raute oder Anfuehrungszeichen brauchen Quotes, sonst bricht der Kopf
    # (siehe die Korrektur am PLM-Projektauftrag im Korpus).
    if any(c in s for c in ":#\"'") or s != s.strip() or s in ("-",):
        return json.dumps(s, ensure_ascii=False)
    return s


def _eindeutiger_slug(basis: str) -> str:
    d = erweiterung_dir()
    slug, n = basis, 1
    while (d / f"{slug}.md").exists():
        n += 1
        slug = f"{basis}-{n}"
    return slug


def frontmatter(meta: access.PageMeta, titel: str, stufe: str, user: str, filename: str,
                datum: str | None = None) -> str:
    heute = datetime.now().strftime("%Y-%m-%d")
    werte = {
        "doc_id": meta.doc_id or f"LTT-{datetime.now():%Y-%m%d}-UPLOAD-{datetime.now():%H%M%S}",
        "titel": titel,
        "dokumenttyp": meta.dokumenttyp or "Dokument",
        "datum": datum or meta.datum or heute,
        "verfasser": meta.verfasser or access.user_name(user),
        "rolle": meta.rolle or access.user_name(user),
        "organisationseinheit": meta.organisationseinheit or "-",
        "empfaenger": list(meta.empfaenger),
        "projekt": meta.projekt or "-",
        "geschaeftsbereich": meta.geschaeftsbereich or "-",
        "vertraulichkeit": stufe,
        "informationsdomaene": list(meta.informationsdomaene) or ["unternehmensweit"],
        "ablageort": ABLAGEORT,
        "quelle": "upload",
        "erstellt_von": user,
        "erstellt_am": _jetzt(),
        "original_datei": Path(filename).name,
    }
    zeilen = ["---"] + [f"{k}: {_yaml_wert(werte[k])}" for k in FELDER + HERKUNFT] + ["---"]
    return "\n".join(zeilen) + "\n"


def dokument_anlegen(filename: str, data: bytes, user: str) -> tuple[Path, str]:
    """Wandelt eine hochgeladene Datei in ein Korpusdokument unter corpus/erweiterung/.

    Rueckgabe: (Pfad der Markdown-Datei, Titel). Das Original liegt unter
    <uploads>/erweiterung/. Wirft Uploadfehler bei leerem Inhalt oder Extraktionsfehler.
    """
    if not filename:
        raise Uploadfehler("Datei ohne Namen.")
    if not data:
        raise Uploadfehler(f'Die Datei "{filename}" ist leer.')
    original = wiki.save_uploaded_file(filename, data, domaene=ABLAGEORT)
    try:
        text = extractors.extract_text_from_file(original, filename)
    except Exception as e:  # noqa: BLE001 - jeder Extraktionsfehler ist ein Nutzerfehler
        raise Uploadfehler(f'"{filename}": Textextraktion fehlgeschlagen: {e}') from e
    text = (text or "").strip()
    if not text:
        raise Uploadfehler(f'"{filename}": kein Text gefunden (Bild-PDF oder leeres Dokument).')

    stufe = stufe_fuer(user)
    _header, meta, titel = llm_metadata.generate_header(
        text, filename, user, custom_domain=DOMAENE, custom_confidentiality=stufe,
    )
    titel = (titel or Path(filename).stem).strip()
    slug = _eindeutiger_slug(wiki.slugify(titel))
    kopf = frontmatter(meta, titel, stufe, user, filename)
    einstufung = f"Einstufung: {stufe}\n" if stufe != "intern" else ""
    body = (
        f"# {titel}\n\n"
        f"**Lahnberg Thermotechnik GmbH & Co. KG** - {meta.organisationseinheit or '-'}\n"
        f"{meta.dokumenttyp or 'Dokument'}, hochgeladen von {access.user_name(user)}\n\n"
        f"Von:       {meta.verfasser or access.user_name(user)}\n"
        f"Datum:     {meta.datum or datetime.now().strftime('%Y-%m-%d')}\n"
        f"{einstufung}\n"
        f"{text}\n"
    )
    d = erweiterung_dir()
    d.mkdir(parents=True, exist_ok=True)
    ziel = d / f"{slug}.md"
    ziel.write_text(kopf + "\n" + body, encoding="utf-8")
    return ziel, titel


# ---------------------------------------------------------------------------
# Jobs: Import und Reset als Subprozess mit Fortschritt
# ---------------------------------------------------------------------------


@dataclass
class Job:
    job_id: str
    dir: Path
    art: str = ""
    titel: str = ""
    gestartet_von: str = ""
    gestartet_am: str = ""
    beendet_am: str | None = None
    exit_code: int | None = None
    dateien: list[str] = field(default_factory=list)
    weiter: str = "/"
    fortschritt: str = ""
    log_ende: str = ""
    status: str = STATUS_FEHLER
    fehler: str = ""

    @property
    def status_text(self) -> str:
        return STATUS_TEXT.get(self.status, self.status)

    @property
    def laeuft(self) -> bool:
        return self.status == STATUS_LAEUFT

    @property
    def fertig(self) -> bool:
        return self.status == STATUS_FERTIG

    @property
    def prozent(self) -> int | None:
        """Fortschritt in Prozent aus "Sicht: n von N" oder "Einbettung: p %"; sonst None."""
        if self.fertig:
            return 100
        m = re.match(r"Sicht: (\d+) von (\d+)", self.fortschritt)
        if m and int(m.group(2)) > 0:
            return int(100 * int(m.group(1)) / int(m.group(2)))
        m = re.match(r"Einbettung: (\d+) %", self.fortschritt)
        if m:
            return int(m.group(1))
        return None


def _status_lesen(d: Path) -> dict[str, Any]:
    f = d / JOB_STATUS
    if not f.exists():
        return {}
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _status_schreiben(d: Path, daten: dict[str, Any]) -> None:
    (d / JOB_STATUS).write_text(json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")


def aktiver_job() -> str | None:
    with _SPERRE:
        for job_id, p in list(_PROZESSE.items()):
            if p.poll() is None:
                return job_id
    return None


def _neue_job_id(art: str) -> str:
    basis = f"{art}-{datetime.now():%Y%m%d-%H%M%S}"
    job_id, n = basis, 1
    while (jobs_dir() / job_id).exists():
        n += 1
        job_id = f"{basis}-{n}"
    return job_id


def _warte(proc: subprocess.Popen, d: Path, log) -> None:
    try:
        code = proc.wait()
    finally:
        try:
            log.close()
        except OSError:
            pass
    daten = _status_lesen(d)
    daten["beendet_am"] = _jetzt()
    daten["exit_code"] = code
    _status_schreiben(d, daten)


def starte_job(art: str, cmd: list[str], user: str, titel: str, dateien: list[str] | None = None,
               weiter: str = "/") -> Job:
    """Startet einen Ingest-Subprozess aus qmd/. Ein Job zugleich, sonst JobAktiv."""
    with _SPERRE:
        for jid, p in list(_PROZESSE.items()):
            if p.poll() is None:
                raise JobAktiv(jid)
        job_id = _neue_job_id(art)
        d = jobs_dir() / job_id
        d.mkdir(parents=True, exist_ok=True)
        daten = {
            "job_id": job_id, "art": art, "titel": titel, "gestartet_von": user,
            "gestartet_am": _jetzt(), "beendet_am": None, "exit_code": None,
            "dateien": list(dateien or []), "weiter": weiter, "cmd": cmd,
        }
        _status_schreiben(d, daten)
        env = dict(os.environ)
        env["MPB_CORPUS_DIR"] = str(corpus_dir())
        env["MPB_PROPOSALS_DIR"] = str(proposals.proposals_dir())
        env.setdefault("PYTHONIOENCODING", "utf-8")
        log = (d / LOG).open("ab")
        try:
            proc = subprocess.Popen(cmd, cwd=str(qmd_dir()), stdout=log, stderr=subprocess.STDOUT, env=env)
        except OSError as e:
            log.close()
            daten["beendet_am"] = _jetzt()
            daten["exit_code"] = -1
            daten["fehler"] = f"Job nicht startbar: {e}"
            _status_schreiben(d, daten)
            return lies_job(d)
        _PROZESSE[job_id] = proc
    threading.Thread(target=_warte, args=(proc, d, log), daemon=True).start()
    return lies_job(d)


def _log(d: Path) -> list[str]:
    f = d / LOG
    if not f.exists():
        return []
    try:
        return f.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []


def lies_job(d: Path) -> Job:
    w = _status_lesen(d)
    job = Job(job_id=w.get("job_id") or d.name, dir=d, art=str(w.get("art") or ""),
              titel=str(w.get("titel") or ""), gestartet_von=str(w.get("gestartet_von") or ""),
              gestartet_am=str(w.get("gestartet_am") or ""), beendet_am=w.get("beendet_am"),
              exit_code=w.get("exit_code"), dateien=list(w.get("dateien") or []),
              weiter=str(w.get("weiter") or "/"), fehler=str(w.get("fehler") or ""))
    zeilen = _log(d)
    for z in reversed(zeilen):
        if FORTSCHRITT_RE.match(z.strip()):
            job.fortschritt = z.strip()
            break
    job.log_ende = "\n".join(zeilen[-20:])
    if job.exit_code is not None:
        job.status = STATUS_FERTIG if job.exit_code == 0 else STATUS_FEHLER
    elif job.fehler:
        job.status = STATUS_FEHLER
    else:
        p = _PROZESSE.get(job.job_id)
        job.status = STATUS_LAEUFT if (p is not None and p.poll() is None) else STATUS_FEHLER
    return job


def job_fuer(job_id: str) -> Job | None:
    if not job_id or "/" in job_id or "\\" in job_id or ".." in job_id:
        return None
    d = jobs_dir() / job_id
    if not d.is_dir():
        return None
    return lies_job(d)


def letzte_jobs(n: int = 10) -> list[Job]:
    basis = jobs_dir()
    if not basis.exists():
        return []
    jobs = [lies_job(d) for d in basis.iterdir() if d.is_dir() and (d / JOB_STATUS).exists()]
    jobs.sort(key=lambda j: (j.gestartet_am, j.job_id), reverse=True)
    return jobs[:n]


def darf_sehen(job: Job, user: str) -> bool:
    return job.gestartet_von == user or access.is_admin(user)


# ---------------------------------------------------------------------------
# Die vier Aufgaben
# ---------------------------------------------------------------------------


def starte_import_erweiterung(user: str, dateien: list[str]) -> Job:
    return starte_job("import-erweiterung", import_cmd() + ["wissen", "--ablageort", ABLAGEORT], user,
                      f"{len(dateien)} Dokument(e) in die Wissensbasis aufnehmen", dateien,
                      weiter="/wissen/upload")


def starte_import_corpus(user: str) -> Job:
    return starte_job("import-corpus", import_cmd() + ["wissen"], user,
                      "Unternehmenswissen aus corpus/ importieren", weiter="/admin")


def starte_import_antraege(user: str) -> Job | None:
    """Nach dem Einreichen: Antraege in die Collection antraege, ohne Wartezeit fuer
    den Nutzer. Laeuft ein anderer Job, wird uebersprungen und das vermerkt; der Admin
    kann den Import jederzeit nachholen."""
    if not antraege_index_aktiv():
        return None
    try:
        return starte_job("import-antraege", import_cmd() + ["antraege"], user,
                          "Projektantraege in den Index aufnehmen", weiter="/proposals")
    except JobAktiv:
        return None


def reset_wissen(user: str) -> Job:
    return starte_job("reset-wissen", reset_cmd() + ["wissen"], user,
                      "Unternehmenswissen zurücksetzen", weiter="/admin")


def _leeren(d: Path) -> int:
    """Loescht den Inhalt eines Verzeichnisses, nicht das Verzeichnis. Rueckgabe: Eintraege."""
    if not d.is_dir():
        return 0
    n = 0
    for p in list(d.iterdir()):
        if p.name == ".gitkeep":
            continue
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
        n += 1
    return n


def reset_antraege(user: str) -> Job:
    """Antragsdateien, Uploads und Bewertungslaeufe loeschen, dann den Index-Teil."""
    if aktiver_job():
        raise JobAktiv(aktiver_job() or "")
    geloescht = _leeren(proposals.proposals_dir())
    geloescht += _leeren(bewertung.laeufe_dir())
    return starte_job("reset-antraege", reset_cmd() + ["antraege"], user,
                      f"Projektanträge zurücksetzen ({geloescht} Einträge gelöscht)", weiter="/admin")
