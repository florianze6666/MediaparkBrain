"""T2: Completeness Gate. Lahnberg besteht, die vier Company-Antraege fallen durch."""

from __future__ import annotations

import pytest

import gate
from conftest import COMPANY, EISENACH


def test_eisenach_paar_besteht():
    erg = gate.pruefe(EISENACH)
    assert erg.bestanden, erg.fehlend
    assert len(erg.gefunden) == len(gate.MINDESTANGABEN) == 15


def test_eisenach_charter_allein_faellt_an_den_kaufmaennischen_angaben():
    erg = gate.pruefe([EISENACH[0]])
    assert not erg.bestanden
    fehlend = {f["angabe"] for f in erg.fehlend}
    assert {"Business Case", "Erwartete Kosten", "Erwarteter wirtschaftlicher Nutzen"} <= fehlend
    assert all(f["grund"] == "keine Ueberschrift" for f in erg.fehlend)


@pytest.mark.parametrize("pfad", COMPANY, ids=[p.stem for p in COMPANY])
def test_company_antraege_fallen_mit_markierten_luecken_durch(pfad):
    erg = gate.pruefe([pfad])
    assert not erg.bestanden
    assert len(erg.fehlend) >= 8, erg.fehlend
    je_angabe = {f["angabe"]: f["grund"] for f in erg.fehlend}
    for angabe in ("Betroffene Geschaeftsprozesse", "Betroffene Organisationseinheiten",
                   "Risikoanalyse", "Bekannte technische Abhaengigkeiten"):
        assert je_angabe.get(angabe) == "als Informationsluecke markiert", angabe
    # Was die Company-Antraege haben, wird auch erkannt:
    assert "Business Case" in erg.gefunden and "Erwartete Kosten" in erg.gefunden


def test_ohne_ueberschriften_fehlt_alles(tmp_path):
    f = tmp_path / "leer.md"
    f.write_text("# Antrag\n\nNur Prosa ohne Gliederung. Projektname steht im Text, nicht im Kopf.\n",
                 encoding="utf-8")
    erg = gate.pruefe([f])
    assert not erg.bestanden and len(erg.fehlend) == 15
    assert all(x["grund"] == "keine Ueberschrift" for x in erg.fehlend)


def test_nummerierung_und_ebene_sind_egal(tmp_path):
    f = tmp_path / "a.md"
    f.write_text(
        "---\ntitel: x\n---\n# Vorhaben\n## 1. Projektname\nX\n### 2) Beschreibung\nY\n## Zielsetzung\nZ\n"
        "## 4 Fachlicher und organisatorischer Nutzen\nN\n## Betroffene Geschäftsprozesse\nP\n"
        "## Betroffene Organisationseinheiten\nO\n## Business Case\nB\n## Erwartete Kosten\nK\n"
        "## Erwarteter wirtschaftlicher Nutzen\nW\n## Geplante Laufzeit\nL\n"
        "## Bekannte technische Abhängigkeiten\nT\n## Bekannte organisatorische Abhängigkeiten\nA\n"
        "## Risikoanalyse\nR\n## Begründung\nG\n## Relevante Anbieterinformationen\nI\n",
        encoding="utf-8")
    erg = gate.pruefe([f])
    assert erg.bestanden, erg.fehlend


def test_markierte_luecke_zaehlt_nicht_als_vorhanden(tmp_path):
    f = tmp_path / "b.md"
    f.write_text("## Risikoanalyse\n\n*Nicht enthalten — Informationslücke.*\n", encoding="utf-8")
    erg = gate.pruefe([f])
    r = next(x for x in erg.fehlend if x["angabe"] == "Risikoanalyse")
    assert r["grund"] == "als Informationsluecke markiert"


def test_informationsanforderung_struktur():
    erg = gate.pruefe([COMPANY[0]])
    a = gate.informationsanforderung(erg, "2026-09-06T00:00:00+00:00")
    assert a["status"] == "INFORMATIONSANFORDERUNG"
    assert a["fehlende_angaben"] == erg.fehlend and a["dateien"] == erg.dateien


def test_cli_exitcodes(capsys):
    assert gate.main([str(p) for p in EISENACH]) == 0
    assert gate.main([str(COMPANY[0])]) == 3
    assert "NICHT BESTANDEN" in capsys.readouterr().out
