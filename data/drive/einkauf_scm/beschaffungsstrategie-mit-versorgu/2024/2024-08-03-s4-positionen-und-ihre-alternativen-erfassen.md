---
doc_id: LTT-20240803-SCM-01
titel: "Risikoregister: S4-Positionen und ihre Alternativen erfassen"
dokumenttyp: Risikoregister
datum: 2024-08-03
verfasser: Petra Ehlers
rolle: Leiterin strategischer Einkauf
organisationseinheit: SCM
empfaenger: ["-"]
projekt: "-"
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [bereichsintern, management]
ablageort: einkauf_scm
---

# Risikoregister Beschaffung - Versorgungsklasse S4

Lahnberg Thermotechnik GmbH & Co. KG, Supply Chain & Operations Planning, Strategischer Einkauf

| | |
|---|---|
| Stand | 03.08.2024 |
| Version | 0.9, Erstaufnahme |
| Bearbeitung | P. Ehlers, Leiterin strategischer Einkauf |
| Grundlage | SOP Versorgungsklassen S1 bis S4, freigegeben 15.07.2024, gültig ab 01.08.2024 |
| Geltungsbereich | Warengruppen mit Rahmenvertrags- oder Serienbezug, Standorte Kassel und Eisenach |
| Fortschreibung | monatlich, nächster Stand 30.09.2024 |
| Status | Vorbereitung des in der SOP vorgeschriebenen Management-Reviews; Termin noch nicht angesetzt |

---

## 1. Zweck und Abgrenzung

Die SOP schreibt für jede Position der Klasse S4 ein Management-Review sowie fünf Instrumente vor:
Mindestbestand, Second-Source-Roadmap, technische Substitutionsanalyse, Business-Continuity-Plan und
einen jährlichen Financial-Health-Check. Dieses Register ist die Arbeitsgrundlage dafür. Es erfasst,
welche Positionen betroffen sind, welche Alternative es tatsächlich gibt und was diese Alternative
technisch kosten würde. Es entscheidet nichts.

Klassifiziert wurde zwischen Mai und Juli 2024 auf Basis der Bestellhistorie 2021 bis 2023 und der
Rahmenvertragsübersicht. Von 486 bewerteten Positionen entfallen 21 auf S4. In dieser Fassung sind
neun davon aufgenommen; die übrigen zwölf betreffen überwiegend Eisenach (Verdichterbauteile,
Prüfstandstechnik, Gießereibedarf) und sind noch nicht bewertet.

Zur Erinnerung an die Klassendefinition: S4 bedeutet, dass ein Ausfall der Quelle nicht innerhalb von
zwölf Wochen kompensiert werden kann und unmittelbar auf Auslieferungs- oder Inbetriebnahmetermine
durchschlägt. S3 bedeutet, dass eine Kompensation möglich, aber mit Mehrkosten oder Terminverschiebung
verbunden ist.

Nicht Gegenstand dieses Registers sind Bauleistungen, Fremdmontage, Ingenieurdienstleistungen und
Handelsware ohne Anlagenbezug.

---

## 2. Erfasste S4-Positionen

Bewertung: Eintrittswahrscheinlichkeit E und Auswirkung A jeweils 1 bis 5, Risikozahl RZ = E mal A.
Ab RZ 15 ist die Position im Review gesondert aufzurufen.

