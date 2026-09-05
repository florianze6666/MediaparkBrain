---
doc_id: LTT-20230307-IT-05
titel: Systemseitige Voraussetzungen der Umstellung
dokumenttyp: Management Summary
datum: 2023-03-07
verfasser: Andrea Faber
rolle: Leiterin IT-Applikationen
organisationseinheit: IT
empfaenger: [Programmleitung ONE LTT, Leitung IT]
projekt: ONE LTT
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [projektintern, bereichsintern]
ablageort: it_doku
---

Lahnberg Thermotechnik GmbH & Co. KG
IT - Applikationen, Kassel

Management Summary

Von: Andrea Faber, Leiterin IT-Applikationen
An: Programmleitung ONE LTT; Leitung IT
Datum: 7. März 2023
Betreff: ONE LTT - systemseitige Voraussetzungen der Umstellung
Einstufung: intern

## Anlass

Das Programm ONE LTT läuft seit Januar operativ. Der Implementierungspartner arbeitet in einem
Greenfield-Ansatz nach dem Leitsatz "Adopt before adapt". Seit der Eskalation vom 24. Februar wird
diskutiert, ob das Standardmodell zum Projektgeschäft passt. Diese Zusammenfassung greift dieser
Entscheidung nicht vor. Sie beschreibt, was auf der Systemseite unabhängig von ihrem Ausgang
vorliegen muss, bevor ein Umstellungstermin überhaupt geplant werden kann, und an welchen Stellen
diese Voraussetzungen heute nicht erfüllt sind.

## Ausgangslage

Wir betreiben zwei ERP-Systeme: in Kassel die proALPHA-Suite seit 2006, in Eisenach das
Infor-System, das mit der Übernahme 2018 dazugekommen ist. Das PLM wird faktisch von der
mechanischen Konstruktion genutzt; Elektrotechnik, Verfahrenstechnik und Projektmanagement arbeiten
daneben mit EPLAN, MS Project, Excel und Netzlaufwerken. Dazu kommt eine Zahl lokaler Access- und
Excel-Anwendungen, die wir nicht vollständig kennen - in Eisenach mehr als in Kassel, aber nicht nur
dort. Die Schnittstellen zwischen diesen Systemen sind über Jahre gewachsen. Wir betreiben sie
zuverlässig, eine gepflegte Gesamtübersicht gibt es nicht.

Das ist der Bestand, aus dem heraus umgestellt werden muss. Greenfield heißt nicht, dass dieser
Bestand verschwindet. Es heißt zunächst nur, dass daneben etwas Neues entsteht.

## 1. Stammdaten

Die Erhebung im Master-Data-Projekt zeigt konzernweit mehr als 180.000 Materialnummern, mit
Dubletten, projektspezifischen Einmalteilen, verschiedenen Benennungslogiken, unterschiedlichen
Einheiten und Altmaterialien ohne Sperrstatus. Das Ziel von zunächst 40 Prozent Reduktion aktiver
Materialstämme halte ich für erreichbar, aber nicht in der jetzigen Reihenfolge.

Zwei Punkte dazu. Erstens lässt sich nicht bereinigen, bevor das Zieldatenmodell steht. Klassifikation,
Nummernlogik, Einheiten und die Behandlung von Einmalteilen sind Teil genau der Prozessentscheidung,
die derzeit offen ist. Wer vorher bereinigt, bereinigt zweimal.

Zweitens sind Einmalteile im Projektgeschäft keine Datenfehler. Ein erheblicher Teil von ihnen ist
die unmittelbare Folge kundenspezifischer Auslegung. Ob wir sie künftig anders anlegen, ist eine
berechtigte Frage; als Bereinigungsmasse taugen sie nur begrenzt.

Was heute fehlt, ist eine benannte Verantwortung je Stammdatenobjekt - Material, Kunde, Lieferant,
Stückliste - mit Entscheidungsbefugnis. Ohne sie ist keine Bereinigung abnehmbar, weil niemand die
Abnahme unterschreiben kann.

## 2. Altsysteme, Datenübernahme, Abschaltung

Für jedes Altsystem brauchen wir drei Festlegungen, und zwar vor dem Aufbau, nicht danach.

- Umfang der Datenübernahme: welche Jahre, welche Belegarten, welche laufenden Projekte. Projekte mit
  mehrjähriger Laufzeit werden jeden realistischen Umstellungstermin überschreiten. Für sie ist zu
  klären, ob sie im Altsystem zu Ende geführt oder mitgenommen werden.
- Abschaltplan je System, einschließlich der Frage, was mit den aufbewahrungspflichtigen Daten
  geschieht. Ein lesender Archivzugriff über zehn Jahre ist keine Restarbeit, sondern eine eigene
  Lösung mit eigenem Aufwand. In der jetzigen Programmplanung sehe ich sie nicht.
