from __future__ import annotations

import os

from .wiki import Snippet

DEFAULT_MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = (
    "Du bist der Wiki-Assistent von MediaparkBrain. "
    "Beantworte die Frage ausschliesslich auf Basis des mitgelieferten Kontexts aus dem internen Wiki. "
    "Wenn die Antwort nicht im Kontext enthalten ist, sage das explizit, statt zu spekulieren. "
    "Antworte auf Deutsch, kurz und praezise, und nenne die Titel der verwendeten Wiki-Seiten."
)


def is_configured() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def ask_llm(question: str, snippets: list[Snippet]) -> str:
    if not snippets:
        return "Dazu findet sich nichts im Wiki. Lege ggf. eine neue Seite dazu an."

    context = "\n\n".join(
        f"### {s.page.title}\n{s.paragraph}" for s in snippets
    )

    if not is_configured():
        return (
            "Kein ANTHROPIC_API_KEY gesetzt - zeige nur passende Wiki-Ausschnitte "
            "(reine Volltextsuche, keine LLM-Antwort):\n\n" + context
        )

    from anthropic import Anthropic

    client = Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Kontext aus dem Wiki:\n\n{context}\n\nFrage: {question}",
            }
        ],
    )
    return "".join(block.text for block in response.content if block.type == "text")
