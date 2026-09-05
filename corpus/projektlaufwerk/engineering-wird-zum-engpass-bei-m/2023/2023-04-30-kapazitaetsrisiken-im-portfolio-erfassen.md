---
doc_id: LTT-20230430-PMO-01
titel: "Risikoregister: Kapazitätsrisiken im Portfolio erfassen"
dokumenttyp: Risikoregister
datum: 2023-04-30
verfasser: Gerd Sattler
rolle: Leiter PMO
organisationseinheit: PMO
empfaenger: ["-"]
projekt: "-"
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit, projektintern]
ablageort: projektlaufwerk
---

# Risikoregister: Kapazitätsrisiken im Portfolio erfassen

**Register-Nr.** PMO-RR-PF-2023 - **Fassung** 1.0 - **Stand** 30.04.2023
**Geführt von** PMO, G. Sattler
**Geltungsbereich** Projektportfolio LTT gesamt, Kunden- und Transformationsprojekte, beide Standorte
**Grundlage** POL-PM-001 v1.1; POL-PM-002 v1.0 Projektampel und Eskalationsstufen, gültig ab 01.04.2023
**Datenbasis** Meldungen der Business Units zum 14.04.2023, Monatsreviews März und April, Auswertung der Engineering-Auslastung vom 16.04.2023
**Verteiler** Geschäftsführung, Leitungen der Business Units, Engineering (Central), Programmleitung ONE LTT
**Fortschreibung** monatlich zum Monatsreview, nächste Fassung 31.05.2023

## 1 Warum dieses Register geführt wird

Kapazitätsrisiken werden bei LTT bisher projektbezogen geführt. Jedes Projektregister weist eine
angespannte Personallage aus, jedes begründet damit eine Verschiebung von wenigen Wochen, und jede
dieser Verschiebungen ist für sich genommen vertretbar. Portfolioweit ergibt sich daraus ein anderes
Bild, und dieses Bild steht bisher nirgends.

Das PMO führt deshalb ab April ein portfolioweites Register ausschließlich für Kapazitätsrisiken. Es
bewertet keine einzelnen Projekte, sondern die gemeinsame Ressource, aus der alle bedient werden. Die
Bewertung folgt derselben Skala wie die neue Projektampel, damit beide Instrumente dieselbe Sprache
sprechen.

Ausgangslage: LTT arbeitet in diesem Jahr zeitweise an mehr als 80 größeren Kundenprojekten
gleichzeitig. Knapp sind nach den Meldungen der Business Units durchgehend vier Qualifikationen -
Senior Process Engineers, Automatisierungsingenieure, Projektleiter und Inbetriebnehmer. Die
durchschnittliche Zahl paralleler Projekte je Projektleiter ist gegenüber dem Vorjahr deutlich
gestiegen; das PMO zählt für April sechs bis acht laufende Projekte je Projektleiter, wobei die
Abgrenzung zwischen laufendem Projekt, Angebotsbegleitung und Gewährleistungsfall zwischen den
Business Units nicht einheitlich ist. Die Zahl ist als Größenordnung belastbar, nicht als Kennzahl.

## 2 Bewertungsschema

Eintrittswahrscheinlichkeit E: 1 gering, 2 möglich, 3 wahrscheinlich, 4 bereits eingetreten oder sehr
wahrscheinlich innerhalb von sechs Monaten.
Auswirkung A: 1 gering, 2 spürbar, 3 erheblich, 4 kritisch für Termin, Ergebnis oder Kundenbeziehung.
Risikowert RW = E x A. Ampel nach POL-PM-002: rot ab 9, gelb 4 bis 8, grün bis 3.

## 3 Register

