---
doc_id: LTT-20180901-SITE-04
titel: "Risikoregister: Risiken der getrennten Systemlandschaft erfassen"
dokumenttyp: Risikoregister
datum: 2018-09-01
verfasser: Klaus Rothenberger
rolle: Standortleiter Eisenach
organisationseinheit: SITE
empfaenger: ["-"]
projekt: IP-2018-01
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [projektintern, bereichsintern]
ablageort: projektlaufwerk
---

LAHNBERG THERMOTECHNIK GMBH & CO. KG
Standort Eisenach

RISIKOREGISTER

Projekt:                 IP-2018-01, Integration Rothenberg Verdichtertechnik
Teilregister:            Systemlandschaft, Folgen des Weiterbetriebs zweier getrennter Landschaften
Registerstand:           01.09.2018, Fassung 1.0, Erstaufstellung
Aufgestellt von:         Klaus Rothenberger, Standortleitung Eisenach
Grundlage:               POL-PM-001 v1.1, Abschnitt Risikoregister; Architekturentscheidung vom 11.07.2018 zum Weiterbetrieb beider ERP-Landschaften
Ablage:                  Projektlaufwerk IP-2018-01
Verteiler:               Projektakte; Einzelabstimmung mit den unten benannten Verantwortlichen
Fortschreibung:          monatlich, erstmals zum Monatsreview Oktober 2018

## Vorbemerkung

Die Architekturentscheidung vom 11. Juli hat die Richtung festgelegt: beide ERP-Landschaften bleiben
vorerst nebeneinander bestehen, Eisenach arbeitet weiter mit dem Infor-System, Kassel mit proALPHA und
dem Teamcenter-PLM. Gegen den Leitsatz "Erst Geschäft integrieren, dann IT" habe ich sachlich nichts
einzuwenden. Wir sind seit Januar bei LTT, wir haben in diesem Jahr Verdichter zu liefern, und eine
Systemumstellung parallel zum laufenden Geschäft hätte uns beides gekostet.

Was die Entscheidung nicht geregelt hat, ist die Frage, wer den Aufwand trägt, der aus der Trennung
täglich entsteht, und nach welchen Regeln zwischen den beiden Häusern gearbeitet wird, solange sie
getrennt sind. Dieser Aufwand fällt derzeit ganz überwiegend hier an, in einem Standort mit rund 125
Mitarbeitern und einer IT-Betreuung, die für einen Betrieb dieser Größe ausgelegt war und nicht für
den Datenaustausch mit einem zweiten Werk.

Ich stelle die Punkte deshalb als Risikoregister nach dem Projektmanagement-Standard auf und nicht als
Sachstandsnotiz. Zwei Gründe: die Punkte sind bewertbar, und sie gehören in das Monatsreview des
Projekts und nicht in ein Gespräch am Rande. Ich beantrage mit diesem Register ausdrücklich keine
Investitionsfreigabe für eine Systemzusammenführung. Der weit überwiegende Teil der Maßnahmen unten
kostet kein Geld, sondern eine Festlegung, wer wofür zuständig ist.

## Bewertungsmaßstab

Eintrittswahrscheinlichkeit E und Auswirkung A jeweils in drei Stufen nach POL-PM-001 (1 gering,
2 mittel, 3 hoch). Risikoklasse K = E x A. Ab K = 6 berichtspflichtig im Monatsreview. Die Bewertung
ist meine eigene und mit den Verantwortlichen in Kassel nur teilweise abgestimmt; wo das nicht der
Fall ist, steht es in der Spalte Stand.

## Register

