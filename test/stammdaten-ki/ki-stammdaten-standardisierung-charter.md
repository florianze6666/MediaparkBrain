---
project_id: IP-2026-09
project_name: "KI-gestützte Stammdaten-Standardisierung – Material-, Lieferanten- und Kundenstamm über drei Systemlandschaften"
program: "Digital Core, Folgevorhaben"
status: proposal
start_fy: 2027
go_live_fy: 2027
project_manager: "Leitung Supply Chain Management, Kassel"
project_sponsor: "COO / Operations"
affected_countries: [DE]
source_documents:
  - "test/stammdaten-ki/ki-stammdaten-standardisierung-charter.md"
  - "test/stammdaten-ki/ki-stammdaten-standardisierung-businesscase.md"
classification: internal
dokumenttyp: Projektsteckbrief
datum: 2026-09-02
verfasser: Supply Chain Management Kassel
organisationseinheit: Operations
---

# Project Charter IP-2026-09

**Vorhaben:** KI-gestützte Stammdaten-Standardisierung
**Vorlage nach:** POL-FIN-002 §5, vorsorglich; nach Einschätzung des Antragstellers
liegt die Investitionssumme unter der Vorlagegrenze
**Stand:** 02.09.2026

## 1. Projektname

KI-gestützte Stammdaten-Standardisierung – Material-, Lieferanten- und Kundenstamm über
drei Systemlandschaften

## 2. Beschreibung des vorgeschlagenen Vorhabens

Die Stammdaten des Hauses liegen heute in drei kaufmännischen Systemen und im PLM
nebeneinander, mit abweichender Nummerierung, abweichenden Klassenlogiken und Pflegeprozessen.
Das Vorhaben legt die KI-Plattform **KORDIAL MDM** der Kordial Data GmbH als
Harmonisierungsschicht über diese Systeme. Die Plattform wird als Software-as-a-Service
aus einem europäischen Rechenzentrum des Anbieters bezogen und leistet vier Dinge:

1. **Klassenzuordnung** aller Material-, Lieferanten- und Kundenstammsätze nach einem
   einheitlichen Klassenschema, das die Plattform aus Bezeichnungen, Zeichnungsköpfen
   und Bestellhistorie ableitet.
2. **Dublettenerkennung** über Systemgrenzen hinweg, auch bei abweichender Schreibweise
   und Sprache.
3. **Golden-Record-Vorschläge**: Für jede erkannte Gruppe schlägt die Plattform einen
   führenden Datensatz vor. Erreicht die Konfidenz der Plattform mindestens 95 Prozent,
   wird der Vorschlag automatisch freigegeben und in die Quellsysteme zurückgeschrieben;
   darunter prüft ein Data Steward.
4. **Datenqualitäts-Cockpit** mit Kennzahlen zu Vollständigkeit, Durchlaufzeit und
   Rückstand, aufgeschlüsselt nach Standort, Team und Bearbeiter, mit Export in das
   Berichtswesen.

Das Vorhaben ist gestuft: Stufe 1 harmonisiert den Materialstamm der Standorte Kassel
und Eisenach, Stufe 2 nimmt Lieferanten- und Kundenstamm hinzu und koppelt das PLM,
Stufe 3 bindet die Auslandsstandorte an.

## 3. Zielsetzung

Ein Materialstamm für beide deutschen Standorte mit einheitlicher Klassenzuordnung und
einer Dublettenquote unter einem Prozent, ausgehend von heute schätzungsweise neun
Prozent. Damit entstehen die bereinigten Stammdaten, die für eine spätere Wiederaufnahme der
Engineering-Integration vorausgesetzt werden. Die Plattform soll die Frage, welcher
Datensatz führend ist, künftig regelbasiert beantworten und so die heutigen
Abstimmungsschleifen zwischen Konstruktion, Arbeitsvorbereitung und Einkauf ersetzen.

## 4. Fachlicher und organisatorischer Nutzen

- weniger Fehlbestellungen, Doppelanlagen und Nacharbeit durch widersprüchliche
  Stammdaten
- kürzere Angebotskalkulation, weil Wiederholteile über Standorte hinweg gefunden werden
- Entlastung der Konstruktion und der Arbeitsvorbereitung von manueller Suche und Pflege
- eine belastbare Zahl zur Datenqualität je Bereich, die es heute nicht gibt
- Vorbedingung für die Wiederaufnahme der Engineering-Integration und für den
  Anschluss der Auslandsstandorte

## 5. Betroffene Geschäftsprozesse

Materialanlage und -pflege, Beschaffung und Lieferantenanlage, Angebotskalkulation,
Übergabe der Stückliste von der Konstruktion an die Arbeitsvorbereitung, Kundenanlage
im Vertriebsinnendienst, Forecast und Berichtswesen.

## 6. Betroffene Organisationseinheiten

Einkauf und Supply Chain Management, Konstruktion Kassel und Eisenach,
Arbeitsvorbereitung beider Standorte, Vertriebsinnendienst, IT-Applikationen,
Controlling. In Eisenach sind zwei Bearbeiter in der Materialpflege betroffen, in Kassel
elf. Die Auslandsstandorte folgen in Stufe 3.

## 7. Business Case

Der Business Case liegt als eigenes Dokument bei. Kernzahlen: Investition 1.540.000 EUR,
Bruttonutzen 932.000 EUR je Jahr ab Vollwirkung, Amortisation rund 20 Monate.

## 8. Erwartete Kosten

Investition 1.540.000 EUR in den Jahren 2027 und 2028. Laufend ab 2028 eine
volumenabhängige Subskription mit einem Richtwert von 310.000 EUR je Jahr sowie
Support und interner Betrieb, zusammen 385.000 EUR je Jahr zahlungswirksam. Der
Aufwand der Data Stewards wird aus dem Tagesgeschäft erbracht und ist nicht beziffert.

