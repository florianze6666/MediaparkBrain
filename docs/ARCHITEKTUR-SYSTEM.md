# Systemarchitektur — Module, Backend, Frontend, Cloud, Konnektoren, Workflow

> **Status:** v0.1, 2026-09-05, Anselm (Rolle: Systemarchitekt). Ergänzt
> [`ARCHITEKTUR-RAG.md`](ARCHITEKTUR-RAG.md) (Wissensschicht) um das Gesamtsystem. Leitsatz:
> **So modular wie möglich.** Jedes Modul hat genau eine öffentliche Schnittstelle, ist ohne
> die anderen testbar und durch Konfiguration austauschbar. Das RAG ist die Plattform; der
> PMO-Workflow ist der erste Use Case darauf, nicht das System.

## 1. Schichten

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│  FRONTEND        Web-UI (htmx + Jinja, später optional React)                │
│                  spricht ausschließlich JSON mit der API                      │
├──────────────────────────────────────────────────────────────────────────────┤
│  API             FastAPI: /runs /projects /assessments /escalations /audit   │
│                  authentifiziert den user, sonst nichts — keine Logik         │
├──────────────────────────────────────────────────────────────────────────────┤
│  USE CASES       mpb.workflow   Run-Zustandsautomat (PMO-Workflow)           │
│                  mpb.gate       Completeness Check                            │
│                  mpb.agents     Rollen als Plugins + Runner                   │
│                  mpb.merge      Zusammenführung, Konflikte, Ranking           │
│                  mpb.escalation Eskalationen + Grants                         │
├──────────────────────────────────────────────────────────────────────────────┤
│  PLATTFORM       mpb.knowledge  Sources → Ingest → Access → Index → Retrieval │
│  (das RAG)       mpb.access     permissions, acl-rules, decide()             │
│                  mpb.llm        complete() — Anthropic | Mock                 │
│                  mpb.store      SQLite-Repositories (Katalog, Runs, Audit)   │
│                  mpb.config     DATA_DIR, Provider-Auswahl, Secrets aus env  │
└──────────────────────────────────────────────────────────────────────────────┘
```

Abhängigkeiten zeigen nur **nach unten**. Use Cases kennen die Plattform; die Plattform kennt
keinen Use Case. Das Frontend kennt nur die API.

## 2. Modulschnitt und Schnittstellen

Jedes Modul = ein Python-Paket mit `__init__.py`, das **genau** die öffentliche Schnittstelle
exportiert. Interne Struktur ist Privatsache. Austauschbare Teile sind `Protocol`s; die
Implementierung wählt `mpb.config`.

| Modul | Öffentliche Schnittstelle | Austauschbar | Kennt |
|---|---|---|---|
| `mpb.config` | `Settings` (pydantic-settings) | — | nichts |
| `mpb.store` | `Repository`-Protokolle: `CatalogRepo`, `RunRepo`, `EscalationRepo`, `AuditRepo` | SQLite → Postgres | config |
| `mpb.access` | `load_permissions()`, `resolve_acl(path, head, rules)`, `decide(principal, acl)`, `Principal`, `ACL` | — (ist der Kern) | config |
| `mpb.knowledge.sources` | `DriveSource` Protocol: `list()`, `read(path)`, `sidecar(path)` | `LocalFolderSource` → `SharePointGraphSource`, `GoogleDriveSource` | config |
| `mpb.knowledge.extract` | `Extractor` Protocol: `extract(bytes, suffix) -> Document` | je Dateityp ein Plugin: md, docx, pdf, xlsx, txt | — |
| `mpb.knowledge.ingest` | `scan(source) -> ScanReport`, `ingest(path)` | — | sources, extract, access, index, store |
| `mpb.knowledge.index` | `Index` Protocol: `add(chunks)`, `remove(doc_id)`, `query(text, allowed_ids, k)` | `BM25Index` → `HybridIndex` (Embeddings) | store |
| `mpb.knowledge.retrieval` | `retrieve(query, ctx, k) -> RetrievalResult` | — | access, index, store (audit) |
| `mpb.knowledge.enrich` | `enrich(content, ctx, derived_from) -> doc_id` | — | access, ingest |
| `mpb.llm` | `complete(system, messages, tools=None) -> Completion` | `AnthropicProvider`, `MockProvider` (Tests) | config |
| `mpb.agents` | `RoleRegistry`, `run_role(role, project, ctx) -> Assessment` | Rollen = Ordner `roles/<name>/` | llm, retrieval (als Client!), escalation |
| `mpb.gate` | `check(project) -> GateResult` | Regeln aus `gate.yaml` | — |
| `mpb.merge` | `merge(assessments) -> ProjectResult`, `rank(results) -> Portfolio` | Formel aus `merge.yaml` | access (Output-Klassifikation) |
| `mpb.escalation` | `create()`, `approve()`, `reject()`, `grants(run_id)` | — | store, access |
| `mpb.workflow` | `start_run(files, user)`, `advance(run_id)`, `status(run_id)` | — | alle Use-Case-Module |
| `mpb.api` | FastAPI-App | — | workflow, escalation, store |
| `mpb.cli` | `python -m mpb <befehl>` | — | dieselben Services wie die API |

**Die eine Regel, die Modularität erzwingt:** `mpb.agents` importiert `mpb.knowledge` **nicht**.
Es bekommt einen `RetrievalClient` injiziert (lokal: Funktionsaufruf; im Container: HTTP zum
Knowledge-Dienst). Damit ist der Agentenprozess ohne Dateizugriff — Konzept §2.8.

## 3. Rollen als Plugins

```text
roles/
├── ceo/
│   ├── role.yaml        # name, represents-Schlüssel, score_focus, playbook-Overrides
│   ├── ROLE.md          # Mandat, Leitfrage, Prüfkatalog (aus ROLLEN.md, wird dorthin ausgelagert)
│   ├── criteria.md      # Bewertungskriterien — separat pflegbar (TODO.md)
│   └── prompt.md        # System-Prompt-Kern
├── cfo/ …
├── betriebsrat/ …
└── it_security/ …
```

`RoleRegistry` lädt jeden Ordner. Eine fünfte Rolle ist ein fünfter Ordner. Das Playbook
(`PLAN.md` §7, Phasen 1–7) ist **eine** Implementierung im Runner; Rollen liefern nur Inhalte.
Personen dahinter: `data/permissions.yaml → agents.<name>.represents`.

## 4. Der PMO-Workflow (Use Case 1)

```text
 PMO-Leiterin                    System                                        Owner
     │  1. Upload (10 Dateien / ZIP)  │                                            │
     ├───────────────────────────────►│ Run anlegen, Dateien → data/drive/         │
     │                                │   uploads/<run_id>/ mit ACL:               │
     │                                │   Verteiler = Uploaderin + vier Rollen     │
     │                                │ Ingest (ACL zuerst, dann Index)            │
     │                                │ 2. Gate je Projekt                          │
     │◄───────────────────────────────┤   unvollständig → Feldliste                 │
     │                                │   bereit → in Bewertung                     │
     │                                │ 3. je Projekt × Rolle: Playbook             │
     │                                │   retrieve() ─ allowed / denied / hidden    │
     │                                │   denied wesentlich? ──► Eskalation ───────►│
     │                                │   Assessment (JSONL, cited_chunks)          │  approve /
     │                                │ 4. Merge je Projekt, Ranking über alle      │◄─ reject
     │  5. Ergebnis im Frontend       │   Output-Klassifikation je Betrachter       │
     │◄───────────────────────────────┤                                            │
