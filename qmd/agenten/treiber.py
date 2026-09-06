"""Treiber: eine Rolle, ein Antrag, ein Lauf.

Generische Fassung des CFO-Treibers `qmd/eval/cfo_e2e.py` nach `.plans/08_orchestrator.md`.
Die Kette je Rolle:

    Prompt aus Modulen  ->  Werkzeugrunden (Agent fragt die Wissensbasis selbst)
    ->  Zug A: Essay mit API-Zitaten ueber document-Bloecke
    ->  Zug B: Bewertungsfelder per Structured Output (client.messages.parse)
    ->  Zeile nach Kapitel 17 (AE-04: acht Felder, flach) in <rolle>.jsonl
    ->  Laufmetadaten in <rolle>.protokoll.json

Zuverlaessigkeitsregeln Z1 bis Z13 aus 08 Abschnitt 3 sind im Code markiert. Z2, Z5, Z12
und Z13 folgen der Diagnose des Laufs vom 06.09.2026 05:12 (`.test/1b_diagnose.md`):
Abstuerze des Rerankers auf CUDA wurden als Nulltreffer gelesen, und die qmd-Scores sind je
Abfrage normiert, weshalb eine abfrageuebergreifende Sortierung die Golden-Dokumente
verdraengt hat.

Umgebungsvariablen des Treibers:
    TREIBER_QMD_GPU        Geraet fuer qmd-Abfragen (Z13), Vorgabe vulkan; cuda, metal, auto
    TREIBER_QMD_TYPISIERT  1 = Agentenfragen als lex:/vec:-Anfragedokument (ohne Erweiterung)
    EVAL_MODEL             Modellkennung, Vorgabe claude-opus-5

Aufruf, aus qmd/ in dessen uv-Umgebung (pyproject.toml, einmalig `uv sync`):
    uv run python agenten/treiber.py --rolle cfo --antrag ../project_proposals/a.md \
        --antrag ../project_proposals/b.md --lauf <id>
    uv run python agenten/treiber.py --rolle it --antrag ... --dry-run   # nur Prompt, keine API

Der Aufrufpfad steht ausschliesslich in AUFRUF unten; nach einer Umgebungsaenderung ist
das die einzige Stelle.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

AGENTEN_DIR = Path(__file__).resolve().parent
QMD_DIR = AGENTEN_DIR.parent
ROOT = QMD_DIR.parent
LAEUFE_DIR = QMD_DIR / "laeufe"
CORPUS_DIR = ROOT / "corpus"

for _p in (str(QMD_DIR / "ingest"), str(AGENTEN_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from rollen import RollenFehler, collections_for_role  # noqa: E402
from schema import ROLLEN, Bewertungsfelder, Zeile  # noqa: E402
from pydantic import ValidationError  # noqa: E402

AUFRUF = "uv run python agenten/treiber.py"  # aus qmd/, eigene uv-Umgebung

MODELL = os.environ.get("EVAL_MODEL", "claude-opus-5")
MAX_TOOL_RUNDEN = 6          # harte Grenze; das Abfragebudget im Initialteil nennt vier Runden
TREFFER_JE_ABFRAGE = 8       # Z5: -n je Abfrage
KONTEXT_DECKEL = 16          # Z5: Deckel der Kontextdokumente (vorher 12, siehe Diagnose)
K_JE_ABFRAGE = 3             # Z12: garantierte Plaetze je Abfrage
K_NAMENSBEZUG = 5            # Z12: garantierte Plaetze fuer Abfragen mit Namensbezug
CACHE_SCHWELLE_S = 10.0      # Antworten unter dieser Dauer stammen aus dem qmd-Cache
TOOL_MAX_TOKENS = 8000
ZUG_A_MAX_TOKENS = 32000     # 08 Abschnitt 2
ZUG_B_MAX_TOKENS = 4000
QMD_WIEDERHOLUNGEN = 2       # Z2: bis zu zwei Wiederholungen, die letzte als Rueckfall (Z13)
QMD_TIMEOUT_S = 900
# Z13: Geraet fuer den Abfragepfad. In der Diagnose vom 06.09.2026 stuerzte CUDA bei 24 von
# 37 Abfragen mit Reranking ab (ggml-cuda.cu:106, Exitcode 0xC0000409), Vulkan bei 0 von 5,
# bei 45 bis 80 s je Abfrage. Der Rueckfall laeuft auf CUDA ohne Reranking (0 von 4 Abstuerze).
QMD_GERAET = os.environ.get("TREIBER_QMD_GPU", "vulkan").strip().lower() or "vulkan"
QMD_RUECKFALL_GERAET = "cuda"
# Typisierte Anfragen (lex:/vec:) umgehen die Anfrageerweiterung (M-3); Vorgabe aus.
QMD_TYPISIERT = os.environ.get("TREIBER_QMD_TYPISIERT", "0").strip().lower() in ("1", "true", "ja")
BEWERTUNGSLOGIK = "Bewertungslogik_Experten-Agent.md"

# Rollenkennung (Kapitel 17) -> Nutzerkennung in permissions.yaml und Persona-Dateien.
ROLLEN_KONFIG: dict[str, dict[str, str]] = {
    "betriebsrat": {
        "nutzer": "betriebsrat",
        "name": "Betriebsrat / Employee Interests",
        "persona": "persona/betriebsrats_persona.md",
        "kalibrierung": "persona/betriebsrats_kriterienkalibrierung.md",
    },
    "cfo": {
        "nutzer": "cfo",
        "name": "CFO / Controlling",
        "persona": "persona/cfo_persona.md",
        "kalibrierung": "persona/cfo_kriterienkalibrierung.md",
    },
    "it": {
        "nutzer": "it-security",
        "name": "IT / Architektur / Cybersecurity",
        "persona": "persona/it_persona.md",
        "kalibrierung": "persona/it_kriterienkalibrierung.md",
    },
    "ceo": {
        "nutzer": "ceo",
        "name": "CEO / Strategie",
        "persona": "persona/ceo_persona.md",
        "kalibrierung": "persona/ceo_kriterienkalibrierung.md",
    },
}


# ---------------------------------------------------------------------------
# Fehlerklassen
# ---------------------------------------------------------------------------


class TreiberFehler(Exception):
    """Vorbedingung verletzt (Modul fehlt, Rolle unbekannt). Kein Laufergebnis."""


class TechnischerFehler(TreiberFehler):
    """Die Rolle liefert keine Zeile; der Orchestrator meldet das und laeuft weiter (Z9)."""

    def __init__(self, art: str, details: Any = None):
        super().__init__(f"{art}: {details}" if details is not None else art)
        self.art = art
        self.details = details


class WissensbasisFehler(TechnischerFehler):
    def __init__(self, details: Any = None):
        super().__init__("wissensbasis_nicht_erreichbar", details)


# ---------------------------------------------------------------------------
# Prompt-Module. Reihenfolge ist Absicht, siehe Architekturdokument 5.1 bis 5.7.
# ---------------------------------------------------------------------------

INITIALTEIL = """Du bist ein Experten-Gutachter in einem Multi-Stakeholder-Bewertungsprozess
fuer Projektportfolio-Entscheidungen der Lahnberg Thermotechnik GmbH & Co. KG.

