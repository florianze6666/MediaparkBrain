# Projektbeschreibung — Mediapark Brain

> **Status:** v0.1, 2026-09-05, Anselm (Rolle: Produktmanagement). Beschreibt Scope,
> Personas, Epics und User Stories mit Akzeptanzkriterien. Fachliches Zielbild:
> [`PLAN.md`](../PLAN.md). Technik: [`ARCHITEKTUR-RAG.md`](ARCHITEKTUR-RAG.md),
> [`BERECHTIGUNGSKONZEPT.md`](BERECHTIGUNGSKONZEPT.md), [`ROLLEN.md`](ROLLEN.md).

## 1. Ein Satz

**Primärziel:** ein enterprise-reifes RAG über dem gesamten Firmenwissen, das die
Berechtigungen des Drives konsequent respektiert. **Erster Use Case darauf:** Eine
PMO-Leiterin lädt eine Liste von 10 bis 100 Projektvorschlägen hoch und bekommt zu jedem
Projekt die Stellungnahmen eines *virtuellen Gremiums* — vier Rollen-Agenten, die mit dem
Unternehmenswissen und der Unternehmenssituation argumentieren, nicht mit allgemeinem
LLM-Wissen — bevor sie mit den echten Menschen spricht.

Die vier Rollen zum Start, erweiterbar: **CEO** (Business und Strategie), **CFO** (Finanzen
und Controlling), **Betriebsrat** (die restriktive Sicht), **IT Security**. Weitere Rollen
sind Plugins, kein Umbau (`ROLLEN.md`, `TODO.md`).

## 2. Problem

Unternehmen haben ihr Wissen in SharePoint und Drives, sortiert nach Bereichen und geschützt
durch Berechtigungen. Jeder RAG-Piloten-Versuch scheitert an derselben Stelle: Die KI sieht
entweder alles (Datenschutz und Betriebsrat stoppen das Projekt) oder nichts Vertrauliches
(dann ist sie nutzlos). Dazu kommt: Projektvorschläge werden heute von einer Person bewertet,
die eine Perspektive hat — und die Perspektiven von Controlling, IT, Betriebsrat und Strategie
werden nachgereicht, wenn überhaupt.

## 3. Zielbild

Vom Flipchart: Excel-Business-Case + PDF-Projektbeschreibung → Wissensdatenbank →
Portfolio-Evaluation (P1 98, P2 91, P3 86 …) mit Kommentaren von CEO, CFO, BR, IT-Security.

**Muss:** Dokumente auslesen · Rollenberechtigungen (technisch umgesetzt) ·
Wissensdatenbank aktualisiert sich.
**Optional:** Audio-Eingang · Prozess-Visualisierung.

## 4. Personas

Die Demo-Firma ist die Lahnberg Thermotechnik (LTT), siehe `DEMOCOMPANY.md`. Personen sind
Daten (`data/permissions.yaml`), nicht Teil des Konzepts. Die, die in der Demo sprechen:

- **Gerd Sattler (P-040, Project Excellence Office)** reicht IP-2026-02 ein und will eine
  belastbare Bewertung, ohne selbst Finance- oder Beiratsunterlagen öffnen zu dürfen.
- **Susanne Kirchner (P-032, HR-Leitung)** ist Owner des HR-SharePoints und gibt Eskalationen
  frei — oder nicht.
- **Dr. Eva Kessler (P-002, CEO)** trifft die Portfolio-Entscheidung und will Zielkonflikte
  sehen, nicht einen weichgespülten Konsens.
- **Max Mustermann (P-900, Projektingenieur)** ist der „normale Mitarbeiter", der das Brain im
  Chat-Modus fragt — und nur Veröffentlichtes und sein Projektlaufwerk bekommt.

## 5. Epics und User Stories

Format: *Als … möchte ich …, damit …* + Akzeptanzkriterien (AK). Priorität nach MoSCoW.
Status: `offen` / `in Arbeit` / `fertig`.

### E0 — Der PMO-Workflow (Use Case 1)

