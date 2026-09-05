---
doc_id: LTT-20250116-IT-00
titel: "Projektauftrag: Erhebung geschäftskritischer Tabellen beauftragen"
dokumenttyp: Projektauftrag
datum: 2025-01-16
verfasser: Dr. Philipp Nowak
rolle: CIO
organisationseinheit: IT
empfaenger: "-"
projekt: IP-2025-01
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit, projektintern]
ablageort: it_doku
---

# Projektauftrag IP-2025-01

**Erhebung geschäftskritischer Tabellenanwendungen**

| | |
|---|---|
| Projektnummer | IP-2025-01 |
| Interne Kurzbezeichnung | Excel-Amnestie, Stufe 2 |
| Auftraggeber | Dr. Philipp Nowak, CIO |
| Projektleitung | Andrea Faber, Leiterin IT-Applikationen |
| Laufzeit | 20.01.2025 bis 30.04.2025 |
| Fassung | 1.0 vom 16.01.2025 |
| Ablage | IT-Dokumentation, gelenkt nach POL-QM-001 |

## 1 Ausgangslage

Die IT hat im vierten Quartal 2024 dazu aufgerufen, selbstgebaute Tabellenlösungen zu melden, die im
laufenden Betrieb tatsächlich gebraucht werden. Der Aufruf war ausdrücklich sanktionsfrei: Wer meldet,
muss weder eine Abschaltung noch eine Rückfrage danach erwarten, warum die Datei überhaupt entstanden
ist. Der Rücklauf ist zum Jahreswechsel geschlossen worden. Gemeldet wurden mehr als 430 Dateien.

Das ist deutlich mehr, als die Applikationsbetreuung erwartet hatte. In einer ersten Sichtung wurden
60 dieser Dateien als geschäftskritisch eingestuft, das heißt: Bei Ausfall oder Verlust steht ein
laufender Prozess innerhalb weniger Tage. Sie verteilen sich auf sieben Kategorien.

| Kategorie | als geschäftskritisch eingestuft |
|---|---:|
| Projektkalkulationen | 14 |
| Berechnungstools | 11 |
| Lieferterminlisten | 9 |
| Inbetriebnahmechecklisten | 8 |
| Ressourcenpläne | 7 |
| Ersatzteilmatrizen | 6 |
| Angebotskonfiguratoren | 5 |
| Summe | 60 |

Der Befund als solcher ist nicht neu. Lokale Tabellen- und Datenbanklösungen sind seit der
Zusammenführung der beiden Standorte 2018 bekannt und mehrfach beschrieben worden. Neu ist allein,
dass wir sie einzeln benennen können statt sie als Kategorie zu beklagen.

Ebenso festzuhalten: Die Annahme, ein einheitliches ERP nehme diese Lösungen im Vorbeigehen mit, hat
sich nicht bestätigt. Die im Oktober produktiv gegangenen Umfänge Finance und Procurement des Digital
Core haben an keiner der sieben Kategorien etwas geändert. Wer eine Ablösung plant, ohne vorher zu
wissen, was die einzelne Datei leistet, plant sie ein zweites Mal an der Sache vorbei.

## 2 Zielsetzung

Das Projekt erstellt eine einzeln geprüfte Bestandsaufnahme der 60 als geschäftskritisch eingestuften
Anwendungen und liefert:

1. ein Register mit einem einheitlichen Datensatz je Anwendung,
2. eine Bewertung nach Ausfallwirkung und nach Ablösbarkeit,
3. eine Empfehlung, welche Anwendung in ein bestehendes System gehört, welche als Fachanwendung
   abzusichern ist und welche dauerhaft lokal bleiben darf.

Das Ergebnis ist die Entscheidungsgrundlage. Die Entscheidung selbst trifft dieses Projekt nicht.

## 3 Abgrenzung

Nicht Gegenstand dieses Auftrags sind:

- die Abschaltung, Sperrung oder Einschränkung einer gemeldeten Datei,
- der Start eines Ablösungs- oder Migrationsvorhabens,
- die Bewertung der Arbeitsweise einzelner Bereiche oder Personen,
- die Beschaffung eines Werkzeugs,
- die inhaltliche Prüfung der lokalen Access-Datenbanken. Sie werden gezählt und mit Standort und
  Kategorie vermerkt, mehr nicht.

Die Punkte stehen hier nicht als Formalie. Die Zusage der Sanktionsfreiheit ist der einzige Grund,
warum wir 430 statt 40 Dateien kennen.

