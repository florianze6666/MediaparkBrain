"""Tests des parallelen Orchestrators (Plan 09, Abschnitt 10, Gruppe T-O).

Ohne API und ohne Einbettungsmodell. `rollenlauf`, `suche` und `kontext` sind hier
Attrappen; sie werden von den Bauauftraegen 1 und 2 gebaut. Geprueft wird genau das,
was der Orchestrator selbst verantwortet: die drei Abschnitte, die Nebenlaeufigkeit,
die Informationsgrenze der Vorsuche, und dass eine gescheiterte Rolle die anderen
nicht mitreisst.
"""

from __future__ import annotations

import hashlib
import json
import sys
import threading
import time
from pathlib import Path

import pytest

AGENTEN_DIR = Path(__file__).resolve().parent.parent
if str(AGENTEN_DIR) not in sys.path:
    sys.path.insert(0, str(AGENTEN_DIR))

import kontext as kontext_modul  # noqa: E402
import orchestrator as orch  # noqa: E402
import rollenlauf as rollenlauf_modul  # noqa: E402
import suche as suche_modul  # noqa: E402
from schema import Zeile  # noqa: E402

from tests.conftest import COMPANY, EISENACH, STAMMDATEN  # noqa: E402

ROLLEN4 = ["betriebsrat", "cfo", "it", "ceo"]


# ---------------------------------------------------------------------------
# Attrappen
# ---------------------------------------------------------------------------


class FakeKontext:
    """Minimale, aber echte Fork-Semantik: Praefix geteilt, Rest eigen."""

    def __init__(self, praefix=(), versiegelt=False):
        self._praefix = tuple(praefix)
        self._rest = []
        self._versiegelt = versiegelt

    def append(self, *bloecke):
        if self._versiegelt and not self._rest and self._ist_basis:
            raise ValueError("versiegelt")
        self._rest.extend(bloecke)
        return self

    _ist_basis = False

    def fork(self):
        k = FakeKontext(self._praefix, versiegelt=True)
        return k

    def freeze(self):
        self._praefix = self._praefix + tuple(self._rest)
        self._rest = []
        self._versiegelt = True
        self._ist_basis = True
        return self

    def fingerprint(self):
        roh = "|".join(f"{b.art}:{b.quelle}:{len(b.inhalt)}:{len(b.dokumente)}"
                       for b in self._praefix)
        return hashlib.sha256(roh.encode("utf-8")).hexdigest()

    def speichern(self, pfad: Path):
        pfad.write_text(json.dumps({
            "fingerprint": self.fingerprint(),
            "bloecke": [{"art": b.art, "quelle": b.quelle} for b in self._praefix],
        }, ensure_ascii=False, indent=2), encoding="utf-8")


class FakeBruecke:
    def __init__(self):
        self.aufrufe = []
        self.sperre = threading.Lock()

    def embed(self, texte):
        with self.sperre:
            self.aufrufe.append(list(texte))
        return [[0.1] * 8 for _ in texte]

    def ping(self):
        return {"modell": "fake"}

    def schliessen(self):
        pass


def treffer(quelle: str, score: float, collection: str = "intern") -> dict:
    return {"quelle": quelle, "titel": Path(quelle).stem, "collection": collection,
            "score": score, "chunk": 0}


@pytest.fixture
def basis_umgebung(monkeypatch, tmp_path):
    """Setzt alle Fremdmodule auf Attrappen und liefert die Bruecke zurueck."""
    monkeypatch.setattr(kontext_modul, "Kontext", FakeKontext)
    monkeypatch.setattr(rollenlauf_modul, "INITIALTEIL", "Onboarding-Text.", raising=False)
    monkeypatch.setattr(suche_modul, "lies_dokument", lambda q: f"Volltext von {q}")
    monkeypatch.setattr(suche_modul, "suche_vektoriell",
                        lambda vek, cols, v, m, top_n=8: [
                            treffer("projektlaufwerk/a.md", 0.9),
                            treffer("qm_lenkung/b.md", 0.8),
                            treffer("sharepoint_finance/c.md", 0.7),
                        ])
    monkeypatch.setattr(suche_modul, "dedup_und_top_k",
                        lambda listen, vorhanden, ziel_anzahl=4: listen[0][:ziel_anzahl])
    monkeypatch.setattr(suche_modul, "vorbedingungen",
                        lambda bruecke=None: {"erfuellt": True, "befunde": []})
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")
    return FakeBruecke()


