"""Antwort mit Quellenzitat (Paket 10).

Die Antwort ist keine Textwand, sondern eine Liste von Fakten. Zu jedem Fakt
gehoert das **woertliche** Zitat aus der Wissensbasis, aus dem er stammt.

Der Kern ist nicht die huebsche Zitatbox, sondern `_beleg_suchen`: Ein Zitat
wird nur angezeigt, wenn es woertlich in einem der uebergebenen Ausschnitte
steht. Erfundene oder umformulierte Zitate werden verworfen und der Fakt als
"ohne Beleg" gekennzeichnet. Sonst wuerde die Box eine Halluzination
glaubwuerdiger machen, statt sie aufzudecken.

Weil ausschliesslich gegen die uebergebenen Snippets geprueft wird - und die
kommen aus `wiki.search_snippets(frage, user)`, also bereits nach Rechten
gefiltert (Paket 1) - kann ein Zitat nie aus einer Seite stammen, die der
Fragende nicht sehen darf.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field

from .wiki import Snippet

DEFAULT_MODEL = "claude-sonnet-5"

# Belegstelle, die pdf_ingest (Paket 8) in den Absatz schreibt: *(Seite 7)*
SEITE_RE = re.compile(r"\*\(Seite (\d+)\)\*")
WS_RE = re.compile(r"\s+")

# Ein Beleg muss ein Stueck Satz sein. Einzelne Woerter belegen nichts:
# "450" steht in jedem Zahlenwerk, und "Betriebsrat" belegt nicht die Aussage
# "Der Betriebsrat ist einer der vier Experten-Agenten" - das tut erst der
# Satz, in dem das Wort steht. Gemessen wird in Woertern, nicht in Zeichen:
# eine Zeichengrenze trennt willkuerlich ("CFO/Controlling" haette bestanden,
# "CEO/Strategie" nicht).
MIN_ZITAT_WOERTER = 3

SYSTEM_PROMPT = (
    "Du bist der Wiki-Assistent von MediaparkBrain. "
    "Beantworte die Frage ausschliesslich aus dem mitgelieferten Kontext. "
    "Zerlege deine Antwort in einzelne Fakten. Zu jedem Fakt gibst du das "
    "woertliche Zitat an, aus dem er stammt - Zeichen fuer Zeichen aus dem "
    "Kontext kopiert, nicht umformuliert, nicht gekuerzt, nicht zusammengesetzt. "
    "Zitiere immer einen vollstaendigen Satz, nie ein einzelnes Wort und nie eine "
    "Aufzaehlungsposition: erst der ganze Satz belegt die Aussage. "
    "Findest du zu einer Teilfrage nichts im Kontext, sage das als eigenen Fakt "
    "mit leerem Zitat, statt zu spekulieren.\n\n"
    "Antworte ausschliesslich mit JSON in genau dieser Form:\n"
    '{"fakten": [{"aussage": "Der Fakt in einem Satz.", '
    '"zitat": "woertlich aus dem Kontext", "quelle": "Titel der Wiki-Seite"}]}'
)


@dataclass
class Fakt:
    """Eine Aussage samt ihrem Beleg. Ohne `quelle_slug` gilt sie als unbelegt."""

    aussage: str
    zitat: str = ""
    quelle_titel: str = ""
    quelle_slug: str = ""
    belegstelle: str = ""

    @property
    def belegt(self) -> bool:
        return bool(self.quelle_slug and self.zitat)


@dataclass
class Antwort:
    fakten: list[Fakt] = field(default_factory=list)
    hinweis: str = ""

    @property
    def belegte(self) -> list[Fakt]:
        return [f for f in self.fakten if f.belegt]

    @property
    def unbelegte(self) -> list[Fakt]:
        return [f for f in self.fakten if not f.belegt]

    def __bool__(self) -> bool:
        return bool(self.fakten or self.hinweis)


def is_configured() -> bool:
    return bool(os.environ.get("LLM_API_KEY"))


def _client():
    """Client fuer den konfigurierten OpenAI-kompatiblen Endpoint.

    `LLM_BASE_URL` zeigt auf den /v1-Pfad des Anbieters (z.B.
    https://hybridai.one/v1). Ist die Variable leer, faellt das SDK auf die
    OpenAI-Standard-URL zurueck - der Endpoint ist also austauschbar, ohne
    dass Code angefasst werden muss.
    """
    from openai import OpenAI

    return OpenAI(
        base_url=os.environ.get("LLM_BASE_URL") or None,
        api_key=os.environ.get("LLM_API_KEY"),
    )


def _extra_body() -> dict:
    """Anbieterspezifische Felder, die die OpenAI-API selbst nicht kennt.

    hybridai.one verlangt zusaetzlich eine `chatbot_id` im Request-Body und
    antwortet sonst mit 400. Andere OpenAI-kompatible Anbieter kennen das Feld
    nicht, deshalb wird es nur mitgeschickt, wenn LLM_CHATBOT_ID gesetzt ist -
    so bleibt der Endpoint austauschbar.
    """
    chatbot_id = os.environ.get("LLM_CHATBOT_ID", "").strip()
    return {"chatbot_id": chatbot_id} if chatbot_id else {}


def chat(system_prompt: str, user_prompt: str, max_tokens: int) -> str:
    """Ein einzelner Frage-Antwort-Durchgang - der einzige Weg nach aussen.

    Alle drei Aufrufstellen (Zitat-Antwort, Projektbewertung, Dokumentkopf)
    laufen hierueber: ein System-Prompt, eine Nutzerfrage, Klartext zurueck.
    Kein Streaming, keine Tools, keine Historie - genau das, was die App
    braucht.
    """
    response = _client().chat.completions.create(
        model=os.environ.get("LLM_MODEL", DEFAULT_MODEL),
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        extra_body=_extra_body(),
    )
    # Ein leerer Abschluss (content=None) darf die Aufrufer nicht mit einem
    # AttributeError treffen - sie erwarten durchgaengig einen String.
    return response.choices[0].message.content or ""


# ---------------------------------------------------------------------------
# Zitatpruefung - der eigentliche Kern des Pakets
# ---------------------------------------------------------------------------


def _normalisiert(text: str) -> str:
    """Nur Gross-/Kleinschreibung und Leerraum werden geglaettet.

    Ein Zeilenumbruch mitten im Satz darf einen sonst woertlichen Beleg nicht
    entwerten; ein umformulierter Satz bleibt aber ungleich.
    """
    return WS_RE.sub(" ", text).strip().lower()


def _beleg_suchen(zitat: str, snippets: list[Snippet]) -> Snippet | None:
    """Der Ausschnitt, der `zitat` woertlich enthaelt - sonst None."""
    z = _normalisiert(zitat)
    if len(z.split()) < MIN_ZITAT_WOERTER:
        return None
    for s in snippets:
        if z in _normalisiert(s.paragraph):
            return s
    return None


def _belegstelle(paragraph: str) -> str:
    """"Seite 7", falls der Absatz aus einem eingelesenen PDF stammt (Paket 8)."""
    treffer = SEITE_RE.search(paragraph)
    return f"Seite {treffer.group(1)}" if treffer else ""


def pruefe_fakt(aussage: str, zitat: str, snippets: list[Snippet]) -> Fakt:
    """Baut einen Fakt und belegt ihn nur, wenn das Zitat woertlich vorkommt."""
    quelle = _beleg_suchen(zitat, snippets)
    if quelle is None:
        return Fakt(aussage=aussage.strip())
    return Fakt(
        aussage=aussage.strip(),
        zitat=zitat.strip(),
        quelle_titel=quelle.page.title,
        quelle_slug=quelle.page.slug,
        belegstelle=_belegstelle(quelle.paragraph),
    )


# ---------------------------------------------------------------------------
# Modellantwort einlesen
# ---------------------------------------------------------------------------


def _json_aus(text: str) -> dict | None:
    """Holt das JSON-Objekt aus der Modellantwort, auch aus einem Codeblock."""
    start, ende = text.find("{"), text.rfind("}")
    if start == -1 or ende <= start:
        return None
    try:
        daten = json.loads(text[start : ende + 1])
    except json.JSONDecodeError:
        return None
    return daten if isinstance(daten, dict) else None


def _modell_fragen(frage: str, kontext: str) -> str:
    """Der einzige Aufruf nach aussen - in Tests ersetzbar."""
    return chat(
        SYSTEM_PROMPT,
        f"Kontext aus dem Wiki:\n\n{kontext}\n\nFrage: {frage}",
        max_tokens=1024,
    )


# ---------------------------------------------------------------------------
# Oeffentliche Schnittstelle
# ---------------------------------------------------------------------------


def _ohne_modell(snippets: list[Snippet]) -> Antwort:
    """Ohne API-Key gibt es keine Aussagen - aber die Belege gibt es trotzdem."""
    fakten = [
        Fakt(
            aussage="",
            zitat=s.paragraph,
            quelle_titel=s.page.title,
            quelle_slug=s.page.slug,
            belegstelle=_belegstelle(s.paragraph),
        )
        for s in snippets
    ]
    return Antwort(
        fakten=fakten,
        hinweis=(
            "Kein LLM_API_KEY gesetzt - unten stehen die gefundenen "
            "Belegstellen, aber keine daraus formulierte Antwort."
        ),
    )


def ask_llm(question: str, snippets: list[Snippet]) -> Antwort:
    """Beantwortet die Frage als Liste belegter Fakten.

    `snippets` ist bereits nach Rechten gefiltert; es wird ausschliesslich
    dagegen belegt.
    """
    if not snippets:
        return Antwort(
            hinweis="Dazu findet sich nichts im Wiki. Lege ggf. eine neue Seite dazu an."
        )

    if not is_configured():
        return _ohne_modell(snippets)

    kontext = "\n\n".join(f"### {s.page.title}\n{s.paragraph}" for s in snippets)
    rohtext = _modell_fragen(question, kontext)
    daten = _json_aus(rohtext)

    if daten is None or not isinstance(daten.get("fakten"), list):
        # Unerwartetes Format: die Antwort geht nicht verloren, gilt aber als
        # unbelegt - lieber sichtbar ohne Beleg als scheinbar belegt.
        return Antwort(
            fakten=[Fakt(aussage=rohtext.strip())] if rohtext.strip() else [],
            hinweis="Die Antwort kam in unerwartetem Format und konnte nicht belegt werden.",
        )

    fakten = [
        pruefe_fakt(str(eintrag.get("aussage", "")), str(eintrag.get("zitat", "")), snippets)
        for eintrag in daten["fakten"]
        if isinstance(eintrag, dict) and str(eintrag.get("aussage", "")).strip()
    ]
    antwort = Antwort(fakten=fakten)
    if antwort.unbelegte:
        antwort.hinweis = (
            f"{len(antwort.unbelegte)} von {len(fakten)} Aussagen konnten nicht mit "
            "einem woertlichen Zitat aus der Wissensbasis belegt werden."
        )
    return antwort