| ID | Warengruppe / Position | Quelle | Risikoursache | E | A | RZ |
|---|---|---|---|---:|---:|---:|
| SCM-R-2024-01 | Frequenzumrichter ab 250 kW, Verdichter- und Pumpenantriebe | Vectron Drive Systems GmbH (SUP-014) | seit 2021 als Ausnahme vom Dual-Source-Grundsatz geführt; Baltic Power Electronics OÜ (SUP-015) und Drivetec Nord AB (SUP-016) sind nur bis 160 kW freigegeben | 3 | 5 | 15 |
| SCM-R-2024-02 | Steuerungshardware und Bausteinbibliothek der Anlagenautomatisierung | Auconta Steuerungstechnik GmbH (SUP-017) | die gesamte Applikationssoftware setzt auf den Bibliotheken des Herstellers auf; Litec Automation B.V. (SUP-018) arbeitet mit abweichendem Bausteinkonzept | 2 | 5 | 10 |
| SCM-R-2024-03 | Schaltschränke, komplexe Konfigurationen für Quartiers- und Großanlagen | NordControl Schaltanlagen GmbH (SUP-001), ElektroPlan Süd GmbH (SUP-002) | zwei Lieferanten, aber kein gemeinsamer Standard: unterschiedliche Klemmensysteme, Dokumentationsstandards, Prüfprotokolle und Bibliotheken; kurzfristige Umverteilung nur mit Engineering-Aufwand | 3 | 4 | 12 |
| SCM-R-2024-04 | Plattenwärmetauscher, kundenspezifisch, Hochtemperaturbereich | Calorex Spezialwärmetauscher GmbH (SUP-009) | Auslegung und Druckgerätenachweise sind fabrikatsgebunden; Thermoplan Wärmetechnik GmbH (SUP-006) und Nordisk Varmeteknik A/S (SUP-007) decken nur Standardbaureihen ab | 2 | 5 | 10 |
| SCM-R-2024-05 | Leistungsschalter und Schutzorgane | Kontakta Schaltgeräte GmbH (SUP-025) | Allokationslage aus 2022 ist nicht strukturell behoben; ein zweites Fabrikat erfordert Änderungen an E-Planung und Makrobibliothek | 3 | 3 | 9 |
| SCM-R-2024-06 | Speziallager für Schraubenverdichter, Eisenach | kein Rahmenvertrag, Bezug über wechselnde Handelsstufe | Einzelquelle ohne vertragliche Bindung; Lieferzeiten 2022 zeitweise über 40 Wochen; keine Zusage zu Vorhaltung oder Vorlauf | 3 | 5 | 15 |
| SCM-R-2024-07 | Druck- und Temperatursensorik mit Ex-Zulassung | Sensoria Instruments AG (SUP-024), teilweise Messtechnik Ostwestfalen GmbH (SUP-023) | die zweite Quelle ist nur für Ausführungen ohne Ex-Zulassung freigegeben; die Zulassung selbst ist fabrikatsgebunden | 2 | 4 | 8 |
| SCM-R-2024-08 | Gussteile Verdichtergehäuse | eigene Gießerei Eisenach, Werragrund Guss GmbH (SUP-005), Moravia Precision Castings a.s. (SUP-004) | Modellgebundenheit: jede Verlagerung erfordert neue Modelle und erneute Erstmusterprüfung; nach dem Stopp des weiteren Guss-Outsourcings im Januar 2024 liegt der Schwerpunkt wieder intern | 2 | 4 | 8 |
| SCM-R-2024-09 | Regelarmaturen Hochtemperatur | Armaturenwerk Vogtland GmbH (SUP-021) | Valvo Nord A/S (SUP-022) ist nur bis 130 Grad Celsius Mediumstemperatur qualifiziert, darüber besteht kein freigegebenes Fabrikat | 2 | 4 | 8 |

Anmerkung zu SCM-R-2024-06: Für diese Position existiert kein Lieferantenstammsatz mit
Rahmenvertragsbezug. Die Beschaffung läuft seit Jahren über wechselnde Handelspartner, weil das
Volumen früher als unkritisch galt. Das ist der einzige Fall im Register, in dem nicht einmal die
Erstquelle vertraglich gebunden ist.

---

## 3. Erfüllungsstand der fünf S4-Instrumente

| ID | Mindestbestand | Second-Source-Roadmap | Substitutionsanalyse | Business-Continuity-Plan | Financial-Health-Check |
|---|---|---|---|---|---|
| 01 | vorhanden, 14 Wochen ab 01.08. | offen | offen | offen | vorhanden, Abschluss 2023 |
| 02 | vorhanden, 10 Wochen | nicht sinnvoll, siehe 4.2 | offen | offen | vorhanden, Abschluss 2023 |
| 03 | entfällt, Auftragsfertigung | in Arbeit, dritte Quelle seit 01.08. | offen | in Arbeit | vorhanden für SUP-001 und SUP-002 |
| 04 | entfällt, Auftragsfertigung | nicht sinnvoll, siehe 4.3 | offen | offen | offen |
| 05 | vorhanden, 8 Wochen | in Arbeit | in Arbeit | offen | offen |
| 06 | offen | offen | offen | offen | offen, Lieferant nicht identifiziert |
| 07 | vorhanden, 6 Wochen | in Arbeit | offen | offen | vorhanden, Abschluss 2023 |
| 08 | entfällt, Modellfertigung | vorhanden | vorhanden | in Arbeit | vorhanden für SUP-004 und SUP-005 |
| 09 | vorhanden, 12 Wochen | offen | offen | offen | offen |