def fake_rollenlauf_fabrik(lauf_dir: Path, fehlerhaft=(), verzoegerung=0.0, scores=None):
    """Baut eine Attrappe fuer `rollenlauf.rollenlauf`, die echte Dateien schreibt."""
    scores = scores or {}
    zeiten: dict[str, tuple[float, float]] = {}
    sperre = threading.Lock()

    def fn(basis, prae_quellen, rolle, dir_, bruecke=None, index=None, on_cache_warm=None):
        start = time.monotonic()
        # Schritt 0: Protokoll-Rumpf SOFORT, damit das Dashboard den Start sieht.
        rumpf = {
            "rolle": rolle,
            "prompt_version": basis.fingerprint(),
            "tokens": {"input_tokens": 10, "output_tokens": 5,
                       "cache_creation_input_tokens": 0,
                       "cache_read_input_tokens": 0 if rolle == "betriebsrat" else 100,
                       "aufrufe": 3},
            "technischer_fehler": None,
        }
        (dir_ / f"{rolle}.protokoll.json").write_text(
            json.dumps(rumpf, ensure_ascii=False), encoding="utf-8")
        if verzoegerung:
            time.sleep(verzoegerung / 2)
            if on_cache_warm:
                on_cache_warm()
            time.sleep(verzoegerung / 2)
        elif on_cache_warm:
            on_cache_warm()
        ende = time.monotonic()
        with sperre:
            zeiten[rolle] = (start, ende)

        if rolle in fehlerhaft:
            rumpf["technischer_fehler"] = {"art": "WissensbasisFehler", "details": "Attrappe"}
            (dir_ / f"{rolle}.protokoll.json").write_text(
                json.dumps(rumpf, ensure_ascii=False), encoding="utf-8")
            return {"rolle": rolle, "ok": False, "protokoll": rumpf,
                    "technischer_fehler": rumpf["technischer_fehler"]}

        z = Zeile(rolle=rolle, status="BEWERTET", score=scores.get(rolle, 5),
                  begruendung=f"Begruendung {rolle} mit Zitat und 3.547.000 EUR.",
                  fehlende_informationen=[], quellen=list(prae_quellen))
        (dir_ / f"{rolle}.jsonl").write_text(z.als_jsonl() + "\n", encoding="utf-8")
        return {"rolle": rolle, "ok": True, "zeile": z, "protokoll": rumpf}

    fn.zeiten = zeiten
    return fn


# ---------------------------------------------------------------------------
# Antragszerlegung (Abschnitt A)
# ---------------------------------------------------------------------------


def test_zwei_dateien_werden_an_der_natuerlichen_grenze_geteilt():
    """Steckbrief gegen Business Case: die Antraege liegen genau so vor."""
    t1, t2, strategie = orch.teile_antrag(EISENACH)
    assert strategie == "dateien"
    assert "Project Charter" in t1 or "Steckbrief" in t1 or "Projektname" in t1
    assert "Business Case" in t2
    assert t1 != t2 and t1.strip() and t2.strip()


def test_eine_datei_wird_nach_abschnitten_geteilt():
    """Ohne zweite Datei entscheiden dieselben Ueberschriftenmuster wie im Gate."""
    einzeln = [COMPANY[0]]
    t1, t2, strategie = orch.teile_antrag(einzeln)
    assert strategie in ("abschnitte", "haelftig")
    assert t1.strip() and t2.strip()
    if strategie == "abschnitte":
        # Die kaufmaennischen Angaben duerfen nicht im Steckbriefteil landen.
        assert "Business Case" not in t1 or "Business Case" in t2


def test_unerkennbarer_antrag_faellt_haelftig_zurueck(tmp_path):
    """Kein stiller Verlust des halben Antrags, sondern eine benannte Strategie."""
    p = tmp_path / "ohne_ueberschriften.md"
    p.write_text("Fliesstext ohne jede Ueberschrift. " * 50, encoding="utf-8")
    t1, t2, strategie = orch.teile_antrag([p])
    assert strategie == "haelftig"
    assert t1.strip() and t2.strip()
    assert len(t1) + len(t2) == len(p.read_text(encoding="utf-8"))


def test_beide_teile_gehen_in_die_vorsuche(basis_umgebung, monkeypatch):
    """Der Antrag ueberschreitet das Fenster des Modells; er wird zweimal eingebettet."""
    bruecke = basis_umgebung
    orch.vorsuche(["teil eins", "teil zwei"], bruecke, (None, None))
    assert bruecke.aufrufe == [["teil eins", "teil zwei"]]


