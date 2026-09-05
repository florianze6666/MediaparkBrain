---
doc_id: LTT-20250619-IT-01
titel: Überführung einer geschäftskritischen Tabelle in ein zentrales System
dokumenttyp: Arbeitsanweisung
datum: 2025-06-19
verfasser: Andrea Faber
rolle: Leiterin IT-Applikationen
organisationseinheit: IT
empfaenger: ["-"]
projekt: Excel Amnesty
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit]
ablageort: it_doku
---

# Arbeitsanweisung AA-IT-014

## Überführung einer geschäftskritischen Tabelle in ein zentrales System

| | |
|---|---|
| Dokumentnummer | AA-IT-014, Version 1.0 |
| Herausgeber | IT-Applikationen |
| Erstellt | Andrea Faber, Leiterin IT-Applikationen, 19.06.2025 |
| Geprüft | Qualitätsmanagement, Dokumentenlenkung nach POL-QM-001 |
| Freigegeben | Dr. Philipp Nowak, CIO |
| Gültig ab | 01.07.2025 |
| Geltungsbereich | alle Standorte; Dateien aus dem Verzeichnis der geschäftskritischen Tabellen |
| Nächste Prüfung | 06/2026 |
| Mitgeltende Unterlagen | POL-IT-005 Excel- und Schattenanwendungs-Governance; SOP Owner- und Versionskontrolle für geschäftskritische Tabellen vom 19.04.2025; POL-IT-006 Stammdatenrichtlinie; POL-IT-001 Zugriffsrechte und Rollenkonzept; POL-IT-002 Informationssicherheit; BV-2023-01 |

---

## 1 Zweck und Abgrenzung

Aus der Erfassung im ersten Quartal 2025 sind mehr als 430 Dateien gemeldet und rund 60 davon als
geschäftskritisch eingestuft worden. Diese Arbeitsanweisung beschreibt den Ablauf, wenn eine dieser
Dateien in ein zentrales System überführt wird.

Sie regelt nicht, **ob** überführt wird. Die Einstufung und die Entscheidung über den Zielzustand
regeln POL-IT-005 und die SOP vom 19.04.2025. Dort ist auch festgehalten, was diese Anweisung
voraussetzt: Es gibt zwei zulässige Zielzustände, und sie sind gleichwertig. Der eine ist die
Überführung in ein zentrales System, der andere ist die Datei mit benanntem Owner und
Versionskontrolle. Ein Excel-Verbot ist ausdrücklich nicht beschlossen worden, und diese Anweisung
ist keines auf Umwegen.

Nicht im Geltungsbereich sind lokale Hilfsmittel im Sinne von POL-IT-005, also Dateien, deren Ausfall
nur die Arbeit ihres Erstellers betrifft. Für sie gilt diese Anweisung nicht, auch nicht sinngemäß.

## 2 Begriffe

**Geschäftskritische Schattenanwendung** - eine Datei ausserhalb der zentralen Systeme, von der ein
Prozess, ein Termin, eine Zahl im Berichtswesen oder eine Kundenzusage abhängt, und deren Ausfall
oder Fehler über den Ersteller hinaus wirkt.

**Owner** - die im Verzeichnis eingetragene Person, die für Inhalt, Aktualität und Gültigkeit der
Datei einsteht. Der Owner ist keine IT-Rolle.

**Zielsystem** - ein zentral betriebenes System aus Abschnitt 5, in dem der Inhalt künftig geführt
wird.

**Überführung** - die Verlagerung von Datenhaltung und, soweit möglich, Rechenlogik in das
Zielsystem, verbunden mit der Stilllegung der Datei.

## 3 Voraussetzungen

Vor Beginn müssen alle fünf Punkte erfüllt sein:

1. Die Einstufung als geschäftskritisch liegt vor und ist im Verzeichnis eingetragen.
2. Ein Owner ist benannt.
3. Die Bereichsleitung hat den Zeitanteil des Owners für die Dauer der Überführung zugesagt.
4. Die gültige Fassung der Datei ist eindeutig identifiziert - eine Datei, ein Stand, ein
   Speicherort. Existieren mehrere Fassungen im Umlauf, ist das vorher zu klären.
5. Ein Zielsystem ist nach Abschnitt 5 bestimmt.

Fehlt einer der Punkte, wird nicht begonnen. Erfahrungsgemäss ist Punkt 4 der Punkt, an dem die
meiste Zeit verloren geht, wenn man ihn überspringt.

## 4 Ablauf