## 4 Leistungsumfang

**AP1 - Erhebungsraster.** Ein Datensatz je Anwendung, einheitlich für alle Kategorien: Bezeichnung,
Ablageort, fachlicher Ansprechpartner mit Rolle, Nutzerkreis, Datenquellen, Zielsysteme,
Aktualisierungsfrequenz, Anteil an Makros und Formelwerk, Angaben zu einzelnen Beschäftigten ja/nein,
Abhängigkeit von einer einzelnen Person, Wirkung eines Ausfalls, geschätzte Ablösbarkeit,
Prüfvermerk. Abstimmung mit Oliver Bensch, soweit Stammdaten aus dem ERP einfließen.

**AP2 - Erhebung.** Je Anwendung ein Termin mit dem fachlichen Ansprechpartner, höchstens 90 Minuten,
Aufnahme durch die Applikationsbetreuung. Die Datei wird gemeinsam geöffnet und besprochen, nicht aus
der Ferne beurteilt.

**AP3 - Sicht der Informationssicherheit.** Sven Bruckner bewertet Ablage, Zugriffsschutz, Sicherung
und Wiederanlauf. Bezug: POL-IT-002 in der Fassung vom Januar und POL-IT-007. Eine Anwendung, deren
Ausfall einen Prozess anhält, deren Datei aber nur auf einem persönlichen Ablageort liegt, ist ein
Punkt für die Betroffenheitsanalyse und nicht nur ein Ordnungsthema.

**AP4 - Bewertung.** Einordnung jeder Anwendung in eine von vier Klassen: gehört in den Digital Core,
gehört in den Engineering Backbone, gehört in die Service Transformation, bleibt lokal und wird
abgesichert. Für die vierte Klasse ist zu benennen, was Absicherung konkret heißt.

**AP5 - Bericht.** Bericht mit Register, Bewertung und Empfehlung, vorgelegt an mich.

## 5 Meilensteine

| M | Termin | Inhalt |
|---|---|---|
| M1 | 20.01.2025 | Projektstart, Erhebungsraster abgestimmt |
| M2 | 07.02.2025 | Unterrichtung des Gesamtbetriebsrats erfolgt |
| M3 | 14.03.2025 | Erhebung der 60 Anwendungen abgeschlossen |
| M4 | 04.04.2025 | Bewertung abgeschlossen |
| M5 | 30.04.2025 | Bericht und Empfehlung vorgelegt |

M2 liegt vor dem Beginn der Gespräche. Das ist beabsichtigt.

## 6 Projektorganisation und Mitwirkung

Projektleitung: Andrea Faber. Erhebung durch die Applikationsbetreuung.

Fachliche Ansprechpartner je Kategorie:

| Kategorie | Bereich |
|---|---|
| Projektkalkulationen, Ressourcenpläne | Project Excellence Office, Gerd Sattler; kalkulatorische Anteile mit Dieter Anselm |
| Lieferterminlisten | Supply Chain, Ulrich Damm |
| Inbetriebnahmechecklisten, Ersatzteilmatrizen | Lifecycle & Service, Michael Aurich, Elke Sandmann |
| Angebotskonfiguratoren | Vertrieb, Jana Ostermann |
| Berechnungstools | Central Engineering, Dr. Ingrid Sommer |

Weiter beteiligt: Bernd Hoffmann für Fragen der Dokumentenlenkung, Sabine Kroll, sobald eine
Anwendung Angaben zu einzelnen Beschäftigten enthält, Oliver Bensch für den Stammdatenbezug.

Die Mitwirkung der Fachbereiche ist der knappe Teil des Vorhabens, nicht die IT-Kapazität. Deshalb
die feste Obergrenze von 90 Minuten je Anwendung und die Terminierung in Blöcken.

## 7 Aufwand und Budget

| Position | Umfang |
|---|---|
| IT, Applikationsbetreuung und Informationssicherheit | rund 25 Personentage |
| Fachbereiche | rund 40 Personentage |
| externe Unterstützung, ausschließlich Berechnungstools | bis 20.000 EUR, optional |

Der externe Anteil wird nur abgerufen, wenn sich in AP2 zeigt, dass die Auslegungsgrundlagen der
Berechnungstools nicht ohne Weiteres nachvollziehbar sind; die Freigabe behalte ich mir vor. Eine
Investitionsvorlage nach POL-FIN-002 ist nicht erforderlich, das Vorhaben liegt weit unterhalb der
Schwelle von 2 Mio EUR und wird im IT-Budget 2025 geführt.

