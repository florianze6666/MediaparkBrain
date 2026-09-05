---
doc_id: LTT-20230124-PROG-00
titel: "Projektauftrag: Bereinigung der Materialstämme beauftragen"
dokumenttyp: Projektauftrag
datum: 2023-01-24
verfasser: Oliver Bensch
rolle: Teilprojektleiter ERP und Stammdaten
organisationseinheit: Programm
empfaenger: ["-"]
projekt: IP-2023-02
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [projektintern]
ablageort: projektlaufwerk
---

Lahnberg Thermotechnik GmbH & Co. KG
Programm ONE LTT, Teilprojekt ERP und Stammdaten

# Projektauftrag

| | |
|---|---|
| Auftragsnummer | IP-2023-02 |
| Projekt | PRJ-MDM-2023, Bereinigung und Harmonisierung der Materialstämme |
| Fassung | 1.0 vom 24.01.2023 |
| Auftraggeber | Dr. Simone Hartwig, Programmleiterin ONE LTT |
| Auftragnehmer | Oliver Bensch, Teilprojektleiter ERP und Stammdaten |
| Verteiler | Programmleitung; IT-Applikationen (A. Faber); Konstruktion mechanisch (M. Gehrke); Elektrotechnik und Automatisierung (R. Wiesner); strategischer Einkauf (P. Ehlers); Arbeitsvorbereitung (N. Feld); Standortleitung Eisenach (A. Puhl); Compressor Systems (Dr. F. Steinbach); Lifecycle & Service (M. Aurich); Controlling (D. Anselm); Qualitätsmanagement (B. Hoffmann) |
| Ablage | Projektlaufwerk, PRJ-MDM-2023, Ordner 01_Auftrag, gelenkt nach POL-QM-001 v2.0 |

## 1. Anlass und Ausgangslage

Das Programm ONE LTT ist im Januar operativ angelaufen. Für das Zielbild eines konzernweit
einheitlichen ERP gilt der Leitsatz "Adopt before adapt": die Standardsoftware soll möglichst
unverändert genutzt werden. Dieser Leitsatz verlagert die Last vollständig auf die Daten. Wer den
Standard nicht anpasst, muss die Stammdaten so bereitstellen, wie der Standard sie erwartet.

Seit der Übernahme des Eisenacher Werks 2018 gilt die Reihenfolge "erst Geschäft integrieren, dann
IT". Die beiden ERP-Landschaften in Kassel und Eisenach sind seither unverändert nebeneinander
betrieben worden, und die Materialstämme sind fünf Jahre lang getrennt weitergewachsen. Es gibt
keinen gemeinsamen Schlüssel, keine gemeinsame Benennungslogik und keine gemeinsame Warengruppen-
struktur.

Die Erstauswertung beider Systeme aus Kalenderwoche 2 ergibt rund 182.000 aktive Materialnummern,
davon etwa 117.000 in Kassel und etwa 65.000 in Eisenach. Auffällig sind vier Befunde:

- Dubletten innerhalb eines Standorts und zwischen den Standorten, teils mit abweichenden
  Mengeneinheiten für dasselbe Teil.
- Projektspezifische Einmalteile, die als vollwertige Materialstämme angelegt wurden und nach
  Projektende nie wieder verwendet worden sind. Sie machen den größten Einzelblock aus.
- Mehrere parallel gewachsene Benennungslogiken. Sprechende Nummernkreise aus der Zeit vor 2014
  stehen neben Kurztexten ohne feste Reihenfolge der Merkmale.
- Altmaterial ohne Sperrstatus. Nicht mehr beschaffbare oder abgekündigte Teile sind im System
  weiterhin dispositiv verfügbar.

Ohne Bereinigung überträgt jede Migration diesen Zustand in das Zielsystem. Der Aufwand, ihn dort zu
korrigieren, ist deutlich höher als heute, weil dann zwei Systemwelten gleichzeitig betroffen sind.

## 2. Zielsetzung

Das Projekt schafft einen bereinigten, konzernweit einheitlich strukturierten Materialstammbestand
als Migrationsbasis für ONE LTT. Es leistet dazu drei Dinge:

1. ein verbindliches Regelwerk für Benennung, Nummernkreise, Warengruppen, Mengeneinheiten und
   Sperrlogik,
2. die maschinelle Analyse beider Bestände gegen dieses Regelwerk,
3. die fachliche Entscheidung über jeden aktiven Materialstamm: übernehmen, zusammenführen, sperren
   oder nicht übernehmen.

## 3. Zielgrößen

| Nr | Zielgröße | Wert |
|---|---|---|
| Z1 | Reduktion der aktiven Materialstämme | 40 Prozent, Zielbestand rund 109.000 |
| Z2 | Anteil entschiedener Materialstämme zum Einfrieren | 100 Prozent |
| Z3 | Materialstämme mit regelkonformer Benennung und Klassifizierung im übernommenen Bestand | 100 Prozent |
| Z4 | Materialstämme ohne zugeordneten Datenverantwortlichen | 0 |

