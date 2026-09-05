---
doc_id: LTT-20220810-ENG-01
titel: Technische Unterschiede der beiden Schaltschrankpartner
dokumenttyp: Meeting Minutes
datum: 2022-08-10
verfasser: Rolf Wiesner
rolle: Leiter Elektrotechnik und Automatisierung
organisationseinheit: ENG
empfaenger: "-"
projekt: SUP-ELEKTROPLAN
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [bereichsintern, projektintern]
ablageort: projektlaufwerk
---

# Besprechungsprotokoll

**Thema:** Technische Unterschiede NordControl / ElektroPlan Süd im Schaltschrankbau
**Datum, Zeit:** Mittwoch, 10.08.2022, 09:00 bis 10:45 Uhr
**Ort:** Kassel, Besprechungsraum B2-14; J. Kowalski über Teams zugeschaltet
**Sitzungsleitung und Protokoll:** R. Wiesner
**Teilnehmer:** R. Wiesner (Elektrotechnik und Automatisierung), P. Ehlers (strategischer Einkauf),
B. Hoffmann (Qualitätsmanagement), A. Yildirim (Projektleitung), J. Kowalski (Projektleitung,
Inbetriebnahme)
**Entschuldigt:** U. Damm (Supply Chain & Operations Planning)
**Verteiler:** Teilnehmer, U. Damm; Ablage Projektlaufwerk SUP-ELEKTROPLAN

## Anlass

Nach der Vorlage vom 12.07. ist ElektroPlan Süd als zweiter Schaltschrankpartner qualifiziert. Ziel
dieser Runde war ausschließlich, die technischen Unterschiede der beiden Häuser zusammenzutragen und
zu benennen, welcher Aufwand daraus in der Elektrokonstruktion entsteht. Kaufmännische Fragen,
Rahmenvertrag und Preisniveau waren nicht Gegenstand.

## 1. Ausgangslage

NordControl fertigt seit Jahren den weit überwiegenden Teil unserer Schränke, zuletzt rund 65 Prozent;
der Rest verteilt sich im Wesentlichen auf Auconta und Litec. Terminzusagen wurden in den vergangenen
Monaten mehrfach nicht gehalten. P. Ehlers erinnert an den Dual-Source-Grundsatz von 2021
(POL-SCM-001): komplexe Schaltschrankkonfigurationen waren dort ausdrücklich ausgenommen, genau diese
Ausnahme wird mit der Qualifizierung jetzt geschlossen.

Ich halte für das Protokoll fest, dass ich die Zweitquelle für richtig halte. Zwei Partner heißen für
mich aber nicht zwei Standards. Was wir an Durchlaufzeit gewinnen, dürfen wir nicht in der
Elektrokonstruktion wieder verlieren.

## 2. Klemmensysteme

- NordControl: Schraubklemmen als Hausstandard, Doppelstockklemmen für Sensorik, fortlaufende
  Klemmennummerierung über den gesamten Schrank.
- ElektroPlan Süd: Push-in-Federkraftklemmen, Klemmenblöcke nach Funktionsgruppen getrennt und je
  Gruppe neu beginnend nummeriert.

Auswirkung: Unsere Klemmenpläne sind nicht mehr ohne Nacharbeit für beide Häuser verwendbar.
J. Kowalski weist darauf hin, dass die Inbetriebnehmer auf der Baustelle dann eine andere Nummerierung
vorfinden als im Anlagenschaltplan; Änderungen werden dort ohnehin zuerst handschriftlich auf dem
Ausdruck festgehalten und laufen erst später zurück. Zwei Systematiken erhöhen dort die Fehlerquote
spürbar. Die Ersatzteilseite ist damit ebenfalls berührt, wurde aber nicht vertieft, weil der Service
nicht vertreten war.

## 3. Dokumentationsstandard

NordControl liefert den Revisionsstand als PDF-Satz und zusätzlich das bearbeitete EPLAN-Projekt
zurück. ElektroPlan Süd arbeitet ebenfalls mit EPLAN, verwendet aber eine eigene Deckblatt- und
Seitennummernsystematik, und die Betriebsmittelkennzeichnung weicht in Teilen von unserer Vorgabe nach
DIN EN 81346 ab. Ob EPS die As-built-Unterlagen als vollständiges EPLAN-Projekt zurückgibt oder wie im
Qualifizierungsmuster nur als PDF mit Excel-Kabelliste, ist derzeit offen.

B. Hoffmann: Die Dokumentenlenkung in der Fassung von 2022 (POL-QM-001, v2.0) verlangt für die digitale
Projektakte eine einheitliche Benennung. Zwei Zulieferersystematiken sind darin nur mit einer
Zusatzregel abbildbar, und die schreibt QM nicht ohne Vorgabe aus der Elektrotechnik.