Von den 45 nach SOP geforderten Nachweisen liegen elf vor, sechs sind in Arbeit, drei sind mit
Begründung als nicht zielführend gekennzeichnet, 25 sind offen.

---

## 4. Positionen, bei denen eine zweite Quelle konstruktive Änderungen auslöst

Die SOP behandelt die Second-Source-Roadmap als Beschaffungsaufgabe. Bei vier der neun Positionen
trifft das nicht zu. Dort ist die zweite Quelle keine Vertragsfrage, sondern eine Änderung an der
Baugruppe mit anschließendem Nachweisaufwand. Die folgenden Schätzungen stammen aus Rücksprachen mit
Konstruktion und Elektrotechnik und sind grob.

### 4.1 Frequenzumrichter ab 250 kW (SCM-R-2024-01)

Die Regelparametrierung, die Schaltschrankauslegung und der EMV-Nachweis auf Anlagenebene sind auf das
eingesetzte Fabrikat abgestimmt. Ein zweites Fabrikat bedeutet geänderte Leistungsteilanordnung,
geänderte Kühlkonzeption im Schrank, einen erneuten EMV-Nachweis je Baugröße und Prüfstandszeit in
Eisenach. Geschätzt 150 bis 200 Konstruktionsstunden je Baugröße zuzüglich Prüfstand. Bei drei
relevanten Baugrößen ist das kein Nebenbei-Vorgang, sondern ein Entwicklungsvorhaben.

Der Bestand ist zum 01.08. auf 14 Wochen angehoben worden. Das ist die Maßnahme, die ich ohne
Konstruktionsressourcen ergreifen kann.

### 4.2 Steuerungshardware und Bausteinbibliothek (SCM-R-2024-02)

Hier halte ich eine Second-Source-Roadmap für nicht zielführend und habe sie entsprechend
gekennzeichnet. Der Wechsel des Steuerungsfabrikats bedeutet die Portierung der gesamten
Applikationssoftware einschließlich der über Jahre gewachsenen Bausteinbibliothek, dazu neue
Schulung der Inbetriebnehmer und in einem Teil der Projekte eine erneute Kundenabnahme. Das ist ein
Vorhaben in der Größenordnung eines Plattformprojekts und keine Beschaffungsmaßnahme.

Sinnvoll und in meinem Zugriff sind stattdessen: vertragliche Hinterlegung der Bibliotheken und der
Quellstände, eine Zusage zu Ersatzteilverfügbarkeit über die Anlagenlaufzeit, und der jährliche
Financial-Health-Check, weil bei diesem Lieferanten nicht die Lieferfähigkeit das Risiko ist, sondern
sein Fortbestand. Ich werde das in der Vertragsverlängerung aufrufen.

### 4.3 Plattenwärmetauscher Hochtemperatur (SCM-R-2024-04)

Die Geräte werden je Projekt ausgelegt; die Nachweise nach Druckgeräterichtlinie sind fabrikats- und
auslegungsgebunden. Ein Wechsel innerhalb eines laufenden Projekts ist ausgeschlossen, weil die
Kundenfreigabe auf dem konkreten Datenblatt beruht. Bei mehreren Bestandskunden, unter anderem im
Fernwärmebereich, ist der Lieferant zudem in der Anlagendokumentation benannt. Eine zweite Quelle ließe
sich nur für künftige Projekte aufbauen, und auch dann erst nach Qualifizierung über mindestens eine
Referenzanlage.

Ich schlage vor, diese Position nicht über eine Roadmap zu führen, sondern über eine Erweiterung der
Rahmenvereinbarung: Kapazitätsvorhalt, Vorlaufzeitzusage, Informationspflicht bei Änderungen an
Produktionsstandorten.

### 4.4 Regelarmaturen Hochtemperatur (SCM-R-2024-09)