| Schritt | Inhalt | Verantwortung |
|---|---|---|
| 1 | **Steckbrief erstellen.** Formular F-IT-014-1: Zweck, Nutzerkreis, Nutzungsfrequenz, Datenquellen, Empfänger der Ergebnisse, enthaltene Rechenlogik, Abhängigkeiten zu anderen Dateien, geschätzter Schaden bei Ausfall. | Owner |
| 2 | **Zielsystem bestimmen** nach der Entscheidungshilfe in Abschnitt 5. Ergebnis wird im Steckbrief festgehalten, auch wenn es "kein Zielsystem" lautet. | IT-Applikationen mit Owner |
| 3 | **Datenhaltung und Rechenlogik trennen.** In den gemeldeten Dateien liegen beide meist vermischt vor. Zuerst wird bestimmt, welche Daten künftig im Zielsystem geführt werden; erst danach, welche Berechnung dort abgebildet wird und welche entfällt. | IT-Applikationen |
| 4 | **Stammdatenbezug prüfen.** Material-, Lieferanten-, Kunden- und Projektnummern werden gegen die zentralen Stammdaten nach POL-IT-006 abgeglichen. Lokale Nummernkreise, Kurzbezeichnungen und Sammelpositionen werden vor der Überführung aufgelöst, nicht danach. | Owner mit IT-Applikationen |
| 5 | **Personenbezug prüfen.** Enthält die Datei personenbezogene Daten oder Kennzahlen, die einer Person zurechenbar sind, gilt das Verfahren nach BV-2023-01: Unterrichtung, Systembeschreibung mit Datenkatalog, gegebenenfalls Teilvereinbarung vor Produktivsetzung. Die Prüfung erfolgt gemeinsam mit der Datenschutzbeauftragten Sabine Kroll. Bei Projektkennzahlen ist zusätzlich BV-2025-01 zu beachten. | IT-Applikationen, Datenschutz |
| 6 | **Aufbau im Zielsystem.** Keine Nachbildung der Datei eins zu eins. Was das Zielsystem im Standard trägt, wird im Standard abgebildet. Was es nicht trägt, wird weggelassen, in eine klar abgegrenzte Auswertung verlagert oder bleibt bewusst ausserhalb - aber es wird nicht durch Zusatzentwicklung erzwungen. | IT-Applikationen |
| 7 | **Parallelbetrieb.** Höchstens zwei fachliche Zyklen, längstens acht Wochen. Abweichungen zwischen Datei und Zielsystem werden aufgezeichnet und geklärt. Ein Parallelbetrieb ohne Enddatum gilt als gescheiterte Überführung und ist als solche zu melden. | Owner |
| 8 | **Abnahme.** Der Owner bestätigt schriftlich, dass das Zielsystem den Zweck erfüllt. Die Abnahmekriterien werden vor Schritt 6 festgelegt, nicht danach. | Owner |
| 9 | **Stilllegung der Datei.** Die Datei wird schreibgeschützt, mit dem Vermerk "stillgelegt am TT.MM.JJJJ, überführt nach <Zielsystem>" versehen und im Bereichsordner belassen. Sie wird nicht gelöscht; der Lesezugriff bleibt 24 Monate bestehen. Der Eintrag im Verzeichnis wird auf "überführt" gesetzt. | Owner, IT-Applikationen |

## 5 Entscheidungshilfe Zielsystem

| Inhalt der Tabelle | Zielsystem |
|---|---|
| Material-, Lieferanten-, Preis-, Bestell- und Auftragsdaten, Kalkulationen mit Auftragsbezug | SAP S/4HANA |
| Beschaffungsvorgänge, Anfragen und Lieferantenkommunikation | SAP Ariba |
| Kunden, Angebote, Opportunities, Auftragseingangsprognosen | Microsoft Dynamics 365 |
| Konstruktionsdaten, Stücklisten, Zeichnungsstände, Dokumente mit Revisionsstand | Teamcenter |
| Reisekosten und Auslagen | SAP Concur |
| Auswertungen und Verdichtungen aus bereits zentral vorhandenen Daten | Power BI auf der zentralen Datenplattform |
| Projektkennzahlen und Statusdaten | Projekt-Dashboard, Regeln nach BV-2025-01 |
| Listen mit Dokumentcharakter, Checklisten, Protokolle, Übergaben | SharePoint mit Versionierung |
| Berechnungs- und Auslegungswerkzeuge mit fachlicher Logik | derzeit kein Zielsystem - Verbleib als Datei mit Owner und Versionskontrolle |

