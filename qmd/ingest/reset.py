"""Wissensmanagement zuruecksetzen, getrennt (Phase 5, UC-01, Fit-Gap I-3).

    python ingest/reset.py wissen     [--dry-run]   intern, br, clevel: Sicht, Dokumente, Vektoren
    python ingest/reset.py antraege   [--dry-run]   Collection antraege ebenso

Was passiert: `qmd collection remove <name>` loescht die Dokumente der Collection
aus dem Index, der Sichtordner wird geleert, die Collection wird leer wieder
angelegt (br, clevel und antraege ausgeschlossen), `qmd cleanup` raeumt verwaiste
Vektoren ab. Der Korpus unter corpus/ und die Antragsdateien bleiben unberuehrt;
Antragsdateien loescht das Wiki selbst (UC-01, zweiter Knopf).

Die beiden Bereiche haengen nicht voneinander ab: `wissen` laesst antraege
stehen und umgekehrt. Danach stellt ingest/import.py den Zustand wieder her.
Pfade wie in import.py per Umgebung ueberschreibbar.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_view as bv  # noqa: E402
import qmdcli  # noqa: E402

BEREICHE = {
    "wissen": {"collections": list(bv.KLASSEN), "manifest": bv.MANIFEST},
    "antraege": {"collections": [bv.ANTRAEGE], "manifest": bv.MANIFEST_ANTRAEGE},
}


def reset(bereich: str, dry_run: bool) -> int:
    spec = BEREICHE[bereich]
    vorhanden = qmdcli.collections()
    docs_vor, vec_vor = qmdcli.dokumente_im_index() if not dry_run else (0, 0)
    for name in spec["collections"]:
        ordner = bv.VIEW_DIR / name
        if dry_run:
            qmdcli.drucke(f"--dry-run: wuerde Collection {name} entfernen"
                          + (" (fehlt im Index)" if name not in vorhanden else "")
                          + f", Ordner {ordner} leeren und leer neu anlegen")
            continue
        if name in vorhanden:
            qmdcli.drucke(f"Reset: {name}: {qmdcli.collection_remove(name).splitlines()[-1].strip()}")
        else:
            qmdcli.drucke(f"Reset: {name}: Collection fehlte im Index")
        if ordner.exists():
            shutil.rmtree(ordner)
        qmdcli.collection_add(name, ordner, excluded=(name != "intern"))
        qmdcli.drucke(f"Reset: {name}: leer neu angelegt"
                      + ("" if name == "intern" else ", ausgeschlossen"))
    manifest: Path = spec["manifest"]
    if dry_run:
        qmdcli.drucke(f"--dry-run: wuerde {manifest.name} entfernen. Nichts geaendert.")
        return 0
    if manifest.exists():
        manifest.unlink()
    r = qmdcli.run(["cleanup"], timeout=1800)
    if r.returncode != 0:
        qmdcli.drucke(f"Warnung: qmd cleanup Exit {r.returncode}: {(r.stderr or r.stdout).strip()[-200:]}")
    docs, vec = qmdcli.dokumente_im_index()
    qmdcli.drucke(f"Fertig: {bereich} zurueckgesetzt, Index {docs_vor} -> {docs} Dokumente, "
                  f"{vec_vor} -> {vec} Vektoren")
    return 0


def main() -> int:
    qmdcli.stdout_utf8()
    ap = argparse.ArgumentParser(description="Wissensspeicher getrennt zuruecksetzen.")
    ap.add_argument("bereich", choices=sorted(BEREICHE))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not qmdcli.config_file().exists():
        raise SystemExit(f"FEHLER: {qmdcli.config_file()} fehlt; nichts zurueckzusetzen.")
    return reset(args.bereich, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