Der zweite Lieferant ist vorhanden, aber nur bis 130 Grad Celsius qualifiziert. Die Erweiterung der
Freigabe ist der günstigste Fall im Register: eine Baumusterprüfung, Anpassung der Werkstoffpaarung
und eine Anpassung der Ausschreibungsspezifikation. Ich rechne mit deutlich unter 50
Konstruktionsstunden und einer Freigabe bis Jahresende, sofern die Prüfung eingeplant wird.

### 4.5 Nachrichtlich: Leistungsschalter (SCM-R-2024-05)

Kein konstruktiver Eingriff an der Anlage, aber eine Änderung an der Makrobibliothek der E-Planung und
an den Schaltplanvorlagen. Aufwand in der Elektrotechnik, nicht in der Mechanik. Diese Position ist
zügig lösbar, wenn die Bibliothekspflege priorisiert wird.

---

## 5. Bewertung aus Sicht des strategischen Einkaufs

Die Klassifizierung leistet etwas, das der Dual-Source-Grundsatz von 2021 nicht geleistet hat. Damals
wurden genau die kritischsten Komponenten als Ausnahme geführt: kundenspezifische Wärmetauscher,
proprietäre Steuerungshardware, bestimmte Frequenzumrichter, komplexe Schaltschrankkonfigurationen.
Die Ausnahme stand in einer Fußnote und wurde nie wieder aufgerufen. Jetzt sind dieselben Positionen
eine eigene Klasse mit Berichtspflicht. Das ist der eigentliche Fortschritt und der Grund, warum ich
das Register führe.

Drei Punkte muss das Management-Review aus meiner Sicht klären.

**Erstens die Menge.** Neun Positionen mal fünf Instrumente sind 45 Nachweise, von denen elf
vorliegen. Für die zwölf noch nicht erfassten Eisenacher Positionen kommen weitere 60 hinzu. Ohne
Priorisierung entsteht ein Register, das vollständig aussieht und leer ist. Ich schlage vor, für 2024
die beiden Positionen mit RZ 15 vollständig zu bearbeiten und für die übrigen nur Mindestbestand und
Business-Continuity-Plan zu verlangen.

**Zweitens die Zuordnung des Aufwands.** Bei vier Positionen ist die zweite Quelle eine
Konstruktionsentscheidung. Der Einkauf kann den Lieferanten wechseln, nicht die Baugruppe. Wenn die
Second-Source-Roadmap als Beschaffungsleistung geführt wird, ohne dass in Konstruktion und
Elektrotechnik Stunden dafür hinterlegt sind, bleibt die Spalte leer und die Verantwortung liegt
trotzdem bei mir. Ich bitte darum, die technische Substitutionsanalyse mit benannten Bearbeitern in
der Kapazitätsplanung zu hinterlegen. Andernfalls beantrage ich, sie aus dem Instrumentenkasten zu
streichen, statt sie zu behaupten.

**Drittens ein Widerspruch in der Regellage.** Die SOP verlangt für S4 einen Mindestbestand. Die
Richtlinie zu Sicherheitsbeständen ist 2021 zugunsten des Working Capital reduziert worden und gilt
unverändert. Ich habe die Bestände für die Positionen 01, 02, 05, 07 und 09 zum 01.08. angehoben und
halte das für richtig, aber ich tue es gegen eine geltende Richtlinie. Das gehört entschieden und
nicht ausgesessen; die Bestandswirkung ist im Controlling anzumelden.

Vorschlagen möchte ich außerdem eine Unterteilung der Klasse. S4-a für Positionen, bei denen eine
zweite Quelle technisch und wirtschaftlich erreichbar ist; dort gilt der volle Instrumentenkasten.
S4-b für strukturelle Einzelquellen, bei denen die zweite Quelle teurer wäre als das Risiko, das sie
beseitigt; dort treten an die Stelle der Roadmap vertragliche Instrumente: Vorhaltevereinbarung,
Vorlaufzeitzusage, Informations- und Fortführungspflichten, Hinterlegung von Modellen, Bibliotheken
und Fertigungsunterlagen, dazu der Financial-Health-Check. Nach heutigem Stand fielen 02, 04 und 06 in
S4-b.

---

## 6. Offene Punkte und Bewertungslücken

