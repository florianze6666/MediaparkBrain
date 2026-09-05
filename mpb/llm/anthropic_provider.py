"""Anthropic-Adapter. Vor der Implementierung das claude-api-Skill laden (Model-IDs, Caching, Tool-Use)."""
from __future__ import annotations
from typing import Any
from mpb.types import Completion
from mpb.config import Settings


class AnthropicProvider:
    def __init__(self, settings: Settings):
        import anthropic  # noqa: F401
        self.settings = settings
        self.client = anthropic.Anthropic()

    def complete(self, system: str, messages: list[dict[str, Any]], tools=None, model=None, max_tokens=2048) -> Completion:
        model = model or self.settings.model_agent
        kwargs: dict[str, Any] = dict(model=model, system=system, messages=messages, max_tokens=max_tokens)
        if tools:
            kwargs["tools"] = tools
        resp = self.client.messages.create(**kwargs)
        text = "".join(getattr(b, "text", "") for b in resp.content if getattr(b, "type", "") == "text")
        tool_calls = [b.model_dump() for b in resp.content if getattr(b, "type", "") == "tool_use"]
        usage = {"input": resp.usage.input_tokens, "output": resp.usage.output_tokens}
        return Completion(text=text, model=model, usage=usage, tool_calls=tool_calls)
