# Systemarchitektur — Mediapark Brain (RAG mit Berechtigungen)

> **Status:** Entwurf v0.1, 2026-09-05, Anselm. Ergänzt `PLAN.md` um das, was dort fehlt:
> wie Wissen ins Brain kommt, wie es aktuell bleibt und wie Berechtigungen durch die
> gesamte Kette getragen werden. Das Berechtigungsmodell selbst steht in
> [`BERECHTIGUNGSKONZEPT.md`](BERECHTIGUNGSKONZEPT.md) — hier steht, **wo** es greift.

## 1. Leitsatz

Berechtigungen sind **Metadaten des Wissens, nicht Logik des Abrufs.** Sie werden beim
Einlesen erfasst, mit jedem Chunk gespeichert, beim Abruf als Vorfilter angewendet und beim
Zurückschreiben vererbt. Kein LLM entscheidet je über Zugriff.

Ein Mitarbeiter bekommt aus dem Brain genau das, was er auch im Drive sehen dürfte.

## 2. Überblick

```text
 Drive / SharePoint                       Brain
 ┌─────────────────┐     ┌──────────────────────────────────────────────┐
 │ sales/          │     │  INGEST                                       │
 │ finance/        │ ──► │  Discovery → Extraktion → Chunking            │
 │ hr/             │     │           → ACL-Tagging → Index + Katalog     │
 │ it/             │     └──────────────────┬───────────────────────────┘
 │ management/     │                        │
 │ projects/       │                        ▼
 │ _brain/  ◄──────┼──┐   ┌──────────────────────────────────────────────┐
 └─────────────────┘  │   │  KNOWLEDGE STORE                              │
                      │   │  Chunks + Metadaten + ACL + Versionen         │
                      │   └──────────────────┬───────────────────────────┘
                      │                      │  retrieve(query, ctx)
                      │                      │  → allowed / denied / conflicts
                      │                      ▼
                      │   ┌──────────────────────────────────────────────┐
                      │   │  AGENTEN (BR · CFO · IT · CEO) + ORCHESTRATOR │
                      └───┤  lesen mit Rollen-Rechten, eskalieren bei     │
        enrich()          │  Lücken, schreiben Erkenntnisse zurück        │
                          └──────────────────┬───────────────────────────┘
                                             │  Assessments (JSONL)
                                             ▼
                          ┌──────────────────────────────────────────────┐
                          │  OUTPUT-KLASSIFIKATION → Mensch               │
                          │  Scores immer, Begründung nach Clearance      │
                          └──────────────────────────────────────────────┘
```

## 3. Komponenten

| Komponente | Aufgabe | Hackathon-Minimum | Enterprise |
|---|---|---|---|
| **Quelle** | Dateien nach Bereichen, Rechte am Ordner | `data/drive/<domäne>/` lokal | SharePoint-Sites / Shared Drives |
| **Discovery** | Neue, geänderte, gelöschte, verschobene Dateien finden | Scan + Manifest-Vergleich | Graph Delta Query / Drive `changes.list` / Webhooks |
| **Extraktion** | Text aus PDF, DOCX, XLSX, MD, Bild | pypdf, python-docx, openpyxl | Azure Document Intelligence o. ä. |
| **Chunking** | Text in abrufbare Stücke schneiden | Absätze/Überschriften, ~600 Tokens, 10 % Überlappung | semantisches Chunking |
| **ACL-Tagging** | Jedem Chunk seine Rechte anheften — **vor** Indexierung | Ordner-Vererbung + Sidecar | Label-/Gruppen-Sync aus Entra ID |
| **Index** | Suche | BM25 (`rank-bm25`) | Hybrid BM25 + Embeddings, Vektor-DB mit Metadaten-Filter |
| **Katalog** | Was ist drin, in welcher Version, mit welchem Hash | SQLite `documents` | dito, zentral |
| **Retrieval** | Vorgefilterte Suche pro Principal | `retrieve(query, ctx)` | dito + Query-Rewriting |
| **Enrichment-Writer** | Agenten-Erkenntnisse zurückschreiben | Markdown nach `_brain/<domäne>/` | dito + Review-Queue |
| **Audit** | Jede Zugriffsentscheidung protokollieren | `audit.jsonl` | SIEM |

## 4. Datenquelle: Drive-Struktur