| ID | Risiko | Ursache | Mögliche Auswirkung | E | A | K |
|---|---|---|---|---|---|---|
| R-01 | Artikel-, Stücklisten- und Preisdaten der Verdichter laufen in beiden Systemen auseinander | Verdichter ist in Eisenach Erzeugnis, in Kassel Zukaufteil; beide Sätze werden getrennt gepflegt | falsche Kalkulationen, falsche Bedarfe, Rückfragen bei jeder Änderung | 3 | 2 | 6 |
| R-02 | Werkaufträge und Liefertermine zwischen Kassel und Eisenach werden manuell übertragen | keine Schnittstelle zwischen den ERP-Systemen; Abwicklung über Excel-Listen und E-Mail | Übertragungsfehler, keine belastbare Terminaussage gegenüber der Projektleitung, Terminverzug in Anlagenprojekten | 3 | 3 | 9 |
| R-03 | Kalkulations- und Kostendaten beider Werke sind nicht vergleichbar | unterschiedliche Kostenstellenlogik, unterschiedliche Zuschlagssätze, zwei Systeme | Bewertungen, die den Standort betreffen, stützen sich auf Zahlen, die methodisch nicht gleich gebildet sind | 3 | 3 | 9 |
| R-04 | Verdichterzeichnungen und Änderungsstände liegen außerhalb des PLM | Eisenach ist nicht an Teamcenter angebunden; Ablage auf Laufwerken und in lokalen Datenbanken | Kassel konstruiert gegen einen Stand, der hier bereits geändert wurde; Nacharbeit, im ungünstigen Fall Ausschuss | 2 | 3 | 6 |
| R-05 | Access- und Excel-Lösungen in Eisenach sind an einzelne Mitarbeiter gebunden | historisch gewachsen, keine Dokumentation, keine Vertretungsregelung | Ausfall einer Person legt Teilprozesse still (Prüfstandsdaten, Bearbeitungsplanung, Gussdisposition) | 2 | 3 | 6 |
| R-06 | Monatsabschluss und Projektmargenberichterstattung nach POL-FIN-003 müssen aus zwei Systemen zusammengeführt werden | keine gemeinsame Berichtsbasis | verspätete oder fehlerhafte Zahlen, Diskussion über die Zahl statt über die Sache | 3 | 2 | 6 |
| R-07 | Kapazitäten des Standorts (Prüfstände, mechanische Bearbeitung, Gießerei) sind in der zentralen Ressourcenplanung nach POL-PM-003 nicht abgebildet | Planung wurde 2017 für Kassel eingeführt; Eisenach plant weiter mit eigenen Listen | Zusagen an Projekte ohne Kapazitätsdeckung, insbesondere bei Prüfstandsbelegung | 3 | 2 | 6 |
| R-08 | Die Trennung wird örtlich als Dauerzustand gelesen | Leitsatz "Erst Geschäft integrieren, dann IT" ohne genannten Zeithorizont | jeder Monat erzeugt weitere Eigenlösungen, die eine spätere Zusammenführung teurer machen | 3 | 2 | 6 |
| R-09 | Zwei Verfahren für Benutzer und Berechtigungen | POL-IT-001 gilt formal für Kassel; Eisenach verwaltet eigenständig | unklare Zuständigkeit bei Ein- und Austritten und im Störungsfall, offene Zugänge nach Personalwechsel | 2 | 2 | 4 |
| R-10 | Lieferantenbasis doppelt geführt, Bewertung nach POL-EK-001 nur für Kassel | Rothenberg behält die eigenen Lieferanten | keine gemeinsame Sicht auf Doppelbezug und Abhängigkeiten; Bewertungsergebnisse nicht vergleichbar | 2 | 2 | 4 |
| R-11 | Dokumentenlenkung in Eisenach nach eigenem Verfahren, nicht nach POL-QM-001 | Übernahme ohne Anpassung der Verfahrensanweisungen | Nachweisführung gegenüber Kunden bei Verdichtern uneinheitlich | 2 | 2 | 4 |
| R-12 | Wiederanlauf nach einem Ausfall der Anbindung oder der Eisenacher Server ist nicht geregelt | Anbindung über die vorhandene VPN-Lösung, Sicherung lokal, kein abgestimmtes Verfahren mit Kassel | Stillstand der Auftragsabwicklung am Standort, Dauer nicht abschätzbar | 1 | 3 | 3 |

## Maßnahmen und Verantwortlichkeiten

| ID | Vorgeschlagene Maßnahme | Verantwortlich | Termin | Stand |
|---|---|---|---|---|
| R-01 | ein gemeinsamer Datensatz je Verdichtertyp, geführt in Eisenach, monatlicher Abgleich mit Kassel; Regel, wer ändern darf | K. Rothenberger, fachlich mit H. Zeller | 31.10.2018 | Vorschlag, noch nicht abgestimmt |
| R-02 | verbindliche Bestell- und Rückmeldeform zwischen den Werken; ein Formular, ein Weg, eine Ablage, bis eine technische Lösung entschieden ist | offen, aus meiner Sicht IT | 31.10.2018 | Zuständigkeit ungeklärt, mit K. Löbner zu klären |
| R-03 | Abstimmung einer gemeinsamen Kalkulationsbasis, mindestens für Verdichter und Gussteile | D. Anselm | 30.11.2018 | am 22.08. angefragt, Antwort steht aus |
| R-04 | Freigabestände der Verdichterzeichnungen werden in einer abgestimmten Liste geführt; keine Konstruktionsänderung ohne Meldung nach Kassel | K. Rothenberger, M. Gehrke | 15.10.2018 | in Abstimmung |
| R-05 | Bestandsaufnahme der lokalen Datenbanken und Tabellen, Vertretungsregelung für die drei wichtigsten | K. Rothenberger | 30.11.2018 | begonnen |
| R-06 | feste Termine und ein festes Format für die Zulieferung aus Eisenach | D. Anselm | 31.10.2018 | offen |
| R-07 | Eisenacher Engpasskapazitäten werden in der zentralen Ressourcenplanung mitgeführt, zunächst nur Prüfstände | G. Sattler | 30.11.2018 | angesprochen, nicht entschieden |
| R-08 | Aussage der Geschäftsführung, in welchem Zeitraum die Frage der Systemlandschaft wieder aufgerufen wird | W. Bergmann, Dr. J. Mahlberg | offen | zur Kenntnis, keine Maßnahme des Projekts |
| R-09 | einheitliches Verfahren für Ein- und Austritte; Berechtigungen bleiben lokal, das Verfahren nicht | K. Löbner | 31.10.2018 | offen |
| R-10 | Übersicht der Eisenacher Lieferanten an den strategischen Einkauf, ohne Änderung bestehender Bezugswege | P. Ehlers | 15.10.2018 | zugesagt |
| R-11 | Abgleich der Eisenacher Verfahrensanweisungen mit POL-QM-001, Anpassung nur dort, wo Kundennachweise betroffen sind | B. Hoffmann | 31.12.2018 | offen |
| R-12 | schriftliche Festlegung, wer im Ausfall wen informiert und in welcher Reihenfolge wieder angefahren wird | K. Löbner, K. Rothenberger | 30.11.2018 | offen |