## 8 Randbedingungen und Auflagen

**8.1 Die Sanktionsfreiheit gilt fort.** Aus einer Meldung entsteht kein Nachteil, weder für den
Melder noch für den Bereich. Im Projektzeitraum wird keine gemeldete Datei abgeschaltet oder
eingeschränkt. Sollte die Informationssicherheit einen Fall finden, der sofort zu behandeln ist,
gehen wir ihn mit dem Bereich an und nicht über eine Sperrung.

**8.2 Personenbezug.** Erfasst wird der fachliche Ansprechpartner mit Rolle und Organisationseinheit,
weil eine Anwendung ohne Ansprechpartner nicht erhebbar ist. Auswertungen und Bericht erfolgen
ausschließlich auf Ebene Kategorie und Organisationseinheit. Es gibt keine Aufstellung je Person,
keine Zählung von Dateien je Beschäftigtem und keine Nutzungsstatistik.

**8.3 Unterrichtung des Gesamtbetriebsrats.** Nach meiner Einschätzung führen wir kein System ein und
ändern keines, sodass eine Teilvereinbarung nach BV-2023-01 nicht erforderlich ist. Ich will die Frage
trotzdem vor Beginn der Gespräche geklärt haben. Mehrere der erhobenen Kategorien, namentlich
Ressourcenpläne und Inbetriebnahmechecklisten, enthalten Angaben zu einzelnen Beschäftigten, und wir
haben die Auseinandersetzung über die Personenbeziehbarkeit von Projektdaten erst im November beim
Projekt-Dashboard geführt. Sie im März ein zweites Mal zu führen, mitten in der Erhebung, würde uns
den Zeitplan kosten. Frau Faber stimmt den Termin mit Frau Kirchner ab; ich nehme selbst teil.

**8.4 Verhältnis zur Vorhabensteuerung.** Das Vorhaben ist eine zentrale Bestandsaufnahme und belegt
keinen der drei Plätze, die einer Business Unit nach POL-ORG-001 zustehen. Es verbraucht dennoch
Fachbereichskapazität. Der enge Zeitrahmen und die Obergrenze je Termin sind die Gegenleistung dafür.

**8.5 Ergebnisablage.** Register und Bericht werden in der IT-Dokumentation geführt und nach
POL-QM-001 gelenkt.

## 9 Risiken

| Risiko | Wirkung | Maßnahme |
|---|---|---|
| Die Zusage der Sanktionsfreiheit wird angezweifelt | keine weiteren Meldungen, der Rest der 430 bleibt im Dunkeln | Wortlaut der Zusage in der Ankündigung wiederholen, keine Abschaltung im Projektzeitraum |
| Fachbereiche stellen die Ansprechpartner nicht frei | Erhebung verschiebt sich | feste Zeitfenster, Eskalation an mich nach zwei ausgefallenen Terminen |
| Berechnungstools ohne nachvollziehbare Auslegungsgrundlage, deren Ergebnisse in Angebote eingehen | offene Frage zu Qualität und Verantwortung | Klärung mit Central Engineering und Qualitätsmanagement, bei Bedarf eigener Prüfauftrag außerhalb dieses Projekts |
| Die Erhebung wird als angekündigte Ablösung gelesen | Abwehr statt Auskunft | Abgrenzung nach Abschnitt 3 in jeder Einladung mitschicken |

## 10 Freigabe und offene Punkte

Ich erteile den Auftrag hiermit in der Fassung 1.0.

Offen bleiben zwei Punkte, die mit dem Bericht zu entscheiden sind: die Zuordnung der Berechnungstools,
die fachlich zwischen Central Engineering und dem Engineering Backbone liegen, und die Frage, ob die
rund 370 nicht als geschäftskritisch eingestuften Dateien überhaupt weiterverfolgt werden. Ich neige
dazu, sie liegen zu lassen, will die Entscheidung aber auf der Grundlage der Erhebung treffen und
nicht davor.

Anmerkung zur Tabelle in Abschnitt 1: Die Zahlen stammen aus der ersten Sichtung und werden sich mit
der Erhebung verschieben. Ich habe sie trotzdem aufgenommen, damit wir im April sehen, wie weit die
erste Einschätzung getragen hat.

Kassel, 16.01.2025

Dr. Philipp Nowak
CIO
