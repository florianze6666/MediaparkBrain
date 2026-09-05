---
doc_id: LTT-20230218-PROG-03
titel: Prozessworkshops Kernprozesse ERP mit Key Usern, Workshopreihe 06. bis 16. Februar 2023
dokumenttyp: Meeting Minutes
datum: 2023-02-18
verfasser: Oliver Bensch
rolle: Teilprojektleiter ERP und Stammdaten
organisationseinheit: Programm
empfaenger: ["-"]
projekt: IP-2023-01
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [projektintern]
ablageort: projektlaufwerk
---

# Protokoll der Workshopreihe Kernprozesse ERP

Teilprojekt ERP und Stammdaten, Programm ONE LTT

Termine: 06.02., 08.02., 14.02. und 16.02.2023, jeweils 09:00 bis 13:00 Uhr
Ort: Kassel, Besprechungsraum Fulda; am 14.02. zusätzlich Eisenach, Raum Werra, und Teams
Protokollführung: O. Bensch, Teilprojektleitung ERP und Stammdaten
Fassung vom 18.02.2023, Entwurf. Einwände bitte bis 24.02.2023 an die Teilprojektleitung, danach gilt das Protokoll als abgestimmt.
Verteiler: Teilnehmer, Programmleitung, IT-Applikationen, benannte Process Owner

## Teilnehmer

| Name | Funktion | W1 | W2 | W3 | W4 |
|---|---|---|---|---|---|
| Dr. Simone Hartwig | Programmleitung ONE LTT | teilweise | - | - | teilweise |
| Oliver Bensch | Teilprojektleitung ERP und Stammdaten | x | x | x | x |
| Andrea Faber | Leiterin IT-Applikationen | x | x | x | x |
| Nicole Brandt | Lead Project Manager IHS | x | - | - | - |
| Tobias Kern | Commercial Project Manager | x | - | - | x |
| Martin Gehrke | Leiter Konstruktion mechanisch | - | x | - | - |
| Norbert Feld | Leiter Arbeitsvorbereitung | - | x | x | - |
| Hartmut Zeller | Leiter Operations | - | x | - | - |
| Bernd Hoffmann | Leiter Qualitätsmanagement | - | x | - | - |
| Dr. Frank Steinbach | Leiter Compressor Systems | - | Teams | - | - |
| Petra Ehlers | Leiterin strategischer Einkauf | - | - | x | - |
| Ulrich Damm | Leiter Supply Chain & Operations Planning | - | - | x | - |
| Annette Puhl | Standortleiterin Eisenach | - | - | Teams | - |
| Dieter Anselm | Leiter Controlling | - | - | - | x |
| Elke Sandmann | Leiterin Servicedisposition | - | - | - | x |
| Implementierungspartner | zwei Berater | x | x | x | x |
| Key User der Fachbereiche | je Workshop vier bis sieben Personen | x | x | x | x |

## 1. Anlass und Auftrag

Die erste Steuerungssitzung am 02.02.2023 hat die Teilprojekte beauftragt, die Kernprozesse bis
Ende des ersten Quartals gemeinsam mit den benannten Key Usern gegen das Standardmodell des
Implementierungspartners zu spiegeln. Grundlage ist der im Januar festgelegte Greenfield-Ansatz mit
dem Leitsatz "Adopt before adapt": der Standard wird übernommen, jede Abweichung ist zu begründen
und einzeln zu entscheiden.

Ergebnis der Reihe sollen sein: eine Prozesslandkarte auf zweiter Ebene, eine Liste der
Abweichungsanträge (Gap-Liste) und die ersten Anforderungen an den künftigen Materialstamm.

## 2. Workshop 1 am 06.02.2023: Angebot, Auftrag, Projektstruktur

Der Implementierungspartner stellte den Standardablauf von der Anfrage über die Angebotskalkulation
bis zum Kundenauftrag vor. Der Ablauf setzt einen konfigurierbaren Artikel voraus, der im Auftrag
variantenbezogen ausgeprägt wird.

