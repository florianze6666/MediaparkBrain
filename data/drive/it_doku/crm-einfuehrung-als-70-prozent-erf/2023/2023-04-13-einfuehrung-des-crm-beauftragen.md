---
doc_id: LTT-20230413-IT-00
titel: "Projektauftrag: Einführung des CRM beauftragen"
dokumenttyp: Projektauftrag
datum: 2023-04-13
verfasser: Dr. Philipp Nowak
rolle: CIO
organisationseinheit: IT
empfaenger: ["-"]
projekt: PRJ-CRM-2023
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit, projektintern, management]
ablageort: it_doku
---

# Projektauftrag PRJ-CRM-2023 - Einführung eines konzernweiten CRM

**Programm:** ONE LTT (PRJ-ONELTT), Teilprojekt CRM
**Auftraggeber:** Dr. Philipp Nowak, CIO
**Fachlicher Auftraggeber:** Jana Ostermann, Leiterin Vertrieb
**Projektleitung:** Andrea Faber, Leiterin IT-Applikationen
**Fassung:** 1.0 vom 13.04.2023, hiermit erteilt
**Aktenzeichen:** IT-PA-2023-004

## 1. Ausgangslage

Der Vertrieb arbeitet ohne führendes System. Kundenkontakte liegen in Outlook, Chancen und
erwarteter Auftragseingang in Excel-Listen, die jeder Key Account Manager und jede Vertriebsregion
in eigener Struktur pflegt. Angebotsstände stehen teils im ERP Kassel, teils in persönlichen
Notizen. Eisenach führt zusätzlich sein eigenes ERP. Der monatliche Forecast im S&OP-Prozess
(POL-SCM-002) entsteht daher aus Zulieferungen, deren Stand, Abgrenzung und Bewertungslogik von
Person zu Person abweichen.

Die Sichtung der Vertriebsanwendungen in den ersten zwei Wochen nach meinem Eintritt bestätigt das
Bild, das die Programmvorbereitung seit Januar dokumentiert. Der Befund ist nicht neu und war auch
nicht der Anlass des Programms; er ist aber der Grund, weshalb das CRM aus dem Zielbild von ONE LTT
vorgezogen und nicht erst nach der ERP-Harmonisierung angegangen wird.

Die Produktentscheidung ist Anfang April gefallen: eingeführt wird die CRM-Anwendung der
Dynamics-365-Familie von Microsoft. Ausschlaggebend waren die bereits vorhandene Microsoft-365-Basis
mit Teams und SharePoint, der gemeinsame Identitätsdienst und der Programmleitsatz "Adopt before
adapt". Ich trage diesen Leitsatz mit, verstehe ihn aber nicht als Verbot jeder Abweichung, sondern
als Beweislastumkehr: wer vom Standard abweichen will, begründet es.

## 2. Ziel

Das CRM schafft erstmals eine konzernweite Sicht auf Pipeline, Kundenkontakte, Angebotsstatus und
erwarteten Auftragseingang. Aus dieser Sicht wird der Forecast erzeugt, statt ihn aus Listen
zusammenzutragen. Der Kundenstamm wird vereinheitlicht - ein Kunde, eine Nummer, unabhängig von
Business Unit und Standort.

Woran sich das Projekt messen lässt, zwölf Monate nach Produktivsetzung:

- alle Angebote über 250.000 EUR sind im CRM geführt, mit Status und Bewertungsdatum,
- der Auftragseingangs-Forecast wird ohne manuelle Listenzulieferung aus dem System erzeugt,
- die vertriebsseitigen Excel-Pipelines sind abgelöst und nicht durch neue ersetzt.

## 3. Gegenstand und Abgrenzung

**Gegenstand:** Kunden- und Kontaktverwaltung, Opportunity- und Angebotsverfolgung, Aktivitäten und
Besuchsberichte, Forecast, Übergabe des gewonnenen Angebots an das ERP Kassel, Auswertung über den
BI-Dienst.

**Ausdrücklich nicht Gegenstand:**

- Kalkulation und Angebotserstellung. Sie bleiben im ERP und in den bestehenden
  Kalkulationswerkzeugen. Das CRM führt den Angebots*status*, nicht den Angebots*inhalt*.
- Serviceauftragsabwicklung und Einsatzdisposition der BU Lifecycle & Service.
- Kampagnen- und Marketingfunktionen.
- Anbindung des Eisenacher ERP und der BU Compressor Systems. Stufe 1 bildet das Projektgeschäft
  von Kassel ab; Eisenach folgt erst mit der ERP-Harmonisierung, weil eine Zwischenlösung zweimal
  bezahlt und einmal weggeworfen würde.
