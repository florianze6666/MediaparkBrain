---
doc_id: LTT-20240312-PROG-00
titel: Verschiebung des ERP-Go-live und Anpassung des Programmaufwands
dokumenttyp: Entscheidungsvorlage
datum: 2024-03-12
verfasser: Dr. Simone Hartwig
rolle: Programmleiterin ONE LTT
organisationseinheit: Programm
empfaenger: [Geschäftsführung]
projekt: ONE LTT
geschaeftsbereich: "-"
vertraulichkeit: C-Level
informationsdomaene: [c-level-beirat, projektintern]
ablageort: sharepoint_gf
---

# Entscheidungsvorlage: Verschiebung des ERP-Go-live und Anpassung des Programmaufwands

**Vorlage** ONE-LTT/EV-2024-03
**An** Geschäftsführung
**Von** Dr. Simone Hartwig, Programmleitung ONE LTT
**Nachrichtlich** Dr. Nowak (IT), Herr Anselm (Controlling), Herr Bensch (Teilprojekt ERP und Stammdaten)
**Datum** 12.03.2024
**Einstufung** C-Level, nicht zur Weitergabe in die Business Units
**Entscheidung erbeten bis** 20.03.2024, wegen der Vorbereitung der Beiratsunterlage

## 1. Anlass

Der Steuerungskreis hat am 05.03.2024 die Terminlage des Teilprojekts ERP behandelt und die
Verschiebung des für April vorgesehenen Go-live als kontrollierte Risikoreduktion eingeordnet. Diese
Vorlage führt den förmlichen Beschluss herbei, benennt die Bedingungen, unter denen die
Programmleitung den neuen Termin für haltbar hält, und ordnet die Aufwandsfolge ein.

Die Programmleitung hat den Reifegrad der Stammdaten und der Migration zuletzt im Dezember 2023 als
kritisch berichtet. Die Lage hat sich seither nicht wesentlich verbessert; sie ist jetzt belastbar
gemessen.

## 2. Beschlussvorschlag

1. Die Produktivsetzung des Ziel-ERP für Kassel und Eisenach wird von April auf den 01.10.2024
   verschoben. Cutover-Fenster ist das Wochenende 27. bis 30.09.2024.
2. Für den Zeitraum bis zum Cutover gilt ein Scope-Freeze. Zusätzliche Anforderungen werden
   ausschließlich über das Change Board des Programms entschieden und nur bei gesetzlicher oder
   vertraglicher Notwendigkeit zugelassen.
3. Die Business Units stellen die benannten Key User verbindlich mit mindestens 50 Prozent ihrer
   Arbeitszeit frei, für Stammdaten und Auftragsabwicklung mit 80 Prozent. Die Freistellung wird über
   die Ressourcenplanung nach POL-PM-003 v2.0 geführt und monatlich berichtet.
4. Die Programmleitung führt gemeinsam mit dem Implementierungspartner bis zum 30.04.2024 ein
   Re-Baselining durch. Die aktualisierte Investitionsvorlage nach POL-FIN-002 einschließlich
   Betrachtung der Gesamtbetriebskosten wird der Geschäftsführung bis zum 15.05.2024 vorgelegt.
5. Auftrag, Umfang und Zeitfenster des vom Beirat gewünschten unabhängigen Reviews werden bis zum
   20.03.2024 festgelegt.
6. Die Verhandlung der Teilvereinbarung zum ERP nach BV-2023-01 wird im April aufgenommen.

## 3. Ausgangslage

Das Programm läuft seit Januar 2023. Produktiv sind das CRM seit April 2023, die
Managementberichterstattung seit 2023, die zentrale Datenplattform seit Oktober 2023 sowie das
Beschaffungsnetzwerk und die Reisekostenlösung seit Januar 2024. Diese Bausteine sind abgenommen und
stehen nicht zur Disposition.

Offen ist das Kernstück, die Ablösung der beiden bestehenden ERP-Landschaften in Kassel und Eisenach
durch ein gemeinsames Ziel-ERP. Für die Freigabe eines Go-live hat das Programm sechs
Reifegradkriterien definiert. Ihr Stand zum 08.03.2024:

