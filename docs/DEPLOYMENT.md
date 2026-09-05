# Deployment — vom Laptop in die Cloud

> **Status:** v0.1, 2026-09-05, Anselm (Rolle: Systemarchitekt). Antwort auf „wir bauen alles
> mit Claude — wo läuft das nachher?". Grundsatz: **Das System läuft zuerst lokal, dann als
> Container, dann irgendwo.** Wo genau, entscheidet eine Zeile Konfiguration, nicht der Code.

## 1. Was das System zur Laufzeit braucht

| Bedarf | Lokal (heute) | Cloud (später) |
|---|---|---|
| Python 3.12+ | vorhanden | Container-Image |
| Dateiablage für `data/drive/` | Ordner im Repo | Volume oder Object Storage; bei echtem Kunden: SharePoint via Graph |
| Index + Katalog | SQLite-Datei | SQLite auf Volume; ab ~50 k Chunks Postgres + pgvector |
| LLM-Zugang | `ANTHROPIC_API_KEY` in `.env` | Secret der Plattform |
| Audit-Log | `audit.jsonl` | dieselbe Datei auf Volume, später Log-Service |
| Eingang | CLI | HTTP-API (FastAPI) + kleines Web-UI |
| Netz | keins nötig außer LLM-API | ausgehend LLM-API und Web-Recherche; eingehend nur die API |

Alles Zustandsbehaftete liegt an **einem** Ort (`DATA_DIR`). Das ist die einzige Voraussetzung,
damit lokal und Cloud derselbe Code sind.

## 2. Drei Stufen

### Stufe 0 — lokal (Hackathon)

```bash
python -m mpb.ingest scan          # Korpus einlesen
python -m mpb.access --as agent:cfo --query "Programmbudget"
python -m mpb.demo                 # Drehbuch komplett
```

`.env` mit `ANTHROPIC_API_KEY`, `DATA_DIR=./data`. Fertig. Das ist die Stufe, auf der die
Demo läuft — alles andere ist Bonus.

### Stufe 1 — Container

Ein `Dockerfile` (Python-Slim, `pip install .`, `CMD uvicorn mpb.api:app`), `DATA_DIR` als
Volume. Läuft mit `docker run` auf jedem Laptop und auf jeder Plattform, die Container
nimmt. Der Ingest läuft als Startbefehl oder als Sidecar-Job.

### Stufe 2 — Cloud

| Option | Passt, wenn | Aufwand | Anmerkung |
|---|---|---|---|
| **Azure Container Apps** | der Demo-Kunde Microsoft 365 hat (LTT: ja) | ½ Tag | Entra ID für Login, Graph für SharePoint-Adapter, Key Vault für Secrets — die Enterprise-Story aus einem Guss |
| **Fly.io / Railway / Render** | schnell eine URL, ohne Cloud-Konto-Bürokratie | 1 h | Volume für `DATA_DIR`, Secrets im Dashboard. Für die Jury-Demo völlig ausreichend |
| **Vercel** | — | — | Serverless ohne persistenten Index und ohne lange Läufe: **ungeeignet** für das RAG-Backend. Nur für ein Frontend, das die API anspricht |
| **„HybridClaw"** | unklar | ? | Kenne ich nicht. Wenn es Container mit Volume, Secrets und ausgehendem Netz kann, läuft Stufe 1 dort unverändert. Wenn es ein Agenten-Framework ist: Adapter für `retrieve()` und `enrich()`, sonst nichts — siehe §4 |

**Empfehlung:** Stufe 0 heute, Stufe 1 morgen früh, Stufe 2 auf Fly.io für die Demo-URL;
Azure als Antwort auf die Jury-Frage „und bei uns?".

## 3. LLM-Schicht

Ein Adapter, eine Funktion: `complete(system, messages, tools) -> response`. Dahinter die
Anthropic-API (Modelle: `claude-sonnet-5` für die Gutachter, `claude-haiku-4-5-20251001` für
Extraktion und Klassifikation, `claude-opus-5` für die Zusammenführung, wenn Budget da ist).
Details und aktuelle IDs: bei der Implementierung das `claude-api`-Skill laden — nicht aus dem
Gedächtnis.

Regeln, die aus dem Berechtigungskonzept folgen:

- Ein LLM-Aufruf enthält **nur** `allowed`-Chunks. Nie den Index, nie Dateipfade.
- `retrieve()` ist als Tool verfügbar; ein Datei- oder Shell-Tool ist es **nicht**.
- Der Playbook-Prompt wird gecacht (Prompt Caching), die Chunks nicht.
- **Datenresidenz:** Welche Region die API nutzt, ist beim Kunden zu klären; für LTT
  (Vorschlag §12: EU-Hosting) ist das eine Bedingung, keine Präferenz. Offen.

## 4. Adapter-Grenzen

Drei Stellen sind austauschbar, jede hinter genau einer Schnittstelle:

| Adapter | Lokal | Enterprise |
|---|---|---|
| **Drive** (`DriveSource`) | Ordner + `.acl.yaml` + Dokumentkopf | Graph API: Sites, Permissions, Sensitivity Labels, Delta Query |
| **LLM** (`complete()`) | Anthropic-API | dieselbe, oder ein Gateway des Kunden |
| **Agent-Laufzeit** | eigener Runner (Python) | ein Framework (falls „HybridClaw" eines ist) ruft `retrieve()` / `enrich()` als Tools |

Solange diese drei Grenzen halten, ist der Rest des Systems von der Umgebung unabhängig.

## 5. Betriebssicherheit

- Secrets nur aus der Umgebung; `.env` in `.gitignore`; Test, der das Repo nach Schlüsselmustern
  durchsucht.
- **Zwei Prozesse, zwei Benutzer.** Der Retrieval-Dienst (`mpb.knowledge`) läuft als
  Service-User `mpb-knowledge` mit Leserecht auf `data/drive/` und den Index. Der
  Agentenprozess (`mpb.agents`) läuft als `mpb-agents` **ohne** diese Rechte (`chmod 700`
  auf `data/`, Owner `mpb-knowledge`) und erreicht Wissen nur über die interne
  Retrieval-API. Im Container: zwei Container, das Volume nur im ersten gemountet. Lokal in
  der Demo: derselbe Effekt über einen Unix-Socket und `os.setuid`, oder — Minimum — der
  Agent-Runner bekommt keinen Pfad, nur eine `RetrievalClient`-Instanz (Konzept §2.8, T23).
- Prompt Injection aus Dokumenten trifft damit auf zwei Schichten: keine Datei-Tools im Code
  **und** keine Leserechte im Dateisystem.
- `audit.jsonl` ist append-only und liegt auf dem Volume; Rotation später.
- Keine eingehenden Verbindungen außer der API; die API authentifiziert den `user` (lokal:
  Parameter; Cloud: Entra ID / Header).

## 6. Was heute gebaut wird

Stufe 0. `pyproject.toml`, `mpb/`-Paket, `.env.example`, `python -m mpb.demo`. Das
`Dockerfile` ist zehn Zeilen und kommt, sobald die Demo lokal durchläuft.
