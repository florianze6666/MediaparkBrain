"""T4, Teil Wissensbasis: Z2 (Absturz gegen Nulltreffer), Z13 (Geraet und Rueckfall),
Cache-Kennzeichnung, typisierte Anfragen und der Initialteil nach der Diagnose des Laufs
vom 06.09.2026 05:12 (`.test/1b_diagnose.md`). Keine API, kein qmd-Subprozess.
"""

from __future__ import annotations

import pytest

import treiber
from conftest import EISENACH, FRAGE_GLASWERK, FakeClient, FakeQmd


def lauf_dir(tmp_path):
    return tmp_path / "laeufe" / "t4w"


# ---------------------------------------------------------------------------
# Z2: werte_qmd_ausgabe unterscheidet Absturz, Nulltreffer und ungerankt
# ---------------------------------------------------------------------------

STDERR_ABSTURZ = ("Reranking 40 chunks...D:\\a\\node-llama-cpp\\node-llama-cpp\\llama\\llama.cpp\\ggml\\src"
                  "\\ggml-cuda\\ggml-cuda.cu:106: CUDA error\n")
STDERR_CACHE = "Reranking 40 chunks... (4ms)\n"
STDERR_UNGERANKT = ("Reranker unavailable — skipping reranking (context size of 4096 is too large for "
                    "the available VRAM).\n")
JSON_TREFFER = '[{"file":"qmd://intern/a/b.md","score":1.0,"snippet":"x"}]'


def test_z2_exitcode_0xc0000409_ist_absturz():
    with pytest.raises(treiber.WissensbasisFehler, match="0xc0000409"):
        treiber.werte_qmd_ausgabe(3221226505, "", STDERR_ABSTURZ)


def test_z2_cuda_error_bei_exitcode_null_ist_absturz():
    with pytest.raises(treiber.WissensbasisFehler, match="Laufzeitfehler"):
        treiber.werte_qmd_ausgabe(0, "", STDERR_ABSTURZ)


def test_z2_leeres_stdout_bei_exitcode_null_ist_nulltreffer():
    assert treiber.werte_qmd_ausgabe(0, "", STDERR_CACHE) == ([], False)


def test_z2_reranker_ausgelassen_ist_gueltig_aber_ungerankt():
    treffer, ungerankt = treiber.werte_qmd_ausgabe(0, JSON_TREFFER, STDERR_UNGERANKT)
    assert ungerankt is True and treffer[0]["file"] == "qmd://intern/a/b.md"
    treffer, ungerankt = treiber.werte_qmd_ausgabe(0, JSON_TREFFER, STDERR_CACHE)
    assert ungerankt is False and len(treffer) == 1


def test_z2_unlesbare_ausgabe_ist_fehler():
    with pytest.raises(treiber.WissensbasisFehler, match="keine JSON"):
        treiber.werte_qmd_ausgabe(0, "Fehlertext ohne Klammer", "")
    with pytest.raises(treiber.WissensbasisFehler, match="JSON unlesbar"):
        treiber.werte_qmd_ausgabe(0, "[{kaputt", "")


# ---------------------------------------------------------------------------
# Z13: Geraet
# ---------------------------------------------------------------------------


def test_z13_vorgabe_vulkan_und_ueberschreibung(monkeypatch):
    monkeypatch.setattr(treiber, "QMD_GERAET", "vulkan")
    e = treiber.qmd_env()
    assert e["QMD_LLAMA_GPU"] == "vulkan"
    assert e["QMD_CONFIG_DIR"].endswith(".qmd") and e["XDG_CACHE_HOME"].endswith(".cache")
    assert treiber.qmd_env("cuda")["QMD_LLAMA_GPU"] == "cuda"
    monkeypatch.setenv("QMD_LLAMA_GPU", "metal")
    assert "QMD_LLAMA_GPU" not in treiber.qmd_env("auto")       # auto: qmd waehlt selbst


def test_z13_rueckfall_ist_letzter_versuch_und_ungerankt():
    qmd = FakeQmd(fehler_anzahl=2)
    erg, versuch, rueckfall = treiber.abfrage_mit_wiederholung(qmd, FRAGE_GLASWERK, ["intern"], 8)
    assert versuch == 3 and rueckfall is True
    assert erg.ungerankt is True and erg.rerank is False and erg.geraet == treiber.QMD_RUECKFALL_GERAET
    assert qmd.optionen == [{}, {}, {"geraet": "cuda", "rerank": False}]


def test_z13_erfolg_im_ersten_versuch_kein_rueckfall():
    qmd = FakeQmd()
    erg, versuch, rueckfall = treiber.abfrage_mit_wiederholung(qmd, FRAGE_GLASWERK, ["intern"], 8)
    assert (versuch, rueckfall, erg.ungerankt) == (1, False, False)
    assert len(erg.treffer) == 7


def test_z13_alle_versuche_scheitern():
    qmd = FakeQmd(immer_fehler=True)
    with pytest.raises(treiber.WissensbasisFehler, match="nach 3 Versuchen"):
        treiber.abfrage_mit_wiederholung(qmd, FRAGE_GLASWERK, ["intern"], 8)
    assert len(qmd.aufrufe) == 3


def test_ohne_wiederholung_kein_rueckfall():
    qmd = FakeQmd(fehler_anzahl=1)
    with pytest.raises(treiber.WissensbasisFehler, match="nach 1 Versuchen"):
        treiber.abfrage_mit_wiederholung(qmd, FRAGE_GLASWERK, ["intern"], 8, wiederholungen=0)