Zu Z1 ist eine Anmerkung nötig. Die 40 Prozent stammen aus dem Zielbild des Programms, nicht aus
einer Analyse des Bestands. Ob sie erreichbar sind, lässt sich erst nach Abschluss des
Dublettenabgleichs beurteilen. Ich schlage vor, die Größe nach Meilenstein M2 einmalig zu überprüfen
und gegebenenfalls anzupassen, statt sie das Jahr über als unerreichbare Vorgabe mitzuführen.

## 4. Abgrenzung

Nicht Gegenstand dieses Auftrags sind:

- Kunden- und Lieferantenstammdaten. Sie werden gesondert beauftragt.
- Stücklisten und Arbeitspläne. Sie folgen der Materialbereinigung, nicht umgekehrt.
- Die Klassifizierung des Produktportfolios und die Plattformstruktur nach POL-ENG-002.
- Anpassungen der Standardsoftware an bestehende Benennungslogiken. Der Leitsatz des Programms
  schließt das aus.
- Bereinigung der lokalen Excel- und Access-Bestände in den Fachbereichen. Diese Bestände werden
  erhoben, aber in diesem Auftrag nicht überführt.

## 5. Leistungsumfang

| AP | Inhalt | Verantwortung |
|---|---|---|
| AP1 | Regelwerk Materialstamm: Benennungssyntax, Merkmalsreihenfolge, Nummernkreise, Warengruppen, Mengeneinheiten, Sperr- und Auslaufstatus | Teilprojekt, Abstimmung mit Konstruktion, Einkauf, AV |
| AP2 | Extraktion beider Bestände, Vereinheitlichung der Auswertungsformate, Aufbau der Arbeitsdatenbasis | IT-Applikationen |
| AP3 | Dublettenanalyse innerhalb und zwischen den Standorten, Kandidatenlisten je Warengruppe | Teilprojekt |
| AP4 | Fachliche Entscheidung je Materialstamm anhand der Kandidatenlisten | Datenverantwortliche der Fachbereiche |
| AP5 | Umsetzung im Quellsystem: Zusammenführung, Sperrung, Statuspflege | IT-Applikationen und Fachbereiche |
| AP6 | Einfrieren des bereinigten Bestands, Freigabe als Migrationsbasis, Übergabe an die Migrationsvorbereitung | Teilprojekt |

Die Dublettenanalyse liefert Kandidaten, keine Ergebnisse. Ein automatischer Abgleich über Kurztext,
Sachmerkmale und Lieferantenteilenummer erkennt einen Teil der Fälle; die Entscheidung, ob zwei
Nummern dasselbe Teil bezeichnen, kann nur der Fachbereich treffen. Dieser Punkt ist für die Planung
entscheidend, weil er den Aufwand aus der IT in die Fachbereiche verlagert.

## 6. Termine

| Meilenstein | Inhalt | Termin |
|---|---|---|
| M1 | Regelwerk verabschiedet und als gelenktes Dokument in Kraft | 31.03.2023 |
| M2 | Dublettenanalyse abgeschlossen, Kandidatenlisten je Warengruppe verteilt | 31.05.2023 |
| M3 | Entscheidung je aktivem Materialstamm getroffen | 30.09.2023 |
| M4 | Bereinigter Bestand eingefroren und als Migrationsbasis freigegeben | 30.11.2023 |

M3 ist der kritische Meilenstein. Er hängt nicht am Teilprojekt, sondern an der Verfügbarkeit der
Fachbereiche.

## 7. Organisation und Mitwirkung

Die Fachbereiche benennen bis zum 15.02.2023 je Warengruppe einen Datenverantwortlichen mit
Entscheidungsbefugnis und benennen dazu die zugesagte Kapazität in Personentagen. Vorgesehene
Ansprechpartner:

| Bereich | Ansprechpartner | Warengruppen |
|---|---|---|
| Konstruktion mechanisch | M. Gehrke | Rohrleitungsbau, Wärmeübertrager, Skidbau, Normteile |
| Elektrotechnik und Automatisierung | R. Wiesner | Schaltschrankkomponenten, Sensorik, Antriebe |
| Strategischer Einkauf | P. Ehlers | Kaufteile, Handelsware, C-Teile |
| Arbeitsvorbereitung | N. Feld | Eigenfertigungsteile, Halbzeuge |
| Compressor Systems, Eisenach | Dr. F. Steinbach | Verdichterkomponenten, mechanische Bearbeitung, Guss |
| Lifecycle & Service | M. Aurich | Ersatz- und Verschleißteile |

