"""Die sechs Schritte einer Rolle (Plan 09, Abschnitt 2 B und 4.3).

Drei Modellaufrufe statt sieben bis neun: Fragenbuendel, Essay mit Zitaten, Felder.
Keine Werkzeugrunden mehr -- der Agent hat GENAU EINE Gelegenheit zu fragen, und der
Prompt sagt ihm das.

Warum das Fragenbuendel ueber ein Werkzeug und nicht ueber Structured Output laeuft:
Zitate (`citations`) und `output_config.format` schliessen sich in der API aus (400).
Der Kontext traegt ab Abschnitt A Dokumente mit eingeschalteten Zitaten, also kann Zug 1
kein Structured Output verwenden, ohne den geteilten Praefix zu veraendern und damit die
Zwischenspeicherung zu verlieren. Ein Werkzeug mit `strict: true` liefert dieselbe
Formgarantie und vertraegt sich mit Zitaten. Zug B kommt ohne Dokumente aus und nutzt
deshalb `messages.parse`.

Kennt nicht: Aggregation, andere Rollen.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

from pydantic import BaseModel, Field, ValidationError

AGENTEN_DIR = Path(__file__).resolve().parent
QMD_DIR = AGENTEN_DIR.parent
ROOT = QMD_DIR.parent
sys.path.insert(0, str(AGENTEN_DIR))
sys.path.insert(0, str(QMD_DIR / "ingest"))

import suche  # noqa: E402
from kontext import Block, Dokument  # noqa: E402
from rollen import RollenFehler, collections_for_role  # noqa: E402
from schema import Bewertungsfelder, Zeile  # noqa: E402

MODELL = os.environ.get("EVAL_MODEL", "claude-sonnet-5")   # Plan 09, Festlegung 6

# --- Manifest: die einzige hartcodierte Stelle -----------------------------
# Der Orchestrator liest ROLLEN_KONFIG und neutrale_bloecke() von hier, damit
# Rollenwissen und Prompttexte an einer Stelle stehen.
BEWERTUNGSLOGIK = "Bewertungslogik_Experten-Agent.md"
ROLLEN_KONFIG: dict[str, dict[str, str]] = {
    "betriebsrat": {
        "nutzer": "betriebsrat",
        "persona": "persona/betriebsrats_persona.md",
        "kalibrierung": "persona/betriebsrats_kriterienkalibrierung.md",
    },
    "cfo": {
        "nutzer": "cfo",
        "persona": "persona/cfo_persona.md",
        "kalibrierung": "persona/cfo_kriterienkalibrierung.md",
    },
    "it": {
        "nutzer": "it-security",
        "persona": "persona/it_persona.md",
        "kalibrierung": "persona/it_kriterienkalibrierung.md",
    },
    "ceo": {
        "nutzer": "ceo",
        "persona": "persona/ceo_persona.md",
        "kalibrierung": "persona/ceo_kriterienkalibrierung.md",
    },
}
FRAGEN_JE_BUENDEL = 3        # Festlegung 2
ROLLEN_DOKUMENTE = 4         # Festlegung 3: drei bis fuenf rollenspezifisch
TREFFER_JE_FRAGE = 8
ZUG_1_MAX_TOKENS = 8000
ZUG_A_MAX_TOKENS = 12000
ZUG_B_MAX_TOKENS = 4000


class FragenBuendel(BaseModel):
    """Genau drei Fragen. Form wird ueber das Werkzeugschema erzwungen, hier geprueft."""

    fragen: list[str] = Field(
        min_length=FRAGEN_JE_BUENDEL,
        max_length=FRAGEN_JE_BUENDEL,
        description="Genau 3 praezise, eigenstaendige Recherchefragen an die Wissensbasis",
    )


class RollenlaufFehler(Exception):
    """Fehler, der den Lauf dieser Rolle beendet."""


class TechnischerFehler(RollenlaufFehler):
    def __init__(self, art: str, details: Any = None) -> None:
        super().__init__(f"{art}: {details}")
        self.art = art
        self.details = details


# ---------------------------------------------------------------------------
# Prompttexte
# ---------------------------------------------------------------------------

INITIALTEIL = """Du bist ein Experten-Gutachter in einem Multi-Stakeholder-Bewertungsprozess
fuer Projektportfolio-Entscheidungen der Lahnberg Thermotechnik GmbH & Co. KG.