| Nr | Punkt | Wirkung auf das Register |
|---|---|---|
| 1 | Zwölf S4-Positionen aus Eisenach sind nicht erfasst | Register ist nicht vollständig; Version bleibt 0.9 |
| 2 | Für SCM-R-2024-06 ist der Hersteller nicht identifiziert und kein Stammsatz angelegt | weder Financial-Health-Check noch Rahmenvertrag möglich |
| 3 | Der Financial-Health-Check ist methodisch nicht definiert: Datenquelle, Kennzahlen, Schwellenwert und Folge einer Auffälligkeit fehlen in der SOP | die Spalte ist derzeit nicht prüffähig, "vorhanden" heißt bisher nur, dass eine Bonitätsauskunft vorliegt |
| 4 | Lieferantenstammdaten in SAP Ariba sind für Guss und Sensorik unvollständig | Bewertung stützt sich insoweit auf die Bestellhistorie aus dem ERP |
| 5 | Der am 01.08.2024 geschlossene Rahmenvertrag mit RheinMain Automation Systems ist noch nicht risikomindernd berücksichtigt | SCM-R-2024-03 wird erst nach der ersten abgeschlossenen Projektabwicklung neu bewertet |
| 6 | Nach der teilweisen Rücknahme der Zentralisierung zum 01.08.2024 ist offen, wer die S4-Positionen der Business Unit Compressor Systems führt | Zuständigkeit für Punkt 1 ungeklärt |
| 7 | Das Management-Review nach SOP hat nicht stattgefunden | ohne Beschluss keine Freigabe der Version 1.0 |

Zu Punkt 5: Der Rahmenvertrag ist geschlossen, weil die Kapazitätslage im Schaltschrankbau seit 2022
eng ist und zwei Quellen sich bei Quartiersprojekten mehrfach als knapp erwiesen haben. Er löst das
Problem aus Position 03 aber nicht automatisch, weil auch der dritte Lieferant seine eigenen
Klemmensysteme und Dokumentationsstandards mitbringt. Wir hatten 2022 zwei Lieferanten und keinen
Standard; wir haben jetzt drei Lieferanten und keinen Standard. Die Kapazität steigt, der
Engineering-Aufwand steigt mit.

---

## 7. Nächste Schritte

| Nr | Maßnahme | vorgeschlagene Zuständigkeit | Termin |
|---|---|---|---|
| 1 | Erfassung der zwölf Eisenacher S4-Positionen, Zuständigkeit vorab klären | strategischer Einkauf mit Standort Eisenach | 30.09.2024 |
| 2 | Management-Review ansetzen, Vorlage dieses Registers in Version 0.9 | Leitung Supply Chain & Operations Planning | offen |
| 3 | Konkretisierung des Financial-Health-Checks als Anlage zur SOP | strategischer Einkauf, Abstimmung mit Controlling | 30.09.2024 |
| 4 | Hinterlegung von Stunden für die technische Substitutionsanalyse zu 01, 04, 09 | Konstruktion und Elektrotechnik | mit der Kapazitätsplanung Q4 |
| 5 | Erweiterung der Freigabe Regelarmaturen über 130 Grad Celsius | Konstruktion, Beschaffung begleitend | 31.12.2024 |
| 6 | Identifikation des Lagerherstellers, Rahmenvertrag und Konsignationslösung prüfen | strategischer Einkauf | 30.11.2024 |
| 7 | Anmeldung der Bestandswirkung aus den angehobenen Mindestbeständen | strategischer Einkauf an Controlling | 31.08.2024 |
| 8 | Qualifizierungsplan für den dritten Schaltschranklieferanten, einschließlich Dokumentationsstandard | strategischer Einkauf mit Elektrotechnik | 31.10.2024 |

---

## 8. Fortschreibung

Das Register wird monatlich zum Monatsletzten fortgeschrieben und im Rahmen des S&OP-Zyklus
berichtet. Eine Herabstufung von S4 auf S3 erfolgt erst nach dokumentierter Qualifizierung der
Alternative, nicht bereits mit Abschluss eines Vertrages. Änderungen an der Klassifizierung werden mit
Datum und Grund in der jeweiligen Zeile vermerkt.

Ablage: Einkauf, Warengruppenstrategie, Versorgungsklassen. Die zugehörigen Lieferantenunterlagen
liegen bei den jeweiligen Rahmenverträgen.

P. Ehlers, 03.08.2024