| ID | Story | Prio |
|---|---|---|
| **US-001** | Als **PMO-Leiterin** möchte ich eine Liste von Projektvorschlägen hochladen (Dateien: MD, DOCX, PDF, XLSX; einzeln oder als ZIP), damit ich nicht jedes Projekt einzeln einreiche. | Must |
| | AK: Upload von 10 Dateien erzeugt 10 Projekte in einem Run; jede Datei wird mit der ACL des Uploads (Verteiler: Uploaderin + Gutachter) ins Brain eingelesen. | |
| **US-002** | Als **PMO-Leiterin** möchte ich je Projekt sofort sehen, ob es vollständig ist, damit ich Lücken vor der Bewertung schließe. | Must |
| | AK: Status je Projekt: `unvollständig (Felder: …)` / `bereit` / `in Bewertung` / `bewertet`. | |
| **US-003** | Als **PMO-Leiterin** möchte ich je Projekt die Stellungnahmen der vier Rollen nebeneinander sehen, mit Scores, Begründung, Quellen und Zielkonflikten. | Must |
| | AK: Frontend zeigt je Projekt eine Karte mit vier Spalten; Begründungen nach meinen Rechten redigiert; Quellen verlinkt auf `doc_id`. | |
| **US-004** | Als **PMO-Leiterin** möchte ich die Projekte als Ranking sehen, damit ich die Gremiumssitzung vorbereiten kann. | Should |
| | AK: Tabelle aller Projekte mit drei Scores je Rolle, Gesamtwert, Sortierung, Filter „mit Zielkonflikt", „mit offener Eskalation". | |
| **US-005** | Als **Domänen-Owner** möchte ich offene Eskalationen aus allen Runs in einer Liste sehen und freigeben können. | Must |
| | AK: Eskalationsliste je Owner; Freigabe wirkt nur im jeweiligen Run. | |
| **US-006** | Als **PMO-Leiterin** möchte ich, dass die Stellungnahmen die Firma zitieren, nicht das Internet. | Must |
| | AK: Jede Aussage im Assessment trägt eine `doc_id`; Aussagen ohne Quelle sind als „Einschätzung ohne Beleg" markiert; externe Recherche ist als solche gekennzeichnet. | |

### E1 — Wissensquelle und Ingest

| ID | Story | Prio |
|---|---|---|
| **US-01** | Als **Bereichsleiter** möchte ich Dateien einfach in den Bereichsordner legen, damit sie ohne weiteres Zutun mit den richtigen Rechten im Brain landen. | Must |
| | AK: Datei in `finance/` → Chunks tragen `domain: finance, classification: confidential, allow: [grp-finance, grp-management]`. Keine manuelle Rechtevergabe. | |
| **US-02** | Als **System** möchte ich PDF, DOCX, XLSX, MD und TXT auslesen, damit alle üblichen Dokumenttypen im Brain sind. | Must |
| | AK: Je Typ ein Demo-Dokument, Text extrahiert, Seiten-/Blattnummer im Chunk. XLSX: Kopfzeile in jedem Chunk. | |
| **US-03** | Als **System** möchte ich geänderte Dateien erkennen, damit das Brain nie veraltetes Wissen als aktuell ausgibt. | Must |
| | AK: Datei geändert → alte Chunks `superseded`, neue Version `version+1`, Retrieval liefert nur die neue. | |
| **US-04** | Als **System** möchte ich gelöschte Dateien erkennen, damit gelöschtes Wissen nicht mehr abrufbar ist. | Must |
| | AK: Datei entfernt → Scan setzt `status: deleted`, Retrieval liefert sie nicht mehr, Audit hat sie noch. | |
| **US-05** | Als **Bereichsleiter** möchte ich, dass Verschieben einer Datei ihre Rechte ändert, damit der Ordner die Wahrheit bleibt. | Must |
| | AK: `hr/x.md` → `sales/x.md`: Chunks tragen `domain: sales`, ohne Re-Extraktion. | |
| **US-06** | Als **System** möchte ich Dubletten erkennen, damit dieselbe Datei nicht dreimal in den Treffern steht. | Should |
| | AK: Gleicher Hash an zwei Orten → ein Dokument, `locations: 2`, ACL = Vereinigung. | |
| **US-07** | Als **Agent** möchte ich zu jedem Treffer Datum und Gültigkeit sehen, damit ich Aktualität bewerten kann. | Must |
| | AK: Jeder Treffer hat `doc_date`, Status `aktuell` / `überholt` / `unbestimmt`. | |
| **US-08** | Als **Administrator** möchte ich den Ingest per Befehl anstoßen (`scan`), damit ich ohne Cloud-Anbindung arbeiten kann. | Must |
| | AK: `python -m mpb.ingest scan` meldet neu / geändert / gelöscht / verschoben mit Zahlen. | |