Einwand von Frau Brandt: In unseren Projekten liegt zum Angebotszeitpunkt kein Artikel vor, sondern
eine Anlagenauslegung, die aus den Prozessdaten des Kunden entsteht. Die technische Angebotsreview
nach POL-VTR-001 v2.0 mit Wärmequellendaten und Annahmenprotokoll ist Bestandteil des
Angebotsprozesses und muss im System nachweisbar bleiben, nicht in einem Nebendokument.

Herr Kern ergänzte, dass die Angebotskalkulation heute in drei Ebenen geführt wird (Modul, Baugruppe,
Zukaufposition) und die Übernahme in die Auftragskalkulation über eine Excel-Zwischenstufe erfolgt.
Der Standard sieht zwei Ebenen vor.

Die Berater hielten dagegen, die dritte Ebene sei in der Mehrzahl der Angebote nicht befüllt und
damit ein Kandidat für Vereinfachung. Das wurde von den anwesenden Key Usern für das
Großanlagengeschäft bestritten, für das Servicegeschäft dagegen bestätigt.

Nicht abschließend geklärt. Aufgenommen als Gap-Anträge G-01 bis G-06, davon zwei auf Wunsch der
Programmleitung zurückgestellt, bis die Zielarchitektur für die Angebotskalkulation vorliegt.

## 3. Workshop 2 am 08.02.2023: Materialstamm, Stückliste, Änderungswesen

Ausgangslage aus der Bestandsaufnahme des Teilprojekts, im Workshop unbestritten: konzernweit
mehr als 180.000 Materialnummern, darunter Dubletten aus den beiden getrennten ERP-Beständen,
projektspezifische Einmalteile, mindestens vier Benennungslogiken aus verschiedenen Jahren,
uneinheitliche Mengeneinheiten und Altmaterialien ohne Sperrstatus. Das Programm arbeitet mit dem
Ziel, den Bestand aktiver Materialstämme zunächst um 40 Prozent zu senken.

Herr Gehrke widersprach der Lesart, ein hoher Anteil Einmalteile sei ein Datenproblem. Einmalteile
seien das Ergebnis kundenspezifischer Konstruktion und entstünden in jedem Projekt neu; wer sie
wegkürze, kürze das Geschäft. Herr Feld wies darauf hin, dass die Arbeitsvorbereitung eine von der
Konstruktionsstückliste getrennte Fertigungsstückliste benötigt und diese Trennung im Standardmodell
nur eingeschränkt vorgesehen ist.

Herr Hoffmann forderte, dass die digitale Projektakte nach POL-QM-001 v2.0 und der Freigabestand der
Zeichnungen an den Materialstamm gekoppelt bleiben. Design Freeze und Engineering Change Request
nach POL-ENG-001 müssen im Zielsystem abbildbar sein, einschließlich der Genehmigung verspäteter
Änderungen.

Herr Dr. Steinbach schilderte für Eisenach eine andere Lage: bei Verdichtern und beim laufenden
OEM-Rahmenabruf ist der Anteil wiederkehrender Teile hoch, dort trifft das Standardmodell die
Wirklichkeit deutlich besser als in Kassel.

Die Berater blieben bei ihrer Einschätzung, ein erheblicher Teil der bestehenden Sonderprozesse sei
historisch gewachsene Ineffizienz und werde durch die Migration ohnehin entfallen. Herr Gehrke und
Herr Zeller widersprachen ausdrücklich.

Vorschlag der Teilprojektleitung, im Workshop nicht bestritten, aber auch nicht beschlossen: Die
Zielquote bezieht sich auf Dubletten, Altbestände ohne Bewegung und stillgelegte Varianten. Projekt-
spezifische Einmalteile erhalten eine eigene Materialart, werden gesondert gezählt und gehen nicht
in die Bezugsgröße ein. Ohne diese Trennung ist die Quote weder erreichbar noch aussagefähig.

## 4. Workshop 3 am 14.02.2023: Beschaffung, Wareneingang, Lieferantenstamm