## Deine Aufgabe

Du bewertest EIN Vorhaben aus GENAU EINER Perspektive, naemlich der weiter unten
beschriebenen Rolle. Du bist nicht der Orchestrator und nicht der Entscheider. Andere
Rollen bewerten dasselbe Vorhaben getrennt; du nimmst ihre Urteile nicht vorweg.

## Die Wissensbasis

Sie enthaelt 218 Dokumente der Lahnberg Thermotechnik aus den Jahren 2011 bis 2025 in
neun Ablageorten: Projektreviews und Lessons Learned, Protokolle von Steering, Beirat
und Betriebsrat, gelenkte Richtlinien (POL-...), Management Summaries, Beiratsvorlagen
und Investitionsantraege, Mailverkehr, Organigramme, Kennzahlenberichte und die
Unternehmenschronik.

**Was sie nicht enthaelt:** keine Budgetrahmen oder Investitionsplaene kuenftiger Jahre,
keine Energiepreis-, CO2- oder Marktpraemissen, keine Angebote oder Unterlagen Dritter,
nichts nach 2025. Danach zu fragen bringt nichts. Fehlt dir so etwas fuer die Bewertung,
ist es eine Informationsluecke des Antrags.

Du siehst nur, was deine Rolle sehen darf. Bleiben Bereiche verschlossen, ist das kein
Fehler, sondern gehoert als Informationsluecke in die Bewertung.

## Wie dieser Ablauf aussieht

Zusammen mit dem Antrag hast du bereits einige Grundlagendokumente erhalten, die fuer
alle Rollen gleich sind. Danach bekommst du **genau eine** Gelegenheit, eigene Fragen an
die Wissensbasis zu stellen: drei Fragen, in einem Zug. **Es folgt keine zweite Runde.**
Auf die Treffer hin schreibst du unmittelbar deine Bewertung.

Was du nicht findest, erfindest du nicht. Fehlt eine Information, benennst du die Luecke
ausdruecklich.
"""

FRAGEN_AUFTRAG = """## Deine drei Fragen

Oben stehen der Projektantrag und die gemeinsamen Grundlagendokumente, darunter deine
Rollenbeschreibung und dein Kriterienkatalog.

Stelle jetzt **genau drei** Fragen an die Wissensbasis, ueber das Werkzeug
`recherchefragen`, in einem einzigen Aufruf. **Du hast genau diesen einen Versuch; eine
zweite Runde gibt es nicht.** Waehle die drei Fragen deshalb so, dass sie zusammen deinen
Informationsbedarf abdecken, und stelle keine, deren Antwort schon in den beigefuegten
Dokumenten steht.

Richte sie aus:

1. **Zuerst der erinnerte Fall, mit Namen und Jahr.** Deine Rollenbeschreibung enthaelt
   Erfahrungen aus frueheren Vorhaben. Erinnert dich der Antrag an einen davon, ist das
   die wichtigste Spur; nenne ihn beim Namen.
2. **Die Regel, die daraus wurde** -- Richtlinie, Beschluss oder Vereinbarung, an der
   das Vorhaben zu messen ist.
3. **Der offene Punkt deiner Perspektive**, den weder Antrag noch Grundlagen klaeren.

Formuliere in ganzen Saetzen, so wie du sie einem Archivar stellen wuerdest.
"""

# Kein `minItems`/`maxItems` im Schema: die Schnittstelle laesst fuer Arrays nur die
# Werte 0 und 1 zu und lehnt alles andere mit HTTP 400 ab
# ("For 'array' type, 'minItems' values other than 0 or 1 are not supported").
# Der Integrationslauf vom 06.09.2026 ist daran in allen vier Rollen gescheitert.
# Die Dreizahl wird deshalb dreifach abgesichert, ohne Schema-Zwang: im Beschreibungstext
# des Werkzeugs, im Frageauftrag, und danach in Python ueber `FragenBuendel`. Liefert das
# Modell zwei oder vier Fragen, ist das ein Protokolleintrag und kein technischer Fehler;
# ein Lauf darf daran nicht scheitern.
FRAGEN_TOOL = [{
    "name": "recherchefragen",
    "description": (
        "Uebergibt GENAU DREI Recherchefragen an die Wissensbasis - nicht zwei, nicht vier. "
        "Ein einziger Aufruf, danach folgt unmittelbar die Bewertung; eine zweite Runde "
        "gibt es nicht."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "fragen": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "GENAU DREI Fragen in eigenen Worten, je ein ganzer Satz. Die Liste "
                    "muss drei Eintraege haben."
                ),
            }
        },
        "required": ["fragen"],
        "additionalProperties": False,
    },
    "strict": True,
}]

ABSCHLUSS_AUFTRAG_A = """## Jetzt bewerten

