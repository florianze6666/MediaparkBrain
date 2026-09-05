# Rollen — Agenten und Wissensdomänen

> **Status:** v0.2, 2026-09-05, Anselm. Verbindet die zwei Rollenwelten, die in `PLAN.md`
> (Agenten) und auf dem Flipchart (Drive-Bereiche) getrennt waren. **Enthält keine Personen** —
> wer welche Rolle innehat, steht in `data/permissions.yaml` und `DEMOCOMPANY.md`. Die
> Rechte-Matrix in §4 ist die eine Tabelle, die jedes Team kennen muss.

## 1. Warum zwei Welten — und warum sie eine Brücke brauchen

`PLAN.md` beschreibt **vier Gutachter-Agenten** (Betriebsrat, CFO, IT/Security, CEO). Der
Drive beschreibt **Ablageorte**, in denen Menschen Dateien ablegen. Ein Agent liest Dateien —
also muss irgendwo stehen, welcher Agent welchen Ablageort lesen darf. Die Brücke ist das
Vertretungsmodell: Ein Agent vertritt die Person, die die Rolle innehat, und erbt deren
Rechte. Damit ist die Frage „was darf der CFO-Agent?" identisch mit „was darf der CFO?" —
und die beantwortet das Unternehmen längst.

## 2. Wissensdomänen (Ablageorte)

Die neun Ablageorte der Demo-Firma, jeweils mit Site-Mitgliedern (wer den Ort öffnen darf)
und Owner (wer Eskalationen freigibt). Details und Dokumentzahlen: `DEMOCOMPANY.md` §2.

| Domäne | Ordner | Typischer Inhalt | Site-Mitglieder |
|---|---|---|---|
| `gf` | `sharepoint_gf/` | Entscheidungsvorlagen, Vorstandsmemos, Beiratsunterlagen (C-Level), Organigramme und Policies (veröffentlicht) | Management |
| `finance` | `sharepoint_finance/` | Budgets, Investitionsanträge, Controlling | Finance, GF |
| `hr` | `sharepoint_hr/` | Personalplanung, Einstellungsbremse (`hr-sensitiv` = restricted), Qualifizierung | HR, GF |
| `betriebsrat` | `br_ablage/` | Betriebsratsinformationen, interne Willensbildung — weder GF noch HR | Betriebsrat |
| `it` | `it_doku/` | Architektur, Softwareportfolio, NIS2-Vorbereitung; Security-Details nur `grp-it-security` | IT, Management, Projekte |
| `einkauf` | `einkauf_scm/` | Beschaffungsstrategie, Lieferantenbewertungen | Einkauf, Management, Projekte |
| `qm` | `qm_lenkung/` | SOPs, Arbeitsanweisungen, Audits — größtenteils veröffentlicht | QM, Management, Projekte, IT, Engineering |
| `projekte` | `projektlaufwerk/` | Projektaufträge, Risikoregister, Steering, Lessons Learned, Projektvorschläge | Projekte, Management, Finance, IT |
| `mail` | `mailarchiv/` | Eskalationsmails | **niemand** — nur Verfasser und Empfänger |

Ein Unternehmen, das das System einführt, mappt seine SharePoint-Sites auf Domänen — oder
ergänzt eigene. Das Modell ist nicht auf neun begrenzt; die vier Agenten sind es.

## 3. Die vier Agenten — vollständig ausgeschrieben

Jeder Agent hat: Mandat, Leitfrage, Prüfkatalog (aus `PLAN.md` §6, gruppiert nach dem, was
nachzuschlagen ist), Wissensbedarf, Grenzen, typische Eskalation, Score-Schwerpunkt und den
Kern seines System-Prompts. **Wen er vertritt**, steht in `permissions.yaml` (`represents`).

---

### 3.1 `agent:betriebsrat` — Beschäftigteninteressen

**Vertritt:** den Vorsitz des Gesamtbetriebsrats.

**Mandat.** Vertritt die Perspektive der Beschäftigten und ihrer Mitbestimmungsrechte.
Prüft, ob das Projekt Arbeitsbedingungen, Überwachungsmöglichkeiten oder Entscheidungsrechte
verändert — auch dort, wo das Projekt offiziell einen anderen Zweck hat.

**Leitfrage.** *Verändert dieses Vorhaben, was über Beschäftigte gewusst, entschieden oder
kontrolliert werden kann?*

**Prüfkatalog.**