| ID | Risiko | E | A | RW | Ampel | Verantwortlich | Status |
|---|---|---:|---:|---:|---|---|---|
| R-PF-01 | Portfolio übersteigt die verfügbare Engineering-Kapazität | 4 | 4 | 16 | rot | Geschäftsführung | offen, eskaliert |
| R-PF-02 | Engpass Auslegung, Senior Process Engineers | 4 | 4 | 16 | rot | Engineering (Central) | offen |
| R-PF-03 | Engpass Automatisierung und Schaltschrankengineering | 3 | 3 | 9 | rot | P-029 Wiesner | offen |
| R-PF-04 | Zahl paralleler Projekte je Projektleiter beeinträchtigt die Steuerbarkeit | 4 | 3 | 12 | rot | PMO, BU-Leitungen | offen |
| R-PF-05 | Engpass Inbetriebnahme, insbesondere Auslandsbaustellen | 3 | 3 | 9 | rot | P-013 Aurich | offen |
| R-PF-06 | Doppelbindung von Schlüsselpersonen durch ONE LTT | 3 | 4 | 12 | rot | Programmleitung, Geschäftsführung | offen |
| R-PF-07 | Zusatzaufwand aus der EBOM-MBOM-Übergabe in laufenden Projekten | 3 | 2 | 6 | gelb | P-028 Gehrke, P-026 Zeller | in Klärung |
| R-PF-08 | Ressourcenplanung nach POL-PM-003 ist nicht belastbar | 4 | 2 | 8 | gelb | PMO | offen |
| R-PF-09 | Engineering-Kapazität ist nicht Bestandteil des S&OP | 4 | 3 | 12 | rot | P-024 Damm | offen seit 2021 |
| R-PF-10 | Kein Rahmen für den Zukauf externer Engineering-Kapazität | 3 | 3 | 9 | rot | P-025 Ehlers | offen |
| R-PF-11 | Einarbeitungsdauer neu eingestellter Ingenieure | 3 | 2 | 6 | gelb | P-032 Kirchner | offen |
| R-PF-12 | Kapazitätslage Compressor Systems, Eisenach | - | - | - | nicht bewertet | P-012 Steinbach | Rückmeldung ausstehend |

Neun von zwölf Einträgen stehen bei Erstaufnahme auf rot oder gelb. Das ist kein Ergebnis einer
strengen Bewertung, sondern der Grund, warum dieses Register angelegt wurde.

## 4 Erläuterung der Einträge mit Risikowert ab 12

### R-PF-01 Portfolio übersteigt die verfügbare Engineering-Kapazität

Ursache: Aufträge werden angenommen, ohne dass die Engineering-Kapazität zum geplanten
Bearbeitungszeitraum geprüft wird. Eine kapazitätsgestützte Portfolioplanung existiert nicht; geprüft
werden Angebotsrisiko und Marge, nicht die Verfügbarkeit der Auslegung.

Wirkung: Projektstarts werden verschoben, ohne dass die Kundentermine nachgezogen werden. Der Puffer
wird jeweils aus der Engineering-Phase entnommen, weil sie am Anfang liegt und der Kunde sie nicht
sieht. Der Aufholbedarf verlagert sich in Konstruktion und Inbetriebnahme.

Bisherige Handhabung: Priorisierung im Einzelfall, meist telefonisch zwischen Business Unit und
Engineering, ohne Dokumentation. Wer zuerst ruft, bekommt den Konstrukteur.

Vorschlag des PMO: Freigabe neuer Projekte im Monatsreview gegen eine Kapazitätsaussage der
betroffenen Fachbereiche. Das setzt eine Entscheidung darüber voraus, wer im Konfliktfall
priorisiert. Diese Entscheidung liegt nicht beim PMO.

### R-PF-02 Engpass Auslegung, Senior Process Engineers

Ursache: Die thermische Auslegung anspruchsvoller Projekte, insbesondere Hochtemperaturanwendungen
und Wärmequellenanalysen beim Kunden, wird von einem sehr kleinen Kreis erfahrener Ingenieure
getragen. Freigabeberechtigt für Auslegungsergebnisse nach POL-VTR-001 v2.0 ist ein noch kleinerer
Kreis. Application Engineering in Brno kann zuarbeiten, aber nicht freigeben.

Wirkung: Die Angebotsreviews für Projekte über 500.000 EUR laufen in eine Warteschlange. Zwei
Angebote im April wurden nach dem vom Vertrieb zugesagten Termin abgegeben. Bei Ausfall oder Urlaub
einzelner Personen ist keine Vertretung vorhanden.

Anmerkung: Dieses Risiko ist kein Planungsproblem, sondern ein Personenproblem. Es lässt sich mit
keiner Methodik des PMO lösen.