def test_qmd_kommando_meidet_den_batch_wrapper(monkeypatch):
    # Mit node wird die qmd-JavaScript-Datei direkt gerufen: cmd.exe wuerde ein Argument mit
    # Zeilenumbruch (lex:/vec:-Dokument) zerlegen und --format json samt Collections verlieren.
    monkeypatch.setattr(treiber.shutil, "which", lambda name: r"C:\node\node.exe" if name == "node" else None)
    cmd = treiber.qmd_kommando()
    assert cmd[0] == r"C:\node\node.exe" and len(cmd) == 2
    assert cmd[1].endswith(("qmd", "qmd.js")) and "@tobilu" in cmd[1] and not cmd[1].endswith(".cmd")
    monkeypatch.setattr(treiber.shutil, "which", lambda name: None)
    assert treiber.qmd_kommando() == [str(treiber.qmd_exe())]


# ---------------------------------------------------------------------------
# Cache und Dauer im Protokoll
# ---------------------------------------------------------------------------


def test_protokoll_traegt_dauer_cache_geraet_und_rerank(tmp_path):
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4w", client=FakeClient(), qmd_query=FakeQmd())
    a = erg.protokoll["rag_abfragen"][0]
    assert a["dauer_s"] == 0.0 and a["aus_cache"] is True      # die Faelschung antwortet sofort
    assert a["rueckfall"] is False and a["ungerankt"] is False and a["rerank"] is True
    assert a["typisiert"] is False and "stderr" not in a
    assert erg.protokoll["abfragen_aus_cache"] == 1
    assert erg.protokoll["qmd"]["geraet"] == treiber.QMD_GERAET
    assert erg.protokoll["qmd"]["cache_schwelle_s"] == 10.0


def test_abfrageergebnis_cache_schwelle():
    assert treiber.AbfrageErgebnis(treffer=[], dauer_s=6.0).aus_cache is True
    assert treiber.AbfrageErgebnis(treffer=[], dauer_s=45.0).aus_cache is False


# ---------------------------------------------------------------------------
# Typisierte Anfragen (lex:/vec:)
# ---------------------------------------------------------------------------


def test_typisiertes_dokument_kennungen_jahre_eigennamen():
    d = treiber.typisiertes_dokument(
        'Was ist beim Projekt "Glaswerk Nord" 2013 passiert, als POL-VTR-001 noch nicht galt?')
    zeilen = d.split("\n")
    assert len(zeilen) == 2 and zeilen[0].startswith("lex: ") and zeilen[1].startswith("vec: ")
    lex = zeilen[0][5:].split()
    assert "POL-VTR-001" in lex and "2013" in lex and "Glaswerk" in lex
    assert "Was" not in lex and "Projekt" not in lex          # kurz oder Stoppliste
    assert '"' not in d and "'" not in d                       # qmd verlangt balancierte Quotes
    assert zeilen[1] == "vec: Was ist beim Projekt Glaswerk Nord 2013 passiert, als POL-VTR-001 noch nicht galt?"


def test_typisiertes_dokument_nur_vec_ohne_lexterme():
    d = treiber.typisiertes_dokument("Welche Kosten gibt es?")
    assert d == "vec: Welche Kosten gibt es?"


def test_typisiert_option_wird_durchgereicht(tmp_path):
    qmd = FakeQmd()
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4w", client=FakeClient(),
                                   qmd_query=qmd, typisiert=True)
    assert qmd.optionen[0] == {"typisiert": True}
    assert erg.protokoll["qmd"]["typisiert"] is True
    assert erg.protokoll["rag_abfragen"][0]["typisiert"] is True
    # Vorgabe: nichts durchreichen, die Wissensbasis-Funktion entscheidet selbst
    qmd2 = FakeQmd()
    treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4w2", client=FakeClient(), qmd_query=qmd2)
    assert qmd2.optionen[0] == {}


def test_typisiert_auch_im_rueckfall(tmp_path):
    qmd = FakeQmd(fehler_anzahl=2)
    treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4w", client=FakeClient(),
                             qmd_query=qmd, typisiert=True)
    assert qmd.optionen[2] == {"geraet": "cuda", "rerank": False, "typisiert": True}


# ---------------------------------------------------------------------------
# Initialteil und Werkzeugbeschreibung
# ---------------------------------------------------------------------------


def test_initialteil_sagt_was_drin_ist_und_was_nicht():
    t = treiber.INITIALTEIL
    assert "218 Dokumente" in t and "2011 bis" in t and "neun Ablageorten" in t
    assert "Was sie nicht enthaelt" in t and "kuenftiger Jahre" in t and "nichts nach 2025" in t
    assert "Zuerst der erinnerte Fall, mit Namen und Jahr" in t
    assert "vier Runden" in t and "bis zu drei Fragen" in t
    assert "Keine Treffer" in t and "nicht um" in t
    assert "Wissensbasis nicht erreichbar" in t and "technischer Ausfall" in t
    assert "anders formulierten Frage noch einmal" not in t      # die alte Regel 6 ist weg


def test_werkzeugbeschreibung_nennt_beide_antworten():
    d = treiber.TOOLS[0]["description"]
    assert "Keine Treffer" in d and "Wissensbasis nicht erreichbar" in d


def test_prompt_version_haengt_am_initialteil(monkeypatch):
    v1 = treiber.prompt_version("cfo")
    monkeypatch.setattr(treiber, "INITIALTEIL", treiber.INITIALTEIL + "\nZusatz")
    assert treiber.prompt_version("cfo") != v1
