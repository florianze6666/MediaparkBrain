"""Import in den Wissensspeicher mit Fortschritt (Phase 5: UC-02, UC-03, I-3).

    python ingest/import.py wissen                 ganzer Korpus: Sicht, Index, Einbettung
    python ingest/import.py wissen --ablageort erweiterung
                                                   dieselbe Kette, Fortschritt nur fuer
                                                   die Dateien dieses Ablageorts
    python ingest/import.py antraege               project_proposals/ in die Collection antraege
    python ingest/import.py alles                  beides nacheinander
    ...                     --dry-run              nur berichten, nichts anlegen

Fortschritt geht zeilenweise auf stdout ("Sicht: 3 von 218", "Einbettung: 40 %",
"Fertig"), damit das Wiki die letzte Zeile anzeigen kann (NFR-11). Eingebettet wird
ohne -f: nur Dokumente ohne Vektor. Die drei Wissens-Collections werden nie
entfernt; dafuer gibt es ingest/reset.py.

Pfade per Umgebung (Vorgabe in Klammern): MPB_CORPUS_DIR (corpus/), MPB_VIEW_DIR
(qmd/view/), MPB_PROPOSALS_DIR (project_proposals/), QMD_CONFIG_DIR (qmd/.qmd),
MPB_QMD_CACHE (qmd/.cache). Laeuft ueber die uv-Umgebung von qmd/ oder jedes
Python 3 mit PyYAML.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_view as bv  # noqa: E402
import qmdcli  # noqa: E402

PROPOSALS_DIR = Path(os.environ.get("MPB_PROPOSALS_DIR") or bv.PROJECT_DIR / "project_proposals")
ANTRAEGE_DIR = bv.VIEW_DIR / bv.ANTRAEGE
PROZENT = re.compile(r"(\d{1,3})%")


# ---------------------------------------------------------------------------
# Gemeinsame Schritte: Index und Einbettung
# ---------------------------------------------------------------------------


def _index_und_einbettung(collection: str | None, dry_run: bool) -> tuple[int, int]:
    """qmd update, dann qmd embed (ohne -f). Fortschritt der Einbettung in Prozent."""
    if dry_run:
        qmdcli.drucke("--dry-run: kein qmd update, kein qmd embed.")
        return (0, 0)
    qmdcli.drucke("Index: qmd update")
    r = qmdcli.run(["update"], timeout=3600,
                   zeile=lambda t, _: qmdcli.drucke("Index: " + t.strip()) if "Index" in t else None)
    if r.returncode != 0:
        raise SystemExit(f"FEHLER: qmd update, Exit {r.returncode}\n{r.stdout[-800:]}")

    letzter = [-1]

    def prozent(text: str, _stderr: bool) -> None:
        m = PROZENT.search(text)
        if m:
            p = int(m.group(1))
            if p != letzter[0]:
                letzter[0] = p
                qmdcli.drucke(f"Einbettung: {p} %")

    args = ["embed", "--timeout", "0"]
    if collection:
        args += ["-c", collection]
    qmdcli.drucke("Einbettung: 0 %")
    r = qmdcli.run(args, timeout=24 * 3600, zeile=prozent)
    if r.returncode != 0 and qmdcli.ist_absturz(r) and os.environ.get("QMD_LLAMA_GPU") != "vulkan":
        # Mangel M-1: CUDA-Pfad instabil. Einmal ueber Vulkan wiederholen (Z13).
        qmdcli.drucke("Einbettung: CUDA-Absturz, Wiederholung ueber Vulkan")
        os.environ["QMD_LLAMA_GPU"] = "vulkan"
        r = qmdcli.run(args, timeout=24 * 3600, zeile=prozent)
    if r.returncode != 0:
        raise SystemExit(f"FEHLER: qmd embed, Exit {r.returncode}\n{r.stdout[-800:]}")
    qmdcli.drucke("Einbettung: 100 %")
    return qmdcli.dokumente_im_index()


# ---------------------------------------------------------------------------
# Unternehmenswissen: corpus/ -> view/<klasse>/ -> intern, br, clevel
# ---------------------------------------------------------------------------


def import_wissen(ablageort: str | None, dry_run: bool) -> int:
    permissions = bv.load_yaml(bv.PERMISSIONS_FILE)
    mapping = bv.load_yaml(bv.MAPPING_FILE)
    stufen = permissions.get("vertraulichkeitsstufen") or {}
    endungen = {e.lower() for e in mapping.get("endungen", [".md"])}
    if ablageort and ablageort not in mapping["ablageorte"]:
        raise SystemExit(f"FEHLER: Ablageort {ablageort!r} steht nicht in ingest/mapping.yaml.")
    fehler = bv.check_domains(mapping, permissions)
    if fehler:
        raise SystemExit("FEHLER: " + "; ".join(fehler))
    if not bv.CORPUS_DIR.is_dir():
        raise SystemExit(f"FEHLER: {bv.CORPUS_DIR} fehlt.")

    entries, warnungen, fehler = bv.plan_entries(mapping, stufen, endungen, klassen_modus=True)
    if fehler:
        raise SystemExit("ABBRUCH: unbekannte Vertraulichkeitsstufe:\n  " + "\n  ".join(fehler[:10]))
    teil = [e for e in entries if not ablageort or e["ablageort"] == ablageort]
    gesamt = len(teil)
    qmdcli.drucke(f"Wissen: {len(entries)} Dateien in {bv.CORPUS_DIR}"
                  + (f", davon {gesamt} in {ablageort}" if ablageort else ""))
    if gesamt == 0:
        qmdcli.drucke("Sicht: 0 von 0")
    if dry_run:
        for i, e in enumerate(teil, 1):
            qmdcli.drucke(f"Sicht: {i} von {gesamt} ({e['klasse']}) {e['quelle']}")
        qmdcli.drucke("--dry-run: nichts angelegt.")
        return 0

    zaehler = [0]
    im_teil = {e["quelle"] for e in teil}

    def fortschritt(_i: int, _n: int, quelle: str) -> None:
        if quelle in im_teil:
            zaehler[0] += 1
            qmdcli.drucke(f"Sicht: {zaehler[0]} von {gesamt} {quelle}")

    verlinkt, kopiert = bv.build(entries, fortschritt=fortschritt)
    bv.schreibe_manifest(entries, warnungen, verlinkt, kopiert)
    # Die Collections selbst legt index.ps1 beziehungsweise reset.py an; hier nur
    # nachziehen, falls eine fehlt (frischer Rechner, Temp-Index im Test).
    vorhanden = qmdcli.collections()
    for klasse in bv.KLASSEN:
        if klasse not in vorhanden:
            qmdcli.collection_add(klasse, bv.VIEW_DIR / klasse, excluded=(klasse != "intern"))
    docs, vec = _index_und_einbettung(None, dry_run)
    qmdcli.drucke(f"Fertig: Wissen {gesamt} von {gesamt} verarbeitet, Index {docs} Dokumente, {vec} Vektoren")
    return 0


# ---------------------------------------------------------------------------
# Projektantraege: project_proposals/ -> view/antraege/ -> antraege
# ---------------------------------------------------------------------------


def _antrag_titel(pfad: Path) -> str:
    head, _ = bv.split_frontmatter(pfad.read_text(encoding="utf-8", errors="replace"))
    if head.get("project_name"):
        return str(head["project_name"])
    for line in pfad.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return pfad.stem


def antraege_dateien() -> list[tuple[Path, Path]]:
    """(Quelle, Ziel relativ zu view/antraege) fuer jede Markdown-Datei eines Antrags."""
    if not PROPOSALS_DIR.is_dir():
        return []
    paare: list[tuple[Path, Path]] = []
    for f in sorted(PROPOSALS_DIR.glob("*.md")):
        paare.append((f, Path(f.name)))
    uploads = PROPOSALS_DIR / "uploads"
    if uploads.is_dir():
        for slug_dir in sorted(p for p in uploads.iterdir() if p.is_dir()):
            for f in sorted(slug_dir.glob("*.md")):
                paare.append((f, Path("uploads") / slug_dir.name / f.name))
    return paare


def import_antraege(dry_run: bool) -> int:
    paare = antraege_dateien()
    gesamt = len(paare)
    qmdcli.drucke(f"Antraege: {gesamt} Markdown-Dateien in {PROPOSALS_DIR}")
    if dry_run:
        for i, (q, z) in enumerate(paare, 1):
            qmdcli.drucke(f"Sicht: {i} von {gesamt} {z.as_posix()}")
        qmdcli.drucke("--dry-run: nichts angelegt.")
        return 0

    if ANTRAEGE_DIR.exists():
        shutil.rmtree(ANTRAEGE_DIR)
    ANTRAEGE_DIR.mkdir(parents=True, exist_ok=True)
    eintraege = []
    verlinkt = kopiert = 0
    for i, (quelle, rel) in enumerate(paare, 1):
        ziel = ANTRAEGE_DIR / rel
        ziel.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(quelle, ziel)
            verlinkt += 1
        except OSError:
            shutil.copy2(quelle, ziel)
            kopiert += 1
        head, _ = bv.split_frontmatter(quelle.read_text(encoding="utf-8", errors="replace"))
        eintraege.append({
            "quelle": str(quelle).replace("\\", "/"),
            "ziel": (str(ziel.relative_to(bv.QMD_DIR)) if ziel.is_relative_to(bv.QMD_DIR)
                     else str(ziel)).replace("\\", "/"),
            "klasse": bv.ANTRAEGE,
            "titel": _antrag_titel(quelle),
            "eingereicht_von": str(head.get("eingereicht_von") or bv.UNKNOWN),
            "vertraulichkeit": str(head.get("vertraulichkeit") or "intern"),
            "project_id": str(head.get("project_id") or ""),
        })
        qmdcli.drucke(f"Sicht: {i} von {gesamt} {rel.as_posix()}")
    bv.MANIFEST_ANTRAEGE.write_text(json.dumps({
        "quelle": str(PROPOSALS_DIR), "dateien": gesamt, "hardlinks": verlinkt,
        "kopien": kopiert, "eintraege": eintraege,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    if bv.ANTRAEGE not in qmdcli.collections():
        qmdcli.collection_add(bv.ANTRAEGE, ANTRAEGE_DIR, excluded=True)
        qmdcli.drucke(f"Collection {bv.ANTRAEGE} angelegt (ausgeschlossen)")
    docs, vec = _index_und_einbettung(bv.ANTRAEGE if gesamt else None, dry_run)
    qmdcli.drucke(f"Fertig: Antraege {gesamt} von {gesamt} verarbeitet, Index {docs} Dokumente, {vec} Vektoren")
    return 0


def main() -> int:
    qmdcli.stdout_utf8()
    ap = argparse.ArgumentParser(description="Import in den qmd-Wissensspeicher mit Fortschritt.")
    ap.add_argument("was", choices=["wissen", "antraege", "alles"])
    ap.add_argument("--ablageort", help="nur Fortschritt fuer diesen Ablageort (Sicht wird ganz gebaut)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not qmdcli.config_file().exists():
        raise SystemExit(f"FEHLER: {qmdcli.config_file()} fehlt; erst index.ps1 ausfuehren.")
    if args.was in ("wissen", "alles"):
        import_wissen(args.ablageort, args.dry_run)
    if args.was in ("antraege", "alles"):
        import_antraege(args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
