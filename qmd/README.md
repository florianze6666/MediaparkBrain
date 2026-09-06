# qmd — abgeschottetes Teilprojekt

Semantische Suche über `corpus/` mit [QMD](https://github.com/tobi/qmd) (Query Markup
Documents, MIT). **Evaluation, kein Einbau.** Die Wiki-Anwendung in `llm-wiki/` weiß nichts
von diesem Ordner und wird davon nicht berührt.

Planungsdokument: `.plans/qmd_standalone_plan.md`.

## Was es ist

QMD ist eine On-Device-Suchmaschine für Markdown. Sie kombiniert drei Verfahren und
fusioniert die Ergebnisse per Reciprocal Rank Fusion:

| Verfahren | Umsetzung |
|---|---|
| Volltext (BM25) | SQLite FTS5 |
| Vektorsuche | sqlite-vec mit lokalen Embeddings |
| Reranking | lokales LLM |

Alle Modelle laufen als GGUF auf diesem Rechner. Das Retrieval braucht keine API-Aufrufe
und kostet nichts. Ein Vertraulichkeitsargument ist das nach AE-01 nicht mehr: Der Korpus
ist erfunden und darf vollständig an ein Anthropic-Modell.

## Abschottung

Es existiert **keine Datei außerhalb dieses Ordners**. Weder Modelle noch Konfiguration
landen in den globalen Verzeichnissen unter `%USERPROFILE%`.

| Was | Wohin | Steuerung |
|---|---|---|
| Pakete | `qmd/node_modules/` | lokales `npm install`, kein `-g` |
| GGUF-Modelle | `qmd/.cache/qmd/models/` | `XDG_CACHE_HOME` in `env.ps1` |
| Konfiguration und Index | `qmd/.qmd/` | `qmd init`, projektlokal |

`corpus/` wird ausschließlich lesend verwendet. `llm-wiki/`, `permissions.yaml`, `pages/`
und die Root-`.gitignore` bleiben unverändert.

## Benutzung

Jedes Skript zieht sich zuerst die Umgebung aus `env.ps1`. Wer QMD von Hand aufruft, macht
das genauso:

```powershell
cd D:\dev\prj\hackathon_rag\MediaparkBrain\qmd
. .\env.ps1
.\node_modules\.bin\qmd.ps1 status
```

Ohne `env.ps1` greift QMD auf die globalen Pfade zu. Dann stimmt die Abschottung nicht mehr.

Die drei Suchmodi unterscheiden sich in Qualität und Tempo:

```powershell
.\node_modules\.bin\qmd.ps1 search  "Betriebsvereinbarung"   # nur BM25, ohne LLM
.\node_modules\.bin\qmd.ps1 vsearch "Betriebsvereinbarung"   # nur Vektoren
.\node_modules\.bin\qmd.ps1 query   "Betriebsvereinbarung"   # hybrid, empfohlen
```

Nützliche Flags: `-c <collection>` grenzt auf Collections ein und ist mehrfach erlaubt,
`-n <zahl>` setzt die Trefferzahl, `--explain` zeigt die Scoring-Aufschlüsselung,
`--no-rerank` spart Zeit, `--format json` liefert maschinenlesbare Ausgabe.

## Stand

Der Wissensspeicher steht und ist indiziert.

| Posten | Ist |
|---|---|
| Dokumente | 224: 218 aus `corpus/` plus 6 Anträge aus `project_proposals/`, per Hardlink, Original unberührt |
| Vektoren | 1017 Chunks eingebettet, 2048 Dimensionen |
| Embedding | `nvidia/Nemotron-3-Embed-1B`, GGUF Q8_0 (seit 06.09.2026, davor embeddinggemma-300M) |
| Collections | `intern` 182, `br` 13 `[excluded]`, `clevel` 23 `[excluded]`, `antraege` 6 `[excluded]` |