## 9. Erwarteter wirtschaftlicher Nutzen

Vermiedene Fehler- und Dublettenkosten von 620.000 EUR je Jahr, dazu eine
Produktivitätswirkung in Konstruktion und Arbeitsvorbereitung von 3.900 Stunden je Jahr.
Beide Werte stützen sich auf eine Bereichsauswertung des Einkaufs aus dem Vorjahr und
auf Erfahrungswerte des Anbieters aus vergleichbaren Einführungen.

## 10. Geplante Laufzeit und Einführungszeitraum

Vergabe Q1/2027, Pilot Materialstamm Kassel Q2/2027, Erstbereinigung und Anbindung
Eisenach Q3/2027, Produktivsetzung Stufe 1 Q4/2027. Die Entscheidung über Stufe 2 fällt
im Q1/2028 nach Abschluss der Stufe 1. Für Stufe 3 gibt es keinen Termin.

## 11. Bekannte technische Abhängigkeiten

- Anbindung an das führende ERP-System über die Standardschnittstelle des Anbieters;
  das PLM wird in Stufe 2 gekoppelt, bis dahin bleibt die Stücklistenübergabe wie heute
- Export der Cockpit-Kennzahlen in das Berichtswesen
- Betrieb als SaaS in einem europäischen Rechenzentrum des Anbieters; die Beurteilung
  nach POL-IT-003 erfolgt nach der Vergabe im Rahmen der Einführung
- eigene Benutzerverwaltung der Plattform, eine Anbindung an das zentrale
  Identitätsmanagement ist für eine spätere Version des Anbieters angekündigt
- Datenrückgabe bei Vertragsende im Exportformat des Anbieters
- Fernzugang des Anbietersupports zur Störungsbeseitigung
- Verfügbarkeitszusage des Anbieters 99,5 Prozent; ein eigenes Wiederanlaufkonzept ist
  nicht vorgesehen, da die Quellsysteme führend bleiben
- Personenbezogene Daten werden nicht verarbeitet; die Kennungen der Bearbeiter dienen
  ausschließlich der Nachvollziehbarkeit von Freigaben
- die Datenverantwortung je Objektart wird im Projekt gemeinsam mit den
  Fachbereichen festgelegt
- Betrieb durch IT-Applikationen mit geschätzt 0,3 Vollzeitstellen

## 12. Bekannte organisatorische Abhängigkeiten

- Sechs Data Stewards aus Einkauf, Konstruktion und Arbeitsvorbereitung mit je rund
  20 Prozent ihrer Arbeitszeit, neben ihrer bisherigen Tätigkeit; eine Freistellung oder
  Vertretung ist nicht vorgesehen
- Die Key User sind dieselben, die im Teilprogramm Digital Core mitwirken
- Nach Einschätzung des Antragstellers ist das Vorhaben eine Querschnittsinitiative und
  zählt nicht auf die Initiativen einer einzelnen Business Unit nach POL-ORG-001; eine
  Abstimmung mit IT, Recht und Datenschutz zu dieser Einordnung ist nicht erfolgt
- Der Gesamtbetriebsrat wird vor der Produktivsetzung unterrichtet. Die Systembeschreibung
  wird im Rahmen der Einführung erstellt. Auswertungen des Cockpits erfolgen nur auf
  Team- und Standortebene; dies wird organisatorisch sichergestellt. Eine
  Mitbestimmungspflicht wird nicht gesehen, da das Cockpit der Prozessverbesserung dient
  und keine Leistungsbewertung vorgesehen ist
- Die Kennzahlen des Cockpits werden unbegrenzt historisiert, um Verläufe auswertbar
  zu halten

## 13. Risikoanalyse

| Risiko | Bewertung |
|---|---|
| Fachbereiche akzeptieren automatische Freigaben nicht | gering, Konfidenzschwelle einstellbar |
| Verfügbarkeit der Data Stewards neben dem Tagesgeschäft | mittel |
| Abweichung der Nutzenwerte vom Erfahrungswert des Anbieters | gering, Erfahrungswert aus vergleichbaren Häusern |
| Preisanpassung der Subskription bei steigender Datensatzzahl | gering |
| Verzögerung der Stufe 2 durch offene PLM-Kopplung | mittel |
| Einwände des Betriebsrats gegen das Cockpit | gering, keine Leistungsbewertung vorgesehen |

## 14. Begründung des erwarteten Vorteils

Wachstum ohne einheitliche Stammdaten wächst in Abstimmungsstunden mit. Das Vorhaben
setzt dort an, wo heute jeder zweite Klärungsfall zwischen Konstruktion, Arbeitsvorbereitung
und Einkauf entsteht, und wirkt über alle Business Units und beide deutschen Standorte.
Es schafft den bereinigten Stammdatenbestand, den eine spätere Engineering-Integration voraussetzt, und
liefert erstmals eine gemessene Datenqualität je Bereich. Die Amortisation liegt nach
Business Case deutlich unter zwei Jahren.

## 15. Relevante Anbieter- und Produktinformationen

Plattform: KORDIAL MDM der Kordial Data GmbH, Software-as-a-Service, Preismodell nach
Datensatzzahl mit jährlicher Anpassung. Einführungspartner: Hallermann Consulting,
Angebot mit Festpreis für Stufe 1. Referenzen des Anbieters: zwei Maschinenbauer
vergleichbarer Größe, Namen auf Anfrage. Die trainierten Klassifikationsmodelle und das
Regelwerk verbleiben beim Anbieter; die Stammdaten selbst bleiben im Eigentum des Hauses.
Angebote sind bis 31.12.2026 gültig.
