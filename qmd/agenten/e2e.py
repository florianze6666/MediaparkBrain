"""Generischer Golden-Test fuer eine Rolle (Phase 2 nach dem CFO-Muster).

Nachfolger von `qmd/eval/cfo_e2e.py` (dort hartcodiert: Rolle, Persona, Antrag, Golden
Dataset). Hier kommt alles von aussen: Rolle, Antragsdateien und eine
`golden_dataset.json`, wie sie unter `test/<fall>/` liegt.

Erwartetes Format der Golden-Datei (je Rolle ein Eintrag; die Eintraege duerfen direkt
auf oberster Ebene oder unter dem Schluessel "rollen" liegen):

    {"rollen": {"cfo": {"golden": ["projektlaufwerk/.../datei.md", ...],
                        "mindest": 4,
                        "erinnerungsspur": "...", "praezedenz": "...", ...}}}

Die fuenf harten Pruefungen des CFO-Treibers:
    1. aktive RAG-Abfrage mit Treffern erfolgt
    2. Golden-Abdeckung erreicht (mindestens `mindest` der Golden-Pfade unter den Treffern)
    3. mindestens ein Zitat vorhanden
    4. mindestens ein Zitat stammt aus dem Golden Dataset
    5. Zeile nach Kapitel 17 gueltig
Dazu weich: die Praezedenz aus der Golden-Datei wird im Essay oder Feld genannt.

Fit-Gap A-3: `--laeufe 3` faehrt dreimal, bestanden bei mindestens zwei, Streuung im
Bericht (NFR-03: status gleich, score hoechstens +-1).

Aufruf, aus qmd/ in dessen uv-Umgebung:
    uv run python agenten/e2e.py --rolle cfo --antrag ../project_proposals/a.md \
        --antrag ../project_proposals/b.md --golden ../test/stammdaten-ki/golden_dataset.json \
        [--laeufe 3] [--lauf <id>]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

AGENTEN_DIR = Path(__file__).resolve().parent
if str(AGENTEN_DIR) not in sys.path:
    sys.path.insert(0, str(AGENTEN_DIR))

import treiber  # noqa: E402
from schema import ROLLEN  # noqa: E402


def lade_golden(pfad: Path, rolle: str) -> dict:
    daten = json.loads(pfad.read_text(encoding="utf-8"))
    rollen = daten.get("rollen", daten)
    if rolle not in rollen:
        raise SystemExit(f"FEHLER: Golden-Datei {pfad} kennt die Rolle {rolle!r} nicht.")
    g = rollen[rolle]
    golden = [p.replace("\\", "/").removeprefix("corpus/") for p in g.get("golden", [])]
    if not golden:
        raise SystemExit(f"FEHLER: Golden-Liste fuer {rolle!r} ist leer.")
    mindest = int(g.get("mindest", max(1, min(len(golden), 4))))
    return {"golden": golden, "mindest": mindest, "praezedenz": g.get("praezedenz"),
            "erinnerungsspur": g.get("erinnerungsspur"), "collections": g.get("collections")}


def pruefe_lauf(erg: treiber.RollenErgebnis, golden: dict) -> dict:
    p = erg.protokoll
    gefunden_alle = {t["datei"] for a in p.get("rag_abfragen", []) for t in a.get("treffer", [])}
    golden_set = set(golden["golden"])
    golden_gefunden = sorted(golden_set & gefunden_alle)
    zitierte = {z["datei"] for z in p.get("zitate", [])}
    praez = (golden.get("praezedenz") or "").strip()
    praez_kurz = praez.split("(")[0].strip().lower() if praez else ""
    praez_genannt = None
    if praez_kurz:
        essay = (p.get("essay") or "").lower()
        feld = ((erg.zeile.praezedenz or "") if erg.zeile else "").lower()
        praez_genannt = praez_kurz in essay or praez_kurz in feld
    pruef = {
        "1_aktive_rag_abfrage": any(a.get("treffer") for a in p.get("rag_abfragen", [])),
        "2_golden_abdeckung": len(golden_gefunden) >= golden["mindest"],
        "2_golden_anteil": f"{len(golden_gefunden)}/{len(golden_set)} (min {golden['mindest']})",
        "3_zitat_vorhanden": bool(p.get("zitate")),
        "4_zitat_aus_golden": bool(zitierte & golden_set),
        "5_zeile_kapitel_17": erg.zeile is not None,
        "weich_praezedenz_genannt": praez_genannt,
        "golden_im_kontext": sorted(golden_set & {d["datei"] for d in p.get("dokumente_im_kontext", [])}),
    }
    harte = [pruef["1_aktive_rag_abfrage"], pruef["2_golden_abdeckung"], pruef["3_zitat_vorhanden"],
             pruef["4_zitat_aus_golden"], pruef["5_zeile_kapitel_17"]]
    return {
        "bestanden": all(harte),
        "pruefung": pruef,
        "golden_gefunden": golden_gefunden,
        "status": erg.zeile.status if erg.zeile else None,
        "score": erg.zeile.score if erg.zeile else None,
        "technischer_fehler": erg.fehler,
        "abfragen": len(p.get("rag_abfragen", [])),
        "abfragen_leer": sum(1 for a in p.get("rag_abfragen", []) if not a.get("treffer")),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Golden-Test einer Rolle ueber den Treiber.")
    ap.add_argument("--rolle", required=True, choices=ROLLEN)
    ap.add_argument("--antrag", action="append", required=True)
    ap.add_argument("--golden", required=True, help="golden_dataset.json")
    ap.add_argument("--laeufe", type=int, default=1, help="Zahl der Laeufe (A-3: 3, bestanden bei 2)")
    ap.add_argument("--lauf", default=None, help="Lauf-Kennung; Vorgabe: Zeitstempel")
    ap.add_argument("--modell", default=treiber.MODELL)
    args = ap.parse_args(argv)

    treiber.lade_env()
    golden = lade_golden(Path(args.golden).resolve(), args.rolle)
    pfade = [Path(a).resolve() for a in args.antrag]
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("FEHLER: ANTHROPIC_API_KEY fehlt.", file=sys.stderr)
        return 2
    lauf_id = args.lauf or datetime.now().strftime("%Y%m%d-%H%M%S")
    basis = treiber.LAEUFE_DIR / lauf_id

    ergebnisse = []
    for i in range(1, args.laeufe + 1):
        lauf_dir = basis / f"{args.rolle}-e2e-{i}" if args.laeufe > 1 else basis
        erg = treiber.fuehre_rolle_aus(args.rolle, pfade, lauf_dir, f"{lauf_id}-{i}", modell=args.modell)
        r = pruefe_lauf(erg, golden)
        r["lauf_dir"] = str(lauf_dir)
        ergebnisse.append(r)
        print(f"Lauf {i}: {'BESTANDEN' if r['bestanden'] else 'DURCHGEFALLEN'}  "
              f"golden {r['pruefung']['2_golden_anteil']}, status {r['status']}, score {r['score']}, "
              f"abfragen {r['abfragen']} (leer {r['abfragen_leer']})"
              + (f"  fehler: {r['technischer_fehler']}" if r["technischer_fehler"] else ""))

    bestanden = sum(1 for r in ergebnisse if r["bestanden"])
    scores = [r["score"] for r in ergebnisse if r["score"] is not None]
    stati = {r["status"] for r in ergebnisse}
    gesamt = bestanden >= (2 if args.laeufe >= 3 else args.laeufe)
    streuung = {
        "status_gleich": len(stati) <= 1,
        "score_spanne": (max(scores) - min(scores)) if scores else None,
        "nfr_03": len(stati) <= 1 and (not scores or (max(scores) - min(scores)) <= 2),
    }
    bericht = {
        "zeitpunkt": datetime.now(timezone.utc).isoformat(), "rolle": args.rolle, "modell": args.modell,
        "golden": golden, "laeufe": ergebnisse, "bestanden": gesamt,
        "bestanden_laeufe": f"{bestanden}/{args.laeufe}", "streuung": streuung,
    }
    basis.mkdir(parents=True, exist_ok=True)
    out = basis / f"e2e_{args.rolle}.json"
    out.write_text(json.dumps(bericht, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nGESAMT: {'BESTANDEN' if gesamt else 'DURCHGEFALLEN'} ({bestanden}/{args.laeufe}); "
          f"Streuung: {streuung}\nBericht: {out}")
    return 0 if gesamt else 1


if __name__ == "__main__":
    raise SystemExit(main())
