"""Konnektor zu einem OpenAI-kompatiblen Endpunkt. Optional, nicht eingebaut.

**Herkunft.** Herausgeloest aus `llm-wiki/app/llm.py` in der Fassung von
`origin/main` (Commit d59cde8, "LLM-Anbindung auf OpenAI-kompatiblen Endpoint
umstellen"). Uebernommen wurde ausschliesslich der Konnektor: Schluesselpruefung,
Client und ein Frage-Antwort-Durchgang. Die Zitatpruefung jener Datei ist
**nicht** uebernommen, weil sie auf der Wortsuche `wiki.search_snippets`
aufsetzt, die in diesem Zweig entfernt bleibt.

**Status.** Nichts in der App importiert dieses Modul. Es aendert kein Verhalten,
solange es niemand einbindet. Auch das Paket `openai` wird erst beim ersten
Aufruf importiert, steht also nicht in `pyproject.toml`; wer den Konnektor
einbaut, traegt es dort nach.

**Wozu.** Zwei Verwendungen sind vorgesehen, beide spaeter zu planen:

1. *Textaufrufe der Wiki-Anwendung* ueber einen austauschbaren Anbieter. Der
   Endpunkt `https://hybridai.one/v1` liefert Claude-Modelle ueber die
   OpenAI-Schnittstelle; das ist ein zweiter Weg zum Modell neben dem direkten
   Anthropic-Zugang, den der Agentenpfad unter `qmd/` nutzt. Beide Konnektoren
   bleiben nebeneinander bestehen, keiner loest den anderen ab.
2. *Einbettungen* ueber `/v1/embeddings` als Alternative zum lokalen
   Nemotron-Modell. Das waere der Weg zu Einbettungen ohne GPU und ohne die
   4,4 Sekunden Ladezeit je Prozess. `embed` unten ist dafuer vorbereitet, aber
   **gegen diesen Endpunkt ungeprueft**: ob er Einbettungen anbietet, welche
   Modellkennung gilt und wie viele Dimensionen zurueckkommen, ist offen. Der
   qmd-Index steht auf 2048 Dimensionen; ein Modell mit anderer Dimensionszahl
   verlangt einen vollstaendigen Neuaufbau der Vektoren.

**Umgebung** (siehe `.env.example` in `origin/main`):

    LLM_BASE_URL=https://hybridai.one/v1   # leer heisst OpenAI direkt
    LLM_API_KEY=
    LLM_MODEL=claude-haiku-4-5-20251001
    LLM_EMBED_MODEL=                       # nur fuer embed(), noch offen
"""
from __future__ import annotations

import os
from typing import Any

DEFAULT_MODEL = "claude-haiku-4-5-20251001"


def is_configured() -> bool:
    """Wahr, wenn ein Schluessel gesetzt ist. Ohne Schluessel kein Aufruf."""
    return bool(os.environ.get("LLM_API_KEY"))


def client() -> Any:
    """Client fuer den konfigurierten OpenAI-kompatiblen Endpunkt.

    `LLM_BASE_URL` zeigt auf den /v1-Pfad des Anbieters. Ist die Variable leer,
    faellt das SDK auf die OpenAI-Standard-URL zurueck; der Endpunkt ist also
    austauschbar, ohne dass Code angefasst werden muss.

    Der Import steht absichtlich in der Funktion: solange niemand den Konnektor
    ruft, braucht das Projekt das Paket `openai` nicht.
    """
    from openai import OpenAI

    return OpenAI(
        base_url=os.environ.get("LLM_BASE_URL") or None,
        api_key=os.environ.get("LLM_API_KEY"),
    )


def chat(system_prompt: str, user_prompt: str, max_tokens: int) -> str:
    """Ein einzelner Frage-Antwort-Durchgang, Klartext zurueck.

    Kein Streaming, keine Werkzeuge, keine Historie. Wortlaut aus der Herkunft
    uebernommen, einschliesslich der Absicherung gegen einen leeren Abschluss:
    `content` kann None sein, die Aufrufer erwarten aber einen String.
    """
    response = client().chat.completions.create(
        model=os.environ.get("LLM_MODEL", DEFAULT_MODEL),
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content or ""


def embed(texte: list[str], modell: str | None = None) -> list[list[float]]:
    """Einbettungen ueber `/v1/embeddings`. **Ungeprueft gegen diesen Endpunkt.**

    Vorbereitung fuer die zweite Verwendung aus dem Modulkopf. Vor einem Einbau
    ist dreierlei zu klaeren: ob der Anbieter Einbettungen anbietet, welche
    Modellkennung gilt, und wie viele Dimensionen zurueckkommen. Weicht die
    Dimensionszahl von den 2048 des qmd-Index ab, muessen alle Vektoren neu
    gebaut werden.
    """
    name = modell or os.environ.get("LLM_EMBED_MODEL")
    if not name:
        raise ValueError(
            "Kein Einbettungsmodell gesetzt (LLM_EMBED_MODEL). Der Konnektor "
            "kennt keinen sinnvollen Vorgabewert, siehe Modulkopf."
        )
    antwort = client().embeddings.create(model=name, input=texte)
    return [d.embedding for d in antwort.data]