- Jede personenbezogene Auswertung der Systemnutzung. Siehe Abschnitt 8.

## 4. Zielarchitektur und Schnittstellen

Führendes System für Kunde, Kontakt und Opportunity ist künftig das CRM. Führend für Auftrag,
Kalkulation und Fakturierung bleibt das ERP Kassel.

| Schnittstelle | Richtung | Inhalt |
|---|---|---|
| ERP Kassel - CRM | initial und laufend | Kundenstamm, Auftragshistorie |
| CRM - ERP Kassel | ereignisbezogen | gewonnenes Angebot als Auftragsanlage |
| CRM - BI-Dienst | täglich | Pipeline, Forecast, Auftragseingang |
| Identitätsdienst | Anmeldung | Rollen und Berechtigungen |
| SharePoint | Verweis | Angebots- und Kundenunterlagen, keine Doppelablage |

Die Kundenstammbereinigung ist Voraussetzung, nicht Nebenprodukt. Das Master-Data-Projekt
PRJ-MDM-2023 arbeitet am Materialstamm; für den Kundenstamm ist ein eigener Bereinigungslauf
erforderlich. Die Stammdatenrichtlinie POL-IT-006 deckt bisher nur den Materialstamm ab, ihre
Erweiterung auf Kundenstammdaten ist im Projekt zu erarbeiten und dem Programm vorzulegen.

Abweichungen vom Produktstandard bedürfen der gemeinsamen Freigabe durch die Programmleitung und
mich. Sie werden mit Aufwand, Betriebsfolge und Upgradefähigkeit dokumentiert.

## 5. Organisation

| Rolle | Person |
|---|---|
| Auftraggeber | Dr. Philipp Nowak, CIO |
| Fachlicher Auftraggeber und Prozessverantwortung Vertrieb | Jana Ostermann |
| Projektleitung | Andrea Faber |
| Abstimmung Stammdaten und ERP | Oliver Bensch |
| Programmleitung | Dr. Simone Hartwig |
| Lead Key User | Ralf Steinke |
| Key User Auslandsvertrieb | Maike Jansen, David Corley |
| Forecast-Definition und Kennzahlen | Dieter Anselm |
| Informationssicherheit | Sven Bruckner |
| Datenschutz | Sabine Kroll |

Die Verantwortung für den Vertriebsprozess und für die Qualität der eingegebenen Daten liegt bei der
Vertriebsleitung. Die IT verantwortet System, Schnittstellen, Berechtigungen und Betrieb. Diese
Trennung ist Bestandteil des Auftrags und keine Auslegungsfrage.

Berichtsweg: monatlicher Statusbericht nach POL-PM-001 an die Programmleitung, Statusbewertung nach
POL-PM-002. Eskalation über die Programmleitung an die Geschäftsführung.

## 6. Termine

| Meilenstein | Termin |
|---|---|
| Kick-off, Projektteam und Key User benannt | 08.05.2023 |
| Unterrichtung des Gesamtbetriebsrats nach BV-2023-01 | bis 28.04.2023 |
| Prozess- und Feldkonzept, Systembeschreibung mit Datenkatalog | 30.06.2023 |
| Konfiguration abgeschlossen, Schnittstellen ERP getestet | 29.09.2023 |
| Kundenstamm bereinigt und migriert | 31.10.2023 |
| Teilvereinbarung mit dem Gesamtbetriebsrat unterzeichnet | 30.11.2023 |
| Key-User- und Anwenderschulung | November bis Januar |
| Produktivsetzung Stufe 1 (Kassel, BU IHS und DGE) | 01.02.2024 |
| Stufe 2 (Vertrieb LCS, Rotterdam, Houston, Shanghai) | Q2 2024 |
| Evaluation nach zwölf Monaten | Q1 2025 |

Die Produktivsetzung setzt die unterzeichnete Teilvereinbarung voraus. Ein Start ohne sie findet
nicht statt, auch nicht befristet oder als Pilot.

## 7. Budget und Ressourcen

Das Projekt wird aus dem Programmbudget ONE LTT finanziert; ein Volumen von 1,45 Mio EUR ist
zugeordnet, davon rund 0,62 Mio EUR externe Einführungsleistung. Eine gesonderte Investitionsvorlage
nach POL-FIN-002 ist nicht erforderlich, da der Rahmen im beschlossenen Programmbudget enthalten
ist; die Einzelbeauftragung der externen Leistung erfolgt nach POL-FIN-001 in der geltenden Fassung.

