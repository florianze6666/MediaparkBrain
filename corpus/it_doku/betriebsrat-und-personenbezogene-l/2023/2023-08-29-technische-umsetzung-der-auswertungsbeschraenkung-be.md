---
doc_id: LTT-20230829-IT-04
titel: Technische Umsetzung der Auswertungsbeschränkung im CRM
dokumenttyp: Management Summary
datum: 2023-08-29
verfasser: Dr. Philipp Nowak
rolle: CIO
organisationseinheit: IT
empfaenger: "-"
projekt: PRJ-CRM-2023
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [projektintern, br-management-verhandlung]
ablageort: it_doku
---

# Management Summary: Technische Umsetzung der Auswertungsbeschränkung im CRM

**Verfasser:** Dr. Philipp Nowak, CIO
**Datum:** 29.08.2023
**Bezug:** BV-2023-02 (Personenbezogene Daten im CRM), unterzeichnet am 04.07.2023, Ausfertigung mit Anlagen seit dem 19.08.2023 vorliegend; Rahmenvereinbarung BV-2023-01 vom 16.03.2023; Teilprojekt CRM im Programm ONE LTT
**Einstufung:** intern

## 1. Kern in vier Sätzen

Das CRM erzeugt seit der Produktivsetzung im April Datensätze, die über Verantwortlichkeit und
Bearbeitungshistorie eindeutig einzelnen Vertriebsmitarbeitern zuzuordnen sind. BV-2023-02 lässt
Auswertungen nur auf Ebene Team und Region zu; eine Verdichtung zu individuellen Leistungsaussagen ist
ausgeschlossen. Die Umsetzung erfolgt nicht durch Löschen der Personenzuordnung im System, sondern
durch Trennung von operativer Bearbeitungsebene und Auswertungsebene. Die Konfiguration ist bis auf die
unter Abschnitt 5 genannten Punkte abgeschlossen.

## 2. Warum die Personenzuordnung im System bleibt

Ein CRM ohne Bearbeiterkennung ist funktionslos. Die Felder für Verantwortlichen, Ersteller und letzte
Änderung steuern Zuständigkeit, Vertretung, Wiedervorlage und Zugriffsrechte; sie sind kein
Auswertungsmerkmal, sondern die Adressierung des Datensatzes. Wir haben mit Frau Kroll geprüft, ob eine
Pseudonymisierung im operativen Bestand möglich ist. Sie ist es nicht, ohne den Zweck des Systems
aufzuheben.

Die Beschränkung setzt deshalb eine Ebene höher an: die Daten entstehen personenbezogen, sie werden
aber nur aggregiert auswertbar gemacht. Das ist derselbe Weg, den wir 2020 bei der
Kollaborationsplattform gegangen sind - dort war der auswertbare Anwesenheitsstatus das Problem, nicht
die Anwesenheit selbst.

## 3. Was umgesetzt wurde

**Berechtigungsebene (Dynamics 365).** Das Rollenmodell nach POL-IT-001 v2.0 wurde um drei
CRM-Sicherheitsrollen ergänzt. Der Zugriff auf einen einzelnen Datensatz bleibt im operativen Kontext
erhalten - ein Vertriebsleiter muss eine Opportunity seines Teams öffnen können. Entfallen ist die
Möglichkeit, personenbezogene Ergebnismengen zu erzeugen: Listenansichten, die nach Verantwortlichem
gruppieren oder sortieren, sind aus dem Rollenumfang der Führungsrollen entfernt, ebenso die
Feldauswahl "Verantwortlicher" im erweiterten Suchdialog.

**Berichtsebene (Power BI).** Hier liegt der eigentliche Hebel. Das semantische Modell führt keine
Personendimension mehr. Die Zuordnung Mitarbeiter zu Team und Region erfolgt bereits beim Laden; was
im Berichtsmodell ankommt, ist Team und Region. Damit ist eine personenbezogene Auswertung nicht
verboten, sondern nicht konstruierbar. Drillthrough auf Einzeldatensätze ist deaktiviert, eine
Mindestgruppengröße von fünf verhindert, dass ein Team mit zwei Mitarbeitern faktisch zur
Einzelauswertung wird. Die drei Standard-Dashboards des Herstellers zur Verkäuferleistung sind aus
allen Arbeitsbereichen entfernt.

