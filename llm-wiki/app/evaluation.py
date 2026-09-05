from __future__ import annotations

import json
import logging
import os

from .llm import is_configured as llm_is_configured
from .proposals import Proposal

DEFAULT_MODEL = "claude-haiku-4-5-20251001"
log = logging.getLogger(__name__)

# Kurzfassung der vier Experten-Dimensionen aus PLAN.md §6.
ROLE_CRITERIA = {
    "betriebsrat": {
        "name": "Betriebsrat / Employee-Interests-Agent",
        "kriterien": (
            "Werden Mitarbeiterdaten verarbeitet? Entstehen neue Moeglichkeiten der "
            "Leistungs- oder Verhaltenskontrolle? Koennen Beschaeftigte ueberwacht werden? "
            "Werden automatisierte Bewertungen ueber Mitarbeiter durchgefuehrt? Veraendert "
            "das Projekt Arbeitsinhalte/-organisation? Werden Entscheidungsrechte von "
            "Menschen auf Algorithmen uebertragen? Besteht Mitbestimmungsbedarf? Sind "
            "Transparenz und Nachvollziehbarkeit fuer Beschaeftigte gewaehrleistet? "
            "Bestehen Risiken fuer Datenschutz, Fairness oder Gleichbehandlung?"
        ),
    },
    "cfo": {
        "name": "CFO / Controlling-Agent",
        "kriterien": (
            "Investitionskosten, laufende Kosten, Lizenzkosten, Implementierungs- und "
            "Integrationskosten, Betriebs-/Supportkosten, Schulungskosten, versteckte "
            "Kosten, finanzielle Risiken, Belastbarkeit des Business Case, erwartete "
            "Einsparungen/Produktivitaetsgewinne, ROI, Payback-Zeit, Budget-Fit, "
            "Vendor-Lock-in- oder Preissteigerungsrisiken."
        ),
    },
    "it": {
        "name": "IT-, Architektur- und Cybersecurity-Agent",
        "kriterien": (
            "Kompatibilitaet mit bestehender IT-Architektur, Schnittstellen, "
            "Integrationsaufwand, IAM, Hosting-Modell, Datenfluesse/-haltung, "
            "Verschluesselung, Logging/Monitoring, Backup/Recovery, Verfuegbarkeit, "
            "Skalierbarkeit, Wartbarkeit, Exit-/Migrationsfaehigkeit, Herstellerabhaengigkeit, "
            "Zertifizierungen, bekannte Schwachstellen, Patch-/Vulnerability-Management, "
            "Supply-Chain-Risiken, interne IT-Richtlinien, regulatorische Anforderungen (NIS2)."
        ),
    },
    "ceo": {
        "name": "CEO- / Strategie-Agent",
        "kriterien": (
            "Unterstuetzung der Unternehmensstrategie, Wettbewerbsfaehigkeit, "
            "schnellere/schlankere Geschaeftsprozesse, organisatorische Agilitaet, "
            "Reaktionsfaehigkeit auf Marktveraenderungen, Kundennutzen, Geschwindigkeit/"
            "Qualitaet der Wertschoepfung, strategisch relevante neue Faehigkeiten, "
            "Skalierbarkeit fuer kuenftige Geschaeftsmodelle, strategische "
            "Anbieterabhaengigkeit, nachhaltiger strategischer Vorteil vs. lokale Optimierung."
        ),
    },
}

BEWERTUNGSLOGIK_KURZ = (
    "Score 0-10, ganzzahlig (10 = starke Priorisierungsempfehlung aus dieser Perspektive, "
    "0 = vollstaendig negativ). Bewerte NUR, wenn die vorliegenden Informationen fuer eine "
    "fachlich belastbare Bewertung ausreichen; sonst Status 'INFORMATION FEHLT' und KEIN "
    "Score (auch kein neutraler Ersatzwert wie 5). Keine Annahmen, keine erfundenen "
    "Fakten, keine Dezimalscores. Kurze, konkrete Begruendung (2-5 Saetze)."
)

SYSTEM_PROMPT_TEMPLATE = """Du bist ein Multi-Experten-Bewertungssystem fuer \
Projektportfolio-Entscheidungen. Du bewertest EIN Projekt gleichzeitig aus vier \
unabhaengigen Expertenperspektiven.

Allgemeine Bewertungslogik (verbindlich fuer jede Rolle):
{bewertungslogik}

Die vier Rollen und ihre Kriterien:
{rollen}

Antworte AUSSCHLIESSLICH mit validem JSON, ohne zusaetzlichen Text und ohne \
Markdown-Codeblock, in genau dieser Struktur (ein Objekt pro Rollen-Schluessel):
{{"betriebsrat": {{"status": "BEWERTET" oder "INFORMATION FEHLT", "score": Zahl 0-10 \
oder null, "begruendung": "...", "fehlende_informationen": ["..."]}}, \
"cfo": {{...gleiche Struktur...}}, "it": {{...}}, "ceo": {{...}}}}"""