## Deine Aufgabe

Du bewertest EIN Vorhaben aus GENAU EINER Perspektive, naemlich der weiter unten
beschriebenen Rolle. Du bist nicht der Orchestrator und nicht der Entscheider. Andere
Rollen bewerten dasselbe Vorhaben getrennt; du nimmst ihre Urteile nicht vorweg.

## Das Wissensmanagement, und wie du es bedienst

Dir steht die Wissensbasis des Unternehmens zur Verfuegung. Du erreichst sie ueber das
Werkzeug `wissensbasis_suchen`.

**Was sie enthaelt:** 218 Dokumente der Lahnberg Thermotechnik aus den Jahren 2011 bis
2025 in neun Ablageorten: Projektreviews und Lessons Learned, Protokolle von Steering,
Beirat und Betriebsrat, gelenkte Richtlinien (POL-...), Management Summaries,
Beiratsvorlagen und Investitionsantraege, Mailverkehr, Organigramme, Kennzahlenberichte
und die Unternehmenschronik.

**Was sie nicht enthaelt:** keine Budgetrahmen oder Investitionsplaene kuenftiger Jahre,
keine Energiepreis-, CO2- oder Marktpraemissen, keine Angebote oder Unterlagen Dritter,
nichts nach 2025. Danach zu fragen kostet Abfragen und bringt nichts. Fehlt dir so etwas
fuer die Bewertung, ist es eine Informationsluecke des Antrags.

Verbindliche Regeln fuer die Bedienung:

1. **Du MUSST das Werkzeug benutzen.** Eine Bewertung allein aus dem Projektantrag, aus
   deiner Rollenbeschreibung oder aus Allgemeinwissen ist ungueltig.
2. **Zuerst der erinnerte Fall, mit Namen und Jahr.** Deine Rollenbeschreibung enthaelt
   Erfahrungen aus frueheren Vorhaben. Erinnert dich der Antrag an einen davon, ist das
   die wichtigste Spur: Frage in der ersten Runde nach diesem Fall mit seinem Namen und
   seinem Jahr, und in derselben oder der naechsten Runde nach den Regeln und
   Beschluessen, die aus ihm hervorgegangen sind. Erst danach Richtlinien, Kennzahlen und
   Vergleichsfaelle.
3. **Frage in eigenen Worten, als ganzer Satz**, so wie du sie einem Archivar stellen
   wuerdest, und nenne den Vorgang beim Namen, wenn du ihn kennst. Wiederhole keine
   Frage, die schon beantwortet ist.
4. **Dein Abfragebudget:** hoechstens vier Runden mit je bis zu drei Fragen. Zwei bis
   vier Abfragen mit unterschiedlicher Stossrichtung sind der Normalfall.
5. **„Keine Treffer" ist eine Antwort.** Sie heisst, dass die Wissensbasis das Thema
   nicht traegt. Formuliere die Frage dann nicht um, sondern halte die Luecke als
   Informationsluecke fest.
6. **„Wissensbasis nicht erreichbar" ist ein technischer Ausfall**, keine Aussage ueber
   den Inhalt. Benenne ihn in deiner Bewertung als solchen; was du deshalb nicht pruefen
   konntest, gilt als nicht belegt, nicht als nicht vorhanden.
7. **Was du nicht findest, erfindest du nicht.** Fehlt eine Information, benennst du die
   Luecke ausdruecklich.
8. Du siehst nur, was deine Rolle sehen darf. Bleiben Bereiche verschlossen, ist das
   kein Fehler, sondern gehoert als Informationsluecke in die Bewertung.

## Wie du vorgehst

Zuerst liest du den Projektantrag und bestimmst deinen Informationsbedarf. Dann befragst
du die Wissensbasis nach den Regeln oben, beginnend mit dem erinnerten Fall. Danach
bewertest du nach den unten folgenden Katalogen und gibst das vereinbarte Format aus.
"""

NUTZERANWEISUNG = (
    "Analysiere dieses Vorhaben. Bestimme deinen Informationsbedarf und befrage die "
    "Wissensbasis, bevor du urteilst. Melde dich mit deiner Einschaetzung erst, wenn "
    "du die Wissensbasis befragt hast."
)

ABSCHLUSS_AUFTRAG_A = """## Jetzt bewerten

Oben stehen die Dokumente, die deine eigenen Abfragen an die Wissensbasis geliefert
haben. Erstelle nun deine abschliessende Bewertung als Fliesstext nach Kapitel 12 der
Bewertungslogik.

Zwingend:

1. **Zitiere woertlich** aus den beigefuegten Dokumenten. Deine Begruendung muss den
   Satz enthalten, der deine Einschaetzung traegt, unveraendert.
2. Nenne mindestens einen Betrag oder eine Regelbezugnahme mit Fassung.
3. Wenn dich das Vorhaben an einen frueheren Fall erinnert, benenne ihn und belege ihn
   aus den Dokumenten.
4. Halte die Gliederung aus Kapitel 12 ein: Status, Score (oder KEIN SCORE),
   Begruendung, gegebenenfalls Entscheidungsrelevanter Hinweis, bei INFORMATION FEHLT
   die Liste der fehlenden Informationen und warum sie benoetigt werden.

