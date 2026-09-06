"""Ende-zu-Ende-Test: CFO-Gutachter als vollstaendiges RAG-System.

Testgegenstand ist nicht die Suche allein, sondern die Kette:

    Persona-Erinnerung -> Wiedererkennung -> AKTIVE RAG-Abfrage
    -> Golden Dataset im Kontext -> Zitat im Bewertungsessay -> JSONL

Der Nachweis "der Agent hat aktiv gefragt" wird nicht behauptet, sondern belegt:
das Modell bekommt ein Werkzeug `wissensbasis_suchen` und muss es von sich aus
aufrufen. Jeder Aufruf wird mit seinem Wortlaut protokolliert. Ein Lauf ohne
Werkzeugaufruf faellt durch, egal wie gut der Essay klingt.

Der Nachweis "das Wissen steht im Essay" laeuft ueber die Zitatfunktion der
Messages-API: die vom Agenten selbst gefundenen Dokumente gehen als
`document`-Bloecke mit `citations: {enabled: true}` in den finalen Zug. Die
Antwort liefert dann `document_index` und `cited_text`, also einen garantierten
Zeiger in ein konkretes Dokument statt einer Textsuche im Antwortstring.

Aufruf in der eigenen uv-Umgebung von qmd/ (pyproject.toml, einmalig `uv sync`):
    uv run --project qmd python qmd/eval/cfo_e2e.py             # aus dem Projektwurzelverzeichnis
    uv run python eval/cfo_e2e.py --dry-run                     # aus qmd/, nur Prompt bauen, keine API
Das blanke System-Python traegt ein altes anthropic-SDK und bricht ab (siehe README).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

QMD_DIR = Path(__file__).resolve().parent.parent
ROOT = QMD_DIR.parent
EVAL_DIR = QMD_DIR / "eval"

MODEL = os.environ.get("EVAL_MODEL", "claude-opus-5")
MAX_TOOL_RUNDEN = 4
TREFFER_JE_ABFRAGE = 8

# --------------------------------------------------------------------------
# Golden Dataset: vorab festgelegt, VOR dem Testlauf.
# Erinnerungsspur: cfo_persona.md, "Eine Annahme ohne Beleg ist die teuerste
# Position einer Vorlage" - Glaswerk Nord 2013, ungemessene Quellentemperatur
# aus muendlicher Kundenauskunft.
# --------------------------------------------------------------------------

GOLDEN = [
    "mailarchiv/glaswerk-nord-margenverlust-durch-/2013/2013-04-21-auf-die-abweichende-waermequellentemperatur-hinweise.md",
    "projektlaufwerk/glaswerk-nord-margenverlust-durch-/2013/2013-02-22-abweichung-von-kalkulation-und-ist-kosten-festhalten.md",
    "projektlaufwerk/glaswerk-nord-margenverlust-durch-/2013/2013-05-01-technische-bewertung-der-abweichung-protokollieren.md",
    "projektlaufwerk/glaswerk-nord-margenverlust-durch-/2013/2013-09-25-erfahrungen-aus-der-abwicklung-festhalten.md",
    "projektlaufwerk/glaswerk-nord-margenverlust-durch-/2013/2013-11-07-nachtragsforderung-gegenueber-dem-kunden-dokumentier.md",
    "qm_lenkung/glaswerk-nord-margenverlust-durch-/2013/2013-09-02-technische-angebotsreviews-ab-500000-eur-verbindlich.md",
    "sharepoint_gf/glaswerk-nord-margenverlust-durch-/2013/2013-06-16-ergebnisauswirkung-fuer-die-geschaeftsfuehrung-zusam.md",
]
# Mindestabdeckung: der Korpus dokumentiert das Ereignis siebenfach. Verlangt
# wird, dass der Agent die Spur breit genug trifft, nicht ein bestimmtes Blatt.
GOLDEN_MINDEST = 4

# Die Rolle, die dieser Treiber spielt. Welche Collections sie durchsuchen darf,
# leitet ingest/rollen.py aus llm-wiki/permissions.yaml ab: Klassen, nicht
# Domaenen. Hier ist nichts hartcodiert, damit Ingest und Abfrage dieselbe
# Quelle lesen. Der Orchestrator ruft spaeter dieselbe Funktion je Rolle.
ROLLE = "cfo"

sys.path.insert(0, str(QMD_DIR / "ingest"))
from rollen import RollenFehler, collections_for_role  # noqa: E402


# --------------------------------------------------------------------------
# Umgebung
# --------------------------------------------------------------------------


def load_env() -> None:
    """Liest die .env im Projektwurzelverzeichnis, ohne Zusatzabhaengigkeit."""
    f = ROOT / ".env"
    if not f.exists():
        return
    for line in f.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", line)
        if m and not line.lstrip().startswith("#"):
            os.environ.setdefault(m.group(1), m.group(2).strip().strip('"').strip("'"))


def qmd_env() -> dict:
    e = dict(os.environ)
    e["XDG_CACHE_HOME"] = str(QMD_DIR / ".cache")
    e["QMD_CONFIG_DIR"] = str(QMD_DIR / ".qmd")
    return e


def qmd_query(frage: str, collections: list[str], n: int = TREFFER_JE_ABFRAGE) -> list[dict]:
    """Eine RAG-Abfrage aus Sicht der Rolle. Volle Kette inkl. Reranking.

    `collections` kommt aus collections_for_role und ist nie leer: ohne `-c`
    wuerde qmd die Standard-Collection `intern` durchsuchen, und der Aufruf
    saehe von aussen wie ein gewollter aus.
    """
    if not collections:
        raise ValueError("qmd_query ohne Collections aufgerufen")
    exe = QMD_DIR / "node_modules" / ".bin" / "qmd.cmd"
    cmd = [str(exe), "query", frage, "-n", str(n), "--format", "json"]
    for c in collections:
        cmd += ["-c", c]
    r = subprocess.run(cmd, cwd=QMD_DIR, env=qmd_env(),
                       capture_output=True, text=True, encoding="utf-8", timeout=900)
    raw = (r.stdout or "").strip()
    start = raw.find("[")
    treffer = None
    if start >= 0:
        try:
            treffer = json.loads(raw[start:])
        except json.JSONDecodeError:
            treffer = None
    if treffer is None or r.returncode != 0:
        # Ein Absturz von qmd (z. B. CUDA-Fehler, wenn ein zweiter Prozess die GPU
        # belegt) darf nicht wie "keine Treffer" aussehen: laut melden, leer zurueck.
        fehler = (r.stderr or "").strip().splitlines()
        print(f"  WARNUNG: qmd query fehlgeschlagen (exit {r.returncode}): "
              f"{fehler[-1][:160] if fehler else 'keine Fehlermeldung'}", file=sys.stderr)
        return []
    return treffer


def qmd_uri_to_relpath(uri: str) -> str:
    """qmd://intern/mailarchiv/... -> mailarchiv/... (Pfad wie in corpus/)."""
    p = uri.replace("qmd://", "")
    return p.split("/", 1)[1] if "/" in p else p