Die Zuordnung der Eisenacher Warengruppen wird mit der Standortleitung abgestimmt. Der Bestand aus
Eisenach ist kleiner, aber schlechter dokumentiert; ich rechne dort mit einem höheren Aufwand je
Materialstamm.

Die Bereinigung wird in den Fachbereichen bislang als IT-Thema wahrgenommen. Sie ist keines. Die IT
liefert Auswertungen, Werkzeuge und die technische Umsetzung; die Entscheidung, welches Teil bleibt,
trifft ausschließlich der Fachbereich. Dieser Punkt gehört in die Kick-off-Kommunikation.

## 8. Aufwand und Budget

| Position | Aufwand |
|---|---|
| Teilprojekt ERP und Stammdaten | 2 Vollzeitäquivalente, ganzjährig |
| IT-Applikationen | 120 Personentage |
| Fachbereiche gesamt, Schwerpunkt Q2 und Q3 | rund 480 Personentage |
| Externe Unterstützung Analyse und Werkzeuge | 90 Beratertage |

Die Kosten sind im Programmbudget von ONE LTT enthalten. Ein eigener Investitionsantrag nach
POL-FIN-002 ist nicht erforderlich, da keine gesonderte Investition über der dortigen Schwelle
ausgelöst wird. Die Genehmigung erfolgt innerhalb der Programmvollmacht nach POL-FIN-001 v2.0.

Der Aufwand der Fachbereiche ist nicht budgetiert, sondern Arbeitszeit. Er trifft dieselben
Personen, die derzeit die laufenden Kundenprojekte tragen.

## 9. Risiken

| Nr | Risiko | Bewertung | Maßnahme |
|---|---|---|---|
| R1 | Die Fachbereiche stellen die zugesagte Kapazität nicht bereit. Das Haus arbeitet an mehr als 80 größeren Kundenprojekten parallel, Konstruktion und Automatisierung sind der Engpass | hoch | verbindliche Kapazitätszusage bis 15.02.2023, monatliche Nachverfolgung je Warengruppe |
| R2 | Historische Einmalteile haben keinen Verantwortlichen mehr, die Entscheidung bleibt liegen | hoch | Vorabregel im Regelwerk: Teile ohne Bewegung seit mehr als fünf Jahren und ohne Serviceverwendung werden gesperrt, sofern kein Widerspruch bis Fristende erfolgt |
| R3 | Ersatzteilversorgung wird durch Sperrungen beeinträchtigt | mittel | Lifecycle & Service prüft jede Sperrliste vor Umsetzung, Servicedisposition wird einbezogen |
| R4 | Der automatische Abgleich erkennt Dubletten zwischen Kassel und Eisenach nur unvollständig, weil kein gemeinsamer Schlüssel existiert | mittel | Abgleich über Lieferantenteilenummer als zusätzliches Merkmal, stichprobenhafte manuelle Gegenprüfung je Warengruppe |
| R5 | Die Zielgröße von 40 Prozent ist analytisch nicht unterlegt | mittel | Überprüfung nach M2, Entscheidung durch die Programmleitung |
| R6 | Bereinigte Stände laufen wieder auseinander, weil weiterhin ohne Regel angelegt wird | mittel | Anlageregel und Vier-Augen-Prüfung für Neuanlagen ab Inkrafttreten des Regelwerks |

## 10. Berichtswesen und Eskalation

Monatlicher Statusbericht nach POL-PM-001 v1.1 an die Programmleitung. Fortschrittskennzahl ist der
Anteil entschiedener Materialstämme je Warengruppe; die Auswertung wird über den neuen
BI-Berichtsdienst bereitgestellt, sobald dieser im Programm verfügbar ist, bis dahin als
Tabellenauswertung. Eskalationsweg: Teilprojektleitung, Programmleitung, Geschäftsführung.

## 11. Entscheidungsbedarf

Mit diesem Auftrag bitte ich um:

1. Freigabe von PRJ-MDM-2023 im beschriebenen Umfang und mit den Meilensteinen M1 bis M4,
2. Aufforderung der Fachbereiche zur Benennung der Datenverantwortlichen und zur verbindlichen
   Kapazitätszusage bis zum 15.02.2023,
3. Bestätigung, dass die Vorabregel zu bewegungslosen Altmaterialien (R2) angewendet werden darf,
4. Zustimmung zur Überprüfung der Zielgröße Z1 nach Meilenstein M2.

Ohne Punkt 2 ist der Termin M3 nach meiner Einschätzung nicht zu halten. Alles andere lässt sich im
Teilprojekt lösen.

## Freigabe

| Rolle | Name | Datum | Unterschrift |
|---|---|---|---|
| Auftragnehmer | Oliver Bensch | 24.01.2023 | |
| Auftraggeber | Dr. Simone Hartwig | | |
| Kenntnisnahme IT | Karin Löbner | | |
