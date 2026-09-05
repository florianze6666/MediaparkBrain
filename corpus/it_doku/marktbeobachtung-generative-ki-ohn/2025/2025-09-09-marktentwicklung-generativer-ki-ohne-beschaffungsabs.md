---
doc_id: LTT-20250909-IT-00
titel: "Software-Evaluation: Marktentwicklung generativer KI ohne Beschaffungsabsicht beobachten"
dokumenttyp: Software-Evaluation
datum: 2025-09-09
verfasser: Dr. Philipp Nowak
rolle: CIO
organisationseinheit: IT
empfaenger: ["-"]
projekt: "-"
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [bereichsintern, management]
ablageort: it_doku
---

# Marktbeobachtung generative KI - Stand September 2025, ohne Beschaffungsabsicht

Lahnberg Thermotechnik GmbH & Co. KG, IT
Erstellt am 09.09.2025 von Dr. Philipp Nowak, CIO
Ablage: IT-Dokumentation / Marktbeobachtung
Status: Beobachtung. Kein Beschaffungsvorgang, keine Evaluierung im Sinne von POL-IT-003.
Bezug: POL-IT-002 v3.0, POL-IT-003 v2.0, POL-IT-005 v1.0, POL-IT-007 v1.0, BV-2023-01

## 1 Anlass und Abgrenzung

Seit dem Frühjahr häufen sich zwei Arten von Anfragen: Anbieter aus unserem eigenen Bestand kündigen
Assistenzfunktionen an und bitten um Gesprächstermine, und aus den Fachbereichen kommt in
unterschiedlicher Formulierung die Frage, ob LTT "etwas mit KI macht". Beides habe ich bisher einzeln
beantwortet. Diese Notiz hält den Stand einmal fest, damit die Antwort nicht davon abhängt, wer wen
zuletzt gefragt hat.

Was diese Notiz nicht ist: kein Auftrag, keine Vorauswahl, keine Anbieterbewertung nach POL-IT-003,
keine Vorbereitung einer Investitionsvorlage nach POL-FIN-002. Es gibt zu diesem Thema bei LTT keinen
Vorgang. Es gibt keine Testlizenz, keine Pilotinstallation und kein Budget. Wer diese Notiz später
liest, soll das nicht anders verstehen, als es hier steht.

Nicht Gegenstand sind Rechen- und Auslegungsverfahren in Simulation und Engineering. Die laufen seit
Jahren und haben mit dem hier beschriebenen Markttrend nichts zu tun, auch wenn im Sprachgebrauch
inzwischen alles KI heißt.

## 2 Was sich am Markt beobachten lässt

Ich unterscheide zwei Bewegungen, die im Marketing gern vermischt werden.

Erstens eigenständige Produkte: Textassistenten, Dokumentensuche über eigene Ablagen, Übersetzung,
Programmierunterstützung. Sie werden als separate Anwendung beschafft, verlangen einen eigenen
Zugriffsweg auf unsere Daten und wären damit ein normaler Beschaffungs- und Sicherheitsvorgang.

Zweitens - und das ist für uns der relevantere Teil - Assistenzfunktionen, die unsere vorhandenen
Anbieter in ihre Standardprodukte einbauen. Microsoft in der Kollaborations- und Office-Umgebung und
im CRM, SAP in der ERP- und Beschaffungssuite, Siemens in der Engineering-Umgebung. Diese Funktionen
kommen nicht über eine Beschaffungsentscheidung ins Haus, sondern über einen Releasewechsel und einen
Lizenzbaustein. Genau darin liegt der Unterschied zu jeder Softwareeinführung, die wir bisher
gemacht haben.

Zur Preisseite kann ich wenig Belastbares sagen. Die Modelle sind überwiegend Zusatzlizenzen je
Nutzer und Monat auf bestehende Verträge. Listenpreise sind öffentlich, unsere tatsächlichen
Konditionen entstünden erst in einer Verhandlung, und die führe ich nicht. Wer eine Zahl für einen
Business Case braucht, bekommt von mir derzeit keine.

Die beworbenen Anwendungsfälle sind quer über die Anbieter ähnlich: Suchen und Zusammenfassen von
Dokumenten, Entwürfe für Schriftverkehr, Vorqualifizierung von Servicetickets, Codeunterstützung.
Die Vorführungen laufen auf sauberen Daten. Das ist keine Unterstellung, das ist der Zweck einer
Vorführung.

## 3 Bezug zur eigenen Systemlandschaft

Unsere Projektinformation liegt verteilt: Dokumente in der SharePoint-Umgebung und weiterhin in
erheblichem Umfang auf gewachsenen Netzlaufwerken, kaufmännische Projektdaten seit dem ERP-Start im
Oktober 2024 im Digital Core, technische Daten in der PLM-Plattform, Serviceunterlagen zu einem
guten Teil unstrukturiert. Dazwischen liegen Medienbrüche, die wir kennen und in den laufenden
Programmen Stück für Stück abarbeiten.

Aus der Excel Amnesty haben wir mehr als 430 gemeldete Dateien, davon rund 60 als geschäftskritisch
eingestuft. Ein Assistenzsystem, das über unsere Ablagen sucht, findet als Erstes genau diese
Landschaft. Es findet drei Versionen derselben Kalkulation, es findet die abgelöste
Lieferterminliste neben der gültigen, und es unterscheidet beide nicht, weil wir sie selbst nur an
der Person unterscheiden, die sie pflegt. Meine Position dazu ist unverändert: die interessante
Frage ist nicht, was ein solches System kann, sondern was wir ihm vorlegen würden.