def volltext(rel: str) -> str:
    f = ROOT / "corpus" / rel
    return f.read_text(encoding="utf-8", errors="replace") if f.exists() else ""


# --------------------------------------------------------------------------
# Prompt aus Modulen. Reihenfolge ist Absicht, siehe Architekturdokument 5.1-5.7.
# --------------------------------------------------------------------------

INITIALTEIL = """Du bist ein Experten-Gutachter in einem Multi-Stakeholder-Bewertungsprozess
fuer Projektportfolio-Entscheidungen der Lahnberg Thermotechnik GmbH & Co. KG.

## Deine Aufgabe

Du bewertest EIN Vorhaben aus GENAU EINER Perspektive, naemlich der weiter unten
beschriebenen Rolle. Du bist nicht der Orchestrator und nicht der Entscheider.

## Das Wissensmanagement, und wie du es bedienst

Dir steht die Wissensbasis des Unternehmens zur Verfuegung: rund 220 Dokumente aus
vierzehn Jahren, darunter Projektreviews, Protokolle, Richtlinien, Management Summaries
und Mailverkehr. Du erreichst sie ueber das Werkzeug `wissensbasis_suchen`.

Verbindliche Regeln fuer die Bedienung:

1. **Du MUSST das Werkzeug benutzen.** Eine Bewertung allein aus dem Projektantrag, aus
   deiner Rollenbeschreibung oder aus Allgemeinwissen ist ungueltig.
2. **Frage in eigenen Worten.** Formuliere die Frage so, wie du sie einem Archivar
   stellen wuerdest. Ganze Saetze funktionieren besser als Stichworte.
3. **Frage mehrfach.** Eine Abfrage deckt selten den ganzen Informationsbedarf. Zwei bis
   vier Abfragen mit unterschiedlicher Stossrichtung sind der Normalfall.
4. **Was du nicht findest, erfindest du nicht.** Fehlt eine Information, benennst du die
   Luecke ausdruecklich.
5. Du siehst nur, was deine Rolle sehen darf. Bleiben Bereiche verschlossen, ist das
   kein Fehler, sondern gehoert als Informationsluecke in die Bewertung.

## Wie du vorgehst

Zuerst liest du den Projektantrag und bestimmst deinen Informationsbedarf. Achte dabei
besonders darauf, **ob dich das Vorhaben an einen frueheren Fall erinnert**. Deine
Rollenbeschreibung enthaelt Erfahrungen aus vergangenen Vorhaben; wenn ein Muster
wiederkehrt, ist das die wichtigste Spur, der du nachgehen kannst. Frage dann gezielt
nach diesem frueheren Fall.

Danach bewertest du nach den unten folgenden Katalogen und gibst das vereinbarte Format
aus.
"""