Die Demo-Firma (`DEMOCOMPANY.md`) bringt neun Ablageorte mit; jeder ist eine Domäne und trägt
ein Sidecar mit Site-Mitgliedern und Owner:

```text
data/drive/
├── sharepoint_gf/         .acl.yaml  domain: gf         site_members: [grp-management]
├── sharepoint_finance/    .acl.yaml  domain: finance    site_members: [grp-finance, grp-gf]
├── sharepoint_hr/         .acl.yaml  domain: hr         site_members: [grp-hr, grp-gf]
├── br_ablage/             .acl.yaml  domain: betriebsrat site_members: [grp-betriebsrat]
├── it_doku/               .acl.yaml  domain: it
├── einkauf_scm/           .acl.yaml  domain: einkauf
├── qm_lenkung/            .acl.yaml  domain: qm
├── projektlaufwerk/       .acl.yaml  domain: projekte   ← hier liegt der 2026-Vorschlag
│   └── <thema>/<jahr>/<datum>-<titel>.md
├── mailarchiv/            .acl.yaml  domain: mail       site_members: []  (nur Verteiler)
└── _brain/<domain>/       von Agenten zurückgeschriebenes Wissen, erbt die Domäne
```

Jedes Dokument trägt einen YAML-Kopf (`vertraulichkeit`, `informationsdomaene`,
`empfaenger`, `verfasser`, `datum`, `projekt` …). **Die ACL entsteht aus Ordner + Kopf**,
nach `data/acl-rules.yaml`; Regeln in `BERECHTIGUNGSKONZEPT.md` §6. `data/canon/` (Chronik,
Register) ist Ground Truth für uns und **kein** Ablageort — es wird nicht indexiert.

## 5. Neue Dateien einlesen (Ingest)

Reihenfolge ist Pflicht — ACL **vor** Index, sonst landen Rechte nie im Chunk:

1. **Discovery** — Datei ist neu (Pfad nicht im Katalog).
2. **Fingerprint** — `sha256(inhalt)`, Größe, `mtime`. Exakt-Dublette? → §7, kein Re-Ingest.
3. **ACL berechnen** — Sidecar des Ablageorts (Site-Mitglieder) + Dokumentkopf (Label,
   Informationsdomänen, Verteiler) nach `acl-rules.yaml`; Ergebnis
   `{domain, classification, allow, published}` + `acl_hash`. Unbekannte Namen im Verteiler
   werden ignoriert und geloggt.
4. **Extraktion** — Text nach Dateityp, Seiten-/Blattnummern behalten (Zitierbarkeit).
5. **Chunking** — mit `chunk_index`, `page`, Überlappung.
6. **Metadaten** — siehe unten. Datum aus Dateisystem **und**, falls vorhanden, aus dem
   Dokument (Frontmatter, Excel-Property, PDF-Info) — das Dokumentdatum gewinnt.
7. **Indexieren + Katalogisieren** — Chunks in Index, Dokument im Katalog mit `version: 1`.

**Chunk-Metadaten (Pflichtfelder):**

```json
{
  "chunk_id": "LTT-20221015-GF-00#3",
  "doc_id": "LTT-20221015-GF-00",
  "source_path": "sharepoint_gf/beschluss-des-programms-one-ltt/2022/2022-10-15-digitalisierungsprogramm-zur-beschlussfassung-vorleg.md",
  "domain": "gf",
  "classification": "confidential",
  "allow": ["grp-c-level", "P-002"],
  "published": false,
  "acl_hash": "a1b2…",
  "doc_date": "2022-10-15",
  "dokumenttyp": "Entscheidungsvorlage",
  "projekt": "IP-2022-03",
  "verfasser": "P-002",
  "valid_from": null,
  "valid_to": null,
  "version": 1,
  "content_hash": "8f3a…",
  "chunk_index": 3,
  "topics": ["one-ltt", "programmbudget"]
}
```

**Dateitypen:**

| Typ | Extraktion | Hinweis |
|---|---|---|
| `.md`, `.txt` | direkt, Frontmatter → Metadaten | |
| `.pdf` | pypdf; bei Scans OCR | Seite je Chunk |
| `.docx` | python-docx, Überschriften als Chunk-Grenzen | |
| `.xlsx` | openpyxl, **je Blatt** ein Dokumentteil, Kopfzeile in jeden Chunk | Zahlen bleiben mit Spaltennamen |
| Bilder | optional: Vision-Modell → Beschreibung | ACL wie Ordner |