### R-PF-04 Zahl paralleler Projekte je Projektleiter beeinträchtigt die Steuerbarkeit

Ursache: Wachsender Auftragsbestand bei nahezu unveränderter Zahl von Projektleitern. Hinzu kommt,
dass mehrere Projektleiter neben ihren Projekten in Programmarbeitskreisen mitwirken.

Wirkung: Statusberichte kommen verspätet oder unvollständig. Risikoregister der Einzelprojekte werden
fortgeschrieben, aber nicht mehr überarbeitet. Änderungen kommen später in den Change-Request-Prozess,
teilweise erst nach begonnener Umsetzung. Die Berichtsqualität sinkt genau dann, wenn sie am
wichtigsten wäre.

Maßnahme: Die Projektampel nach POL-PM-002 ist seit dem 01.04. in Anwendung; der erste vollständige
Durchlauf erfolgt mit dem Monatsreview im Mai. Sie macht die Lage sichtbar, sie entlastet niemanden.
Ihre Aussagekraft hängt daran, dass die Business Units die Einstufung nicht nach Wunschbild vergeben.
Das PMO wird die Einstufungen ab Mai stichprobenweise gegen Termin- und Kostenstand prüfen.

Offen: eine Obergrenze der gleichzeitig geführten Projekte je Projektleiter. Das PMO hält eine solche
Regel für sinnvoll, sieht aber, dass sie ohne Entscheidung über die Auftragsannahme nur die
Warteschlange an eine andere Stelle verschiebt.

### R-PF-06 Doppelbindung von Schlüsselpersonen durch ONE LTT

Ursache: Das Programm arbeitet seit Januar mit Process Ownern und Key Usern aus den Fachbereichen.
Die Master-Data-Bereinigung mit konzernweit mehr als 180.000 Materialnummern und die Einführung der
durchgängigen EBOM-MBOM-Struktur greifen auf dieselben Konstrukteure und Arbeitsvorbereiter zu, die
in den Projekten die Auslegung und die Stücklisten verantworten. Der Greenfield-Ansatz des Programms
verlangt eine intensive Beteiligung der Fachbereiche an der Prozessdefinition, weil die
Standardprozesse gegen die heutige Arbeitsweise gehalten werden müssen.

Wirkung: Mitarbeiterinnen und Mitarbeiter mit Programmrolle stehen den Projekten faktisch nicht
vollständig zur Verfügung. In der Projektplanung sind sie weiterhin voll eingeplant, weil die
Programmrollen keinen Kapazitätsabzug auslösen. Der Konflikt taucht deshalb nicht in der Planung auf,
sondern erst in der Terminmeldung.

Vorschlag des PMO: benannte Key User mit ausgewiesenem Zeitanteil, dieser Anteil in der
Ressourcenplanung als gebunden geführt, und eine Vertretungsregelung für Projektaufgaben. Die
Qualifizierung der Key User ist nach BV-2023-01 ohnehin zugesagt; der Zeitbedarf dafür ist in keiner
Projektplanung enthalten.

Neben ONE LTT binden PRJ-BU-REORG-2022, PRJ-MDM-2023, PRJ-EBOM-MBOM-2023 und PRJ-FOUNDRY2025
Leitungskapazität, die in den Projektplänen nicht abgebildet ist. Transformationsprojekte erscheinen
im Portfolio, aber nicht in der Ressourcenplanung.

### R-PF-09 Engineering-Kapazität ist nicht Bestandteil des S&OP

Ursache: Der monatliche S&OP-Prozess nach POL-SCM-002 plant Material und Fertigungskapazität. Die
Engineering-Kapazität ist seit Einführung 2021 nicht Teil des Prozesses.

Wirkung: Es entsteht regelmäßig die Lage, dass die Fertigung nach S&OP freie Kapazität ausweist,
während Projekte nicht anlaufen können, weil Konstruktion und Auslegung nicht verfügbar sind. Die
Fertigung plant auf einen Auftragseingang, der so nicht kommt, und schiebt anschließend nach.