| Kriterium | Stand | Bewertung |
|---|---|---|
| Bereinigung der Materialstämme | rund 18 Prozent der aktiven Stämme bereinigt gegenüber zuletzt angestrebten 25 Prozent | nicht erreicht |
| Migrationsprobeläufe | zwei Läufe durchgeführt, im zweiten Lauf 6,4 Prozent Abweichungen in den Materialstammdaten, überwiegend Einheiten und Bezeichnungslogik | nicht erreicht |
| Integrierter Testzyklus | erster Zyklus vom 05. bis 23.02.2024, 412 aufgenommene Fehler, davon 47 der Kategorie 1 | teilweise |
| Berechtigungskonzept nach POL-IT-001 v3.0 | Rollenmodell entworfen, Abgleich mit den Freigabegrenzen nach POL-FIN-001 v2.0 offen | nicht erreicht |
| Übergabe Engineering- an Fertigungsstückliste | Verfahren nach POL-ENG-001 v1.1 steht, Datenlage in den Altsystemen uneinheitlich | teilweise |
| Verfügbarkeit der Key User | im Mittel 31 Prozent der zugesagten Zeit | nicht erreicht |

Drei der sechs Kriterien sind nicht erreicht, zwei nur teilweise. Ein Go-live im April würde bedeuten,
die Auftragsabwicklung beider Standorte auf einer Datenbasis zu starten, deren Fehlerquote wir kennen
und nicht beherrschen. Die Folgekosten einer misslungenen Produktivsetzung im laufenden Geschäft
liegen erfahrungsgemäß deutlich über den Kosten einer Verschiebung.

Die Ursache liegt nicht allein im Programm. Der Zugriff auf die Key User konkurriert seit 2023 mit
einem außergewöhnlich hohen Auftragsbestand. Dieselben Personen, die die Stammdaten beurteilen können,
werden in den Projekten gebraucht. Diese Konkurrenz ist im Programmplan von 2022 nicht abgebildet
worden.

## 4. Geprüfte Optionen

**Option A, Festhalten am April.** Technisch möglich, wenn der Umfang auf die Auftragsabwicklung
reduziert und die Stammdatenbereinigung nach dem Go-live fortgesetzt wird. Die Programmleitung rät
davon ab. Wir würden die bekannten Fehler in das produktive System übernehmen und im Hochlastbetrieb
korrigieren; die Belastung träfe die Bereiche, die derzeit ohnehin am Anschlag arbeiten.

**Option B, Verschiebung auf Oktober.** Empfohlen. Sechs Monate erlauben zwei weitere Migrationsläufe,
einen zweiten und dritten Testzyklus, den Abschluss des Berechtigungskonzepts und eine Schulungsphase
ab August. Der Termin liegt außerdem nach der Urlaubszeit und vor dem Jahresabschluss, der Cutover
kollidiert nicht mit der Inventur.

**Option C, gestufter Go-live, Kassel zuerst.** Verworfen. Der Nutzen des Programms entsteht gerade
aus der gemeinsamen Datenbasis. Ein Zwischenstand mit einem produktiven Ziel-ERP in Kassel und einem
Altsystem in Eisenach erfordert Übergangsschnittstellen, die wir nach wenigen Monaten wieder
abschalten. Der Aufwand dafür liegt nach Schätzung des Partners bei 0,6 bis 0,9 Mio EUR, ohne
bleibenden Wert.

## 5. Aufwand und Budget

Der Implementierungspartner hat den erwarteten Gesamtaufwand am 04.03.2024 von 14,8 auf rund 19,0 Mio
EUR angehoben. Die Zuordnung der Differenz nach Angaben des Partners:

| Position | Betrag |
|---|---:|
| verlängerte Präsenz des Partners von April bis Oktober | 2,3 Mio EUR |
| zusätzliche Migrations- und Testzyklen | 0,8 Mio EUR |
| verlängerter Parallelbetrieb und Lizenzen der Altsysteme | 0,5 Mio EUR |
| interne Freistellung der Key User | 0,6 Mio EUR |
| **Summe** | **4,2 Mio EUR** |

Zwei Hinweise der Programmleitung. Erstens ist diese Aufstellung die Sicht des Partners und von uns
noch nicht geprüft; insbesondere die verlängerte Präsenz enthält Leistungen, die nach unserer Lesart
zum ursprünglichen Festpreisanteil gehören. Ich schlage vor, dem Beirat keine Zahl vorzulegen, die
allein vom Partner stammt, sondern das Ergebnis des Re-Baselining nach Nummer 4 des
Beschlussvorschlags. Zweitens sind die 0,6 Mio EUR für interne Freistellung nicht zahlungswirksam;
das Controlling möge die Behandlung im Programmbudget bestätigen, damit die Zahl gegenüber dem Beirat
nicht doppelt gelesen wird.