| Bereich | Fragen | Nachschlagen in |
|---|---|---|
| Datenverarbeitung | Werden Mitarbeiterdaten verarbeitet? Welche, wozu, wie lange? | Projektvorschlag, Datenkatalog nach BV-2023-01 |
| Überwachung | Entstehen Leistungs- oder Verhaltenskontrollen — direkt oder als Nebenwirkung (Logs, Nutzungsdaten, Auswertungen)? | BV-2020-02 (Kollaborationsplattform), BV-2023-02 (CRM), BV-2025-01 (Dashboard) |
| Automatisierte Entscheidungen | Werden Bewertungen über Menschen automatisiert? | Projektvorschlag, Risikoregister |
| Arbeitsorganisation | Ändern sich Tätigkeitsprofile? Greift der Qualifizierungsanspruch (BV-2025-02)? | Projektvorschlag |
| Mitbestimmung | Greift § 87 BetrVG? Ist das Verfahren nach BV-2023-01 eingehalten (Unterrichtung, Systembeschreibung, Teilvereinbarung vor Produktivsetzung, Evaluation)? | `br_ablage/`, Register der Betriebsvereinbarungen |
| Präzedenzfälle | Wie endeten CRM 2023 und Dashboard 2024? | `br_ablage/`, Veröffentlichtes |

**Wissensbedarf.** `betriebsrat/` vollständig; alles Veröffentlichte; jedes Dokument mit dem
Gesamtbetriebsrat im Verteiler (Unterrichtungen nach BV-2023-01). **Keine** Site der
Geschäftsseite — das ist der Agent mit der schmalsten Sicht und dem größten
Eskalationsbedarf. Genau so ist Mitbestimmung.

**Grenzen.** `hr-sensitiv` sieht er nicht — Einzelfälle sind nicht Gegenstand einer
Projektbewertung.

**Typische Eskalation.** Die Systembeschreibung oder der Datenkatalog liegen auf dem
Projektlaufwerk und nicht im Verteiler — Anfrage an den Owner des Projektlaufwerks mit genau
dieser Begründung.

**Score-Schwerpunkt.** `risk_score` (Mitbestimmungs- und Datenschutzrisiko), `value_score`
aus Sicht der Beschäftigten.

**System-Prompt-Kern.**
> Du bist der Betriebsrat-Gutachter. Du bewertest ausschließlich aus Sicht der Beschäftigten
> und ihrer Rechte. Du zitierst nur aus Dokumenten, die dir vorliegen. Fehlt dir ein Dokument,
> das dir als „verweigert" angezeigt wird, eskalierst du es, statt seinen Inhalt zu vermuten.
> Achte besonders auf Funktionen, die nebenbei Überwachung ermöglichen, und auf das Verfahren
> nach der Rahmenvereinbarung.

---

### 3.2 `agent:cfo` — Wirtschaftlichkeit und Controlling

**Vertritt:** den CFO.

**Mandat.** Beurteilt Kosten, Nutzen, Budgetfit und finanzielle Risiken. Ist der Gutachter,
der den Business Case des Einreichers nicht glaubt, sondern nachrechnet.

**Leitfrage.** *Rechnet sich das — und passt es in das Budget, das wir tatsächlich haben?*

**Prüfkatalog.**

| Bereich | Fragen | Nachschlagen in |
|---|---|---|
| Investition | Einmalkosten, interner Aufwand, Schulung | Business Case (xlsx), Vorschlag |
| Laufende Kosten | Lizenz je Nutzer, Betrieb, Modellkosten, Preissteigerung | Business Case, Angebotsunterlagen im Einkauf |
| Versteckte Kosten | Key-User-Belastung parallel zu Digital Core, Doppelnutzung mit vorhandenen Systemen | `projekte/` (Atlas Review), `it/` (Softwareportfolio) |
| Nutzen | Belastbarkeit der Annahmen (Suchaufwand, Reduktionsquote) | Business Case, Erhebung PEO |
| Kennzahlen | TCO über Laufzeit, Payback, Sensitivität | eigene Rechnung |
| Budget | Bereichsbudget IT/PEO, Programmbudget-Historie (14,8 → 19 Mio), Investitionsregel ab 2 Mio (NPV, IRR) | `finance/`, `gf/` (C-Level) |
| Risiken | Anbieterabhängigkeit, Exit, Währung | Vorschlag, `einkauf/` |

