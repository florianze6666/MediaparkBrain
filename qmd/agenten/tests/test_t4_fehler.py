"""T4: Fehlerinjektion mit gefaelschtem Client und gefaelschter Wissensbasis.

Geprueft werden Z2 (Wiederholung), Z3 (keine Treffer), Z4 (max_tokens, refusal),
Z5/Z12 (Kontextauswahl), Z6 (17.5 im Treiber), Z9 (Orchestrator laeuft weiter) und die
Ablage aus 08 Abschnitt 5. Keine API, kein qmd.
"""

from __future__ import annotations

import json

# Diese Datei prueft den Treiber mit Werkzeugrunden und den SEQUENZIELLEN Orchestrator.
# Beide sind am 06.09.2026 abgeloest worden (Plan 09); der sequenzielle Orchestrator liegt
# seither unter orchestrator_sequenziell.py, der parallele hat seinen Test in
# tests/test_orchestrator.py. Der Pruefgegenstand ist unveraendert, nur sein Name.
import orchestrator_sequenziell as orchestrator
import treiber
from conftest import (ABLENKER, COMPANY, EISENACH, FRAGE_GLASWERK, GOLDEN, STANDARD_HITS, FakeClient,
                      FakeQmd, felder, hit)
from schema import FELDER


def lauf_dir(tmp_path):
    return tmp_path / "laeufe" / "t4"


# ---------------------------------------------------------------------------
# Happy Path: Zeile und Protokoll
# ---------------------------------------------------------------------------


def test_happy_path_schreibt_zeile_und_protokoll(tmp_path):
    client, qmd = FakeClient(), FakeQmd()
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4", client=client, qmd_query=qmd)
    assert erg.fehler is None, erg.fehler
    zeile = json.loads((lauf_dir(tmp_path) / "cfo.jsonl").read_text(encoding="utf-8"))
    assert tuple(zeile.keys()) == FELDER
    assert zeile["rolle"] == "cfo" and zeile["score"] == 3 and zeile["status"] == "BEWERTET"
    # Zitat aus document_index 0; nach Z12 steht dort ein Glaswerk-Dokument
    assert zeile["quellen"] == [f"corpus/{erg.protokoll['dokumente_im_kontext'][0]['datei']}"]
    assert zeile["quellen"][0].split("corpus/")[1] in GOLDEN
    prot = json.loads((lauf_dir(tmp_path) / "cfo.protokoll.json").read_text(encoding="utf-8"))
    for k in ("essay", "zitate", "rag_abfragen", "prompt_version", "modell", "zeitpunkt", "lauf_id", "collections"):
        assert prot[k], k
    assert prot["technischer_fehler"] is None
    assert prot["collections"] == ["intern", "clevel"]
    assert qmd.aufrufe[0][1] == ["intern", "clevel"]
    # Z11: Systemprompt mit cache_control in jedem Zug
    for kw in client.messages.stream_aufrufe + client.messages.parse_aufrufe:
        assert kw["system"][0]["cache_control"] == {"type": "ephemeral"}
    # Zug B ohne Dokumente, mit dem Essay als Assistant-Nachricht
    zug_b = client.messages.parse_aufrufe[0]
    assert zug_b["messages"][1]["role"] == "assistant" and "Glaswerk" in zug_b["messages"][1]["content"]
    assert zug_b["output_format"].__name__ == "Bewertungsfelder"


def test_score_abweichung_zwischen_essay_und_feld_wird_protokolliert(tmp_path):
    client = FakeClient(essay_text="**Score:** 5/10\nBegruendung: verloren gegangen ist die Marge.")
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4", client=client, qmd_query=FakeQmd())
    assert erg.zeile.score == 3  # das Feld gilt
    assert erg.protokoll["score_abweichung"] == {"essay": 5, "feld": 3, "regel": "das Feld gilt (Kapitel 17)"}


# ---------------------------------------------------------------------------
# Z2, Z3: Wissensbasis
# ---------------------------------------------------------------------------


