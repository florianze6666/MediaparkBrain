"""Testsuite fuer den QMD-Wissensspeicher.

Prueft die ganze Kette gegen den vollstaendig indizierten Korpus, ohne API-Kosten:

    1. Patch      patches/apply.mjs ist in node_modules angewandt (Praefixe, BOS)
    2. Modell     eval/embed_smoke.mjs: GGUF laedt auf dem Geraet, 2048-d, Semantik
    3. Doctor     qmd doctor: Fingerprints aktuell, Vektorstichprobe reproduzierbar
    4. Status     qmd status: alle Dokumente indiziert und eingebettet
    5. Bench      qmd bench eval/fixture_intern.json: Vektorsuche und volle Kette
                  treffen je mindestens drei Viertel der Fragen in den ersten drei;
                  jede Frage steht in einem der beiden in den ersten fuenf; BM25
                  schlechter als Vektor (sonst prueft die Frage Wortgleichheit)
    6. Rechte     qmd bench eval/fixture_clevel.json -c clevel trifft; dieselbe Frage
                  ohne -c liefert keinen Treffer aus clevel oder br
    7. Reranker   qmd query mit Reranking liefert das Zieldokument in den ersten
                  drei, meldet keinen Reranker-Ausfall, und --no-rerank laeuft ebenfalls
    8. E2E        optional (--e2e): eval/cfo_e2e.py, braucht ANTHROPIC_API_KEY

Aufruf aus qmd/:
    python eval\\run_tests.py            # GPU, wenn vorhanden
    python eval\\run_tests.py --cpu      # CPU erzwingen (QMD_FORCE_CPU=1)
    python eval\\run_tests.py --quick    # nur 1 bis 4, fuer langsame CPU-Rechner
    python eval\\run_tests.py --e2e      # zusaetzlich der CFO-Ende-zu-Ende-Test

Exit-Code 0 nur, wenn alle harten Pruefungen bestanden sind.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

QMD_DIR = Path(__file__).resolve().parent.parent
EVAL_DIR = QMD_DIR / "eval"
QMD_CMD = QMD_DIR / "node_modules" / ".bin" / ("qmd.cmd" if os.name == "nt" else "qmd")

ERGEBNISSE: list[tuple[str, bool, str]] = []


def pruefung(name: str, ok: bool, detail: str = "") -> bool:
    ERGEBNISSE.append((name, ok, detail))
    print(f"  {'OK    ' if ok else 'FEHLER'} {name}" + (f"  ({detail})" if detail else ""))
    return ok


def qmd_env(cpu: bool) -> dict:
    e = dict(os.environ)
    e["XDG_CACHE_HOME"] = str(QMD_DIR / ".cache")
    e["QMD_CONFIG_DIR"] = str(QMD_DIR / ".qmd")
    if cpu:
        e["QMD_FORCE_CPU"] = "1"
    else:
        e.pop("QMD_FORCE_CPU", None)
    return e


def run(cmd: list[str], cpu: bool, timeout: int = 3600) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=QMD_DIR, env=qmd_env(cpu), capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=timeout)


def qmd(args: list[str], cpu: bool, timeout: int = 3600) -> subprocess.CompletedProcess:
    return run([str(QMD_CMD), *args], cpu, timeout)


def json_aus(stdout: str):
    start = stdout.find("[")
    start_obj = stdout.find("{")
    if start < 0 or (0 <= start_obj < start):
        start = start_obj
    return json.loads(stdout[start:]) if start >= 0 else None


# --------------------------------------------------------------------------


def t_patch(cpu: bool) -> None:
    r = run(["node", str(QMD_DIR / "patches" / "apply.mjs"), "--check"], cpu, 60)
    pruefung("Patch angewandt", r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[:200])


def t_modell(cpu: bool) -> None:
    t = time.time()
    r = run(["node", str(EVAL_DIR / "embed_smoke.mjs"), *(["--cpu"] if cpu else [])], cpu, 3600)
    geraet = next((l for l in r.stdout.splitlines() if l.startswith("Geraet:")), "")
    tempo = next((l for l in r.stdout.splitlines() if l.startswith("Tempo:")), "")
    pruefung("Modell laedt und ordnet Frage/Passage richtig", r.returncode == 0,
             f"{geraet}; {tempo}; {time.time() - t:.0f} s")
    if r.returncode != 0:
        print(r.stdout[-1500:], r.stderr[-800:])


def t_doctor(cpu: bool) -> None:
    r = qmd(["doctor"], cpu, 1800)
    out = r.stdout + r.stderr
    device = next((l.strip() for l in out.splitlines() if "device probe" in l), "")
    print(f"        {device}")
    pruefung("Doctor: Fingerprints aktuell", "✓ embedding fingerprints" in out or "embedding fingerprints" in out and "✗" not in out)
    pruefung("Doctor: Vektorstichprobe reproduzierbar", "✓ embedding vector sample" in out,
             next((l.strip() for l in out.splitlines() if "vector sample" in l), "")[:120])


def t_status(cpu: bool) -> None:
    r = qmd(["status"], cpu, 600)
    m_docs = re.search(r"Total:\s+(\d+) files", r.stdout)
    m_vec = re.search(r"Vectors:\s+(\d+) embedded", r.stdout)
    docs = int(m_docs.group(1)) if m_docs else 0
    vec = int(m_vec.group(1)) if m_vec else 0
    m_embed = re.search(r"Embedding:\s+(\S+)", r.stdout)
    pruefung("Status: Dokumente indiziert und eingebettet", docs > 0 and vec >= docs,
             f"{docs} Dokumente, {vec} Vektoren, Embedding {m_embed.group(1) if m_embed else '?'}")


def bench(fixture: str, cpu: bool, collection: str | None):
    args = ["bench", str(EVAL_DIR / fixture), "--json"]
    if collection:
        args += ["-c", collection]
    r = qmd(args, cpu, 7200)
    if "CUDA error" in r.stderr or "GGML_ASSERT" in r.stderr:
        print("        Laufzeitfehler:", r.stderr.strip().splitlines()[-1][:200])
    try:
        d = json_aus(r.stdout)
    except json.JSONDecodeError:
        d = None
    if d:
        (EVAL_DIR / f"bench_{Path(fixture).stem.replace('fixture_', '')}.json").write_text(
            json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return d


def t_bench_intern(cpu: bool) -> None:
    d = bench("fixture_intern.json", cpu, None)
    if not d:
        pruefung("Bench intern laeuft", False, "kein JSON-Ergebnis")
        return
    # Die Vektorsuche ist deterministisch, die volle Kette nicht (Anfrageerweiterung
    # und Reranking sind LLM-getrieben). Deshalb je Backend eine 75-%-Schwelle in den
    # ersten drei und zusaetzlich: kein Fall geht verloren, jedes Zieldokument steht
    # in mindestens einem der beiden Backends in den ersten fuenf.
    vek = [r["backends"]["vector"]["hits_at_k"] >= 1 for r in d["results"]]
    voll = [r["backends"]["full"]["hits_at_k"] >= 1 for r in d["results"]]
    top5 = [r["backends"]["vector"]["recall_at_5"] > 0 or r["backends"]["full"]["recall_at_5"] > 0
            for r in d["results"]]
    s = d["summary"]
    print("        Frage                        bm25   vektor r@3 r@5 mrr   full r@3 r@5 mrr")
    for r in d["results"]:
        b, v, f = r["backends"], r["backends"]["vector"], r["backends"]["full"]
        print(f"        {r['id']:28s} {b['bm25']['mrr']:.2f}   {v['recall_at_3']:.2f} {v['recall_at_5']:.2f} {v['mrr']:.2f}     "
              f"{f['recall_at_3']:.2f} {f['recall_at_5']:.2f} {f['mrr']:.2f}")
    offen = lambda flags: ", ".join(r["id"] for r, ok in zip(d["results"], flags) if not ok)
    pruefung("Bench intern: Vektorsuche trifft >= 75 % der Fragen in den ersten drei",
             sum(vek) >= 0.75 * len(vek), f"{sum(vek)}/{len(vek)}" + (f", offen: {offen(vek)}" if not all(vek) else ""))
    pruefung("Bench intern: volle Kette trifft >= 75 % der Fragen in den ersten drei",
             sum(voll) >= 0.75 * len(voll), f"{sum(voll)}/{len(voll)}" + (f", offen: {offen(voll)}" if not all(voll) else ""))
    pruefung("Bench intern: jede Frage in den ersten fuenf (Vektor oder volle Kette)",
             all(top5), f"{sum(top5)}/{len(top5)}" + (f", verloren: {offen(top5)}" if not all(top5) else ""))
    pruefung("Bench intern: Semantik statt Wortgleichheit (BM25 < Vektor)",
             s["bm25"]["avg_mrr"] < s["vector"]["avg_mrr"],
             f"MRR bm25 {s['bm25']['avg_mrr']:.2f}, vektor {s['vector']['avg_mrr']:.2f}, full {s['full']['avg_mrr']:.2f}")


def t_rechte(cpu: bool) -> None:
    d = bench("fixture_clevel.json", cpu, "clevel")
    if not d:
        pruefung("Bench clevel laeuft", False, "kein JSON-Ergebnis")
        return
    voll = [r["backends"]["full"]["hits_at_k"] >= 1 for r in d["results"]]
    pruefung("Bench clevel mit -c: full trifft", all(voll), f"{sum(voll)}/{len(voll)}")
    frage = d["results"][0]["query"]
    r = qmd(["vsearch", frage, "-n", "5", "--format", "json"], cpu, 1800)
    try:
        treffer = json_aus(r.stdout) or []
    except json.JSONDecodeError:
        treffer = []
    fremd = [t["file"] for t in treffer if t["file"].startswith(("qmd://clevel/", "qmd://br/"))]
    pruefung("Rechte: ohne -c kein Treffer aus clevel oder br", bool(treffer) and not fremd,
             f"{len(treffer)} Treffer, davon fremd: {len(fremd)}")


def t_reranker(cpu: bool) -> None:
    fixture = json.loads((EVAL_DIR / "fixture_intern.json").read_text(encoding="utf-8"))
    q = next(x for x in fixture["queries"] if x["id"].startswith("02-"))
    ziel = q["expected_files"][0].lower()
    r1 = qmd(["query", q["query"], "-c", "intern", "-n", "5", "--format", "json"], cpu, 3600)
    r2 = qmd(["query", q["query"], "-c", "intern", "-n", "5", "--format", "json", "--no-rerank"], cpu, 3600)
    try:
        t1 = json_aus(r1.stdout) or []
        t2 = json_aus(r2.stdout) or []
    except json.JSONDecodeError:
        t1, t2 = [], []
    ausfall = "Reranker unavailable" in r1.stderr or "skipping reranking" in r1.stderr
    top3 = [t["file"].lower() for t in t1[:3]]
    pruefung("Reranker laeuft (kein Ausfall gemeldet, Treffer vorhanden)", bool(t1) and not ausfall,
             (r1.stderr.strip().splitlines()[-1][:160] if ausfall else f"{len(t1)} Treffer"))
    pruefung("Reranker: Zieldokument in den ersten drei", any(f.endswith(ziel) for f in top3),
             "; ".join(f.split("/")[-1][:40] for f in top3))
    pruefung("--no-rerank laeuft ebenfalls", r2.returncode == 0 and bool(t2), f"{len(t2)} Treffer")


def t_e2e(cpu: bool) -> None:
    # Der Treiber braucht ein aktuelles anthropic-SDK. Das liegt in der eigenen
    # uv-Umgebung dieses Teilprojekts (qmd/pyproject.toml, `uv sync`); das
    # systemweite Python traegt eine alte Fassung und bricht ab. Kein Rueckgriff
    # mehr auf llm-wiki (Entkopplung, 06.09.2026).
    import shutil
    venv_python = QMD_DIR / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if shutil.which("uv"):
        cmd = ["uv", "run", "--project", str(QMD_DIR), "--no-python-downloads",
               "python", str(EVAL_DIR / "cfo_e2e.py")]
    elif venv_python.exists():
        cmd = [str(venv_python), str(EVAL_DIR / "cfo_e2e.py")]
    else:
        cmd = [sys.executable, str(EVAL_DIR / "cfo_e2e.py")]
    r = subprocess.run(cmd, cwd=QMD_DIR, env=qmd_env(cpu),
                       text=True, encoding="utf-8", errors="replace", timeout=7200)
    pruefung("E2E CFO-Gutachter bestanden", r.returncode == 0, "Bericht in eval/cfo_e2e_report.json")


# --------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cpu", action="store_true", help="CPU erzwingen (QMD_FORCE_CPU=1)")
    ap.add_argument("--quick", action="store_true", help="nur Patch, Modell, Doctor, Status")
    ap.add_argument("--e2e", action="store_true", help="zusaetzlich eval/cfo_e2e.py (API-Kosten)")
    args = ap.parse_args()

    if not QMD_CMD.exists():
        sys.exit(f"FEHLER: {QMD_CMD} fehlt. Erst 'npm install' in {QMD_DIR}.")

    # UTF-8 und zeilenweise ausgeben: qmd meldet mit Symbolen (✓ ⚠), die eine
    # cp1252-Konsole nicht kennt, und ein umgeleitetes Protokoll soll waehrend
    # langer Schritte (CPU, E2E) mitlaufen statt erst am Ende zu erscheinen.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

    start = time.time()
    print(f"QMD-Testsuite  ({'CPU erzwungen' if args.cpu else 'Geraet automatisch'})\n")
    schritte = [("1 Patch", t_patch), ("2 Modell", t_modell), ("3 Doctor", t_doctor), ("4 Status", t_status)]
    if not args.quick:
        schritte += [("5 Bench intern", t_bench_intern), ("6 Rechte", t_rechte), ("7 Reranker", t_reranker)]
    if args.e2e:
        schritte.append(("8 E2E", t_e2e))
    for name, fn in schritte:
        print(f"[{name}]")
        t = time.time()
        try:
            fn(args.cpu)
        except Exception as e:  # noqa: BLE001 - jede Ausnahme ist ein Testfehler
            pruefung(f"{name}: Ausnahme", False, f"{type(e).__name__}: {e}"[:200])
        print(f"        {time.time() - t:.0f} s")

    gefallen = [n for n, ok, _ in ERGEBNISSE if not ok]
    print(f"\n{len(ERGEBNISSE) - len(gefallen)}/{len(ERGEBNISSE)} Pruefungen bestanden, {time.time() - start:.0f} s gesamt.")
    if gefallen:
        print("Gefallen: " + "; ".join(gefallen))
    return 1 if gefallen else 0


if __name__ == "__main__":
    raise SystemExit(main())
