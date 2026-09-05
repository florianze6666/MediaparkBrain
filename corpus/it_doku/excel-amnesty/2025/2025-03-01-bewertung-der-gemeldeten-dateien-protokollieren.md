---
doc_id: LTT-20250301-IT-04
titel: Bewertung der gemeldeten Dateien aus der Excel Amnesty
dokumenttyp: Meeting Minutes
datum: 2025-03-01
verfasser: Andrea Faber
rolle: Leiterin IT-Applikationen
organisationseinheit: IT
empfaenger: [Teilnehmer, IT-Leitung]
projekt: Excel Amnesty
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [bereichsintern, projektintern]
ablageort: it_doku
---

**Besprechung:** Excel Amnesty - Bewertung der gemeldeten Dateien, zweiter Durchgang
**Datum/Zeit:** Donnerstag, 27.02.2025, 09:00 bis 11:30 Uhr
**Ort:** Kassel, Besprechungsraum Fulda, Teams-Zuschaltung Eisenach
**Protokoll:** A. Faber, IT-Applikationen (Fassung vom 01.03.2025)

**Teilnehmer:** A. Faber (Leitung, IT-Applikationen), O. Bensch (ERP und Stammdaten), G. Sattler
(Project Excellence Office), M. Gehrke (Konstruktion mechanisch), E. Sandmann (Servicedisposition),
S. Bruckner (Informationssicherheit), D. Anselm (Controlling), Dr. P. Nowak (CIO, zu TOP 1 und 2)
**Entschuldigt:** S. Kroll (Datenschutz), U. Damm (Supply Chain)
**Verteiler:** Teilnehmer, Entschuldigte

---

## TOP 1 - Meldestand

Das Meldefenster ist zum 31.01.2025 geschlossen. Registriert sind 434 Meldungen, nach Bereinigung
von Doppel- und Mehrfachmeldungen 423 unterschiedliche Dateien. 60 davon sind im ersten Durchgang
als geschäftskritisch eingestuft worden. Die Meldungen liegen in der Liste auf SharePoint, die
Bewertung ist dort spaltenweise dokumentiert.

Faber weist darauf hin, dass die Meldung sanktionsfrei zugesagt wurde und diese Zusage unabhängig
vom weiteren Vorgehen gilt. Wer eine Datei gemeldet hat, hat damit die Anforderung erfüllt.

Nowak: Die Zahl liegt über der Erwartung und ist als Ergebnis zu werten, nicht als Vorwurf. Der
Bestand ist über Jahre entstanden.

Der Sachverhalt ist im Risikoregister vom 16.02.2025 als Risiko geführt.

## TOP 2 - Bewertungsraster

Angewandt wurden fünf Kriterien, gleichgewichtet, dreistufig bewertet:

1. Auswirkung eines Fehlers oder Ausfalls auf Termin, Kosten oder Qualität eines laufenden Auftrags
2. Zahl der abhängigen Prozesse und Bereiche
3. Ersetzbarkeit durch eine heute vorhandene Systemfunktion
4. Nachvollziehbarkeit: Versionsstand, Ablageort, Freigabe
5. personelle Abhängigkeit, also ob die Datei ohne eine bestimmte Person weiter nutzbar ist

Geschäftskritisch ist eine Datei, die bei Kriterium 1 die höchste Stufe erreicht oder bei den
Kriterien 2 und 5 gemeinsam. Bruckner merkt an, dass Kriterium 4 in der Praxis fast durchgängig
schlecht abschneidet und deshalb wenig trennt. Wird für den nächsten Durchgang berücksichtigt.

## TOP 3 - Ergebnis nach Kategorien

| Kategorie | geschäftskritisch | Hauptbefund |
|---|---:|---|
| Projektkalkulationen | 14 | teilweise Parallelrechnung zum Projektcontrolling, abweichende Zuschlagssätze |
| Berechnungstools | 11 | Auslegungs- und Nachrechnungstools, über Jahre gewachsen, keine Freigabehistorie |
| Angebotskonfiguratoren | 9 | Preis- und Variantenlogik ausserhalb jedes Systems |
| Lieferterminlisten | 8 | Abgleich zwischen Bestellbestätigung und Baustellentermin, Medienbruch |
| Ersatzteilmatrizen | 7 | Zuordnung Anlage zu Ersatzteil, offline im Serviceeinsatz genutzt |
| Ressourcenpläne | 6 | Personenplanung je Bereich, parallel zur Projektcontrolling-Sicht |
| Inbetriebnahmechecklisten | 5 | Prüfschritte und Abnahmestände, teils kundenspezifisch |
| **Summe** | **60** | |

Die Grenze ist nicht scharf. Drei weitere Dateien sind strittig und in der Liste als offen markiert.

## TOP 4 - Diskussion

Faber: Die 60 Dateien sind nicht ein Problem, sondern drei. Erstens Dateien, die eine Funktion
nachbilden, die es inzwischen im System gibt - hier geht es um Umgewöhnung. Zweitens Dateien, die
eine Lücke zwischen zwei Systemen überbrücken; die verschwinden nicht, solange die Lücke bleibt.
Drittens Dateien, die Fachwissen enthalten, das nie in einem System stand. Wer alle drei Gruppen
gleich behandelt, wird bei keiner fertig. Aus Sicht der Applikationsbetreuung ist ausserdem
festzuhalten: Die Ablösung lokaler Excel-Lösungen ist seit 2018 mehrfach angekündigt und in keinem
Anlauf abgeschlossen worden. Eine Liste allein ändert daran nichts, und die Anwendungsbetreuung kann
60 Ablösungen weder parallel begleiten noch mit dem heutigen Personalstand betreuen.