def test_z2_zweimal_fehler_dann_erfolg_ueber_rueckfall(tmp_path):
    qmd = FakeQmd(fehler_anzahl=2)
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4", client=FakeClient(), qmd_query=qmd)
    assert erg.fehler is None
    abfrage = erg.protokoll["rag_abfragen"][0]
    assert abfrage["versuche"] == 3
    assert len(qmd.aufrufe) == 3
    # Z13: der dritte Versuch ist der Rueckfall auf CUDA ohne Reranking
    assert qmd.optionen[0] == {} and qmd.optionen[1] == {}
    assert qmd.optionen[2] == {"geraet": treiber.QMD_RUECKFALL_GERAET, "rerank": False}
    assert abfrage["rueckfall"] is True and abfrage["ungerankt"] is True and abfrage["rerank"] is False
    assert abfrage["geraet"] == treiber.QMD_RUECKFALL_GERAET


def test_z2_z3_wissensbasis_unerreichbar_ergibt_technischen_fehler(tmp_path):
    client, qmd = FakeClient(), FakeQmd(immer_fehler=True)
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4", client=client, qmd_query=qmd)
    assert erg.zeile is None and "keine_treffer" in erg.fehler
    assert len(qmd.aufrufe) == 3  # ein Versuch plus zwei Wiederholungen
    abfrage = erg.protokoll["rag_abfragen"][0]
    assert "nach 3 Versuchen" in abfrage["fehler"]
    # der Agent hat is_error gesehen, kein "Keine Treffer"
    # messages ist dieselbe Liste ueber alle Zuege; Index 2 ist die Nutzer-Nachricht mit den tool_results
    tool_results = client.messages.stream_aufrufe[1]["messages"][2]["content"]
    assert tool_results[0]["is_error"] is True and "nicht erreichbar" in tool_results[0]["content"]
    assert not (lauf_dir(tmp_path) / "cfo.jsonl").exists()
    assert json.loads((lauf_dir(tmp_path) / "cfo.protokoll.json").read_text(encoding="utf-8"))["technischer_fehler"]["art"] == "keine_treffer"


def test_z3_leere_treffer_ohne_absturz_ist_auch_fehler(tmp_path):
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4", client=FakeClient(), qmd_query=FakeQmd(leer=True))
    assert erg.zeile is None and erg.protokoll["technischer_fehler"]["art"] == "keine_treffer"


def test_fr_04_agent_ohne_abfrage_ist_fehler(tmp_path):
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4", client=FakeClient(fragen=[]), qmd_query=FakeQmd())
    assert erg.protokoll["technischer_fehler"]["art"] == "keine_abfrage"


# ---------------------------------------------------------------------------
# Z4: max_tokens und refusal
# ---------------------------------------------------------------------------


def test_z4_max_tokens_genau_eine_wiederholung_dann_erfolg(tmp_path):
    client = FakeClient(zug_a_stops=["max_tokens", "end_turn"])
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4", client=client, qmd_query=FakeQmd())
    assert erg.fehler is None
    assert erg.protokoll["stop_reasons"]["zug_a_1"] == "max_tokens"
    assert erg.protokoll["stop_reasons"]["zug_a_2"] == "end_turn"
    zug_a = [kw for kw in client.messages.stream_aufrufe if not kw.get("tools")]
    assert len(zug_a) == 2
    assert "kuerzer" in zug_a[1]["messages"][-1]["content"][-1]["text"]


def test_z4_max_tokens_zweimal_technischer_fehler(tmp_path):
    client = FakeClient(zug_a_stops=["max_tokens", "max_tokens"])
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4", client=client, qmd_query=FakeQmd())
    assert erg.zeile is None and erg.protokoll["technischer_fehler"]["art"] == "max_tokens"
    assert len([kw for kw in client.messages.stream_aufrufe if not kw.get("tools")]) == 2
    assert len(client.messages.parse_aufrufe) == 0
    assert not (lauf_dir(tmp_path) / "cfo.jsonl").exists()


def test_z4_refusal_in_zug_a_sofort_fehler(tmp_path):
    client = FakeClient(refusal_in="zug_a")
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4", client=client, qmd_query=FakeQmd())
    assert erg.protokoll["technischer_fehler"]["art"] == "refusal"
    assert erg.protokoll["technischer_fehler"]["details"]["stop_details"]["category"] == "test"
    assert len([kw for kw in client.messages.stream_aufrufe if not kw.get("tools")]) == 1


def test_z4_refusal_in_werkzeugrunde(tmp_path):
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4", client=FakeClient(refusal_in="runde"), qmd_query=FakeQmd())
    assert erg.protokoll["technischer_fehler"]["art"] == "refusal"
    assert erg.protokoll["technischer_fehler"]["details"]["zug"] == "runde_1"