Kein JSON. Die maschinenlesbare Fassung entsteht in einem zweiten Schritt aus diesem
Text.
"""

KUERZER_ZUSATZ = (
    "\n\nHinweis: Deine vorige Fassung wurde am Tokenlimit abgeschnitten. Fasse dich "
    "deutlich kuerzer; die Zitate und die Gliederung nach Kapitel 12 bleiben Pflicht."
)

ZUG_B_AUFTRAG = """Uebertrage deine Bewertung von oben unveraendert in das vorgegebene Schema.
Kein neues Urteil, keine neue Abwaegung: Status, Score, Begruendung, fehlende
Informationen, Praezedenz und entscheidungsrelevanter Hinweis genau so, wie sie in
deinem Text stehen. Bei INFORMATION FEHLT ist score null. Die Begruendung uebernimmt
den tragenden Satz mit dem woertlichen Zitat und dem Betrag oder Regelbezug."""

TOOLS = [{
    "name": "wissensbasis_suchen",
    "description": (
        "Durchsucht die Wissensbasis des Unternehmens (Projektreviews, Protokolle, "
        "Richtlinien, Management Summaries, Mailverkehr aus den Jahren 2011 bis 2025) "
        "semantisch und liefert die relevantesten Dokumente. Stelle eine Frage in ganzen "
        "Saetzen und nenne den Vorgang beim Namen, wenn du ihn kennst. Antwortet mit "
        "Treffern, mit 'Keine Treffer' (das Thema ist nicht in der Wissensbasis) oder mit "
        "dem Fehler 'Wissensbasis nicht erreichbar' (technischer Ausfall, keine Aussage "
        "ueber den Inhalt)."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "frage": {
                "type": "string",
                "description": "Die Suchfrage in eigenen Worten, als ganzer Satz.",
            }
        },
        "required": ["frage"],
        "additionalProperties": False,
    },
}]


def lade_env() -> None:
    """Liest die .env im Projektwurzelverzeichnis (ANTHROPIC_API_KEY), ohne Zusatzabhaengigkeit;
    vorhandene Umgebungsvariablen gewinnen. Wie in eval/cfo_e2e.py."""
    f = ROOT / ".env"
    if not f.exists():
        return
    for line in f.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", line)
        if m and not line.lstrip().startswith("#"):
            os.environ.setdefault(m.group(1), m.group(2).strip().strip('"').strip("'"))


def lies(rel: str) -> str:
    """Laedt ein Prompt-Modul. Bricht laut ab, wenn es fehlt oder leer ist."""
    f = ROOT / rel
    if not f.exists():
        raise TreiberFehler(f"Prompt-Modul fehlt: {f}")
    text = f.read_text(encoding="utf-8")
    if not text.strip():
        raise TreiberFehler(f"Prompt-Modul ist leer: {f}")
    return text


def rollen_konfig(rolle: str) -> dict[str, str]:
    if rolle not in ROLLEN_KONFIG:
        raise TreiberFehler(f"Unbekannte Rolle {rolle!r}; erlaubt: {', '.join(ROLLEN)}")
    return ROLLEN_KONFIG[rolle]


def baue_system_prompt(rolle: str) -> tuple[str, list[tuple[str, int]]]:
    k = rollen_konfig(rolle)
    module = [
        ("Generischer Initialteil", INITIALTEIL),
        (f"Rollen-Persona ({k['persona']})", lies(k["persona"])),
        (f"Bewertungslogik, generischer Kriterienkatalog ({BEWERTUNGSLOGIK})",
         lies(BEWERTUNGSLOGIK)),
        (f"Rollenspezifische Kalibrierung ({k['kalibrierung']})", lies(k["kalibrierung"])),
    ]
    teile, index = [], []
    for name, text in module:
        teile.append(f"\n\n{'=' * 78}\n# MODUL: {name}\n{'=' * 78}\n\n{text}")
        index.append((name, len(text)))
    return "".join(teile), index


def prompt_version(rolle: str) -> str:
    """NFR-10: Hash ueber Initialteil, Persona, Bewertungslogik und Kalibrierung."""
    k = rollen_konfig(rolle)
    h = hashlib.sha256()
    for text in (INITIALTEIL, lies(k["persona"]), lies(BEWERTUNGSLOGIK), lies(k["kalibrierung"])):
        h.update(text.encode("utf-8"))
        h.update(b"\x00")
    return h.hexdigest()[:12]


def baue_projektobjekt(pfade: list[Path]) -> tuple[str, list[tuple[str, int]]]:
    if not pfade:
        raise TreiberFehler("kein Antrag angegeben")
    teile, index = [], []
    for p in pfade:
        if not p.exists():
            raise TreiberFehler(f"Antragsdatei fehlt: {p}")
        text = p.read_text(encoding="utf-8")
        if not text.strip():
            raise TreiberFehler(f"Antragsdatei ist leer: {p}")
        teile.append(f"\n\n### Projektdatei: {p.name}\n\n{text}")
        index.append((str(p), len(text)))
    n = len(pfade)
    kopf = (f"# Zu bewertendes Vorhaben\n\nDas Projektobjekt besteht aus {n} "
            f"Datei{'en' if n != 1 else ''}.\n")
    return kopf + "".join(teile), index


def system_bloecke(system_prompt: str) -> list[dict]:
    # Z11: der Systemprompt ist ueber alle Zuege identisch, deshalb cache_control.
    return [{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}]


# ---------------------------------------------------------------------------
# Wissensbasis
# ---------------------------------------------------------------------------


def qmd_env(geraet: str | None = None) -> dict:
    """Umgebung fuer qmd-Subprozesse.

    Z13: `QMD_LLAMA_GPU` auf das Abfragegeraet (Vorgabe vulkan, siehe QMD_GERAET); `auto`
    laesst qmd selbst waehlen. Die Index-Konfiguration unter .qmd/ bleibt unberuehrt.
    """
    e = dict(os.environ)
    e["XDG_CACHE_HOME"] = str(QMD_DIR / ".cache")
    e["QMD_CONFIG_DIR"] = str(QMD_DIR / ".qmd")
    g = (geraet if geraet is not None else QMD_GERAET).strip().lower()
    if g in ("", "auto"):
        e.pop("QMD_LLAMA_GPU", None)
    else:
        e["QMD_LLAMA_GPU"] = g
    return e


def qmd_exe() -> Path:
    return QMD_DIR / "node_modules" / ".bin" / ("qmd.cmd" if os.name == "nt" else "qmd")


def qmd_kommando() -> list[str]:
    """Argumentvektor fuer qmd-Abfragen. Unter Windows ist `qmd.cmd` ein Batch-Wrapper, und
    cmd.exe zerlegt ein Argument mit Zeilenumbruch: bei einem lex:/vec:-Anfragedokument
    gingen `--format json` und die Collections verloren. Deshalb node direkt mit der
    qmd.js, wenn beides da ist; sonst der Wrapper."""
    paket = QMD_DIR / "node_modules" / "@tobilu" / "qmd"
    node = shutil.which("node")
    if node:
        for js in (paket / "bin" / "qmd", paket / "dist" / "cli" / "qmd.js"):   # was der Wrapper ruft
            if js.exists():
                return [node, str(js)]
    return [str(qmd_exe())]


_CRASH_MARKER = ("CUDA error", "GGML_ASSERT", "Segmentation fault", "FATAL")
_UNGERANKT_MARKER = ("Reranker unavailable", "skipping reranking")


@dataclass
class AbfrageErgebnis:
    """Antwort der Wissensbasis auf eine Abfrage, mit dem, was das Protokoll braucht."""
    treffer: list[dict]
    ungerankt: bool = False       # Reranker ausgelassen (Meldung von qmd) oder --no-rerank
    geraet: str = ""              # QMD_LLAMA_GPU des Aufrufs
    rerank: bool = True
    typisiert: bool = False       # lex:/vec:-Anfragedokument statt Freitext
    dauer_s: float = 0.0
    stderr_ende: str = ""

    @property
    def aus_cache(self) -> bool:
        """Identischer Wortlaut kommt aus dem qmd-Cache in Sekunden; fuer NFR-03-Laeufe
        ist so eine Antwort kuenstlich stabil und wird deshalb ausgewiesen."""
        return self.dauer_s < CACHE_SCHWELLE_S


def werte_qmd_ausgabe(returncode: int, stdout: str, stderr: str) -> tuple[list[dict], bool]:
    """Z2: Absturz von Nulltreffer unterscheiden.

    Liefert (Treffer, ungerankt) oder wirft WissensbasisFehler. Exitcode ungleich 0
    (unter Windows 0xC0000409 beim Fail-fast von llama.cpp) und `CUDA error` in stderr
    sind Abstuerze; leeres stdout bei Exitcode 0 ist ein echter Nulltreffer.
    """
    err = stderr or ""
    ende = err.strip()[-300:]
    if returncode != 0:
        raise WissensbasisFehler(f"Exitcode {returncode} ({returncode & 0xFFFFFFFF:#x}): {ende}")
    if any(m in err for m in _CRASH_MARKER):
        raise WissensbasisFehler(f"Laufzeitfehler: {ende}")
    ungerankt = any(m in err for m in _UNGERANKT_MARKER)
    raw = (stdout or "").strip()
    start = raw.find("[")
    if start < 0:
        if raw:
            raise WissensbasisFehler(f"keine JSON-Ausgabe: {raw[:200]}")
        return [], ungerankt
    try:
        return json.loads(raw[start:]), ungerankt
    except json.JSONDecodeError as e:
        raise WissensbasisFehler(f"JSON unlesbar: {e}")


_KENNUNG = re.compile(r"\b[A-Z]{2,6}(?:-[A-Z0-9]{1,8}){1,3}\b")     # POL-FIN-002, INV-2024-01, BV-2023-01
_JAHR = re.compile(r"\b(?:19|20)\d{2}\b")
_GROSSWORT = re.compile(r"\b[A-ZÄÖÜ][a-zäöüß]{3,}(?:-[A-ZÄÖÜa-zäöüß]+)?\b")


def typisiertes_dokument(frage: str) -> str:
    """Anfragedokument fuer `qmd query`: `lex:` mit Kennungen, Jahreszahlen und seltenen
    Eigennamen, `vec:` mit dem ganzen Satz. qmd ueberspringt dann die Anfrageerweiterung
    durch das 1,7-B-Modell (07_qmd_maengel M-3: entstelltes Deutsch). Jede Zeile einzeilig
    und ohne Anfuehrungszeichen, wie qmd es verlangt (parseStructuredQuery in dist/cli/qmd.js)."""
    satz = " ".join(frage.replace('"', " ").replace("'", " ").split())
    lex: list[str] = []
    for m in _KENNUNG.findall(satz) + _JAHR.findall(satz):
        if m not in lex:
            lex.append(m)
    for w in _GROSSWORT.findall(satz):
        if len(lex) >= 10:
            break
        if seltene_terme(w) and w not in lex:
            lex.append(w)
    zeilen = []
    if lex:
        zeilen.append("lex: " + " ".join(lex))
    zeilen.append("vec: " + satz)
    return "\n".join(zeilen)


def qmd_query_subprocess(frage: str, collections: list[str], n: int = TREFFER_JE_ABFRAGE, *,
                         geraet: str | None = None, rerank: bool = True,
                         typisiert: bool | None = None) -> AbfrageErgebnis:
    """Eine RAG-Abfrage ueber den qmd-Subprozess.

    Z2: Exitcode und stderr werden ausgewertet (werte_qmd_ausgabe), ein Absturz ist ein
    WissensbasisFehler und wird nicht zu "Keine Treffer". Z13: `geraet` waehlt den
    GPU-Pfad, `rerank=False` haengt `--no-rerank` an. `typisiert` schaltet das
    lex:/vec:-Anfragedokument (Vorgabe QMD_TYPISIERT).
    """
    if not collections:
        raise ValueError("qmd_query ohne Collections aufgerufen")
    exe = qmd_exe()
    if not exe.exists():
        raise WissensbasisFehler(f"qmd fehlt: {exe}")
    typ = QMD_TYPISIERT if typisiert is None else bool(typisiert)
    anfrage = typisiertes_dokument(frage) if typ else frage
    cmd = [*qmd_kommando(), "query", anfrage, "-n", str(n), "--format", "json"]
    if not rerank:
        cmd.append("--no-rerank")
    for c in collections:
        cmd += ["-c", c]
    g = (geraet if geraet is not None else QMD_GERAET)
    t = time.time()
    try:
        r = subprocess.run(cmd, cwd=QMD_DIR, env=qmd_env(g), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=QMD_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        raise WissensbasisFehler(f"Zeitlimit {QMD_TIMEOUT_S}s ueberschritten")
    dauer = round(time.time() - t, 1)
    treffer, ungerankt = werte_qmd_ausgabe(r.returncode, r.stdout or "", r.stderr or "")
    return AbfrageErgebnis(treffer=treffer, ungerankt=ungerankt or not rerank, geraet=g,
                           rerank=rerank, typisiert=typ, dauer_s=dauer,
                           stderr_ende=(r.stderr or "").strip()[-200:])


def rel_aus_uri(uri: str) -> str:
    """qmd://intern/mailarchiv/... -> mailarchiv/... (Pfad wie in corpus/)."""
    p = uri.replace("qmd://", "")
    return p.split("/", 1)[1] if "/" in p else p


