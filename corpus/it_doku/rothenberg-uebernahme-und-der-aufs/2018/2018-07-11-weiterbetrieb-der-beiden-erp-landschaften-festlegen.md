---
doc_id: LTT-20180711-IT-03
titel: Weiterbetrieb der beiden ERP-Landschaften Kassel und Eisenach
dokumenttyp: Architekturentscheidung
datum: 2018-07-11
verfasser: Karin Löbner
rolle: Leiterin IT
organisationseinheit: IT
empfaenger: "-"
projekt: IP-2018-01
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [bereichsintern, projektintern]
ablageort: it_doku
---

Lahnberg Thermotechnik GmbH & Co. KG - Informationstechnologie
Architekturentscheidung AE-2018-03

| | |
|---|---|
| Dokument | LTT-20180711-IT-03, Fassung 1.0 |
| Datum | 11.07.2018 |
| Verfasserin | K. Löbner, Leiterin IT |
| Gegenstand | ERP-Betrieb an den Standorten Kassel und Eisenach |
| Bezug | Projektauftrag Integrationsprojekt Eisenach (IP-2018-01) vom 03.06.2018 |
| Status | entschieden, wirksam ab 01.08.2018 |
| Wiedervorlage | Investitionsplanung 2020, spätestens 30.09.2019 |
| Lenkung | POL-QM-001 |
| Abgestimmt mit | W. Bergmann (kaufmännische Geschäftsführung), D. Anselm (Controlling), K. Rothenberger (Standortleitung Eisenach) |

## 1. Anlass

Mit der Übernahme der Rothenberg Verdichtertechnik GmbH zum Jahresbeginn gehören rund 125
Mitarbeiter und knapp 19 Mio. EUR Umsatz zum Unternehmen, die vollständig außerhalb unserer
Systemlandschaft arbeiten. Eisenach hat seine eigene Organisation, sein eigenes ERP und seine eigenen
Lieferanten behalten. Der Projektauftrag vom 03.06.2018 hat den Leitsatz "Erst Geschäft integrieren,
dann IT" bestätigt.

Damit ist die geschäftliche Reihenfolge geklärt, die technische Frage aber nicht: Wir betreiben seit
Januar zwei getrennte ERP-Landschaften, ohne dass irgendwo festgehalten wäre, dass das so gewollt ist,
wie lange es gelten soll und was in dieser Zeit erlaubt ist und was nicht. Genau das regelt dieses
Dokument. Ein Zustand, den niemand entschieden hat, wird sonst durch bloße Dauer zur Architektur.

## 2. Ausgangslage

Kassel arbeitet seit 2006 auf der ERP-Suite der proALPHA Business Solutions GmbH, seit 2014 ergänzt um
die PLM-Plattform von Siemens mit angebundenem 3D-CAD. Eisenach arbeitet auf einem ERP der Infor
Deutschland GmbH und daneben auf einer größeren Zahl lokaler Access-Datenbanken und Excel-Lösungen,
insbesondere in der Arbeitsvorbereitung, an den Verdichterprüfständen und in der Gießerei. Wie viele
dieser Anwendungen produktiv geführt werden und wer sie pflegt, ist mir bis heute nicht vollständig
bekannt.

Fachlich sind beide Häuser unterschiedlich zugeschnitten. Kassel rechnet und steuert im Wesentlichen
auftragsbezogen, Eisenach fertigt Baugruppen in wiederkehrenden Losen. Artikelnummernkreise,
Kontenrahmen, Stücklistenlogik und Fertigungssteuerung folgen jeweils dieser Ausrichtung. Das ist kein
Versäumnis von Rothenberg, sondern das Ergebnis eines anderen Geschäfts.

Praktisch berühren sich die beiden Welten heute an vier Stellen:

- Verdichterlieferungen aus Eisenach an Kassel. Bestellung und Auftrag stehen in zwei Systemen und
  sind nicht miteinander verknüpft; die Zuordnung erfolgt über die Belegnummer im Text.
- Ein und dieselbe Verdichterbaugruppe trägt in Kassel und in Eisenach unterschiedliche Sachnummern.
- Controlling verdichtet die Monatszahlen Eisenachs über eine Excel-Vorlage von Hand.
- Die Lieferantenbewertung nach POL-EK-001 endet an der Standortgrenze. Der strategische Einkauf sieht
  die Eisenacher Lieferanten nicht.

Die Netzanbindung Eisenachs über unsere bestehende Fortinet-Strecke ist davon unabhängig, läuft und
bleibt in Betrieb. Sie ist Voraussetzung für alles Weitere, aber kein Ersatz für eine
Anwendungsentscheidung.

## 3. Geprüfte Möglichkeiten

**A - Migration Eisenachs auf das Kasseler ERP.** Ein zweiter Mandant wäre grundsätzlich vorstellbar,
wäre aber ein eigenes Projekt mit Neuaufbau von Kontenrahmen, Nummernkreisen und
Fertigungssteuerung, mit Datenübernahme und mit Schulung der gesamten Eisenacher Verwaltung. Nach
meiner Schätzung binden wir dafür ein Jahr und eine erhebliche Investition, und zwar genau in dem
Zeitraum, in dem Eisenach Liefermengen für Kassel hochfahren soll. Es liegt keine Investitionsfreigabe
für eine Systemzusammenführung vor.

**B - Weiterbetrieb beider Systeme mit definierten Berührungspunkten.** Beide ERP bleiben produktiv.
Die vier oben genannten Berührungspunkte werden beschrieben, verantwortet und, wo es sich lohnt,
technisch unterstützt. Keine der beiden Landschaften wird ausgebaut.