Bensch: Bei den Projektkalkulationen ist zunächst zu klären, welche Rechnung führend ist. Wenn im
Projekt eine Excel-Kalkulation gepflegt wird und im System eine zweite, ist nicht die Datei das
Problem, sondern dass zwei Zahlen existieren. Vorschlag, die 14 Fälle gegen die Auswertungen im
Projektcontrolling zu stellen, bevor über Ablösung gesprochen wird.

Anselm unterstützt das und ergänzt, dass abweichende Zuschlagssätze in der Nachkalkulation seit
Jahren auffallen. Er hält den Abgleich für dringender als die Frage nach dem Werkzeug.

Sattler: Für Ressourcenpläne gibt es mit dem Projektcontrolling und dem Projekt-Dashboard eine
vorgesehene Sicht. Aus Sicht des Project Excellence Office sollten diese sechs Dateien nicht
weitergeführt werden. Faber hält dagegen, dass die gemeldeten Pläne auf Namen und Wochen laufen,
die Systemsicht dagegen auf Rollen und Monate; das ist keine Formatfrage.

Gehrke widerspricht der Einordnung der Berechnungstools als Schattenanwendung deutlich. Die Tools
enthalten Auslegungsannahmen und Korrekturfaktoren aus Projekten seit den frühen Jahren, teilweise
gegen Messwerte aus der Inbetriebnahme abgeglichen. Er will sie als Engineering-Werkzeuge geführt
sehen, mit Freigabe und Versionsstand, aber ohne Ablösungsauftrag. Zur Kenntnis genommen; die
Einordnung ist offen.

Sandmann: Ersatzteilmatrizen und Inbetriebnahmechecklisten werden im Einsatz beim Kunden genutzt,
häufig ohne belastbare Netzverbindung. Eine Lösung ohne Offline-Fähigkeit ersetzt sie nicht,
sondern erzeugt eine zweite Datei neben der ersten.

Bruckner: Von den 60 Dateien liegen 22 auf persönlichen Laufwerken oder lokal auf Endgeräten, ohne
Sicherung und ohne Zugriffsschutz. Mehrere enthalten Kundenpreise und Lieferantenkonditionen.
Unabhängig von der Frage, was mit den Dateien geschieht, ist die Ablage kurzfristig zu bereinigen.
Kein Widerspruch.

Zur Owner-Zuweisung: In der Liste ist zu jeder Datei eine Person genannt. Faber weist darauf hin,
dass daraus eine namentliche Auswertung entstehen kann und die Zuweisung mit der Datenschutz-
beauftragten zu klären ist. Der Gesamtbetriebsrat hat am 13.02.2025 protokolliert, dass die
Owner-Zuweisung nicht als zusätzliche Verpflichtung ohne Zeitbudget ausgestaltet werden soll. Der
Punkt wird in die Vorlage aufgenommen.

Lieferterminlisten konnten ohne Supply Chain nicht abschliessend besprochen werden. Separater
Termin erforderlich.

## TOP 5 - Handlungsoptionen, keine Festlegung

Skizziert wurden drei Optionen, ohne Bewertung und ohne Beschluss:

- A: Ablösung in Wellen nach Kritikalität, mit fester Reihenfolge und benanntem Aufwand
- B: Duldung mit Auflagen - gelenkte Ablage, Versionsstand, benannte Vertretung, jährliche Prüfung
- C: Einordnung als reguläres Werkzeug für die Fälle, in denen kein System die Funktion abbildet

Die Optionen schliessen einander nicht aus und werden voraussichtlich je Kategorie unterschiedlich
zu beantworten sein. Eine Entscheidung ist heute ausdrücklich nicht getroffen worden. Die Vorlage
für die Geschäftsführung wird von IT-Applikationen entworfen; Aufwand und Betreuungsbedarf sind
darin auszuweisen, damit die Entscheidung nicht ohne Ressourcenaussage fällt.

## Maßnahmen

| Nr | Maßnahme | Verantwortlich | Termin |
|---:|---|---|---|
| 1 | Sicherung der 22 ungeschützt abgelegten Dateien auf gelenkte Ablage, Backup und Zugriffsschutz | Faber, Bruckner | 14.03.2025 |
| 2 | Abgleich der 14 Projektkalkulationen mit den Auswertungen im Projektcontrolling | Bensch, Anselm | 14.03.2025 |
| 3 | Vorschlag zur Einordnung der Berechnungstools, mit Freigabe- und Versionsregel | Gehrke | 21.03.2025 |
| 4 | Offline-Anforderungen aus Service und Inbetriebnahme zusammenstellen | Sandmann | 21.03.2025 |
| 5 | Klärung der Owner-Zuweisung mit Datenschutz, Rückmeldung an den Gesamtbetriebsrat vorbereiten | Faber, Kroll | 21.03.2025 |
| 6 | Sondertermin Lieferterminlisten mit Supply Chain | Faber, Damm | 21.03.2025 |
| 7 | Entwurf der Entscheidungsvorlage einschliesslich Aufwandsschätzung | Faber | 28.03.2025 |

**Nächster Termin:** Donnerstag, 20.03.2025, 09:00 Uhr, gleicher Kreis.

Einwendungen zum Protokoll bitte bis 07.03.2025 an IT-Applikationen.