def volltext(rel: str) -> str:
    f = CORPUS_DIR / rel
    return f.read_text(encoding="utf-8", errors="replace") if f.exists() else ""


def _als_ergebnis(x: Any) -> AbfrageErgebnis:
    """Eine Wissensbasis-Funktion darf auch eine blosse Trefferliste liefern (Tests)."""
    return x if isinstance(x, AbfrageErgebnis) else AbfrageErgebnis(treffer=list(x or []))


def abfrage_mit_wiederholung(fn: Callable, frage: str, collections: list[str], n: int,
                             wiederholungen: int = QMD_WIEDERHOLUNGEN,
                             **optionen: Any) -> tuple[AbfrageErgebnis, int, bool]:
    """Z2 und Z13: Versuch 1 bis `wiederholungen` auf dem Abfragegeraet mit Reranking; der
    letzte Versuch ist der Rueckfall auf QMD_RUECKFALL_GERAET ohne Reranking. Danach
    WissensbasisFehler. Liefert (Ergebnis, Versuchsnummer, rueckfall).

    Bei rund zwei Dritteln Absturzquote auf CUDA (Diagnose vom 06.09.2026) genuegen drei
    Versuche fuer rund 95 Prozent; mit Vulkan als Vorgabe ist der Rueckfall die Ausnahme.
    """
    letzter: Exception | None = None
    versuche = wiederholungen + 1
    for versuch in range(1, versuche + 1):
        rueckfall = versuch == versuche and versuche > 1
        try:
            if rueckfall:
                erg = _als_ergebnis(fn(frage, collections, n, geraet=QMD_RUECKFALL_GERAET,
                                       rerank=False, **optionen))
                erg.ungerankt, erg.rerank = True, False
                erg.geraet = erg.geraet or QMD_RUECKFALL_GERAET
            else:
                erg = _als_ergebnis(fn(frage, collections, n, **optionen))
            return erg, versuch, rueckfall
        except WissensbasisFehler as e:
            letzter = e
            if versuch < versuche:
                time.sleep(0.2 * versuch)
    raise WissensbasisFehler(f"nach {versuche} Versuchen: {letzter}")


