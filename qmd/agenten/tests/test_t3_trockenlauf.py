"""T3: Trockenlauf aller vier Rollen mit dem Eisenach-Antrag, ohne qmd und ohne API."""

from __future__ import annotations

import re

import pytest

import treiber
from conftest import EISENACH, STAMMDATEN

ERWARTETE_COLLECTIONS = {
    "betriebsrat": ["intern", "br"],
    "cfo": ["intern", "clevel"],
    "it": ["intern"],
    "ceo": ["intern", "clevel"],
}


@pytest.mark.parametrize("antrag", [EISENACH, STAMMDATEN], ids=["eisenach", "stammdaten"])
@pytest.mark.parametrize("rolle", list(ERWARTETE_COLLECTIONS))
def test_trockenlauf_je_rolle(rolle, antrag):
    for p in antrag:
        assert p.exists(), p
    d = treiber.trockenlauf(rolle, antrag)
    assert d["collections"] == ERWARTETE_COLLECTIONS[rolle]
    assert len(d["module"]) == 4
    assert all(m["zeichen"] > 1000 for m in d["module"]), d["module"]
    assert d["module"][1]["name"].endswith(f"({treiber.ROLLEN_KONFIG[rolle]['persona']})")
    assert d["module"][3]["name"].endswith(f"({treiber.ROLLEN_KONFIG[rolle]['kalibrierung']})")
    assert len(d["antrag"]) == 2 and all(a["zeichen"] > 1000 for a in d["antrag"])
    assert re.fullmatch(r"[0-9a-f]{12}", d["prompt_version"])
    assert d["system_prompt_zeichen"] > 40000
    assert d["qmd"]["geraet"] == treiber.QMD_GERAET and d["qmd"]["deckel"] == 16


def test_nutzerkennung_it_security():
    assert treiber.ROLLEN_KONFIG["it"]["nutzer"] == "it-security"
    assert treiber.ROLLEN_KONFIG["betriebsrat"]["persona"].endswith("betriebsrats_persona.md")


def test_prompt_version_stabil_und_rollenspezifisch():
    assert treiber.prompt_version("cfo") == treiber.prompt_version("cfo")
    assert len({treiber.prompt_version(r) for r in ERWARTETE_COLLECTIONS}) == 4


def test_system_prompt_reihenfolge():
    text, index = treiber.baue_system_prompt("ceo")
    namen = [n for n, _ in index]
    assert namen[0].startswith("Generischer Initialteil")
    assert "Rollen-Persona" in namen[1] and "Bewertungslogik" in namen[2] and "Kalibrierung" in namen[3]
    assert text.index("MODUL: Rollen-Persona") < text.index("MODUL: Bewertungslogik") < text.index("MODUL: Rollenspezifische Kalibrierung")


def test_unbekannte_rolle():
    with pytest.raises(treiber.TreiberFehler, match="Unbekannte Rolle"):
        treiber.trockenlauf("hr", EISENACH)


def test_fehlender_antrag(tmp_path):
    with pytest.raises(treiber.TreiberFehler, match="fehlt"):
        treiber.baue_projektobjekt([tmp_path / "gibt-es-nicht.md"])


def test_leeres_modul_bricht_laut_ab(tmp_path, monkeypatch):
    (tmp_path / "persona").mkdir()
    (tmp_path / "persona" / "cfo_persona.md").write_text("   \n", encoding="utf-8")
    monkeypatch.setattr(treiber, "ROOT", tmp_path)
    with pytest.raises(treiber.TreiberFehler, match="leer"):
        treiber.baue_system_prompt("cfo")


def test_cli_dry_run(capsys):
    code = treiber.main(["--rolle", "it", "--antrag", str(EISENACH[0]), "--antrag", str(EISENACH[1]), "--dry-run"])
    assert code == 0
    out = capsys.readouterr().out
    assert '"collections"' in out and '"intern"' in out
