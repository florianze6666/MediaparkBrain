"""T-R: der Rollenlauf mit drei Modellaufrufen (Plan 09, Abschnitt 2 B).

Ohne Modell, ohne API, ohne Einbettungsmodell: Client, Bruecke und die drei Funktionen
aus `suche` sind Attrappen. Geprueft wird der Ablauf, die Informationsgrenze, das sofort
geschriebene Protokoll und die Regel, dass ein technischer Fehler zurueckgegeben und
nicht geworfen wird (Z9).
"""
from __future__ import annotations

import json
from types import SimpleNamespace

import numpy as np
import pytest

import rollenlauf as rl
from kontext import Block, Dokument, Kontext
from schema import Bewertungsfelder

ESSAY = (
    "**Status:** BEWERTET\n**Score:** 3/10\n**Begruendung:** "
    "Bei Glaswerk Nord war die Anlage technisch in Ordnung, verloren gegangen ist die "
    "Marge. Investition 3.547.000 EUR ohne zugeordnete Deckung."
)
FRAGEN = [
    "Was ist beim Projekt Glaswerk Nord 2013 passiert?",
    "Welche Regel entstand daraus fuer Angebotsreviews?",
    "Wie ist der Investitionsrahmen belegt?",
]


# --- Attrappen ----------------------------------------------------------------


