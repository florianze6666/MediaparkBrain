"""Tests zu suche.py (Plan 09, T-S1, T-S2, T-N1, T-N2).

Ohne Modell und ohne API. Die Tests gegen den echten Index werden uebersprungen,
wenn er fehlt; der Test der Bruecke wird uebersprungen, wenn kein Modell da ist
oder wenn er nicht ausdruecklich angefordert wird -- er belegt die Grafikkarte,
und in dieser Sitzung darf immer nur ein Prozess das Modell laden.

Bruecke einschalten mit:  QMD_TEST_BRUECKE=1 uv run pytest agenten/tests -q
"""
from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

import numpy as np
import pytest

AGENTEN_DIR = Path(__file__).resolve().parent.parent
if str(AGENTEN_DIR) not in sys.path:
    sys.path.insert(0, str(AGENTEN_DIR))

import suche  # noqa: E402


# ---------------------------------------------------------------------------
# Hilfen
# ---------------------------------------------------------------------------


def treffer(quelle: str, score: float, collection: str = "intern", chunk: int = 0) -> dict:
    return {"quelle": quelle, "collection": collection, "titel": quelle,
            "chunk": chunk, "pos": 0, "score": score}


def einheitsvektoren(zeilen: list[list[float]]) -> np.ndarray:
    v = np.array(zeilen, dtype=np.float32)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


# ---------------------------------------------------------------------------
# T-S1: Pfad-Dedup
# ---------------------------------------------------------------------------


def test_ts1_chunks_derselben_datei_werden_zusammengefasst():
    """Drei Chunks einer Datei ergeben ein Dokument, und zwar mit dem besten Score."""
    liste = [treffer("a.md", 0.9, chunk=0),
             treffer("a.md", 0.7, chunk=1),
             treffer("a.md", 0.5, chunk=2),
             treffer("b.md", 0.6)]
    ergebnis = suche.dedup_und_top_k([liste], bereits_vorhanden=[], ziel_anzahl=4)

    assert [t["quelle"] for t in ergebnis] == ["a.md", "b.md"]
    assert ergebnis[0]["score"] == pytest.approx(0.9)


def test_ts1_bereits_vorhandene_pfade_werden_uebersprungen():
    """Die Prae-Dokumente aus Abschnitt A stehen schon im Kontext."""
    liste = [treffer("prae.md", 0.99), treffer("neu.md", 0.4)]
    ergebnis = suche.dedup_und_top_k([liste], bereits_vorhanden=["prae.md"], ziel_anzahl=4)

    assert [t["quelle"] for t in ergebnis] == ["neu.md"]


def test_ts1_dieselbe_datei_aus_zwei_fragen_zaehlt_einmal():
    frage_a = [treffer("gemeinsam.md", 0.9), treffer("nur_a.md", 0.8)]
    frage_b = [treffer("gemeinsam.md", 0.85), treffer("nur_b.md", 0.7)]
    ergebnis = suche.dedup_und_top_k([frage_a, frage_b], [], ziel_anzahl=4)

    quellen = [t["quelle"] for t in ergebnis]
    assert quellen.count("gemeinsam.md") == 1
    assert set(quellen) == {"gemeinsam.md", "nur_a.md", "nur_b.md"}


# ---------------------------------------------------------------------------
# T-S2: Top-K und Reihum
# ---------------------------------------------------------------------------


def test_ts2_liefert_hoechstens_die_zielanzahl():
    listen = [[treffer(f"f{f}_{i}.md", 1.0 - i / 10) for i in range(8)] for f in range(3)]
    ergebnis = suche.dedup_und_top_k(listen, [], ziel_anzahl=4)

    assert len(ergebnis) == 4
    assert len({t["quelle"] for t in ergebnis}) == 4


def test_ts2_reihum_jede_frage_kommt_zum_zug():
    """Auch wenn eine Frage durchweg hoehere Werte liefert, ist jede Frage vertreten.

    Das ist der Kern der Reihum-Auswahl: sonst fuellt eine einzige Frage den Deckel,
    genau der Fehler, an dem der CFO-Lauf am 06.09.2026 null Golden-Treffer hatte.
    """
    stark = [treffer(f"stark{i}.md", 0.99 - i / 100) for i in range(8)]
    schwach = [treffer(f"schwach{i}.md", 0.30 - i / 100) for i in range(8)]
    ergebnis = suche.dedup_und_top_k([stark, schwach], [], ziel_anzahl=4)

    quellen = [t["quelle"] for t in ergebnis]
    assert any(q.startswith("stark") for q in quellen)
    assert any(q.startswith("schwach") for q in quellen), (
        "Die schwaechere Frage wurde vollstaendig verdraengt: Reihum greift nicht."
    )


