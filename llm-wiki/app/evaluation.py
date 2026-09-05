from __future__ import annotations

import json
import os
import re
from pathlib import Path

from .llm import is_configured as llm_is_configured
from .proposals import Proposal

DEFAULT_MODEL = "claude-haiku-4-5-20251001"

# Simulierte Unternehmenswissensbasis (PLAN.md §3) - Richtlinien, Architektur-,
# Budget- und Prozessdokumente der fiktiven "Lahnberg Thermotechnik GmbH".
# corpus/ dient hier als allgemeiner Referenzrahmen fuer die Bewertung (z.B.
# Budgetgrenzen, IT-Richtlinien, Mitbestimmungsregeln) - nicht als Tatsachen
# ueber das jeweils konkrete, andere fiktive Unternehmen im Projektvorschlag.
CORPUS_DIR = Path(__file__).resolve().parent.parent.parent / "corpus"

# Welche corpus/-Ordner zu welcher Experten-Dimension passen.
ROLE_TO_CORPUS_DIRS = {
    "betriebsrat": ["br_ablage"],
    "cfo": ["sharepoint_finance", "einkauf_scm"],
    "it": ["it_doku"],
    "ceo": ["sharepoint_gf", "mailarchiv"],
}

WORD_RE = re.compile(r"[a-zA-ZäöüÄÖÜß0-9]+")


def _tokenize(text: str) -> set[str]:
    return {w.lower() for w in WORD_RE.findall(text)}

# Ordnet angemeldete Nutzer (permissions.yaml) ihrer Experten-Dimension zu.
# Nur diese vier Nutzer sehen im Bewertungsreport ausschliesslich ihre eigene
# Rolle (US: "Als Betriebsrat will ich nur die Betriebsrat-Bewertung sehen,
# nicht die des CEO"). Alle anderen Nutzer (u.a. orchestrator, admin,
# pmo-leitung) sehen weiterhin den vollstaendigen Report ueber alle vier
# Rollen - passend zur Orchestrator-Rolle aus PLAN.md, die alle Perspektiven
# zusammenfuehrt statt selbst zu bewerten.
USER_TO_ROLE = {
    "betriebsrat": "betriebsrat",
    "cfo": "cfo",
    "it-security": "it",
    "ceo": "ceo",
}


def viewer_role(user_id: str) -> str | None:
    """Auf welche Rolle dieser Nutzer im Bewertungsreport beschraenkt ist -
    None bedeutet: sieht den vollstaendigen Report (alle vier Rollen)."""
    return USER_TO_ROLE.get(user_id)


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

Die Nutzernachricht kann zusaetzlich einen Abschnitt "Zusaetzlicher Kontext aus \
der Unternehmenswissensbasis (corpus/)" enthalten - dort steht bereits, wie \
er einzuordnen ist (allgemeiner Referenzrahmen je Rolle, keine Tatsachen \
ueber das konkrete Projekt).

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


def _corpus_snippets_for_role(role_key: str, query_words: set[str], top_k: int = 3) -> list[tuple[str, str]]:
    """Findet die zum Projekt passendsten Absaetze aus den corpus/-Ordnern der
    jeweiligen Rolle (Keyword-Ueberlappung, gleiches Prinzip wie
    wiki.search_snippets). Gibt (relativer Pfad, Absatz) zurueck."""
    dirs = ROLE_TO_CORPUS_DIRS.get(role_key, [])
    if not query_words or not dirs:
        return []

    results: list[tuple[float, str, str]] = []
    for d in dirs:
        folder = CORPUS_DIR / d
        if not folder.is_dir():
            continue
        for f in folder.rglob("*.md"):
            try:
                text = f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for para in text.split("\n\n"):
                para = para.strip()
                if not para:
                    continue
                overlap = query_words & _tokenize(para)
                if not overlap:
                    continue
                score = len(overlap) / len(query_words)
                results.append((score, str(f.relative_to(CORPUS_DIR)), para))

    results.sort(key=lambda r: r[0], reverse=True)
    return [(path, para) for _, path, para in results[:top_k]]


def _corpus_context_block(proposal: Proposal, project_text: str) -> str:
    """Baut fuer jede Rolle einen eigenen Kontextabschnitt aus der
    Unternehmenswissensbasis (corpus/) - als Referenzrahmen, nicht als
    Tatsachen ueber das konkrete Projekt (siehe Hinweis bei CORPUS_DIR)."""
    query_words = _tokenize(proposal.project_name) | _tokenize(project_text)
    sections = []
    for key, role in ROLE_CRITERIA.items():
        snippets = _corpus_snippets_for_role(key, query_words)
        if not snippets:
            continue
        body = "\n\n".join(f"(Quelle: corpus/{path})\n{para}" for path, para in snippets)
        sections.append(f"#### Fuer {role['name']} (Schluessel \"{key}\")\n{body}")
    if not sections:
        return ""
    return (
        "\n\n### Zusaetzlicher Kontext aus der Unternehmenswissensbasis (corpus/)\n"
        "Diese Auszuege stammen aus internen Richtlinien-, Architektur- und "
        "Budgetdokumenten (allgemeiner Referenzrahmen, KEINE Tatsachen ueber das "
        "konkrete Projekt oben) und sind je Rolle nach Relevanz vorsortiert. Nutze "
        "sie nur als Massstab (z.B. geltende Budgetgrenzen, IT-Richtlinien, "
        "Mitbestimmungsregeln), nicht als Aussagen ueber das Projekt selbst:\n\n"
        + "\n\n".join(sections)
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


def evaluate_proposal(proposal: Proposal) -> dict:
    """Bewertet einen Projektvorschlag in allen vier Experten-Dimensionen gemaess
    Bewertungslogik_Experten-Agent_MVP.md. Gibt bei fehlendem API-Key oder
    Parsing-Fehlern ein dict mit "error" zurueck."""
    if not llm_is_configured():
        return {"error": "Kein ANTHROPIC_API_KEY gesetzt - Bewertung nicht moeglich."}

    from anthropic import Anthropic

    project_text = _project_text(proposal)
    corpus_block = _corpus_context_block(proposal, project_text)

    client = Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=_build_system_prompt(),
        messages=[
            {
                "role": "user",
                "content": (
                    f"Projekt: {proposal.project_name}\n\n"
                    f"Projektunterlagen:\n\n{project_text}"
                    f"{corpus_block}"
                ),
            }
        ],
    )
    raw = "".join(block.text for block in response.content if block.type == "text").strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {
            "error": "Antwort des Modells konnte nicht als JSON gelesen werden.",
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