Die drei Klassen bilden das Rechtemodell ab: alle sehen `intern`, der Betriebsrat
zusätzlich `br`, C-Level zusätzlich `clevel`, und die beiden letzten sehen einander nicht.
Weil `br` und `clevel` als `[excluded]` markiert sind, durchsucht eine Abfrage ohne `-c`
nur `intern`. Wer das Flag vergisst, bekommt weniger Treffer, niemals mehr.

Sicht neu bauen nach Änderungen am Korpus:

```powershell
python ingest\build_view.py --klassen --dry-run   # nur berichten
python ingest\build_view.py --klassen             # bauen
.\node_modules\.bin\qmd.ps1 embed
```

## Aufbau auf einem neuen Rechner

`index.ps1` baut den Wissensspeicher reproduzierbar auf: Sicht, Konfiguration aus
`index.template.yml` mit den Pfaden des Rechners, Freigabe des Modells (`qmd trust`),
Modell-Download, Indizierung, Einbettung ohne Zeitlimit und zuletzt die Testsuite.

```powershell
npm install            # holt @tobilu/qmd 2.8.3 und wendet patches/apply.mjs an
.\index.ps1            # GPU, wenn vorhanden, sonst CPU
.\index.ps1 -Cpu       # CPU erzwingen
```

`.qmd/index.yml` ist rechnerspezifisch (absolute Pfade) und bleibt unversioniert; die
versionierte Wahrheit ist `index.template.yml`. Wer nur das Embedding-Modell wechselt,
trägt es dort **und** in `env.ps1` (`QMD_EMBED_MODEL`) ein und bettet mit `qmd embed -f` neu.

## Modelle

| Aufgabe | Modell | Datei | Größe |
|---|---|---|---|
| Embedding | `nvidia/Nemotron-3-Embed-1B` (Ministral3-Encoder, 2048-d, Mean-Pooling) | `NeoRoth/nemotron-3-embed-1b-gguf`, Q8_0 | 1,2 GB |
| Reranking | `Qwen3-Reranker-0.6B` | `ggml-org`, Q8_0 | 640 MB |
| Query-Expansion | `qmd-query-expansion-1.7B` | `tobil`, Q4_K_M | 1,3 GB |

Das Embedding-Modell wurde am 06.09.2026 von embeddinggemma-300M auf Nemotron-3-Embed-1B
umgestellt (MMTEB Retrieval 71,0, 34 Sprachen einschließlich Deutsch, OpenMDW-Lizenz).
Die GGUF-Datei ist eine Community-Konvertierung mit llama.cpp b10015; SHA-256
`58e41095…8d8e92` ist gegen die Herkunftsangabe geprüft, die Tokenisierung stimmt
tokengenau mit der HuggingFace-Referenz überein.

QMD 2.8.3 kennt das Modell nicht. `patches/apply.mjs` zieht drei Dinge in
`node_modules/@tobilu/qmd/dist/llm.js` nach und läuft bei jedem `npm install` als
postinstall (`npm run check` prüft, ob der Patch sitzt):

1. Anfragen bekommen das Präfix `query: `, Dokumente `passage: ` mit dem Titel als erster
   Zeile. Ohne Patch würde QMD das embeddinggemma-Format `task: search result | query:`
   verwenden.
2. Kein BOS-Token. Das Modell ist ohne `<s>` trainiert; llama.cpp würde für den
   Pixtral-Tokenizer eins voranstellen, was die Vektoren um bis zu 1,5 % verdreht.
3. Der Fingerprint des Index ändert sich mit dem Modell, `qmd embed -f` ist danach Pflicht.

`most-embed-de` (deutsches Fine-Tuning desselben Basismodells) war der erste Kandidat
und ist verworfen: die einzige fertige GGUF-Datei nutzt eine llama.cpp-fremde
Architektur, und eine eigene Konvertierung hätte Werkzeuge außerhalb dieses Ordners
gebraucht.

## Hardware: GPU und CPU

QMD wählt das Gerät selbst, in der Reihenfolge CUDA, Vulkan, CPU. Es gibt keine
getrennte Konfiguration; `env.ps1 -Cpu` beziehungsweise `QMD_FORCE_CPU=1` erzwingt den
CPU-Pfad. Gemessen auf diesem Rechner (RTX 2080 Max-Q, i7-9750H mit 6 Kernen):

