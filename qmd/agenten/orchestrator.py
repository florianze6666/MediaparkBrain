"""Orchestrator (FR-09) nach `.plans/09_fork_buendel_dedup.md`.

Drei Abschnitte. **A** laeuft einmal: Gate, Vorbedingungen, Antrag in zwei Teile
eingebettet, Vorsuche ausschliesslich in `intern`, gemeinsamer Kontext, versiegeln,
`basis.json`. **B** laeuft viermal gleichzeitig: je Rolle ein Fork der versiegelten
Basis, drei Modellaufrufe, eigene Dateien. **C** laeuft einmal: Validierung nach 17.5,
Aggregation nach Kapitel 16, Zwischenspeicher-Nachpruefung, Bericht.

Der Orchestrator ist kein fuenfter Gutachter. Er urteilt nicht, er prueft Form und
fuehrt zusammen; die Inhalte der Kontextbloecke kennt er nicht, die liefert
`rollenlauf`.

Aufrufvertrag, unveraendert gegenueber der sequenziellen Fassung, weil
`llm-wiki/app/bewertung.py` ihn fest verdrahtet hat:

    uv run python agenten/orchestrator.py --antrag <md> [--antrag <md>] --lauf <id>

Exit-Codes: 0 alle Rollen gueltig - 1 mindestens eine Rolle ohne gueltige Zeile
(Ergebnis liegt trotzdem vor) - 2 Vorbedingung verletzt - 3 Gate nicht bestanden.
Ablage: qmd/laeufe/<lauf_id>/, Dateinamen unveraendert (Plan 09 Abschnitt 6).

Kein Reranking mehr, siehe AE-05 im Architekturdokument.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

AGENTEN_DIR = Path(__file__).resolve().parent
QMD_DIR = AGENTEN_DIR.parent
ROOT = QMD_DIR.parent
for _p in (str(AGENTEN_DIR), str(QMD_DIR / "ingest")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import gate  # noqa: E402
import kontext as kontext_modul  # noqa: E402
import rollenlauf as rollenlauf_modul  # noqa: E402
import suche as suche_modul  # noqa: E402
from schema import ROLLEN, Zusammenfassung, aggregiere, validiere_zeilen  # noqa: E402

REIHENFOLGE: tuple[str, ...] = ROLLEN  # Kapitel 17.1: betriebsrat, cfo, it, ceo
LAEUFE_DIR = QMD_DIR / "laeufe"

# Abschnitt A: Vorsuche ausschliesslich hier. Das ist die Schnittmenge aller vier
# Rollen; ein Dokument aus `br` oder `clevel` im gemeinsamen Anfang waere ein Bruch
# der Informationsgrenze (AE-03).
BASIS_COLLECTION = "intern"
BASIS_DOKUMENTE = 3          # Plan 09: zwei bis drei Basisdokumente
TREFFER_JE_TEIL = 8

# Tokenfelder der Messages-API, wie sie `rollenlauf` ins Protokoll schreibt.
USAGE_FELDER = ("input_tokens", "output_tokens",
                "cache_creation_input_tokens", "cache_read_input_tokens")

# Zuordnung der Mindestangaben auf die beiden Einbettungsteile, falls der Antrag aus
# EINER Datei besteht. Bei zwei Dateien gewinnt die natuerliche Grenze (Steckbrief
# gegen Business Case), siehe teile_antrag.
TEIL1_ANGABEN = {
    "Projektname",
    "Beschreibung des Vorhabens",
    "Zielsetzung",
    "Fachlicher und organisatorischer Nutzen",
    "Betroffene Geschaeftsprozesse",
    "Betroffene Organisationseinheiten",
    "Begruendung des Vorteils fuer die Organisation",
}


def _jetzt() -> str:
    return datetime.now(timezone.utc).isoformat()


def lade_env() -> None:
    """Liest die .env im Projektwurzelverzeichnis; vorhandene Umgebungsvariablen gewinnen."""
    f = ROOT / ".env"
    if not f.exists():
        return
    for line in f.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", line)
        if m and not line.lstrip().startswith("#"):
            os.environ.setdefault(m.group(1), m.group(2).strip().strip('"').strip("'"))


def lies(rel: str) -> str:
    """Laedt eine Projektdatei. Bricht laut ab, wenn sie fehlt ODER leer ist: ein leeres
    Prompt-Modul faellt im Ergebnis nicht auf (A-7)."""
    f = ROOT / rel
    if not f.exists():
        raise FileNotFoundError(f"Prompt-Modul fehlt: {f}")
    text = f.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"Prompt-Modul ist leer: {f}")
    return text


# ---------------------------------------------------------------------------
# Abschnitt A: die gemeinsame Basis
# ---------------------------------------------------------------------------


def teile_antrag(antrag_pfade: list[Path]) -> tuple[str, str, str]:
    """Zerlegt den Antrag in zwei Teile fuer die Einbettung.

    Der Antrag hat rund 2200 Token und passt damit nicht in das Fenster des
    Einbettungsmodells von 2048. Er wird deshalb zweimal eingebettet, nicht
    abgeschnitten.

    Drei Wege, in dieser Reihenfolge:

    1. **Zwei Dateien**: die natuerliche Grenze. Steckbrief gegen Business Case,
       genau so liegen die Antraege im Projekt vor.
    2. **Eine Datei**: nach Abschnitten, zugeordnet ueber dieselben Ueberschriften-
       muster, die `gate.py` fuer die fuenfzehn Mindestangaben benutzt. Es gibt
       keine zweite Erkennung.
    3. **Rueckfall**: haelftig nach Zeichen. Das steht dann im Protokoll, statt dass
       still der halbe Antrag verloren geht.

    Rueckgabe: (teil1, teil2, strategie).
    """
    texte = {p: p.read_text(encoding="utf-8", errors="replace") for p in antrag_pfade}

    if len(antrag_pfade) >= 2:
        mitte = len(antrag_pfade) // 2
        t1 = "\n\n".join(texte[p] for p in antrag_pfade[:mitte])
        t2 = "\n\n".join(texte[p] for p in antrag_pfade[mitte:])
        if t1.strip() and t2.strip():
            return t1, t2, "dateien"

    if len(antrag_pfade) == 1:
        pfad = antrag_pfade[0]
        muster = {angabe: re.compile(m) for angabe, m in gate.MINDESTANGABEN}
        teil1: list[str] = []
        teil2: list[str] = []
        ziel = teil1  # Abschnitte vor der ersten erkannten Angabe gehoeren zum Steckbrief
        for a in gate.abschnitte(pfad):
            kopf = gate.normalisiere(a.ueberschrift)
            treffer = [angabe for angabe, rx in muster.items() if rx.search(kopf)]
            if treffer:
                # Ein Abschnitt kann auf mehrere Angaben passen; die erste in
                # Dateireihenfolge entscheidet, damit die Zuordnung stabil ist.
                ziel = teil1 if treffer[0] in TEIL1_ANGABEN else teil2
            ziel.append(f"## {a.ueberschrift}\n{a.text}")
        t1, t2 = "\n\n".join(teil1).strip(), "\n\n".join(teil2).strip()
        if t1 and t2:
            return t1, t2, "abschnitte"

    ganz = "\n\n".join(texte[p] for p in antrag_pfade)
    mitte = len(ganz) // 2
    return ganz[:mitte], ganz[mitte:], "haelftig"


def vorsuche(teile: list[str], bruecke, index) -> list[dict[str, Any]]:
    """Basisdokumente fuer den gemeinsamen Anfang. NUR aus `intern` (AE-03).

    Vereinigung der Treffer beider Antragsteile, Pfad-Dedup, die besten
    BASIS_DOKUMENTE. Kein Modellaufruf.
    """
    # `index` ist (Vektoren, Metadaten) aus suche.lade_index_vektoren. Attrappen in den
    # Tests reichen nichts durch; die Suche selbst ist dort ersetzt.
    vektoren, metadaten = index if index is not None else (None, None)
    listen = []
    for vek in bruecke.embed(teile):
        listen.append(suche_modul.suche_vektoriell(
            vek, [BASIS_COLLECTION], vektoren, metadaten, top_n=TREFFER_JE_TEIL))
    gewaehlt = suche_modul.dedup_und_top_k(listen, [], ziel_anzahl=BASIS_DOKUMENTE)
    fremd = [d for d in gewaehlt if d.get("collection") != BASIS_COLLECTION]
    if fremd:
        # Harte Zusicherung, kein Randfall: die Basis sehen alle vier Rollen.
        raise ValueError(
            "Vorsuche lieferte Dokumente ausserhalb von "
            f"{BASIS_COLLECTION}: {[d.get('quelle') for d in fremd]}"
        )
    return gewaehlt


def baue_basis(antrag_pfade: list[Path], bruecke, index) -> tuple[Any, list[dict], str]:
    """Der gemeinsame, versiegelte Anfang. Rueckgabe: (Kontext, Basisdokumente, Strategie).

    Reihenfolge nach Plan 09 Abschnitt 5, und sie ist der Grund des ganzen Umbaus:
    Systemprompt mit Onboarding und Bewertungslogik, dann der vollstaendige Antrag,
    dann die Basisdokumente. Erst DAHINTER haengt jeder Fork Persona und Kalibrierung
    an. Stuende die Persona vor dem Antrag, waere der gemeinsame Anfang nicht mehr
    gemeinsam und jede Rolle zahlte die rund 14 000 Token neu.
    """
    Block = kontext_modul.Block
    Dokument = kontext_modul.Dokument

    teil1, teil2, strategie = teile_antrag(antrag_pfade)
    basis_treffer = vorsuche([teil1, teil2], bruecke, index)

    dokumente = tuple(
        Dokument(
            quelle=d["quelle"],
            titel=d.get("titel") or Path(d["quelle"]).stem,
            collection=d.get("collection", BASIS_COLLECTION),
            text=suche_modul.lies_dokument(d["quelle"]),
            score=float(d.get("score", 0.0)),
        )
        for d in basis_treffer
    )

    antragstext = "\n\n".join(
        f"### Projektdatei: {p.name}\n\n{p.read_text(encoding='utf-8', errors='replace')}"
        for p in antrag_pfade
    )

    k = kontext_modul.Kontext()
    k.append(
        Block(art="system", inhalt=rollenlauf_modul.INITIALTEIL, quelle="initialteil"),
        Block(art="system", inhalt=lies(rollenlauf_modul.BEWERTUNGSLOGIK),
              quelle=rollenlauf_modul.BEWERTUNGSLOGIK),
        Block(art="user", inhalt="# Zu bewertendes Vorhaben\n\n" + antragstext, quelle="antrag"),
        Block(art="dokumente", dokumente=dokumente, quelle="vorsuche"),
    )
    return k.freeze(), basis_treffer, strategie


# ---------------------------------------------------------------------------
# Vorbedingungen (Z10) und Guthaben
# ---------------------------------------------------------------------------


def vorbedingungen(rollen: list[str], bruecke=None) -> list[str]:
    """Liste der Verstoesse; leer heisst: alles bereit (A-7: keine Attrappe bauen).

    Index, Collections und Bruecke prueft `suche`; die rollenbezogenen Dateien prueft
    der Orchestrator, weil `suche` von Rollen nichts weiss.
    """
    probleme: list[str] = []
    if not os.environ.get("ANTHROPIC_API_KEY"):
        probleme.append("ANTHROPIC_API_KEY fehlt")

    for rolle in rollen:
        k = rollenlauf_modul.ROLLEN_KONFIG.get(rolle)
        if k is None:
            probleme.append(f"unbekannte Rolle: {rolle}")
            continue
        for rel in (k["persona"], k["kalibrierung"], rollenlauf_modul.BEWERTUNGSLOGIK):
            try:
                lies(rel)
            except (FileNotFoundError, ValueError) as e:
                probleme.append(str(e))

    try:
        erg = suche_modul.vorbedingungen(bruecke)
        if not erg.get("erfuellt"):
            probleme.extend(erg.get("befunde") or ["Suche meldet Vorbedingungen als nicht erfuellt"])
    except Exception as e:  # noqa: BLE001
        probleme.append(f"Vorbedingungen der Suche nicht pruefbar: {type(e).__name__}: {e}")
    return probleme


def pruefe_guthaben(client) -> Optional[str]:
    """Ein winziger Modellaufruf, bevor vier Rollen gleichzeitig starten.

    Ohne diese Pruefung brechen bei knappem Guthaben alle vier Rollen zugleich ab und
    verbrennen den halben Lauf; genau das ist beim T5-Lauf am 06.09.2026 passiert.
    Rueckgabe: Fehlertext oder None.
    """
    if client is None:
        return None
    try:
        client.messages.create(
            model=rollenlauf_modul.MODELL,
            max_tokens=1,
            messages=[{"role": "user", "content": "."}],
        )
    except Exception as e:  # noqa: BLE001
        text = str(e)
        if "credit balance" in text or "insufficient" in text.lower():
            return f"Guthaben reicht nicht: {text[:200]}"
        # Andere Fehler sind hier kein Abbruchgrund; sie treffen die Rollen ohnehin
        # und werden dort je Rolle als technischer Fehler sichtbar (Z9).
        return None
    return None


# ---------------------------------------------------------------------------
# Abschnitt B: vier Rollen (versetzter Start: 1 Vorhut, danach 3 parallel)
# ---------------------------------------------------------------------------


def fuehre_rollen_aus(
    basis,
    prae_quellen: list[str],
    rollen: list[str],
    lauf_dir: Path,
    bruecke,
    index,
    ausgabe: Callable[[str], None] = print,
    rollenlauf_fn: Callable | None = None,
    stagger_s: float | None = None,
) -> dict[str, dict]:
    """Event-gesteuertes Scheduling: die erste Rolle startet als Vorhut. Sobald sie
    ihren Tool-Call (Zug 1) erhaelt, ist das Praefix bei Anthropic im RAM geschrieben.
    Ein Event signalisiert den Folgerollen den Start, die dann gestaffelt (z.B. je 2s Versatz)
    loslaufen und vollstaendig aus dem Cache lesen.

    Z9: eine gescheiterte Rolle stoppt die anderen nicht. Der Rollenlauf faengt selbst;
    was hier ankommt, ist der Notnagel fuer alles, was er nicht gefangen hat.
    """
    fn = rollenlauf_fn or rollenlauf_modul.rollenlauf

    if not rollen:
        return {}

    default_stagger = "0.0" if "PYTEST_CURRENT_TEST" in os.environ else "2.0"
    versatz = float(os.environ.get("FORK_STAGGER_S", default_stagger)) if stagger_s is None else stagger_s
    cache_bereit = threading.Event()
    erste = rollen[0]
    rest = rollen[1:]

    import inspect
    sig = inspect.signature(fn)
    unterstuetzt_callback = "on_cache_warm" in sig.parameters or any(
        p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
    )

    def eine(rolle: str, ist_vorhut: bool = False, delay_s: float = 0.0) -> dict:
        if not ist_vorhut:
            # Warten bis Vorhut Zug 1 (Tool-Call) abgeschlossen hat
            cache_bereit.wait(timeout=180.0)
            if delay_s > 0:
                time.sleep(delay_s)

        def on_warm():
            if ist_vorhut and not cache_bereit.is_set():
                ausgabe(f"  [Cache bereit] {rolle} hat Zug 1 beendet -> Folgerollen freigegeben.")
                cache_bereit.set()

        kwargs = {}
        if unterstuetzt_callback:
            kwargs["on_cache_warm"] = on_warm if ist_vorhut else None

        try:
            return fn(basis, prae_quellen, rolle, lauf_dir, bruecke=bruecke, index=index, **kwargs)
        except Exception as e:  # noqa: BLE001
            return {"rolle": rolle, "ok": False,
                    "technischer_fehler": {"art": type(e).__name__, "details": str(e)}}
        finally:
            # Sicherheitsnetz: stuerzt die Vorhut ab, wird das Event trotzdem ausgeloest (Z9)
            if ist_vorhut and not cache_bereit.is_set():
                cache_bereit.set()

    with ThreadPoolExecutor(max_workers=len(rollen)) as ex:
        f_erste = ex.submit(eine, erste, True, 0.0)
        f_rest = [
            ex.submit(eine, r, False, i * versatz)
            for i, r in enumerate(rest)
        ]
        ergebnisse = [f_erste.result()]
        for f in f_rest:
            ergebnisse.append(f.result())

    out: dict[str, dict] = {}
    for erg in ergebnisse:
        rolle = (erg or {}).get("rolle", "?")
        out[rolle] = erg or {}
        if (erg or {}).get("ok"):
            z = erg.get("zeile")
            score = getattr(z, "score", None) if z is not None else None
            status = getattr(z, "status", "?") if z is not None else "?"
            ausgabe(f"  {rolle:<13} {status}, Score {score if score is not None else 'KEIN SCORE'}")
        else:
            tf = (erg or {}).get("technischer_fehler") or {}
            ausgabe(f"  {rolle:<13} technischer Fehler: {tf.get('art')}: {tf.get('details')}")
    return out


# ---------------------------------------------------------------------------
# Abschnitt C: einsammeln, aggregieren, nachpruefen
# ---------------------------------------------------------------------------


def summiere_tokens(protokolle: dict[str, dict]) -> dict:
    """Tokenverbrauch je Rolle und gesamt, auch fuer gescheiterte Rollen: bezahlt ist bezahlt."""
    felder = (*USAGE_FELDER, "aufrufe")
    gesamt = {k: 0 for k in felder}
    je_rolle: dict[str, dict] = {}
    for rolle, prot in protokolle.items():
        t = (prot or {}).get("tokens") or {}
        je_rolle[rolle] = {k: int(t.get(k, 0) or 0) for k in felder}
        for k in felder:
            gesamt[k] += je_rolle[rolle][k]
    return {"je_rolle": je_rolle, "gesamt": gesamt}


def pruefe_zwischenspeicher(protokolle: dict[str, dict], erwartet: Optional[str] = None) -> dict:
    """Hat der gemeinsame Anfang wirklich getragen?

    Zwei Fragen. Erstens: haben alle Rollen denselben Fingerabdruck gesehen? Wenn nicht,
    war der Anfang nicht gemeinsam. Zweitens: gab es Lesevorgaenge aus dem
    Zwischenspeicher? Bei vier Rollen schreibt die erste, die drei uebrigen lesen.

    Ohne diese Nachpruefung bliebe eine vertauschte Prompt-Reihenfolge unbemerkt und
    stillschweigend teuer: jede Rolle zahlte die rund 14 000 Token des Anfangs neu.
    """
    fingerabdruecke = {r: (p or {}).get("prompt_version") for r, p in protokolle.items()}
    vorhanden = {f for f in fingerabdruecke.values() if f}
    gelesen = [r for r, p in protokolle.items()
               if int(((p or {}).get("tokens") or {}).get("cache_read_input_tokens", 0) or 0) > 0]

    warnungen: list[str] = []
    if len(vorhanden) > 1:
        warnungen.append(
            "Die Rollen haben verschiedene Prompt-Fingerabdruecke gesehen: "
            f"{sorted(vorhanden)}. Der gemeinsame Anfang war nicht gemeinsam."
        )
    if erwartet and vorhanden and vorhanden != {erwartet}:
        warnungen.append(
            f"Fingerabdruck weicht von der versiegelten Basis ab (erwartet {erwartet})."
        )
    if len(protokolle) > 1 and len(gelesen) < len(protokolle) - 1:
        warnungen.append(
            f"Nur {len(gelesen)} von {len(protokolle)} Rollen haben aus dem Zwischenspeicher "
            "gelesen. Erwartet: alle ausser der ersten. Reihenfolge im Prompt pruefen "
            "(Plan 09 Abschnitt 5)."
        )
    return {
        "fingerabdruecke": fingerabdruecke,
        "aus_zwischenspeicher_gelesen": gelesen,
        "warnungen": warnungen,
    }


def bericht(z: Zusammenfassung, rollen: list[str], zwischenspeicher: dict | None = None) -> str:
    zeilen = ["Rolle         Status              Score", "-" * 44]
    je_rolle = {r.rolle: r for r in z.rollen}
    for rolle in rollen:
        r = je_rolle.get(rolle)
        if r is None:
            zeilen.append(f"{rolle:<13} technischer Fehler  -")
        else:
            sc = r.score if r.score is not None else "KEIN SCORE"
            zeilen.append(f"{rolle:<13} {r.status:<19} {sc}")
    zeilen.append("-" * 44)
    gs = z.gesamtscore if z.gesamtscore is not None else "KEIN SCORE"
    zeilen.append(f"Gesamt        {z.gesamtstatus:<19} {gs}  (ueber {z.anzahl_bewertet} gueltige Scores)")
    if z.spanne is not None:
        zeilen.append(f"Spanne {z.spanne}" + (
            "; Konflikte: " + ", ".join(
                f"{k.rolle_a} {k.score_a} gegen {k.rolle_b} {k.score_b}" for k in z.konflikte)
            if z.konflikte else "; keine Rollenpaare mit Abstand ab 4"))
    if z.fehlende_informationen:
        zeilen.append("Fehlende Informationen (16.5):")
        zeilen.extend(f"  - {l}" for l in z.fehlende_informationen)
    if z.technische_fehler:
        zeilen.append("Technische Fehler:")
        zeilen.extend(f"  - {t.get('rolle')}: {t.get('fehler')}" for t in z.technische_fehler)
    for w in (zwischenspeicher or {}).get("warnungen", []):
        zeilen.append(f"WARNUNG Zwischenspeicher: {w}")
    return "\n".join(zeilen)


# ---------------------------------------------------------------------------
# Der ganze Lauf
# ---------------------------------------------------------------------------


def orchestriere(
    antrag_pfade: list[Path],
    rollen: list[str],
    lauf_dir: Path,
    lauf_id: str,
    client=None,
    bruecke=None,
    index=None,
    mit_vorbedingungen: bool = True,
    ausgabe: Callable[[str], None] = print,
    rollenlauf_fn: Callable | None = None,
    bruecke_factory: Callable | None = None,
    index_factory: Callable | None = None,
) -> tuple[Optional[Zusammenfassung], int]:
    """Abschnitt A, B und C. Liefert (Zusammenfassung oder None, Exit-Code).

    `bruecke_factory` und `index_factory` werden erst NACH dem Gate gerufen. Das Gate
    ist der billige Pfad; ein durchgefallener Antrag darf nicht erst das
    Einbettungsmodell laden (4,4 Sekunden, 1,2 GB Grafikspeicher).
    """
    lauf_dir.mkdir(parents=True, exist_ok=True)
    zeitpunkt = _jetzt()

    # --- A1: Completeness Gate (FR-08) ------------------------------------
    g = gate.pruefe(antrag_pfade)
    (lauf_dir / "gate.json").write_text(
        json.dumps(g.als_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    if not g.bestanden:
        (lauf_dir / "informationsanforderung.json").write_text(
            json.dumps(gate.informationsanforderung(g, zeitpunkt), ensure_ascii=False, indent=2),
            encoding="utf-8")
        ausgabe(f"Gate NICHT bestanden: {len(g.fehlend)} Angaben fehlen. Kein Agent gestartet.")
        for f in g.fehlend:
            ausgabe(f"  - {f['angabe']} ({f['grund']})")
        return None, 3
    ausgabe(f"Gate bestanden: {len(g.gefunden)} von {len(gate.MINDESTANGABEN)} Angaben.")

    # Erst jetzt das teure Geraet: Modell laden und Vektoren lesen.
    if bruecke is None and bruecke_factory is not None:
        bruecke = bruecke_factory()
    if index is None and index_factory is not None:
        index = index_factory()

    # --- A2: Vorbedingungen (Z10) und Guthaben ----------------------------
    if mit_vorbedingungen:
        probleme = vorbedingungen(rollen, bruecke)
        guthaben = pruefe_guthaben(client)
        if guthaben:
            probleme.append(guthaben)
        if probleme:
            ausgabe("Vorbedingungen verletzt, Abbruch (Z10):")
            for p in probleme:
                ausgabe(f"  - {p}")
            (lauf_dir / "vorbedingungen.json").write_text(
                json.dumps({"zeitpunkt": zeitpunkt, "probleme": probleme},
                           ensure_ascii=False, indent=2), encoding="utf-8")
            return None, 2

    # --- A3: gemeinsame Basis ---------------------------------------------
    basis, basis_treffer, strategie = baue_basis(antrag_pfade, bruecke, index)
    prae_quellen = [d["quelle"] for d in basis_treffer]
    basis.speichern(lauf_dir / "basis.json")
    ausgabe(f"Basis versiegelt: {len(prae_quellen)} Dokumente aus {BASIS_COLLECTION}, "
            f"Antragsteilung '{strategie}', Fingerabdruck {basis.fingerprint()[:12]}")

    # --- B: vier Rollen gleichzeitig --------------------------------------
    ausgabe(f"\n== {len(rollen)} Rollen gleichzeitig")
    ergebnisse = fuehre_rollen_aus(basis, prae_quellen, rollen, lauf_dir, bruecke, index,
                                   ausgabe=ausgabe, rollenlauf_fn=rollenlauf_fn)

    technische_fehler: list[dict] = []
    protokolle: dict[str, dict] = {}
    for rolle in rollen:
        erg = ergebnisse.get(rolle) or {}
        protokolle[rolle] = erg.get("protokoll") or _protokoll_von_platte(lauf_dir, rolle)
        if not erg.get("ok"):
            tf = erg.get("technischer_fehler") or {"art": "unbekannt", "details": "keine Rueckgabe"}
            technische_fehler.append({
                "rolle": rolle,
                "fehler": f"{tf.get('art')}: {tf.get('details')}",
                "protokoll": str(lauf_dir / f"{rolle}.protokoll.json"),
            })

    # --- C: einsammeln (17.5), aggregieren (Kapitel 16), nachpruefen ------
    roh: list[str] = []
    for rolle in rollen:
        f = lauf_dir / f"{rolle}.jsonl"
        if f.exists():
            roh.extend(f.read_text(encoding="utf-8").splitlines())
    gueltig, zeilenfehler = validiere_zeilen(roh)
    for zf in zeilenfehler:
        technische_fehler.append({"rolle": zf.rolle, "fehler": f"17.5: {zf.fehler}"})

    zusammenfassung = aggregiere(gueltig, zeilenfehler, lauf_id, technische_fehler, zeitpunkt)
    zusammenfassung.tokens = summiere_tokens(protokolle)
    zwischenspeicher = pruefe_zwischenspeicher(protokolle, basis.fingerprint())

    reihen = {z.rolle: z for z in gueltig}
    with (lauf_dir / "bewertungen.jsonl").open("w", encoding="utf-8") as fh:
        for rolle in REIHENFOLGE:
            if rolle in reihen:
                fh.write(reihen[rolle].als_jsonl() + "\n")

    # Zwischenspeicher-Befund als eigener Schluessel neben dem Kapitel-16-Ergebnis:
    # `Zusammenfassung` traegt ihn nicht als Feld, und `schema.py` gehoert einem
    # anderen Bauauftrag. Das Dashboard liest unbekannte Schluessel nicht mit.
    daten = json.loads(zusammenfassung.model_dump_json())
    daten["zwischenspeicher"] = zwischenspeicher
    daten["antrag_teilung"] = strategie
    (lauf_dir / "zusammenfassung.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    ausgabe("\n" + bericht(zusammenfassung, rollen, zwischenspeicher))
    ausgabe(f"Ablage: {lauf_dir}")
    return zusammenfassung, (0 if len(gueltig) == len(rollen) else 1)


def _protokoll_von_platte(lauf_dir: Path, rolle: str) -> dict:
    """Notnagel: ist eine Rolle so hart gescheitert, dass sie nichts zurueckgab, steht
    ihr Protokoll-Rumpf trotzdem auf der Platte (Plan 09, Abschnitt 6)."""
    f = lauf_dir / f"{rolle}.protokoll.json"
    if not f.exists():
        return {}
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Orchestrator: Gate, gemeinsame Basis, vier Rollen gleichzeitig, Kapitel 16.")
    ap.add_argument("--antrag", action="append", required=True, help="Antragsdatei, mehrfach erlaubt")
    ap.add_argument("--rollen", default=",".join(REIHENFOLGE),
                    help="kommagetrennt, Vorgabe alle vier in Kapitel-17-Reihenfolge")
    ap.add_argument("--lauf", default=None, help="Lauf-Kennung; Vorgabe: Zeitstempel")
    ap.add_argument("--modell", default=rollenlauf_modul.MODELL)
    ap.add_argument("--ohne-vorbedingungen", action="store_true",
                    help="Z10 ueberspringen (nur fuer Tests mit gefaelschtem Client)")
    args = ap.parse_args(argv)

    rollen = [r.strip() for r in args.rollen.split(",") if r.strip()]
    unbekannt = [r for r in rollen if r not in ROLLEN]
    if unbekannt:
        print(f"FEHLER: unbekannte Rolle(n): {', '.join(unbekannt)}", file=sys.stderr)
        return 2

    lade_env()
    os.environ.setdefault("EVAL_MODEL", args.modell)
    pfade = [Path(a).resolve() for a in args.antrag]
    lauf_id = args.lauf or datetime.now().strftime("%Y%m%d-%H%M%S")
    lauf_dir = LAEUFE_DIR / lauf_id

    from anthropic import Anthropic

    gestartet: list[Any] = []

    def bruecke_starten():
        b = suche_modul.bruecke_start()
        gestartet.append(b)
        return b

    try:
        _, code = orchestriere(pfade, rollen, lauf_dir, lauf_id, client=Anthropic(),
                               mit_vorbedingungen=not args.ohne_vorbedingungen,
                               bruecke_factory=bruecke_starten,
                               index_factory=suche_modul.lade_index_vektoren)
        return code
    finally:
        for b in gestartet:
            try:
                b.schliessen()
            except Exception:  # noqa: BLE001 - beim Aufraeumen nicht neu scheitern
                pass


if __name__ == "__main__":
    raise SystemExit(main())