Oben stehen die Dokumente, die deine drei Fragen geliefert haben, dazu die gemeinsamen
Grundlagen. Weitere Fragen sind nicht moeglich. Erstelle nun deine abschliessende
Bewertung als Fliesstext nach Kapitel 12 der Bewertungslogik.

Zwingend:

1. **Zitiere woertlich** aus den beigefuegten Dokumenten. Deine Begruendung muss den
   Satz enthalten, der deine Einschaetzung traegt, unveraendert.
2. Nenne mindestens einen Betrag oder eine Regelbezugnahme mit Fassung.
3. Wenn dich das Vorhaben an einen frueheren Fall erinnert, benenne ihn und belege ihn
   aus den Dokumenten.
4. Halte die Gliederung aus Kapitel 12 ein: Status, Score (oder KEIN SCORE),
   Begruendung, gegebenenfalls Entscheidungsrelevanter Hinweis, bei INFORMATION FEHLT
   die Liste der fehlenden Informationen und warum sie benoetigt werden.
5. Was du wegen der begrenzten Recherche nicht pruefen konntest, gilt als nicht belegt,
   nicht als nicht vorhanden. Benenne es als Informationsluecke.
6. **Laenge:** Fasse dich praezise und substanziell (ca. 800 bis 1.200 Woerter). Konzentriere
   dich auf die tragenden Kernargumente und Zitate.

