"""ABGELOEST am 06.09.2026. Sequenzielle Fassung des Orchestrators, aufbewahrt als Beleg.

Diese Fassung fuehrt die vier Rollen NACHEINANDER ueber `treiber.fuehre_rolle_aus` aus,
mit Werkzeugrunden und sieben bis neun Modellaufrufen je Rolle. Der T5-Lauf vom
06.09.2026 brauchte damit rund elf Minuten je Rolle, vier Rollen rund fuenfundvierzig.

Abgeloest durch `orchestrator.py` nach `.plans/09_fork_buendel_dedup.md`: gemeinsamer
versiegelter Kontext, vier Rollen gleichzeitig, drei Modellaufrufe je Rolle, Suche ueber
die Bruecke statt ueber einen Unterprozess je Abfrage.

Sie wird nicht mehr gerufen und nicht mehr gepflegt. Sie steht hier, weil sie den
Zustand dokumentiert, gegen den gemessen wurde, und weil `treiber.py` als Referenz
daneben liegen bleibt. Wer sie wieder braucht, muss pruefen, ob `treiber.py` und das
Dateilayout unter `qmd/laeufe/` noch dazu passen.

Der urspruengliche Kopf der Datei folgt.

---

Geskripteter Orchestrator (FR-09), Phase 3 des Dachplans.

Ablauf: Completeness Gate (FR-08) -> Vorbedingungen (Z10) -> vier Rollen nacheinander
(Z1, Z9) -> Zeilen einsammeln und nach 17.5 validieren (Z6) -> Kapitel 16 aggregieren
(Z7) -> Konflikte sichtbar machen (Z8) -> Bericht.

Der Orchestrator ist kein fuenfter Gutachter. Er urteilt nicht, er prueft Form und
fuehrt zusammen.

Aufruf, aus qmd/ in dessen uv-Umgebung:
    uv run python agenten/orchestrator_sequenziell.py --antrag <md> [--antrag <md>] [--rollen cfo,ceo] [--lauf <id>]

Exit-Codes: 0 alle Rollen gueltig - 1 mindestens eine Rolle ohne gueltige Zeile
(Ergebnis liegt trotzdem vor) - 2 Vorbedingung verletzt - 3 Gate nicht bestanden.
Ablage: qmd/laeufe/<lauf_id>/ (siehe 08 Abschnitt 5).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

AGENTEN_DIR = Path(__file__).resolve().parent
QMD_DIR = AGENTEN_DIR.parent
ROOT = QMD_DIR.parent
if str(AGENTEN_DIR) not in sys.path:
    sys.path.insert(0, str(AGENTEN_DIR))

import gate  # noqa: E402
import treiber  # noqa: E402
from schema import ROLLEN, Zusammenfassung, aggregiere, validiere_zeilen  # noqa: E402

REIHENFOLGE: tuple[str, ...] = ROLLEN  # Kapitel 17.1: betriebsrat, cfo, it, ceo


def _jetzt() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Z10: Vorbedingungen
# ---------------------------------------------------------------------------


def _qmd(args: list[str], timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run([str(treiber.qmd_exe()), *args], cwd=QMD_DIR, env=treiber.qmd_env(),
                          capture_output=True, text=True, encoding="utf-8", errors="replace",
                          timeout=timeout)


def vorbedingungen(rollen: list[str]) -> list[str]:
    """Liste der Verstoesse; leer heisst: alles bereit. A-7: keine Attrappe bauen."""
    probleme: list[str] = []
    if not os.environ.get("ANTHROPIC_API_KEY"):
        probleme.append("ANTHROPIC_API_KEY fehlt")
    for rolle in rollen:
        try:
            k = treiber.rollen_konfig(rolle)
            for rel in (k["persona"], k["kalibrierung"], treiber.BEWERTUNGSLOGIK):
                treiber.lies(rel)
        except treiber.TreiberFehler as e:
            probleme.append(str(e))
    benoetigt: set[str] = set()
    for rolle in rollen:
        try:
            benoetigt.update(treiber.collections_for_role(treiber.rollen_konfig(rolle)["nutzer"]))
        except Exception as e:  # noqa: BLE001
            probleme.append(f"{rolle}: {e}")
    if not treiber.qmd_exe().exists():
        probleme.append(f"qmd fehlt: {treiber.qmd_exe()} (npm install in qmd/)")
        return probleme
    try:
        st = _qmd(["status"])
        m_docs = re.search(r"Total:\s+(\d+) files", st.stdout)
        m_vec = re.search(r"Vectors:\s+(\d+) embedded", st.stdout)
        docs = int(m_docs.group(1)) if m_docs else 0
        vec = int(m_vec.group(1)) if m_vec else 0
        if docs <= 0 or vec < docs:
            probleme.append(f"Index nicht gesund: {docs} Dokumente, {vec} Vektoren")
        cl = _qmd(["collection", "list"])
        vorhanden = set(re.findall(r"^(\w+) \(qmd://", cl.stdout, re.M))
        fehlend = sorted(benoetigt - vorhanden)
        if fehlend:
            probleme.append(f"Collections fehlen im Index: {', '.join(fehlend)}")
    except Exception as e:  # noqa: BLE001
        probleme.append(f"qmd status nicht ausfuehrbar: {e}")
    return probleme


# ---------------------------------------------------------------------------
# Lauf
# ---------------------------------------------------------------------------


def orchestriere(
    antrag_pfade: list[Path],
    rollen: list[str],
    lauf_dir: Path,
    lauf_id: str,
    client=None,
    qmd_query: Callable | None = None,
    modell: str = treiber.MODELL,
    mit_vorbedingungen: bool = True,
    ausgabe: Callable[[str], None] = print,
) -> tuple[Optional[Zusammenfassung], int]:
    """Der ganze Ablauf. Liefert (Zusammenfassung oder None, Exit-Code)."""
    lauf_dir.mkdir(parents=True, exist_ok=True)
    zeitpunkt = _jetzt()

    # 1. Completeness Gate (FR-08)
    g = gate.pruefe(antrag_pfade)
    (lauf_dir / "gate.json").write_text(json.dumps(g.als_dict(), ensure_ascii=False, indent=2),
                                        encoding="utf-8")
    if not g.bestanden:
        anforderung = gate.informationsanforderung(g, zeitpunkt)
        (lauf_dir / "informationsanforderung.json").write_text(
            json.dumps(anforderung, ensure_ascii=False, indent=2), encoding="utf-8")
        ausgabe(f"Gate NICHT bestanden: {len(g.fehlend)} Angaben fehlen. Kein Agent gestartet.")
        for f in g.fehlend:
            ausgabe(f"  - {f['angabe']} ({f['grund']})")
        ausgabe(f"Informationsanforderung: {lauf_dir / 'informationsanforderung.json'}")
        return None, 3
    ausgabe(f"Gate bestanden: {len(g.gefunden)} von {len(gate.MINDESTANGABEN)} Angaben.")

    # 2. Vorbedingungen (Z10)
    if mit_vorbedingungen:
        probleme = vorbedingungen(rollen)
        if probleme:
            ausgabe("Vorbedingungen verletzt, Abbruch (Z10):")
            for p in probleme:
                ausgabe(f"  - {p}")
            (lauf_dir / "vorbedingungen.json").write_text(
                json.dumps({"zeitpunkt": zeitpunkt, "probleme": probleme}, ensure_ascii=False, indent=2),
                encoding="utf-8")
            return None, 2

    # 3. Rollen nacheinander (Z1); ein Fehler stoppt die anderen nicht (Z9)
    technische_fehler: list[dict] = []
    protokolle: dict[str, dict] = {}
    for rolle in rollen:
        ausgabe(f"\n== Rolle {rolle}")
        try:
            erg = treiber.fuehre_rolle_aus(rolle, antrag_pfade, lauf_dir, lauf_id, client=client,
                                           qmd_query=qmd_query, modell=modell)
        except Exception as e:  # noqa: BLE001 - der Treiber faengt selbst; das hier ist der Notnagel
            erg = treiber.RollenErgebnis(rolle=rolle, zeile=None, protokoll={}, fehler=f"{type(e).__name__}: {e}")
        protokolle[rolle] = erg.protokoll or {}
        if erg.fehler:
            technische_fehler.append({"rolle": rolle, "fehler": erg.fehler,
                                      "protokoll": erg.dateien.get("protokoll")})
            ausgabe(f"   technischer Fehler: {erg.fehler}")
        else:
            z = erg.zeile
            ausgabe(f"   {z.status}, Score {z.score if z.score is not None else 'KEIN SCORE'}, "
                    f"{len(erg.protokoll.get('rag_abfragen', []))} Abfragen, "
                    f"{len(erg.protokoll.get('zitate', []))} Zitate")

    # 4. Einsammeln aus den Dateien, 17.5 (Z6)
    roh: list[str] = []
    for rolle in rollen:
        f = lauf_dir / f"{rolle}.jsonl"
        if f.exists():
            roh.extend(f.read_text(encoding="utf-8").splitlines())
    gueltig, zeilenfehler = validiere_zeilen(roh)
    for zf in zeilenfehler:
        technische_fehler.append({"rolle": zf.rolle, "fehler": f"17.5: {zf.fehler}"})

    # 5. Kapitel 16 (Z7) und Konflikte (Z8)
    zusammenfassung = aggregiere(gueltig, zeilenfehler, lauf_id, technische_fehler, zeitpunkt)
    zusammenfassung.tokens = summiere_tokens(protokolle)
    reihen = {z.rolle: z for z in gueltig}
    with (lauf_dir / "bewertungen.jsonl").open("w", encoding="utf-8") as fh:
        for rolle in REIHENFOLGE:
            if rolle in reihen:
                fh.write(reihen[rolle].als_jsonl() + "\n")
    (lauf_dir / "zusammenfassung.json").write_text(
        zusammenfassung.model_dump_json(indent=2), encoding="utf-8")

    ausgabe("\n" + bericht(zusammenfassung, rollen))
    ausgabe(f"Ablage: {lauf_dir}")
    exit_code = 0 if len(gueltig) == len(rollen) else 1
    return zusammenfassung, exit_code


def summiere_tokens(protokolle: dict[str, dict]) -> dict:
    """Tokenverbrauch je Rolle und gesamt aus den Rollenprotokollen (`tokens`), auch fuer
    Rollen, die technisch gescheitert sind: bezahlt ist bezahlt."""
    felder = (*treiber._USAGE_FELDER, "aufrufe")
    gesamt = {k: 0 for k in felder}
    je_rolle: dict[str, dict] = {}
    for rolle, prot in protokolle.items():
        t = (prot or {}).get("tokens") or {}
        je_rolle[rolle] = {k: int(t.get(k, 0) or 0) for k in felder}
        for k in felder:
            gesamt[k] += je_rolle[rolle][k]
    return {"je_rolle": je_rolle, "gesamt": gesamt}


def bericht(z: Zusammenfassung, rollen: list[str]) -> str:
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
            "; Konflikte: " + ", ".join(f"{k.rolle_a} {k.score_a} gegen {k.rolle_b} {k.score_b}" for k in z.konflikte)
            if z.konflikte else "; keine Rollenpaare mit Abstand ab 4"))
    if z.fehlende_informationen:
        zeilen.append("Fehlende Informationen (16.5):")
        zeilen.extend(f"  - {l}" for l in z.fehlende_informationen)
    if z.technische_fehler:
        zeilen.append("Technische Fehler:")
        zeilen.extend(f"  - {t.get('rolle')}: {t.get('fehler')}" for t in z.technische_fehler)
    return "\n".join(zeilen)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Orchestrator (sequenziell, abgeloest): Gate, vier Rollen, Kapitel 16.")
    ap.add_argument("--antrag", action="append", required=True, help="Antragsdatei, mehrfach erlaubt")
    ap.add_argument("--rollen", default=",".join(REIHENFOLGE),
                    help="kommagetrennt, Vorgabe alle vier in Kapitel-17-Reihenfolge")
    ap.add_argument("--lauf", default=None, help="Lauf-Kennung; Vorgabe: Zeitstempel")
    ap.add_argument("--modell", default=treiber.MODELL)
    ap.add_argument("--ohne-vorbedingungen", action="store_true",
                    help="Z10 ueberspringen (nur fuer Tests mit gefaelschtem Client)")
    args = ap.parse_args(argv)

    rollen = [r.strip() for r in args.rollen.split(",") if r.strip()]
    unbekannt = [r for r in rollen if r not in ROLLEN]
    if unbekannt:
        print(f"FEHLER: unbekannte Rolle(n): {', '.join(unbekannt)}", file=sys.stderr)
        return 2
    treiber.lade_env()
    pfade = [Path(a).resolve() for a in args.antrag]
    lauf_id = args.lauf or datetime.now().strftime("%Y%m%d-%H%M%S")
    lauf_dir = treiber.LAEUFE_DIR / lauf_id
    _, code = orchestriere(pfade, rollen, lauf_dir, lauf_id, modell=args.modell,
                           mit_vorbedingungen=not args.ohne_vorbedingungen)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
