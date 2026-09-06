"""Semantische Suche im Korpus über den qmd-Index.

Löst die alte Wortsuche `wiki.search_snippets` ab. Gesucht wird nicht mehr in
den Wiki-Seiten, sondern im Korpus: 218 Dokumente der Lahnberg Thermotechnik
aus 2011 bis 2025, dazu die indizierten Projektanträge.

**Der schnelle Weg, nicht der langsame.** Diese Anbindung ruft
`qmd/agenten/suche.py`, das das Einbettungsmodell im Speicher hält und die
Ähnlichkeit mit numpy gegen die Indexvektoren rechnet: rund achtzig
Millisekunden je Abfrage. Der frühere Weg über einen eigenen Prozess je
Abfrage (`qmd query`, rund zwölf Sekunden) ist verworfen und wird hier nicht
nachgebaut.

**Einbindung** über `sys.path`, genauso wie `qmd/agenten/treiber.py` das
Rechtemodul `qmd/ingest/rollen.py` einbindet. `qmd/` wird nur gelesen.

**Solange die Brücke fehlt**, meldet diese Schicht das offen. Die Umsetzung
von `suche.py` entsteht gerade; bis dahin werfen ihre Funktionen
`NotImplementedError`, und die Oberfläche sagt, dass die semantische Suche noch
nicht verfügbar ist. Es gibt keinen stillen Rückfall auf eine Wortsuche und
keine vorgetäuschten Treffer.
"""
from __future__ import annotations

import logging
import os
import sys
import threading
from dataclasses import dataclass
from pathlib import Path

from . import access

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent.parent   # MediaparkBrain/
TREFFER = 8


def qmd_dir() -> Path:
    env = os.environ.get("MPB_QMD_DIR")
    return Path(env) if env else ROOT / "qmd"


def _qmd_module(paketordner: str, name: str):
    """Modul aus dem qmd-Teilprojekt laden. Muster wie in agenten/treiber.py."""
    pfad = str(qmd_dir() / paketordner)
    if pfad not in sys.path:
        sys.path.insert(0, pfad)
    return __import__(name)


class SucheNichtVerfuegbar(RuntimeError):
    """Brücke, Index oder Rechte erlauben keine Suche. Die Oberfläche zeigt das an."""


@dataclass
class Treffer:
    quelle: str        # Pfad relativ zu corpus/
    titel: str
    collection: str
    ausschnitt: str
    score: float


def collections_fuer(user: str) -> list[str]:
    """Collections, die dieser Nutzer durchsuchen darf.

    Quelle ist `qmd/ingest/rollen.py`, dieselbe Ableitung wie für die Agenten:
    die Gruppen der Rolle gegen die Empfängerlisten der Vertraulichkeitsstufen,
    gelesen aus derselben `permissions.yaml`. Die Wiki-Nutzerkennungen stimmen
    mit den dortigen Rollen überein.

    Wirft `SucheNichtVerfuegbar` für den Gast, für unbekannte Rollen und für
    Rollen ohne Gruppen; für die wird nicht gesucht.
    """
    if not user or user == access.GUEST:
        raise SucheNichtVerfuegbar("Als Gast wird nicht gesucht.")
    try:
        rollen = _qmd_module("ingest", "rollen")
        return list(rollen.collections_for_role(user))
    except ImportError as exc:
        raise SucheNichtVerfuegbar(f"Rechtemodul nicht erreichbar: {exc}") from exc
    except Exception as exc:  # RollenFehler: unbekannte Rolle, Rolle ohne Gruppen
        raise SucheNichtVerfuegbar(str(exc)) from exc


# --- Brücke und Index, einmal geladen und dann gehalten ---------------------

_sperre = threading.Lock()
_bruecke = None
_index: tuple | None = None


_startfehler = ""

NICHT_GEBAUT = ("Die semantische Suche ist noch nicht verfügbar: die "
                "Einbettungsbrücke wird gerade gebaut.")


def aktiviert() -> bool:
    """Ob die Brücke geladen werden soll. In Tests aus (MPB_SUCHE_BRUECKE=0)."""
    return os.environ.get("MPB_SUCHE_BRUECKE", "1").strip().lower() not in ("0", "false", "nein")


def _suche_modul():
    try:
        return _qmd_module("agenten", "suche")
    except ImportError as exc:
        raise SucheNichtVerfuegbar(f"Suchmodul nicht erreichbar: {exc}") from exc


