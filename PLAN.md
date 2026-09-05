# Hackathon-Konzept: Agentisches KI-Wissensmanagement für Projekt-Portfolio-Entscheidungen

> **Ergänzungen (2026-09-05):** Die Abschnitte 14 und 15 am Ende beschreiben, was dieses
> Konzept offen lässt — wie Wissen ins System kommt und aktuell bleibt, und wie Berechtigungen
> durch die gesamte Kette getragen werden. Die ausgearbeiteten Konzepte liegen unter
> [`docs/`](docs/README.md). Die Demo-Firma (Lahnberg Thermotechnik, 136 Dokumente 2011–2025)
> liegt unter `data/` — siehe [`docs/DEMOCOMPANY.md`](docs/DEMOCOMPANY.md).

## 1. Zielbild

Im Hackathon soll ein prototypisches *agentisches KI-System für die Bewertung von Projekten im Portfolio-Management* entwickelt werden.

Ausgangspunkt ist ein Projektvorschlag für ein neues Vorhaben. Häufig ist dabei Software ein wichtiger oder sogar der zentrale Bestandteil des Projekts, das System soll jedoch grundsätzlich für *allgemeines Projektmanagement* ausgelegt sein. Dieser Vorschlag wird nicht nur von einer einzelnen Instanz bewertet, sondern in einem *Multi-Stakeholder-Evaluationsprozess* aus mehreren organisatorischen Perspektiven analysiert.

Das System verbindet dabei drei zentrale Elemente:

1. *Wissensmanagement mittels RAG*
2. *spezialisierte KI-Agenten für unterschiedliche Stakeholder-Rollen*
3. *einen Orchestrator-Agenten zur Steuerung des Gesamtprozesses*

Der Schwerpunkt des Hackathons liegt nicht allein auf der automatisierten Bewertung, sondern insbesondere darauf, wie relevante Informationen gefunden, aufbereitet, zugriffsabhängig bereitgestellt, im Wissenssystem gespeichert und anschließend von unterschiedlichen Agenten für ihre jeweiligen Entscheidungen genutzt werden können.

---

## 2. Eingangspunkt: Projektvorschlag

Der Prozess beginnt mit einem *Project Owner bzw. Projektmanager*, der einen neuen Projektvorschlag einreicht.

Der Projektvorschlag muss mindestens folgende Informationen enthalten:

- Projektname
- Beschreibung des vorgeschlagenen Vorhabens und gegebenenfalls der eingesetzten Software bzw. Lösung
- Zielsetzung des Projekts
- fachlicher und organisatorischer Nutzen
- betroffene Geschäftsprozesse
- betroffene Organisationseinheiten
- Business Case
- erwartete Kosten
- erwarteter wirtschaftlicher Nutzen
- geplante Laufzeit bzw. Einführungszeitraum
- bekannte technische Abhängigkeiten
- bekannte organisatorische Abhängigkeiten
- Risikoanalyse
- Begründung, warum das Projekt für die Organisation vorteilhaft ist
- relevante Anbieter-, Produkt- bzw. Projektinformationen, soweit bereits vorhanden

Vor Beginn der eigentlichen Evaluation findet ein *Completeness Check* statt.

Erst wenn die notwendigen Mindestinformationen vorhanden sind, übergibt das System den Projektvorschlag an den agentischen Evaluationsprozess.

Fehlende Informationen führen zunächst zu einer Rückfrage bzw. Informationsanforderung und nicht unmittelbar zu einer fachlichen Bewertung.

---

## 3. Wissensmanagement als gemeinsame Informationsbasis

Das zentrale Wissensmanagement-System basiert auf einem *RAG-System*.

Es enthält sowohl bereits vorhandenes internes Wissen als auch während eines Evaluationsprozesses neu beschaffte und aufbereitete Informationen.

Für den Hackathon wird dabei eine *simulierte Unternehmenswissensdatenbank* verwendet.

Mögliche Wissensquellen sind beispielsweise:

### Interne Informationen

- Unternehmensrichtlinien
- IT-Architekturprinzipien
- Cybersecurity-Vorgaben
- Beschaffungsrichtlinien
- Compliance-Vorgaben
- Betriebsvereinbarungen
- Datenschutzrichtlinien
- vorhandene Softwarelandschaft
- Schnittstellenkataloge
- Projekt- und Portfolioinformationen
- Kosten- und Lizenzinformationen
- *Budgets und Budgetgrenzen für Projekte, Bereiche und Portfoliosegmente*
- strategische Unternehmensziele