# ---------------------------------------------------------------------------
# Kontextauswahl: Z12 (Auswahl je Abfrage, Namensbezug bevorzugt) mit Deckel aus Z5
# ---------------------------------------------------------------------------

_UMLAUTE = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "Ä": "ae", "Ö": "oe", "Ü": "ue"})
_WORT = re.compile(r"[a-z]{5,}")

# Woerter, die in fast jeder Abfrage und in vielen Pfaden vorkommen und deshalb keinen
# Namensbezug tragen.
STOPP = {
    "projekt", "projekte", "projekts", "vorhaben", "unternehmen", "unternehmens", "welche",
    "welches", "welcher", "wurde", "wurden", "worden", "haben", "hatte", "hatten", "werden",
    "einem", "einer", "eines", "ihrer", "ihren", "dieser", "dieses", "diesem", "durch",
    "ueber", "unter", "gegen", "zwischen", "sowie", "nicht", "keine", "kosten", "nutzen",
    "risiko", "risiken", "angaben", "deren", "dessen", "wenn", "dass", "damit", "dabei",
    "davon", "dafuer", "wofuer", "warum", "weshalb", "woher", "wohin", "frueher", "heute",
    "aktuell", "jahre", "jahren", "prozent", "anteil", "richtlinie", "richtlinien", "vorgaben",
    "regeln", "gelten", "geltend", "konzern", "standort", "standorte", "erfahrungen",
    "erfahrung", "ergebnis", "ergebnisse", "vorlage", "vorlagen", "antrag", "antraege",
    "investition", "investitionen", "business", "wissensbasis", "dokument", "dokumente",
    "informationen", "information", "geschaeftsfuehrung", "geschaeftsjahr", "gibt",
    "wurde", "wieder", "immer", "bereits", "danach", "bevor", "nachdem", "seitdem",
    "beispiel", "insbesondere", "hinsichtlich", "bezueglich", "gemaess", "aufgrund",
    "innerhalb", "ausserhalb", "waehrend", "sollen", "sollte", "sollten", "koennen",
    "konnte", "konnten", "muessen", "musste", "mussten", "duerfen", "gehoert", "gehoeren",
    "bewertung", "bewertet", "bewerten", "entscheidung", "entscheidungen", "massnahme",
    "massnahmen", "projektantrag", "projektvorschlag", "ablage", "ablageort", "sharepoint",
    "protokoll", "protokolle", "summary", "management", "systeme", "system",
}


def normalisiere(text: str) -> str:
    return text.translate(_UMLAUTE).lower()


def seltene_terme(frage: str) -> set[str]:
    """Woerter ab fuenf Buchstaben, die nicht generisch sind: Eigennamen, Vorgaenge,
    Kennungen wie 'glaswerk', 'giesserei', 'outsourcing'."""
    return {w for w in _WORT.findall(normalisiere(frage)) if w not in STOPP}


_PFAD_TOKEN = re.compile(r"[a-z]+")
PRAEFIX_AB = 8  # ab dieser Laenge zaehlt ein Term auch als Praefix eines Pfadworts (giesserei-investition)


def pfad_traegt_term(rel: str, terme: set[str]) -> bool:
    """Ein Term aus der Frage ist ein ganzes Wort des Pfads, oder Praefix eines Pfadworts ab
    PRAEFIX_AB Buchstaben. Teilwortsuche ("budget" in "programmbudget", "fertigung" in
    "fertigungstechnik") machte im T5-Lauf sechs von neun Abfragen zu Namensbezuegen."""
    tokens = set(_PFAD_TOKEN.findall(normalisiere(rel)))
    for term in terme:
        if term in tokens:
            return True
        if len(term) >= PRAEFIX_AB and any(t.startswith(term) for t in tokens):
            return True
    return False


def hat_namensbezug(rel: str, fragen: list[str]) -> bool:
    """Der Pfad des Dokuments traegt ein seltenes Wort aus einer der Fragen."""
    terme = set().union(*(seltene_terme(f) for f in fragen)) if fragen else set()
    return pfad_traegt_term(rel, terme)


def abfrage_hat_namensbezug(frage: str, treffer: list[str]) -> bool:
    """Die Abfrage nennt einen Vorgang beim Namen, und mindestens ein Treffer ist unter
    diesem Namen abgelegt: der Agent hat den in seiner Persona erinnerten Fall gefunden."""
    terme = seltene_terme(frage)
    return any(pfad_traegt_term(rel, terme) for rel in treffer)


def waehle_kontext(abfragen: list[dict], deckel: int = KONTEXT_DECKEL,
                   k: int = K_JE_ABFRAGE, k_namen: int = K_NAMENSBEZUG) -> list[str]:
    """Reihenfolge der Kontextdokumente = document_index in der Antwort.

    Z12, Auswahl je Abfrage statt global: qmd normiert die Scores je Abfrage, der beste
    Treffer jeder Abfrage bekommt 1,0, der zweite rund 0,62, unabhaengig von der Relevanz.
    Eine abfrageuebergreifende Sortierung nach Score ist deshalb bedeutungslos; im Lauf vom
    06.09.2026 05:12 verdraengten die Rang-2-Treffer beliebiger Abfragen alle vier
    gefundenen Golden-Dokumente (Diagnose: Golden auf den globalen Raengen 3, 9, 14, 25).

    Verfahren, in dieser Reihenfolge, Duplikate zusammengefuehrt, Abbruch am Deckel (Z5):
      1. Rang 1 jeder Abfrage, chronologisch: der beste Treffer keiner Frage geht verloren.
      2. Abfragen mit Namensbezug (der Agent nannte den erinnerten Fall, und ein Treffer
         ist unter diesem Namen abgelegt): Raenge 2 bis `k_namen`.
      3. Alle Abfragen in chronologischer Reihenfolge: Raenge 2 bis `k`.
      4. Reihum ueber die uebrigen Raenge aller Abfragen, bis der Deckel voll ist.

    Warum Rang 1 zuerst (Fassung 2, nach dem T5-Lauf t5-stammdaten-1): dort galten sechs
    von neun CFO-Abfragen als Namensbezug, ihre Raenge 1 bis 5 fuellten den Deckel 16, und
    drei Abfragen mit Golden-Dokumenten auf Rang 1 und 2 kamen nie an die Reihe.

    `abfragen`: [{"frage": str, "treffer": [rel, ...]}] je Abfrage in Rangfolge von qmd,
    chronologisch. Abfragen ohne Treffer tragen nichts bei.
    """
    ranglisten = [list(dict.fromkeys(a.get("treffer") or [])) for a in abfragen]
    benannt = [abfrage_hat_namensbezug(a.get("frage", ""), r) for a, r in zip(abfragen, ranglisten)]
    auswahl: list[str] = []
    gesehen: set[str] = set()

    def nimm(rel: str) -> None:
        if rel not in gesehen and len(auswahl) < deckel:
            gesehen.add(rel)
            auswahl.append(rel)

    for r in ranglisten:                             # 1. Rang 1 jeder Abfrage
        if r:
            nimm(r[0])
    for r, b in zip(ranglisten, benannt):            # 2. Namensbezug: Raenge 2..k_namen
        if b:
            for rel in r[1:k_namen]:
                nimm(rel)
    for r in ranglisten:                             # 3. garantierte Plaetze je Abfrage
        for rel in r[1:k]:
            nimm(rel)
    laengste = max((len(r) for r in ranglisten), default=0)
    for rang in range(k, laengste):                  # 4. reihum auffuellen
        for r in ranglisten:
            if rang < len(r):
                nimm(r[rang])
    return auswahl


