"""T1: Kapitel-17-Schema, 17.5-Validierung und Kapitel-16-Aggregation."""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from schema import FELDER, KONFLIKT_ABSTAND, Zeile, aggregiere, validiere_zeilen


def z(rolle, status="BEWERTET", score=5, **kw):
    return Zeile(rolle=rolle, status=status, score=score, begruendung=kw.pop("begruendung", "Begruendung."), **kw)


def test_information_fehlt_mit_score_faellt():
    with pytest.raises(ValidationError, match="17.2 Regel 1"):
        z("cfo", "INFORMATION FEHLT", 5)


def test_bewertet_ohne_score_faellt():
    with pytest.raises(ValidationError, match="17.2 Regel 1"):
        z("cfo", "BEWERTET", None)


def test_null_ist_gueltiger_score():
    assert z("cfo", score=0).score == 0


def test_information_fehlt_mit_null_ist_gueltig():
    x = z("it", "INFORMATION FEHLT", None, fehlende_informationen=["Hosting-Modell"])
    assert x.score is None and x.fehlende_informationen == ["Hosting-Modell"]


@pytest.mark.parametrize("wert", [11, -1, 3.5, True])
def test_ungueltige_scores_fallen(wert):
    with pytest.raises(ValidationError):
        z("ceo", score=wert)


def test_integraler_float_wird_ganzzahl():
    assert z("ceo", score=7.0).score == 7


def test_leere_begruendung_faellt():
    with pytest.raises(ValidationError, match="Kapitel 8"):
        z("cfo", begruendung="   ")


def test_unbekannte_rolle_faellt():
    with pytest.raises(ValidationError):
        z("hr")


def test_extra_feld_faellt_17_2_regel_3():
    with pytest.raises(ValidationError):
        Zeile(rolle="cfo", status="BEWERTET", score=4, begruendung="x", essay="nicht erlaubt")


def test_jsonl_hat_genau_acht_felder_in_reihenfolge():
    line = z("betriebsrat", score=2, quellen=["corpus/a.md"]).als_jsonl()
    d = json.loads(line)
    assert tuple(d.keys()) == FELDER
    assert len(d) == 8
    assert "\n" not in line


def test_validiere_zeilen_doppelte_rolle_und_kaputtes_json():
    zeilen = [
        z("cfo", score=3).als_jsonl(),
        z("cfo", score=4).als_jsonl(),
        "{nicht json",
        json.dumps({"rolle": "it", "status": "BEWERTET", "score": None, "begruendung": "x",
                    "fehlende_informationen": []}),
        z("ceo", score=8).als_jsonl(),
    ]
    gueltig, fehler = validiere_zeilen(zeilen)
    assert [g.rolle for g in gueltig] == ["cfo", "ceo"]
    assert len(fehler) == 3
    assert any("mehr als einmal" in f.fehler for f in fehler)
    assert any("JSON" in f.fehler for f in fehler)
    assert any(f.rolle == "it" and "17.2" in f.fehler for f in fehler)


def test_aggregation_null_zeile_rechnet_ueber_drei():
    gueltig = [z("betriebsrat", score=10), z("cfo", score=8),
               z("it", "INFORMATION FEHLT", None, fehlende_informationen=["Hosting", "Schnittstellen"]),
               z("ceo", score=6)]
    s = aggregiere(gueltig, [], "L1")
    assert s.gesamtscore == 8.0
    assert s.anzahl_bewertet == 3 and s.anzahl_gueltige_zeilen == 4
    assert s.gesamtstatus == "BEWERTET"
    assert s.fehlende_informationen == ["it: Hosting", "it: Schnittstellen"]
    assert [r.rolle for r in s.rollen] == ["betriebsrat", "cfo", "it", "ceo"]


def test_aggregation_alle_ohne_score_ergibt_kein_score():
    gueltig = [z(r, "INFORMATION FEHLT", None, fehlende_informationen=[f"{r}-luecke"])
               for r in ("betriebsrat", "cfo", "it", "ceo")]
    s = aggregiere(gueltig, [], "L2")
    assert s.gesamtscore is None and s.gesamtstatus == "INFORMATION FEHLT"
    assert s.anzahl_bewertet == 0 and len(s.fehlende_informationen) == 4


def test_kein_score_ist_nicht_null_und_null_ist_gueltig():
    s = aggregiere([z("cfo", score=0), z("ceo", score=10),
                    z("it", "INFORMATION FEHLT", None)], [], "L3")
    assert s.gesamtscore == 5.0
    assert s.spanne == 10
    assert len(s.konflikte) == 1 and s.konflikte[0].abstand == 10


def test_rundung_auf_eine_dezimalstelle():
    s = aggregiere([z("betriebsrat", score=9), z("cfo", score=7), z("it", score=8), z("ceo", score=6)], [], "L4")
    assert s.gesamtscore == 7.5 and s.spanne == 3 and s.konflikte == []


def test_konflikt_ab_abstand_vier():
    assert KONFLIKT_ABSTAND == 4
    s = aggregiere([z("cfo", score=3), z("ceo", score=7), z("it", score=4)], [], "L5")
    paare = {(k.rolle_a, k.rolle_b) for k in s.konflikte}
    assert paare == {("cfo", "ceo")}


def test_technische_fehler_landen_in_zusammenfassung():
    s = aggregiere([z("cfo", score=3)], [], "L6", technische_fehler=[{"rolle": "it", "fehler": "refusal"}])
    assert s.technische_fehler[0]["rolle"] == "it"
    assert json.loads(s.model_dump_json())["gesamtscore"] == 3.0