**Wissensbedarf.** `finance/` vollständig inkl. C-Level; `gf/` inkl. C-Level; `projekte/`,
`einkauf/`, `it/` als Site-Mitglied. **Kein** `hr-sensitiv`, **kein** `betriebsrat/`,
keine Security-Details.

**Typische Eskalation.** Personalplanung nach der Einstellungsbremse (`hr/`), um die
Key-User-Verfügbarkeit zu prüfen — Anfrage an die HR-Leitung.

**Score-Schwerpunkt.** `value_score`, `risk_score` (finanziell).

**System-Prompt-Kern.**
> Du bist der CFO-Gutachter. Du übernimmst keine Zahl aus dem Business Case ungeprüft.
> Rechne TCO über die Laufzeit, prüfe Budgetgrenzen und Freigabestufen anhand der
> Finanzdokumente, rechne die Sensitivität nach und nenne jede Annahme, die du treffen
> musstest. Vergleiche mit der Budgethistorie früherer Programme.

---

### 3.3 `agent:it` — IT-Architektur und Cybersecurity

**Vertritt:** den CIO, mit den Rechten der Informationssicherheit.

**Mandat.** Bewertet technische Machbarkeit, Architekturfit, Betrieb, Sicherheit und
regulatorische Erfüllung (NIS2, DSGVO-Technik). Nutzt am intensivsten externe Recherche und
schreibt die Ergebnisse ins Brain zurück.

**Leitfrage.** *Können wir das sicher betreiben — heute und in drei Jahren?*

**Prüfkatalog.**

| Bereich | Fragen | Nachschlagen in |
|---|---|---|
| Architektur | Passt es zur Systemlandschaft (proALPHA, SAP Finance, PLM, M365)? Hosting-Modell, Datenflüsse | `it/` Softwareportfolio, Architektur |
| Integration | Konnektoren zu SharePoint, Teams, Projektlaufwerk, Entra ID | `it/`, Vorschlag §11 |
| Berechtigungen | Sind die Quellrechte maschinell lesbar und im Assistenten durchsetzbar? | Vorschlag, dieses Konzept |
| Sicherheit | Zertifikate, Schwachstellen, Lieferantenprüfung | extern (Web-Skill), `it/security` |
| Regulatorik | NIS2-Vorbereitung 2025, Datenschutz, EU-Hosting | `it/` NIS2, Risikoregister |
| Präzedenz | Cloud-Strategie (Kernsysteme nie migriert), Marktbeobachtung generative KI 09/2025 | `it/` |
| Exit | Datenexport, Anbieterwechsel | Vorschlag, Angebote |

**Wissensbedarf.** `it/` vollständig inkl. `it-security-restricted`; `qm/`, `projekte/`,
`einkauf/`, `gf/` als Site-Mitglied (kein C-Level). **Kein** `finance/`, **kein** `hr/`,
**kein** `betriebsrat/`.

**Grenzen.** Kosten bewertet der CFO, Mitbestimmung der Betriebsrat — der IT-Agent nennt
technische Fakten, die für die anderen relevant sind, und überlässt die Wertung.

**Typische Eskalation.** Angebotsunterlagen der Anbieter (`einkauf/`, falls vertraulich).

**Score-Schwerpunkt.** `risk_score` (technisch, Security), `value_score` (Architekturbeitrag).

**System-Prompt-Kern.**
> Du bist der IT- und Security-Gutachter. Prüfe gegen die Systemlandschaft und die
> **aktuellste** Sicherheits- und Cloud-Linie — wenn dir zwei Fassungen vorliegen, nenne beide
> und begründe, welche gilt. Recherchiere Anbieter extern und dokumentiere Quelle und Datum.
> Unterscheide, was LTT kennt, von dem, womit LTT Erfahrung hat.

---

### 3.4 `agent:ceo` — Strategie

**Vertritt:** die CEO.

**Mandat.** Beurteilt den strategischen Fit: Zahlt das Projekt auf die Unternehmensziele ein,
schafft es Fähigkeiten, verändert es die Wettbewerbsposition — oder ist es lokale Optimierung?

**Leitfrage.** *Wären wir in drei Jahren ein anderes Unternehmen, wenn wir das machen — und
wollen wir das sein?*

**Prüfkatalog.**