**C - Neuauswahl eines gemeinsamen Systems für beide Standorte.** Wäre die sauberste Zielarchitektur
und ist zum jetzigen Zeitpunkt nicht ernsthaft zu diskutieren. Wir hätten zwei laufende
Ablösungen gleichzeitig, in einem Jahr, in dem die Belegschaft um ein Drittel gewachsen ist.

## 4. Entscheidung

Es gilt Möglichkeit B. Beide ERP-Landschaften bleiben bis auf Weiteres in Betrieb, mit folgenden
Festlegungen:

1. Eisenach führt sein Infor-System eigenverantwortlich weiter. Die IT Kassel übernimmt bis zur
   Wiedervorlage weder Betrieb noch Support dieses Systems.
2. Es entsteht keine automatische Kopplung der beiden ERP. Die Übergabe zwischen Bestellung und
   Auftrag bleibt manuell und wird stattdessen sauber beschrieben.
3. Für die Verdichterbaugruppen, die zwischen den Standorten geliefert werden, wird eine gepflegte
   Zuordnungsliste geführt: Kasseler Sachnummer, Eisenacher Sachnummer, Benennung, gültig ab. Sie liegt
   in der Verantwortung der Arbeitsvorbereitung Kassel und ist bis 30.09.2018 erstmals vollständig.
4. **Ausbaustopp.** In Eisenach wird bis zur Wiedervorlage keine neue Access- oder Excel-Anwendung in
   produktiven Gebrauch genommen, die Daten führt, welche später zu übernehmen wären. Bestehende
   Anwendungen werden bis 31.10.2018 in einer Liste erfasst: Zweck, Verantwortlicher, Datenbestand,
   Ablageort. Ohne diese Liste ist eine spätere Zusammenführung nicht kalkulierbar, sondern eine
   Entdeckungsreise.
5. Beschaffungen von Anwendungssoftware an beiden Standorten laufen ab 01.08.2018 über die IT Kassel.
   Das ist keine Bevormundung Eisenachs, sondern die einzige Möglichkeit, den Abstand zwischen den
   Landschaften nicht weiter wachsen zu lassen.
6. Das PLM wird nicht auf Eisenach ausgedehnt. Die Verdichterunterlagen bleiben dort, wo sie heute
   sind.

## 5. Begründung

Die Entscheidung folgt der geschäftlichen Reihenfolge, die die Geschäftsführung gesetzt hat, und ich
halte sie für dieses Jahr für richtig. Eine Systemumstellung während der Übernahme hätte beide
Vorhaben gefährdet, und die IT hat in Kassel keine freie Kapazität für ein zweites Systemprojekt neben
dem laufenden Betrieb.

Ich halte gleichzeitig fest, was die Entscheidung kostet, damit es später nicht neu ermittelt werden
muss: zwei Wartungs- und Supportverträge, zwei Releasestände, zwei Berechtigungswelten, zwei
Sicherungsverfahren, doppelt gepflegte Artikel- und Lieferantenstämme sowie ein Berichtsweg für die
Monatszahlen, der von einer Excel-Datei und der Sorgfalt einzelner Personen abhängt. Die Zahlen
stimmen, aber sie stimmen nicht von selbst.

Der zweite Punkt wiegt für mich schwerer als der erste. Beim PLM haben wir 2014 ein gutes System
eingeführt und es der mechanischen Konstruktion überlassen. Vier Jahre später arbeiten Elektrotechnik,
Verfahrenstechnik und Projektmanagement immer noch daneben, und niemand hat das je entschieden - es hat
sich eingerichtet. Ein Übergangszustand ohne Enddatum und ohne benanntes Zielsystem wird zur
Dauerlösung, weil die Ablösung mit jedem Monat teurer wird, den er dauert. Deshalb sind Ziffer 4 und 5
oben nicht Beiwerk, sondern der eigentliche Inhalt dieser Entscheidung.

## 6. Was hiermit nicht entschieden ist

Nicht entschieden ist, welches der beiden ERP das Zielsystem wird, ob es überhaupt eines der beiden
wird und wann die Zusammenführung beginnt. Nicht entschieden ist die Behandlung der Gießerei, die
fertigungsseitig anders aussieht als alles, was wir in Kassel abbilden. Nicht entschieden ist die
künftige Betreuung der Eisenacher Anwendungen über die Wiedervorlage hinaus.

Zur Wiedervorlage lege ich eine Kostenaufstellung des Parallelbetriebs und einen Vorschlag für ein
Zielsystem vor. Ich bitte darum, diesen Punkt in der Investitionsplanung 2020 als eigene Position zu
führen und nicht im laufenden IT-Budget.

## 7. Offene Punkte

| Nr | Punkt | bei wem | bis |
|---|---|---|---|
| 1 | Bestandsliste der lokalen Anwendungen Eisenach | Standortleitung Eisenach, IT | 31.10.2018 |
| 2 | Zuordnungsliste Sachnummern Verdichterbaugruppen | Arbeitsvorbereitung Kassel | 30.09.2018 |
| 3 | Geltung von POL-IT-001 für die Benutzerverwaltung Eisenach | IT, Personal | 31.12.2018 |
| 4 | Reichweite der Betriebsvereinbarung BV-2017-01 am Standort Eisenach; dort besteht seit der Übernahme ein eigenes Gremium. Zur Trennung der Systemlandschaften ist bisher keine Mitbestimmungsfrage an mich herangetragen worden | Personal | offen |
| 5 | Aufnahme der Eisenacher Lieferanten in die Bewertung nach POL-EK-001 | strategischer Einkauf | offen |
| 6 | Beschreibung des manuellen Belegwegs Kassel - Eisenach | Controlling, IT | 30.09.2018 |

K. Löbner, 11.07.2018