### Externe Informationen

- Herstellerinformationen
- Produktdokumentationen
- technische Dokumentationen
- Sicherheitsinformationen
- Zertifizierungen
- regulatorische Informationen
- öffentlich verfügbare Erfahrungsberichte
- gegebenenfalls Sicherheitsmeldungen oder bekannte Schwachstellen

Externe Informationen können über einen bereits vorbereiteten *Web-/Scraping-Skill* beschafft werden.

Die Wissensbasis soll bewusst eine realistische Unternehmenssituation simulieren. Dokumente können daher *unterschiedliche, teilweise widersprüchliche oder zeitlich überholte Aussagen* enthalten. Ein älteres Dokument kann beispielsweise weiterhin eine frühere Regelung beschreiben, während ein neueres Dokument bereits aktualisierte regulatorische Anforderungen berücksichtigt. So kann etwa ein Dokument aus dem Jahr 2015 naturgemäß noch keine später eingeführten *NIS2-Anforderungen* enthalten.

Die Agenten müssen deshalb bei der Bewertung auch Aktualität, Herkunft, Gültigkeitszeitraum und gegebenenfalls Widersprüche zwischen Informationsquellen berücksichtigen.

Die Informationen sollen möglichst nicht nur temporär im Kontext eines Agenten verbleiben. Relevante, aufbereitete und nachvollziehbar belegte Informationen sollen wieder in das Wissensmanagement-System zurückgeführt werden.

Damit entsteht ein iterativer Prozess:

*Retrieve → Research → Validate → Enrich → Store → Reuse*

Das Wissenssystem entwickelt sich damit während der Evaluationsprozesse weiter.

---

## 4. Zugriffsrechte und Informationsgrenzen

Nicht jeder Agent darf zwangsläufig auf alle Informationen zugreifen.

Das Wissensmanagement berücksichtigt daher:

- Rollen
- Zugriffsrechte
- Informationsklassifikation
- gegebenenfalls vertrauliche Daten
- Herkunft und Nachvollziehbarkeit von Informationen

Ein Agent erhält zunächst nur die Informationen, die für seine Rolle vorgesehen und zugänglich sind.

Benötigt ein Agent weitere Informationen, auf die er nicht unmittelbar zugreifen darf, kann er einen *Eskalationsprozess* auslösen.

Eine Eskalation enthält mindestens:

- benötigte Information
- Begründung für den Informationsbedarf
- Zweck der Nutzung
- betroffene Bewertungskriterien
- gegebenenfalls benötigte Berechtigungsstufe

Für den Hackathon kann die eigentliche Genehmigung dieser Eskalation vereinfacht oder simuliert werden. Entscheidend ist, dass der Prozess als expliziter Bestandteil des agentischen Workflows sichtbar wird.

---

## 5. Orchestrator-Agent

Sobald der Projektvorschlag den Completeness Check bestanden hat, übernimmt ein *Orchestrator-Agent*.

Der Orchestrator ist nicht selbst einer der fachlichen Gutachter.

Seine Aufgabe besteht darin, den gesamten Multi-Agenten-Prozess zu koordinieren.

Zu seinen Aufgaben gehören insbesondere:

- Validierung, dass der Projektvorschlag vollständig ist
- Initialisierung eines Evaluationsprozesses
- Bereitstellung des relevanten Projektkontexts
- Aktivierung der vier Experten-Agenten
- Überwachung der jeweiligen Bearbeitungsstände
- Erkennung fehlender Informationen
- Koordination von Informationsanforderungen und Eskalationen
- Prüfung, ob jeder Experten-Agent sein Playbook vollständig durchlaufen hat
- Validierung der strukturierten Ergebnisse
- Zusammenführung der vier Einzelbewertungen

Die fachliche Bewertung selbst soll jedoch durch die jeweiligen Experten-Agenten erfolgen.

---

## 6. Vier Experten-Agenten

Für den Hackathon wird der Stakeholder-Kreis bewusst auf vier Rollen begrenzt.

### 6.1 Betriebsrat / Employee-Interests-Agent

Dieser Agent betrachtet das Projekt primär aus Perspektive der Beschäftigten und ihrer Rechte.

Typische Fragestellungen sind:

- Werden Mitarbeiterdaten verarbeitet?
- Entstehen neue Möglichkeiten der Leistungs- oder Verhaltenskontrolle?
- Können Beschäftigte direkt oder indirekt überwacht werden?
- Werden automatisierte Bewertungen über Mitarbeiter durchgeführt?
- Verändert das Projekt Arbeitsinhalte oder Arbeitsorganisation?
- Werden Entscheidungsrechte von Menschen auf Algorithmen übertragen?
- Besteht ein Mitbestimmungsbedarf?
- Sind Transparenz und Nachvollziehbarkeit für Beschäftigte gewährleistet?
- Bestehen Risiken für Datenschutz, Fairness oder Gleichbehandlung?

Der Agent soll insbesondere auch auf Funktionen achten, die offiziell einem anderen Zweck dienen, faktisch aber eine Mitarbeiterüberwachung ermöglichen könnten.

---

### 6.2 CFO-/Controlling-Agent

Dieser Agent beurteilt das Vorhaben aus wirtschaftlicher und finanzieller Perspektive.

Typische Fragestellungen sind:

- Wie hoch sind Investitionskosten?
- Wie hoch sind laufende Kosten?
- Wie entwickeln sich gegebenenfalls Lizenzkosten?
- Gibt es nutzungs-, user- oder volumenabhängige Kosten?
- Welche Implementierungs- und Integrationskosten entstehen?
- Welche Betriebs- und Supportkosten entstehen?
- Welche Schulungskosten entstehen?
- Welche versteckten oder indirekten Kosten sind wahrscheinlich?
- Welche finanziellen Projektrisiken bestehen?
- Wie belastbar ist der Business Case?
- Welche Einsparungen oder Produktivitätsgewinne werden erwartet?
- Wie plausibel sind ROI und gegebenenfalls Payback-Zeit?
- *Passt das Projekt in das verfügbare Budget und die geltenden Budgetgrenzen?*
- Gibt es Vendor-Lock-in- oder Preissteigerungsrisiken?

---

### 6.3 IT-, Architektur- und Cybersecurity-Agent

Dieser Agent bewertet technische Machbarkeit, Architektur, Betrieb, Compliance und Cybersecurity, soweit diese für das jeweilige Projekt relevant sind.

Dazu gehören insbesondere:

- Kompatibilität mit der bestehenden IT-Architektur
- vorhandene und notwendige Schnittstellen
- Integrationsaufwand
- Identity- und Access-Management
- Hosting-Modell
- Cloud-/On-Premise-Anforderungen
- Datenflüsse
- Datenhaltung
- Verschlüsselung
- Logging und Monitoring
- Backup und Recovery
- Verfügbarkeit
- Skalierbarkeit
- Wartbarkeit
- Exit- und Migrationsfähigkeit
- Herstellerabhängigkeit
- technische Zertifizierungen
- Security-Zertifizierungen
- bekannte Schwachstellen
- Patch- und Vulnerability-Management
- Supply-Chain-Risiken
- Erfüllung interner IT-Richtlinien
- regulatorische Anforderungen, insbesondere soweit relevant *NIS2*

Gerade dieser Agent wird bei software- oder IT-lastigen Projekten voraussichtlich intensiv den Web-/Scraping-Skill verwenden, um aktuelle Informationen über Anbieter, Produkt, Zertifizierungen, Sicherheitsmerkmale oder bekannte Risiken zu recherchieren.

Die relevanten Ergebnisse werden anschließend strukturiert in das Wissensmanagement-System zurückgespeichert.

---

### 6.4 CEO-/Strategie-Agent

Dieser Agent betrachtet das Vorhaben primär aus strategischer Unternehmensperspektive.

Zentrale Fragen sind:

- Unterstützt das Projekt die Unternehmensstrategie?
- Verbessert das Vorhaben die Wettbewerbsfähigkeit?
- Werden Geschäftsprozesse schneller oder schlanker?
- Steigert das Projekt organisatorische Agilität?
- Verbessert es die Fähigkeit, auf Marktveränderungen zu reagieren?
- Kann das Unternehmen Kundenbedürfnisse besser bedienen?
- Erhöht es Geschwindigkeit oder Qualität der Wertschöpfung?
- Schafft es strategisch relevante neue Fähigkeiten?
- Unterstützt es Skalierbarkeit oder zukünftige Geschäftsmodelle?
- Besteht die Gefahr einer strategischen Abhängigkeit von einem Anbieter?
- Ist das Vorhaben lediglich eine lokale Optimierung oder erzeugt es einen nachhaltigen strategischen Vorteil?

---

## 7. Gemeinsames Agenten-Playbook

Alle vier Experten-Agenten besitzen unterschiedliche Rollenbeschreibungen, Informationsbedarfe und Bewertungskriterien.