### E2 — Berechtigungen

| ID | Story | Prio |
|---|---|---|
| **US-10** | Als **Administrator** möchte ich Gruppen, Nutzer und Agenten in einer Datei pflegen, damit Rechte an einer Stelle stehen. | Must |
| | AK: `permissions.yaml` nach Konzept §13; Änderung wirkt beim nächsten Aufruf. | |
| **US-11** | Als **System** möchte ich eine einzige Entscheidungsfunktion, damit Retrieval, Enrichment und Output nie voneinander abweichen. | Must |
| | AK: `decide()` liefert `ALLOW` / `DENY` / `HIDE`; alle drei Stellen rufen sie auf; Tests T1–T6. | |
| **US-12** | Als **Bereichsleiter** möchte ich einzelne Dateien abweichend freigeben, damit ich nicht für eine Ausnahme einen Ordner anlegen muss. | Must |
| | AK: `<datei>.acl.yaml` überschreibt Ordner-ACL; T7. | |
| **US-13** | Als **HR-Leitung** möchte ich, dass Personalakten für niemanden sichtbar sind, der nicht namentlich genannt ist — auch nicht als Titel. | Must |
| | AK: `restricted` → `HIDE`; T3, T5. | |
| **US-14** | Als **Datenschutzbeauftragter** möchte ich jede Zugriffsentscheidung nachlesen können, damit ich das System freigeben kann. | Must |
| | AK: `audit.jsonl`, eine Zeile je Anfrage mit user, agent, allow/deny/hide; T12. | |
| **US-15** | Als **Administrator** möchte ich, dass ein Ordner ohne Konfiguration geschlossen ist, damit Vergessen kein Leck erzeugt. | Must |
| | AK: Ordner ohne `.acl.yaml` in der Kette → `allow: []`; T16. | |

### E3 — Retrieval

| ID | Story | Prio |
|---|---|---|
| **US-20** | Als **Agent** möchte ich nur Treffer bekommen, die ich lesen darf, und zwar bevor die besten zehn gebildet werden. | Must |
| | AK: Vorfilter; kein `denied`-Dokument in `allowed`; Top-k aus erlaubter Menge. | |
| **US-21** | Als **Agent** möchte ich sehen, dass ein Dokument existiert, das ich nicht lesen darf, damit ich eskalieren kann statt zu raten. | Must |
| | AK: `denied[]` mit `doc_id`, `title`, `domain`, `classification`, `reason` — ohne Inhalt. | |
| **US-22** | Als **Agent** möchte ich Widersprüche zwischen Dokumenten gemeldet bekommen, damit ich die aktuelle Regel anwende. | Should |
| | AK: Demo-Paar IT-Richtlinie 2015 / 2024 → `conflicts[]` mit `newer`, `older`. | |
| **US-23** | Als **Agent** möchte ich zitierfähige Treffer (Pfad, Seite, Datum), damit meine Bewertung nachvollziehbar ist. | Must |
| | AK: Jeder Treffer hat `source_path`, `page`/`chunk_index`, `doc_date`. | |
| **US-24** | Als **Mitarbeiter** möchte ich das Brain direkt fragen (Chat-Modus), damit ich Wissen aus meinem Bereich finde. | Could |
| | AK: `purpose: chat` ohne Agent → Rechte des Users; keine Output-Redaktion nötig. | |

