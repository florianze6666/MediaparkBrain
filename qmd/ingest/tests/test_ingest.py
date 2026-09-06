"""Phase 5, Wissensspeicher: Reset und Import gegen einen eigenen kleinen Index.

Der Test legt unter tmp_path ein komplettes Teilprojekt nach: Korpus mit vier
Dokumenten (intern, C-Level, Betriebsrat-intern, eines unter erweiterung/),
zwei Antraege, eine Sicht, eine Konfiguration `.qmd/index.yml` mit den Modellen
aus index.template.yml. qmd findet die Konfiguration ueber den Ordnernamen
`.qmd` im Arbeitsverzeichnis und legt die Datenbank daneben ab; der echte
Index unter qmd/.qmd wird nie beruehrt. Modelle kommen aus dem echten Cache
qmd/.cache (nur lesend), das Geraet ist Vulkan (Z13), weil der CUDA-Pfad des
Rerankers instabil ist.

Laufzeit: einige Einbettungen kleiner Dokumente, je Aufruf Modell laden plus
wenige Sekunden. Aufruf aus qmd/:  uv run --with pytest pytest ingest/tests -q
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

QMD_DIR = Path(__file__).resolve().parents[2]
INGEST = QMD_DIR / "ingest"
TEMPLATE = QMD_DIR / "index.template.yml"
CACHE = QMD_DIR / ".cache"
PERMISSIONS = QMD_DIR.parent / "llm-wiki" / "permissions.yaml"

pytestmark = pytest.mark.skipif(
    not (QMD_DIR / "node_modules" / ".bin").exists() or not (CACHE / "qmd" / "models").exists(),
    reason="qmd oder Modelle fehlen (npm install, qmd pull)",
)


def _doc(titel: str, stufe: str, ablageort: str, text: str) -> str:
    return (f"---\ndoc_id: LTT-2026-0906-T-001\ntitel: \"{titel}\"\ndokumenttyp: Notiz\n"
            f"datum: 2026-09-06\nverfasser: Test\nrolle: \"-\"\norganisationseinheit: IT\n"
            f"empfaenger: []\nprojekt: \"-\"\ngeschaeftsbereich: \"-\"\nvertraulichkeit: {stufe}\n"
            f"informationsdomaene: [unternehmensweit]\nablageort: {ablageort}\n---\n# {titel}\n\n{text}\n")


@pytest.fixture(scope="module")
def welt(tmp_path_factory):
    """Ein Teilprojekt unter tmp: Korpus, Antraege, Sicht, .qmd-Konfiguration."""
    root = tmp_path_factory.mktemp("qmdwelt")
    corpus = root / "corpus"
    (corpus / "it_doku" / "x").mkdir(parents=True)
    (corpus / "sharepoint_gf" / "x").mkdir(parents=True)
    (corpus / "br_ablage" / "x").mkdir(parents=True)
    (corpus / "erweiterung").mkdir()
    (corpus / "it_doku" / "x" / "a.md").write_text(
        _doc("Softwareportfolio", "intern", "it_doku",
             "Das Softwareportfolio fuehrt proALPHA in Kassel und Infor in Eisenach."), encoding="utf-8")
    (corpus / "sharepoint_gf" / "x" / "b.md").write_text(
        _doc("Beiratsvorlage", "C-Level", "sharepoint_gf",
             "Der Beirat beraet die Verschiebung des Produktivstarts."), encoding="utf-8")
    (corpus / "br_ablage" / "x" / "c.md").write_text(
        _doc("Gremienprotokoll", "Betriebsrat-intern", "br_ablage",
             "Das Gremium prueft die Auswertbarkeit der Dashboard-Daten."), encoding="utf-8")
    (corpus / "erweiterung" / "d.md").write_text(
        _doc("Hochgeladene Richtlinie", "C-Level", "erweiterung",
             "Eine von einem Anwender hochgeladene Richtlinie zur Stammdatenpflege."), encoding="utf-8")
    proposals = root / "project_proposals"
    (proposals / "uploads" / "antrag-eins").mkdir(parents=True)
    (proposals / "antrag-eins.md").write_text(
        "---\neingereicht_von: projektmanager\nrolle: PM\neingereicht_am: 2026-09-06T06:00:00\n"
        "vertraulichkeit: intern\ndomaene: projekt\nempfaenger: []\n---\n# Antrag Eins\n\n"
        "Eingereicht am: 2026-09-06\nEingereicht von: projektmanager\nStatus: Eingereicht\n\n"
        "## Beschreibung\n\nEin Vorhaben zur Abwaermenutzung.\n", encoding="utf-8")
    (proposals / "uploads" / "antrag-eins" / "businesscase.md").write_text(
        "# Business Case\n\nInvestition 1.000.000 EUR, Amortisation vier Jahre.\n", encoding="utf-8")
    (proposals / "antrag-zwei.md").write_text("# Antrag Zwei\n\nKI-gestuetzte Stammdatenpflege.\n",
                                              encoding="utf-8")
    view = root / "view"
    view.mkdir()
    for name in ("intern", "br", "clevel", "antraege"):
        (view / name).mkdir()
    cfg_dir = root / ".qmd"
    cfg_dir.mkdir()
    vorlage = yaml.safe_load(TEMPLATE.read_text(encoding="utf-8").replace("{{QMD_ROOT}}", str(root)))
    cfg = {"collections": {}, "models": vorlage["models"]}
    for name in ("intern", "br", "clevel", "antraege"):
        cfg["collections"][name] = {"path": str(view / name), "pattern": "**/*.md"}
        if name != "intern":
            cfg["collections"][name]["includeByDefault"] = False
    (cfg_dir / "index.yml").write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    env = dict(os.environ)
    env.update({
        "MPB_CORPUS_DIR": str(corpus), "MPB_VIEW_DIR": str(view),
        "MPB_PROPOSALS_DIR": str(proposals), "MPB_PERMISSIONS_FILE": str(PERMISSIONS),
        "QMD_CONFIG_DIR": str(cfg_dir), "MPB_QMD_CACHE": str(CACHE),
        "QMD_TRUST_LOCAL_CONFIG": "1", "QMD_LLAMA_GPU": os.environ.get("QMD_LLAMA_GPU", "vulkan"),
        "PYTHONIOENCODING": "utf-8",
    })
    return {"root": root, "corpus": corpus, "proposals": proposals, "view": view, "env": env}


def _skript(name: str, *args: str, welt: dict, timeout: int = 1200) -> subprocess.CompletedProcess:
    r = subprocess.run([sys.executable, str(INGEST / name), *args], cwd=welt["root"], env=welt["env"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-2000:])
    return r


def _qmd(*args: str, welt: dict) -> str:
    exe = QMD_DIR / "node_modules" / ".bin" / ("qmd.cmd" if os.name == "nt" else "qmd")
    env = dict(welt["env"])
    env["XDG_CACHE_HOME"] = str(CACHE)
    r = subprocess.run([str(exe), *args], cwd=welt["root"], env=env, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=900)
    return r.stdout + r.stderr


def _dokumente(welt: dict) -> tuple[int, int]:
    s = _qmd("status", welt=welt)
    docs = re.search(r"Total:\s+(\d+) files", s)
    vec = re.search(r"Vectors:\s+(\d+) embedded", s)
    return (int(docs.group(1)) if docs else 0, int(vec.group(1)) if vec else 0)


def _dateien(welt: dict, collection: str) -> set[str]:
    return {l.strip() for l in _qmd("ls", collection, welt=welt).splitlines()
            if l.strip().endswith(".md")}


def test_dry_run_meldet_ohne_zu_schreiben(welt):
    r = _skript("import.py", "alles", "--dry-run", welt=welt)
    assert r.returncode == 0
    assert "Sicht: 1 von 4" in r.stdout and "Sicht: 1 von 3" in r.stdout
    assert not any((welt["view"] / "intern").iterdir())
    assert not (welt["root"] / ".qmd" / "index.sqlite").exists()


def test_import_alles_zaehlt_hoch_und_bettet_ein(welt):
    r = _skript("import.py", "alles", welt=welt)
    assert r.returncode == 0, r.stdout
    zeilen = r.stdout.splitlines()
    assert "Sicht: 1 von 4" in r.stdout and "Sicht: 4 von 4" in r.stdout
    assert "Sicht: 3 von 3 uploads/antrag-eins/businesscase.md" in r.stdout
    assert any(z.startswith("Einbettung: 100 %") for z in zeilen)
    assert sum(1 for z in zeilen if z.startswith("Fertig:")) == 2
    docs, vec = _dokumente(welt)
    assert docs == 7 and vec >= 7
    # Erweiterung landet in der Klasse ihres Frontmatters (C-Level -> clevel)
    manifest = json.loads((welt["view"] / "_manifest.json").read_text(encoding="utf-8"))
    e = next(x for x in manifest["eintraege"] if x["quelle"].startswith("erweiterung/"))
    assert e["klasse"] == "clevel" and e["ablageort"] == "erweiterung" and e["domaene"] == "allgemein"
    assert any(f.endswith("d.md") for f in _dateien(welt, "clevel"))
    assert not any(f.endswith("d.md") for f in _dateien(welt, "intern"))
    # Antraege liegen in ihrer eigenen Collection, nie in den Wissensklassen
    antraege = _dateien(welt, "antraege")
    assert len(antraege) == 3 and any(f.endswith("businesscase.md") for f in antraege)
    ma = json.loads((welt["view"] / "_manifest_antraege.json").read_text(encoding="utf-8"))
    assert {x["titel"] for x in ma["eintraege"]} == {"Antrag Eins", "Business Case", "Antrag Zwei"}


def test_reset_antraege_laesst_wissen_stehen(welt):
    docs_vor, _ = _dokumente(welt)
    r = _skript("reset.py", "antraege", "--dry-run", welt=welt)
    assert r.returncode == 0 and "wuerde Collection antraege entfernen" in r.stdout
    assert _dokumente(welt)[0] == docs_vor
    r = _skript("reset.py", "antraege", welt=welt)
    assert r.returncode == 0, r.stdout
    assert "Fertig: antraege zurueckgesetzt" in r.stdout
    docs, _ = _dokumente(welt)
    assert docs == docs_vor - 3
    assert _dateien(welt, "antraege") == set()
    assert not (welt["view"] / "_manifest_antraege.json").exists()
    assert (welt["view"] / "_manifest.json").exists()
    assert len(_dateien(welt, "intern")) == 1 and len(_dateien(welt, "clevel")) == 2
    assert "antraege" in yaml.safe_load((welt["root"] / ".qmd" / "index.yml").read_text(encoding="utf-8"))["collections"]


def test_reset_wissen_laesst_antraege_stehen(welt):
    r = _skript("import.py", "antraege", welt=welt)
    assert r.returncode == 0, r.stdout
    assert len(_dateien(welt, "antraege")) == 3
    r = _skript("reset.py", "wissen", welt=welt)
    assert r.returncode == 0, r.stdout
    docs, _ = _dokumente(welt)
    assert docs == 3
    for k in ("intern", "br", "clevel"):
        assert _dateien(welt, k) == set()
        assert (welt["view"] / k).is_dir() and not any((welt["view"] / k).iterdir())
    assert len(_dateien(welt, "antraege")) == 3
    assert not (welt["view"] / "_manifest.json").exists()
    cfg = yaml.safe_load((welt["root"] / ".qmd" / "index.yml").read_text(encoding="utf-8"))["collections"]
    assert set(cfg) == {"intern", "br", "clevel", "antraege"}
    assert cfg["br"].get("includeByDefault") is False and "includeByDefault" not in cfg["intern"]


def test_import_wissen_nur_ablageort_zaehlt_teilmenge(welt):
    r = _skript("import.py", "wissen", "--ablageort", "erweiterung", welt=welt)
    assert r.returncode == 0, r.stdout
    assert "Sicht: 1 von 1 erweiterung/d.md" in r.stdout
    assert "Sicht: 2 von" not in r.stdout
    docs, vec = _dokumente(welt)
    assert docs == 7 and vec >= 7
    assert len(_dateien(welt, "br")) == 1


def test_unbekannter_ablageort_bricht_ab(welt):
    r = _skript("import.py", "wissen", "--ablageort", "gibtesnicht", "--dry-run", welt=welt)
    assert r.returncode != 0 and "mapping.yaml" in (r.stdout + r.stderr)