ABSCHLUSS_AUFTRAG = """## Jetzt bewerten

Oben stehen die Dokumente, die deine eigenen Abfragen an die Wissensbasis geliefert
haben. Erstelle nun deine abschliessende Bewertung.

Zwingend:

1. **Zitiere woertlich** aus den beigefuegten Dokumenten. Deine Begruendung muss den
   Satz enthalten, der deine Einschaetzung traegt, unveraendert.
2. Nenne mindestens einen Betrag oder eine Regelbezugnahme mit Fassung.
3. Wenn dich das Vorhaben an einen frueheren Fall erinnert, benenne ihn und belege ihn
   aus den Dokumenten.

## Ausgabeformat, verbindlich

Schliesse mit GENAU EINEM JSON-Objekt in einem ```json-Block ab, nach diesem Schema:

```json
{
  "rolle": "cfo",
  "status": "BEWERTET",
  "score": 4,
  "begruendung": "Fliesstext mit woertlichem Zitat und Betrag.",
  "praezedenz": "Kurzbezeichnung des frueheren Falls, oder null",
  "fehlende_informationen": ["..."],
  "entscheidungsrelevanter_hinweis": "hoechstens drei Zeilen, oder null"
}
```

`status` ist "BEWERTET" oder "INFORMATION FEHLT". Bei "INFORMATION FEHLT" ist `score`
null, niemals ein Ersatzwert. `score` ist eine ganze Zahl von 0 bis 10; 10 ist die
starke Priorisierungsempfehlung aus deiner Perspektive, 0 vollstaendig negativ.
"""

TOOLS = [{
    "name": "wissensbasis_suchen",
    "description": (
        "Durchsucht die Wissensbasis des Unternehmens (Projektreviews, Protokolle, "
        "Richtlinien, Management Summaries, Mailverkehr aus vierzehn Jahren) semantisch "
        "und liefert die relevantesten Dokumente. Stelle eine Frage in ganzen Saetzen. "
        "Nutze das Werkzeug mehrfach mit unterschiedlicher Stossrichtung."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "frage": {
                "type": "string",
                "description": "Die Suchfrage in eigenen Worten, als ganzer Satz.",
            }
        },
        "required": ["frage"],
        "additionalProperties": False,
    },
}]