Der Lieferantenstamm liegt heute doppelt vor, in Kassel im proALPHA-System und in Eisenach im
Infor-System. Eine erste Gegenüberstellung der beiden Bestände durch das Teilprojekt zeigt eine
dreistellige Zahl von Lieferanten, die in beiden Systemen mit abweichender Schreibweise, teils auch
mit abweichenden Zahlungsbedingungen geführt werden. Frau Ehlers hält die Bereinigung für machbar,
wenn die Bewertungsdaten nach POL-EK-001 v2.0 mitgeführt werden und nicht neu erhoben werden müssen.

Herr Damm forderte, dass die Risikokategorien und der Dual-Source-Grundsatz nach POL-SCM-001 im
Lieferantenstamm hinterlegbar bleiben und dass die Sicherheitsbestandsregelung nach POL-SCM-005 v2.0
je Komponente abgebildet wird. Der Standardprozess kennt eine Wiederbeschaffungslogik über
Dispositionsparameter, aber keine Risikokategorie als Feld.

Frau Puhl meldete für Eisenach an, dass die Beschaffung im Gussbereich mit lokalen Lieferanten
arbeitet, unter anderem Werragrund Guss und seit Januar Moravia Precision Castings, und dass die
dortigen Abrufmodalitäten sich vom Kasseler Projektgeschäft unterscheiden. Sie bat darum, den
Eisenacher Ablauf nicht über die Kasseler Vorlage zu definieren.

Offen blieb die Frage, wie die projektbezogene Direktbeschaffung ohne Lagerzugang abgebildet wird.
Die Berater sehen dafür die Standard-Bestellanforderung mit Kontierung auf das Projekt, die Key User
halten die Freigabestrategie für zu langsam bei Terminlieferungen auf die Baustelle. Aufgenommen als
G-11 bis G-14.

Der Abgleich mit dem monatlichen S&OP-Prozess nach POL-SCM-002 wurde aus Zeitgründen vertagt.

## 5. Workshop 4 am 16.02.2023: Projektkosten, Abrechnung, Berichtswesen

Herr Anselm legte dar, dass die Projektmargenberichterstattung nach POL-FIN-003 heute an zwei
Stellen zusammengeführt wird und die Vergleichbarkeit zwischen den Standorten nur über manuelle
Nacharbeit hergestellt wird. Erwartung an das Zielsystem ist eine Kostenartenstruktur, die den
Vergleich mit den Vorjahren zulässt; für den seit Januar bereitstehenden Reporting-Dienst der IT ist
das die Voraussetzung.

Die Berater wiesen darauf hin, dass eine übernommene Kostenartenstruktur dem Greenfield-Ansatz
zuwiderläuft und die spätere Standardauswertung einschränkt. Herr Anselm hielt daran fest, dass eine
Kennzahlenreihe, die 2023 abreißt, gegenüber Beirat und Gesellschafter nicht vertretbar ist.

Kein Beschluss. Der Punkt wird der Programmleitung als Entscheidungsbedarf vorgelegt.

Frau Sandmann brachte die Serviceeinsätze ein: Abrechnung nach Aufwand, Ersatzteile aus dem
Projektbestand, heute mit eigener Nummernlogik. Der Punkt konnte nicht mehr behandelt werden, der
Workshop endete um 11:30 Uhr, weil zwei Key User wegen Kundenterminen kurzfristig absagten und Frau
Sandmann allein den Servicebereich vertrat. Nachholtermin ist zu vereinbaren.

## 6. Über alle vier Workshops wiederkehrend

1. Passung des Standardmodells. Die Key User führen an, das Modell des Implementierungspartners sei
   auf Serienfertigung zugeschnitten. Der Einwand kam in allen vier Workshops, in Eisenach schwächer
   als in Kassel.
2. Verfügbarkeit der Key User. Von 14 benannten Key Usern waren im Mittel acht anwesend. Vier
   Termine wurden vorab verschoben, zwei Teilnehmer sagten am Vortag ab. Als Grund wurde durchgehend
   die Projektlast genannt; derzeit laufen über 80 größere Kundenprojekte parallel.