| Vorgang | GPU (CUDA) | CPU erzwungen |
|---|---|---|
| eine Einbettung, kurzer Text | 68 ms | 15 s |
| Durchsatz Nemotron Q8_0 | rund 600 Token/s | 2 Token/s |
| gesamter Korpus, 992 Chunks | 3 min 18 s | rechnerisch über 24 h |

Die Vektoren sind auf beiden Geräten dieselben (`qmd doctor` reproduziert die
gespeicherten Vektoren auch mit `QMD_FORCE_CPU=1`). Für die Indizierung ist eine GPU
praktisch Pflicht; ein Rechner mit AMD- oder Intel-Grafik nimmt automatisch Vulkan.
Reine CPU taugt für Abfragen (`--no-rerank` spart dort am meisten) und für kleine
Korpora.

**Nicht tun:** `npx node-llama-cpp source build` in diesem Ordner. Ein lokaler
CPU-Build wird von node-llama-cpp bevorzugt geladen; QMD lädt dann zusätzlich den
CUDA-Build, und Reranking und Query-Expansion stürzen mit `CUDA error` ab. Der Build
brachte auf der CPU außerdem keinen Gewinn (getestet mit llama.cpp b10361).

## Tests

`eval/run_tests.py` prüft die Kette gegen den vollständig indizierten Korpus, ohne
API-Kosten, in rund acht Minuten auf der GPU:

```powershell
python eval\run_tests.py            # Patch, Modell, Doctor, Status, Bench, Rechte, Reranker
python eval\run_tests.py --quick    # nur Patch, Modell, Doctor, Status (für CPU-Rechner)
python eval\run_tests.py --cpu      # CPU erzwingen
python eval\run_tests.py --e2e      # zusätzlich der CFO-Ende-zu-Ende-Test (API-Kosten)
```

| Schritt | Werkzeug | Bestanden, wenn |
|---|---|---|
| Patch | `patches/apply.mjs --check` | die drei Änderungen in `dist/llm.js` stehen |
| Modell | `eval/embed_smoke.mjs` | GGUF lädt, 2048-d, jede Testfrage findet ihre Passage mit Abstand ≥ 0,05 |
| Doctor, Status | `qmd doctor`, `qmd status` | Fingerprints aktuell, Vektorstichprobe reproduzierbar, Vektoren ≥ Dokumente |
| Bench intern | `qmd bench eval/fixture_intern.json` | Vektorsuche und volle Kette treffen je ≥ 75 % der acht Fragen in den ersten drei; jede Frage steht in einem der beiden in den ersten fünf; BM25 schlechter als Vektor |
| Rechte | `qmd bench eval/fixture_clevel.json -c clevel` | trifft mit `-c`; dieselbe Frage ohne `-c` liefert nichts aus `clevel` oder `br` |
| Reranker | `qmd query` mit und ohne `--no-rerank` | kein Reranker-Ausfall, Zieldokument in den ersten drei |

Die Fixtures folgen Abschnitt 9 des Plans: jede Frage ist anders formuliert als das
Zieldokument, BM25 soll leer ausgehen. Berichte landen als `eval/bench_*.json`
(unversioniert).

## Reset und Import mit Fortschritt (Phase 5)

Zwei Skripte unter `ingest/`, beide über die uv-Umgebung dieses Ordners, beide mit
zeilenweisem Fortschritt auf stdout, den das Wiki als Jobseite anzeigt (NFR-11):

```powershell
uv run python ingest\import.py wissen                        # Korpus: Sicht, qmd update, qmd embed
uv run python ingest\import.py wissen --ablageort erweiterung # dasselbe, Fortschritt nur fuer diesen Ablageort
uv run python ingest\import.py antraege                      # project_proposals/ in die Collection antraege
uv run python ingest\reset.py wissen [--dry-run]             # intern, br, clevel leeren und leer neu anlegen
uv run python ingest\reset.py antraege [--dry-run]           # Collection antraege ebenso
```