def usage(**kw):
    felder = {"input_tokens": 100, "output_tokens": 20,
              "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}
    felder.update(kw)
    return SimpleNamespace(**felder)


def textblock(text, citations=None):
    return SimpleNamespace(type="text", text=text, citations=citations)


def zitat(document_index, cited_text):
    return SimpleNamespace(type="char_location", document_index=document_index,
                           cited_text=cited_text, start_char_index=0,
                           end_char_index=len(cited_text))


def werkzeugaufruf(fragen, name="recherchefragen"):
    return SimpleNamespace(type="tool_use", id="tu_1", name=name, input={"fragen": list(fragen)})


def antwort(content, stop_reason="end_turn", stop_details=None, **u):
    return SimpleNamespace(content=content, stop_reason=stop_reason,
                           stop_details=stop_details, usage=usage(**u))


def felder(status="BEWERTET", score=3):
    return Bewertungsfelder(
        status=status, score=score,
        begruendung="Verloren gegangen ist die Marge. 3.547.000 EUR ohne Deckung.",
        fehlende_informationen=[] if status == "BEWERTET" else ["Deckungsquelle"],
        praezedenz="Glaswerk Nord 2013", entscheidungsrelevanter_hinweis="Messprotokoll vorlegen.")


class FakeStream:
    def __init__(self, m):
        self.m = m

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def get_final_message(self):
        return self.m


class FakeMessages:
    def __init__(self, fragen=None, kein_aufruf=False, tool_name="recherchefragen",
                 zug_a_stops=None, refusal_in=None, parse_felder=None, parse_none=False,
                 zitat_index=0):
        self.fragen = FRAGEN if fragen is None else fragen
        self.kein_aufruf = kein_aufruf
        self.tool_name = tool_name
        self.zug_a_stops = list(zug_a_stops or ["end_turn"])
        self.refusal_in = refusal_in
        self.parse_felder = parse_felder
        self.parse_none = parse_none
        self.zitat_index = zitat_index
        self.stream_aufrufe: list[dict] = []
        self.parse_aufrufe: list[dict] = []
        self._zug_a = 0

    def stream(self, **kw):
        self.stream_aufrufe.append(kw)
        if kw.get("tools"):
            if self.refusal_in == "zug_1":
                return FakeStream(antwort([textblock("")], stop_reason="refusal",
                                          stop_details=SimpleNamespace(
                                              type="refusal", category="test",
                                              explanation="Test")))
            if self.kein_aufruf:
                return FakeStream(antwort([textblock("Ich frage nicht.")]))
            return FakeStream(antwort(
                [textblock("Ich stelle drei Fragen."), werkzeugaufruf(self.fragen, self.tool_name)],
                stop_reason="tool_use"))
        self._zug_a += 1
        if self.refusal_in == "zug_a":
            return FakeStream(antwort([textblock("")], stop_reason="refusal",
                                      stop_details=SimpleNamespace(type="refusal",
                                                                   category="test",
                                                                   explanation="Test")))
        stop = self.zug_a_stops[min(self._zug_a - 1, len(self.zug_a_stops) - 1)]
        return FakeStream(antwort(
            [textblock(ESSAY, [zitat(self.zitat_index, "verloren gegangen ist die Marge")])],
            stop_reason=stop))

    def parse(self, **kw):
        self.parse_aufrufe.append(kw)
        f = self.parse_felder if self.parse_felder is not None else felder()
        return SimpleNamespace(content=[], stop_reason="end_turn", stop_details=None,
                               parsed_output=None if self.parse_none else f,
                               usage=usage(cache_read_input_tokens=4200))


class FakeClient:
    def __init__(self, **kw):
        self.messages = FakeMessages(**kw)


class FakeBruecke:
    def __init__(self, fehler=None):
        self.fehler = fehler
        self.texte: list[list[str]] = []

    def embed(self, texte):
        if self.fehler:
            raise self.fehler
        self.texte.append(list(texte))
        return [[1.0] + [0.0] * 15 for _ in texte]


def treffer(quelle, score, collection="intern"):
    return {"quelle": quelle, "collection": collection, "titel": quelle.rsplit("/", 1)[-1],
            "chunk": 0, "score": score}


@pytest.fixture
def suche_attrappe(monkeypatch):
    """Ersetzt die drei Funktionen aus `suche`, die ein Modell oder den Index braeuchten."""
    zustand = {"treffer": None, "collections": []}

    def fake_suche(query_vektor, collections, index_vektoren, metadaten, top_n=8):
        zustand["collections"].append(list(collections))
        if zustand["treffer"] is not None:
            return list(zustand["treffer"])
        return [treffer(f"projektlaufwerk/fall/2013/t{i}.md", 0.9 - i / 10) for i in range(3)]

    def fake_dedup(treffer_listen, bereits_vorhanden, ziel_anzahl=4):
        gesehen = set(bereits_vorhanden)
        out = []
        for liste in treffer_listen:
            for t in liste:
                if t["quelle"] in gesehen:
                    continue
                gesehen.add(t["quelle"])
                out.append(t)
                if len(out) >= ziel_anzahl:
                    return out
        return out

    monkeypatch.setattr(rl.suche, "suche_vektoriell", fake_suche)
    monkeypatch.setattr(rl.suche, "dedup_und_top_k", fake_dedup)
    monkeypatch.setattr(rl.suche, "lies_dokument", lambda q: f"Volltext von {q}")
    return zustand


@pytest.fixture
def basis():
    k = Kontext()
    k.append(*rl.neutrale_bloecke())
    k.append(Block.user("# Zu bewertendes Vorhaben\n\nAntragstext."))
    k.append(Block.dokumente_block(
        [Dokument("sharepoint_finance/policies/2022/richtlinie.md", "Richtlinie",
                  "intern", "Basisdokument", 0.8)], quelle="vorsuche"))
    return k.freeze()


@pytest.fixture
def index():
    return (np.zeros((3, 16), dtype=np.float32),
            [{"quelle": f"x{i}.md", "collection": "intern", "titel": f"x{i}", "chunk": 0}
             for i in range(3)])


def lauf(basis, tmp_path, client=None, prae=None, **kw):
    return rl.rollenlauf(
        basis=basis, prae_quellen=prae if prae is not None else
        ["sharepoint_finance/policies/2022/richtlinie.md"],
        rolle=kw.pop("rolle", "cfo"), lauf_dir=tmp_path / "lauf-1",
        bruecke=kw.pop("bruecke", FakeBruecke()), index=kw.pop("index"),
        client=client or FakeClient(), modell="fake-modell")


# --- Der gute Fall ------------------------------------------------------------


def test_vollstaendiger_lauf(basis, index, tmp_path, suche_attrappe):
    c = FakeClient()
    erg = lauf(basis, tmp_path, client=c, index=index)

    assert erg["ok"] is True
    z = erg["zeile"]
    assert z.rolle == "cfo" and z.status == "BEWERTET" and z.score == 3
    assert z.quellen  # aus den Zitaten

    # Drei Modellaufrufe: Fragen, Essay, Felder. Keine Werkzeugrunden.
    assert len(c.messages.stream_aufrufe) == 2
    assert len(c.messages.parse_aufrufe) == 1
    assert c.messages.stream_aufrufe[0]["tools"][0]["name"] == "recherchefragen"
    assert "tools" not in c.messages.stream_aufrufe[1]

    p = erg["protokoll"]
    assert p["fragen"] == FRAGEN
    assert len(p["rag_abfragen"]) == 3
    assert p["prompt_version"] == basis.fingerprint()
    assert p["tokens"]["aufrufe"] == 3
    assert p["zitate"] and p["zitate"][0]["datei"]
    assert p["technischer_fehler"] is None

    zeile_datei = tmp_path / "lauf-1" / "cfo.jsonl"
    assert json.loads(zeile_datei.read_text(encoding="utf-8"))["rolle"] == "cfo"


def test_zug_b_bekommt_keine_dokumente(basis, index, tmp_path, suche_attrappe):
    """Zitate und Structured Output schliessen sich aus; Zug B baut eigene Nachrichten."""
    c = FakeClient()
    lauf(basis, tmp_path, client=c, index=index)
    inhalte = c.messages.parse_aufrufe[0]["messages"]
    assert all(isinstance(m["content"], str) for m in inhalte)
    assert c.messages.parse_aufrufe[0]["output_format"] is Bewertungsfelder


def test_basisdokument_wird_nicht_doppelt_geladen(basis, index, tmp_path, suche_attrappe):
    suche_attrappe["treffer"] = [
        treffer("sharepoint_finance/policies/2022/richtlinie.md", 0.99),   # schon in der Basis
        treffer("projektlaufwerk/fall/2013/neu.md", 0.80),
    ]
    erg = lauf(basis, tmp_path, index=index)
    dateien = [d["datei"] for d in erg["protokoll"]["dokumente_im_kontext"]]
    assert dateien.count("sharepoint_finance/policies/2022/richtlinie.md") == 1
    assert "projektlaufwerk/fall/2013/neu.md" in dateien


# --- Informationsgrenze -------------------------------------------------------


def test_collections_kommen_aus_dem_rechtemodell(basis, index, tmp_path, suche_attrappe):
    erg = lauf(basis, tmp_path, index=index, rolle="it")
    assert erg["protokoll"]["collections"] == ["intern"]
    assert all(c == ["intern"] for c in suche_attrappe["collections"])

    erg = lauf(basis, tmp_path, index=index, rolle="betriebsrat")
    assert erg["protokoll"]["collections"] == ["intern", "br"]


def test_treffer_aus_fremder_collection_ist_ein_fehler(basis, index, tmp_path, suche_attrappe):
    suche_attrappe["treffer"] = [treffer("br_ablage/protokoll.md", 0.9, collection="br")]
    erg = lauf(basis, tmp_path, index=index, rolle="it")   # it sieht nur intern
    assert erg["ok"] is False
    assert erg["technischer_fehler"]["art"] == "collection_verletzt"


# --- Z9: ein Fehler wird zurueckgegeben, nicht geworfen ------------------------


@pytest.mark.parametrize("stelle,art", [("zug_1", "refusal"), ("zug_a", "refusal")])
def test_refusal_ergibt_technischen_fehler(basis, index, tmp_path, suche_attrappe, stelle, art):
    erg = lauf(basis, tmp_path, client=FakeClient(refusal_in=stelle), index=index)
    assert erg["ok"] is False and erg["technischer_fehler"]["art"] == art


def test_ohne_werkzeugaufruf_kein_lauf(basis, index, tmp_path, suche_attrappe):
    erg = lauf(basis, tmp_path, client=FakeClient(kein_aufruf=True), index=index)
    assert erg["ok"] is False
    assert erg["technischer_fehler"]["art"] == "kein_fragenbuendel"


def test_max_tokens_wird_genau_einmal_wiederholt(basis, index, tmp_path, suche_attrappe):
    c = FakeClient(zug_a_stops=["max_tokens", "end_turn"])
    erg = lauf(basis, tmp_path, client=c, index=index)
    assert erg["ok"] is True
    assert c.messages.stream_aufrufe[-1]["messages"][-1]["content"][0]["text"].endswith(
        rl.KUERZER_ZUSATZ)

    c2 = FakeClient(zug_a_stops=["max_tokens", "max_tokens"])
    erg2 = lauf(basis, tmp_path, client=c2, index=index)
    assert erg2["ok"] is False and erg2["technischer_fehler"]["art"] == "max_tokens"


def test_bruecke_tot_ergibt_wissensbasis_fehler(basis, index, tmp_path, suche_attrappe):
    kaputt = FakeBruecke(fehler=rl.suche.SucheFehler("Bruecke ist beendet"))
    erg = lauf(basis, tmp_path, index=index, bruecke=kaputt)
    assert erg["ok"] is False and erg["technischer_fehler"]["art"] == "wissensbasis"


def test_keine_treffer_ist_ein_befund(basis, index, tmp_path, suche_attrappe):
    suche_attrappe["treffer"] = []
    erg = lauf(basis, tmp_path, index=index)
    assert erg["ok"] is False and erg["technischer_fehler"]["art"] == "keine_treffer"


def test_fehlendes_parsed_output_ergibt_fehler(basis, index, tmp_path, suche_attrappe):
    erg = lauf(basis, tmp_path, client=FakeClient(parse_none=True), index=index)
    assert erg["ok"] is False and erg["technischer_fehler"]["art"] == "structured_output"


def test_information_fehlt_koppelt_score_auf_null(basis, index, tmp_path, suche_attrappe):
    c = FakeClient(parse_felder=felder(status="INFORMATION FEHLT", score=None))
    erg = lauf(basis, tmp_path, client=c, index=index)
    assert erg["ok"] is True
    assert erg["zeile"].status == "INFORMATION FEHLT" and erg["zeile"].score is None
    assert erg["protokoll"]["score_abweichung"]["essay"] == 3


def test_unbekannte_rolle_ergibt_fehler(basis, index, tmp_path, suche_attrappe):
    erg = lauf(basis, tmp_path, index=index, rolle="hausmeister")
    assert erg["ok"] is False and erg["technischer_fehler"]["art"] == "unbekannte_rolle"


# --- T-O2: das Protokoll liegt sofort -----------------------------------------


def test_protokoll_rumpf_liegt_vor_dem_ersten_modellaufruf(basis, index, tmp_path,
                                                           suche_attrappe):
    lauf_dir = tmp_path / "lauf-1"
    gesehen = {}

    class Spion(FakeClient):
        def __init__(self):
            super().__init__()
            aussen = self

            class M(FakeMessages):
                def stream(self, **kw):
                    if "rumpf" not in gesehen:
                        f = lauf_dir / "cfo.protokoll.json"
                        gesehen["rumpf"] = json.loads(f.read_text(encoding="utf-8"))
                    return FakeMessages.stream(self, **kw)

            self.messages = M()
            _ = aussen

    rl.rollenlauf(basis=basis, prae_quellen=[], rolle="cfo", lauf_dir=lauf_dir,
                  bruecke=FakeBruecke(), index=index, client=Spion(), modell="fake-modell")

    assert gesehen["rumpf"]["rolle"] == "cfo"
    assert gesehen["rumpf"]["essay"] is None
    assert gesehen["rumpf"]["technischer_fehler"] is None


def test_protokoll_traegt_die_felder_die_das_wiki_liest(basis, index, tmp_path,
                                                        suche_attrappe):
    erg = lauf(basis, tmp_path, index=index)
    p = erg["protokoll"]
    for feld in ("essay", "zitate", "rag_abfragen", "modell", "prompt_version",
                 "tokens", "zeiten_s", "technischer_fehler"):
        assert feld in p, feld
    assert p["tokens"]["cache_read_input_tokens"] > 0


# --- Prompt und Manifest ------------------------------------------------------


def test_initialteil_kuendigt_genau_eine_gelegenheit_an():
    assert "genau eine" in rl.INITIALTEIL.lower()
    assert "keine zweite runde" in rl.INITIALTEIL.lower()
    assert "genau drei" in rl.FRAGEN_AUFTRAG.lower()


def test_neutrale_bloecke_sind_rollenneutral():
    """Sie tragen Initialteil und Bewertungslogik, aber keine Persona und keine
    Kalibrierung; sonst waere der geteilte Anfang nicht geteilt."""
    bloecke = rl.neutrale_bloecke()
    assert [b.art for b in bloecke] == ["system", "system"]
    assert bloecke[0].inhalt == rl.INITIALTEIL
    assert bloecke[1].quelle == rl.BEWERTUNGSLOGIK
    gesamt = bloecke[0].inhalt + bloecke[1].inhalt
    for k in rl.ROLLEN_KONFIG.values():
        assert rl.lies(k["persona"]) not in gesamt
        assert rl.lies(k["kalibrierung"]) not in gesamt


def test_rollen_block_ist_eine_nutzernachricht():
    b = rl.rollen_block("cfo")
    assert b.art == "user"
    assert "cfo_persona" in b.inhalt or "CFO" in b.inhalt


# --- Werkzeugschema: die Schranke der Schnittstelle ----------------------------


def test_werkzeugschema_ohne_unerlaubte_array_grenzen():
    """Die Schnittstelle laesst fuer Arrays nur minItems 0 oder 1 zu und lehnt alles
    andere mit HTTP 400 ab. Der Integrationslauf vom 06.09.2026 ist daran in allen vier
    Rollen gescheitert; dieser Test haelt die Reparatur fest."""

    def pruefe(knoten, pfad="input_schema"):
        if isinstance(knoten, dict):
            for schluessel in ("minItems", "maxItems"):
                if schluessel in knoten:
                    assert knoten[schluessel] in (0, 1), (
                        f"{pfad}.{schluessel} = {knoten[schluessel]}; die Schnittstelle "
                        "erlaubt nur 0 oder 1 und antwortet sonst mit 400."
                    )
            for k, v in knoten.items():
                pruefe(v, f"{pfad}.{k}")
        elif isinstance(knoten, list):
            for i, v in enumerate(knoten):
                pruefe(v, f"{pfad}[{i}]")

    for werkzeug in rl.FRAGEN_TOOL:
        pruefe(werkzeug["input_schema"])


def test_dreizahl_steht_im_beschreibungstext():
    """Was das Schema nicht erzwingen kann, muss der Text sagen."""
    werkzeug = rl.FRAGEN_TOOL[0]
    assert "DREI" in werkzeug["description"]
    assert "DREI" in werkzeug["input_schema"]["properties"]["fragen"]["description"]
    assert "drei" in rl.FRAGEN_AUFTRAG.lower()


@pytest.mark.parametrize("gelieferte, erwartet", [(2, 2), (4, 3)])
def test_falsche_fragenzahl_ist_ein_befund_kein_abbruch(basis, index, tmp_path,
                                                        suche_attrappe, gelieferte, erwartet):
    """Zu wenige Fragen gehen so weiter, zu viele werden gekuerzt; beides steht im
    Protokoll und laesst den Lauf weiterlaufen."""
    fragen = [f"Frage {i} an die Wissensbasis?" for i in range(gelieferte)]
    erg = lauf(basis, tmp_path, client=FakeClient(fragen=fragen), index=index)
    assert erg["ok"] is True
    protokoll = json.loads((tmp_path / "lauf-1" / "cfo.protokoll.json").read_text(encoding="utf-8"))
    assert len(protokoll["fragen"]) == erwartet
    assert str(gelieferte) in protokoll["fragen_abweichung"]


def test_drei_fragen_ohne_abweichungsvermerk(basis, index, tmp_path, suche_attrappe):
    erg = lauf(basis, tmp_path, client=FakeClient(), index=index)
    assert erg["ok"] is True
    protokoll = json.loads((tmp_path / "lauf-1" / "cfo.protokoll.json").read_text(encoding="utf-8"))
    assert "fragen_abweichung" not in protokoll