Der zweite Punkt ist das Berechtigungsmodell. Ein Assistent arbeitet mit den Rechten des Nutzers.
Das klingt harmlos und ist es an den Stellen, an denen unser Rollenkonzept nach POL-IT-001 v3.0
greift. An den historisch gewachsenen Freigaben auf den alten Laufwerken ist es das nicht. Was heute
niemand findet, weil er den Pfad nicht kennt, wäre dann auffindbar. Das ist kein Argument gegen die
Technik, sondern eine Aufgabe, die wir ohnehin haben und die dadurch dringender würde.

## 4 Rahmenbedingungen, die unabhängig von jeder Produktwahl gelten

BV-2023-01 verlangt für jedes System mit Bezug zu personenbezogenen Daten Unterrichtung,
Systembeschreibung mit Datenkatalog und eine Teilvereinbarung vor Produktivsetzung. Nach meinem
Verständnis ist eine Assistenzfunktion, die in einem bereits vereinbarten System nachträglich
aktiviert wird, nicht automatisch von der Teilvereinbarung dieses Systems gedeckt. Ich habe das
bewusst nicht zur Klärung gestellt, weil es nichts zu klären gibt, solange nichts eingeführt wird.
Sobald sich das ändert, ist es der erste Schritt und nicht der letzte.

BV-2020-02 schließt jede Auswertung personenbezogener Nutzungsdaten der Kollaborationsplattform aus.
Funktionen, die Besprechungen zusammenfassen oder Kommunikationsverläufe auswerten, berühren diese
Vereinbarung unmittelbar und nicht am Rand.

Datenschutzrechtlich habe ich mit Frau Kroll bisher nur allgemein gesprochen. Eine belastbare
Einschätzung zur Verarbeitung unserer Dokumente durch einen Anbieterdienst liegt nicht vor und wäre
ohne konkreten Anwendungsfall auch nicht sinnvoll einzuholen.

POL-IT-003 v2.0 verlangt Anbieterbewertung, Exit-Fähigkeit und Vorgaben zur Datenhaltung. Die
Exit-Fähigkeit ist bei einer Funktion, die im Standardprodukt mitläuft, praktisch nicht herstellbar:
wir könnten sie abschalten, aber nicht ersetzen. Wer sie in Arbeitsabläufe einbaut, erhöht die
Abhängigkeit von einem Anbieter, mit dem wir ohnehin schon eng verbunden sind.

Nach POL-IT-007 und POL-IT-002 v3.0 gehört ein Dienst, der unsere Dokumente verarbeitet, in die
Betrachtung der Lieferkettensicherheit. Das ist keine Besonderheit dieses Themas, sondern die
normale Folge unserer NIS2-Betroffenheit.

## 5 Was ich nicht beurteilen kann

Zum Nutzen gibt es weder eine eigene Messung noch belastbare Zahlen aus dem Markt, die auf den
Anlagenbau übertragbar wären. Anbieterangaben zur Zeitersparnis beziehen sich in der Regel auf
Büroarbeit mit hohem Textanteil. Wie sich ein solches System bei deutschsprachiger technischer
Dokumentation mit unserer Terminologie, unseren Abkürzungen und unseren Anlagenbezeichnungen
verhält, weiß ich nicht.

Zum Aufwand ebenso wenig. Ohne Aussage über die Datenbasis ist jede Aufwandsschätzung eine Zahl ohne
Grundlage.

Was ich einschätzen kann, ist der Preis einer enttäuschten Erwartung. Den haben wir in den letzten
Jahren bezahlt, und die Organisation erinnert sich daran genauer als an jedes Zielbild.

## 6 Vorgehen bis auf Weiteres

Die IT beobachtet und dokumentiert, mehr nicht. Zwei Dinge tun wir aktiv:

Bei jedem Releasewechsel unserer Standardprodukte verlangen wir vom Anbieter eine Aussage, ob
Assistenzfunktionen enthalten sind, ob sie standardmäßig aktiv sind und wie sie abgeschaltet werden.
Das ist der einzige Weg, auf dem uns dieses Thema ohne Entscheidung erreichen kann, und das halte
ich für den derzeit dringlichsten Punkt.

Anfragen aus den Fachbereichen laufen über IT-Applikationen. Die Antwort lautet bis auf Weiteres:
kein Vorgang, keine Testinstallation, keine Anbieterkontakte mit Beschaffungscharakter über die IT
hinaus.

Zur Einordnung, weil die Frage sicher kommt: die drei Top-Priority-Change-Initiatives je Business
Unit sind vergeben, Digital Core, Engineering Backbone und Service Transformation binden die
Kapazität, die wir haben. Ich habe für dieses Thema keine freien Leute und würde sie in diesem Jahr
auch nicht beantragen. Für unsere Projektberichterstattung sehe ich am Markt ohnehin nichts, was
über das Zusammenfassen vorhandener Berichte hinausginge, und unser Problem sind nicht die Berichte,
sondern die Daten darunter.

Ich schreibe diese Notiz fort, wenn sich am Markt oder an unserer Lage etwas ändert.

Nowak