# ---------------------------------------------------------------------------
# Informationsgrenze (T-N1)
# ---------------------------------------------------------------------------


def test_vorsuche_ausserhalb_von_intern_ist_ein_fehler(basis_umgebung, monkeypatch):
    """Ein clevel-Dokument im gemeinsamen Anfang saehe jede Rolle, auch die IT (AE-03)."""
    monkeypatch.setattr(suche_modul, "dedup_und_top_k",
                        lambda listen, vorhanden, ziel_anzahl=4: [
                            treffer("sharepoint_gf/geheim.md", 0.9, collection="clevel")])
    with pytest.raises(ValueError, match="ausserhalb von intern"):
        orch.vorsuche(["a", "b"], basis_umgebung, (None, None))


def test_vorsuche_fragt_nur_die_basis_collection_ab(basis_umgebung, monkeypatch):
    gesehen: list[list[str]] = []

    def spion(vek, cols, v, m, top_n=8):
        gesehen.append(list(cols))
        return [treffer("projektlaufwerk/a.md", 0.9)]

    monkeypatch.setattr(suche_modul, "suche_vektoriell", spion)
    monkeypatch.setattr(suche_modul, "dedup_und_top_k",
                        lambda listen, vorhanden, ziel_anzahl=4: listen[0])
    orch.vorsuche(["a", "b"], basis_umgebung, (None, None))
    assert gesehen == [["intern"], ["intern"]]


# ---------------------------------------------------------------------------
# Abschnitt A: Gate und Vorbedingungen
# ---------------------------------------------------------------------------


def test_gate_durchfall_ergibt_exit_3_und_keine_rolle_startet(basis_umgebung, tmp_path):
    """Die vier Company-Antraege fallen durch; FR-08 haelt den Lauf an."""
    gestartet = []

    def nie(*a, **k):
        gestartet.append(a)
        return {}

    z, code = orch.orchestriere([COMPANY[0]], ROLLEN4, tmp_path, "t", bruecke=basis_umgebung,
                                mit_vorbedingungen=False, ausgabe=lambda s: None,
                                rollenlauf_fn=nie)
    assert code == 3 and z is None
    assert (tmp_path / "gate.json").exists()
    assert (tmp_path / "informationsanforderung.json").exists()
    assert not gestartet