def _build_system_prompt() -> str:
    rollen_block = "\n\n".join(
        f'### {r["name"]} (Schluessel: "{key}")\nRelevante Kriterien: {r["kriterien"]}'
        for key, r in ROLE_CRITERIA.items()
    )
    return SYSTEM_PROMPT_TEMPLATE.format(
        bewertungslogik=BEWERTUNGSLOGIK_KURZ, rollen=rollen_block
    )


def _project_text(proposal: Proposal) -> str:
    """Text-Grundlage fuer die Bewertung: hochgeladene Projektdateien, sonst die
    Beschreibung aus dem Vorschlag."""
    parts: list[str] = []
    if proposal.upload_dir.exists():
        for f in sorted(proposal.upload_dir.iterdir()):
            if not f.is_file():
                continue
            try:
                parts.append(f"### Datei: {f.name}\n\n{f.read_text(encoding='utf-8')}")
            except UnicodeDecodeError:
                continue
    if not parts:
        parts.append(f"### Beschreibung\n\n{proposal.description}")
    return "\n\n---\n\n".join(parts)


def _ask_model(model: str, proposal: Proposal) -> str:
    """Ruft das Modell auf und liefert den rohen Antworttext (ohne Codeblock-Zaun)."""
    from anthropic import Anthropic

    client = Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=_build_system_prompt(),
        messages=[
            {
                "role": "user",
                "content": (
                    f"Projekt: {proposal.project_name}\n\n"
                    f"Projektunterlagen:\n\n{_project_text(proposal)}"
                ),
            }
        ],
    )
    raw = "".join(block.text for block in response.content if block.type == "text").strip()
    return raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()


def _describe_api_error(e: Exception, model: str) -> str:
    """Verstaendliche Fehlermeldung fuer die Seite statt eines nackten Tracebacks."""
    import anthropic

    if isinstance(e, anthropic.AuthenticationError):
        return "ANTHROPIC_API_KEY wird vom Anbieter abgelehnt - Bewertung nicht moeglich."
    if isinstance(e, anthropic.NotFoundError):
        return f'Modell "{model}" ist beim Anbieter nicht verfuegbar (ANTHROPIC_MODEL pruefen).'
    if isinstance(e, anthropic.RateLimitError):
        return "Anbieter meldet Rate-Limit - bitte spaeter erneut versuchen."
    if isinstance(e, anthropic.APIConnectionError):
        return "Keine Verbindung zum LLM-Anbieter (Netzwerk oder ANTHROPIC_BASE_URL pruefen)."
    if isinstance(e, anthropic.APIStatusError):
        return f"LLM-Anbieter antwortet mit Fehler {e.status_code} - Bewertung nicht moeglich."
    return f"Bewertung fehlgeschlagen: {type(e).__name__}: {e}"


def evaluate_proposal(proposal: Proposal) -> dict:
    """Bewertet einen Projektvorschlag in allen vier Experten-Dimensionen gemaess
    Bewertungslogik_Experten-Agent_MVP.md. Gibt bei fehlendem API-Key oder
    Parsing-Fehlern ein dict mit "error" zurueck."""
    if not llm_is_configured():
        return {"error": "Kein ANTHROPIC_API_KEY gesetzt - Bewertung nicht moeglich."}

    model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
    try:
        raw = _ask_model(model, proposal)
    except Exception as e:  # noqa: BLE001 - jede API-/Netzstoerung wird auf der Seite gezeigt
        # Ohne diesen Fang wuerde ein ungueltiger Key, ein unbekanntes Modell oder
        # ein Netzfehler die ganze Seite als HTTP 500 abbrechen - die Bewertung
        # der uebrigen Vorschlaege inklusive.
        log.exception("Bewertung von %s fehlgeschlagen", proposal.slug)
        return {"error": _describe_api_error(e, model)}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {
            "error": "Antwort des Modells konnte nicht als JSON gelesen werden.",
            "raw": raw,
        }
    if not isinstance(data, dict):
        return {
            "error": "Antwort des Modells hat nicht die erwartete Struktur.",
            "raw": raw,
        }

    valid_scores = [
        v["score"]
        for v in data.values()
        if isinstance(v, dict)
        and v.get("status") == "BEWERTET"
        and isinstance(v.get("score"), (int, float))
    ]
    data["_gesamtscore"] = round(sum(valid_scores) / len(valid_scores), 1) if valid_scores else None
    data["_anzahl_bewertet"] = len(valid_scores)
    return data


def risk_class(score: float | int | None) -> str:
    """Gaengiges Ampel-Colour-Coding fuer Risk-/Portfolio-Reports:
    gruen = niedriges Risiko / starke Empfehlung, gelb = mittel, rot = hoch/kritisch,
    grau = keine belastbare Bewertung moeglich."""
    if score is None:
        return "risk-neutral"
    if score >= 7:
        return "risk-green"
    if score >= 4:
        return "risk-amber"
    return "risk-red"