Bewertung: Der Sachverhalt ist seit zwei Jahren bekannt und in mehreren Projektreviews benannt
worden. Er ist hier aufgenommen, weil er bei der aktuellen Portfoliogröße nicht mehr als
Reibungsverlust durchgeht.

## 5 Einträge mit geringerem Risikowert, in Kurzform

**R-PF-03** Automatisierung ist doppelt gebunden: durch die Projekte selbst und durch den
Mehraufwand aus zwei Schaltschrankpartnern mit unterschiedlichen Klemmensystemen,
Dokumentationsstandards und Bibliotheken. Der Aufwand fällt intern an und ist keinem Lieferanten
zugeordnet. Solange kein gemeinsamer Standard besteht, ist die Zweitquelle
kapazitätsseitig ein Zusatzaufwand und keine Entlastung.

**R-PF-05** Inbetriebnehmer sind über längere Zeiträume auf Auslandsbaustellen gebunden, unter
anderem in Dänemark und in den Vereinigten Staaten. Reise- und Standzeiten sind in der Planung mit
Erfahrungswerten hinterlegt, die aus der Zeit vor 2020 stammen. Rückkehrer stehen für die
Projektabnahme im Inland nicht zur Verfügung.

**R-PF-07** Die formelle Übergabe zwischen Konstruktion und Produktion nach POL-ENG-001 v1.1 gilt
seit dem 01.04. Für Projekte, die vor diesem Datum den Design Freeze passiert haben, fehlt eine
Übergangsregelung. Engineering meldet zusätzlichen Dokumentationsaufwand, die Arbeitsvorbereitung
erwartet weniger Rückfragen. Beides kann zutreffen; belastbare Zahlen liegen frühestens im Herbst
vor.

**R-PF-08** Die zentrale Ressourcenplanung nach POL-PM-003 wird von mehreren Fachbereichen parallel
zu eigenen Tabellen geführt. Die Stände weichen voneinander ab, und im Zweifel gilt die Tabelle des
Abteilungsleiters. Das ist seit 2017 so und war bei dreißig Projekten verkraftbar. Die
Kapazitätsaussagen in diesem Register stützen sich deshalb auf Meldungen, nicht auf eine Auswertung.

**R-PF-10** Für den kurzfristigen Zukauf von Konstruktions- und Auslegungsleistungen existiert kein
Rahmenvertrag und kein qualifizierter Anbieter. Ein Zukauf im Einzelfall dauert nach Einschätzung des
Einkaufs länger als der Engpass, den er beheben soll. Der strategische Einkauf ist um eine
Einschätzung gebeten.

**R-PF-11** Neu eingestellte Ingenieure sind nach den Erfahrungen der Fachbereiche erst nach
mehreren Monaten eigenständig einsatzfähig, bei der Auslegung deutlich später. Einstellungen wirken
im laufenden Geschäftsjahr kapazitätsseitig kaum entlastend und binden zunächst erfahrene Kollegen.

**R-PF-12** Compressor Systems hat zum Stichtag nicht gemeldet. Die Kapazitätslage in Eisenach ist
daher nicht bewertet. Das Register bildet insoweit nur die Kassler Sicht ab. Nachtrag zur Fassung vom
31.05. zugesagt.

## 6 Anmerkung des PMO

Das PMO kann Kapazitätsrisiken sichtbar machen, es kann sie nicht auflösen. Alle Instrumente, die in
diesem Register als Maßnahme genannt sind - Ampel, Monatsreview, Ressourcenplanung - erzeugen
Transparenz und keine Ingenieurstunden. Die eigentliche Entscheidung ist eine Portfolioentscheidung:
entweder werden weniger Projekte gleichzeitig geführt, oder die Termine werden bei Annahme
realistisch gesetzt, oder es wird Kapazität aufgebaut beziehungsweise zugekauft. Solange keine dieser
drei Entscheidungen fällt, verteilt die Organisation den Engpass informell, und das Ergebnis dieser
Verteilung erfährt das PMO im Nachhinein aus den Terminmeldungen.

Das Register wird zum Monatsreview am 31.05.2023 fortgeschrieben. Bitte um Rückmeldungen zu den
Verantwortlichkeiten bis zum 12.05.2023.

G. Sattler, PMO