def test_zug_b_refusal_oder_ohne_parsed_output(tmp_path):
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4", client=FakeClient(refusal_in="zug_b"), qmd_query=FakeQmd())
    assert erg.protokoll["technischer_fehler"]["art"] == "refusal"
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4b", client=FakeClient(parse_none=True), qmd_query=FakeQmd())
    assert erg.protokoll["technischer_fehler"]["art"] == "structured_output"


# ---------------------------------------------------------------------------
# Z6: 17.5 im Treiber
# ---------------------------------------------------------------------------


def test_z6_kopplung_verletzt_wird_technischer_fehler(tmp_path):
    client = FakeClient(parse_felder=felder(status="BEWERTET", score=None))
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4", client=client, qmd_query=FakeQmd())
    assert erg.zeile is None and erg.protokoll["technischer_fehler"]["art"] == "17.5"
    assert "17.2 Regel 1" in erg.protokoll["technischer_fehler"]["details"]
    assert erg.protokoll["zug_b_felder"]["status"] == "BEWERTET"
    assert not (lauf_dir(tmp_path) / "cfo.jsonl").exists()


def test_information_fehlt_zeile_ist_gueltig(tmp_path):
    client = FakeClient(parse_felder=felder(status="INFORMATION FEHLT", score=None,
                                            fehlende=["Messprotokoll"], praezedenz=None, hinweis=None))
    erg = treiber.fuehre_rolle_aus("it", EISENACH, lauf_dir(tmp_path), "t4", client=client, qmd_query=FakeQmd())
    assert erg.fehler is None and erg.zeile.score is None
    assert erg.protokoll["collections"] == ["intern"]


# ---------------------------------------------------------------------------
# Z5 und Z12: Kontextauswahl
# ---------------------------------------------------------------------------


FRAGE_POL = "Welche Vorgaben macht POL-FIN-002 zu Investitionsvorlagen?"


def _abl(i: int) -> str:
    return f"it_doku/sonstiges/2020/2020-01-{i:02d}-ablenker-{i}.md"


def test_z12_namensbezug_bekommt_raenge_zwei_bis_fuenf_nach_den_rang_eins_treffern():
    # Fassung 2: zuerst Rang 1 jeder Abfrage, dann die Raenge 2 bis 5 der Glaswerk-Abfrage
    # (Namensbezug: Treffer unter "glaswerk-nord" abgelegt), erst danach die uebrigen Raenge.
    abfragen = [
        {"frage": FRAGE_POL, "treffer": [_abl(1), _abl(2), _abl(3), _abl(4)]},
        {"frage": FRAGE_GLASWERK, "treffer": [ABLENKER[0], ABLENKER[1], GOLDEN[0], GOLDEN[1], GOLDEN[2], _abl(9)]},
    ]
    auswahl = treiber.waehle_kontext(abfragen, deckel=6, k=3, k_namen=5)
    assert auswahl == [_abl(1), ABLENKER[0], ABLENKER[1], GOLDEN[0], GOLDEN[1], GOLDEN[2]]


def test_z12_ohne_namensbezug_drei_je_abfrage_dann_reihum():
    abfragen = [
        {"frage": "Welche Regeln gelten fuer Investitionen?", "treffer": [_abl(1), _abl(2), _abl(3), _abl(4), _abl(5)]},
        {"frage": "Wie ist die Ergebnislage laut Kennzahlenbericht?", "treffer": [_abl(6), _abl(7), _abl(8), _abl(9)]},
    ]
    auswahl = treiber.waehle_kontext(abfragen, deckel=8, k=3, k_namen=5)
    # Rang 1 beider Abfragen, dann je Abfrage die Raenge 2 bis 3, dann reihum Rang 4 der
    # ersten, Rang 4 der zweiten
    assert auswahl == [_abl(1), _abl(6), _abl(2), _abl(3), _abl(7), _abl(8), _abl(4), _abl(9)]


def test_z12_duplikate_und_deckel():
    abfragen = [
        {"frage": "Frage eins", "treffer": [_abl(1), _abl(2), _abl(1)]},
        {"frage": "Frage zwei", "treffer": [_abl(2), _abl(3), _abl(4)]},
        {"frage": "Frage ohne Treffer", "treffer": []},
    ]
    assert treiber.waehle_kontext(abfragen, deckel=3, k=3) == [_abl(1), _abl(2), _abl(3)]
    assert treiber.waehle_kontext([], deckel=3) == []