### E4 — Agenten

| ID | Story | Prio |
|---|---|---|
| **US-30** | Als **Portfolio-Manager** möchte ich vier Gutachter mit klar getrenntem Mandat, damit Perspektiven nicht vermischt werden. | Must |
| | AK: Vier Agenten nach `ROLLEN.md` §4, jeder mit eigenem Prompt-Kern und eigener Rechte-Zeile. | |
| **US-31** | Als **Agent** möchte ich dem Playbook folgen (`PLAN.md` §7), damit alle Bewertungen vergleichbar entstehen. | Must |
| | AK: Phasen 1–7 im Ablauf sichtbar (Log). | |
| **US-32** | Als **Orchestrator** möchte ich jedes Assessment im selben Schema, damit ich sie zusammenführen kann. | Must |
| | AK: JSONL nach `PLAN.md` §8, Pydantic-valide, plus `cited_chunks[]`, `open_escalations[]`, `classification`. | |
| **US-33** | Als **Gutachter** möchte ich Lücken benennen statt füllen, damit niemand einer erfundenen Zahl vertraut. | Must |
| | AK: Assessment bei offener Eskalation enthält den Abschnitt „Informationslücken"; kein Zitat aus `denied`. | |
| **US-34** | Als **IT-Agent** möchte ich extern recherchieren (Web-Skill) und Ergebnisse mit Quelle und Datum ablegen. | Should |
| | AK: Recherche-Ergebnis als `_brain/external/…md` mit `source_url`, `retrieved_at`. | |

### E5 — Orchestrator

| ID | Story | Prio |
|---|---|---|
| **US-40** | Als **Projektleiter** möchte ich sofort erfahren, was an meinem Vorschlag fehlt, statt eine Bewertung auf Lücken zu bekommen. | Must |
| | AK: Completeness Gate gegen die 15 Felder aus `PLAN.md` §2; Rückfrageliste bei Lücken; T20. | |
| **US-41** | Als **Orchestrator** möchte ich vier Agenten starten und ihren Stand sehen. | Must |
| | AK: Run-Status je Agent: `pending` / `running` / `waiting_escalation` / `done`. | |
| **US-42** | Als **Orchestrator** möchte ich Assessments zurückweisen, die das Schema verletzen oder Verbotenes zitieren. | Must |
| | AK: Assessment mit `denied`-ID in `cited_chunks` → Zurückweisung mit Grund; T13. | |
| **US-43** | Als **Geschäftsführung** möchte ich die vier Bewertungen nebeneinander mit sichtbaren Zielkonflikten. | Must |
| | AK: Tabelle nach `PLAN.md` §9; Markierung bei > 30 Punkten Abstand; kein Mittelwert-Konsens. | |
| **US-44** | Als **Orchestrator** darf ich keine Dokumentinhalte lesen. | Must |
| | AK: `retrieve()` mit `agent: orchestrator` → Fehler; T13. | |

### E6 — Eskalation

| ID | Story | Prio |
|---|---|---|
| **US-50** | Als **Agent** möchte ich eine Eskalation mit Begründung anlegen, damit ein Mensch entscheiden kann. | Must |
| | AK: Objekt nach Konzept §9; Status `open`; Approver = Domänen-Owner. | |
| **US-51** | Als **Domänen-Owner** möchte ich Eskalationen freigeben oder ablehnen. | Must |
| | AK: CLI `approve` / `reject`; Audit-Zeile. | |
| **US-52** | Als **Datenschutzbeauftragter** möchte ich, dass eine Freigabe nur für diesen Lauf gilt. | Must |
| | AK: Grant an `run_id` gebunden, `expires_at`; T9. | |
| **US-53** | Als **Geschäftsführung** möchte ich offene Eskalationen im Ergebnis sehen. | Must |
| | AK: Report-Abschnitt „Offene Eskalationen" mit Agent, Dokument, Begründung. | |