## 4. Kabelführung und Schrankaufbau

NordControl führt die Kabel von unten über eine Abfangschiene ein, Verdrahtungskanäle sind großzügig
dimensioniert, der Klemmenraum ist getrennt. EPS führt seitlich ein, baut kompakter und mit engeren
Kanalquerschnitten. Für unsere Skids ist die kompaktere Bauform teilweise ein Vorteil, bei
Nachrüstungen und bei Aufstellung in Containern eher nicht. A. Yildirim merkt an, dass die
Aufstellfläche in mehreren laufenden Anfragen ohnehin knapp ist.

## 5. Prüfprotokolle

Beide Häuser prüfen nach DIN EN 61439-1/-2. Unterschiedlich ist die Protokolltiefe: NordControl
protokolliert je Betriebsmittel, EPS liefert ein Sammelprotokoll mit Stichprobenliste. B. Hoffmann
hält das für unsere FAT-Systematik (POL-QM-002) für nicht ausreichend; Isolationsmesswerte und
Durchgangsprüfung müssen je Stromkreis vorliegen, sonst wiederholen wir die Prüfung im eigenen Haus.
Das wäre der Kapazitätsgewinn, der uns an anderer Stelle wieder abgeht.

## 6. Bibliotheken

Das ist aus meiner Sicht der eigentliche Aufwandstreiber und nicht die Klemme. Unsere Makro- und
Artikelstammbibliothek in EPLAN ist über Jahre auf den NordControl-Aufbau abgestimmt worden, der
Artikelstamm hängt am ERP. Für EPS brauchen wir zweite Varianten der betroffenen Makros. Damit haben
wir doppelte Pflege und die naheliegende Fehlerquelle, dass in einem Projekt die falsche Variante
gezogen wird.

Grobschätzung von mir, ausdrücklich keine Kalkulation: 15 bis 20 Personentage Erstaufbau, danach
rund zwei Tage im Monat Pflege. Seit Juli bearbeiten wir außerdem Anfragen faktisch in zwei
Ausführungsvarianten, was pro Anfrage ungefähr einen halben Tag zusätzlich kostet. Genau dieser
Aufwand ist in der Vorlage vom 12.07. nicht beziffert.

## 7. Diskussion zur Verbindlichkeit

Mein Vorschlag: eine LTT-Elektrovorgabe für Schaltschränke mit Klemmensystem, Kennzeichnung, Umfang
und Format der Dokumentationsrücklieferung sowie Prüfumfang, verbindliche Anlage zu jeder Anfrage und
Bestellung, für beide Häuser gleich.

P. Ehlers hält eine vollständige Angleichung in der Anlaufphase bei EPS für nicht durchsetzbar; wir
hätten den Partner qualifiziert, weil er Kapazität und kurze Zusagen bietet, und sollten ihn nicht
sofort auf den Hausstandard des Wettbewerbers zwingen. Ihr Gegenvorschlag: Mindestumfang jetzt
verbindlich, alles Weitere über die Lieferantenbewertung (POL-EK-001, v2.0) entwickeln.

Ein Beschluss ist nicht gefasst worden. Der Punkt geht mit U. Damm in eine gesonderte Abstimmung.

## Maßnahmen

| Nr | Maßnahme | Wer | Bis |
|---|---|---|---|
| 1 | Entwurf der Elektro-Mindestvorgabe (Klemmensystem, Kennzeichnung, Doku-Rücklieferung) | Wiesner | 02.09.2022 |
| 2 | Klärung mit EPS, ob und in welchem Versionsstand EPLAN-Projekte zurückgeliefert werden | Ehlers | 26.08.2022 |
| 3 | Ergänzungsblatt Prüfprotokoll je Stromkreis, abgestimmt auf die FAT-Systematik | Hoffmann | 09.09.2022 |
| 4 | Aufwandsschätzung Bibliothekspflege belastbar unterlegen | Wiesner | 07.09.2022 |
| 5 | Abstimmungstermin mit U. Damm zur Verbindlichkeit der Vorgabe | Ehlers | KW 35 |
| 6 | Zuordnung des ersten Schrankpakets an EPS | offen | offen |

## Offene Punkte

- Verbindlichkeit der Elektrovorgabe ist nicht entschieden (siehe Nr. 5).
- Service und Ersatzteilhaltung waren nicht vertreten; Nachholtermin mit E. Sandmann ist zu vereinbaren.
- Auswirkungen auf Auconta und Litec wurden nicht betrachtet. Wir reden derzeit über zwei Häuser und
  haben faktisch vier.
- Ob wir bei EPS auf den vollständigen EPLAN-Rücklauf bestehen, hängt an Nr. 2.

Nächster Termin: 07.09.2022, 09:00, gleicher Raum.

R. Wiesner