# Die verbindliche Bewertungslogik. Es gibt genau diese eine Fassung; wer den Namen
# aendert, aendert ihn hier und nirgends sonst.
BEWERTUNGSLOGIK = "Bewertungslogik_Experten-Agent.md"


def lies(rel: str) -> str:
    """Laedt ein Prompt-Modul. Bricht laut ab, wenn es fehlt ODER leer ist.

    Die Leerpruefung ist kein Ziererei: eine vorhandene, aber leere Datei wuerde
    sonst ein leeres Modul in den Prompt schieben, und ein Prompt ohne
    Kriterienkatalog faellt im Ergebnis nicht auf.
    """
    f = ROOT / rel
    if not f.exists():
        sys.exit(f"FEHLER: Prompt-Modul fehlt: {f}")
    text = f.read_text(encoding="utf-8")
    if not text.strip():
        sys.exit(f"FEHLER: Prompt-Modul ist leer: {f}")
    return text


def baue_system_prompt() -> tuple[str, list[tuple[str, int]]]:
    """Konkateniert die Prompt-Module. Rueckgabe: (Prompt, Modulliste mit Zeichenzahl)."""
    module = [
        ("Generischer Initialteil", INITIALTEIL),
        ("Rollen-Persona (persona/cfo_persona.md)", lies("persona/cfo_persona.md")),
        (f"Bewertungslogik, generischer Kriterienkatalog ({BEWERTUNGSLOGIK})",
         lies(BEWERTUNGSLOGIK)),
        ("Rollenspezifische Kalibrierung (persona/cfo_kriterienkalibrierung.md)",
         lies("persona/cfo_kriterienkalibrierung.md")),
    ]
    teile, index = [], []
    for name, text in module:
        teile.append(f"\n\n{'=' * 78}\n# MODUL: {name}\n{'=' * 78}\n\n{text}")
        index.append((name, len(text)))
    return "".join(teile), index


def baue_projektobjekt() -> tuple[str, list[tuple[str, int]]]:
    """Das Projektobjekt aus ZWEI Dateien, wie in 'test project data'."""
    dateien = [
        "project_proposals/abwaermenutzung-giesserei-eisenach-charter.md",
        "project_proposals/abwaermenutzung-giesserei-eisenach-businesscase.md",
    ]
    teile, index = [], []
    for rel in dateien:
        text = lies(rel)
        teile.append(f"\n\n### Projektdatei: {Path(rel).name}\n\n{text}")
        index.append((rel, len(text)))
    kopf = ("# Zu bewertendes Vorhaben\n\nDas Projektobjekt besteht aus zwei Dateien, "
            "einem Steckbrief und einem Business Case.\n")
    return kopf + "".join(teile), index


