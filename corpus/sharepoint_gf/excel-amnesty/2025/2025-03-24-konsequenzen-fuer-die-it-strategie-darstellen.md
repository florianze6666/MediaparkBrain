---
doc_id: LTT-20250324-IT-06
titel: "Excel Amnesty: Konsequenzen für die IT-Strategie"
dokumenttyp: Management Summary
datum: 2025-03-24
verfasser: Dr. Philipp Nowak
rolle: CIO
organisationseinheit: IT
empfaenger: [Geschäftsführung]
projekt: Excel Amnesty
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit, management]
ablageort: sharepoint_gf
---

# Excel Amnesty: Konsequenzen für die IT-Strategie

Management Summary für die Geschäftsführung

An: Dr. Eva Kessler, Markus Heine, Dr. Jens Mahlberg
Von: Dr. Philipp Nowak, CIO
Datum: 24. März 2025
Zeichen: IT/2025-014
Nachrichtlich: Gerd Sattler (Project Excellence Office), Andrea Faber (IT-Applikationen)

## Kernaussage

Die Meldephase der Excel Amnesty ist abgeschlossen. Registriert sind mehr als 430 Dateien, rund 60
davon haben wir als geschäftskritisch eingestuft. Ich lese dieses Ergebnis nicht als Befund über die
Disziplin der Belegschaft, sondern als Anforderungsliste an unsere Systemlandschaft. Jede dieser 60
Dateien trägt eine Funktion, die unsere Systeme heute nicht oder nicht brauchbar abdecken; sonst gäbe
es die Datei nicht. Die Konsequenz für die IT-Strategie ist deshalb kein zusätzliches Vorhaben,
sondern eine Reihenfolge: erst die Funktion beschreiben, dann das Trägersystem benennen, dann
ablösen. In dieser Reihenfolge sind wir bisher nie vorgegangen, und genau deshalb steht die Liste
heute vor uns.

Ich hatte mit rund 150 Meldungen gerechnet. Die Zahl habe ich deutlich unterschätzt.

## 1. Was die Meldung ergeben hat

Gemeldet wurden Dateien aus sieben Kategorien: Projektkalkulationen, Lieferterminlisten,
Ressourcenpläne, Inbetriebnahmechecklisten, Ersatzteilmatrizen, Angebotskonfiguratoren und
Berechnungstools. Die Kategorien sind nicht gleich stark besetzt; die größten Blöcke sind
Projektkalkulationen und Lieferterminlisten.

Als geschäftskritisch haben wir eine Datei eingestuft, wenn ihr Verlust oder ein unbemerkter Fehler
darin unmittelbar auf einen Kundentermin, eine Kalkulation oder eine Zusage durchschlägt. Bei einem
Teil dieser Dateien gibt es genau eine Person, die sie beherrscht, und keine Vertretung. Das ist die
Zahl, die mich an dem Ergebnis beunruhigt, nicht die 430.

Die Meldung war sanktionsfrei zugesagt. Diese Zusage ist die eigentliche Errungenschaft der
Initiative. Wir haben zum ersten Mal ein belastbares Bild davon, wo im Unternehmen tatsächlich
gearbeitet wird. Ein zweites Mal bekommen wir dieses Bild nur, wenn die erste Amnestie für die
Meldenden folgenlos geblieben ist.

## 2. Warum ein Abschaltprogramm nicht funktionieren wird

Seit der Übernahme in Eisenach 2018 kündigen wir an, lokale Excel- und Access-Lösungen abzulösen.
Diese Ankündigung ist in jeder Programmphase wiederholt worden, zuletzt in der Zielarchitektur des
damaligen ONE LTT. Abgeschafft hat sie keine einzige Datei. Abgelöst wurde immer nur das, wofür ein
Zielsystem produktiv, eingeführt und akzeptiert war.

Ich empfehle deshalb ausdrücklich, aus der Liste kein Abschaltprogramm mit Stichtag zu machen. Wer
eine Datei stilllegt, bevor ihre Funktion getragen wird, erzeugt keine Standardisierung, sondern eine
zweite Datei, die uns diesmal niemand meldet. Für die IT-Strategie leite ich daraus zwei Grundsätze
ab:

- Keine Ablösung ohne benanntes Trägersystem und benannten Termin.
- Für Dateien ohne Trägersystem: Bestandsschutz mit Auflagen statt Duldung ohne Regeln.

## 3. Die Liste zerfällt in drei sehr unterschiedliche Teile

**Erstens: Funktion ist im Zielsystem vorhanden, wird aber nicht genutzt.** Das betrifft vor allem
Projektkalkulationen und Ressourcenpläne. Beides ist im Projektcontrolling und in der
Ressourcenplanung nach POL-FIN-003 und POL-PM-003 abgebildet. Hier liegt kein Architekturproblem vor,
sondern ein Einführungs- und Vertrauensproblem: Die Projektleiter rechnen parallel, weil sie dem
Systemergebnis nicht trauen oder weil ihnen die letzte Rechenzeile fehlt. Das ist mein Thema, und
dafür brauche ich kein neues Programm, sondern Zugang zu den Projektleitern und die Bereitschaft,
Systemfelder nachzuziehen, statt die Datei zu verbieten.