### E7 — Enrichment

| ID | Story | Prio |
|---|---|---|
| **US-60** | Als **Agent** möchte ich belastbare Erkenntnisse ins Brain zurückschreiben, damit die nächste Bewertung davon profitiert. | Should |
| | AK: `enrich()` nach Konzept §11; Klassifikation = max, `allow` = Schnittmenge; T10. | |
| **US-61** | Als **Datenschutzbeauftragter** möchte ich, dass nichts aus `restricted` je zurückgeschrieben wird. | Must |
| | AK: Quelle `restricted` → `enrich()` lehnt ab. | |

### E8 — Ergebnis und Portfolio

| ID | Story | Prio |
|---|---|---|
| **US-70** | Als **Projektleiter** möchte ich immer die Scores sehen, auch wenn ich die Quellen nicht lesen darf. | Must |
| | AK: Scores unklassifiziert; T15. | |
| **US-71** | Als **Projektleiter** möchte ich wissen, warum eine Begründung fehlt und wen ich fragen kann. | Must |
| | AK: Platzhalter mit Domäne, Klassifikation, Approver. | |
| **US-72** | Als **Geschäftsführung** möchte ich mehrere Projekte als Portfolio-Ranking sehen (P1 98, P2 91 …). | Should |
| | AK: Gesamtwert je Projekt aus den drei Scores, Ranking, Zielkonflikte je Zeile. Formel dokumentiert. | |

### E9 — Betrieb

| ID | Story | Prio |
|---|---|---|
| **US-80** | Als **Entwickler** möchte ich das System mit einem Befehl lokal starten. | Must |
| | AK: `make demo` oder `python -m mpb.demo` läuft durch, ohne Cloud. | |
| **US-81** | Als **Team** möchte ich das System als Container bauen, damit es irgendwo läuft. | Should |
| | AK: `Dockerfile`, `docker run` startet die API. | |
| **US-82** | Als **Team** möchte ich das System in der Cloud erreichen. | Could |
| | AK: Siehe `DEPLOYMENT.md`; eine URL. | |
| **US-83** | Als **Security-Architekt** möchte ich Secrets ausschließlich aus der Umgebung lesen. | Must |
| | AK: `.env` lokal, Plattform-Secrets in der Cloud; kein Key im Repo (`.gitignore`, Test). | |

## 6. Nicht-funktionale Anforderungen

| Thema | Anforderung |
|---|---|
| Sicherheit | Alle 16 Leak-Tests grün; Berechtigung nie im Prompt |
| Nachvollziehbarkeit | Jede Bewertung zitiert Chunks; jeder Zugriff im Audit |
| Determinismus | Ingest, ACL, Retrieval-Filter sind ohne LLM testbar |
| Latenz (Demo) | Bewertung eines Vorschlags < 3 Minuten mit vier Agenten |
| Austauschbarkeit | Drive-Adapter (lokal / Graph / Google) und LLM-Adapter hinter je einer Schnittstelle |
| Datenresidenz | LLM-Aufrufe enthalten nur erlaubte Chunks; Region klären (offen) |

## 7. Demo-Drehbuch

Der Fall: **IP-2026-02 KI-Wissensassistent** — LTT will genau das einführen, was wir bauen.
Details und Fundstellen je Agent: `DEMOCOMPANY.md` §6.

1. **Sattler** reicht den Vorschlag ein (Projektlaufwerk, Verteiler GF, Portfolio-Board,
   Gesamtbetriebsrat). Completeness Gate gegen 15 Felder: vollständig → Start. (Für die Demo:
   Business-Case-Anlage kurz entfernen → Gate lehnt ab und nennt das Feld.)
2. Vier Agenten laufen. Log zeigt je Agent: Informationsbedarf → Retrieval mit
   `allowed` / `denied` / `hidden`. Der Betriebsrat-Agent hat die kürzeste `allowed`-Liste.