def test_ts2_leere_eingabe_ergibt_leere_auswahl():
    assert suche.dedup_und_top_k([], [], ziel_anzahl=4) == []
    assert suche.dedup_und_top_k([[], []], [], ziel_anzahl=4) == []


# ---------------------------------------------------------------------------
# T-N2: Rechte
# ---------------------------------------------------------------------------


def test_tn2_nur_erlaubte_collections_kommen_zurueck():
    vektoren = einheitsvektoren([[1, 0], [0.99, 0.1], [0.98, 0.2], [1, 0]])
    metadaten = [
        {"quelle": "i.md", "collection": "intern", "titel": "i", "chunk": 0, "pos": 0},
        {"quelle": "b.md", "collection": "br", "titel": "b", "chunk": 0, "pos": 0},
        {"quelle": "c.md", "collection": "clevel", "titel": "c", "chunk": 0, "pos": 0},
        {"quelle": "a.md", "collection": "antraege", "titel": "a", "chunk": 0, "pos": 0},
    ]
    frage = np.array([1.0, 0.0], dtype=np.float32)

    nur_intern = suche.suche_vektoriell(frage, ["intern"], vektoren, metadaten, top_n=8)
    assert {t["collection"] for t in nur_intern} == {"intern"}

    cfo = suche.suche_vektoriell(frage, ["intern", "clevel"], vektoren, metadaten, top_n=8)
    assert {t["collection"] for t in cfo} == {"intern", "clevel"}
    assert all(t["collection"] != "br" for t in cfo), "C-Level darf den Betriebsrat nicht sehen."

    br = suche.suche_vektoriell(frage, ["intern", "br"], vektoren, metadaten, top_n=8)
    assert all(t["collection"] != "clevel" for t in br), "Betriebsrat darf C-Level nicht sehen."


def test_tn2_leere_collectionliste_liefert_nichts_statt_alles():
    """Der gefaehrliche Fall: ein vergessenes Argument darf nie den Vollzugriff oeffnen."""
    vektoren = einheitsvektoren([[1, 0], [0, 1]])
    metadaten = [
        {"quelle": "i.md", "collection": "intern", "titel": "i", "chunk": 0, "pos": 0},
        {"quelle": "c.md", "collection": "clevel", "titel": "c", "chunk": 0, "pos": 0},
    ]
    assert suche.suche_vektoriell(np.array([1.0, 0.0], dtype=np.float32),
                                  [], vektoren, metadaten) == []


def test_suche_sortiert_absteigend_und_haelt_top_n():
    vektoren = einheitsvektoren([[1, 0], [0.8, 0.6], [0.6, 0.8], [0, 1]])
    metadaten = [
        {"quelle": f"{i}.md", "collection": "intern", "titel": str(i), "chunk": 0, "pos": 0}
        for i in range(4)
    ]
    ergebnis = suche.suche_vektoriell(np.array([1.0, 0.0], dtype=np.float32),
                                      ["intern"], vektoren, metadaten, top_n=2)
    assert len(ergebnis) == 2
    assert ergebnis[0]["score"] >= ergebnis[1]["score"]
    assert ergebnis[0]["quelle"] == "0.md"


def test_unpassende_metadaten_werfen():
    vektoren = einheitsvektoren([[1, 0], [0, 1]])
    with pytest.raises(suche.SucheFehler):
        suche.suche_vektoriell(np.array([1.0, 0.0], dtype=np.float32),
                               ["intern"], vektoren, [{"collection": "intern"}])


# ---------------------------------------------------------------------------
# Pfadabbildung und Dokumente
# ---------------------------------------------------------------------------


def test_wurzelpraefix_der_sicht_wird_entfernt():
    """build_view.py legt Dateien ohne Ablageort nach `_wurzel/`; corpus/ kennt das nicht."""
    assert suche._als_quelle("_wurzel/ATTRIBUTION.md") == "ATTRIBUTION.md"
    assert suche._als_quelle("br_ablage/2020/x.md") == "br_ablage/2020/x.md"
    assert suche._als_quelle("br_ablage\\2020\\x.md") == "br_ablage/2020/x.md"


def test_unbekanntes_dokument_wirft_klar():
    with pytest.raises(suche.SucheFehler):
        suche.lies_dokument("gibt/es/nicht.md")


# ---------------------------------------------------------------------------
# Index (uebersprungen, wenn er fehlt)
# ---------------------------------------------------------------------------

ohne_index = pytest.mark.skipif(
    not suche.INDEX_SQLITE.exists(), reason="kein Index vorhanden"
)


