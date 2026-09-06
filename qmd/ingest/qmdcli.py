"""Duenne Huelle um die qmd-Kommandozeile fuer Ingest-Skripte (Phase 5).

Warum eine Huelle: import.py und reset.py rufen qmd mehrfach (update, embed,
collection add/remove/exclude, cleanup). Umgebung, Arbeitsverzeichnis und die
Erkennung von Abstuerzen (CUDA-Fehler des Rerankers, Mangel M-1) sollen an einer
Stelle stehen. Die Konfiguration wird wie in eval/cfo_e2e.py und env.ps1 auf das
Teilprojekt gebogen; Tests biegen sie per Umgebung auf ein Temp-Verzeichnis.

Umgebung (Vorgabe in Klammern):
    QMD_CONFIG_DIR   Ordner mit index.yml und index.sqlite   (qmd/.qmd)
    MPB_QMD_CACHE    XDG_CACHE_HOME fuer die GGUF-Modelle     (qmd/.cache)
    QMD_LLAMA_GPU    Geraet fuer llama.cpp; unveraendert durchgereicht

Das Arbeitsverzeichnis jedes Aufrufs ist der Elternordner von QMD_CONFIG_DIR:
qmd findet die projektlokale Konfiguration ueber den Ordnernamen `.qmd` und legt
die Datenbank daneben ab. Ein Aufruf mit falschem Arbeitsverzeichnis wuerde still
den globalen Index unter dem Nutzerprofil anlegen.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

QMD_DIR = Path(__file__).resolve().parent.parent
QMD_CMD = QMD_DIR / "node_modules" / ".bin" / ("qmd.cmd" if os.name == "nt" else "qmd")

CUDA_FEHLER = re.compile(r"CUDA error|GGML_ASSERT|ggml-cuda", re.IGNORECASE)


def config_dir() -> Path:
    return Path(os.environ.get("QMD_CONFIG_DIR") or QMD_DIR / ".qmd")


def config_file() -> Path:
    return config_dir() / "index.yml"


def cache_dir() -> Path:
    return Path(os.environ.get("MPB_QMD_CACHE") or QMD_DIR / ".cache")


def env() -> dict[str, str]:
    e = dict(os.environ)
    e["XDG_CACHE_HOME"] = str(cache_dir())
    e["QMD_CONFIG_DIR"] = str(config_dir())
    # Eigene Modelle in einer projektlokalen Konfiguration sind "gated"; ohne
    # Terminal wuerde qmd sie ueberspringen. index.ps1 hat sie mit `qmd trust`
    # freigegeben, die Variable deckt Tests gegen ein frisches Temp-Verzeichnis.
    e.setdefault("QMD_TRUST_LOCAL_CONFIG", "1")
    return e


def cwd() -> Path:
    return config_dir().parent


def run(args: list[str], timeout: int = 3600, zeile=None) -> subprocess.CompletedProcess:
    """qmd <args>. `zeile(text, ist_stderr)` bekommt jede Ausgabezeile sofort,
    damit ein Aufrufer Fortschritt weiterreichen kann. Rueckgabe wie
    subprocess.run mit gesammelter Ausgabe."""
    if not QMD_CMD.exists():
        raise FileNotFoundError(f"{QMD_CMD} fehlt; erst 'npm install' in {QMD_DIR}.")
    cmd = [str(QMD_CMD), *args]
    if zeile is None:
        return subprocess.run(cmd, cwd=cwd(), env=env(), capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout)
    proc = subprocess.Popen(cmd, cwd=cwd(), env=env(), stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                            errors="replace", bufsize=1)
    out: list[str] = []
    assert proc.stdout is not None
    puffer = ""
    while True:
        ch = proc.stdout.read(1)
        if not ch:
            break
        if ch in ("\r", "\n"):
            if puffer.strip():
                out.append(puffer)
                zeile(puffer, False)
            puffer = ""
        else:
            puffer += ch
    if puffer.strip():
        out.append(puffer)
        zeile(puffer, False)
    code = proc.wait(timeout=timeout)
    return subprocess.CompletedProcess(cmd, code, "\n".join(out), "")


def ist_absturz(r: subprocess.CompletedProcess) -> bool:
    text = (r.stdout or "") + (r.stderr or "")
    return r.returncode != 0 and (bool(CUDA_FEHLER.search(text)) or r.returncode in (-1073740791, 3221226505))


def collections() -> dict:
    f = config_file()
    if not f.exists():
        return {}
    data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    return dict(data.get("collections") or {})


def collection_add(name: str, pfad: Path, excluded: bool = True) -> None:
    pfad.mkdir(parents=True, exist_ok=True)
    r = run(["collection", "add", str(pfad), "--name", name])
    if r.returncode != 0:
        raise RuntimeError(f"qmd collection add {name}: {r.stderr.strip() or r.stdout.strip()}")
    if excluded:
        r = run(["collection", "exclude", name])
        if r.returncode != 0:
            raise RuntimeError(f"qmd collection exclude {name}: {r.stderr.strip() or r.stdout.strip()}")


def collection_remove(name: str) -> str:
    """Entfernt Collection und ihre Dokumente aus dem Index. Rueckgabe: qmd-Meldung."""
    r = run(["collection", "remove", name])
    if r.returncode != 0:
        raise RuntimeError(f"qmd collection remove {name}: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.strip()


def status_text() -> str:
    r = run(["status"], timeout=600)
    return r.stdout


def dokumente_im_index() -> tuple[int, int]:
    """(Dokumente, Vektoren) aus `qmd status`."""
    s = status_text()
    m_docs = re.search(r"Total:\s+(\d+) files", s)
    m_vec = re.search(r"Vectors:\s+(\d+) embedded", s)
    return (int(m_docs.group(1)) if m_docs else 0, int(m_vec.group(1)) if m_vec else 0)


def drucke(text: str) -> None:
    """Zeilenweise, sofort: das Wiki liest die letzte Zeile als Fortschritt."""
    print(text, flush=True)


def stdout_utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except (AttributeError, ValueError):
        pass