3. **Betriebsrat-Agent** findet BV-2023-01 (Rahmenvereinbarung) und die Konflikte CRM 2023 und
   Dashboard 2024 → verlangt Datenkatalog und Teilvereinbarung vor Pilot; `risk_score` hoch.
   **IT-Agent** findet NIS2-Vorbereitung 2025, Marktbeobachtung generative KI 09/2025 und die
   Cloud-Linie → SaaS mit EU-Hosting passt, Berechtigungsdurchsetzung ist Voraussetzung.
   **CFO-Agent** rechnet die Sensitivität nach (15 % statt 25 % → Payback im dritten Jahr) und
   vergleicht mit der Budgethistorie ONE LTT (14,8 → 19 Mio). **CEO-Agent** sieht Strategiefit
   („Stabilisieren vor transformieren", Wissensmanagementproblem 2025), aber den
   Kapazitätskonflikt mit Digital Core.
4. **Betriebsrat-Agent eskaliert** die Personalplanung nach der Einstellungsbremse (`hr/`) —
   braucht sie, um die Key-User-Belastung zu bewerten. **Kirchner** gibt frei — nur für diesen
   Lauf. Erneuter Abruf: jetzt in `allowed`. Das `hr-sensitiv`-Dokument bleibt `hidden`.
5. **Ergebnis**: Tabelle mit Zielkonflikt (CEO/IT hoch vs. Betriebsrat-Risiko hoch) markiert.
   **Sattler** sieht Scores; die CFO-Begründung ist für ihn redigiert („enthält
   sharepoint_gf/C-Level — Markus Heine fragen"). **Kessler** sieht alles außer der
   BR-Detailbegründung, die `br_ablage/` zitiert.
6. **Mustermann** fragt im Chat-Modus „Was war das Budget von ONE LTT?" → bekommt die
   veröffentlichte Programmankündigung, nicht die Beiratsvorlage; `denied` zeigt ihm, dass es
   mehr gibt.
7. Jury-Frage „und im SharePoint?" → `BERECHTIGUNGSKONZEPT.md` §14: ein Adapter.

## 8. Entscheidungen

| Datum | Entscheidung | Begründung |
|---|---|---|
| 2026-09-05 | Agent vertritt Rolle (Modell A), Output nach User klassifiziert | Sonst wertlose Bewertung bei Anstoß durch normale Mitarbeiter |
| 2026-09-05 | Rechte beim Ingest, Vorfilter im Retrieval | Leak-Klassen Ranking und Verschieben |
| 2026-09-05 | CEO-Agent ohne Betriebsrats-Ablage und HR-sensitiv | Betriebsverfassungsrecht, glaubwürdige Demo |
| 2026-09-05 | Python, SQLite, BM25 zuerst; Embeddings später | In Stunden lauffähig, Filter deterministisch testbar |
| 2026-09-05 | Demo-Firma = LTT-Korpus (startplatz_hackathon, MIT), Personas = LTT-Personen | Aufgabenstellung dort ist wortgleich mit `PLAN.md`; 136 zeitlich geschichtete Dokumente statt selbstgebauter Fixtures |
| 2026-09-05 | Personen raus aus dem Konzept, rein in `permissions.yaml` | Konzept bleibt stabil, Firma darf sich ändern |
| 2026-09-05 | ACL aus Ablageort **und** Dokumentkopf; Label verschärft nur; eine enge Veröffentlichungsregel | Entspricht SharePoint-Sites × Sensitivity Labels |

## 9. Offene Punkte

| # | Punkt | Wer |
|---|---|---|
| 1 | Ist „HybridClaw" die Ziel-Laufzeit? Was bietet sie (Python? Speicher? Secrets?) | Florian |
| 2 | LLM-Datenresidenz (EU-Region) — Anforderung des Demo-Kunden? | Team |
| 3 | Portfolio-Formel (Gewichtung der drei Scores) | Dirk-Persona / Team |
| 4 | Audio-Eingang (optional) — nur wenn E1–E6 stehen | — |
