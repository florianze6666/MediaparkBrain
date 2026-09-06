"""Einbettung, Vektorsuche, Pfad-Dedup (Plan 09, Abschnitt 4.2 und 11).

Kein Unterprozess je Abfrage, kein Reranking (AE-05), keine Anfrageerweiterung.
Die Bruecke haelt das Einbettungsmodell im Speicher; die Aehnlichkeit rechnet
numpy gegen die Vektoren aus index.sqlite.

Zwei Nutzer, daher zwei Auflagen. Das Modul haengt ausschliesslich von numpy und
der Standardbibliothek ab, damit es sowohl der Agentenpfad als auch die
Wiki-Anwendung einbinden kann. Und die Bruecke laeuft im Wiki in einem Webserver
mit gleichzeitigen Anfragen: `Bruecke.embed` ist deshalb durch eine Sperre
geschuetzt, Aufrufer kuemmern sich nicht darum.

Kennt nicht: Prompts, Rollenlogik.

**Befund zum Speicherformat, geprueft am 06.09.2026.** Die Vektoren liegen in
`vectors_vec_vector_chunks00` als ein Blob von 1024 Plaetzen zu 2048 float32,
also genau 8.388.608 Byte. Welche Plaetze belegt sind, sagt die Bitmaske
`vectors_vec_chunks.validity`; die Zuordnung Platz zu Dokument laeuft ueber
`vectors_vec_rowids.id`, das die Form `<hash>_<seq>` hat.

**Wichtige Abweichung von der Planannahme:** die gespeicherten Vektoren sind
**nicht** L2-normiert, ihre Normen liegen zwischen 41 und 111. `cosine` ist
deshalb nicht das rohe Skalarprodukt. `lade_index_vektoren` normiert einmal beim
Laden, danach gilt die Annahme und `suche_vektoriell` rechnet mit dem
Skalarprodukt.
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import threading
from pathlib import Path
from typing import Any

import numpy as np

AGENTEN_DIR = Path(__file__).resolve().parent
QMD_DIR = AGENTEN_DIR.parent
ROOT = QMD_DIR.parent
CORPUS_DIR = ROOT / "corpus"
ANTRAEGE_DIR = ROOT / "project_proposals"
INDEX_SQLITE = QMD_DIR / ".qmd" / "index.sqlite"
BRUECKE_SKRIPT = AGENTEN_DIR / "bruecke.mjs"
PERSONA_DIR = ROOT / "persona"

# Vulkan, nicht CUDA: Z13 aus Plan 08, gestuetzt auf .test/1b_diagnose.md.
GERAET = "vulkan"

# Jede Protokollzeile der Bruecke traegt dieses Kennzeichen. Alles andere ist
# Rauschen der Modellbibliothek und wird verworfen.
KENNZEICHEN = "@@QMDBR@@"

DIMENSIONEN = 2048
BRUECKE_START_TIMEOUT_S = 300.0   # erstes Laden des Modells, rund 4,4 s auf GPU
BRUECKE_ANTWORT_TIMEOUT_S = 120.0


class SucheFehler(RuntimeError):
    """Die Wissensbasis ist nicht erreichbar oder antwortet nicht verwertbar."""


# ---------------------------------------------------------------------------
# Bruecke
# ---------------------------------------------------------------------------


def modell_aus_index(index: Path | None = None) -> str:
    """Die Modellkennung, mit der die gespeicherten Vektoren erzeugt wurden.

    Quelle ist `content_vectors.model` im Index, nicht `.qmd/index.yml` und nicht
    die Vorgabe von qmd. Das ist die einzige Angabe, die garantiert zu den
    Vektoren passt: waehlt die Bruecke ein anderes Modell, liegen Anfrage und
    Index in verschiedenen Raeumen und die Aehnlichkeit ist wertlos. Genau das
    ist beim ersten Versuch passiert, qmd fiel ohne `QMD_EMBED_MODEL` auf
    embeddinggemma mit 768 Dimensionen zurueck.
    """
    pfad = index or INDEX_SQLITE
    if not pfad.exists():
        raise SucheFehler(f"Index fehlt: {pfad}")
    verbindung = sqlite3.connect(f"file:{pfad}?mode=ro", uri=True)
    try:
        modelle = [r[0] for r in verbindung.execute(
            "select distinct model from content_vectors where model is not null"
        )]
    finally:
        verbindung.close()
    if not modelle:
        raise SucheFehler("Index nennt kein Einbettungsmodell.")
    if len(modelle) > 1:
        raise SucheFehler(
            "Index enthaelt Vektoren aus mehreren Modellen: "
            + ", ".join(sorted(modelle))
            + ". Erst `qmd embed -f` neu einbetten."
        )
    return modelle[0]


def qmd_env(geraet: str = GERAET, modell: str | None = None) -> dict[str, str]:
    """Umgebung wie in treiber.py: alles bleibt unterhalb von qmd/."""
    e = dict(os.environ)
    e["XDG_CACHE_HOME"] = str(QMD_DIR / ".cache")
    e["QMD_CONFIG_DIR"] = str(QMD_DIR / ".qmd")
    e["QMD_LLAMA_GPU"] = geraet
    e["QMD_EMBED_MODEL"] = modell or modell_aus_index()
    e.pop("QMD_FORCE_CPU", None)
    return e


class Bruecke:
    """Haelt das Einbettungsmodell. Ein Node-Prozess, JSON je Zeile.

    Langlebig: das Wiki startet die Bruecke beim Serverstart und haelt sie ueber
    Stunden. Stirbt der Prozess, wirft jeder weitere Aufruf `SucheFehler`; es
    gibt keine stille Wiederbelebung und keine Warteschleife.
    """

    def __init__(self, prozess: subprocess.Popen) -> None:
        self._p = prozess
        self._sperre = threading.Lock()
        self._id = 0
        self._modell = ""

    # -- intern ------------------------------------------------------------

    def _lebt(self) -> bool:
        return self._p.poll() is None

    def _sende(self, anfrage: dict[str, Any]) -> dict[str, Any]:
        """Eine Anfrage, eine Antwort. Nur unter der Sperre aufrufen."""
        if not self._lebt():
            raise SucheFehler(
                f"Bruecke ist beendet (Exitcode {self._p.returncode}); "
                "Wissensbasis nicht erreichbar."
            )
        try:
            self._p.stdin.write(json.dumps(anfrage, ensure_ascii=False) + "\n")
            self._p.stdin.flush()
        except (BrokenPipeError, OSError) as e:
            raise SucheFehler(f"Bruecke nimmt keine Anfragen mehr an: {e}") from e

        # Bis zur naechsten Protokollzeile lesen. Alles ohne Kennzeichen ist
        # Ladeausgabe der Modellbibliothek.
        while True:
            zeile = self._p.stdout.readline()
            if zeile == "":
                raise SucheFehler(
                    "Bruecke hat die Verbindung geschlossen, ohne zu antworten "
                    f"(Exitcode {self._p.poll()})."
                )
            zeile = zeile.strip()
            if not zeile.startswith(KENNZEICHEN):
                continue
            try:
                return json.loads(zeile[len(KENNZEICHEN):])
            except json.JSONDecodeError as e:
                raise SucheFehler(f"Bruecke antwortete unlesbar: {e}") from e

    def _ruf(self, op: str, **felder: Any) -> dict[str, Any]:
        with self._sperre:
            self._id += 1
            antwort = self._sende({"id": self._id, "op": op, **felder})
        if not antwort.get("ok"):
            raise SucheFehler(f"Bruecke meldet Fehler: {antwort.get('fehler')}")
        return antwort

    # -- oeffentlich -------------------------------------------------------

    def embed(self, texte: list[str]) -> list[list[float]]:
        """Vektoren zu 2048 Dimensionen, Praefix `query: ` wie im qmd-Patch.

        Nicht normiert; wer gegen den Index rechnet, normiert selbst
        (`suche_vektoriell` tut das).
        """
        if not texte:
            return []
        antwort = self._ruf("embed", texte=texte)
        vektoren = antwort.get("vektoren") or []
        if len(vektoren) != len(texte):
            raise SucheFehler(
                f"Bruecke lieferte {len(vektoren)} Vektoren fuer {len(texte)} Texte."
            )
        return vektoren

    def ping(self) -> dict[str, Any]:
        antwort = self._ruf("ping")
        self._modell = antwort.get("modell", "")
        return antwort

    def schliessen(self) -> None:
        """Sauber beenden. Mehrfach aufrufbar, wirft nie."""
        if not self._lebt():
            return
        try:
            with self._sperre:
                self._id += 1
                self._sende({"id": self._id, "op": "close"})
        except Exception:
            pass
        try:
            self._p.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self._p.kill()
        finally:
            for strom in (self._p.stdin, self._p.stdout):
                try:
                    if strom:
                        strom.close()
                except Exception:
                    pass


def bruecke_start(geraet: str = GERAET, aufwaermen: bool = True) -> Bruecke:
    """Startet den Node-Prozess und laedt das Modell.

    `aufwaermen` bettet einen kurzen Text ein und erzwingt damit das Laden des
    Modells noch im Start. Das ist der Grund, warum das Wiki die Bruecke beim
    Serverstart hochzieht (Plan 09, Abschnitt 11): ohne Aufwaermen laedt qmd das
    Modell erst bei der ersten Einbettung, und dann waere ausgerechnet die erste
    Suche die langsamste.

    Der Aufrufer ist fuer `schliessen` verantwortlich. Das Wiki tut das beim
    Herunterfahren, der Orchestrator am Ende eines Laufs.
    """
    if not BRUECKE_SKRIPT.exists():
        raise SucheFehler(f"Brueckenskript fehlt: {BRUECKE_SKRIPT}")
    prozess = subprocess.Popen(
        ["node", str(BRUECKE_SKRIPT)],
        cwd=str(QMD_DIR),
        env=qmd_env(geraet),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )
    bruecke = Bruecke(prozess)
    try:
        bruecke.ping()          # belegt die Erreichbarkeit
        if aufwaermen:
            vektor = bruecke.embed(["Aufwaermen"])[0]
            if len(vektor) != DIMENSIONEN:
                raise SucheFehler(
                    f"Bruecke liefert {len(vektor)} Dimensionen, der Index hat "
                    f"{DIMENSIONEN}. Modell und Index passen nicht zusammen."
                )
    except Exception:
        bruecke.schliessen()
        raise
    return bruecke


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------


def lade_index_vektoren(
    index: Path | None = None,
) -> tuple[np.ndarray, list[dict[str, Any]]]:
    """Alle Vektoren und Metadaten aus index.sqlite, **L2-normiert**.

    Rueckgabe: Matrix (M, 2048) float32 und je Zeile ein dict mit
    {quelle, collection, titel, chunk, pos}. `quelle` ist der Pfad relativ zu
    `corpus/`; das Praefix `_wurzel/` der Sicht wird dabei entfernt, weil
    build_view.py Dateien ohne Ablageort dorthin legt.

    Vektoren ohne zugehoeriges aktives Dokument (verwaiste Chunks nach einer
    Korpusaenderung) werden uebergangen.
    """
    pfad = index or INDEX_SQLITE
    if not pfad.exists():
        raise SucheFehler(f"Index fehlt: {pfad}")

    verbindung = sqlite3.connect(f"file:{pfad}?mode=ro", uri=True)
    try:
        blob = verbindung.execute(
            "select vectors from vectors_vec_vector_chunks00 where rowid=1"
        ).fetchone()
        if blob is None:
            raise SucheFehler("Index enthaelt keine Vektoren.")
        roh = np.frombuffer(blob[0], dtype=np.float32).reshape(-1, DIMENSIONEN)

        zeilen = verbindung.execute(
            """
            select r.chunk_offset, d.collection, d.path, d.title, cv.seq, cv.pos
              from vectors_vec_rowids r
              join content_vectors cv
                on cv.hash = substr(r.id, 1, 64)
               and cv.seq  = cast(substr(r.id, 66) as integer)
              join documents d
                on d.hash = cv.hash and d.active = 1
            """
        ).fetchall()
    finally:
        verbindung.close()

    if not zeilen:
        raise SucheFehler("Kein Vektor liess sich einem aktiven Dokument zuordnen.")

    plaetze = [z[0] for z in zeilen]
    vektoren = np.array(roh[plaetze], dtype=np.float32)

    # Der Speicher haelt die Vektoren UNNORMIERT (Normen 41 bis 111). Einmal
    # normieren, danach ist das Skalarprodukt der Kosinus.
    normen = np.linalg.norm(vektoren, axis=1, keepdims=True)
    normen[normen == 0.0] = 1.0
    vektoren = vektoren / normen

    metadaten = [
        {
            "quelle": _als_quelle(pfad_in_sicht),
            "collection": collection,
            "titel": titel or "",
            "chunk": int(seq),
            "pos": int(pos or 0),
        }
        for _, collection, pfad_in_sicht, titel, seq, pos in zeilen
    ]
    return vektoren, metadaten


def _als_quelle(pfad_in_sicht: str) -> str:
    """Sichtpfad zu Korpuspfad: `_wurzel/x.md` wird zu `x.md`."""
    p = pfad_in_sicht.replace("\\", "/")
    return p[len("_wurzel/"):] if p.startswith("_wurzel/") else p


# ---------------------------------------------------------------------------
# Suche
# ---------------------------------------------------------------------------


def suche_vektoriell(
    query_vektor: np.ndarray,
    collections: list[str],
    index_vektoren: np.ndarray,
    metadaten: list[dict[str, Any]],
    top_n: int = 8,
) -> list[dict[str, Any]]:
    """Skalarprodukt gegen alle Vektoren der erlaubten Collections, beste top_n.

    `collections` kommt aus rollen.collections_for_role und wird hart gefiltert:
    ein Treffer aus einer nicht genannten Collection ist ein Fehler, kein
    Randfall (T-N1, T-N2). Eine leere Liste ergibt keine Treffer, niemals alle.
    """
    if not collections:
        return []
    if index_vektoren.shape[0] != len(metadaten):
        raise SucheFehler("Vektoren und Metadaten passen nicht zusammen.")

    q = np.asarray(query_vektor, dtype=np.float32).reshape(-1)
    norm = float(np.linalg.norm(q))
    if norm == 0.0:
        return []
    q = q / norm

    erlaubt = set(collections)
    maske = np.array([m["collection"] in erlaubt for m in metadaten], dtype=bool)
    if not maske.any():
        return []

    punkte = index_vektoren[maske] @ q
    indizes = np.nonzero(maske)[0]

    beste = np.argsort(-punkte)[: max(0, top_n)]
    treffer = []
    for k in beste:
        m = metadaten[int(indizes[int(k)])]
        treffer.append({**m, "score": float(punkte[int(k)])})
    return treffer


def dedup_und_top_k(
    treffer_listen: list[list[dict[str, Any]]],
    bereits_vorhanden: list[str],
    ziel_anzahl: int = 4,
) -> list[dict[str, Any]]:
    """Chunks nach Dateipfad gruppieren, bereits vorhandene ueberspringen,
    reihum ueber die Fragen auswaehlen, hoechstens `ziel_anzahl` Dokumente.

    Kein Kosinus-Schwellwert: nach Review-Entscheidung Pfad-Dedup plus Top-K.
    Reihum heisst: erst der beste Treffer jeder Frage, dann der zweitbeste jeder
    Frage, und so fort. Damit kommt jede Frage zum Zug, auch wenn eine andere
    durchweg hoehere Werte liefert.
    """
    gesperrt = set(bereits_vorhanden or [])
    ranglisten: list[list[dict[str, Any]]] = []

    for liste in treffer_listen or []:
        je_quelle: dict[str, dict[str, Any]] = {}
        for t in liste:
            quelle = t["quelle"]
            if quelle in gesperrt:
                continue
            vorher = je_quelle.get(quelle)
            if vorher is None or t["score"] > vorher["score"]:
                je_quelle[quelle] = t
        ranglisten.append(
            sorted(je_quelle.values(), key=lambda t: -t["score"])
        )

    gewaehlt: list[dict[str, Any]] = []
    genommen: set[str] = set()
    tiefe = max((len(r) for r in ranglisten), default=0)
    for stufe in range(tiefe):
        for rangliste in ranglisten:
            if len(gewaehlt) >= ziel_anzahl:
                return gewaehlt
            if stufe >= len(rangliste):
                continue
            t = rangliste[stufe]
            if t["quelle"] in genommen:
                continue
            genommen.add(t["quelle"])
            gewaehlt.append(t)
    return gewaehlt


# ---------------------------------------------------------------------------
# Dokumente
# ---------------------------------------------------------------------------


def lies_dokument(quelle: str) -> str:
    """Volltext zu `quelle`.

    Regelfall ist `corpus/<quelle>`. Die sechs Dokumente der Collection
    `antraege` liegen nicht im Korpus, sondern in `project_proposals/`; deshalb
    der zweite Versuch. Agenten durchsuchen `antraege` nicht, die Wiki-Suche
    ebenso wenig, aber ein halber Fund waere schlimmer als ein klarer Fehler.
    """
    for wurzel in (CORPUS_DIR, ANTRAEGE_DIR):
        pfad = wurzel / quelle
        if pfad.is_file():
            return pfad.read_text(encoding="utf-8", errors="replace")
    raise SucheFehler(f"Dokument nicht gefunden: {quelle}")


def ausschnitt(quelle: str, pos: int = 0, laenge: int = 400) -> str:
    """Textausschnitt ab `pos`, fuer die Trefferanzeige der Wiki-Suche."""
    text = lies_dokument(quelle)
    start = max(0, min(pos, len(text)))
    return text[start:start + laenge].strip()


# ---------------------------------------------------------------------------
# Vorbedingungen (Z10)
# ---------------------------------------------------------------------------


def vorbedingungen(bruecke: Bruecke | None = None) -> dict[str, Any]:
    """Index gesund, Collections vorhanden, Personas nicht leer, Schluessel
    gesetzt, Bruecke antwortet. Rueckgabe mit 'erfuellt' und 'befunde'."""
    befunde: list[str] = []
    einzeln: dict[str, Any] = {}

    if not INDEX_SQLITE.exists():
        befunde.append(f"Index fehlt: {INDEX_SQLITE}")
    else:
        try:
            vektoren, metadaten = lade_index_vektoren()
            einzeln["vektoren"] = int(vektoren.shape[0])
            gefunden = sorted({m["collection"] for m in metadaten})
            einzeln["collections"] = gefunden
            for pflicht in ("intern", "br", "clevel"):
                if pflicht not in gefunden:
                    befunde.append(f"Collection fehlt im Index: {pflicht}")
            if vektoren.shape[0] == 0:
                befunde.append("Index enthaelt keine zuordenbaren Vektoren.")
        except SucheFehler as e:
            befunde.append(str(e))

    leer = [
        p.name
        for p in sorted(PERSONA_DIR.glob("*.md"))
        if not p.read_text(encoding="utf-8", errors="replace").strip()
    ] if PERSONA_DIR.is_dir() else []
    if not PERSONA_DIR.is_dir():
        befunde.append(f"Persona-Verzeichnis fehlt: {PERSONA_DIR}")
    elif leer:
        befunde.append("Leere Persona-Dateien: " + ", ".join(leer))

    if not os.environ.get("ANTHROPIC_API_KEY"):
        befunde.append("ANTHROPIC_API_KEY ist nicht gesetzt.")

    if bruecke is not None:
        try:
            einzeln["bruecke"] = bruecke.ping()
        except SucheFehler as e:
            befunde.append(f"Bruecke antwortet nicht: {e}")

    return {"erfuellt": not befunde, "befunde": befunde, "einzeln": einzeln}
