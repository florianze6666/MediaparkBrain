"""Anthropic-Konfiguration fuer die App.

Die Frage-Route /ask samt `ask_llm` (Antwort aus Wortsuche-Treffern) ist am
06.09.2026 entfernt worden. Gesucht wird ausschliesslich ueber die
Embedding-Suche im Teilprojekt qmd/ (docs/wissensspeicher-qmd.md). Uebrig
bleibt die Pruefung des API-Schluessels (die Bewertung laeuft seit Phase 4 im
Orchestrator unter qmd/agenten/, siehe app/bewertung.py).
"""
from __future__ import annotations

import os


def is_configured() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))
