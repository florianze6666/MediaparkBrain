# Informationsdomänen

Kanon-Detailstufe. Diese neun Domänen steuern, welchen Zusatzkanon ein schreibender Agent überhaupt
erhält. Sie sind NICHT die Vertraulichkeitsklassifikation des Dokuments - die kennt nach CLAUDE.md nur
`intern`, `C-Level` und `Betriebsrat-intern`.

Der Unterschied ist wesentlich: `vertraulichkeit` markiert das fertige Dokument, `informationsdomaene`
bestimmt, was der Verfasser vorher wusste. Ein als `intern` markiertes Dokument kann von jemandem
stammen, der Zugang zu `it-security-restricted` hatte.

Der Bootstrap einer Kohorte trägt ausschließlich `unternehmensweit`. Alles Weitere wird dem einzelnen
Fork additiv beigegeben.

---

## unternehmensweit

**Inhalt:** Firmenprofil, Standorte, Produktlinien, veröffentlichte Kennzahlen, gültige Organigramme,
offiziell kommunizierte Strategie, in Kraft gesetzte Policies, bekannte Großprojekte und ihr offizieller
Status, Systemlandschaft soweit jeder Anwender sie sieht.

**Rollen:** alle. **Ab:** 2011.

---

## bereichsintern

**Inhalt:** Arbeitsstand, Kapazitäten, Qualitätsprobleme und interne Konflikte einer Organisationseinheit;
Bereichsbudget und dessen Ausschöpfung; nicht eskalierte Reibungen mit Nachbarbereichen.

**Rollen:** Angehörige der jeweiligen Einheit, ihre Leitung, die zuständige Bereichsleitung. Eine Einheit
sieht die bereichsinternen Daten einer anderen Einheit NICHT.

**Ab:** 2011. Ab Q4 2022 zusätzlich je Business Unit geschnitten.

---

## projektintern

**Inhalt:** Projektkalkulation und Marge, Risikoregister, interne Terminpuffer, Aenderungshistorie,
Lieferantenprobleme im Projekt, Konflikte mit dem Kunden, Nachtragslage.

**Rollen:** Projektleitung, Projektteam, das zuständige Steering Committee, Projektcontrolling.
Ein Projektleiter sieht die projektinternen Daten fremder Projekte nicht, wohl aber deren offiziellen
Ampelstatus, sobald das PMO-Reporting existiert.

**Ab:** 2011, formalisiert mit dem PMO 2016.

---

## management

**Inhalt:** Portfoliosicht über Projekte hinweg, aggregierte Auslastung, Forecast, nicht veröffentlichte
Reorganisationsplanung im Entwurfsstadium, Personalbedarfsplanung auf Stellenebene, Bewertung von
Bereichsleistungen.

**Rollen:** Geschäftsführung, Bereichsleitungen, ab Q4 2022 Business-Unit-Leitungen, PMO- bzw.
PEO-Leitung, Controlling.

**Ab:** 2011, deutlich ausgeweitet ab 2022 durch die Kennzahlenorientierung der neuen Eigentümer.

---

## c-level-beirat

**Inhalt:** Beiratsvorlagen und -protokolle, Ausschussarbeit (Audit, Technology, Strategy & Investment),
Gesellschafterthemen, Akquisitionsprüfungen, Investitionsvorlagen über 2 Mio EUR mit NPV und IRR,
Druck auf einzelne Vorstandsmitglieder, Programmbudget-Eskalationen vor ihrer Kommunikation,
Nachfolgeplanung auf Geschäftsführungsebene.

**Rollen:** CEO, CFO, CTO, Beiratsmitglieder, Gesellschaftervertreter. In engem Umfang die
Programmleitung, soweit sie selbst berichtet.

**Vertraulichkeit im Dokument:** in aller Regel `C-Level`.

**Ab:** Q2 2022 mit dem Hansera-Einstieg. Vorher existiert ein solcher Kreis in dieser Form nicht;
davor sind es Gesellschafterbesprechungen der Familie.

---

## hr-sensitiv

**Inhalt:** Personalstammdaten, Beurteilungen, Vergütung, Krankheitsgeschehen, individuelle
Qualifizierungsbedarfe, Kündigungen und Aufhebungen, Nachfolgeplanung unterhalb der
Geschäftsführung, Personalabbau- oder Einstellungsstopp-Planungen vor ihrer Bekanntgabe.

**Rollen:** HR-Leitung und HR-Referenten, die jeweils betroffene Führungskraft, Geschäftsführung.
Ausdrücklich NICHT die Projektleitung für Mitarbeiter außerhalb ihres direkten Teams.

**Ab:** 2011.

---

## it-security-restricted

**Inhalt:** Ergebnisse von Security Reviews und Penetrationstests im Detail, bekannte ungepatchte
Schwachstellen, Berechtigungsfehler, Vorfallsanalysen, Netzsegmentierung und ihre Lücken,
Notfallkonzepte, Zugangsdaten- und Identitätsthemen, Bewertungen der Sicherheitslage von Lieferanten.

**Rollen:** IT-Leitung, Informationssicherheit, betroffene Systemverantwortliche, Geschäftsführung in
zusammengefasster Form.

**Wichtig:** Ein Fachbereich erfährt, DASS ein Review stattgefunden hat, nicht WAS es im Einzelnen
gefunden hat.

**Ab:** 2011 rudimentär, als eigene Domäne mit Substanz ab 2020 (Remote-Zugriff, VPN) und deutlich ab
2023 (Cloud, NIS2-Vorbereitung).

---

## br-intern

**Inhalt:** interne Willensbildung des Betriebsrats, Sitzungsprotokolle des Gremiums,
Verhandlungsstrategie, eingeholter Rechtsrat, Erwägung von Einigungsstelle oder juristischer
Eskalation, Beschwerden einzelner Beschäftigter, Meinungsbild im Gremium.

**Rollen:** Betriebsratsmitglieder, Gesamtbetriebsrat, hinzugezogene Sachverständige.
Ausdrücklich NICHT die Geschäftsführung und NICHT HR.

**Vertraulichkeit im Dokument:** `Betriebsrat-intern`.

**Ab:** siehe `canon/mitbestimmung.md`.

---

## br-management-verhandlung

**Inhalt:** der gemeinsame Verhandlungsstand zwischen Betriebsrat und Arbeitgeber: ausgetauschte
Entwürfe einer Betriebsvereinbarung, Protokollnotizen gemeinsamer Sitzungen, vereinbarte Fristen,
strittige und bereits geeinte Punkte.

**Rollen:** Verhandlungsführer beider Seiten, HR-Leitung, Betriebsratsvorsitz, hinzugezogene
Fachbereiche.

**Wichtig:** Dies ist die einzige Domäne, die beide Seiten teilen. Sie enthält NICHT die interne
Strategie einer der beiden Seiten - die liegt in `br-intern` beziehungsweise `management`. Ein Dokument
dieser Domäne kann als `intern` oder `Betriebsrat-intern` markiert sein, je nachdem, wer es verfasst.

**Ab:** mit der ersten formellen Verhandlung, siehe `canon/mitbestimmung.md`.

---

## Ableitungsregel für Phase 4

Ein Fork erhält den Bootstrap seiner Kohorte (`unternehmensweit`) plus das temporale Delta bis zum
Dokumentdatum plus genau die Zusatzpakete der Domänen, die in seiner Manifestzeile stehen. Steht dort
`[bereichsintern, projektintern]`, sieht er weder Beiratsmaterial noch Security-Befunde noch die interne
Willensbildung des Betriebsrats - und kann sie folglich nicht andeuten.