Die letzte Zeile ist kein Platzhalter. Ein erheblicher Teil der gemeldeten Dateien besteht aus
Angebotskonfiguratoren und Berechnungstools. Für sie existiert kein zentrales System, in das man sie
sinnvoll überführen könnte, und ein solches zu beschaffen ist mit dieser Anweisung nicht beabsichtigt.

Berührt eine Datei mehrere Zeilen, wird sie geteilt: die Daten gehen in das führende System, die
Auswertung in Power BI. Eine Datei, die man nicht teilen kann, ist meist zwei Anwendungen in einer.

## 6 Abbruchkriterien

Die Überführung wird nicht begonnen oder abgebrochen, wenn

- kein Zielsystem den Inhalt ohne Erweiterung des Systems trägt,
- der Prozess, den die Datei stützt, gerade selbst verändert wird - dann wird verschoben, nicht
  parallel umgebaut,
- die Datei von einer einzigen Person und seltener als vierteljährlich genutzt wird; hier genügt die
  Owner-Lösung,
- der Owner entfällt und der Bereich innerhalb von vier Wochen keinen Nachfolger benennt.

Ein Abbruch ist ein zulässiges Ergebnis. Er wird im Verzeichnis mit Begründung eingetragen, und die
Datei geht in den Zustand Owner und Versionskontrolle über.

## 7 Rollen

| Rolle | Verantwortung |
|---|---|
| Owner | fachliche Richtigkeit, Steckbrief, Mitarbeit, Abnahme, Stilllegung |
| Bereichsleitung | Zeitanteil des Owners, Entscheidung bei Abbruch, Benennung eines Nachfolgers |
| IT-Applikationen | Zielsystemvorschlag, technische Umsetzung, Schnittstellen, Einweisung des Owners |
| Informationssicherheit | Berechtigungen, sobald Zugriffe über Bereichsgrenzen hinweg entstehen |
| Datenschutz | Prüfung des Personenbezugs, Verfahren nach BV-2023-01 |
| Qualitätsmanagement | Lenkung dieser Anweisung nach POL-QM-001 |

## 8 Priorisierung und Kapazität

Die IT-Applikationen kann neben dem Regelbetrieb und den laufenden Vorhaben im zweiten Halbjahr 2025
sechs Überführungen begleiten. Bei rund 60 als geschäftskritisch eingestuften Dateien heisst das: die
grosse Mehrheit bleibt vorerst Datei. Das ist kein Rückstand, sondern der zweite zulässige
Zielzustand nach POL-IT-005.

Die Reihenfolge wird quartalsweise mit den Bereichen abgestimmt und nach drei Kriterien gebildet:
Zahl der abhängigen Prozesse, Schadenshöhe bei Ausfall, Abhängigkeit von einer einzelnen Person.
Das dritte Kriterium ist in der Erfassung deutlich häufiger aufgetreten als erwartet und wird
entsprechend gewichtet.

## 9 Nachweise und Aufbewahrung

Steckbrief, Abnahmebestätigung und der aktualisierte Verzeichniseintrag werden unter dem Vorgang
Excel Amnesty abgelegt und für sechs Jahre aufbewahrt. Die stillgelegte Datei verbleibt zusätzlich
im Bereichsordner.

## 10 Offene Punkte

Der Zeitanteil des Owners ist unternehmensweit nicht geregelt. Der Gesamtbetriebsrat hat im Februar
2025 darauf hingewiesen, dass die Owner-Rolle nicht ohne Zeitbudget vergeben werden sollte; die
Klärung liegt bei den Bereichsleitungen und der Personalabteilung. Bis dahin gilt Abschnitt 3
Punkt 3: ohne ausdrückliche Zusage der Bereichsleitung wird nicht begonnen.

Für Angebotskonfiguratoren und Berechnungswerkzeuge ist bisher keine Lösung vorgesehen. Ob dafür ein
eigenes Vorgehen entwickelt wird, ist offen.

---

**Hinweis der IT-Applikationen.** Eine Überführung ist kein IT-Projekt. Die IT stellt System,
Schnittstelle und Betreuung; die Fachlichkeit bleibt im Bereich. Wird diese Trennung aufgeweicht,
entsteht aus einer Schattenanwendung im Fachbereich eine Schattenanwendung in der IT - mit dem
Unterschied, dass sie dann niemandem mehr gehört.

Rückfragen über eine Serviceanfrage an die IT-Applikationen mit dem Betreff "Schattenanwendung".