def test_z12_diagnosefall_golden_auf_globalen_raengen_3_9_14_25():
    # Nachgebaut aus .test/1b_diagnose.md, Abschnitt 2: qmd normiert je Abfrage, der beste
    # Treffer jeder Abfrage bekommt 1,0. Global nach Score sortiert landen die Golden-Dokumente
    # der Glaswerk-Abfrage (1,00 / 0,63 / 0,62 / 0,54) auf den Raengen 3, 9, 14, 25 hinter den
    # Rang-1- bis Rang-3-Treffern beliebiger anderer Abfragen. Die Auswahl je Abfrage haelt sie.
    # Fuenf Abfragen in chronologischer Reihenfolge, Scores je Abfrage normiert wie bei qmd.
    laeufe = [
        ("Welche Pflichtinhalte stellt die Investitionsrichtlinie POL-FIN-002 an Vorlagen?",
         "q02", [1.00, 0.75, 0.625, 0.59, 0.58, 0.52, 0.50, 0.41]),
        ("Wie war der Investitionsantrag INV-2024-01 aufgebaut und wie wurde er bewertet?",
         "q03", [1.00, 0.70, 0.61, 0.57, 0.56, 0.55, 0.53, 0.52]),
        (FRAGE_GLASWERK, "glaswerk", None),
        ("Was hat der Beirat zum Antrag im August 2024 beschlossen?",
         "q11", [1.00, 0.66, 0.60, 0.55, 0.51, 0.50, 0.47, 0.33]),
        ("Welche drei Top-Priority-Initiativen wurden im Februar 2025 ausgewaehlt?",
         "q13", [1.00, 0.63, 0.63, 0.63, 0.62, 0.61, 0.52, 0.50]),
    ]
    glaswerk = [hit(GOLDEN[0], 1.00), hit(GOLDEN[1], 0.63), hit(GOLDEN[2], 0.62),
                hit("projektlaufwerk/glaswerk-nord-margenverlust-durch-/2013/2013-11-07-nachtrag.md", 0.54),
                hit(_abl(1), 0.50), hit(_abl(2), 0.39), hit(_abl(3), 0.25), hit(_abl(4), 0.22)]
    golden4 = [treiber.rel_aus_uri(h["file"]) for h in glaswerk[:4]]
    abfragen, alle = [], []
    for frage, kennung, scores in laeufe:
        hits = glaswerk if scores is None else [
            hit(f"it_doku/{kennung}/2024/2024-01-{i + 1:02d}-{kennung}-treffer-{i + 1}.md", s) for i, s in enumerate(scores)]
        rels = [treiber.rel_aus_uri(h["file"]) for h in hits]
        abfragen.append({"frage": frage, "treffer": rels})
        alle += [(h["score"], rel) for h, rel in zip(hits, rels)]

    # Kontrolle: global nach Score sortiert (stabil, wie der alte Treiber) liegen die vier
    # Golden-Dokumente auf den Raengen 3, 9, 14 und 25, nur zwei davon unter den ersten zwoelf.
    global_sortiert = [rel for _, rel in sorted(alle, key=lambda x: -x[0])]
    assert [global_sortiert.index(g) + 1 for g in golden4] == [3, 9, 14, 25]
    assert len(set(global_sortiert[:12]) & set(golden4)) == 2

    auswahl = treiber.waehle_kontext(abfragen, deckel=16, k=3, k_namen=5)
    assert len(auswahl) == 16
    assert all(g in auswahl for g in golden4)
    # Fassung 2: Rang 1 jeder der fuenf Abfragen zuerst (das dritte ist GOLDEN[0]), dann die
    # Raenge 2 bis 5 der Glaswerk-Abfrage
    assert auswahl[2] == golden4[0]
    assert auswahl[5:9] == [treiber.rel_aus_uri(h["file"]) for h in glaswerk[1:5]]


def test_seltene_terme():
    t = treiber.seltene_terme("Wie ist der Investitionsantrag INV-2024-01 Gießerei Eisenach aufgebaut?")
    assert "giesserei" in t and "eisenach" in t and "investitionsantrag" in t
    assert "welche" not in treiber.seltene_terme("Welche Kosten gibt es?")


def test_abfrage_hat_namensbezug():
    assert treiber.abfrage_hat_namensbezug(FRAGE_GLASWERK, [ABLENKER[0], GOLDEN[0]])
    assert not treiber.abfrage_hat_namensbezug(FRAGE_GLASWERK, [ABLENKER[0], ABLENKER[2]])
    assert not treiber.abfrage_hat_namensbezug("Welche Kosten gibt es?", GOLDEN)