3. Der Begriff "Sonderprozess" ist nicht definiert. Die Beratung zählt über 40 davon, unsere Bereiche
   erkennen ihre Prozesse in dieser Liste teilweise nicht wieder. Es fehlt ein gemeinsames Kriterium.
4. Verfahren für Abweichungen. Jede Abweichung wird als Gap-Antrag mit Begründung, Aufwand und
   Auswirkung erfasst und von der Programmleitung entschieden, ab einer noch festzulegenden Schwelle
   im Steering Committee.

## 7. Ergebnisse

- Prozesslandkarte Ebene 2 liegt für die Bereiche Angebot bis Auftrag, Material und Stückliste sowie
  Beschaffung im Entwurf vor. Projektabrechnung fehlt.
- Gap-Liste eröffnet. Stand 17.02.2023: 19 Einträge, davon 3 entschieden, 14 offen, 2 zurückgestellt.
- Die Zielquote von 40 Prozent bleibt unverändert. Die Bezugsgröße wird bis zum 03.03.2023 definiert
  und der Programmleitung vorgelegt.
- Zur Kostenartenstruktur besteht Entscheidungsbedarf oberhalb des Teilprojekts.

## 8. Maßnahmen

| Nr | Maßnahme | Verantwortlich | Termin |
|---|---|---|---|
| M-01 | Kriterienraster "Sonderprozess" entwerfen und mit der Beratung abstimmen | Bensch | 03.03.2023 |
| M-02 | Materialartenkonzept einschließlich Einmalteile, Entwurf | Bensch mit Gehrke, Feld | 03.03.2023 |
| M-03 | Bezugsgröße der Reduktionsquote definieren und dokumentieren | Bensch | 03.03.2023 |
| M-04 | Dublettenabgleich Lieferantenstamm über beide Systeme, Auswertung | Faber mit Ehlers | 10.03.2023 |
| M-05 | Nachholtermin Serviceprozesse ansetzen | Bensch mit Sandmann | Termin offen |
| M-06 | Entscheidungsvorlage Kostenartenstruktur an die Programmleitung | Anselm mit Bensch | 10.03.2023 |
| M-07 | Verbindliche Freistellung der Key User klären | Programmleitung | 28.02.2023 |
| M-08 | Abgleich Beschaffungsprozess mit S&OP nachholen | Damm mit Bensch | 10.03.2023 |

Nächster Termin: Abstimmung der Gap-Liste mit der Programmleitung am 28.02.2023, 14:00 Uhr.

## 9. Anmerkung der Teilprojektleitung

Drei Punkte, die ich nicht in den Protokollteil schreiben will, aber festhalten muss.

Erstens läuft die Diskussion über "Adopt before adapt" mit unscharfen Begriffen. Solange dasselbe
Wort für eine überflüssige Freigabeschleife und für die technische Substanz des Projektgeschäfts
verwendet wird, wird jeder Workshop denselben Streit neu führen. Der Leitsatz trägt dort, wo unser
Ablauf zufällig so gewachsen ist, und er trägt nicht dort, wo er aus der Anlagenauslegung folgt. Die
Unterscheidung ist Arbeit und niemand hat sie bisher gemacht; M-01 soll das nachholen.

Zweitens halte ich die Reduktionsquote für erreichbar, aber nicht in der bisherigen Zählweise. Wenn
projektspezifische Einmalteile in die Bezugsgröße eingehen, messen wir am Ende die Auftragslage und
nicht die Bereinigung. Ich bitte die Programmleitung, M-03 vor der nächsten Steuerungssitzung zu
bestätigen, damit wir nicht zwei Monate lang gegen eine Kennzahl arbeiten, die niemand halten kann.

Drittens ist der Termin Ende des ersten Quartals aus meiner Sicht bei der derzeitigen Beteiligung
nicht zu halten. Vier von acht Sitzungen mit halber Besetzung sind keine Abstimmung, sondern eine
Vorlage, der niemand widersprochen hat. Ich habe M-07 deshalb bewusst der Programmleitung zugeordnet.

O. Bensch, 18.02.2023