# --------------------------------------------------------------------------
# Lauf
# --------------------------------------------------------------------------


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").replace(" ", " ")).strip().lower()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="nur Prompt bauen und Golden Dataset pruefen, keine API")
    args = ap.parse_args()

    load_env()
    EVAL_DIR.mkdir(parents=True, exist_ok=True)

    try:
        collections = collections_for_role(ROLLE)
    except RollenFehler as e:
        print(f"FEHLER: {e}", file=sys.stderr)
        return 2
    print(f"Rolle {ROLLE}: Collections {', '.join(collections)} "
          "(abgeleitet aus llm-wiki/permissions.yaml)\n")

    system_prompt, modulindex = baue_system_prompt()
    projekt, projektindex = baue_projektobjekt()

    print("Prompt-Module (Reihenfolge ist Absicht):")
    for i, (name, n) in enumerate(modulindex, 1):
        print(f"  {i}. {name:<62} {n:>7} Zeichen")
    print("  5. Projektobjekt aus zwei Dateien:")
    for rel, n in projektindex:
        print(f"       {Path(rel).name:<60} {n:>7} Zeichen")
    print("  6. RAG-Treffer (zur Laufzeit)")
    print("  7. Output-Contract")
    print(f"\nSystem-Prompt gesamt: {len(system_prompt)} Zeichen")

    if args.dry_run:
        print("\n--dry-run: keine API-Aufrufe.")
        return 0

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("FEHLER: ANTHROPIC_API_KEY fehlt (weder Umgebung noch .env).",
              file=sys.stderr)
        return 2

    from anthropic import Anthropic

    client = Anthropic()
    messages = [{"role": "user", "content": projekt + "\n\n" + (
        "Analysiere dieses Vorhaben. Bestimme deinen Informationsbedarf und befrage die "
        "Wissensbasis, bevor du urteilst. Melde dich mit deiner Einschaetzung erst, wenn "
        "du die Wissensbasis befragt hast."
    )}]

    protokoll: list[dict] = []   # jeder Werkzeugaufruf mit Wortlaut
    gefunden: dict[str, dict] = {}   # relpath -> Trefferinfo

    for runde in range(1, MAX_TOOL_RUNDEN + 1):
        resp = client.messages.create(
            model=MODEL, max_tokens=8000, system=system_prompt,
            messages=messages, tools=TOOLS,
        )
        calls = [b for b in resp.content if b.type == "tool_use"]
        messages.append({"role": "assistant", "content": resp.content})
        if not calls:
            print(f"\nRunde {runde}: kein Werkzeugaufruf mehr, Recherche beendet.")
            break

        results = []
        for c in calls:
            frage = (c.input or {}).get("frage", "")
            treffer = qmd_query(frage, collections)
            protokoll.append({
                "runde": runde, "frage": frage,
                "treffer": [t.get("file", "") for t in treffer],
            })
            print(f"\nRunde {runde} | RAG-Abfrage des Agenten:")
            print(f'  "{frage}"')
            zeilen = []
            for t in treffer:
                rel = qmd_uri_to_relpath(t.get("file", ""))
                alt = gefunden.get(rel)
                if alt is None or (t.get("score", 0) > alt.get("score", 0)):
                    gefunden[rel] = t
                marker = "  <== GOLDEN" if rel in GOLDEN else ""
                print(f"    {t.get('score')}  {rel}{marker}")
                zeilen.append(f"- {rel}\n  {(t.get('snippet') or '')[:300]}")
            results.append({
                "type": "tool_result", "tool_use_id": c.id,
                "content": ("Treffer:\n" + "\n".join(zeilen)) if zeilen
                           else "Keine Treffer.",
            })
        messages.append({"role": "user", "content": results})

    if not protokoll:
        print("\nDURCHGEFALLEN: Der Agent hat die Wissensbasis nie befragt.",
              file=sys.stderr)
        return 1

    # Finaler Zug: die vom Agenten selbst gefundenen Dokumente als document-Bloecke
    # mit eingeschalteten Zitaten. Reihenfolge = document_index in der Antwort.
    doc_reihenfolge = [rel for rel, _ in sorted(
        gefunden.items(), key=lambda kv: kv[1].get("score", 0), reverse=True)][:12]
    inhalt = []
    for rel in doc_reihenfolge:
        inhalt.append({
            "type": "document",
            "source": {"type": "text", "media_type": "text/plain",
                       "data": volltext(rel)},
            "title": Path(rel).stem,
            "context": f"Aus der Wissensbasis. Quelle: corpus/{rel}",
            "citations": {"enabled": True},
        })
    inhalt.append({"type": "text", "text": ABSCHLUSS_AUFTRAG})
    messages.append({"role": "user", "content": inhalt})

    # Streaming ist bei diesem max_tokens Pflicht; der SDK lehnt den
    # nicht-streamenden Aufruf sonst ab (Anfragen ueber 10 Minuten).
    with client.messages.stream(
        model=MODEL, max_tokens=16000, system=system_prompt, messages=messages,
    ) as stream:
        final = stream.get_final_message()
    if final.stop_reason == "max_tokens":
        print("WARNUNG: Antwort an der Token-Grenze abgeschnitten.", file=sys.stderr)
    text = "".join(b.text for b in final.content if b.type == "text")
    zitate = [z for b in final.content if b.type == "text"
              for z in (getattr(b, "citations", None) or [])]

    # ---------------- Auswertung ----------------
    zitierte_dateien = {doc_reihenfolge[z.document_index] for z in zitate
                        if 0 <= z.document_index < len(doc_reihenfolge)}
    golden_gefunden = [g for g in GOLDEN if g in gefunden]
    bewertung = None
    for kand in reversed(re.findall(r"```json\s*(.*?)```", text, re.S)):
        try:
            bewertung = json.loads(kand.strip()); break
        except json.JSONDecodeError:
            continue
    if bewertung is None:  # Rueckfall: letztes balanciertes Objekt im Text
        start = text.rfind('{"rolle"')
        if start < 0:
            start = text.rfind("{")
        if start >= 0:
            tiefe = 0
            for k in range(start, len(text)):
                if text[k] == "{":
                    tiefe += 1
                elif text[k] == "}":
                    tiefe -= 1
                    if tiefe == 0:
                        try:
                            bewertung = json.loads(text[start:k + 1])
                        except json.JSONDecodeError:
                            pass
                        break

    pruef = {
        "1_aktive_rag_abfrage": len(protokoll) > 0,
        "2_mehrfach_gefragt": len(protokoll) >= 2,
        "3_golden_abdeckung_erreicht": len(golden_gefunden) >= GOLDEN_MINDEST,
        "4_golden_anteil": f"{len(golden_gefunden)}/{len(GOLDEN)} (min {GOLDEN_MINDEST})",
        "5_zitat_vorhanden": len(zitate) > 0,
        "6_zitat_aus_golden": bool(zitierte_dateien & set(GOLDEN)),
        "7_jsonl_geparst": bewertung is not None,
    }
    harte = [pruef["1_aktive_rag_abfrage"], pruef["3_golden_abdeckung_erreicht"],
             pruef["5_zitat_vorhanden"], pruef["6_zitat_aus_golden"],
             pruef["7_jsonl_geparst"]]
    bestanden = all(harte)

    print("\n" + "=" * 70)
    print("PRUEFUNG")
    print("=" * 70)
    for k, v in pruef.items():
        print(f"  {k:<26} {v}")
    print(f"\n  GESAMT: {'BESTANDEN' if bestanden else 'DURCHGEFALLEN'}")
    if zitate:
        print(f"\n  {len(zitate)} Zitat(e), daraus das erste:")
        z = zitate[0]
        print(f'    aus: {doc_reihenfolge[z.document_index]}')
        print(f'    "{(z.cited_text or "")[:220]}"')

    bericht = {
        "zeitpunkt": datetime.now(timezone.utc).isoformat(),
        "modell": MODEL,
        "rolle": ROLLE,
        "collections": collections,
        "erinnerungsspur": "Glaswerk Nord 2013, ungemessene Quellentemperatur aus "
                           "muendlicher Kundenauskunft (cfo_persona.md)",
        "golden_dataset": GOLDEN,
        "rag_protokoll": protokoll,
        "dokumente_im_kontext": doc_reihenfolge,
        "zitate": [{"datei": doc_reihenfolge[z.document_index],
                    "cited_text": z.cited_text} for z in zitate
                   if 0 <= z.document_index < len(doc_reihenfolge)],
        "pruefung": pruef,
        "bestanden": bestanden,
        "bewertung": bewertung,
        "essay": text,
    }
    (EVAL_DIR / "cfo_e2e_report.json").write_text(
        json.dumps(bericht, ensure_ascii=False, indent=2), encoding="utf-8")
    if bewertung:
        (EVAL_DIR / "bewertungen.jsonl").write_text(
            json.dumps(bewertung, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nBericht: {EVAL_DIR / 'cfo_e2e_report.json'}")
    return 0 if bestanden else 1


if __name__ == "__main__":
    raise SystemExit(main())