## 6. Änderungen erkennen

Der **Katalog** (`documents`) ist die Wahrheit über den Ist-Zustand:

| Feld | Zweck |
|---|---|
| `doc_id` | stabil über Versionen |
| `path`, `size`, `mtime` | Schnellvergleich |
| `content_hash` | Inhaltsvergleich |
| `acl_hash` | Rechtevergleich |
| `version`, `status` (`active` / `superseded` / `deleted`) | Historie |
| `ingested_at` | |

Ein **Scan** vergleicht Dateisystem gegen Katalog und erkennt fünf Fälle:

| Fall | Erkennung | Aktion |
|---|---|---|
| **Neu** | Pfad unbekannt, Hash unbekannt | Ingest §5 |
| **Geändert** | Pfad bekannt, Hash anders | Alte Chunks `superseded`, neu chunken, `version + 1`, `supersedes` setzen |
| **Gelöscht** | Pfad im Katalog, nicht mehr im Drive | `status: deleted` — aus Retrieval raus, Chunks bleiben für Audit (Hard-Delete nach Frist) |
| **Verschoben** | Hash bekannt, Pfad neu | **Nur ACL neu auflösen** — Verschieben von `hr/` nach `sales/` ist eine Rechteänderung, kein Inhaltswechsel |
| **Nur Rechte geändert** | Hash gleich, `acl_hash` anders | Metadaten aller Chunks updaten, kein Re-Embedding |

Der Fall „Verschoben" ist der gefährlichste: Wer nur nach Inhalt dedupliziert, lässt ein
Dokument mit alten Rechten weiterleben.

**Enterprise:** Graph API Delta Query (SharePoint) bzw. `changes.list` (Google Drive) liefern
genau diese fünf Fälle inkrementell; Polling alle 5 Minuten oder Webhook. Der Scan-Code bleibt
derselbe, nur die Discovery-Quelle wechselt.

## 7. Dubletten vermeiden

Fünf Stufen, von billig nach teuer:

1. **Exakt** — gleicher `content_hash`. Ein Dokument, mehrere Standorte (`locations[]`).
   **Effektive ACL = Vereinigung der Standorte** — das ist SharePoint-Semantik: Die Kopie in
   `sales/` ist für Sales lesbar, auch wenn das Original in `hr/` liegt. Wer die Kopie dort
   abgelegt hat, hat die Freigabe erteilt.
2. **Normalisiert** — Text-Hash nach Whitespace-, Groß/Klein- und Metadaten-Bereinigung
   (gleiche PDF, neu exportiert). → `duplicate_of`, kanonisch ist die **neueste** Fassung;
   Retrieval liefert die kanonische und nennt „auch in: …".
3. **Version** — gleicher Pfad, neuer Hash → **keine** Dublette, sondern `version + 1`.
4. **Near-Duplicate** — später: MinHash oder Embedding-Kosinus > 0,95 → nur markieren,
   Mensch entscheidet.
5. **Boilerplate-Chunks** — identischer Chunk-Text in > 3 Dokumenten (Kopf-/Fußzeilen,
   Disclaimer) → `boilerplate: true`, aus Retrieval raus.

## 8. Aktualität und Widersprüche

Aus `PLAN.md` §3: Das Brain ist **keine** widerspruchsfreie Single Source of Truth. Deshalb:

- Jeder Chunk trägt `doc_date`, optional `valid_from` / `valid_to` und `supersedes`.
- Retrieval liefert **immer** das Datum mit und einen Status: `aktuell`, `überholt`
  (es gibt ein `supersedes`-Nachfolgedokument), `unbestimmt`.
- `detect_conflicts()` findet Treffer zum selben `topic` mit unterschiedlichem Datum und
  meldet sie als Paar `{topic, newer, older}` — der Agent muss entscheiden, das System
  verschweigt nichts.

Demo-Paare aus dem LTT-Korpus: Programmbudget ONE LTT 14,8 Mio (Vorlage 10/2022) vs. rund 19
Mio (Verschiebung 03/2024); Cloud-Linie vor und nach der NIS2-Vorbereitung 2025; Ampelstatus
der Projekte 2023 vs. Dashboard 2024. Der Korpus ist bewusst so gebaut — ein Dokument von
2023 weiß nichts vom Scope-Schnitt 2024.