def test_z12_im_lauf_goldene_treffer_bleiben_im_kontext(tmp_path):
    # Zwei Abfragen: erst zwoelf hoch bewertete Ablenker, dann die Glaswerk-Abfrage mit den
    # Golden-Dokumenten auf den Raengen 4 bis 6. Deckel 16: alle drei landen im Kontext.
    frage_abl = "Welche Regeln gelten fuer Investitionsvorlagen?"
    ablenker = [hit(_abl(i), 0.9 - i * 0.01) for i in range(1, 13)]
    glaswerk = [hit(ABLENKER[0], 1.0), hit(ABLENKER[1], 0.63), hit(ABLENKER[2], 0.62)] + [hit(g, 0.5) for g in GOLDEN]
    qmd = FakeQmd(hits_je_frage={frage_abl: ablenker, FRAGE_GLASWERK: glaswerk})
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4",
                                   client=FakeClient(fragen=[frage_abl, FRAGE_GLASWERK]), qmd_query=qmd, n_treffer=12)
    dok = erg.protokoll["dokumente_im_kontext"]
    im_kontext = [d["datei"] for d in dok]
    assert len(im_kontext) == treiber.KONTEXT_DECKEL == 16
    assert all(g in im_kontext for g in GOLDEN)
    # Fassung 2: Rang 1 beider Abfragen, dann die Raenge 2 bis 5 der Glaswerk-Abfrage
    # (Namensbezug), dann die Raenge 2 und 3 der Ablenker-Abfrage; das dritte Golden-Dokument
    # (Rang 6) kommt reihum.
    assert im_kontext[:6] == [_abl(1), ABLENKER[0], ABLENKER[1], ABLENKER[2], GOLDEN[0], GOLDEN[1]]
    assert im_kontext[6:8] == [_abl(2), _abl(3)]
    golden_eintraege = [d for d in dok if d["datei"] in GOLDEN]
    assert all(d["namensbezug"] and d["abfrage"] == 1 and d["rang"] in (4, 5, 6) for d in golden_eintraege)
    assert erg.protokoll["qmd"]["deckel"] == 16 and erg.protokoll["qmd"]["k_namensbezug"] == 5


# ---------------------------------------------------------------------------
# Orchestrator: Gate, Z9, Ablage, Kapitel 16
# ---------------------------------------------------------------------------


def test_orchestrator_gate_faellt_kein_agent(tmp_path):
    client = FakeClient()
    z, code = orchestrator.orchestriere([COMPANY[0]], list(orchestrator.REIHENFOLGE), lauf_dir(tmp_path), "t4",
                                        client=client, qmd_query=FakeQmd(), mit_vorbedingungen=False, ausgabe=lambda s: None)
    assert code == 3 and z is None
    assert (lauf_dir(tmp_path) / "informationsanforderung.json").exists()
    assert client.messages.stream_aufrufe == []
    assert not list(lauf_dir(tmp_path).glob("*.jsonl"))


def test_orchestrator_z9_eine_rolle_faellt_die_anderen_laufen(tmp_path):
    # Die Wissensbasis scheitert nur fuer die IT-Rolle (Collections ["intern"]).
    qmd = FakeQmd(immer_fehler=True, nur_fuer=["intern"])
    z, code = orchestrator.orchestriere(EISENACH, list(orchestrator.REIHENFOLGE), lauf_dir(tmp_path), "t4",
                                        client=FakeClient(), qmd_query=qmd, mit_vorbedingungen=False, ausgabe=lambda s: None)
    assert code == 1
    assert z.anzahl_gueltige_zeilen == 3 and z.anzahl_bewertet == 3 and z.gesamtscore == 3.0
    assert [r.rolle for r in z.rollen] == ["betriebsrat", "cfo", "ceo"]
    assert any(t["rolle"] == "it" and "keine_treffer" in t["fehler"] for t in z.technische_fehler)
    d = lauf_dir(tmp_path)
    assert not (d / "it.jsonl").exists() and (d / "it.protokoll.json").exists()
    assert len((d / "bewertungen.jsonl").read_text(encoding="utf-8").splitlines()) == 3
    zs = json.loads((d / "zusammenfassung.json").read_text(encoding="utf-8"))
    assert zs["gesamtstatus"] == "BEWERTET" and zs["technische_fehler"]


