# Agentenpfad: Treiber, Orchestrator, Golden-Test

Phase 3 des Dachplans (`.plans/Feature_Branch.md`), gebaut nach `.plans/08_orchestrator.md`
und AE-04 (`.plans/architekturentscheidungen/03_…md`). Alles hier läuft in der eigenen
uv-Umgebung von `qmd/` (`pyproject.toml`, einmalig `uv sync`), ohne Rückgriff auf `llm-wiki`.

| Datei | Zweck |
|---|---|
| `schema.py` | Kapitel-17-Objekt `Zeile` (acht Felder, flach, 17.2 und 17.5), Zug-B-Modell `Bewertungsfelder`, Kapitel-16-Aggregation `aggregiere` |
| `gate.py` | Completeness Gate gegen die fünfzehn Mindestangaben aus PLAN.md Abschnitt 2 |
| `treiber.py` | eine Rolle: Prompt-Module, Werkzeugrunden, Zug A mit Zitaten, Zug B per Structured Output, Zeile und Protokoll; Z1 bis Z13 |
| `orchestrator.py` | Gate, Z10, vier Rollen nacheinander, 17.5, Kapitel 16, Konflikte, Bericht |
| `e2e.py` | Golden-Test einer Rolle gegen `golden_dataset.json`, fünf harte Prüfungen, `--laeufe 3` nach A-3 |
| `tests/` | T1 bis T4 ohne API und ohne qmd, dazu `test_t4_wissensbasis.py` für Z2, Z13, Cache und typisierte Anfragen |

## Aufrufe, aus `qmd/`

```powershell
uv sync                                                             # einmalig
uv run pytest agenten\tests -q                                      # T1 bis T4, 90 Tests, rund 5 s
uv run python agenten\gate.py ..\project_proposals\abwaermenutzung-giesserei-eisenach-charter.md ..\project_proposals\abwaermenutzung-giesserei-eisenach-businesscase.md
uv run python agenten\treiber.py --rolle it --antrag <charter> --antrag <businesscase> --dry-run
uv run python agenten\treiber.py --rolle cfo --antrag <charter> --antrag <businesscase> --typisiert   # lex:/vec: statt Anfrageerweiterung
uv run python agenten\orchestrator.py --antrag <charter> --antrag <businesscase> [--rollen cfo,ceo] [--lauf <id>]
uv run python agenten\e2e.py --rolle cfo --antrag <charter> --antrag <businesscase> --golden ..\test\stammdaten-ki\golden_dataset.json --laeufe 3
uv run python agenten\e2e.py --rolle cfo --antrag ..\project_proposals\abwaermenutzung-giesserei-eisenach-charter.md --antrag ..\project_proposals\abwaermenutzung-giesserei-eisenach-businesscase.md --golden ..\test\eisenach\golden_dataset.json
```

`pytest` und `pydantic` stehen in der Gruppe `dev` von `pyproject.toml`; `uv run` installiert sie mit.

Umgebungsvariablen des Treibers: `TREIBER_QMD_GPU` wählt das Gerät der qmd-Abfragen (Vorgabe
`vulkan`, Z13; `cuda`, `metal` oder `auto`), `TREIBER_QMD_TYPISIERT=1` schaltet lex:/vec:-Anfragen
dauerhaft ein, `EVAL_MODEL` die Modellkennung.

Voller Lauf braucht `ANTHROPIC_API_KEY` (aus der `.env` im Projektwurzelverzeichnis oder der
Umgebung) und den gesunden Index (`qmd status`, Z10 prüft das). Modell über `EVAL_MODEL`
oder `--modell`, Vorgabe `claude-opus-5`.

## Ablage je Lauf: `qmd/laeufe/<lauf_id>/` (gitignored)

| Datei | Inhalt |
|---|---|
| `gate.json` | Ergebnis des Completeness Gate |
| `informationsanforderung.json` | nur wenn das Gate nicht besteht; dann startet kein Agent, Exit 3 |
| `vorbedingungen.json` | nur bei Verstoß gegen Z10, Exit 2 |
| `<rolle>.jsonl` | genau eine Zeile: das Kapitel-17-Objekt |
| `<rolle>.protokoll.json` | Essay, Zitate, Abfragen, Kontextdokumente, Modell, `prompt_version`, Zeiten, Fehler; `api_aufrufe` je Zug und `tokens` je Rolle mit `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens` (Summe über alle Rollen in `zusammenfassung.json` unter `tokens`) |
| `bewertungen.jsonl` | die gültigen Zeilen in Kapitel-17-Reihenfolge |
| `zusammenfassung.json` | Gesamtscore, Gesamtstatus, Rollen, Lücken (16.5), Spanne und Konflikte (Z8), technische Fehler |

Exit-Codes des Orchestrators: 0 alle Rollen gültig · 1 mindestens eine Rolle ohne Zeile,
Ergebnis liegt trotzdem vor (Z9) · 2 Vorbedingung · 3 Gate.

## Was der Treiber gegenüber `eval/cfo_e2e.py` ändert

- Rolle, Persona-Pfade und Antrag kommen von außen; die Nutzerkennung für `rollen.py` ist
  je Rolle hinterlegt (`it` heißt in `permissions.yaml` `it-security`).
- qmd-Aufrufe unterscheiden Absturz (Exitcode, `CUDA error`), echten Nulltreffer und
  „Reranker ausgelassen" (Z2); zwei Versuche auf Vulkan, der dritte als Rückfall auf CUDA
  ohne Reranking (Z13), dann sieht der Agent `is_error` statt „Keine Treffer". Ohne eine
  Abfrage mit Treffern gibt es keine Zeile (Z3, FR-04). Je Abfrage stehen Gerät, Dauer und
  `aus_cache` im Protokoll, weil identischer Wortlaut aus dem qmd-Cache künstlich stabil ist.
- Zug A einmal wiederholt bei `max_tokens`, danach technischer Fehler; `refusal` sofort
  technischer Fehler mit `stop_details` (Z4).
- Kontext: Auswahl je Abfrage statt global nach Score. Fassung 2 seit dem Lauf
  `t5-stammdaten-1`: zuerst Rang 1 jeder Abfrage, dann die Ränge 2 bis 5 der Abfragen mit
  Namensbezug (ganzes Pfadwort, kein Teilwort), dann die Ränge 2 bis 3 aller Abfragen, dann
  reihum, Deckel 16 (Z12, Z5). qmd normiert Scores je
  Abfrage; eine abfrageübergreifende Sortierung ist bedeutungslos (`.test/1b_diagnose.md`).
- Der Initialteil sagt, was die Wissensbasis enthält und was nicht, verlangt den erinnerten
  Fall in Runde 1 mit Namen und Jahr, deutet „Keine Treffer" als Lücke und „nicht erreichbar"
  als technischen Ausfall und nennt das Abfragebudget (vier Runden, bis zu drei Fragen).
- Zug B liefert die Felder per `client.messages.parse()` mit Pydantic-Schema; der Treiber
  baut die Zeile, das Modell schreibt nie JSON in Fließtext.
- Der Systemprompt trägt `cache_control` (Z11).

`eval/cfo_e2e.py` bleibt unverändert, solange Phase 1b dort arbeitet. Die Ablösung durch
`agenten/e2e.py --rolle cfo` ist ein offener Punkt; die Golden-Liste des CFO-Falls müsste
dazu in eine `golden_dataset.json` wandern.