```

**Run-Zustandsautomat** (`mpb.workflow`):
`created → ingested → gated → evaluating → merged → done`, je Projekt darin:
`uploaded → incomplete | ready → evaluating → waiting_escalation | assessed`.
Jeder Übergang ist ein Datensatz in `store.RunRepo` und eine Audit-Zeile. Ein abgebrochener
Lauf setzt aus dem Store fort, nie aus dem Speicher.

**Nebenläufigkeit:** Projekte parallel, Rollen je Projekt parallel (Thread-Pool, 4 × N).
Eskalationen blockieren nur die betroffene Rolle; das Assessment wird mit sichtbarer Lücke
trotzdem erzeugt und bei Freigabe neu berechnet.

## 5. Konnektoren (Sources)

```python
class DriveSource(Protocol):
    def list(self) -> Iterable[SourceItem]: ...          # path, size, mtime, etag
    def read(self, path: str) -> bytes: ...
    def sidecar(self, path: str) -> dict | None: ...     # .acl.yaml des Ordners
    def head(self, path: str) -> dict | None: ...        # Dokumentkopf, falls Quelle ihn liefert
    def changes(self, since: str | None) -> Iterable[Change]: ...   # optional: Delta
```

| Implementierung | `list/read` | `sidecar` | `head` | `changes` | Stand |
|---|---|---|---|---|---|
| `LocalFolderSource` | Dateisystem | `.acl.yaml` | YAML-Frontmatter | Scan gegen Katalog | **heute** |
| `SharePointGraphSource` | Graph `/drives/{id}/items` | Site-/Item-Permissions → `site_members`, `allow` | Sensitivity Label → `vertraulichkeit` | Delta Query | nach der Demo |
| `GoogleDriveSource` | Drive API | Freigaben | Drive Labels | `changes.list` | später |
| `UploadSource` | Run-Uploads unter `data/drive/uploads/<run_id>/` | generiert: Verteiler | aus Datei oder generiert | — | **heute** |

Der Ingest kennt nur das Protocol. Ein neuer Konnektor ist eine Datei, kein Umbau.

## 6. Backend

- **Python 3.12, FastAPI, Pydantic v2, SQLite** (eine Datei unter `DATA_DIR/index/mpb.db`:
  Katalog, Chunks, BM25-Statistik, Runs, Eskalationen, Audit). Postgres + pgvector, wenn nötig.
- **Zwei Prozesse**: `mpb-knowledge` (Ingest, Index, Retrieval — hat Leserechte auf
  `data/`) und `mpb-app` (API, Workflow, Agents — hat sie **nicht**). Lokal in der Demo als
  zwei Prozesse mit Unix-Socket oder als einer mit injiziertem Client (`DEPLOYMENT.md` §5).
- **Hintergrundarbeit**: Ingest und Bewertungen laufen als Tasks im Prozess (`asyncio` +
  Thread-Pool); Zustand im Store. Kein Message-Broker, bis einer nötig ist.
- **Fehlerpolitik**: Ein Rollenlauf, der scheitert, erzeugt ein Assessment mit
  `status: failed` und Grund — nie ein fehlendes Assessment.

## 7. Frontend

- **Stufe 0 (Demo):** server-gerendertes HTML mit **Jinja + htmx**, kein Build-Schritt, jede
  Seite eine Route. Seiten: Upload, Run-Übersicht (Projekte × Status), Projekt-Detail (vier
  Spalten), Portfolio-Ranking, Eskalationen (je Owner), Audit.
- **Stufe 1:** dieselben Daten als React-SPA, wenn jemand sie will. Die API ändert sich nicht.
- **Betrachter-Prinzip:** Das Frontend rendert, was die API liefert. Die API liefert, was
  `decide(user, …)` erlaubt (Output-Klassifikation). Das Frontend filtert **nichts** selbst.
- **Login:** lokal ein `user`-Dropdown (Demo: Sattler, Kessler, Kirchner, Mustermann); in der
  Cloud Entra ID.

## 8. Cloud

Details in `DEPLOYMENT.md`. Kurz: lokal → Container → **Azure Container Apps** (Entra ID,
Graph, Key Vault — die M365-Story von LTT) mit **Fly.io** als schneller Demo-URL. Zwei
Container (`knowledge`, `app`), ein Volume nur am ersten. Anthropic-API mit Region nach
Kundenvorgabe (offen, `TODO.md`).

## 9. Was Modularität hier konkret heißt

| Aussage | Nachweis |
|---|---|
| Der Drive ist austauschbar | `DriveSource` Protocol, zwei Implementierungen ab Tag 1 (Local, Upload) |
| Die Suche ist austauschbar | `Index` Protocol; BM25 heute, Hybrid morgen, ohne Änderung am Retrieval |
| Das LLM ist austauschbar | `complete()`; `MockProvider` macht alle Tests LLM-frei |
| Rollen sind erweiterbar | ein Ordner je Rolle, `RoleRegistry` |
| Der Use Case ist austauschbar | `mpb.workflow` ist das einzige Modul, das den PMO-Ablauf kennt; ein Chat-Use-Case ist ein zweites Modul über derselben Plattform |
| Das Frontend ist austauschbar | nur JSON gegen die API |
| Berechtigungen sind an einer Stelle | `mpb.access.decide()` — drei Aufrufer, eine Wahrheit |
| Die Firma ist austauschbar | `data/` komplett ersetzen; kein Personenname im Code |

## 10. Erste Bauschritte (heute)

1. Paket-Skelett mit allen Modulgrenzen als `Protocol`s und Datentypen — die Verträge.
2. `mpb.access` vollständig (Permissions, ACL-Berechnung, `decide`) + Tests T1–T7, T13, T16, T25.
3. `mpb.knowledge`: `LocalFolderSource`, Markdown-Extractor, Chunking, Katalog, BM25, `retrieve()` mit Vorfilter + Audit.
4. `mpb.cli`: `scan`, `query --as <principal>`, `approve`.
5. Danach: `mpb.gate`, Rollen-Ordner, `MockProvider`-Runner, `mpb.merge`, API + zwei htmx-Seiten.