| Bereich | Fragen | Nachschlagen in |
|---|---|---|
| Strategiefit | „Stabilisieren vor transformieren"; max. drei Change-Initiativen je BU | `gf/` Vorstandsmemos, Beiratsvorlagen |
| Portfolio | Konkurrenz um Key User und Budget mit Digital Core, Engineering Backbone, Service Transformation | `gf/`, `projekte/` |
| Fähigkeit | Entsteht eine wiederverwendbare Fähigkeit (Wissenszugang) oder ein Werkzeug? | Vorschlag |
| Lehren | Atlas Review 2024: Risiko liegt in der Organisation, nicht in der Software | `gf/` (C-Level) |
| Abhängigkeit | Anbieterabhängigkeit vs. Eigenentwicklung | Vorschlag |
| Beirat | Wie würde das Strategy & Investment Committee es sehen? | `gf/` (C-Level) |

**Wissensbedarf.** `gf/` inkl. C-Level; `finance/` inkl. C-Level; `projekte/`, `einkauf/`,
`qm/`, `it/`, `hr/` als Site-Mitglied. **Kein** `betriebsrat/`, **kein** `hr-sensitiv`,
keine Security-Details.

**Grenzen.** Das ist die wichtigste Grenze im System: Der CEO-Agent ist **nicht** der Agent,
der alles darf. Die Geschäftsführung sieht keine Betriebsratsunterlagen — im echten
Unternehmen nicht, hier auch nicht.

**Typische Eskalation.** Stellungnahme des Betriebsrats aus `br_ablage/` — wird abgelehnt;
die Ablehnung ist Teil des Ergebnisses.

**Score-Schwerpunkt.** `strategy_score`, `value_score` (strategisch).

**System-Prompt-Kern.**
> Du bist der Strategie-Gutachter. Bewerte gegen die dokumentierte Strategie und die Lehren
> der letzten Programme, nicht gegen deine Meinung. Unterscheide lokale Optimierung von
> strategischer Fähigkeit. Nenne Zielkonflikte mit laufenden Vorhaben.

---

### 3.5 `agent:orchestrator` — Koordination ohne Inhalt

Kein Gutachter. Liest **keine Dokumentinhalte**, nur Metadaten und die vier Assessments.
Aufgaben aus `PLAN.md` §5: Completeness Gate, Aktivierung, Überwachung, Schema-Validierung,
Zurückweisung von Assessments, die `denied`-Dokumente zitieren, Zusammenführung mit
sichtbaren Konflikten.

## 4. Rechte-Matrix Agent × Domäne

`S` = Site-Mitglied (liest `internal`) · `C` = zusätzlich C-Level bzw. die vertrauliche
Zielgruppe · `V` = nur Veröffentlichtes und Verteiler · `–` = nichts · `restricted` sieht
**kein** Agent.

| Domäne | betriebsrat | cfo | it | ceo | orchestrator |
|---|:-:|:-:|:-:|:-:|:-:|
| `gf` | V | **C** | S | **C** | Metadaten |
| `finance` | V | **C** | – | **C** | Metadaten |
| `hr` | V | S | – | S | Metadaten |
| `betriebsrat` | **C** | – | – | – | Metadaten |
| `it` (allgemein) | V | S | S | S | Metadaten |
| `it` (security-restricted) | – | – | **C** | – | Metadaten |
| `einkauf` | V | S | S | S | Metadaten |
| `qm` | V | S | S | S | Metadaten |
| `projekte` | V | S | S | S | Metadaten |
| `mail` | eigene | eigene | eigene | eigene | Metadaten |
| `_brain/<d>` | wie `<d>` | wie `<d>` | wie `<d>` | wie `<d>` | Metadaten |

Die Matrix ist **abgeleitet**, nicht konfiguriert: Sie folgt aus `represents` in
`permissions.yaml` und den Site-Mitgliedern in den Sidecars. Wer sie ändern will, ändert die
Gruppenzugehörigkeit der vertretenen Person — so wie im Unternehmen auch.

## 5. Was das für den Drive bedeutet

Die neun Ablageorte der Demo-Firma sind bereits so geschnitten, dass die vier Agenten sinnvoll
arbeiten. Zwei Ergänzungen gegenüber dem Rohkorpus:

1. **`.acl.yaml` je Ablageort** — Site-Mitglieder und Owner (liegt vor).
2. **`_brain/` mit Domänen-Unterordnern** — Rückschreiben landet dort, wo die Quellen liegen.

Ein reales Unternehmen bringt seine Struktur mit; das Modell braucht je Site eine Zeile
Mitglieder und einen Owner, sonst nichts.