@ohne_index
def test_tn1_index_laedt_normiert_und_vollstaendig():
    vektoren, metadaten = suche.lade_index_vektoren()

    assert vektoren.shape[0] == len(metadaten)
    assert vektoren.shape[1] == suche.DIMENSIONEN
    normen = np.linalg.norm(vektoren, axis=1)
    assert np.allclose(normen, 1.0, atol=1e-4), (
        "Der Speicher haelt die Vektoren unnormiert; lade_index_vektoren muss normieren."
    )
    assert {m["collection"] for m in metadaten} >= {"intern", "br", "clevel"}


@ohne_index
def test_index_quellen_zeigen_auf_lesbare_dateien():
    _, metadaten = suche.lade_index_vektoren()
    intern = [m for m in metadaten if m["collection"] == "intern"][:20]
    for m in intern:
        assert suche.lies_dokument(m["quelle"]), m["quelle"]


@ohne_index
def test_modell_aus_index_passt_zu_den_dimensionen():
    """Die Bruecke muss dasselbe Modell laden, mit dem der Index gebaut wurde.

    Ohne diese Bindung faellt qmd auf embeddinggemma mit 768 Dimensionen zurueck,
    und Anfrage und Index liegen in verschiedenen Raeumen.
    """
    modell = suche.modell_aus_index()
    assert modell
    if "nemotron" in modell.lower():
        assert suche.DIMENSIONEN == 2048


# ---------------------------------------------------------------------------
# Bruecke (nur auf Anforderung, belegt die Grafikkarte)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    os.environ.get("QMD_TEST_BRUECKE", "") not in ("1", "true", "ja"),
    reason="Bruecke laedt das Modell; nur mit QMD_TEST_BRUECKE=1",
)
def test_bruecke_startet_bettet_ein_und_schliesst():
    bruecke = suche.bruecke_start()
    try:
        antwort = bruecke.ping()
        assert antwort["ok"] is True

        vektoren = bruecke.embed(["Eine kurze Testfrage.", "Eine zweite."])
        assert len(vektoren) == 2
        assert len(vektoren[0]) == suche.DIMENSIONEN
    finally:
        bruecke.schliessen()

    # Nach dem Schliessen sind weitere Aufrufe ein klarer Fehler, keine Haengepartie.
    with pytest.raises(suche.SucheFehler):
        bruecke.embed(["danach"])


def test_bruecke_ohne_skript_wirft_klar(monkeypatch, tmp_path):
    monkeypatch.setattr(suche, "BRUECKE_SKRIPT", tmp_path / "fehlt.mjs")
    with pytest.raises(suche.SucheFehler):
        suche.bruecke_start()


def test_toter_prozess_ergibt_fehler_statt_haenger():
    """Ein abgestuerzter Node-Prozess darf nicht zu einem haengenden Aufruf fuehren."""

    class ToterProzess:
        returncode = 1
        stdin = None
        stdout = None

        def poll(self):
            return 1

    bruecke = suche.Bruecke(ToterProzess())
    with pytest.raises(suche.SucheFehler, match="beendet"):
        bruecke.embed(["egal"])
    bruecke.schliessen()   # muss ohne Ausnahme durchlaufen


# ---------------------------------------------------------------------------
# Vorbedingungen
# ---------------------------------------------------------------------------


def test_vorbedingungen_melden_fehlenden_index(monkeypatch, tmp_path):
    monkeypatch.setattr(suche, "INDEX_SQLITE", tmp_path / "keiner.sqlite")
    ergebnis = suche.vorbedingungen()
    assert ergebnis["erfuellt"] is False
    assert any("Index fehlt" in b for b in ergebnis["befunde"])


def test_vorbedingungen_melden_fehlenden_schluessel(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    ergebnis = suche.vorbedingungen()
    assert any("ANTHROPIC_API_KEY" in b for b in ergebnis["befunde"])


def test_mehrere_modelle_im_index_werfen(tmp_path):
    """Vektoren aus zwei Modellen sind nicht vergleichbar; das muss laut auffallen."""
    pfad = tmp_path / "index.sqlite"
    verbindung = sqlite3.connect(pfad)
    verbindung.execute("create table content_vectors (hash text, seq int, model text)")
    verbindung.executemany(
        "insert into content_vectors values (?,?,?)",
        [("a", 0, "modell-eins"), ("b", 0, "modell-zwei")],
    )
    verbindung.commit()
    verbindung.close()

    with pytest.raises(suche.SucheFehler, match="mehreren Modellen"):
        suche.modell_aus_index(pfad)
