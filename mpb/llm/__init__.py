"""LLM-Schicht: eine Funktion, austauschbar. Tests laufen mit MockProvider."""
from __future__ import annotations
from typing import Any
from mpb.types import Completion, LLMProvider
from mpb.config import Settings


class MockProvider:
    """Deterministisch. Antwortet mit dem Inhalt von `canned[key]`, key = erster Wert aus
    messages[-1]['content'] der wie 'ROLE:<name>' aussieht, sonst mit `default`."""

    def __init__(self, canned: dict[str, str] | None = None, default: str = "{}"):
        self.canned = canned or {}
        self.default = default
        self.calls: list[dict[str, Any]] = []

    def complete(self, system, messages, tools=None, model=None, max_tokens=2048) -> Completion:
        self.calls.append({"system": system, "messages": messages, "tools": tools, "model": model})
        text = self.default
        last = messages[-1]["content"] if messages else ""
        for key, val in self.canned.items():
            if key in str(last) or key in system:
                text = val
                break
        return Completion(text=text, model=model or "mock", usage={"input": 0, "output": 0})


def get_provider(settings: Settings | None = None) -> LLMProvider:
    settings = settings or Settings()
    if settings.llm_provider == "anthropic":
        from mpb.llm.anthropic_provider import AnthropicProvider  # lazy: SDK nur wenn gebraucht
        return AnthropicProvider(settings)
    return MockProvider()
