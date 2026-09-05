# Dokumentation — Mediapark Brain

Lesereihenfolge für neue Teammitglieder: erst `PLAN.md` (Zielbild), dann die ersten drei hier.

| Dokument | Rolle | Was drinsteht |
|---|---|---|
| [`../PLAN.md`](../PLAN.md) | Fachliches Zielbild | Aufgabe des Hackathons: vier Agenten, Orchestrator, RAG, Eskalation, Output-Schema |
| [`DEMOCOMPANY.md`](DEMOCOMPANY.md) | Situation | Die Demo-Firma LTT: Ablageorte, Dokumentkopf, Personen, der 2026-Fall. **Ändert sich.** |
| [`BERECHTIGUNGSKONZEPT.md`](BERECHTIGUNGSKONZEPT.md) | Security-Architektur | Grundsätze mit Begründung, ACL-Berechnung beim Ingest, `decide()`, Eskalation, Output-Klassifikation, Bedrohungen |
| [`ROLLEN.md`](ROLLEN.md) | Fachrollen | Die vier Agenten vollständig; Rechte-Matrix Agent × Domäne — **ohne Personen** |
| [`ARCHITEKTUR-SYSTEM.md`](ARCHITEKTUR-SYSTEM.md) | Systemarchitektur | Schichten, Modulschnitt mit Schnittstellen, Rollen als Plugins, PMO-Workflow, Konnektoren, Backend, Frontend, Cloud |
| [`ARCHITEKTUR-RAG.md`](ARCHITEKTUR-RAG.md) | Wissensschicht | Ingest, Änderungserkennung, Dubletten, Aktualität, Retrieval-Vertrag, Enrichment, Audit |
| [`PROJEKTBESCHREIBUNG.md`](PROJEKTBESCHREIBUNG.md) | Produkt | Epics, User Stories mit Akzeptanzkriterien, Demo-Drehbuch, Entscheidungen |
| [`TESTKONZEPT.md`](TESTKONZEPT.md) | QA / Security | Teststufen, Leak-Tests (Angriffe), Agent-Verhaltenstests, Definition of Done |
| [`DEPLOYMENT.md`](DEPLOYMENT.md) | Betrieb | Lokal → Container → Cloud; LLM-Schicht; Adapter-Grenzen |

Daten, die zu den Konzepten gehören:

| Pfad | Inhalt |
|---|---|
| `data/drive/` | Der Korpus der Demo-Firma, ein Ordner je Ablageort, plus `.acl.yaml` und der 2026-Vorschlag |
| `data/canon/` | Ground Truth der Demo-Firma (Chronik, Register). **Nicht im RAG.** |
| `data/permissions.yaml` | Personen, Gruppen, Agenten (`represents`), Aliase |
| `data/acl-rules.yaml` | Wie aus Ablageort + Dokumentkopf die ACL entsteht |
| `data/DEMOCOMPANY-SOURCE.md` | Herkunft und Snapshot-Stand des Korpus |