def kontext_herkunft(abfragen: list[dict], auswahl: list[str]) -> dict[str, dict]:
    """Je gewaehltem Dokument: erste Abfrage (Index) und Rang dort, fuers Protokoll."""
    out: dict[str, dict] = {}
    for i, a in enumerate(abfragen):
        for rang, rel in enumerate(a.get("treffer") or [], start=1):
            if rel in auswahl and rel not in out:
                out[rel] = {"abfrage": i, "rang": rang}
    return out


# ---------------------------------------------------------------------------
# API-Zuege
# ---------------------------------------------------------------------------


def _stream(client, **kw):
    """Streaming ist bei grossem max_tokens Pflicht; get_final_message liefert das Ganze."""
    with client.messages.stream(**kw) as s:
        return s.get_final_message()


def _stop_details(resp) -> Optional[dict]:
    sd = getattr(resp, "stop_details", None)
    if sd is None:
        return None
    return {
        "type": getattr(sd, "type", None),
        "category": getattr(sd, "category", None),
        "explanation": getattr(sd, "explanation", None),
    }


_USAGE_FELDER = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")


def _usage(resp) -> dict:
    """Tokenverbrauch einer API-Antwort (`Message.usage`, anthropic 1.4: input_tokens,
    output_tokens, cache_creation_input_tokens, cache_read_input_tokens). Fehlende oder
    leere Felder zaehlen 0, damit Fake-Clients und aeltere SDKs nicht brechen."""
    u = getattr(resp, "usage", None)
    return {k: int(getattr(u, k, 0) or 0) for k in _USAGE_FELDER}


def _erfasse_usage(protokoll: dict, zug: str, resp) -> None:
    """Je API-Aufruf ein Eintrag unter `api_aufrufe`, Summe je Rolle unter `tokens`."""
    u = _usage(resp)
    protokoll.setdefault("api_aufrufe", []).append({"zug": zug, **u})
    t = protokoll.setdefault("tokens", {**{k: 0 for k in _USAGE_FELDER}, "aufrufe": 0})
    for k in _USAGE_FELDER:
        t[k] += u[k]
    t["aufrufe"] += 1


def _pruefe_refusal(resp, wo: str) -> None:
    if getattr(resp, "stop_reason", None) == "refusal":
        raise TechnischerFehler("refusal", {"zug": wo, "stop_details": _stop_details(resp)})


def _textbloecke(resp) -> list:
    return [b for b in getattr(resp, "content", []) if getattr(b, "type", None) == "text"]


def _essay_text(resp) -> str:
    return "".join(getattr(b, "text", "") for b in _textbloecke(resp))


def _zitate(resp, doc_reihenfolge: list[str]) -> list[dict]:
    out = []
    for b in _textbloecke(resp):
        for z in (getattr(b, "citations", None) or []):
            idx = getattr(z, "document_index", None)
            if idx is None or not 0 <= idx < len(doc_reihenfolge):
                continue
            out.append({
                "datei": doc_reihenfolge[idx],
                "document_index": idx,
                "cited_text": getattr(z, "cited_text", "") or "",
                "start_char_index": getattr(z, "start_char_index", None),
                "end_char_index": getattr(z, "end_char_index", None),
            })
    return out


_SCORE_IM_TEXT = re.compile(r"score\W{0,6}(\d{1,2})\s*/\s*10", re.I)
_KEIN_SCORE_IM_TEXT = re.compile(r"kein\s+score", re.I)


def score_im_essay(essay: str) -> Optional[int] | str:
    """Konsistenzpruefung ohne Urteil (08 Abschnitt 2): was der Fliesstext als Score nennt."""
    m = _SCORE_IM_TEXT.search(essay)
    if m:
        return int(m.group(1))
    if _KEIN_SCORE_IM_TEXT.search(essay):
        return "KEIN SCORE"
    return None


# ---------------------------------------------------------------------------
# Lauf einer Rolle
# ---------------------------------------------------------------------------


@dataclass
class RollenErgebnis:
    rolle: str
    zeile: Optional[Zeile]
    protokoll: dict
    fehler: Optional[str] = None
    dateien: dict = field(default_factory=dict)


def _jetzt() -> str:
    return datetime.now(timezone.utc).isoformat()


def _schreibe_protokoll(lauf_dir: Path, rolle: str, protokoll: dict) -> Path:
    lauf_dir.mkdir(parents=True, exist_ok=True)
    f = lauf_dir / f"{rolle}.protokoll.json"
    f.write_text(json.dumps(protokoll, ensure_ascii=False, indent=2), encoding="utf-8")
    return f


