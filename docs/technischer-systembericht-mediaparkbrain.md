# Technischer Systembericht: MediaparkBrain LLM-Wiki

**Stand:** 06.09.2026  
**Projekt:** MediaparkBrain / LLM-Wiki  
**Repository:** `hackathon_rag/MediaparkBrain`  

---

## 1. Tech Stack & Startup

* **Python-Version:** `>=3.12` ([pyproject.toml:8](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/pyproject.toml#L8)), fixiert auf `3.12` in [.python-version:1](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/.python-version#L1).
* **Paketmanager & Tooling:** `uv` (Fast Python package installer & resolver).
* **Laufzeit-Abhängigkeiten ([pyproject.toml:9-22](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/pyproject.toml#L9-L22)):**
  - **Web & Server:** `fastapi>=0.141.1`, `uvicorn[standard]>=0.52.4`, `jinja2>=3.1.6`, `python-multipart>=0.0.32`
  - **LLM-Integration:** `anthropic>=1.4.0` (Standard: Claude via Anthropic Python SDK)
  - **Dokumentenverarbeitung & Parsing:** `pypdf>=6.17.0`, `pdfplumber>=0.11.10`, `python-docx>=1.2.0`, `openpyxl>=3.1.5`, `markdown>=3.10.3`, `pyyaml>=6.0`
  - **Konfiguration:** `python-dotenv>=1.2.3`
* **Entwicklungs- & Test-Abhängigkeiten ([pyproject.toml:24-25](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/pyproject.toml#L24-L25)):**
  - `pytest>=8`, `httpx>=0.27` (TestClient), `reportlab>=4.0` (dynamische Test-PDF-Generierung).
* **Umgebungsvariablen ([.env.example:1-8](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/.env.example#L1-L8)):**
  - `ANTHROPIC_API_KEY`: API-Schlüssel für Anthropic Claude (wenn ungesetzt, greifen deterministische Fallbacks und Volltext-Suchanzeige).
  - `ANTHROPIC_MODEL`: Modellname, Default: `claude-haiku-4-5-20251001`.
  - `MPB_SECRET`: 32-Byte Secret für HMAC-SHA256 Cookie-Signaturen (`mpb_user`). Fehlt es, wird zur Laufzeit ein temporäres Secret generiert.
  - *Optionale Test-Pfade:* `MPB_PAGES_DIR`, `MPB_UPLOADS_DIR`, `MPB_PROPOSALS_DIR`, `MPB_PERMISSIONS_FILE`, `MPB_CHANGELOG_FILE`.
* **Start der Anwendung:**
  - Über PowerShell-Skript [run.ps1:1-8](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/run.ps1#L1-L8): Legt die venv bewusst außerhalb von OneDrive an (`$HOME\.uv-envs\llm-wiki`) und startet Uvicorn:
    ```powershell
    uv run uvicorn app.main:app --reload --port 8000
    ```

---

## 2. Modul-Übersicht (`app/`)

| Datei | Zweck | Zentrale Klassen & Funktionen | Wichtige Einstiegspunkte |
|---|---|---|---|
| [`app/main.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py) | FastAPI-Hauptapplikation, HTTP-Routen, Middleware & Template-Kontext | `ctx()` (Template-State), `require_page()`, `require_author()`, `require_writable()`, `require_admin()`, Seed/Demo-Initialisierung | [main.py:32](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L32) (`app = FastAPI`), [main.py:167](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L167) (`ctx`) |
| [`app/access.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/access.py) | RBAC-Sicherheitskern, Identitätsprüfung, Session-Signatur & Zugriffsentscheidung | `PageMeta` (Dataclass Metadaten), `decide()`, `can_read()`, `can_write()`, `sign_user()`, `current_user()`, `readable_domains()`, `normalize_confidentiality()` | [access.py:50](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/access.py#L50) (`PageMeta`), [access.py:260](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/access.py#L260) (`decide`) |
| [`app/wiki.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/wiki.py) | Ablage & Verwaltung der Markdown-Wikiseiten, Dateisystem-Scan | `Page`, `list_pages()`, `get_page_for()`, `save_page()`, `delete_page()`, `search_snippets()`, `migrate_flat_pages()`, `save_uploaded_file()` | [wiki.py:84](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/wiki.py#L84) (`Page`), [wiki.py:212](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/wiki.py#L212) (`list_pages`), [wiki.py:266](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/wiki.py#L266) (`save_page`) |
| [`app/proposals.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/proposals.py) | Verwaltung von Projektvorschlägen, Datei-Uploads & Hash-Dublettenprüfung | `Proposal`, `save_proposal()`, `list_proposals()`, `get_proposal_for()`, `find_duplicate_file()`, `file_hash()` | [proposals.py:45](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/proposals.py#L45) (`Proposal`), [proposals.py:196](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/proposals.py#L196) (`find_duplicate_file`) |
| [`app/evaluation.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/evaluation.py) | 4-Experten-Agenten Multi-Perspektiven-Bewertung von Projektanträgen | `evaluate_proposal()`, `_build_system_prompt()`, `risk_class()`, `ROLE_CRITERIA` | [evaluation.py:12](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/evaluation.py#L12) (`ROLE_CRITERIA`), [evaluation.py:111](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/evaluation.py#L111) (`evaluate_proposal`) |
| [`app/llm.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/llm.py) | Prüfung des Anthropic-Keys; die Q&A-Synthese `ask_llm` ist mit der Route `/ask` am 06.09.2026 entfernt | `is_configured()` | [llm.py](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/llm.py) |
| [`app/llm_metadata.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/llm_metadata.py) | Automatischer Dokumentkopf- & Metadaten-Generator nach Vorlagen-Standard | `generate_header()`, `build_fallback_header()`, `is_configured()` | [llm_metadata.py:20](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/llm_metadata.py#L20) (`build_fallback_header`), [llm_metadata.py:89](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/llm_metadata.py#L89) (`generate_header`) |
| [`app/pdf_ingest.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/pdf_ingest.py) | Strukturiertes PDF-Parsing (Textlayer, Folien vs. Fließtext, Tabellen, Header/Footer-Bereinigung) | `PdfPage`, `PdfExtract`, `extract_pdf()`, `is_text_pdf()` | [pdf_ingest.py:78](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/pdf_ingest.py#L78) (`PdfExtract`), [pdf_ingest.py:307](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/pdf_ingest.py#L307) (`extract_pdf`) |
| [`app/extractors.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/extractors.py) | Multi-Format-Textextraktion (DOCX, XLSX, PDF, TXT/MD) inkl. Tabellenkonvertierung nach Markdown | `extract_text_from_file()`, `extract_docx()`, `extract_xlsx()`, `extract_pdf()`, `extract_text_file()` | [extractors.py:107](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/extractors.py#L107) (`extract_text_from_file`) |
| [`app/stats.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/stats.py) | Aggregation von Nutzungsstatistiken und Git-Aktivitätshistorie | `DocumentActivity`, `DashboardStats`, `ProposalActivity`, `get_dashboard_stats()`, `get_proposal_stats()` | [stats.py:95](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/stats.py#L95) (`get_dashboard_stats`) |

---

## 3. HTTP-Routenübersicht (`app/main.py`)

| Methode | Pfad | Zweck / Beschreibung | Auth / Rollenprüfung |
|---|---|---|---|
| `POST` | `/login` | Setzt signierten Session-Cookie `mpb_user` ([main.py:270](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L270)) | Öffentlich / Login-Simulation |
| `POST` | `/logout` | Löscht `mpb_user` Cookie ([main.py:282](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L282)) | Öffentlich |
| `GET` | `/` | Startseite des Wikis ([main.py:294](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L294)) | Alle (Gast sieht nur öffentliche Seiten) |
| `GET` | `/wiki/{slug}` | Anzeige einer Wikiseite ([main.py:304](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L304)) | `require_page` ➔ `can_read(user, meta)` (404 bei Unberechtigten) |
| `GET` | `/wiki/{slug}/edit` | Bearbeitungsmaske einer Seite ([main.py:322](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L322)) | `require_page` (404) + `require_author` (403 für Gast) |
| `POST` | `/wiki/{slug}/edit` | Speichern der geänderten Seite ([main.py:332](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L332)) | `require_author` (403) + `require_writable(user, meta)` (403) |
| `POST` | `/wiki/{slug}/delete` | Löschen einer Wikiseite ([main.py:370](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L370)) | `require_page` (404) + `require_author` (403) |
| `GET` | `/new` | Erfassungsmaske für neue Seite ([main.py:379](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L379)) | `require_author` (403 für Gast) |
| `POST` | `/new` | Speichern einer neuen Seite ([main.py:387](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L387)) | `require_author` (403) + `require_writable` (403 bei fremder Domäne) |
| `POST` | `/api/extract-document` | Extrahiert & analysiert hochgeladene Datei für Formular-Vorbefüllung ([main.py:424](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L424)) | `require_author` (403 für Gast) |
| `GET` | `/upload` | Standalone Upload-Formular ([main.py:462](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L462)) | Alle (Formular zeigt `readable_domains`) |
| `POST` | `/upload` | Direkter Upload & One-Click Überführung ins Wiki ([main.py:482](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L482)) | `require_author` (403) + `require_writable` (403) |
| `GET` | `/proposals` | Liste der sichtbaren Projektanträge ([main.py:560](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L560)) | `can_read`-gefiltert |
| `GET` | `/proposals/new` | Einreichungsmaske für Anträge ([main.py:586](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L586)) | `require_author` (403 für Gast) |
| `POST` | `/proposals/new` | Speichert Antrag mit Dublettenprüfung ([main.py:592](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L592)) | `require_author` (403) + `require_writable` (403) |
| `GET` | `/proposals/evaluate` | Multi-Agenten-Bewertung der letzten Anträge ([main.py:674](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L674)) | Alle angemeldeten Nutzer |
| `GET` | `/proposals/{slug}` | Detailansicht eines Projektvorschlags ([main.py:689](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L689)) | `require_proposal` ➔ `can_read` (404 bei Unberechtigten) |
| `POST` | `/proposals/{slug}/delete` | Löscht Projektvorschlag ([main.py:701](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L701)) | `require_proposal` + `require_author` |
| `GET` | `/dashboard` | Wiki-Statistik-Dashboard ([main.py:715](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L715)) | `get_dashboard_stats(user)` (Leak-frei gefiltert) |
| `GET` | `/dashboard/projektantraege` | Dashboard für Projektanträge ([main.py:724](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L724)) | `get_proposal_stats(user)` |
| `GET` | `/admin` | Admin-Dashboard für Rechteverwaltung ([main.py:825](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L825)) | `require_admin` (404 für Nicht-Admins) |
| `POST` | `/admin/users/save` | Ändert Name / Gruppen eines Nutzers ([main.py:851](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L851)) | `require_admin` |
| `POST` | `/admin/users/new` | Legt neuen Nutzer an ([main.py:884](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L884)) | `require_admin` |
| `POST` | `/admin/users/delete` | Entfernt Nutzer ([main.py:909](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L909)) | `require_admin` |
| `POST` | `/admin/domains/save` | Ändert Lesegruppen einer Domäne ([main.py:927](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L927)) | `require_admin` |
| `POST` | `/admin/domains/new` | Erstellt neue Domäne & Ordner ([main.py:951](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L951)) | `require_admin` |
| `POST` | `/admin/domains/delete` | Löscht leere Domäne & Ordner ([main.py:976](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L976)) | `require_admin` |
| `POST` | `/admin/groups/new` | Legt neue Gruppe an ([main.py:994](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L994)) | `require_admin` |

---

## 4. Berechtigungsmodell & Sicherheitsarchitektur

### 4.1 Rollen, Gruppen & Domänen ([permissions.yaml](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/permissions.yaml))
* **Gruppen ([permissions.yaml:7](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/permissions.yaml#L7)):** `alle`, `projekt`, `finance`, `hr`, `it`, `br`, `gf`, `einkauf`, `leitung`, `admin`.
* **Nutzer / Rollen ([permissions.yaml:9-20](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/permissions.yaml#L9-L20)):**
  - `gast`: `[]` (nicht angemeldet)
  - `mitarbeiter`: `[alle]`
  - `projektmanager`: `[alle, projekt]`
  - `pmo-leitung`: `[alle, projekt, leitung]`
  - `betriebsrat`: `[alle, br]`
  - `cfo`: `[alle, finance, einkauf, leitung]`
  - `it-security`: `[alle, it, leitung]`
  - `ceo`: `[alle, gf, finance, leitung]`
  - `hr-leitung`: `[alle, hr, leitung]`
  - `orchestrator`: `[alle]`
  - `admin`: `[alle, admin]` (Gewaltenteilung: Verwaltet nur Rechte, erhält kein automatisches Leserecht auf vertrauliche Dokumente!).
* **Domänen ([permissions.yaml:22-31](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/permissions.yaml#L22-L31)):** `allgemein` (Lobby für alle), `projekt`, `finance`, `einkauf`, `hr`, `it`, `br` (nur `br`, auch die Leitung liest nicht mit), `gf`, `mail`.

### 4.2 Die 3 Vertraulichkeitsstufen ([permissions.yaml:33-54](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/permissions.yaml#L33-L54) & [access.py:161-180](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/access.py#L161-L180))
1. **`intern` (Standard):** Für alle authentifizierten Mitarbeiter lesbar (`leseberechtigt: [alle]`).
2. **`C-Level`:** Streng isoliert für Geschäftsführung und Finanzsteuerung (`vertraulichkeit: vertraulich`, `empfaenger: [gf, finance]`).
3. **`Betriebsrat-intern`:** Streng isoliert für den Betriebsrat (`vertraulichkeit: vertraulich`, `empfaenger: [br]`).
*(Basisstufe: `oeffentlich` für uneingeschränkten Lesezugriff inklusive Gäste).*

### 4.3 Die `decide()`-Entscheidungslogik ([access.py:259-289](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/access.py#L259-L289))
Ein einziger, deterministischer Prüfpfad für jede Zugriffsentscheidung:
1. `meta.vertraulichkeit == "oeffentlich"` ➔ **`ALLOW`** (auch für Gast).
2. Nutzer ist `gast` oder hat keine Gruppen ➔ **`DENY`**.
3. Keine Schnittmenge zwischen Nutzer-Gruppen und `domaenen[meta.domaene].lesen` ➔ **`DENY`**.
4. Bei `vertraulich`: Wenn Nutzer weder Ersteller (`meta.erstellt_von`) noch in `meta.empfaenger` (per User-ID oder Gruppe) ➔ **`DENY`**.
5. Sonst ➔ **`ALLOW`**.

### 4.4 Herkunft (Provenance), Leakschutz & Stufe-2-Ablage
* **Herkunft (US-1/US-3):** Im Frontmatter werden `erstellt_von` und `erstellt_am` fest verankert und beim Bearbeiten nicht überschrieben. Bearbeiter werden separat in `geaendert_von` / `geaendert_am` protokolliert ([main.py:347-348](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L347-L348)).
* **Uniform 404 (Anti-Enumeration / Leakschutz):** Fehlende Seiten und verbotene Seiten geben exakt dieselbe 404-Meldung zurück ([main.py:257-263](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/main.py#L257-L263)).
* **Schreibregel (Write ⊆ Read):** `can_write()` erzwingt, dass ein Nutzer nur in Domänen schreiben kann, in denen er auch Leserechte besitzt ([access.py:304-315](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/access.py#L304-L315)).
* **Stufe-2-Ablageschranke ([wiki.py:158-185](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/wiki.py#L158-L185)):** `wiki.list_pages(user)` öffnet physikalisch **ausschließlich** die Verzeichnisse der Domänen, die in `access.readable_domains(user)` liegen. Fremde Verzeichnisse werden nicht einmal betreten.

---

## 5. Wikiseiten-Ablage & Dokumenten-Ingestion

* **Struktur unter `pages/` ([wiki.py:75-80](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/wiki.py#L75-L80)):**
  - Standard/Öffentlich: `pages/<domaene>/<slug>.md`
  - Vertraulich: `pages/<domaene>/vertraulich/<slug>.md`
* **Frontmatter-Format:** YAML-Header umgeben von `---` Delimitern ([wiki.py:146-150](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/wiki.py#L146-L150)), gefolgt von `# Titel` und dem Markdown-Body.
* **Dateiuploads ([wiki.py:51-60](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/wiki.py#L51-L60)):** Originaldateien werden unter `uploads/<domaene>/<sanitized_filename>` abgelegt. `sanitize_filename()` schützt vor Path-Traversal (`../`, `%2e%2e`).
* **Ingestion & Extraktion:**
  - PDF Ingestion ([pdf_ingest.py](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/pdf_ingest.py)): Liest den reinen Textlayer via `pdfplumber` (bewusst **kein OCR**, um Halluzinationen bei Finanzdaten zu verhindern), unterscheidet `folien` von `fliesstext`, entfernt wiederkehrende Kopf-/Fußzeilen am Seitenrand und extrahiert Tabellen.
  - Multi-Format Extraktion ([extractors.py](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/extractors.py)): Parst Word (.docx) und Excel (.xlsx) und wandelt Absätze, Überschriften und Tabellenzeilen direkt in standardkonforme Markdown-Tabellen (`| ... |`) um.

---

## 6. Projektvorschläge & Multi-Agenten-Bewertung

* **Ablage von Vorschlägen ([proposals.py:27](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/proposals.py#L27)):**
  - Markdown-Dateien unter `project_proposals/<slug>.md`.
  - Zugehörige Projektdateien unter `project_proposals/uploads/<slug>/<dateiname>`.
* **Dubletten-Prüfung per Hash ([proposals.py:192-216](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/proposals.py#L192-L216)):** Berechnet den SHA256-Hash hochgeladener Projektdateien und blockiert Einreichungen mit identischem Inhalt selbst unter abweichendem Projektnamen (Status 409).
* **Multi-Experten-Bewertung ([evaluation.py:12-81](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/evaluation.py#L12-L81)):**
  - **4 Rollen:**
    1. `betriebsrat`: Mitarbeiterdaten, Überwachung, Mitbestimmung, Fairness.
    2. `cfo`: ROI, TCO, Investitions-/Lizenzkosten, Payback-Zeit, Budget-Fit.
    3. `it`: Architektur, IAM, Security, NIS2, Hosting, Schnittstellen.
    4. `ceo`: Unternehmensstrategie, Agilität, Kundennutzen, Wettbewerbsvorteil.
  - **Bewertungslogik:** Ganzzahlige Scores `0–10` (10 = starke Empfehlung). Fehlen Daten, erzwingt der Prompt explizit den Status `"INFORMATION FEHLT"` und setzt den Score auf `null` (keine Annahmen oder neutrale Dummy-Werte wie 5).
  - **Output-Schema:**
    ```json
    {
      "betriebsrat": {"status": "BEWERTET", "score": 8, "begruendung": "...", "fehlende_informationen": []},
      "cfo": {"status": "BEWERTET", "score": 7, "begruendung": "...", "fehlende_informationen": []},
      "it": {"status": "INFORMATION FEHLT", "score": null, "begruendung": "...", "fehlende_informationen": ["Hosting-Modell unklar"]},
      "ceo": {"status": "BEWERTET", "score": 9, "begruendung": "...", "fehlende_informationen": []}
    }
    ```

---

## 7. LLM-Integration

* **SDK & Provider:** Anthropic Python SDK (`anthropic.Anthropic`).
* **Standard-Modell:** `claude-haiku-4-5-20251001` (konfigurierbar über `ANTHROPIC_MODEL`).
* **Keine Frage-Route in der App:** `/ask` mit Wortabgleich über `pages/` ist am 06.09.2026 entfernt worden. Suche ausschließlich über den Embedding-Wissensspeicher `qmd/` ([Wissensspeicher qmd](wissensspeicher-qmd.md)): BM25, sqlite-vec mit `nvidia/Nemotron-3-Embed-1B` und Reranker, rechtegefiltert über Collections je Vertraulichkeitsklasse. Der Wissensspeicher indiziert `corpus/`; hochgeladene Wikiseiten (`pages/`) sind noch nicht angebunden.
* **LLM-Aufrufe in der App:** Metadaten-Generator ([llm_metadata.py](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/llm_metadata.py)) und Multi-Agenten-Bewertung ([evaluation.py](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/evaluation.py)).

---

## 8. Frontend & UI-Struktur

* **Dateien in `app/templates/`:**
  - [`layout.html`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/templates/layout.html): Basislayout, Branding, Nutzer-Umschalter, Aktionsmenü, Domänen-gruppierte Seitenliste.
  - [`index.html`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/templates/index.html): Anzeige von Wikiseiten mit Markdown-Rendering & Aktions-Buttons.
  - [`_herkunft.html`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/templates/_herkunft.html): Provenance-Box (Autor, Datum, Domäne, Vertraulichkeitsstufe, Ablagepfad).
  - [`edit.html`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/templates/edit.html): Erfassungs- und Bearbeitungsmaske mit Magenta-Button **„Dokument hochladen ...“** (asynchrones Pre-Populate).
  - [`upload.html`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/templates/upload.html): Standalone Upload-Dialog.
  - [`proposal_list.html`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/templates/proposal_list.html) / [`proposal_new.html`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/templates/proposal_new.html) / [`proposal_view.html`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/templates/proposal_view.html): Antragsverwaltung.
  - [`proposal_evaluation.html`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/templates/proposal_evaluation.html): Ampel-Visualisierung (Grün/Gelb/Rot) der Multi-Experten-Bewertung.
  - [`dashboard.html`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/templates/dashboard.html) & [`dashboard_proposals.html`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/templates/dashboard_proposals.html): Statistiken & Antrags-Metriken.
  - [`admin.html`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/templates/admin.html): Rechteverwaltung für Nutzer, Gruppen, Domänen & Audit-Changelog.
* **Styling in `app/static/style.css`:**
  - Komplettes Corporate Design (Dark Magenta Theme `#e5007d`, Dark Navy Sidebar `#1b1e2b`, Status-Badges, Ampel-Farben, responsive Grid-Layouts).

---

## 9. Test-Suite & Coverage

Alle **100 Tests** laufen vollständig grün durch (`uv run pytest`):

* [`tests/conftest.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/tests/conftest.py): Fixtures für isolierte Testumgebungen (`pages_env` in `tmp_path`), Signatur-Helper `as_user(uid)` und Testdaten.
* [`tests/test_ablage.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/tests/test_ablage.py): Testet Domänenordner-Ablage, automatische Migration flacher Altdaten (`migrate_flat_pages`) und Verschieben bei Domänenwechsel.
* [`tests/test_access_routes.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/tests/test_access_routes.py): HTTP-Zugriffskontrollen, 404-Isolation unberechtigter URLs und Gast-Schreibsperre.
* [`tests/test_admin.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/tests/test_admin.py): Admin-Dashboard (US-13 bis US-16), Audit-Changelog-Schreiben, Selbstaussperrungs-Schutz.
* [`tests/test_decide.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/tests/test_decide.py): Unit-Tests aller Regeln der `access.decide()`-Matrix.
* [`tests/test_extractors.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/tests/test_extractors.py): Extraktion von DOCX-, XLSX-, PDF- und TXT-Dateien inklusive Markdown-Tabellenkonvertierung.
* [`tests/test_frontmatter.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/tests/test_frontmatter.py): Robustheit des YAML-Frontmatter-Parsers und Rendering.
* [`tests/test_pdf_ingest.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/tests/test_pdf_ingest.py): PDF-Layout-Erkennung (`folien` vs. `fliesstext`), Tabellenerkennung und Ablehnung reiner Bild-PDFs.
* [`tests/test_proposals.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/tests/test_proposals.py): Proposal-Lifecycle, Hash-Dublettenprüfung und Dateiuploads.
* [`tests/test_security_fixes.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/tests/test_security_fixes.py): Security-Fixes gegen Cookie-Manipulation, Open Redirects und URL-Enumeration.
* [`tests/test_upload_routes.py`](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/tests/test_upload_routes.py): End-to-End Upload-Routen, Pre-Population API, Path-Traversal-Abwehr und C-Level/BR-Isolierung.

---

## 10. Gaps, TODOs & Auffälligkeiten

1. **Semantische Suche nicht in der App:**
   - Die Wortsuche der App ist entfernt (06.09.2026). Die Embedding-Suche lebt im Teilprojekt `qmd/` ([Wissensspeicher qmd](wissensspeicher-qmd.md)) und indiziert `corpus/`. Offen: HTTP-Modus von QMD und Anbindung an die App, damit auch hochgeladene Wikiseiten durchsuchbar werden.
2. **Dateisystem-Synchronisation & Concurrency:**
   - Änderungen an Seiten oder Rechten schreiben direkt synchron auf die `.md`- und `.yaml`-Dateien. Für eine reine Einzelinstanz-Applikation ist dies schlank und robust; im horizontal skalierten Multi-Server-Betrieb wären Dateisperren oder eine Datenbank erforderlich.
3. **Login-Simulation:**
   - Das Nutzersystem basiert auf einer Dropdown-Simulation mit signierten Cookies. Für den Produktivbetrieb fehlt die Anbindung an ein echtes IdP (z.B. OIDC / SAML / Keycloak / Entra ID).
4. **Kein OCR bei Scans:**
   - Scans und Bild-PDFs ohne Textlayer werden in [pdf_ingest.py:10-12](file:///d:/dev/prj/hackathon_rag/MediaparkBrain/llm-wiki/app/pdf_ingest.py#L10-L12) bewusst abgewiesen, um Halluzinationen von Zahlen im Business Case zu verhindern.