Lizenz- und Betriebskosten von rund 190 TEUR jährlich für zunächst etwa 150 Nutzer fallen ab
Produktivsetzung an und sind ab dem Budget 2024 im IT-Betrieb zu führen. Diese Position endet nicht
mit dem Projekt und ist bei der Nutzenbetrachtung mitzuführen.

Intern sind 1,5 Vollzeitäquivalente aus IT-Applikationen gebunden sowie je Key User etwa zwei Tage
im Monat. Engineering-Kapazität wird nicht in Anspruch genommen. Das ist beabsichtigt: der Engpass
liegt derzeit bei Prozess- und Automatisierungsingenieuren, und dieses Projekt darf ihn nicht
vergrößern.

## 8. Mitbestimmung, Datenschutz, Informationssicherheit

Das Vorhaben fällt unter die Rahmenvereinbarung BV-2023-01 vom 16.03.2023. Das dort vereinbarte
Verfahren wird vollständig eingehalten: Unterrichtung vor Projektstart, Systembeschreibung mit
Datenkatalog, Teilvereinbarung vor Produktivsetzung, Qualifizierungszusage, Evaluation nach zwölf
Monaten.

Ich lege für die Systemauslegung fest: Auswertungen erfolgen auf der Ebene Kunde, Angebot, Business
Unit und Region. Personenbezogene Auswertungen der Systemnutzung - Anzahl der Aktivitäten,
Bearbeitungszeiten, Pflegequote je Mitarbeiter - werden weder berichtet noch technisch bereitgestellt.
Diese Zweckbindung entspricht der Linie, die seit der elektronischen Zeiterfassung 2016 in jeder
Vereinbarung des Hauses steht. Sie ist hier keine Konzession, sondern die Voraussetzung dafür, dass
die Einführung im Zeitplan bleibt.

Die Standorte Rotterdam, Houston und Shanghai unterliegen keinem deutschen Gremium. Für sie ist die
Einführung nach lokalem Recht zu prüfen; die datenschutzrechtliche Bewertung erfolgt durch die
Datenschutzbeauftragte vor Stufe 2.

Vor Produktivsetzung liegen vor: Security Assessment des Dienstes nach POL-IT-002 und POL-IT-003
sowie ein Berechtigungskonzept nach POL-IT-001 in der geltenden Fassung.

## 9. Risiken und Annahmen

| Risiko | Wirkung | Maßnahme |
|---|---|---|
| Kundenstamm unbereinigt migriert | Doppelanlagen, Pipeline nicht summierbar | eigener Bereinigungslauf vor Migration, Abnahme durch Vertriebsleitung |
| Pflegeaufwand geht von der Vertriebszeit ab | Pflege erst kurz vor dem Forecast-Meeting, Daten veralten zwischen den Terminen | Pflichtfelder je Opportunity auf acht begrenzt, mobiler Zugriff, Verzicht auf Freitextpflichten |
| Vollständig gefüllte Felder werden für belastbare Prognose gehalten | Forecast wirkt sicherer als er ist | Stichprobenreview durch Vertriebsleitung und Controlling, nicht durch die IT; Bewertungsdatum wird mitgeführt |
| Teilvereinbarung verzögert sich | Produktivsetzung verschiebt sich | Unterrichtung im April, Datenkatalog bereits zum Konzeptende |
| Ressourcenkonflikt mit dem ERP-Teilprojekt in IT-Applikationen | Verzug in beiden Vorhaben | Priorisierung durch die Programmleitung, keine stille Umverteilung |

Annahmen: das Eisenacher ERP bleibt in Stufe 1 unberührt; die Angebotskalkulation wird nicht
verlagert; die Zahl der Nutzer in Stufe 1 liegt unter 200.

## 10. Freigabe

Der Auftrag ist hiermit erteilt. Die Projektleitung nimmt die Arbeit mit dem Kick-off auf und legt
zum 30.06.2023 das Prozess- und Feldkonzept vor.

Kassel, 13.04.2023

Dr. Philipp Nowak, CIO - Jana Ostermann, Leiterin Vertrieb

**Verteiler:** Programmleitung ONE LTT, Geschäftsführung, Leitungen der Business Units, Controlling,
Qualitätsmanagement, Datenschutz, Informationssicherheit, Vorsitzende des Gesamtbetriebsrats
