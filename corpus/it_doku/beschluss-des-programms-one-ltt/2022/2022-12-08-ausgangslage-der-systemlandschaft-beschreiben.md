---
doc_id: LTT-20221208-IT-05
titel: Ausgangslage der Systemlandschaft vor dem Start von Project Atlas
dokumenttyp: Management Summary
datum: 2022-12-08
verfasser: Karin Löbner
rolle: Leiterin IT
organisationseinheit: IT
empfaenger: [Geschäftsführung]
projekt: IP-2022-03
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [bereichsintern, management]
ablageort: it_doku
---

# Ausgangslage der Systemlandschaft vor dem Start von Project Atlas

Management Summary

Von: Karin Löbner, Leiterin IT
An: Geschäftsführung
Verteiler: Kessler, Heine, Mahlberg, Sattler (PMO), Faber (IT-Applikationen), Bruckner (Informationssicherheit)
Datum: 8. Dezember 2022
Aktenzeichen: IT/2022-118

## Anlass

Mit dem Grundsatzbeschluss vom November steht der Rahmen für ONE LTT: 14,8 Mio EUR über drei Jahre,
neun Bausteine, intern als Project Atlas geführt. Der Umsetzungsansatz wird derzeit festgelegt. Diese
Zusammenfassung beschreibt, worauf das Programm technisch aufsetzt, und benennt die Punkte, die vor
dieser Festlegung geklärt sein sollten. Sie ergänzt das Risikoregister vom 26.11.2022 und wiederholt
es nicht.

## Kernaussage

1. Sechs der neun Bausteine sind Neueinführungen und keine Ablösungen. Wir betreiben heute kein CRM,
   kein MES, kein Data Warehouse, keine eigenständige Reporting-Schicht und keine Serviceplattform.
2. Der kritische Zustand unserer Landschaft ist nicht das Alter der Systeme, sondern die Teilung der
   Daten: zwei getrennte ERP-Bestände seit 2018 und eine Produktdatenhaltung, die seit 2014 quer
   durch das Engineering verläuft.
3. Der Engpass liegt bei uns, nicht am Markt. Die Auswahl eines Produkts kostet Wochen. Das Ersetzen
   gewachsener Arbeitsschritte kostet Jahre und bindet dieselben Personen, die den laufenden Betrieb
   sicherstellen.

## Bestand zum Dezember 2022

| Baustein | heute im Einsatz | Charakter im Programm |
|---|---|---|
| ERP | Kassel proALPHA seit 2006, Eisenach Infor aus der Übernahme 2018, getrennte Bestände | Konsolidierung zweier Landschaften |
| CRM | kein System. Kundenstamm im jeweiligen ERP, Angebotsverfolgung in Excel und E-Mail | Neueinführung |
| PLM-Integration | PLM-Plattform von Siemens Digital Industries Software seit 2014, eng an das 3D-CAD gekoppelt, genutzt im Wesentlichen von der mechanischen Konstruktion | Ausweitung und Anbindung |
| Projektportfolio | MS Project je Projektleiter, zentrale Ressourcenplanung seit 2017 nach POL-PM-003, daneben weiterhin Abteilungsplanung in Excel | Neueinführung |
| Beschaffung | im jeweiligen ERP abgebildet, S&OP seit 2021 mit Excel-Auswertungen daneben | an die ERP-Entscheidung gebunden |
| MES | nicht vorhanden. Fertigungssteuerung über das ERP, in Eisenach zusätzlich über lokale Access-Datenbanken | Neueinführung |
| Data Warehouse | nicht vorhanden. Auswertungen entstehen als Exporte aus zwei ERP-Systemen | Neueinführung |
| Reporting | Controlling arbeitet auf diesen Exporten in Excel | Neueinführung, abhängig vom Data Warehouse |
| Serviceplattform | nicht vorhanden. Servicedisposition arbeitet mit ERP-Aufträgen und eigenen Listen, Remote-Service seit 2020 | Neueinführung |

Nicht Gegenstand des Programms und tragfähig: Identitäts- und Zugriffsdienst seit 2019,
Kollaborationsplattform und Dokumentenablage seit 2020, VPN-Zugang, Zeitwirtschaft, E-CAD im
Schaltanlagenbau, Simulationssoftware in der Entwicklung. Diese Basis müssen wir nicht anfassen, sie
ist aber der Ort, an dem Berechtigungen für alle neuen Systeme entstehen.

## Drei Befunde

**Die Datenteilung ist älter als das Programm.** Mechanische Stücklisten liegen im PLM, kaufmännische
im ERP, Projektunterlagen auf Netzlaufwerken und seit 2020 zusätzlich in der Dokumentenablage.
Elektrotechnik, Verfahrenstechnik und Projektmanagement arbeiten außerhalb des PLM. Jede Auswertung
über Projekte hinweg beginnt deshalb mit einem Export und einer manuellen Zuordnung. Wer ein Data
Warehouse baut, ohne diese Zuordnung vorher zu klären, automatisiert die Zuordnung nicht, sondern
verlagert sie.