def fuehre_rolle_aus(
    rolle: str,
    antrag_pfade: list[Path],
    lauf_dir: Path,
    lauf_id: str,
    client=None,
    qmd_query: Callable | None = None,
    modell: str = MODELL,
    deckel: int = KONTEXT_DECKEL,
    max_runden: int = MAX_TOOL_RUNDEN,
    n_treffer: int = TREFFER_JE_ABFRAGE,
    typisiert: bool | None = None,
) -> RollenErgebnis:
    """Eine Rolle vollstaendig: Werkzeugrunden, Zug A, Zug B, Zeile, Protokoll.

    Liefert immer ein RollenErgebnis. Ein technischer Fehler steht darin und im
    Protokoll; er wirft nicht, damit der Orchestrator weiterlaufen kann (Z9).
    `typisiert` schaltet lex:/vec:-Anfragen (None = Vorgabe aus TREIBER_QMD_TYPISIERT).
    """
    t0 = time.time()
    typ = QMD_TYPISIERT if typisiert is None else bool(typisiert)
    protokoll: dict[str, Any] = {
        "rolle": rolle, "lauf_id": lauf_id, "modell": modell, "zeitpunkt": _jetzt(),
        "antrag": [str(p) for p in antrag_pfade], "prompt_version": None, "collections": None,
        "qmd": {"geraet": QMD_GERAET, "rueckfall_geraet": QMD_RUECKFALL_GERAET, "typisiert": typ,
                "treffer_je_abfrage": n_treffer, "deckel": deckel, "k_je_abfrage": K_JE_ABFRAGE,
                "k_namensbezug": K_NAMENSBEZUG, "cache_schwelle_s": CACHE_SCHWELLE_S},
        "rag_abfragen": [], "dokumente_im_kontext": [], "zitate": [], "stop_reasons": {},
        "zeiten_s": {}, "score_im_essay": None, "score_abweichung": None,
        "technischer_fehler": None, "essay": None, "zug_b_felder": None,
        "api_aufrufe": [], "tokens": {**{k: 0 for k in _USAGE_FELDER}, "aufrufe": 0},
    }
    qmd_fn = qmd_query or qmd_query_subprocess
    optionen: dict[str, Any] = {} if typisiert is None else {"typisiert": typ}

    try:
        k = rollen_konfig(rolle)
        try:
            collections = collections_for_role(k["nutzer"])
        except RollenFehler as e:
            raise TechnischerFehler("rolle_ohne_index_zugriff", str(e))
        protokoll["collections"] = collections
        system_prompt, modulindex = baue_system_prompt(rolle)
        protokoll["prompt_module"] = [{"name": n, "zeichen": c} for n, c in modulindex]
        protokoll["prompt_version"] = prompt_version(rolle)
        projekt, _ = baue_projektobjekt(antrag_pfade)
        system = system_bloecke(system_prompt)

        if client is None:
            from anthropic import Anthropic
            client = Anthropic()

        # ---- Werkzeugrunden ------------------------------------------------
        messages: list[dict] = [{"role": "user", "content": projekt + "\n\n" + NUTZERANWEISUNG}]
        gefunden: dict[str, dict] = {}          # rel -> bester Score, Fragen, Ausschnitt
        abfragen_kontext: list[dict] = []       # je erfolgreicher Abfrage die Rangliste (Z12)
        t = time.time()
        for runde in range(1, max_runden + 1):
            resp = _stream(client, model=modell, max_tokens=TOOL_MAX_TOKENS, system=system,
                           messages=messages, tools=TOOLS)
            protokoll["stop_reasons"][f"runde_{runde}"] = getattr(resp, "stop_reason", None)
            _erfasse_usage(protokoll, f"runde_{runde}", resp)
            _pruefe_refusal(resp, f"runde_{runde}")
            calls = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]
            messages.append({"role": "assistant", "content": resp.content})
            if not calls:
                break
            results = []
            for c in calls:
                frage = (getattr(c, "input", None) or {}).get("frage", "")
                eintrag: dict[str, Any] = {
                    "runde": runde, "frage": frage, "treffer": [], "versuche": 0, "rueckfall": False,
                    "geraet": None, "rerank": None, "ungerankt": None, "typisiert": typ,
                    "dauer_s": None, "aus_cache": None, "fehler": None,
                }
                try:
                    erg, versuche, rueckfall = abfrage_mit_wiederholung(
                        qmd_fn, frage, collections, n_treffer, **optionen)
                except WissensbasisFehler as e:
                    eintrag["fehler"] = str(e)
                    eintrag["versuche"] = QMD_WIEDERHOLUNGEN + 1
                    protokoll["rag_abfragen"].append(eintrag)
                    results.append({"type": "tool_result", "tool_use_id": c.id, "is_error": True,
                                    "content": "Wissensbasis nicht erreichbar"})
                    continue
                eintrag.update({
                    "versuche": versuche, "rueckfall": rueckfall, "geraet": erg.geraet or None,
                    "rerank": erg.rerank, "ungerankt": erg.ungerankt, "typisiert": erg.typisiert or typ,
                    "dauer_s": erg.dauer_s, "aus_cache": erg.aus_cache,
                })
                if erg.stderr_ende and (rueckfall or erg.ungerankt):
                    eintrag["stderr"] = erg.stderr_ende
                zeilen = []
                rangliste: list[str] = []
                for tr in erg.treffer:
                    rel = rel_aus_uri(tr.get("file", ""))
                    if not rel:
                        continue
                    info = gefunden.setdefault(rel, {"score": 0.0, "fragen": [], "snippet": ""})
                    sc = float(tr.get("score") or 0.0)
                    if sc > info["score"]:
                        info["score"] = sc
                        info["snippet"] = (tr.get("snippet") or "")[:300]
                    info["fragen"].append(frage)
                    eintrag["treffer"].append({"datei": rel, "score": sc})
                    rangliste.append(rel)
                    zeilen.append(f"- {rel}\n  {(tr.get('snippet') or '')[:300]}")
                if rangliste:
                    abfragen_kontext.append({"frage": frage, "treffer": rangliste})
                protokoll["rag_abfragen"].append(eintrag)
                results.append({"type": "tool_result", "tool_use_id": c.id,
                                "content": ("Treffer:\n" + "\n".join(zeilen)) if zeilen else "Keine Treffer."})
            messages.append({"role": "user", "content": results})
        protokoll["zeiten_s"]["werkzeugrunden"] = round(time.time() - t, 1)
        protokoll["abfragen_aus_cache"] = sum(1 for a in protokoll["rag_abfragen"] if a.get("aus_cache"))

        # Z3: ohne eine erfolgreiche Abfrage mit Treffern ist die Bewertung ungueltig.
        if not any(a["treffer"] for a in protokoll["rag_abfragen"]):
            if not protokoll["rag_abfragen"]:
                raise TechnischerFehler("keine_abfrage", "Der Agent hat die Wissensbasis nie befragt (FR-04)")
            raise TechnischerFehler("keine_treffer",
                                    "Keine Abfrage lieferte Treffer; Wissensbasis nicht erreichbar oder leer (Z3)")

        # ---- Kontext: Z12 (je Abfrage) mit Deckel aus Z5 -----------------------
        doc_reihenfolge = waehle_kontext(abfragen_kontext, deckel)
        herkunft = kontext_herkunft(abfragen_kontext, doc_reihenfolge)
        protokoll["dokumente_im_kontext"] = [
            {"datei": rel, "score": gefunden[rel]["score"],
             "namensbezug": hat_namensbezug(rel, gefunden[rel]["fragen"]),
             "abfrage": herkunft.get(rel, {}).get("abfrage"),
             "rang": herkunft.get(rel, {}).get("rang")}
            for rel in doc_reihenfolge
        ]
        inhalt: list[dict] = []
        for rel in doc_reihenfolge:
            inhalt.append({
                "type": "document",
                "source": {"type": "text", "media_type": "text/plain", "data": volltext(rel)},
                "title": Path(rel).stem,
                "context": f"Aus der Wissensbasis. Quelle: corpus/{rel}",
                "citations": {"enabled": True},
            })

        # ---- Zug A: Essay mit Zitaten --------------------------------------
        t = time.time()
        essay_resp = None
        for versuch, auftrag in enumerate((ABSCHLUSS_AUFTRAG_A, ABSCHLUSS_AUFTRAG_A + KUERZER_ZUSATZ), 1):
            msgs_a = messages + [{"role": "user", "content": inhalt + [{"type": "text", "text": auftrag}]}]
            resp = _stream(client, model=modell, max_tokens=ZUG_A_MAX_TOKENS, system=system,
                           messages=msgs_a)
            protokoll["stop_reasons"][f"zug_a_{versuch}"] = getattr(resp, "stop_reason", None)
            _erfasse_usage(protokoll, f"zug_a_{versuch}", resp)
            _pruefe_refusal(resp, f"zug_a_{versuch}")
            if getattr(resp, "stop_reason", None) == "max_tokens":
                continue  # Z4: genau eine Wiederholung mit dem Zusatz "kuerzer"
            essay_resp = resp
            break
        if essay_resp is None:
            raise TechnischerFehler("max_tokens", "Zug A zweimal am Tokenlimit abgeschnitten (Z4)")
        protokoll["zeiten_s"]["zug_a"] = round(time.time() - t, 1)
        essay = _essay_text(essay_resp)
        zitate = _zitate(essay_resp, doc_reihenfolge)
        protokoll["essay"] = essay
        protokoll["zitate"] = zitate
        protokoll["score_im_essay"] = score_im_essay(essay)

        # ---- Zug B: Felder per Structured Output ----------------------------
        t = time.time()
        msgs_b = [
            {"role": "user", "content": projekt + "\n\nErstelle deine Bewertung."},
            {"role": "assistant", "content": essay if essay.strip() else "(leer)"},
            {"role": "user", "content": ZUG_B_AUFTRAG},
        ]
        resp_b = client.messages.parse(model=modell, max_tokens=ZUG_B_MAX_TOKENS, system=system,
                                       messages=msgs_b, output_format=Bewertungsfelder)
        protokoll["stop_reasons"]["zug_b"] = getattr(resp_b, "stop_reason", None)
        _erfasse_usage(protokoll, "zug_b", resp_b)
        _pruefe_refusal(resp_b, "zug_b")
        felder = getattr(resp_b, "parsed_output", None)
        if felder is None:
            raise TechnischerFehler("structured_output",
                                    f"Zug B ohne parsed_output, stop_reason {getattr(resp_b, 'stop_reason', None)}")
        protokoll["zeiten_s"]["zug_b"] = round(time.time() - t, 1)
        protokoll["zug_b_felder"] = felder.model_dump()

        # ---- Zeile nach Kapitel 17 (AE-04) ------------------------------------
        quellen = sorted({f"corpus/{z['datei']}" for z in zitate})
        try:
            zeile = Zeile.aus_feldern(rolle, felder, quellen)
        except ValidationError as e:
            raise TechnischerFehler("17.5", "; ".join(err["msg"] for err in e.errors()))
        s_essay = protokoll["score_im_essay"]
        if s_essay is not None:
            feld = zeile.score if zeile.status == "BEWERTET" else "KEIN SCORE"
            if s_essay != feld:
                protokoll["score_abweichung"] = {"essay": s_essay, "feld": feld,
                                                 "regel": "das Feld gilt (Kapitel 17)"}

        lauf_dir.mkdir(parents=True, exist_ok=True)
        jsonl = lauf_dir / f"{rolle}.jsonl"
        jsonl.write_text(zeile.als_jsonl() + "\n", encoding="utf-8")
        protokoll["zeiten_s"]["gesamt"] = round(time.time() - t0, 1)
        prot = _schreibe_protokoll(lauf_dir, rolle, protokoll)
        return RollenErgebnis(rolle=rolle, zeile=zeile, protokoll=protokoll,
                              dateien={"jsonl": str(jsonl), "protokoll": str(prot)})

    except TechnischerFehler as e:
        protokoll["technischer_fehler"] = {"art": e.art, "details": e.details}
    except TreiberFehler as e:
        protokoll["technischer_fehler"] = {"art": "vorbedingung", "details": str(e)}
    except Exception as e:  # noqa: BLE001 - Z9: nie still abbrechen
        protokoll["technischer_fehler"] = {"art": type(e).__name__, "details": str(e),
                                           "traceback": traceback.format_exc()[-2000:]}
    protokoll["zeiten_s"]["gesamt"] = round(time.time() - t0, 1)
    prot = _schreibe_protokoll(lauf_dir, rolle, protokoll)
    tf = protokoll["technischer_fehler"]
    return RollenErgebnis(rolle=rolle, zeile=None, protokoll=protokoll,
                          fehler=f"{tf['art']}: {tf['details']}", dateien={"protokoll": str(prot)})