Die Anhebung überschreitet die Schwelle nach POL-FIN-002 und ist damit vorlagepflichtig. Diese
Entscheidungsvorlage ersetzt die Investitionsvorlage nicht; sie stellt die Terminentscheidung vorab
her, weil die Beauftragung des Partners für das zweite Quartal davon abhängt.

## 6. Risiken der empfohlenen Option

- Eine Verschiebung ist notwendig, aber nicht hinreichend. Ohne die Freistellung nach Nummer 3 des
  Beschlussvorschlags stehen wir im September an derselben Stelle, nur mit sechs Monaten mehr
  Partnerkosten. Ich bitte die Geschäftsführung ausdrücklich, diesen Punkt mitzuentscheiden und nicht
  an die Business Units zu delegieren.
- In der Programmorganisation wird die Verschiebung teilweise als Vertagung wahrgenommen. Dem lässt
  sich nur mit sichtbar veränderter Arbeitsweise begegnen, nicht mit einer Terminzusage. Die
  Reifegradkriterien werden deshalb ab April monatlich im Steuerungskreis mit Zahlen berichtet.
- Der Parallelbetrieb beider Altsysteme dauert sechs Monate länger. Die Verträge laufen weiter, der
  Betriebsaufwand der IT bleibt gebunden. Dr. Nowak hat dies für die IT-Planung 2024 zu
  berücksichtigen.
- Der Ampelstatus des Programms wird nach POL-PM-002 v1.1 auf Rot gesetzt. Das ist sachlich richtig
  und wird in der Berichterstattung an den Beirat so ausgewiesen.
- Die Erwartung, dass sich die Belastung im Engineering bis zum Herbst entspannt, ist eine Annahme
  und keine Planung. Trifft sie nicht ein, ist die Key-User-Verfügbarkeit erneut der begrenzende
  Faktor.

## 7. Auswirkungen auf Organisation und Mitbestimmung

Nach BV-2023-01 ist vor der Produktivsetzung eines Systems mit Bezug zu personenbezogenen Daten eine
Teilvereinbarung abzuschließen; für das ERP liegt sie nicht vor. Beim CRM lagen zwischen dem
Widerspruch des Gesamtbetriebsrats im Mai und der Unterzeichnung im Juli 2023 sechs Wochen. Für das
ERP ist mit einem längeren Verlauf zu rechnen, weil Auftrags-, Zeit- und Fertigungsdaten zusammenlaufen
und die Zuordenbarkeit einzelner Vorgänge zu Personen weiter reicht als im Vertrieb. Der neue Termin
gibt uns diese Zeit; bei einem Go-live im April hätten wir sie nicht gehabt. Ich schlage vor, Frau
Marquardt und Herrn Rühl im April die Systembeschreibung und den Datenkatalog vorzulegen.

Ebenfalls im zweiten Quartal fällig ist die Evaluation des CRM nach zwölf Monaten, die BV-2023-01
verlangt. Sie bindet dieselben Key User im Vertrieb. Der Termin ist mit HR und der Vertriebsleitung
abzustimmen, damit beides nicht in dieselbe Woche fällt.

Für die Qualifizierung ergibt sich eine Verbesserung. Die Schulungen können ab August in den
Regelbetrieb gelegt werden statt in die Wochen unmittelbar vor dem Cutover.

## 8. Beirat

Der Beirat hat einen unabhängigen Review des Programms verlangt. Die Programmleitung unterstützt das
und wird vollständig zuarbeiten. Ich bitte um Festlegung von Auftrag und Zeitfenster bis zum
20.03.2024. Fällt der Review in dieselben Wochen wie das Re-Baselining, binden beide Vorgänge
dieselben Personen und liefern zwei nicht abgestimmte Zahlenstände. Sinnvoll wäre ein Beginn nach dem
30.04.2024 auf Basis des dann vorliegenden neuen Plans.

## 9. Nächste Schritte

| Schritt | Verantwortlich | Termin |
|---|---|---|
| Beschluss der Geschäftsführung zu Abschnitt 2 | Geschäftsführung | 20.03.2024 |
| Festlegung des Reviewauftrags | Geschäftsführung mit Beirat | 20.03.2024 |
| Information der Business Units und der Programmorganisation | Programmleitung | 22.03.2024 |
| Vorlage der Systembeschreibung an den Gesamtbetriebsrat | Programmleitung, HR | 12.04.2024 |
| Re-Baselining mit dem Partner | Programmleitung, Teilprojekt ERP | 30.04.2024 |
| Aktualisierte Investitionsvorlage nach POL-FIN-002 | Programmleitung, Controlling | 15.05.2024 |

Dr. Simone Hartwig
Programmleitung ONE LTT