**Zwei ERP-Landschaften mit einer bewussten Entscheidung dahinter.** 2018 galt "erst Geschäft
integrieren, dann IT". Die Entscheidung war zu ihrer Zeit richtig und ist vier Jahre später
unverändert offen. Artikel, Lieferanten und Kunden werden in beiden Systemen getrennt gepflegt, mit
unterschiedlichen Nummernkreisen und unterschiedlicher Feldbelegung. Die Verschmelzung zum 01.01.2022
hat daran nichts geändert, weil sie gesellschaftsrechtlich war und nicht technisch.

**Lokale Lösungen tragen Arbeitsschritte, die in keinem System stehen.** Access-Datenbanken und
Excel-Werkzeuge, in Eisenach ausgeprägter als in Kassel, teilweise ohne dokumentierte
Verantwortlichkeit. Diese Schatten-IT ist kein Missstand, den man abschaltet. Sie ist der Beleg
dafür, wo unsere Standardsysteme einen Prozess nicht abbilden. Wer sie abschaltet, muss die Funktion
vorher ersetzt haben, sonst entsteht sie an anderer Stelle neu.

## Randbedingungen

**Betriebskosten.** Das Programmbudget von 14,8 Mio EUR deckt die Einführung. Lizenz- und
Betriebskosten der neuen Systeme fallen ab Produktivsetzung dauerhaft an und landen im IT-Budget,
nicht im Programmbudget. Bei sechs Neueinführungen ist das eine strukturelle Erhöhung unseres
laufenden Aufwands, die in keiner Planung steht. Ich brauche dafür eine Zusage, bevor der erste
Baustein ausgeschrieben wird, sonst finanziere ich den Betrieb des Programms aus dem Budget für den
Betrieb des Bestands.

**Investitionsvorlage.** Nach der seit Juli geltenden Regelung sind ab 2 Mio EUR NPV, IRR und
Szenarien vorzulegen. Mehrere Bausteine liegen einzeln unter dieser Schwelle, das Programm liegt
deutlich darüber. Ob je Baustein oder einmal für das Programm vorgelegt wird, ist eine kaufmännische
Festlegung, hat aber technische Folgen: eine Vorlage je Baustein zwingt uns, die Bausteine einzeln
rechenbar zu schneiden, und genau das sind sie wegen der gemeinsamen Stammdaten nicht.

**Mitbestimmung.** Der Gesamtbetriebsrat hat am 06.12. eine Rahmenvereinbarung für alle im Programm
enthaltenen Systeme verlangt, die Geschäftsführung hat dem Verfahren zugestimmt. Das betrifft uns
unmittelbar: MES, Serviceplattform und Projektportfolio erzeugen personenbezogene Daten, das ERP tut
es in der Zeit- und Leistungsrückmeldung ohnehin. Aus der Einführung der Kollaborationsplattform 2020
weiß ich, dass Tempo möglich ist, wenn die Zweckbindung der Daten sauber geregelt ist. Der Vorlauf
muss aber im Terminplan stehen und nicht in der Risikoliste.

**Standardsoftware gegen Projektgeschäft.** Unser Geschäft ist überwiegend kundenspezifisch, die
Plattformstandardisierung greift in der Konstruktion, nicht in der Abwicklung. Über Kosten und
spätere Betriebsfähigkeit entscheidet der Umfang der Anpassungen, nicht die Produktauswahl. Jede
Anpassung, die wir heute zusagen, zahlen wir bei jedem Release ein zweites Mal.

## Vor der Festlegung des Umsetzungsansatzes zu klären

- Welcher ERP-Bestand ist der führende für Artikel, Lieferanten und Kunden. Diese Frage geht jeder
  Produktauswahl voraus und ist keine IT-Frage, sondern eine Entscheidung über Prozesse.
- Rahmen für die laufenden Betriebskosten ab der ersten Produktivsetzung.
- Schnitt der Investitionsvorlagen: Programm oder Baustein.
- Reihenfolge von Data Warehouse und Reporting gegenüber den Quellsystemen. Beide werten Daten aus,
  deren Struktur sich im Programm selbst ändert.
- Zeitbedarf für die Rahmenvereinbarung mit dem Gesamtbetriebsrat, abgestimmt mit dem
  Einführungsplan.

Aus dem Zustand der Stammdaten heraus spricht wenig dafür, mehrere Bausteine gleichzeitig zu
beginnen. Das ist meine Einschätzung und nicht die Entscheidung. Sobald der Zuschnitt steht, liefere
ich je Baustein den Aufwand für Betrieb, Schnittstellen und Berechtigungen nach; für die
Stammdatenfrage kann ich innerhalb von zwei Wochen eine belastbare Bestandsaufnahme aus beiden
Systemen vorlegen.

Löbner