def test_gate_durchfall_laedt_das_einbettungsmodell_nicht(tmp_path, monkeypatch):
    """Das Gate ist der billige Pfad. Ein durchgefallener Antrag darf nicht erst
    4,4 Sekunden und 1,2 GB Grafikspeicher kosten."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")
    gerufen = []

    z, code = orch.orchestriere(
        [COMPANY[0]], ROLLEN4, tmp_path, "t", mit_vorbedingungen=False,
        ausgabe=lambda s: None, rollenlauf_fn=lambda *a, **k: {},
        bruecke_factory=lambda: gerufen.append("bruecke"),
        index_factory=lambda: gerufen.append("index"),
    )
    assert code == 3 and z is None
    assert gerufen == [], "das Modell wurde trotz Gate-Durchfall geladen"


def test_bestandenes_gate_startet_die_bruecke_genau_einmal(basis_umgebung, tmp_path):
    gerufen = []
    fn = fake_rollenlauf_fabrik(tmp_path)
    orch.orchestriere(EISENACH, ROLLEN4, tmp_path, "t", mit_vorbedingungen=False,
                      ausgabe=lambda s: None, rollenlauf_fn=fn,
                      bruecke_factory=lambda: (gerufen.append("b"), basis_umgebung)[1],
                      index_factory=lambda: (gerufen.append("i"), (None, None))[1])
    assert gerufen == ["b", "i"]


def test_verletzte_vorbedingung_ergibt_exit_2(basis_umgebung, tmp_path, monkeypatch):
    monkeypatch.setattr(suche_modul, "vorbedingungen",
                        lambda bruecke=None: {"erfuellt": False, "befunde": ["Index leer"]})
    z, code = orch.orchestriere(EISENACH, ROLLEN4, tmp_path, "t", bruecke=basis_umgebung,
                                mit_vorbedingungen=True, ausgabe=lambda s: None,
                                rollenlauf_fn=lambda *a, **k: {})
    assert code == 2 and z is None
    daten = json.loads((tmp_path / "vorbedingungen.json").read_text(encoding="utf-8"))
    assert "Index leer" in daten["probleme"]


def test_fehlende_persona_faellt_in_den_vorbedingungen_auf(basis_umgebung, monkeypatch):
    monkeypatch.setattr(rollenlauf_modul, "ROLLEN_KONFIG",
                        {"cfo": {"nutzer": "cfo", "persona": "persona/gibt-es-nicht.md",
                                 "kalibrierung": "persona/cfo_kriterienkalibrierung.md"}})
    probleme = orch.vorbedingungen(["cfo"], basis_umgebung)
    assert any("gibt-es-nicht" in p for p in probleme)


def test_guthaben_zu_knapp_bricht_vor_dem_forken_ab():
    """Sonst brechen vier Rollen gemeinsam ab und verbrennen den halben Lauf."""

    class Pleite:
        class messages:
            @staticmethod
            def create(**k):
                raise RuntimeError("400 credit balance is too low")

    assert "Guthaben reicht nicht" in (orch.pruefe_guthaben(Pleite()) or "")


def test_anderer_api_fehler_bricht_nicht_ab():
    """Ein Netzfehler trifft die Rollen ohnehin und wird dort je Rolle sichtbar (Z9)."""

    class Wackelig:
        class messages:
            @staticmethod
            def create(**k):
                raise RuntimeError("connection reset")

    assert orch.pruefe_guthaben(Wackelig()) is None
    assert orch.pruefe_guthaben(None) is None


# ---------------------------------------------------------------------------
# Abschnitt B: Nebenlaeufigkeit und Z9
# ---------------------------------------------------------------------------


def test_vier_rollen_laufen_wirklich_gleichzeitig(basis_umgebung, monkeypatch, tmp_path):
    """Tool-Call-Scheduling: Vorhut startet, loest bei Tool-Call on_cache_warm aus;
    Nachhut startet noch waehrend Vorhut laeuft, parallel."""
    monkeypatch.setenv("FORK_STAGGER_S", "0.0")
    fn = fake_rollenlauf_fabrik(tmp_path, verzoegerung=0.3)
    start = time.monotonic()
    z, code = orch.orchestriere(EISENACH, ROLLEN4, tmp_path, "t", bruecke=basis_umgebung,
                                mit_vorbedingungen=False, ausgabe=lambda s: None,
                                rollenlauf_fn=fn)
    dauer = time.monotonic() - start
    assert code == 0 and z is not None
    assert dauer < 4 * 0.3, f"kein Parallelbetrieb, {dauer:.2f}s"
    # Vorhut startete zuerst:
    start_erste = fn.zeiten[ROLLEN4[0]][0]
    ende_erste = fn.zeiten[ROLLEN4[0]][1]
    fruehester_start_rest = min(fn.zeiten[r][0] for r in ROLLEN4[1:])
    assert start_erste < fruehester_start_rest, "Vorhut startete nicht zuerst"
    # Nachhut startete beim Tool-Call VOR dem Ende der Vorhut:
    assert fruehester_start_rest < ende_erste, "Nachhut wartete unnoetig auf das Ende der Vorhut"
    # Die uebrigen drei Rollen laufen gleichzeitig (Zeitfenster ueberlappen):
    spaetester_start_rest = max(fn.zeiten[r][0] for r in ROLLEN4[1:])
    fruehestes_ende_rest = min(fn.zeiten[r][1] for r in ROLLEN4[1:])
    assert spaetester_start_rest < fruehestes_ende_rest, "die Nachhut-Zeitfenster ueberlappen nicht"


def test_eine_gescheiterte_rolle_stoppt_die_uebrigen_nicht(basis_umgebung, tmp_path):
    """Z9: der Demonstrator zeigt mit drei von vier Zeilen ein Ergebnis."""
    fn = fake_rollenlauf_fabrik(tmp_path, fehlerhaft={"it"})
    z, code = orch.orchestriere(EISENACH, ROLLEN4, tmp_path, "t", bruecke=basis_umgebung,
                                mit_vorbedingungen=False, ausgabe=lambda s: None,
                                rollenlauf_fn=fn)
    assert code == 1
    assert z.anzahl_gueltige_zeilen == 3
    assert {r.rolle for r in z.rollen} == {"betriebsrat", "cfo", "ceo"}
    assert any(t["rolle"] == "it" for t in z.technische_fehler)
    for rolle in ("betriebsrat", "cfo", "ceo"):
        assert (tmp_path / f"{rolle}.jsonl").exists()
    assert not (tmp_path / "it.jsonl").exists()


def test_protokoll_rumpf_liegt_auch_bei_hartem_absturz_vor(basis_umgebung, tmp_path):
    """T-O2: die Rolle schreibt den Rumpf zuerst; der Orchestrator findet ihn auf der Platte."""

    def stirbt(basis, prae, rolle, dir_, bruecke=None, index=None):
        (dir_ / f"{rolle}.protokoll.json").write_text(
            json.dumps({"rolle": rolle, "tokens": {"input_tokens": 7}}), encoding="utf-8")
        raise RuntimeError("harter Abbruch ohne Rueckgabe")

    z, code = orch.orchestriere(EISENACH, ["cfo"], tmp_path, "t", bruecke=basis_umgebung,
                                mit_vorbedingungen=False, ausgabe=lambda s: None,
                                rollenlauf_fn=stirbt)
    assert code == 1
    assert (tmp_path / "cfo.protokoll.json").exists()
    assert z.tokens["je_rolle"]["cfo"]["input_tokens"] == 7
    assert any("harter Abbruch" in t["fehler"] for t in z.technische_fehler)


def test_jede_rolle_bekommt_einen_eigenen_fork_der_basis(basis_umgebung, tmp_path):
    """A-5: keine geteilte Schreibstelle, jede Rolle arbeitet auf ihrem eigenen Rest."""
    forks: dict[str, object] = {}
    sperre = threading.Lock()

    def fn(basis, prae, rolle, dir_, bruecke=None, index=None):
        k = basis.fork()
        # Jeder Fork haengt etwas Eigenes an; danach darf kein anderer es sehen.
        k.append(kontext_modul.Block(art="user", inhalt=f"Persona {rolle}", quelle=rolle))
        with sperre:
            forks[rolle] = k          # Referenz halten, sonst vergibt Python die id neu
        z = Zeile(rolle=rolle, status="BEWERTET", score=5, begruendung="Text.")
        (dir_ / f"{rolle}.jsonl").write_text(z.als_jsonl() + "\n", encoding="utf-8")
        return {"rolle": rolle, "ok": True, "zeile": z, "protokoll": {}}

    orch.orchestriere(EISENACH, ROLLEN4, tmp_path, "t", bruecke=basis_umgebung,
                      mit_vorbedingungen=False, ausgabe=lambda s: None, rollenlauf_fn=fn)

    assert len(forks) == 4
    assert len({id(k) for k in forks.values()}) == 4, "Forks sind nicht eigenstaendig"
    assert len({k.fingerprint() for k in forks.values()}) == 1, "Forks sehen verschiedene Anfaenge"
    # Der eigene Rest bleibt eigen: keiner traegt den Anhang eines anderen.
    for rolle, k in forks.items():
        eigene = [b.quelle for b in k._rest]
        assert eigene == [rolle], f"{rolle} sieht fremde Anhaenge: {eigene}"


# ---------------------------------------------------------------------------
# Abschnitt C: Aggregation, Dateilayout, Zwischenspeicher
# ---------------------------------------------------------------------------


def test_aggregation_und_dateilayout(basis_umgebung, tmp_path):
    """Kapitel 16 ueber die gueltigen Zeilen; die Dateinamen bleiben, wie das Wiki sie liest."""
    fn = fake_rollenlauf_fabrik(tmp_path, scores={"betriebsrat": 2, "cfo": 2, "it": 8, "ceo": 7})
    z, code = orch.orchestriere(STAMMDATEN, ROLLEN4, tmp_path, "lauf-1",
                                bruecke=basis_umgebung, mit_vorbedingungen=False,
                                ausgabe=lambda s: None, rollenlauf_fn=fn)
    assert code == 0
    assert z.gesamtscore == 4.8 and z.anzahl_bewertet == 4
    assert z.spanne == 6
    assert any(k.abstand >= 4 for k in z.konflikte)

    for name in ("gate.json", "basis.json", "bewertungen.jsonl", "zusammenfassung.json"):
        assert (tmp_path / name).exists(), name
    zeilen = (tmp_path / "bewertungen.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert [json.loads(l)["rolle"] for l in zeilen] == ROLLEN4  # Kapitel-17-Reihenfolge


def test_zusammenfassung_traegt_zwischenspeicher_und_teilung(basis_umgebung, tmp_path):
    fn = fake_rollenlauf_fabrik(tmp_path)
    orch.orchestriere(EISENACH, ROLLEN4, tmp_path, "t", bruecke=basis_umgebung,
                      mit_vorbedingungen=False, ausgabe=lambda s: None, rollenlauf_fn=fn)
    daten = json.loads((tmp_path / "zusammenfassung.json").read_text(encoding="utf-8"))
    assert daten["antrag_teilung"] == "dateien"
    assert daten["zwischenspeicher"]["warnungen"] == []
    assert len(daten["zwischenspeicher"]["aus_zwischenspeicher_gelesen"]) == 3
    # Die Kapitel-16-Felder, die das Dashboard liest, sind unveraendert vorhanden.
    for feld in ("gesamtscore", "gesamtstatus", "anzahl_bewertet", "rollen",
                 "technische_fehler", "zeilenfehler", "spanne", "konflikte",
                 "fehlende_informationen"):
        assert feld in daten, feld


def test_verschiedene_fingerabdruecke_werden_gemeldet():
    """Waere der Anfang nicht gemeinsam, bliebe das sonst unbemerkt teuer."""
    prot = {
        "cfo": {"prompt_version": "aaa", "tokens": {"cache_read_input_tokens": 5}},
        "ceo": {"prompt_version": "bbb", "tokens": {"cache_read_input_tokens": 5}},
    }
    erg = orch.pruefe_zwischenspeicher(prot)
    assert any("verschiedene Prompt-Fingerabdruecke" in w for w in erg["warnungen"])


def test_fehlende_zwischenspeicher_lesungen_werden_gemeldet():
    prot = {r: {"prompt_version": "gleich", "tokens": {"cache_read_input_tokens": 0}}
            for r in ROLLEN4}
    erg = orch.pruefe_zwischenspeicher(prot, erwartet="gleich")
    assert any("Zwischenspeicher" in w for w in erg["warnungen"])
    assert erg["aus_zwischenspeicher_gelesen"] == []


def test_alle_rollen_ohne_score_ergeben_kein_gesamtscore(basis_umgebung, tmp_path):
    """16.5: ohne einen einzigen gueltigen Score gibt es keinen Durchschnitt."""

    def ohne_score(basis, prae, rolle, dir_, bruecke=None, index=None):
        z = Zeile(rolle=rolle, status="INFORMATION FEHLT", score=None,
                  begruendung="Ohne Hosting-Modell nicht beurteilbar.",
                  fehlende_informationen=[f"{rolle}: Hosting-Modell"])
        (dir_ / f"{rolle}.jsonl").write_text(z.als_jsonl() + "\n", encoding="utf-8")
        return {"rolle": rolle, "ok": True, "zeile": z, "protokoll": {}}

    z, code = orch.orchestriere(EISENACH, ROLLEN4, tmp_path, "t", bruecke=basis_umgebung,
                                mit_vorbedingungen=False, ausgabe=lambda s: None,
                                rollenlauf_fn=ohne_score)
    assert code == 0
    assert z.gesamtscore is None and z.gesamtstatus == "INFORMATION FEHLT"
    assert len(z.fehlende_informationen) == 4


def test_summiere_tokens_zaehlt_auch_gescheiterte_rollen():
    """Bezahlt ist bezahlt: eine abgebrochene Rolle hat trotzdem Token verbraucht."""
    prot = {
        "cfo": {"tokens": {"input_tokens": 100, "output_tokens": 10, "aufrufe": 3}},
        "it": {"tokens": {"input_tokens": 40, "output_tokens": 0, "aufrufe": 1}},
    }
    t = orch.summiere_tokens(prot)
    assert t["gesamt"]["input_tokens"] == 140
    assert t["gesamt"]["aufrufe"] == 4
    assert t["je_rolle"]["it"]["output_tokens"] == 0


# ---------------------------------------------------------------------------
# Aufrufvertrag zum Wiki
# ---------------------------------------------------------------------------


def test_aufrufvertrag_unveraendert():
    """`llm-wiki/app/bewertung.py` verdrahtet genau diese Flags und Exit-Codes."""
    ap_hilfe = orch.main.__doc__ or ""
    import argparse

    parser = argparse.ArgumentParser()
    # Die Flags muessen so heissen; das Wiki baut den Befehl daraus zusammen.
    assert "--antrag" in Path(orch.__file__).read_text(encoding="utf-8")
    assert "--lauf" in Path(orch.__file__).read_text(encoding="utf-8")
    assert orch.LAEUFE_DIR.name == "laeufe"
    del parser, ap_hilfe


def test_unbekannte_rolle_ergibt_exit_2():
    assert orch.main(["--antrag", str(EISENACH[0]), "--rollen", "hausmeister"]) == 2
