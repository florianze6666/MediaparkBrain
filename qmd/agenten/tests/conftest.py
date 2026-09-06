"""Gemeinsame Fixtures: gefaelschter Anthropic-Client und gefaelschte Wissensbasis.

Kein Test hier ruft die API oder qmd. Der Fake-Client entscheidet aus den Aufrufparametern,
in welchem Zug er steckt (Werkzeugrunde, Zug A, Zug B), und fuehrt je Rolle (erkannt am
Systemprompt) einen eigenen Zaehler. Damit laufen Treiber und Orchestrator mit vier Rollen
gegen dieselbe kleine Skriptlogik.
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

TESTS_DIR = Path(__file__).resolve().parent
AGENTEN_DIR = TESTS_DIR.parent
QMD_DIR = AGENTEN_DIR.parent
ROOT = QMD_DIR.parent
for p in (str(AGENTEN_DIR), str(QMD_DIR / "ingest")):
    if p not in sys.path:
        sys.path.insert(0, p)

from schema import Bewertungsfelder, FragenBuendel  # noqa: E402

EISENACH = [
    ROOT / "project_proposals" / "abwaermenutzung-giesserei-eisenach-charter.md",
    ROOT / "project_proposals" / "abwaermenutzung-giesserei-eisenach-businesscase.md",
]
COMPANY = [
    ROOT / "project_proposals" / "m-companion.md",
    ROOT / "project_proposals" / "m-invoice-coni-company1.md",
    ROOT / "project_proposals" / "m-invoice-coni-company2.md",
    ROOT / "project_proposals" / "max-marketing-automation.md",
]
# Zweites Testprojekt (Fork testprojekt-stammdaten), fuer alle vier Rollen gebaut.
STAMMDATEN = [
    ROOT / "test" / "stammdaten-ki" / "ki-stammdaten-standardisierung-charter.md",
    ROOT / "test" / "stammdaten-ki" / "ki-stammdaten-standardisierung-businesscase.md",
]

# Echte Korpuspfade (Glaswerk Nord 2013), damit volltext() etwas findet.
GOLDEN = [
    "projektlaufwerk/glaswerk-nord-margenverlust-durch-/2013/2013-02-22-abweichung-von-kalkulation-und-ist-kosten-festhalten.md",
    "projektlaufwerk/glaswerk-nord-margenverlust-durch-/2013/2013-09-25-erfahrungen-aus-der-abwicklung-festhalten.md",
    "mailarchiv/glaswerk-nord-margenverlust-durch-/2013/2013-04-21-auf-die-abweichende-waermequellentemperatur-hinweise.md",
]
ABLENKER = [
    "it_doku/plm-einfuehrung-und-die-dreiteilun/2014/2014-04-26-abgrenzung-von-plm-und-erp-festlegen.md",
    "it_doku/plm-einfuehrung-und-die-dreiteilun/2014/2014-03-13-einfuehrung-des-plm-systems-beauftragen.md",
    "sharepoint_finance/policies/2022/2022-12-06-richtlinie-investitionsvorlagen.md",
    "sharepoint_finance/kennzahlen/2025/2025-03-11-kennzahlenbericht-geschaeftsjahr.md",
]
FRAGE_GLASWERK = "Was ist beim Projekt Glaswerk Nord 2013 passiert, als eine nicht gemessene Quellentemperatur der Auslegung zugrunde lag?"


def hit(rel: str, score: float, collection: str = "intern") -> dict:
    return {"file": f"qmd://{collection}/{rel}", "score": score, "snippet": f"Ausschnitt aus {rel}"}


STANDARD_HITS = [hit(GOLDEN[0], 0.41), hit(GOLDEN[1], 0.39), hit(GOLDEN[2], 0.35),
                 hit(ABLENKER[0], 0.80), hit(ABLENKER[1], 0.75), hit(ABLENKER[2], 0.70),
                 hit(ABLENKER[3], 0.65)]


# ---------------------------------------------------------------------------
# Bausteine fuer Antworten
# ---------------------------------------------------------------------------


def text_block(text: str, citations=None):
    return SimpleNamespace(type="text", text=text, citations=citations or [])


def citation(document_index: int, cited_text: str):
    return SimpleNamespace(type="char_location", document_index=document_index, cited_text=cited_text,
                           start_char_index=0, end_char_index=len(cited_text), document_title="x")


# Tokenverbrauch der Fake-Antworten, wie Message.usage in anthropic 1.4 (vier Felder).
USAGE_STREAM = SimpleNamespace(input_tokens=100, output_tokens=10,
                               cache_creation_input_tokens=5, cache_read_input_tokens=50)
USAGE_PARSE = SimpleNamespace(input_tokens=30, output_tokens=8,
                              cache_creation_input_tokens=0, cache_read_input_tokens=25)


def tool_call(frage: str, id_: str = "tu_1"):
    return SimpleNamespace(type="tool_use", id=id_, name="wissensbasis_suchen", input={"frage": frage})


def msg(content, stop_reason="end_turn", stop_details=None):
    return SimpleNamespace(content=content, stop_reason=stop_reason, stop_details=stop_details,
                           usage=USAGE_STREAM)


def refusal_msg(zug: str):
    return msg([text_block("")], stop_reason="refusal",
               stop_details=SimpleNamespace(type="refusal", category="test", explanation=f"Test-Refusal in {zug}"))


def felder(status="BEWERTET", score=3, begruendung="Begruendung mit Zitat und 3.547.000 EUR.",
           fehlende=None, praezedenz="Glaswerk Nord 2013", hinweis="Vor Freigabe Messprotokoll."):
    return Bewertungsfelder(status=status, score=score, begruendung=begruendung,
                            fehlende_informationen=fehlende or [], praezedenz=praezedenz,
                            entscheidungsrelevanter_hinweis=hinweis)


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
    """Entscheidet aus den Parametern, welcher Zug laeuft, und fuehrt je Systemprompt
    (also je Rolle) einen eigenen Zaehler."""

    def __init__(self, fragen=None, zug_a_stops=None, refusal_in=None, parse_felder=None,
                 parse_stop="end_turn", parse_none=False, essay_text=None, zitat_index=0):
        self.fragen = list(fragen) if fragen is not None else [FRAGE_GLASWERK]
        self.zug_a_stops = list(zug_a_stops or ["end_turn"])
        self.refusal_in = refusal_in
        self.parse_felder = parse_felder
        self.parse_stop = parse_stop
        self.parse_none = parse_none
        self.essay_text = essay_text
        self.zitat_index = zitat_index
        self.stream_aufrufe: list[dict] = []
        self.parse_aufrufe: list[dict] = []
        self._zaehler: dict[str, dict] = {}

    def _rolle(self, kw) -> str:
        sysm = kw.get("system")
        text = sysm[0]["text"] if isinstance(sysm, list) else str(sysm)
        return text[:20000]

    def _z(self, kw) -> dict:
        return self._zaehler.setdefault(self._rolle(kw), {"runden": 0, "zug_a": 0})

    def stream(self, **kw):
        self.stream_aufrufe.append(kw)
        z = self._z(kw)
        if kw.get("tools"):
            z["runden"] += 1
            if self.refusal_in == "runde":
                return FakeStream(refusal_msg("runde"))
            k = z["runden"] - 1
            if k < len(self.fragen):
                return FakeStream(msg([text_block("Ich frage die Wissensbasis."),
                                       tool_call(self.fragen[k], f"tu_{k + 1}")], stop_reason="tool_use"))
            return FakeStream(msg([text_block("Ich habe genug gefunden.")]))
        # Zug A
        z["zug_a"] += 1
        if self.refusal_in == "zug_a":
            return FakeStream(refusal_msg("zug_a"))
        stop = self.zug_a_stops[min(z["zug_a"] - 1, len(self.zug_a_stops) - 1)]
        text = self.essay_text or (
            "**Status:** BEWERTET\n**Score:** 3/10\n**Begruendung:** "
            "Bei Glaswerk Nord war die Anlage technisch in Ordnung, verloren gegangen ist die Marge. "
            "Investition 3.547.000 EUR ohne Deckung.")
        return FakeStream(msg([text_block(text, [citation(self.zitat_index, "verloren gegangen ist die Marge")])],
                              stop_reason=stop))

    def parse(self, **kw):
        self.parse_aufrufe.append(kw)
        if self.refusal_in == "zug_b":
            r = refusal_msg("zug_b")
            r.parsed_output = None
            return r
        if kw.get("response_format") is FragenBuendel:
            buendel = FragenBuendel(fragen=[
                FRAGE_GLASWERK,
                "Welche Richtlinie gilt nach POL-FIN-002 fuer Investitionsvorlagen?",
                "Welche Praezedenzfaelle und Kennzahlen liegen vor?",
            ])
            return SimpleNamespace(content=[], stop_reason=self.parse_stop, stop_details=None,
                                   parsed_output=None if self.parse_none else buendel, usage=USAGE_PARSE)
        f = self.parse_felder if self.parse_felder is not None else felder()
        return SimpleNamespace(content=[], stop_reason=self.parse_stop, stop_details=None,
                               parsed_output=None if self.parse_none else f, usage=USAGE_PARSE)


class FakeClient:
    def __init__(self, **kw):
        self.messages = FakeMessages(**kw)


class FakeQmd:
    """Gefaelschte Wissensbasis. `fehler_anzahl` Aufrufe scheitern zuerst, `immer_fehler`
    laesst jeden scheitern, `leer` liefert nie Treffer, `nur_fuer` beschraenkt Fehler auf
    einen Collection-Satz, `hits_je_frage` liefert je Fragewortlaut eine eigene Rangliste
    (Z12: Auswahl je Abfrage). Optionen des Treibers (Z13 Rueckfall `geraet`/`rerank`,
    `typisiert`) landen in `optionen`, je Aufruf ein dict."""

    def __init__(self, hits=None, fehler_anzahl=0, immer_fehler=False, leer=False, nur_fuer=None,
                 hits_je_frage=None):
        self.hits = list(hits) if hits is not None else list(STANDARD_HITS)
        self.fehler_anzahl = fehler_anzahl
        self.immer_fehler = immer_fehler
        self.leer = leer
        self.nur_fuer = nur_fuer
        self.hits_je_frage = dict(hits_je_frage or {})
        self.aufrufe: list[tuple[str, list[str], int]] = []
        self.optionen: list[dict] = []

    def __call__(self, frage, collections, n, **kw):
        import treiber
        self.aufrufe.append((frage, list(collections), n))
        self.optionen.append(dict(kw))
        betroffen = self.nur_fuer is None or list(collections) == list(self.nur_fuer)
        if betroffen and (self.immer_fehler or self.fehler_anzahl > 0):
            self.fehler_anzahl -= 1
            raise treiber.WissensbasisFehler("CUDA error (Test)")
        if self.leer:
            return []
        if frage in self.hits_je_frage:
            return [dict(h) for h in self.hits_je_frage[frage][:n]]
        return [dict(h) for h in self.hits[:n]]


@pytest.fixture
def lauf(tmp_path):
    return tmp_path / "lauf-test", "lauf-test"


@pytest.fixture
def eisenach():
    for p in EISENACH:
        assert p.exists(), p
    return EISENACH