Kein JSON. Die maschinenlesbare Fassung entsteht in einem zweiten Schritt aus diesem
Text.
"""

KUERZER_ZUSATZ = (
    "\n\nHinweis: Deine vorige Fassung wurde am Tokenlimit abgeschnitten. Fasse dich "
    "deutlich kuerzer; die Zitate und die Gliederung nach Kapitel 12 bleiben Pflicht."
)

ZUG_B_AUFTRAG = """Uebertrage deine Bewertung von oben unveraendert in das vorgegebene Schema.
Kein neues Urteil, keine neue Abwaegung: Status, Score, Begruendung, fehlende
Informationen, Praezedenz und entscheidungsrelevanter Hinweis genau so, wie sie in
deinem Text stehen. Bei INFORMATION FEHLT ist score null. Die Begruendung uebernimmt
den tragenden Satz mit dem woertlichen Zitat und dem Betrag oder Regelbezug."""


# ---------------------------------------------------------------------------
# Prompt-Bausteine
# ---------------------------------------------------------------------------


def lies(rel: str) -> str:
    """Laedt ein Prompt-Modul. Bricht laut ab, wenn es fehlt oder leer ist."""
    f = ROOT / rel
    if not f.exists():
        raise TechnischerFehler("prompt_modul_fehlt", str(f))
    text = f.read_text(encoding="utf-8")
    if not text.strip():
        raise TechnischerFehler("prompt_modul_leer", str(f))
    return text


def rollen_konfig(rolle: str) -> dict[str, str]:
    if rolle not in ROLLEN_KONFIG:
        raise TechnischerFehler(
            "unbekannte_rolle", f"{rolle!r}; erlaubt: {', '.join(ROLLEN_KONFIG)}")
    return ROLLEN_KONFIG[rolle]


def neutrale_bloecke() -> list[Block]:
    """Die rollenneutralen Systembloecke des geteilten Anfangs (Abschnitt A).

    Der Orchestrator baut damit den Praefix; hier stehen sie, damit Prompttexte an einer
    Stelle liegen und keine zweite Fassung entsteht.
    """
    return [
        Block.system(INITIALTEIL, quelle="INITIALTEIL"),
        Block.system(lies(BEWERTUNGSLOGIK), quelle=BEWERTUNGSLOGIK),
    ]


def rollen_block(rolle: str) -> Block:
    """Persona und Kalibrierung als Nutzernachricht HINTER dem Zwischenspeicherpunkt."""
    k = rollen_konfig(rolle)
    text = (
        f"{'=' * 78}\n# MODUL: Rollen-Persona ({k['persona']})\n{'=' * 78}\n\n"
        f"{lies(k['persona'])}\n\n"
        f"{'=' * 78}\n# MODUL: Rollenspezifische Kalibrierung ({k['kalibrierung']})\n{'=' * 78}\n\n"
        f"{lies(k['kalibrierung'])}"
    )
    return Block.user(text, quelle=k["persona"])


# ---------------------------------------------------------------------------
# API-Hilfen (Form aus treiber.py uebernommen)
# ---------------------------------------------------------------------------

_USAGE_FELDER = ("input_tokens", "output_tokens",
                 "cache_creation_input_tokens", "cache_read_input_tokens")


def _jetzt() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stream(client, **kw):
    """Streaming bei grossem max_tokens; get_final_message liefert das Ganze."""
    with client.messages.stream(**kw) as s:
        return s.get_final_message()


def _stop_details(resp) -> Optional[dict]:
    sd = getattr(resp, "stop_details", None)
    if sd is None:
        return None
    return {"type": getattr(sd, "type", None), "category": getattr(sd, "category", None),
            "explanation": getattr(sd, "explanation", None)}


def _usage(resp) -> dict:
    u = getattr(resp, "usage", None)
    return {k: int(getattr(u, k, 0) or 0) for k in _USAGE_FELDER}


def _erfasse_usage(protokoll: dict, zug: str, resp) -> None:
    u = _usage(resp)
    protokoll.setdefault("api_aufrufe", []).append({"zug": zug, **u})
    t = protokoll.setdefault("tokens", {**{k: 0 for k in _USAGE_FELDER}, "aufrufe": 0})
    for k in _USAGE_FELDER:
        t[k] += u[k]
    t["aufrufe"] += 1


def _pruefe_refusal(resp, wo: str) -> None:
    if getattr(resp, "stop_reason", None) == "refusal":
        raise TechnischerFehler("refusal", {"zug": wo, "stop_details": _stop_details(resp)})


def _textbloecke(resp) -> list:
    return [b for b in getattr(resp, "content", []) if getattr(b, "type", None) == "text"]


def _essay_text(resp) -> str:
    return "".join(getattr(b, "text", "") for b in _textbloecke(resp))


def _zitate(resp, doks: list[Dokument]) -> list[dict]:
    """`document_index` zeigt in die Reihenfolge der document-Bloecke, also in
    Kontext.dokumente()."""
    out = []
    for b in _textbloecke(resp):
        for z in (getattr(b, "citations", None) or []):
            idx = getattr(z, "document_index", None)
            if idx is None or not 0 <= idx < len(doks):
                continue
            out.append({
                "datei": doks[idx].quelle,
                "document_index": idx,
                "cited_text": getattr(z, "cited_text", "") or "",
                "start_char_index": getattr(z, "start_char_index", None),
                "end_char_index": getattr(z, "end_char_index", None),
            })
    return out


_SCORE_IM_TEXT = re.compile(r"score\W{0,6}(\d{1,2})\s*/\s*10", re.I)
_KEIN_SCORE_IM_TEXT = re.compile(r"kein\s+score", re.I)


def score_im_essay(essay: str) -> Optional[int] | str:
    """Konsistenzpruefung ohne Urteil: was der Fliesstext als Score nennt."""
    m = _SCORE_IM_TEXT.search(essay)
    if m:
        return int(m.group(1))
    if _KEIN_SCORE_IM_TEXT.search(essay):
        return "KEIN SCORE"
    return None


def _schreibe_protokoll(lauf_dir: Path, rolle: str, protokoll: dict) -> Path:
    lauf_dir.mkdir(parents=True, exist_ok=True)
    f = lauf_dir / f"{rolle}.protokoll.json"
    f.write_text(json.dumps(protokoll, ensure_ascii=False, indent=2), encoding="utf-8")
    return f


def _fragen_aus(resp, protokoll: dict[str, Any] | None = None) -> list[str]:
    """Liest den Werkzeugaufruf aus Zug 1. Ohne Aufruf gibt es nichts zu suchen.

    Die Dreizahl kann das Schema nicht erzwingen (siehe FRAGEN_TOOL), deshalb wird sie
    hier geprueft. Eine Abweichung ist ein Befund, kein Abbruch: zu viele Fragen werden
    auf drei gekuerzt, zu wenige gehen so weiter, und beides steht als
    `fragen_abweichung` im Protokoll.
    """
    for b in getattr(resp, "content", []):
        if getattr(b, "type", None) == "tool_use" and getattr(b, "name", "") == "recherchefragen":
            roh = (getattr(b, "input", None) or {}).get("fragen") or []
            fragen = [f.strip() for f in roh if isinstance(f, str) and f.strip()]
            if not fragen:
                raise TechnischerFehler("fragen_leer", "Werkzeugaufruf ohne Fragen")
            try:
                FragenBuendel(fragen=fragen)
            except ValidationError:
                if protokoll is not None:
                    protokoll["fragen_abweichung"] = (
                        f"{len(fragen)} statt {FRAGEN_JE_BUENDEL} Fragen geliefert"
                    )
            return fragen[:FRAGEN_JE_BUENDEL]
    raise TechnischerFehler("kein_fragenbuendel",
                            "Zug 1 ohne Werkzeugaufruf `recherchefragen` (FR-04)")


# ---------------------------------------------------------------------------
# Der Rollenlauf
# ---------------------------------------------------------------------------


def rollenlauf(
    basis: Any,                 # kontext.Kontext, versiegelt
    prae_quellen: list[str],    # Pfade der Prae-Dokumente aus Abschnitt A
    rolle: str,
    lauf_dir: Path,
    bruecke: Any = None,        # suche.Bruecke
    index: Any = None,          # (vektoren, metadaten) aus suche.lade_index_vektoren
    client: Any = None,         # anthropic.Anthropic; None erzeugt einen
    modell: str = MODELL,
    on_cache_warm: Optional[Callable[[], None]] = None,
) -> dict[str, Any]:
    """Ein vollstaendiger Rollenlauf. Schreibt <rolle>.jsonl und <rolle>.protokoll.json.

    Schritt 0: Protokoll-Rumpf SOFORT schreiben, damit das Dashboard den Start sieht.
    Schritt 1: basis.fork(), Persona und Kalibrierung als Folgenachricht anhaengen.
    Schritt 2: Modellaufruf 1, drei Fragen ueber das Werkzeug `recherchefragen`.
    Schritt 3: Fragen einbetten, suchen gegen collections_for_role(nutzer).
    Schritt 4: dedup_und_top_k gegen prae_quellen, Dokumente anhaengen.
    Schritt 5: Modellaufruf 2, Essay mit citations, Streaming.
    Schritt 6: Modellaufruf 3, Felder ueber Structured Output (schema.Bewertungsfelder).

    Ein technischer Fehler wird ZURUECKGEGEBEN, nicht geworfen (Z9): die uebrigen
    Rollen laufen weiter. Rueckgabe enthaelt mindestens
    {rolle, ok: bool, zeile | technischer_fehler}.
    """
    t0 = time.time()
    lauf_dir = Path(lauf_dir)
    lauf_id = lauf_dir.name
    protokoll: dict[str, Any] = {
        "rolle": rolle, "lauf_id": lauf_id, "modell": modell, "zeitpunkt": _jetzt(),
        "prompt_version": None, "collections": None,
        "fragen": [], "rag_abfragen": [], "dokumente_im_kontext": [],
        "prae_quellen": list(prae_quellen), "zitate": [], "stop_reasons": {},
        "zeiten_s": {}, "score_im_essay": None, "score_abweichung": None,
        "technischer_fehler": None, "essay": None, "zug_b_felder": None,
        "api_aufrufe": [], "tokens": {**{k: 0 for k in _USAGE_FELDER}, "aufrufe": 0},
    }
    # Schritt 0: der Rumpf liegt sofort auf der Platte (Dashboard-Fortschritt).
    _schreibe_protokoll(lauf_dir, rolle, protokoll)

    try:
        # ---- Schritt 1: forken, Rolle anhaengen ----------------------------
        k = rollen_konfig(rolle)
        try:
            collections = collections_for_role(k["nutzer"])
        except RollenFehler as e:
            raise TechnischerFehler("rolle_ohne_index_zugriff", str(e))
        protokoll["collections"] = collections

        kontext = basis.fork()
        kontext.append(rollen_block(rolle))
        protokoll["prompt_version"] = kontext.fingerprint()

        if client is None:
            from anthropic import Anthropic
            client = Anthropic()

        system = kontext.system()

        # ---- Schritt 2: das Fragenbuendel ----------------------------------
        t = time.time()
        msgs_1 = kontext.messages() + [
            {"role": "user", "content": [{"type": "text", "text": FRAGEN_AUFTRAG}]}
        ]
        resp1 = _stream(client, model=modell, max_tokens=ZUG_1_MAX_TOKENS, system=system,
                        messages=msgs_1, tools=FRAGEN_TOOL)
        protokoll["stop_reasons"]["zug_1"] = getattr(resp1, "stop_reason", None)
        _erfasse_usage(protokoll, "zug_1", resp1)
        _pruefe_refusal(resp1, "zug_1")
        fragen = _fragen_aus(resp1, protokoll)
        protokoll["fragen"] = fragen
        protokoll["zeiten_s"]["zug_1"] = round(time.time() - t, 1)

        # Zug 1 hat das Praefix mit cache_control an Anthropic uebertragen.
        # Sobald der Tool-Call 'recherchefragen' da ist, liegt der Praefix-Cache
        # im Server-RAM. Jetzt koennen die Folgerollen aus dem Cache lesen.
        if on_cache_warm is not None:
            try:
                on_cache_warm()
            except Exception:  # noqa: BLE001
                pass

        # ---- Schritt 3: einbetten und suchen -------------------------------
        t = time.time()
        if bruecke is None:
            bruecke = suche.bruecke_start()
        if index is None:
            index = suche.lade_index_vektoren()
        ivek, imeta = index
        # Stoerungen der Bruecke und der Suche werfen suche.SucheFehler; der wird
        # weiter unten als technischer Fehler "wissensbasis" eingeordnet.
        vektoren = bruecke.embed(fragen)

        treffer_listen: list[list[dict]] = []
        for frage, vek in zip(fragen, vektoren):
            treffer = suche.suche_vektoriell(vek, collections, ivek, imeta,
                                             top_n=TREFFER_JE_FRAGE)
            # Harte Zusicherung zur Informationsgrenze (T-N2).
            fremd = [t_["quelle"] for t_ in treffer if t_.get("collection") not in collections]
            if fremd:
                raise TechnischerFehler(
                    "collection_verletzt",
                    f"Treffer ausserhalb der erlaubten Collections {collections}: {fremd[:3]}")
            treffer_listen.append(treffer)
            protokoll["rag_abfragen"].append({
                "frage": frage,
                "treffer": [{"datei": t_["quelle"], "score": float(t_.get("score") or 0.0)}
                            for t_ in treffer],
            })
        protokoll["zeiten_s"]["suche"] = round(time.time() - t, 2)

        if not any(treffer_listen):
            raise TechnischerFehler("keine_treffer",
                                    "Keine der drei Fragen lieferte Treffer (Z3)")

        # ---- Schritt 4: Dedup, Dokumente in den Kontext ---------------------
        neu = suche.dedup_und_top_k(treffer_listen, list(prae_quellen),
                                    ziel_anzahl=ROLLEN_DOKUMENTE)
        doks_neu = [
            Dokument(
                quelle=h["quelle"],
                titel=h.get("titel") or Path(h["quelle"]).stem,
                collection=h["collection"],
                text=suche.lies_dokument(h["quelle"]),
                score=float(h.get("score") or 0.0),
            )
            for h in neu
        ]
        if doks_neu:
            kontext.append(Block.dokumente_block(doks_neu, quelle="rollendokumente"))
        alle_doks = kontext.dokumente()
        protokoll["dokumente_im_kontext"] = [
            {"datei": d.quelle, "collection": d.collection, "score": d.score,
             "aus_basis": d.quelle in set(prae_quellen)}
            for d in alle_doks
        ]

        # ---- Schritt 5: Zug A, Essay mit Zitaten ---------------------------
        t = time.time()
        essay_resp = None
        for versuch, auftrag in enumerate(
                (ABSCHLUSS_AUFTRAG_A, ABSCHLUSS_AUFTRAG_A + KUERZER_ZUSATZ), 1):
            msgs_a = kontext.messages() + [
                {"role": "user", "content": [{"type": "text", "text": auftrag}]}
            ]
            resp = _stream(client, model=modell, max_tokens=ZUG_A_MAX_TOKENS,
                           system=system, messages=msgs_a)
            protokoll["stop_reasons"][f"zug_a_{versuch}"] = getattr(resp, "stop_reason", None)
            _erfasse_usage(protokoll, f"zug_a_{versuch}", resp)
            _pruefe_refusal(resp, f"zug_a_{versuch}")
            if getattr(resp, "stop_reason", None) == "max_tokens":
                continue          # genau eine Wiederholung mit dem Zusatz "kuerzer"
            essay_resp = resp
            break
        if essay_resp is None:
            raise TechnischerFehler("max_tokens", "Zug A zweimal am Tokenlimit abgeschnitten")
        protokoll["zeiten_s"]["zug_a"] = round(time.time() - t, 1)
        essay = _essay_text(essay_resp)
        protokoll["essay"] = essay
        protokoll["zitate"] = _zitate(essay_resp, alle_doks)
        protokoll["score_im_essay"] = score_im_essay(essay)

        # ---- Schritt 6: Zug B, Felder --------------------------------------
        # Ohne Dokumente, weil Zitate und Structured Output sich ausschliessen.
        t = time.time()
        msgs_b = [
            {"role": "user", "content": "Erstelle deine Bewertung zu dem oben genannten Vorhaben."},
            {"role": "assistant", "content": essay if essay.strip() else "(leer)"},
            {"role": "user", "content": ZUG_B_AUFTRAG},
        ]
        resp_b = client.messages.parse(model=modell, max_tokens=ZUG_B_MAX_TOKENS,
                                       system=system, messages=msgs_b,
                                       output_format=Bewertungsfelder)
        protokoll["stop_reasons"]["zug_b"] = getattr(resp_b, "stop_reason", None)
        _erfasse_usage(protokoll, "zug_b", resp_b)
        _pruefe_refusal(resp_b, "zug_b")
        felder = getattr(resp_b, "parsed_output", None)
        if felder is None:
            raise TechnischerFehler(
                "structured_output",
                f"Zug B ohne parsed_output, stop_reason {getattr(resp_b, 'stop_reason', None)}")
        protokoll["zeiten_s"]["zug_b"] = round(time.time() - t, 1)
        protokoll["zug_b_felder"] = felder.model_dump()

        # ---- Zeile nach Kapitel 17 (AE-04) ---------------------------------
        quellen = sorted({f"corpus/{z['datei']}" for z in protokoll["zitate"]})
        try:
            zeile = Zeile.aus_feldern(rolle, felder, quellen)
        except ValidationError as e:
            raise TechnischerFehler("17.5", "; ".join(err["msg"] for err in e.errors()))

        s_essay = protokoll["score_im_essay"]
        if s_essay is not None:
            feld = zeile.score if zeile.status == "BEWERTET" else "KEIN SCORE"
            if s_essay != feld:
                protokoll["score_abweichung"] = {"essay": s_essay, "feld": feld,
                                                 "regel": "das Feld gilt (Kapitel 17)"}

        lauf_dir.mkdir(parents=True, exist_ok=True)
        (lauf_dir / f"{rolle}.jsonl").write_text(zeile.als_jsonl() + "\n", encoding="utf-8")
        protokoll["zeiten_s"]["gesamt"] = round(time.time() - t0, 1)
        _schreibe_protokoll(lauf_dir, rolle, protokoll)
        return {"rolle": rolle, "ok": True, "zeile": zeile, "protokoll": protokoll}

    except TechnischerFehler as e:
        protokoll["technischer_fehler"] = {"art": e.art, "details": e.details}
    except suche.SucheFehler as e:
        # Bruecke tot, Index unlesbar, Dokument fehlt: kein Urteil ueber den Inhalt.
        protokoll["technischer_fehler"] = {"art": "wissensbasis", "details": str(e)}
    except Exception as e:  # noqa: BLE001 - jede Ausnahme ist ein technischer Fehler der Rolle
        protokoll["technischer_fehler"] = {"art": type(e).__name__, "details": str(e)}

    protokoll["zeiten_s"]["gesamt"] = round(time.time() - t0, 1)
    _schreibe_protokoll(lauf_dir, rolle, protokoll)
    return {"rolle": rolle, "ok": False,
            "technischer_fehler": protokoll["technischer_fehler"], "protokoll": protokoll}