## 9. Retrieval-Vertrag

```python
retrieve(query: str, ctx: RequestContext, k: int = 8) -> RetrievalResult
```

```json
{
  "allowed":   [{"chunk_id": "…", "excerpt": "…", "source_path": "…", "doc_date": "…",
                 "status": "aktuell", "classification": "internal"}],
  "denied":    [{"doc_id": "…", "title": "Lizenzkostenübersicht 2026", "domain": "finance",
                 "classification": "confidential", "reason": "no_group_membership"}],
  "conflicts": [{"topic": "NIS2", "newer": "it/richtlinie-2024.md", "older": "hr/bv-2015.md"}],
  "hidden_count": 0
}
```

Drei harte Regeln:

- **Vorfilter, nicht Nachfilter.** Die ACL-Bedingung ist Teil der Index-Abfrage. Wer erst
  Top-k holt und dann filtert, hat zwei Lecks: Die Top-k sind von verbotenen Treffern
  aufgebraucht, und das Ranking selbst verrät, was es gibt.
- **Verweigert heißt sichtbar** — als Metadaten-Stub ohne Inhalt. Das ist der Auslöser für
  die Eskalation aus `PLAN.md` §4. Ausnahme `restricted`: Existenz verborgen, nur
  `hidden_count` zählt hoch.
- **Kein Zitat aus `denied`.** Der Agent bekommt den Stub, nie einen Auszug.

## 10. Zurückschreiben (Enrichment)

`PLAN.md` §7 Phase 4 lässt Agenten Wissen zurückführen. Ohne Regel entsteht das Leck: CEO-Agent
liest vertrauliches Finance-Dokument, schreibt Zusammenfassung ins Brain, Betriebsrat-Agent
liest die Zusammenfassung.

```python
enrich(content: str, ctx: RequestContext, derived_from: list[chunk_id]) -> doc_id
```

- Klassifikation des neuen Dokuments = **Maximum** der Quellen.
- Domäne = Domäne der restriktivsten Quelle; Ablage unter `_brain/<domäne>/`.
- Frontmatter: `author: agent:cfo`, `derived_from: [...]`, `run_id`, `doc_date: heute`.
- Externe Recherche (Web-Skill) ohne interne Quellen → `internal`, `_brain/external/`.

## 11. Audit

Eine Zeile pro Entscheidung, append-only:

```json
{"ts": "2026-09-05T12:04:11Z", "run_id": "r_42", "user": "anna.hr", "agent": "cfo",
 "query": "Lizenzkosten CRM", "allowed": ["finance/budget-2026.xlsx#3"],
 "denied": ["hr/personalakten/…"], "hidden_count": 1}
```

## 12. Schnittstellen zu den anderen Teams

| Team | Bekommt von mir | Gibt mir |
|---|---|---|
| **Inputdateien** (Florian, Elke) | Ablageorte §4, Kopfformat (`data/canon`, `templates/dokumentkopf.md` der Quelle) | Neue Dokumente in `data/drive/<ablageort>/` mit Kopf — keine ACL-Pflege, Ordner + Kopf reichen |
| **Agenten** (Oxana, Frank) | `retrieve()` und `enrich()` mit `RequestContext`; Prompt-Kerne in `ROLLEN.md` | Aufrufe; Umgang mit `denied` → Eskalation |
| **Projektwissen** (Elke) | Domäne `projekte/`, der 2026-Vorschlag als Vorlage | weitere Projektvorschläge |
| **Portfolio-Logik** | Output-Klassifikation (Konzept §10) | Assessments mit `cited_chunks[]` |

## 13. Offene Entscheidungen

| # | Frage | Default, wenn nichts anderes entschieden wird |
|---|---|---|
| 1 | ~~Handelt der Agent mit Rollen-Rechten (A) oder mit den Rechten des Fragenden (B)?~~ | **Entschieden 2026-09-05: A** (Vertretungsmodell), **B** für Chat — Konzept §5 |
| 2 | Stack | Python 3.12, SQLite, `rank-bm25`; Embeddings später |
| 3 | Ist „HybridClaw" das Agent-Framework? Dann Adapter für `retrieve()` | offen |
| 4 | Wer gibt Eskalationen frei? | Domänen-Owner aus `permissions.yaml`, im Hackathon per CLI simuliert |
| 5 | Retention gelöschter Chunks | 30 Tage |