def trockenlauf(rolle: str, antrag_pfade: list[Path]) -> dict:
    """T3: Module, Collections und Antrag laden, ohne qmd und ohne API."""
    k = rollen_konfig(rolle)
    collections = collections_for_role(k["nutzer"])
    system_prompt, modulindex = baue_system_prompt(rolle)
    projekt, projektindex = baue_projektobjekt(antrag_pfade)
    return {
        "rolle": rolle, "nutzer": k["nutzer"], "collections": collections,
        "module": [{"name": n, "zeichen": c} for n, c in modulindex],
        "system_prompt_zeichen": len(system_prompt),
        "antrag": [{"datei": d, "zeichen": c} for d, c in projektindex],
        "projekt_zeichen": len(projekt),
        "prompt_version": prompt_version(rolle),
        "modell": MODELL,
        "qmd": {"geraet": QMD_GERAET, "rueckfall_geraet": QMD_RUECKFALL_GERAET,
                "typisiert": QMD_TYPISIERT, "treffer_je_abfrage": TREFFER_JE_ABFRAGE,
                "deckel": KONTEXT_DECKEL, "k_je_abfrage": K_JE_ABFRAGE, "k_namensbezug": K_NAMENSBEZUG,
                "auswahl": "z12-fassung-2-rang1-zuerst"},
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Eine Rolle bewertet einen Antrag ueber die Wissensbasis.")
    ap.add_argument("--rolle", required=True, choices=ROLLEN)
    ap.add_argument("--antrag", action="append", required=True, help="Antragsdatei, mehrfach erlaubt")
    ap.add_argument("--lauf", default=None, help="Lauf-Kennung; Vorgabe: Zeitstempel")
    ap.add_argument("--modell", default=MODELL)
    ap.add_argument("--typisiert", action="store_true",
                    help="Agentenfragen als lex:/vec:-Anfragedokument an qmd (ohne Anfrageerweiterung)")
    ap.add_argument("--dry-run", action="store_true", help="nur Prompt bauen, keine API, kein qmd")
    args = ap.parse_args(argv)

    lade_env()
    pfade = [Path(a).resolve() for a in args.antrag]
    if args.dry_run:
        d = trockenlauf(args.rolle, pfade)
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0

    lauf_id = args.lauf or datetime.now().strftime("%Y%m%d-%H%M%S")
    lauf_dir = LAEUFE_DIR / lauf_id
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("FEHLER: ANTHROPIC_API_KEY fehlt.", file=sys.stderr)
        return 2
    erg = fuehre_rolle_aus(args.rolle, pfade, lauf_dir, lauf_id, modell=args.modell,
                           typisiert=True if args.typisiert else None)
    if erg.fehler:
        print(f"{args.rolle}: technischer Fehler: {erg.fehler}", file=sys.stderr)
        print(f"Protokoll: {erg.dateien.get('protokoll')}")
        return 1
    print(erg.zeile.als_jsonl())
    print(f"Zeile: {erg.dateien['jsonl']}\nProtokoll: {erg.dateien['protokoll']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