Der grundsätzliche Ablauf folgt jedoch einem gemeinsamen Playbook.

### Phase 1 – Informationsbedarf bestimmen

Der Agent analysiert:

- Projektvorschlag
- Business Case
- Risikoanalyse
- vorhandene Dokumentation

Anschließend bestimmt er, welche Informationen für seine Bewertung benötigt werden.

---

### Phase 2 – Wissensbeschaffung

Der Agent durchsucht zunächst das vorhandene RAG-System.

Er unterscheidet dabei zwischen:

- vorhandenen und ausreichenden Informationen
- vorhandenen, aber unzureichenden Informationen
- nicht vorhandenen Informationen
- *widersprüchlichen oder möglicherweise veralteten Informationen*

---

### Phase 3 – Externe Recherche

Soweit zulässig und erforderlich, beschafft der Agent zusätzliche Informationen über externe Quellen.

Beispielsweise:

- Hersteller-Websites
- technische Dokumentationen
- Zertifizierungsinformationen
- regulatorische Quellen
- öffentlich verfügbare Produktinformationen

Die recherchierten Informationen werden möglichst mit Quelle, Zeitpunkt und Herkunft dokumentiert.

---

### Phase 4 – Knowledge Enrichment

Neu gewonnene, relevante Informationen werden:

1. aufbereitet,
2. strukturiert,
3. mit Metadaten versehen und
4. in das gemeinsame Wissensmanagement-System zurückgeführt.

Damit können sie sowohl im aktuellen Evaluationsprozess als auch bei späteren Projekten wiederverwendet werden.

---

### Phase 5 – Eskalation bei Informationslücken

Sind notwendige Informationen weder verfügbar noch aufgrund bestehender Berechtigungen zugänglich, erstellt der Agent eine Eskalationsanforderung.

Solange eine für die Bewertung wesentliche Informationslücke besteht, muss diese im Ergebnis ausdrücklich sichtbar bleiben.

Ein Agent soll Unsicherheit nicht durch erfundene oder unbelegte Annahmen ersetzen.

---

### Phase 6 – Mehrkriterienbewertung

Sind ausreichend Informationen vorhanden, bewertet der Agent das Projekt anhand seiner rollenspezifischen Kriterien.

Die Einzelkriterien können unterschiedlich sein, das Endergebnis wird jedoch auf ein gemeinsames Bewertungsschema abgebildet.

---

### Phase 7 – Strukturierte Stellungnahme

Jeder Agent liefert dasselbe standardisierte Ergebnisformat.

Dadurch kann der Orchestrator die unterschiedlichen Bewertungen später zusammenführen und vergleichen.

---

## 8. Einheitliches Output-Schema

Jeder der vier Experten-Agenten erzeugt genau einen strukturierten Datensatz.

Das gemeinsame Schema enthält fünf Felder:

```json
{
  "role": "IT",
  "value_score": 0,
  "risk_score": 0,
  "strategy_score": 0,
  "assessment": "Freitextliche Begründung der Bewertung."
}
```

Die drei Kennzahlen sind:

### Value Score

Bewertung des erwarteten Nutzens bzw. Wertbeitrags des Projekts.

### Risk Score

Bewertung des mit dem Projekt verbundenen Risikos.

Hier muss für alle Agenten eindeutig dieselbe Skalenrichtung gelten, beispielsweise:

*hoher Wert = hohes Risiko*

### Strategy Score

Bewertung der strategischen Bedeutung bzw. des strategischen Fits des Projekts.

Für den Hackathon sollte eine einheitliche Skala festgelegt werden, beispielsweise:

*0–100*

Damit ergibt sich beispielsweise:

- 0 = sehr gering
- 50 = mittel
- 100 = sehr hoch

Beim Risk Score bedeutet entsprechend 100 ein sehr hohes Risiko.

Der Freitext assessment begründet die Kennzahlen und enthält insbesondere:

- wesentliche positive Argumente
- wesentliche negative Argumente
- kritische Risiken
- Annahmen
- verbleibende Informationslücken
- gegebenenfalls Empfehlungen oder Bedingungen

Das technische Austauschformat ist *JSONL*, sodass die vier Bewertungen als vier einzelne JSON-Objekte abgelegt bzw. weiterverarbeitet werden können.

---

## 9. Zusammenführung durch den Orchestrator

Nach Abschluss aller vier Bewertungen prüft der Orchestrator zunächst deren formale Vollständigkeit.

Für jede Rolle müssen vorliegen:

- Rollenname
- Value Score
- Risk Score
- Strategy Score
- Assessment

Anschließend können die Ergebnisse gemeinsam dargestellt werden.

Beispielsweise:

| Rolle | Value | Risk | Strategy |
|---|---:|---:|---:|
| Betriebsrat | 65 | 75 | 50 |
| CFO / Controlling | 80 | 55 | 70 |
| IT / Security | 70 | 40 | 75 |
| CEO / Strategy | 90 | 45 | 95 |

Wichtig ist dabei, die unterschiedlichen Perspektiven zunächst *nicht künstlich auf einen Konsens zu reduzieren*.

Gerade widersprüchliche Bewertungen sind für einen Multi-Stakeholder-Prozess wertvolle Informationen.

Beispielsweise könnte ein Projekt:

- strategisch außerordentlich attraktiv sein,
- finanziell sinnvoll erscheinen,
- technisch beherrschbar sein,
- gleichzeitig aber erhebliche Risiken für Beschäftigtenrechte erzeugen.

Diese Spannung soll das System sichtbar machen.

---

## 10. Ergebnis des Gesamtprozesses

Am Ende steht daher zunächst kein automatisch gefällter Managementbeschluss, sondern ein strukturierter *Decision Support*.

Das System liefert:

- vier nachvollziehbare Stakeholder-Bewertungen
- drei vergleichbare Kennzahlen pro Stakeholder
- vier qualitative Stellungnahmen
- die wesentlichen Informationsquellen
- verbleibende Informationslücken
- gegebenenfalls offene Eskalationen
- zentrale Konflikte zwischen Stakeholder-Perspektiven

Der eigentliche Portfolio- bzw. Investmententscheid kann anschließend durch einen Menschen bzw. ein entsprechendes Entscheidungsgremium getroffen werden.

---

## 11. Vereinfachte Gesamtarchitektur

```text
                 PROJECT OWNER
                      │
                      ▼
            Projektvorschlag
        + Business Case + Risiken
                      │
                      ▼
              Completeness Gate
                      │
                      ▼
              ORCHESTRATOR AGENT
                      │
       ┌──────────────┼──────────────┬──────────────┐
       │              │              │              │
       ▼              ▼              ▼              ▼
  Betriebsrat        CFO         IT/Security       CEO
     Agent           Agent          Agent          Agent
       │              │              │              │
       └──────────────┼──────────────┴──────────────┘
                      │
               gemeinsames RAG
                      │
          ┌───────────┴───────────┐
          │                       │
    internes Wissen         externe Recherche
                                Web/Scraping
          │                       │
          └───────────┬───────────┘
                      │
              Knowledge Enrichment
                      │
                      ▼
                RAG / Knowledge Base
                      │
                      ▼
             Agentenbewertungen
                      │
                      ▼
              ORCHESTRATOR AGENT
                      │
                      ▼
              Decision Support
```

---

## 12. Sinnvoller Scope für ein sechsköpfiges Hackathon-Team

Da das Team aus sechs Personen besteht, passt der technische Zuschnitt bemerkenswert gut zu sechs klaren Verantwortungsbereichen:

1. *Orchestration / Gesamtworkflow*
2. *RAG / Knowledge Management*
3. *Betriebsrat-Agent*
4. *CFO-Agent*
5. *IT-/Cybersecurity-Agent*
6. *CEO-/Strategie-Agent*

Das bedeutet nicht, dass jedes Teammitglied ausschließlich an einem Baustein arbeiten muss. Es ergibt aber eine sehr natürliche Aufteilung für Ownership und parallele Entwicklung.

Querschnittsthemen wie:

- gemeinsames Agenten-Playbook
- Output-Schema
- Prompt-Standards
- Evaluationslogik
- Demo-Szenario
- Integration

können gemeinsam definiert werden.

---

## 13. Kernidee des Hackathon-Demonstrators

Die zentrale Story des Demonstrators lautet damit:

> Ein Project Owner reicht einen Projektvorschlag ein.  
> Das System stellt sicher, dass genügend Informationen vorhanden sind.  
> Anschließend analysieren vier autonome Stakeholder-Agenten denselben Projektvorschlag aus unterschiedlichen organisatorischen Perspektiven.  
> Sie greifen auf ein gemeinsames Wissensmanagement-System zurück, beschaffen fehlendes Wissen, bewerten auch Aktualität und mögliche Widersprüche vorhandener Informationen, ergänzen die Wissensbasis, eskalieren nicht zugängliche Informationen und erstellen anschließend jeweils eine strukturierte Mehrkriterienbewertung.  
> Der Orchestrator führt diese Perspektiven zusammen und macht Nutzen, Risiken, strategischen Fit sowie bestehende Zielkonflikte für eine menschliche Portfolio-Entscheidung transparent.