def test_orchestrator_happy_vier_rollen(tmp_path):
    z, code = orchestrator.orchestriere(EISENACH, list(orchestrator.REIHENFOLGE), lauf_dir(tmp_path), "t4",
                                        client=FakeClient(), qmd_query=FakeQmd(), mit_vorbedingungen=False, ausgabe=lambda s: None)
    assert code == 0 and z.anzahl_gueltige_zeilen == 4 and z.gesamtscore == 3.0 and z.spanne == 0
    zeilen = (lauf_dir(tmp_path) / "bewertungen.jsonl").read_text(encoding="utf-8").splitlines()
    assert [json.loads(l)["rolle"] for l in zeilen] == list(orchestrator.REIHENFOLGE)
    assert (lauf_dir(tmp_path) / "gate.json").exists()
    assert "Gesamt" in orchestrator.bericht(z, list(orchestrator.REIHENFOLGE))


def test_orchestrator_17_5_ueber_dateien_faengt_manipulierte_zeile(tmp_path):
    # Eine Rolle liefert eine Zeile, die auf der Platte nachtraeglich verdorben wird:
    # der Orchestrator liest die Dateien neu und meldet 17.5.
    d = lauf_dir(tmp_path)
    z, code = orchestrator.orchestriere(EISENACH, ["cfo"], d, "t4", client=FakeClient(), qmd_query=FakeQmd(),
                                        mit_vorbedingungen=False, ausgabe=lambda s: None)
    assert code == 0
    (d / "cfo.jsonl").write_text('{"rolle":"cfo","status":"INFORMATION FEHLT","score":5,"begruendung":"x","fehlende_informationen":[]}\n',
                                 encoding="utf-8")
    from schema import validiere_zeilen
    gueltig, fehler = validiere_zeilen((d / "cfo.jsonl").read_text(encoding="utf-8").splitlines())
    assert gueltig == [] and "17.2" in fehler[0].fehler


def test_orchestrator_cli_unbekannte_rolle():
    assert orchestrator.main(["--antrag", str(EISENACH[0]), "--rollen", "hr"]) == 2


# ---------------------------------------------------------------------------
# Tokenverbrauch: je API-Aufruf im Protokoll, Summe je Rolle und ueber alle Rollen
# ---------------------------------------------------------------------------


def test_tokens_je_aufruf_und_summe_je_rolle(tmp_path):
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4", client=FakeClient(), qmd_query=FakeQmd())
    assert erg.fehler is None, erg.fehler
    prot = json.loads((lauf_dir(tmp_path) / "cfo.protokoll.json").read_text(encoding="utf-8"))
    # zwei Werkzeugrunden (eine Frage, dann Schluss), Zug A, Zug B; Werte aus conftest.USAGE_*
    assert [a["zug"] for a in prot["api_aufrufe"]] == ["runde_1", "runde_2", "zug_a_1", "zug_b"]
    assert prot["tokens"] == {"input_tokens": 330, "output_tokens": 38, "cache_creation_input_tokens": 15,
                              "cache_read_input_tokens": 175, "aufrufe": 4}


def test_tokens_auch_bei_technischem_fehler_erfasst(tmp_path):
    erg = treiber.fuehre_rolle_aus("cfo", EISENACH, lauf_dir(tmp_path), "t4",
                                   client=FakeClient(refusal_in="zug_a"), qmd_query=FakeQmd())
    assert erg.fehler and erg.fehler.startswith("refusal")
    assert erg.protokoll["tokens"]["aufrufe"] == 3  # zwei Runden und der abgelehnte Zug A, bezahlt ist bezahlt


def test_orchestrator_summiert_tokens_ueber_rollen(tmp_path):
    z, code = orchestrator.orchestriere(EISENACH, list(orchestrator.REIHENFOLGE), lauf_dir(tmp_path), "t4",
                                        client=FakeClient(), qmd_query=FakeQmd(), mit_vorbedingungen=False, ausgabe=lambda s: None)
    assert code == 0
    assert set(z.tokens["je_rolle"]) == set(orchestrator.REIHENFOLGE)
    assert z.tokens["gesamt"]["aufrufe"] == 16 and z.tokens["gesamt"]["input_tokens"] == 4 * 330
    zs = json.loads((lauf_dir(tmp_path) / "zusammenfassung.json").read_text(encoding="utf-8"))
    assert zs["tokens"]["gesamt"]["cache_read_input_tokens"] == 4 * 175
