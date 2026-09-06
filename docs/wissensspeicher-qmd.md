# Wissensspeicher `qmd/`: semantische Suche über den Korpus

Stand: 06.09.2026. Beschreibt das abgeschottete Teilprojekt `qmd/`, das den Korpus mit
[QMD](https://github.com/tobi/qmd) (Query Markup Documents, MIT) semantisch durchsuchbar
macht. Seit dem 06.09.2026 ist es **die einzige Suche des Projekts**: Die Frage-Route `/ask` der
Wiki-Anwendung (Wortabgleich über `pages/`) wurde entfernt (siehe
[technischer Systembericht](technischer-systembericht-mediaparkbrain.md), Abschnitt 7). Seit Phase 4 und 5
(06.09.2026) startet das Wiki den Orchestrator aus `qmd/agenten/` je Antrag und führt Import, Reset
und Wissens-Upload über die Skripte unter `qmd/ingest/`; eine Suchoberfläche für Menschen gibt es
weiterhin nicht. Bedienung und Rückbau stehen in
[`qmd/README.md`](../qmd/README.md), die Planung in `.plans/qmd_standalone_plan.md`.

## 1. In einem Satz

Ein lokaler Index über 218 Korpusdokumente in drei Rechteklassen plus die Projektanträge in einer
vierten, ausgeschlossenen Collection, der Volltext (BM25),
Vektorsuche (Embeddings) und LLM-Reranking kombiniert, seit dem 06.09.2026 mit dem
Embedding-Modell `nvidia/Nemotron-3-Embed-1B` statt embeddinggemma-300M, auf GPU oder CPU
lauffähig und durch eine Testsuite ohne API-Kosten abgesichert.

## 2. Wie die Suche arbeitet

| Stufe | Verfahren | Umsetzung |
|---|---|---|
| Anfrageerweiterung | lokales LLM formuliert Varianten der Frage | `qmd-query-expansion-1.7B`, Q4_K_M |
| Volltext | BM25 | SQLite FTS5 |
| Vektorsuche | Kosinus-Ähnlichkeit von Embeddings | sqlite-vec, 2048 Dimensionen |
| Fusion | Reciprocal Rank Fusion der Trefferlisten | QMD |
| Reranking | Cross-Encoder bewertet Frage-Dokument-Paare neu | `Qwen3-Reranker-0.6B`, Q8_0 |

Dokumente werden in Chunks von 900 Token mit 15 % Überlappung zerlegt (992 Chunks aus 218
Dokumenten). `qmd search` nutzt nur BM25, `qmd vsearch` nur Vektoren, `qmd query` die volle
Kette; `--no-rerank` lässt die letzte Stufe aus.

### Rechtemodell über Collections

`ingest/build_view.py` baut aus `corpus/` eine Sicht `view/` aus Hardlinks, getrennt nach
den drei Vertraulichkeitsklassen des Wikis. Jede Klasse ist eine QMD-Collection:

| Collection | Dokumente | Sichtbar für | Vorgabe |
|---|---|---|---|
| `intern` | 182 | alle Rollen | durchsucht ohne `-c` |
| `br` | 13 | Betriebsrat | `[excluded]`, nur mit `-c br` |
| `clevel` | 23 | C-Level | `[excluded]`, nur mit `-c clevel` |
| `antraege` | 6 | keine Agentenrolle | `[excluded]`; Projektanträge, nur für getrenntes Zurücksetzen und spätere Dublettensuche (Phase 5) |

`br` und `clevel` sehen einander nicht. Eine Abfrage ohne `-c` liefert nur `intern`; wer das
Flag vergisst, bekommt weniger, niemals mehr. Welche Collections eine Rolle durchsuchen
darf, leitet `ingest/rollen.py` aus `llm-wiki/permissions.yaml` ab.

## 3. Modelle

| Aufgabe | Modell | GGUF-Quelle | Größe |
|---|---|---|---|
| Embedding | `nvidia/Nemotron-3-Embed-1B` (Ministral3-Encoder, 16 Schichten, 2048-d, Mean-Pooling, 32k Kontext) | `NeoRoth/nemotron-3-embed-1b-gguf`, Q8_0 | 1,2 GB |
| Reranking | `Qwen3-Reranker-0.6B` | `ggml-org`, Q8_0 | 640 MB |
| Anfrageerweiterung | `qmd-query-expansion-1.7B` | `tobil`, Q4_K_M | 1,3 GB |

Alle drei laufen lokal über node-llama-cpp 3.20.0 (llama.cpp b10361), das QMD 2.8.3
mitbringt. Es gibt keine API-Aufrufe im Retrieval.

### 3.1 Modellwechsel am 06.09.2026

**Vorher:** `embeddinggemma-300M` (Q8_0, 768 Dimensionen, 300 MB), die Vorgabe von QMD.
Das Modell war für den deutschen Fachkorpus zu schwach; der Wechsel wurde angeordnet.

**Erster Kandidat, verworfen:** `malteos/most-embed-de`, ein deutsches Fine-Tuning von
Nemotron-3-Embed-1B (Platz 1 seiner Größenklasse auf dem deutschen MTEB-Retrieval-Schnitt,
CC-BY-NC-4.0). Die einzige fertige GGUF-Datei (`cstr/most-embed-de-GGUF`) nutzt die
Architektur `decoder_embed` der Engine CrispEmbed, die llama.cpp nicht kennt. Eine eigene
Konvertierung hätte den llama.cpp-Konverter patchen und Werkzeuge außerhalb von `qmd/`
gebraucht (Python-Umgebung mit transformers 5, 2,3 GB Safetensors). Der Ansatz wurde
abgebrochen und alle Artefakte entfernt.

**Gewählt:** das Basismodell `nvidia/Nemotron-3-Embed-1B`.

| Kriterium | Wert |
|---|---|
| Qualität | MMTEB Retrieval 71,0; 34 Sprachen einschließlich Deutsch |
| Lizenz | OpenMDW 1.1 (Basis Ministral-3-3B unter Apache 2.0), kommerziell nutzbar |
| Eingabeformat | Präfix `query: ` für Fragen, `passage: ` für Dokumente, kein Instruktionstemplate |
| Pooling, Normierung | Mittelwert über Token, L2-normiert |
| Kontext | bis 32 768 Token; QMD nutzt 2 048 |
| GGUF | Community-Konvertierung mit llama.cpp b10015, Architektur `mistral3`, `causal=false`, `pooling_type=MEAN` in den Metadaten, SHA-256 `58e41095…8d8e92` gegen die Herkunftsangabe geprüft |

Geprüft wurde vor dem Einbau:

- **Tokenizer-Parität:** llama.cpp tokenisiert vier deutsche Testtexte tokengleich mit dem
  HuggingFace-Tokenizer des Modells.
- **BOS-Token:** Das Modell ist ohne `<s>` trainiert (sentence-transformers setzt keins).
  llama.cpp stellt für den Pixtral-Tokenizer standardmäßig eins voran; die Vektoren mit
  und ohne BOS weichen um bis zu 1,5 % ab (Kosinus 0,985). QMD wird deshalb auf „kein BOS"
  gestellt, wie die Referenz.
- **Semantik:** Drei deutsche Frage-Passage-Paare werden richtig zugeordnet, mit einem
  Abstand von mindestens 0,08 zur nächstbesten Passage, auf GPU und CPU identisch.
- **Abgrenzung:** Ein direkter Zahlenvergleich der GGUF-Vektoren mit der
  HuggingFace-Referenz wurde nicht gemacht; er hätte eine eigene Python-Umgebung außerhalb
  des Ordners gebraucht. Belegt ist die Konversionsqualität durch den Konvertierungsbericht
  der Quelle (Q8_0 gegen F16: Kosinus 0,9996).

### 3.2 Anpassung von QMD

QMD 2.8.3 kennt zwei Eingabeformate für Embeddings, embeddinggemma/nomic
(`task: search result | query: …`) und Qwen3-Embedding. Nemotron braucht drei Änderungen in
`node_modules/@tobilu/qmd/dist/llm.js`, die `qmd/patches/apply.mjs` idempotent einträgt:

1. Fragen bekommen das Präfix `query: `, Dokumente `passage: ` mit dem Dokumenttitel als
   erster Zeile.
2. Beim Laden des Embedding-Modells wird das BOS-Token abgeschaltet.
3. Der Index-Fingerprint von QMD enthält Modell und Formate; er ändert sich mit dem Patch,
   sodass `qmd embed -f` (Neuaufbau aller Vektoren, 768 → 2048 Dimensionen) erzwungen wird.

Der Patch läuft als `postinstall` in `qmd/package.json`, überlebt also `npm install`;
`npm run check` prüft, ob er sitzt. Er ist an den exakten Quelltext von QMD 2.8.3 gebunden
und bricht bei anderer Version mit einer Meldung ab, ohne die Datei anzufassen.

## 4. Hardware: GPU und CPU

QMD wählt das Gerät selbst, in der Reihenfolge CUDA, Vulkan, CPU. Es gibt keine getrennte
Konfiguration. `env.ps1 -Cpu` beziehungsweise `QMD_FORCE_CPU=1` erzwingt den CPU-Pfad,
`qmd doctor` zeigt unter „device probe", was gewählt wurde.

| Vorgang | GPU (RTX 2080 Max-Q, CUDA) | CPU erzwungen (i7-9750H, 6 Kerne) |
|---|---|---|
| Modell laden | 4,4 s | 6,4 s |
| eine Einbettung, kurzer Text | 68 ms | 15 s |
| gesamter Korpus, 992 Chunks | 3 min 18 s | rechnerisch mehr als ein Tag |

Die CPU-Werte sind vorläufig: Während der Messung belegte ein hängengebliebener
`qmd query`-Prozess einer anderen Session fünf der sechs Kerne. Die Vektoren sind auf
beiden Geräten dieselben; die Funktion des CPU-Pfads ist belegt, sein Tempo noch nicht.

Folgerungen:

- Für die Indizierung ist eine GPU praktisch Pflicht. Rechner mit AMD- oder Intel-Grafik
  nehmen automatisch Vulkan.
- Reine CPU taugt für Abfragen; `--no-rerank` spart dort am meisten Zeit.
- **Kein lokaler llama.cpp-Build** (`npx node-llama-cpp source build`) auf einem
  GPU-Rechner: node-llama-cpp lädt einen lokalen CPU-Build bevorzugt, QMD lädt daraufhin
  zusätzlich den CUDA-Build, und Reranking wie Anfrageerweiterung stürzen mit `CUDA error`
  ab. Der Build brachte auf der CPU zudem keinen messbaren Gewinn. Er wurde wieder entfernt.

### 4.1 Reranker: CUDA gegen Vulkan (Diagnose vom 06.09.2026)

Die Diagnose des durchgefallenen CFO-Laufs (`.test/1b_diagnose.md`) hat den Reranker unter
CUDA als Hauptursache leerer Abfragen ausgewiesen; Kandidatenzahl, Rerank-Kontext und
Parallelität ändern daran nichts, der Absturz ist nicht deterministisch.

| Einstellung | Versuche | Abstürze | Laufzeit bei Erfolg |
|---|---:|---:|---|
| CUDA mit Reranking, alle Varianten | 37 | 24 | 7 bis 27 s |
| CUDA, `--no-rerank` | 4 | 0 | 6 s |
| Vulkan (`QMD_LLAMA_GPU=vulkan`) mit Reranking | 5 | 0 | 45 bis 80 s |

Der Agenten-Treiber setzt deshalb für seine Abfragen Vulkan als Vorgabe (Regel Z13 in
`.plans/08_orchestrator.md`), mit Rückfall auf CUDA ohne Reranking. Die Index-Konfiguration
selbst ist unverändert; ob Vulkan-Vektoren numerisch den CUDA-Vektoren im Index gleichen, ist
nicht geprüft, die Treffer waren gleichwertig. Zwei Dinge sind bei Messungen zu beachten: qmd
normiert Scores je Abfrage, der beste Treffer hat immer 1,0, eine abfrageübergreifende
Sortierung nach Score ist deshalb sinnlos; und identischer Wortlaut wird in Sekunden aus dem
qmd-Cache beantwortet und ist künstlich stabil.

## 5. Aufbau und Betrieb

| Datei | Zweck |
|---|---|
| `qmd/env.ps1` | setzt `XDG_CACHE_HOME`, `QMD_CONFIG_DIR`, `QMD_EMBED_MODEL`; `-Cpu` erzwingt CPU |
| `qmd/index.template.yml` | versionierte Wahrheit für Collections und Modelle |
| `qmd/index.ps1` | Neuaufbau auf jedem Rechner: `uv sync`, Sicht, Konfiguration mit lokalen Pfaden, `qmd trust`, `qmd pull`, `qmd update`, `qmd embed -f --timeout 0`, Anträge nach `antraege`, Testsuite |
| `qmd/pyproject.toml`, `uv.lock`, `.venv` | eigene Python-Umgebung des Teilprojekts (anthropic, pyyaml, pydantic, pytest), seit dem 06.09.2026 unabhängig von `llm-wiki` |
| `qmd/ingest/import.py`, `reset.py`, `qmdcli.py` | Import mit Fortschritt je Ablageort oder für Anträge, getrenntes Zurücksetzen von Wissen und Anträgen, gemeinsame qmd-Hülle (Phase 5) |
| `qmd/agenten/` | Gate, Treiber je Rolle, Orchestrator, Golden-Test; siehe `qmd/agenten/README.md` und Plan 08 |
| `qmd/patches/apply.mjs` | QMD-Patch, siehe 3.2 |
| `qmd/.qmd/index.yml` | erzeugt, rechnerspezifisch, unversioniert |

Es existiert keine Datei außerhalb von `qmd/`: Pakete in `node_modules/`, Modelle in
`.cache/qmd/models/` (3,1 GB), Index in `.qmd/` (14 MB). Der Rückbau bleibt ein
Löschbefehl und gibt rund 4 GB frei.

## 6. Tests

`qmd/eval/run_tests.py` prüft die Kette gegen den vollständig indizierten Korpus, ohne
API-Kosten, in rund acht Minuten auf der GPU. `--quick` beschränkt sich auf die ersten vier
Schritte (für CPU-Rechner), `--cpu` erzwingt CPU, `--e2e` hängt den CFO-Ende-zu-Ende-Test an.

| Schritt | Werkzeug | Bestanden, wenn |
|---|---|---|
| Patch | `patches/apply.mjs --check` | die drei Änderungen in `dist/llm.js` stehen |
| Modell | `eval/embed_smoke.mjs` | GGUF lädt, 2048-d, BOS abschaltbar, jede Testfrage findet ihre Passage mit Abstand ≥ 0,05 |
| Doctor | `qmd doctor` | Fingerprints aktuell, drei Stichproben-Chunks reproduzieren die gespeicherten Vektoren |
| Status | `qmd status` | Vektoren ≥ Dokumente |
| Bench intern | `qmd bench eval/fixture_intern.json` | Vektorsuche und volle Kette treffen je ≥ 75 % der acht Fragen in den ersten drei (die Vektorsuche ist deterministisch, die volle Kette LLM-getrieben); jede Frage steht in einem der beiden in den ersten fünf; BM25 schlechter als Vektor |
| Rechte | `qmd bench eval/fixture_clevel.json -c clevel` und dieselbe Frage ohne `-c` | trifft mit `-c`; ohne `-c` nichts aus `clevel` oder `br` |
| Reranker | `qmd query` mit und ohne `--no-rerank` | kein Reranker-Ausfall, Zieldokument in den ersten drei, beide Läufe liefern Treffer |
| E2E (optional) | `eval/cfo_e2e.py` über die uv-Umgebung von `qmd/` (`uv run python eval/cfo_e2e.py`) | fünf harte Prüfungen des CFO-Gutachters, siehe `.plans/Feature_Branch.md` Abschnitt 4 |
| Agenten, ohne API | `uv run pytest agenten/tests -q` | 91 Tests: Schema und Aggregation, Gate, Trockenlauf je Rolle, Fehlerinjektion mit gefälschtem Client und gefälschter Wissensbasis |
| Golden je Rolle (API) | `uv run python agenten/e2e.py --rolle <rolle> --antrag … --golden <golden_dataset.json>` | fünf harte Prüfungen je Rolle, optional drei Läufe für NFR-03 |
| Ingest | `uv run --with pytest pytest ingest/tests -q` | 6 Tests gegen einen Temp-Index: Import zählt hoch, Reset trennt Wissen und Anträge, `erweiterung` landet in der Klasse des Frontmatters |

Die Fixtures folgen Abschnitt 9 des Plans: Jede Frage ist anders formuliert als das
Zieldokument, sodass BM25 leer ausgeht und Semantik statt Wortgleichheit geprüft wird.
Sechs Fragen betreffen den Fall Glaswerk Nord 2013 (die Erinnerungsspur des CFO), je eine
die Go-live-Verschiebung von ONE LTT und die Pflege der CRM-Opportunities; eine siebte
prüft das Management Summary in `clevel`.

### 6.1 Ergebnisse mit Nemotron-3-Embed-1B (Testlauf 06.09.2026, 05:20 Uhr, GPU)

Alle 14 Prüfungen der Suite bestanden, Laufzeit 130 s. Bench intern, acht Fragen:

| Frage | Vektor r@3 | Vektor r@5 | Vektor MRR | Volle Kette r@3 | r@5 | MRR |
|---|---|---|---|---|---|---|
| 01 Annahme ohne Messung (6 Zieldokumente) | 0,50 | 0,67 | 1,00 | 0,50 | 0,50 | 1,00 |
| 02 Messkampagne Abgas | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 |
| 03 Nachforderung Kunde | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 0,50 |
| 04 Regel Angebotsreview | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 |
| 05 Eskalationsmail | 1,00 | 1,00 | 1,00 | 0,00 | 1,00 | 0,25 |
| 06 Lehren des Projektleiters | 0,00 | 1,00 | 0,20 | 0,00 | 1,00 | 0,20 |
| 07 ERP-Verschiebung (4 Zieldokumente) | 0,25 | 0,25 | 1,00 | 0,50 | 0,50 | 1,00 |
| 08 CRM-Opportunity-Pflege (2 Zieldokumente) | 1,00 | 1,00 | 1,00 | 0,50 | 1,00 | 1,00 |
| **Mittel MRR** | | | **0,90** | | | **0,74** |

BM25 hat bei allen acht Fragen MRR 0,00: Die Fragen sind echte Semantiktests. Die
Vektorsuche trifft sieben von acht Fragen in den ersten drei, die volle Kette sechs von
acht; jede Frage steht in mindestens einem Backend in den ersten fünf. Die Rechteprüfung
(`clevel` nur mit `-c`, ohne `-c` kein Fremdtreffer) und der Reranker-Lauf bestehen.

Befunde aus den Einzelfällen:

- **Reranker verschlechtert zweimal.** Die Eskalationsmail (05) steht in der Vektorsuche
  auf Rang 1, nach Reranking außerhalb der ersten drei; bei den Lessons Learned (06) setzt
  er sachfremde Dokumente („Rekonstruktion von Entscheidungen in Altprojekten",
  „Erfahrungen mit Remote-Inbetriebnahme") vor das Zieldokument. Das ist ein Befund zum
  Qwen3-Reranker auf deutschen Fachtexten, nicht zum Embedding, und offen.
- **Lessons Learned (06) ist der schwerste Fall:** alle Glaswerk-Dokumente liegen
  semantisch dicht beieinander; die Vektorsuche setzt das Zieldokument auf Rang 5 hinter
  Projektreview, Management Summary und Eskalationsmail desselben Ereignisses.
- Für den Glaswerk-Fall (01) und die ERP-Verschiebung (07) liefert die Vektorsuche
  durchgehend Dokumente des richtigen Ereignisses; die Fixtures nennen deshalb alle
  Dokumente des Ereignisses als Zieldokumente.

**CFO-Ende-zu-Ende-Test:** Der Lauf mit Bericht von 05:12 Uhr fiel durch: 4 von 7 Golden-Dokumenten,
kein Zitat aus dem Golden Dataset, neun von fünfzehn QMD-Abfragen leer, während eine zweite
Session dieselbe GPU nutzte. Die Diagnose (`.test/1b_diagnose.md`, Abschnitt 4.1) fand zwei
Ursachen: CUDA-Abstürze des Rerankers, die der Treiber wie „keine Treffer" behandelte, und eine
abfrageübergreifende Score-Sortierung, die die qmd-Normierung je Abfrage nicht verträgt. Der
Agenten-Treiber unter `qmd/agenten/` ist darauf angepasst (Z2, Z12, Z13). Ein bestandener
E2E-Lauf mit Nemotron steht noch aus; T5 mit vier Rollen läuft.

## 7. Offene Punkte

1. **CPU-Tempo** ist nur unter Fremdlast gemessen (Abschnitt 4); eine neue Messung wurde am
   06.09.2026 ausdrücklich nicht beauftragt.
2. **Reranker-Verhalten** bei deutschen Fachtexten prüfen; Kandidat für einen Vergleich
   ist ein größerer oder deutschsprachig kalibrierter Reranker.
3. **Vergleich zu embeddinggemma** auf demselben Fixture liegt nicht vor; dafür müsste der
   Index vorübergehend zurückgebaut werden, was laufende Sessions stören würde.
4. **Zahlenkollision 420 °C** im CFO-Testfall (siehe `.plans/Feature_Branch.md`) besteht
   weiter; sie erleichtert das Retrieval und schwächt den Semantiktest.
5. Hochgeladene Wikiseiten (`llm-wiki/pages/`) sind nicht indiziert; seit dem Wegfall von `/ask`
   gibt es für Menschen keine Suche. Das Wiki nutzt den Speicher seit Phase 4 und 5 nur über
   Orchestrator, Import, Reset und Wissens-Upload. Der HTTP-Modus von QMD ist offen.
6. Der CUDA-Reranker bleibt instabil (Abschnitt 4.1); der Treiber umgeht das über Vulkan, die
   Index-Konfiguration ist nicht umgestellt. Ob Vulkan- und CUDA-Vektoren numerisch gleich sind,
   ist ungeprüft.
7. `qmd status` meldet nach Phase 5 rund 28 verwaiste Chunks von zwei zwischenzeitlich geänderten
   Korpusdokumenten; `qmd cleanup` wurde nicht ausgeführt.