**Zweitens: Funktion ist bewusst vertagt worden.** Inbetriebnahmechecklisten und Ersatzteilmatrizen
gehören in eine Serviceplattform, Angebotskonfiguratoren und Berechnungstools in die durchgängige
Verbindung von Konstruktion und Auftragsabwicklung. Beides ist beim Scope-Schnitt im Sommer 2024
bewusst zurückgestellt worden. Diese Dateien sind nicht die Folge einer Regelverletzung, sondern die
Folge einer Priorisierungsentscheidung. Sie jetzt abschaffen zu wollen, hieße, den Scope-Schnitt neu
zu verhandeln. Das ist eine Portfolioentscheidung der Geschäftsführung und keine IT-Frage, und ich
bitte darum, sie nicht implizit über eine Aufräumaktion zu treffen.

**Drittens: Funktion fehlt im Prozess, nicht im System.** Die Lieferterminlisten führen wir, weil die
Terminzusagen unserer Lieferanten überwiegend in Mails und Telefonaten entstehen und nirgends
systemseitig festgehalten werden. Solange das so ist, wird jede Liefertermin-Auswertung in einer
Datei nachgebaut. Der Hebel liegt hier in der Beschaffung, nicht in der Applikation.

## 4. Was ich mit dem Bestand tun will

Für alle als geschäftskritisch eingestuften Dateien schlage ich einen Mindeststandard vor, der ohne
neues System auskommt:

- benannter Owner und benannte Vertretung je Datei,
- Ablage in der digitalen Projektakte beziehungsweise auf SharePoint statt auf Netzlaufwerk oder im
  persönlichen Postfach,
- erkennbarer Versionsstand und Angabe, aus welchen Systemen die Datei ihre Daten zieht,
- Aufnahme in das Anwendungsverzeichnis der Informationssicherheit, das wir für die
  NIS2-Vorbereitung nach POL-IT-007 ohnehin aufbauen müssen,
- keine personenbezogenen Daten in diesen Dateien.

Zum Punkt Owner teile ich die Sorge, die der Gesamtbetriebsrat am 13. Februar protokolliert hat und
die ich in meiner Information vom 11. März aufgegriffen habe: Eine Owner-Rolle ohne Zeitbudget ist
eine zusätzliche Verpflichtung, die im Projektalltag als Erste liegen bleibt. Wir haben mit
BV-2025-01 gerade erst geklärt, dass Kennzahlen aus Systemen nicht zur Bewertung einzelner Personen
taugen. Eine Owner-Liste, die im Zweifel zeigt, wer eine kritische Datei unzureichend pflegt, führt
uns denselben Konflikt ein zweites Mal zu - und diesmal hätten wir ihn selbst gebaut. Der
Mindeststandard ist deshalb als Schutz des Owners zu formulieren, nicht als Nachweispflicht.

## 5. Einordnung in die Vorhabenlage 2025

Wir stabilisieren vor transformieren, und je Business Unit sind nur drei Top-Priority-Initiativen
zulässig. Ich beantrage kein viertes. Die 60 Dateien gehören verteilt auf das, was ohnehin läuft:
Projektkalkulation und Ressourcenplanung in den Digital Core, Angebotskonfiguratoren und
Berechnungstools in den Engineering Backbone, Inbetriebnahmechecklisten und Ersatzteilmatrizen in die
Service Transformation. Was dort in dieser Priorität nicht unterkommt, bleibt bewusst und
dokumentiert im Bestand - mit Auflagen, aber ohne Zieltermin.

Ich halte diesen Verzicht auf ein eigenes Vorhaben für richtig, will aber offen sagen, was er
bedeutet: Ein erheblicher Teil der Liste wird 2025 nicht angefasst. Wenn die Erwartung im Haus eine
andere ist, entsteht in einem Jahr der Eindruck, die Amnestie sei folgenlos geblieben, und das würde
die Bereitschaft zur nächsten Offenlegung beenden.

## 6. Was ich von der Geschäftsführung brauche

1. Eine Aussage, dass die gemeldeten Dateien nicht pauschal und nicht mit Stichtag abgeschaltet
   werden. Ohne diese Aussage ist die Zusage der Sanktionsfreiheit aus Sicht der Belegschaft
   gebrochen.
2. Zustimmung zur Zuordnung der 60 Dateien auf die drei laufenden Teilprogramme, abgestimmt mit den
   Business Units.
3. Ein Zeitbudget für die Owner-Rolle, in der Größenordnung eines halben Tages im Monat je
   geschäftskritischer Datei.
4. Eine Bestätigung, dass der Scope-Schnitt für Service und Engineering unverändert bleibt, oder
   andernfalls eine bewusste Neuentscheidung dazu.

Ich schlage vor, die Punkte 1 bis 3 in der Geschäftsführungssitzung im April zu behandeln. Zu Punkt 4
stehe ich für eine gesonderte Vorlage bereit.

Dr. Philipp Nowak
CIO