## Erläuterungen zu einzelnen Punkten

**R-02.** Dies ist der Punkt, der uns im Tagesgeschäft am meisten kostet. Ein Anlagenprojekt aus Kassel
bestellt bei uns einen Verdichtersatz, die Bestellung entsteht im dortigen ERP, wird ausgedruckt oder
als Tabelle geschickt und hier von Hand angelegt. Rückmeldungen laufen denselben Weg zurück. Solange
die Mengen klein waren, war das eine Frage der Sorgfalt. Bei der jetzigen Zahl an Vorgängen ist es
eine Frage der Zeit, bis ein Termin falsch übertragen wird und ein Projektleiter sich zu Recht
beschwert. Mir ist bewusst, dass die Antwort darauf nicht eine Schnittstelle sein kann, die wir gerade
nicht bauen. Die Antwort ist eine verbindliche Form. Die gibt es bisher nicht, weil niemand benannt
ist, der sie festlegt.

**R-03.** Ich führe diesen Punkt bewusst mit der höchsten Klasse. Die Überprüfung der Fertigungstiefe
ist angekündigt, und sie wird die mechanische Bearbeitung und die Gießerei hier betreffen. Unsere
Gießerei steht dabei im unmittelbaren Vergleich mit einem eingeführten externen Gusslieferanten. Ein
solcher Vergleich ist legitim, und ich stelle mich ihm. Er setzt aber voraus, dass die Zahlen beider
Seiten methodisch gleich gebildet sind. Derzeit sind sie das nicht: die Kostenstellenstruktur in
Eisenach stammt aus der Zeit vor der Übernahme, Umlagen und Zuschläge sind anders geschnitten als in
Kassel, und der Vergleich läuft über zwei Systeme, die nichts voneinander wissen. Wer auf dieser
Grundlage rechnet, bekommt ein Ergebnis, das mehr über die Kostenrechnung aussagt als über die
Fertigung. Ich bitte darum, die gemeinsame Basis vor der Bewertung herzustellen, nicht danach.

**R-08.** Der Leitsatz "Erst Geschäft integrieren, dann IT" wird hier im Haus inzwischen verkürzt als
"die IT bleibt, wie sie ist" verstanden. Das ist nicht die Schuld des Leitsatzes, sondern die Folge
eines fehlenden Zeithorizonts. Die praktische Wirkung sehe ich jede Woche: wo etwas zwischen den
Werken nicht geht, baut sich jemand eine Tabelle, und diese Tabelle wird gepflegt, weitergegeben und
nach einem halben Jahr für einen Prozess gehalten. Wir vergrößern damit genau den Bestand an
Eigenlösungen, den eine spätere Zusammenführung abzulösen hätte. Ich erwarte keine Terminzusage für
eine Harmonisierung. Ich halte aber eine Aussage für nötig, wann die Frage überhaupt wieder auf die
Tagesordnung kommt, damit wir uns hier nicht dauerhaft einrichten.

## Noch nicht bewertete Meldungen

Zwei Punkte sind mir mündlich zugetragen worden; sie sind noch nicht geprüft und deshalb ohne
Bewertung aufgenommen:

- Kollisionen im Sachnummernkreis, wenn Zeichnungen aus Kassel in Eisenach abgelegt werden. Umfang
  unklar, Prüfung durch die Arbeitsvorbereitung angefragt.
- Behandlung von Änderungsanträgen an Verdichtern, sobald der im Haus diskutierte
  Design-Freeze-Meilenstein und das geregelte Änderungsverfahren stehen. Solange dort nichts
  entschieden ist, lässt sich der Aufwand für uns nicht abschätzen. Aufnahme in das Register, sobald
  die Festlegung vorliegt.

## Nicht Gegenstand dieses Registers

Fertigungs-, Qualitäts- und Personalrisiken des Standorts, kaufmännische Risiken der Transaktion und
die Frage der Fertigungstiefe selbst. Erfasst sind ausschließlich Risiken, die aus dem parallelen
Betrieb zweier getrennter Systemlandschaften entstehen.

Eisenach, 01.09.2018
K. Rothenberger