Der Import bettet ohne `-f` ein, also nur Dokumente ohne Vektor, und entfernt nie eine
Collection; das tut allein `reset.py`, getrennt je Bereich (UC-01). Die vierte Collection
`antraege` ist ausgeschlossen und steht in keiner Agentenabfrage; `ingest/rollen.py`
kennt weiterhin nur `intern`, `br` und `clevel`. Der Ablageort `corpus/erweiterung/` nimmt
Anwender-Uploads aus dem Wiki auf (`/wissen/upload`); die Klasse kommt aus dem
Frontmatter. Umgebung und Absturzerkennung teilen sich die Skripte in `ingest/qmdcli.py`:
bei einem CUDA-Fehler wird die Einbettung einmal über Vulkan wiederholt (Z13).

Tests gegen einen eigenen Temp-Index, Modelle aus dem echten Cache, rund eine Minute:

```powershell
uv run --with pytest pytest ingest\tests -q
```

## Rollen-zu-Collections-Brücke

Welche Collections ein Agent durchsuchen darf, leitet `ingest/rollen.py` aus
`llm-wiki/permissions.yaml` ab. Der Agent erbt die Vertraulichkeitsklassen seiner Rolle,
nicht ihre Domänen: `intern` bekommt jede Rolle mit Gruppen, `br` und `clevel` kommen dazu,
wenn die Rolle oder eine ihrer Gruppen in der Empfängerliste der Stufe `Betriebsrat-intern`
beziehungsweise `C-Level` steht. Die Zuordnung Stufe zu Collection ist dieselbe Tabelle,
die der Ingest benutzt.

```powershell
python ingest\rollen.py          # Tabelle für alle Rollen
python ingest\rollen.py cfo      # intern, clevel
```

Unbekannte Rollen und Rollen ohne Gruppen ergeben einen Fehler, keine leere Liste. Das
Wiki-Rechtemodell mit Domänen bleibt davon unberührt; es gilt für Menschen an der
Oberfläche, nicht für Agenten.

## Ende-zu-Ende-Test: CFO-Gutachter

`eval/cfo_e2e.py` fährt die vollständige RAG-Kette eines CFO-Bewerters: Persona-Erinnerung,
Wiedererkennung eines früheren Fehlschlags, **aktive** Abfrage der Wissensbasis über ein
Werkzeug, Zitat aus dem gefundenen Dokument im Bewertungsessay, JSONL nach Kapitel 17 der
Bewertungslogik.

```powershell
uv sync --no-python-downloads              # einmalig: .venv aus pyproject.toml, rund 20 MB
uv run python eval\cfo_e2e.py --dry-run    # nur Prompt bauen
uv run python eval\cfo_e2e.py              # kompletter Lauf
```

Braucht `ANTHROPIC_API_KEY`, wird aus der `.env` im Projektwurzelverzeichnis gelesen.
Der Treiber läuft in der eigenen uv-Umgebung dieses Ordners (`pyproject.toml`,
`.python-version` 3.12, `.venv/` gitignored, `uv.lock` versioniert); seit dem 06.09.2026
hängt er nicht mehr an `llm-wiki`. Nicht mit dem blanken System-Python starten: das
systemweite Python 3.14 trägt ein altes `anthropic` 0.46 und bricht mit `'typing.Union'
object has no attribute '__discriminator__'` ab, was wie ein fachlicher Testfehler aussieht.
Bericht landet in `eval/cfo_e2e_report.json`, die Bewertung in `eval/bewertungen.jsonl`.
Details stehen in `.plans/Feature_Branch.md`, Abschnitt 4.

## Rückbau

Ein Befehl, keine Rückstände:

```powershell
Remove-Item -Recurse -Force "D:\dev\prj\hackathon_rag\MediaparkBrain\qmd"
```

Danach sind rund 4 GB wieder frei. Es gibt keine Registry-Einträge, keine globalen
npm-Pakete und keine Änderung an `PATH`.