- Erhebung der lokalen Access- und Excel-Anwendungen. Jede von ihnen enthält Prozesslogik, die
  nirgends beschrieben ist. Wird sie nicht vor der Abschaltung erhoben, entsteht sie nach der
  Umstellung neu, dann in neuen Excel-Dateien. Wir hätten die Schatten-IT damit nicht abgelöst,
  sondern verjüngt.

Ich schlage vor, diese Erhebung als eigenes Arbeitspaket im Programm zu führen und aus dem
Programmbudget zu finanzieren. Neben dem Tagesgeschäft kann meine Mannschaft sie nicht leisten.

## 3. Berechtigungen, Protokollierung, Zugänge

Das Rollenmodell nach POL-IT-001 v2.0 beschreibt die bestehende Landschaft über beide Standorte. Auf
die Zielarchitektur ist es nicht übertragbar; es muss entlang der Zielprozesse neu erarbeitet werden
und hängt damit an derselben offenen Entscheidung wie die Stammdaten.

Hinzu kommt die Mitbestimmung. Der Gesamtbetriebsrat hat im Dezember eine Rahmenvereinbarung für alle
Systeme des Programms verlangt, statt jede Einführung einzeln zu verhandeln; die Geschäftsführung hat
dem Verfahren zugestimmt, die Vereinbarung liegt noch nicht vor. Aus meiner Sicht ist das kein
Hindernis, sondern eine Terminfrage. Protokollierung, Auswertbarkeit und Reporting sind
Konfigurationsentscheidungen, die im Standard früh getroffen werden und später nur schwer
zurückzunehmen sind. Sie gehören deshalb in dieselbe Phase wie die Prozesskonzeption und nicht in die
Vorbereitung des Produktivstarts. Bei der Einführung der Kollaborationsplattform 2020 hat die kurze
Verhandlungszeit funktioniert, weil die Zweckbindung vorher klar war, nicht weil das Thema klein war.

Kurzfristig und praktisch: Die Zugänge der Berater sind nach der seit Januar geltenden Fassung der
Informationssicherheitsrichtlinie einzurichten. Das betrifft externe Zugriffe auf Produktivdaten der
Altsysteme im Rahmen der Datenanalysen und ist bei uns bereits laufender Aufwand.

## 4. Key User

Die Key User stehen anteilig zur Verfügung. Bei über 80 parallel laufenden Kundenprojekten und der
bekannten Engpasslage im Engineering bedeutet "anteilig" in der Praxis: nach dem Projektgeschäft.
Eine Benennung ohne Freistellung ist keine Verfügbarkeit.

Ich bitte um eine verbindliche Zusage je Prozessbereich, mit einer Tageszahl pro Woche und einer
benannten Vertretung. Wo das nicht darstellbar ist, sollte es so im Statusbericht stehen und nicht
über zusätzliche Abstimmungstermine aufgefangen werden. Sonst werden die Konzepte von denen
geschrieben, die Zeit haben, und nicht von denen, die den Prozess kennen.

## 5. Zum Standardmodell

Ob das Standardmodell des Implementierungspartners zum kundenspezifischen Projektgeschäft passt,
entscheide ich nicht. Die Beratung hält viele unserer Sonderprozesse für historisch gewachsene
Ineffizienzen, die Key User halten das Modell für auf Serienfertigung zugeschnitten. Beides kann in
Teilen zutreffen.

Systemseitig ist daran nur eines wichtig: Die Entscheidung muss vor der Festlegung des Datenmodells
fallen. Jede Woche, die sie offen bleibt, verschiebt Stammdatenbereinigung, Berechtigungskonzept und
Schnittstellenplanung mit, weil alle drei daran hängen. Eine späte Korrektur im Standard ist teurer
als eine frühe Entscheidung gegen ihn.

## Was ich bis wann brauche

| Punkt | Wer | Bis |
|---|---|---|
| Entscheidung über die Zielprozesse in Angebot, Projektabwicklung und Einmalteilen | Programmleitung, Process Owner | vor Festlegung des Datenmodells |
| Benannte Stammdatenverantwortliche je Objekt | Programmleitung mit den Fachbereichen | 31.03.2023 |
| Arbeitspaket Erhebung lokaler Anwendungen, mit Budget | Programmleitung | Q2 2023 |
| Verbindliche Key-User-Zusagen mit Tageszahl | Business Units und Zentralfunktionen | 31.03.2023 |
| Abstimmung zu Protokollierung und Auswertbarkeit | Programmleitung, HR, Datenschutz, Gesamtbetriebsrat | Q2 2023 |

## Offene Punkte

Der Umgang mit dem Eisenacher ERP ist nicht entschieden. Ob Eisenach in derselben Welle umgestellt
wird oder später, ändert Aufwand und Reihenfolge erheblich. Ich brauche dazu keine schnelle, aber
eine belastbare Aussage.

Zur Qualität der Bewegungsdaten in beiden Systemen liegt uns bisher nichts Belastbares vor. Wir
prüfen das derzeit und melden nach.

Andrea Faber
IT - Applikationen