Damit ist das Wissensmanagement nicht lediglich eine Datenquelle für die Agenten, sondern ein zentraler Bestandteil des gesamten agentischen Entscheidungsprozesses.

Die wichtigste neue Eigenschaft der Wissensbasis ist damit, dass sie *nicht als widerspruchsfreie „Single Source of Truth“ modelliert wird*, sondern als realistische Unternehmenswissenslandschaft mit Versionen, zeitlicher Gültigkeit und potentiell konkurrierenden Aussagen. Das ist für den RAG-/Agenten-Teil des Hackathons konzeptionell sehr wertvoll.

---

## 14. Ingest und Aktualisierung der Wissensbasis

*(Ergänzung 2026-09-05 — ausgearbeitet in [`docs/ARCHITEKTUR-RAG.md`](docs/ARCHITEKTUR-RAG.md))*

Abschnitt 3 beschreibt, *was* in der Wissensbasis liegt, nicht, *wie es hineinkommt und aktuell
bleibt*. Das ist für ein Enterprise-System die Hälfte der Arbeit:

- **Quelle:** Der Drive bzw. SharePoint des Unternehmens mit seinen Ablageorten. Die Demo-Firma
  bringt neun mit (`sharepoint_gf`, `sharepoint_finance`, `sharepoint_hr`, `br_ablage`,
  `it_doku`, `einkauf_scm`, `qm_lenkung`, `projektlaufwerk`, `mailarchiv`).
- **Einlesen:** Discovery → Fingerprint → **ACL berechnen** → Extraktion (PDF, DOCX, XLSX, MD)
  → Chunking → Metadaten → Index und Katalog. Die Reihenfolge ist Pflicht: Rechte vor Index.
- **Änderungen:** Ein Katalog mit Inhalts- und Rechte-Hash erkennt fünf Fälle — neu, geändert,
  gelöscht, verschoben, nur Rechte geändert. Verschieben ist eine Rechteänderung.
- **Dubletten:** exakt (Hash), normalisiert, Version, Near-Duplicate, Boilerplate. Dieselbe
  Datei an zwei Orten ist ein Dokument mit zwei Standorten.
- **Aktualität:** Jeder Treffer trägt Datum und Status (aktuell / überholt / unbestimmt);
  Widersprüche werden gemeldet, nicht aufgelöst.
- **Rückschreiben:** Was Agenten ins System zurückführen (Phase 4), erbt die Rechte seiner
  Quellen.

## 15. Berechtigungen — Verbindung der Rollenwelten

*(Ergänzung 2026-09-05 — ausgearbeitet in [`docs/BERECHTIGUNGSKONZEPT.md`](docs/BERECHTIGUNGSKONZEPT.md) und [`docs/ROLLEN.md`](docs/ROLLEN.md))*

Abschnitt 4 fordert Zugriffsrechte für Agenten, Abschnitt 6 beschreibt vier Rollen. Offen blieb,
wie beides mit den Berechtigungen zusammenhängt, die im Unternehmen schon existieren. Die
Antwort:

- **Ein Agent vertritt eine Rolle** und hat exakt die Rechte der Person, die sie innehat. Der
  CFO-Agent darf, was der CFO darf — nicht mehr. Der CEO-Agent sieht keine
  Betriebsratsunterlagen, weil die Geschäftsführung sie auch nicht sieht.
- **Rechte entstehen beim Einlesen** aus Ablageort (Site-Mitglieder) und Dokumentkopf
  (Vertraulichkeit, Informationsdomänen, Verteiler). Sie sind Metadaten jedes Chunks.
- **Durchsetzung als Vorfilter vor der Suche**, im Code, nie im Prompt. Verweigerte
  Dokumente sind als Stub sichtbar (Auslöser der Eskalation aus Abschnitt 4); `restricted`
  bleibt verborgen.
- **Ein einziger Zugriffsweg:** Agenten erreichen Wissen ausschließlich über `retrieve()`.
- **Output-Klassifikation:** Scores sind immer sichtbar; die Begründung nur, wenn der
  Empfänger die zitierten Quellen selbst lesen dürfte.
- **Personen sind Daten** (`data/permissions.yaml`), das Konzept ist personenunabhängig.