**Exportwege.** Der Export nach Excel bleibt für den operativen Gebrauch offen; er wird auf die
jeweils sichtbare Ansicht begrenzt. Ich sage deutlich, dass dieser Punkt technisch nicht dicht ist:
Wer die Absicht hat, kann aus Einzelabfragen über die Zeit eine personenbezogene Auswertung
zusammensetzen. Eine vollständige technische Sperre wäre nur um den Preis einer Arbeitsfähigkeit zu
haben, die der Vertrieb zu Recht nicht aufgeben will. Die Restlücke wird durch die Zweckbindung in
BV-2023-02 getragen, nicht durch das System.

**Protokollierung.** Wir protokollieren die Nutzung der verbliebenen personenbezogenen Sichten. Diese
Protokolle sind selbst personenbezogen, und sie unterliegen BV-2017-01. Eine Auswertung findet
anlassbezogen und nur gemeinsam mit der Datenschutzbeauftragten statt. Der Gedanke, die Einhaltung
eines Auswertungsverbots durch laufende Auswertung zu kontrollieren, führt in einen Zirkel, den wir
nicht betreten.

## 4. Aufwand und Beteiligte

Die Konfigurationsarbeit lag bei etwa vier Wochen in der Applikationsbetreuung (Frau Faber), die
Anpassung des Berichtsmodells bei knapp drei Wochen, davon ein Teil bei der externen Beratung. Herr
Bruckner hat die Rollenzuschnitte gegengeprüft, Frau Kroll die Zweckbindung. Der Gesamtbetriebsrat hat
die Systembeschreibung mit Datenkatalog erhalten; Frau Kaya hat die Berichtskonfiguration am Bildschirm
gezeigt bekommen. Das war aufwendiger als eine schriftliche Zusicherung und aus meiner Sicht die
sinnvollere Investition, weil es die Diskussion vom Grundsätzlichen ins Konkrete verlegt hat.

## 5. Offene Punkte und Risiken

- **Herstellerupdates.** Dynamics 365 und Power BI werden im Quartalsrhythmus aktualisiert.
  Entfernte Standardberichte können nach einem Release zurückkehren, neue können hinzukommen. Wir
  nehmen die Prüfung der Auswertungskonfiguration in die Regressionsprüfung jedes Releases auf. Das
  ist dauerhafter Aufwand, kein einmaliger.
- **Zweitsysteme.** Die Beschränkung gilt für das CRM. Angebotsdaten liegen weiterhin auch im ERP,
  Forecast-Listen weiterhin in Excel. Wer eine personenbezogene Auswertung will, braucht das CRM dafür
  nicht. Der Datenkatalog nach BV-2023-01 sollte deshalb bei den nächsten Systemen des Programms nicht
  systemweise, sondern datenweise geführt werden.
- **Evaluation.** BV-2023-01 sieht eine Bewertung nach zwölf Monaten vor. Wir bereiten die dafür
  nötigen Nachweise ab dem zweiten Quartal 2024 auf.

## 6. Was ich daraus für die weiteren Systeme mitnehme

Die Teilvereinbarung ist nach der Produktivsetzung entstanden, nicht davor. Genau diese Reihenfolge
sollte BV-2023-01 verhindern. Die Folge ist keine schlechtere Regelung, aber eine deutlich teurere
Umsetzung: Ein Berichtsmodell, das ohne Personendimension entworfen wird, kostet nichts; dasselbe
Modell nachträglich von ihr zu befreien, hat uns drei Wochen und zwei Abstimmungsrunden gekostet.

Für MES, Serviceplattform und die Managementberichte gilt aus meiner Sicht: Der Datenkatalog gehört
vor die Konfiguration, nicht vor die Produktivsetzung. Ich werde das mit Frau Hartwig für die
Teilprojektplanung so vorsehen.

Die Kritik aus dem Vertrieb an der eingeschränkten Steuerungsfähigkeit ist mir bekannt. Sie richtet
sich gegen den Inhalt der Betriebsvereinbarung, nicht gegen ihre technische Umsetzung; die IT ist
dafür der falsche Adressat. Was technisch möglich wäre, ist eine Frage, die wir beantworten können -
was zulässig ist, ist zwischen Geschäftsführung und Gesamtbetriebsrat entschieden.