def starte() -> str:
    """Brücke und Indexvektoren laden. Wird beim Serverstart einmal gerufen.

    Kostet rund 4,4 Sekunden und dauerhaft 1,2 GB Grafikspeicher. Wirft nie:
    ein Fehlschlag darf den Server nicht am Starten hindern, er macht nur die
    Suchseite unbrauchbar. Rückgabe: leerer String bei Erfolg, sonst der Grund.
    """
    global _bruecke, _index, _startfehler
    if not aktiviert():
        _startfehler = "Die semantische Suche ist in dieser Umgebung abgeschaltet."
        return _startfehler
    try:
        modul = _suche_modul()
        with _sperre:
            _bruecke = modul.bruecke_start()
            _index = modul.lade_index_vektoren()
        _startfehler = ""
        log.info("Suchbrücke geladen, %d Vektoren", len(_index[1]) if _index else 0)
    except NotImplementedError:
        _startfehler = NICHT_GEBAUT
        log.warning("Suchbrücke: %s", _startfehler)
    except Exception as exc:  # noqa: BLE001 - der Server startet trotzdem
        _startfehler = f"Wissensspeicher nicht erreichbar: {exc}"
        log.warning("Suchbrücke nicht geladen: %s", exc)
    return _startfehler


def schliesse() -> None:
    """Beim Herunterfahren. Fehler hier sind belanglos."""
    global _bruecke, _index
    try:
        if _bruecke is not None:
            _bruecke.schliessen()
    except Exception:  # noqa: BLE001
        pass
    _bruecke, _index = None, None


def _bereit():
    """(Suchmodul, Brücke, Vektoren, Metadaten) aus dem Serverstart.

    Es wird hier nicht nachgeladen: das Laden gehört in den Startvorgang, nicht
    in den ersten Anfragepfad. Fehlt die Brücke, sagt die Oberfläche das.
    """
    if _bruecke is None or _index is None:
        raise SucheNichtVerfuegbar(_startfehler or NICHT_GEBAUT)
    return _suche_modul(), _bruecke, _index[0], _index[1]


def _ausschnitt(modul, quelle: str, laenge: int = 240) -> str:
    """Kurzer Textanfang des Dokuments. Die Indexmetadaten tragen keinen Ausschnitt.

    Der YAML-Kopf wird uebersprungen, sonst stuende in jedem Treffer dieselbe
    Feldliste statt des Inhalts.
    """
    try:
        text = modul.lies_dokument(quelle) or ""
    except Exception:  # noqa: BLE001 - ein fehlender Ausschnitt ist kein Fehler
        return ""
    if text.startswith("---"):
        ende = text.find("\n---", 3)
        if ende > 0:
            text = text[ende + 4:]
    text = " ".join(text.split())
    return text[:laenge] + ("…" if len(text) > laenge else "")


def suche(frage: str, user: str, n: int = TREFFER) -> list[Treffer]:
    """Semantische Suche aus Sicht von `user`. Leere Frage -> leere Liste.

    Die Collections werden zwingend übergeben. Ohne sie durchsuchte der Index
    nur `intern`; das liefert nie zu viel, verschweigt dem Betriebsrat und dem
    C-Level aber ihre eigenen Dokumente.
    """
    if not frage.strip():
        return []
    collections = collections_fuer(user)          # wirft bei Gast/unbekannt
    modul, bruecke, vektoren, metadaten = _bereit()
    try:
        import numpy as np

        vektor = np.asarray(bruecke.embed([frage])[0], dtype="float32")
        roh = modul.suche_vektoriell(vektor, collections, vektoren, metadaten, top_n=n)
    except NotImplementedError as exc:
        raise SucheNichtVerfuegbar(NICHT_GEBAUT) from exc
    except Exception as exc:
        raise SucheNichtVerfuegbar(f"Suche fehlgeschlagen: {exc}") from exc

    treffer: list[Treffer] = []
    for t in roh:
        coll = str(t.get("collection") or "")
        if coll not in collections:
            # Darf nicht vorkommen; wenn doch, ist es ein Leck und kein Randfall.
            log.error("Treffer aus %r, erlaubt sind %s", coll, collections)
            continue
        quelle = str(t.get("quelle") or "")
        treffer.append(Treffer(
            quelle=quelle,
            titel=str(t.get("titel") or Path(quelle).stem),
            collection=coll,
            ausschnitt=_ausschnitt(modul, quelle),
            score=float(t.get("score") or 0.0),
        ))
    return treffer
