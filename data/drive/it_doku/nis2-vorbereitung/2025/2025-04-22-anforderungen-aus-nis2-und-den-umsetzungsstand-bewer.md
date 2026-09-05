---
doc_id: LTT-20250422-IT-00
titel: "Security Assessment: Anforderungen aus NIS2 und den Umsetzungsstand bewerten"
dokumenttyp: Security Assessment
datum: 2025-04-22
verfasser: Sven Bruckner
rolle: Informationssicherheitsbeauftragter
organisationseinheit: IT
empfaenger: "-"
projekt: "-"
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [it-security-restricted, unternehmensweit]
ablageort: it_doku
---

# Security Assessment: Anforderungen aus NIS2 und den Umsetzungsstand bewerten

Verfasser: Sven Bruckner, Informationssicherheitsbeauftragter, IT
Datum: 22.04.2025
Fassung: 1.0, Arbeitsstand
Einstufung: intern
Bezug: POL-IT-007 v1.0 (NIS2-Vorbereitung), POL-IT-002 v3.0 (Informationssicherheitsrichtlinie),
Richtlinie (EU) 2022/2555

## 1 Zusammenfassende Bewertung

Nach meiner Prüfung fällt LTT unter die Anforderungen der NIS2-Richtlinie. Die Einstufung ist keine
Ermessensfrage, und sie hängt auch nicht daran, wie schnell das deutsche Umsetzungsgesetz kommt: die
Pflichten treffen uns mit dessen Inkrafttreten, und der Vorlauf, den wir uns dann noch nehmen können,
ist die Zeit, die wir jetzt nutzen.

Der Umsetzungsstand ist uneinheitlich. Bei Identitäten, Berechtigungen und Cloud-Beschaffung stehen
wir besser da als vor drei Jahren, weil POL-IT-001 v3.0 und POL-IT-003 v2.0 aus dem Digital Core
heraus entstanden sind und wir sie ohnehin brauchten. Schwach sind wir überall dort, wo NIS2 nicht
Regelungen, sondern Nachweise und geübte Abläufe verlangt: Vorfallbehandlung mit festen Fristen,
Wiederanlauf, Angriffserkennung, Sicherheit in der Lieferkette und die Trennung von Büro- und
Anlagennetzen. Von den zehn Anforderungsbereichen bewerte ich zwei als weitgehend erfüllt, fünf als
teilweise erfüllt und drei als offen.

Die grösste Lücke ist nicht technischer Natur. Wir haben keinen einzigen erprobten Meldeweg, weil wir
noch nie einen Vorfall hatten, der einen erfordert hätte. Was wir an sicherheitsrelevanten Ereignissen
gesehen haben, blieb unterhalb jeder Schwelle, die nach den kommenden Kriterien eine Meldung ausgelöst
hätte. Das ist ein Glücksfall und kein Reifegrad. Eine Frist von 24 Stunden für die Frühwarnung lässt
sich nicht improvisieren, sie muss geübt sein.

Ich halte fest, dass die Vorbereitung mit der heutigen Personalausstattung der IT nicht in der
gebotenen Zeit zu leisten ist. Die Position des Informationssicherheitsbeauftragten ist seit 2021
besetzt, aber unverändert eine Einzelfunktion neben dem laufenden Betrieb.

## 2 Bewertungsgrundlage und Vorgehen

Bewertet habe ich gegen die zehn Mindestmassnahmen des Risikomanagements nach Artikel 21 Absatz 2 der
Richtlinie (EU) 2022/2555 sowie gegen die Melde- und Registrierungspflichten der Artikel 23 und 3. Die
deutsche Umsetzung ist zum Zeitpunkt dieser Bewertung nicht in Kraft; die Entwürfe folgen der
Richtlinie in Struktur und Fristen so eng, dass ich die Richtlinie als Prüfmassstab für tragfähig
halte. Wo der deutsche Gesetzgeber schärfer werden kann, habe ich das vermerkt.

Grundlage waren die geltenden Richtlinien POL-IT-001 bis POL-IT-007, POL-QM-001 v2.0, POL-SCM-003 v1.0
sowie die Betriebsdokumentation der Anwendungen. Ich habe keine technische Prüfung durchgeführt: keine
Schwachstellenanalyse, keinen Penetrationstest, keine Prüfung der Netzsegmentierung im Werk. Diese
Bewertung ist eine Selbsteinschätzung anhand von Dokumenten und Gesprächen. Sie ersetzt die externe
Prüfung nicht, die ich unter Abschnitt 9 vorschlage.

## 3 Betroffenheit

### 3.1 Einstufung

LTT stellt Maschinen und Ausrüstungen her - industrielle Wärmepumpen, Wärmerückgewinnungsanlagen,
Verdichter. Damit fallen wir unter Anhang II der Richtlinie. Die Grössenkriterien überschreiten wir
mit 720 Beschäftigten und 150 Mio EUR Umsatz deutlich. Nach heutigem Stand wären wir als wichtige
Einrichtung einzustufen, mit Registrierungspflicht bei der zuständigen Behörde binnen der im
Umsetzungsgesetz vorgesehenen Frist.

Der Unterschied zwischen wichtiger und besonders wichtiger Einrichtung betrifft die Aufsicht, nicht
die Massnahmen: die zehn Anforderungen aus Artikel 21 gelten für beide identisch. Wer intern
argumentiert, wir seien "nur" die kleinere Kategorie, hat für den Umsetzungsaufwand nichts gewonnen.

### 3.2 Standorte

Kassel und Eisenach sind Betriebe derselben Rechtsperson und damit gemeinsam erfasst. Eisenach ist
dabei nicht der einfachere Teil: die dortige Systemlandschaft trägt bis heute Reste der Zeit vor der
Verschmelzung, einschliesslich lokal betriebener Datenbanken und Anwendungen, die nie Gegenstand einer
zentralen Betriebsdokumentation waren.

Rotterdam und Brno unterliegen den nationalen Umsetzungen der Niederlande und Tschechiens. Eine
Konzernzuständigkeit am Hauptsitz sieht die Richtlinie für unsere Sektoren nicht vor. Beide
Niederlassungen liegen mit 15 und 28 Beschäftigten unter den Grössenschwellen; ich gehe von keiner
eigenständigen Erfassung aus, halte das aber für rechtlich zu bestätigen. Houston und Shanghai liegen
ausserhalb des Geltungsbereichs, sind über die Fernzugriffe auf unsere Systeme aber Teil derselben
Angriffsfläche.

### 3.3 Mittelbare Betroffenheit

Der Teil, der uns unabhängig von der eigenen Einstufung erreicht, kommt von der Kundenseite. Wir
liefern und betreuen Anlagen bei Stadtwerke Kassel-Land AöR, Stadtwerke Fulda GmbH, Sydhavn
Fjernvarme A/S, Warmtenet Zuid-Holland B.V. und Quartierswerke Leipzig Ost GmbH, dazu beim Klinikum
Weserbergland gGmbH. Diese Kunden fallen selbst unter die Richtlinie, teilweise unter Anhang I. Sie
sind verpflichtet, die Sicherheit ihrer Lieferkette zu bewerten, und werden das an uns weitergeben -
über Fragebögen, Vertragsklauseln und Nachweise, nicht über gutes Zureden.

Das ist keine Prognose, sondern die absehbare Mechanik der Richtlinie. Wir arbeiten seit 2020 mit
Remote-FAT, Remote-Service und VPN-gestützter Inbetriebnahme; in mehreren dieser Projekte haben wir
technischen Zugang in die Anlagennetze unserer Kunden. Ich erwarte, dass genau dieser Zugang der erste
Punkt ist, den ein Betreiber kritischer Infrastruktur bei uns prüft.

Auf unserer eigenen Lieferantenseite betrifft es vor allem die Automatisierungs- und
Schaltanlagenpartner mit Datenaustausch und teilweise mit Zugängen: NordControl Schaltanlagen GmbH,
ElektroPlan Süd GmbH, RheinMain Automation Systems GmbH, Auconta Steuerungstechnik GmbH und Litec
Automation B.V.

## 4 Umsetzungsstand nach Anforderungsbereichen

Bewertung: erfüllt / teilweise / offen.

| Nr | Anforderung nach Art. 21 Abs. 2 | Stand bei LTT | Bewertung |
|---|---|---|---|
| A1 | Risikoanalyse und Sicherheitskonzepte | POL-IT-002 v3.0 vorhanden, Risikobetrachtung nicht systematisch und nicht turnusmässig | teilweise |
| A2 | Bewältigung von Sicherheitsvorfällen | keine dokumentierte Prozessbeschreibung mit Rollen, Eskalation und Fristen | offen |
| A3 | Betriebskontinuität, Backup, Wiederherstellung, Krisenmanagement | Sicherungen laufen, Wiederherstellung nie unter Zeitdruck geprüft; kein Notfallhandbuch | offen |
| A4 | Sicherheit der Lieferkette | POL-EK-001 v3.0 und POL-SCM-003 v1.0 decken Versorgung und Bonität ab, nicht Cybersicherheit | teilweise |
| A5 | Sicherheit bei Beschaffung, Entwicklung und Wartung, Schwachstellenmanagement | POL-IT-003 v2.0 greift für Cloud und SaaS; kein geregelter Umgang mit Schwachstellenmeldungen für Anlagentechnik | teilweise |
| A6 | Bewertung der Wirksamkeit der Massnahmen | keine internen Prüfungen, keine Kennzahlen, keine externe Prüfung | offen |
| A7 | Cyberhygiene und Schulung | Grundunterweisung vorhanden, ohne Nachweisführung und ohne Zielgruppendifferenzierung | teilweise |
| A8 | Kryptografie und Verschlüsselung | Transportverschlüsselung durchgängig, Endgeräteverschlüsselung überwiegend, ohne Konzept | teilweise |
| A9 | Personalsicherheit, Zugriffskontrolle, Verwaltung der Werte | POL-IT-001 v3.0 mit zentraler Benutzerverwaltung und Rollenkonzept; Rezertifizierung nicht etabliert | erfüllt |
| A10 | Multi-Faktor-Authentifizierung, gesicherte Kommunikation | MFA für externe Zugänge und Cloud-Anwendungen aktiv; interne Administrationszugänge teilweise ohne | erfüllt |

Zwei Anmerkungen zur Tabelle. Erstens ist A9 die einzige Zeile, die wir einem Prüfer heute ohne
Vorarbeit vorlegen könnten, und das verdanken wir dem Berechtigungskonzept, das mit der ERP-Einführung
im Oktober 2024 ohnehin entstehen musste. Zweitens ist A6 die unangenehmste Zeile: Ohne eine Bewertung
der Wirksamkeit ist jede der anderen neun Zeilen eine Behauptung, auch die beiden guten.

## 5 Wesentliche Lücken

**L1 - Vorfallbehandlung ohne Prozess und ohne Übung.** Es existiert keine Beschreibung, wer einen
Verdachtsfall entgegennimmt, wer entscheidet, ob gemeldet wird, wer meldet und wer die Geschäftsführung
unterrichtet. Die Richtlinie sieht eine Frühwarnung binnen 24 Stunden, eine Meldung binnen 72 Stunden
und einen Abschlussbericht binnen eines Monats vor. Diese Uhr läuft ab Kenntnis, nicht ab
Klärung des Sachverhalts, und sie läuft auch am Wochenende.

**L2 - Kein geprüfter Wiederanlauf.** Wir sichern, aber wir haben nie unter realistischen Bedingungen
zurückgeholt. Für die Lieferkette haben wir mit POL-SCM-003 einen Business-Continuity-Plan und einen
jährlichen Financial-Health-Check je kritischem Lieferanten. Für den Ausfall unserer eigenen
Kernsysteme haben wir nichts Vergleichbares. Diese Asymmetrie fällt mir seit dem ERP-Produktivstart
auf: Wir haben die Abhängigkeit von einzelnen Systemen erheblich erhöht und die Vorsorge nicht
mitgezogen.

**L3 - IT/OT-Segmentierung nicht bewertet.** Der Zustand der Netze in Fertigung, Montage, auf den
Verdichterprüfständen und in der Gießerei ist nicht dokumentiert. Mit der Modernisierung in Eisenach
kommen automatisierte Formtechnik und zusätzliche elektrische Prozessunterstützung hinzu, also neue
vernetzte Anlagentechnik in einem Bereich, der bisher kaum im Blickfeld der IT lag. Ich habe für
diesen Bereich weder eine Bestandsaufnahme noch eine Zuständigkeitsregelung.

**L4 - Lieferantensicherheit ist kommerziell, nicht technisch geregelt.** Unsere Lieferantenbewertung
kennt Qualität, Preis, Termintreue, Innovationsfähigkeit, Versorgungssicherheit und seit 2024 die
finanzielle Gesundheit. Sie kennt keine Sicherheitsanforderung. In den Rahmenverträgen der
Schaltanlagen- und Automatisierungspartner finde ich keine Klausel zu Meldepflichten bei Vorfällen,
zum Umgang mit unseren Daten oder zu Fernzugängen. POL-IT-002 v2.0 hat Lieferantenzugänge 2023
erstmals adressiert, aber nur betrieblich und nicht vertraglich.

**L5 - Angriffserkennung findet nicht statt.** Wir erzeugen Protokolldaten in erheblichem Umfang,
werten sie aber nicht zusammenführend aus. Ein Angriff, der keinen Betriebsausfall verursacht, würde
uns heute nicht auffallen. Zu den Gründen siehe Abschnitt 7; sie sind nicht nur technischer Art.

## 6 Meldewege

POL-IT-007 v1.0 nennt Meldewege als einen von vier Vorbereitungsschwerpunkten. Der Punkt ist bisher
nur benannt. Zu klären sind die Erreichbarkeit ausserhalb der Regelarbeitszeit, die Vertretung meiner
Funktion, die Rolle der Geschäftsführung bei der Meldeentscheidung und das Verhältnis zur
Datenschutzmeldung nach Artikel 33 DSGVO, für die eine eigene 72-Stunden-Frist und mit Frau Kroll eine
eigene Zuständigkeit besteht. Bei einem Vorfall mit Beschäftigtendaten laufen beide Fristen
gleichzeitig, mit unterschiedlichen Adressaten und unterschiedlichen Inhalten. Das muss vorher geklärt
sein und nicht im Ereignisfall.

Ich schlage eine Meldeübung im dritten Quartal vor, an einem fiktiven Fall, mit
Geschäftsführung, Recht und Datenschutz, Operations und Standortleitung Eisenach. Der Wert einer
solchen Übung liegt erfahrungsgemäss weniger im Ablauf als in den Fragen, die dabei zum ersten Mal
gestellt werden.

## 7 Zielkonflikt Protokolldaten und Mitbestimmung

Eine wirksame Angriffserkennung verlangt die zusammenführende Auswertung von Protokolldaten aus
Netzübergängen, Verzeichnisdienst, Endgeräten und Anwendungen. Diese Daten sind zu einem erheblichen
Teil personenbeziehbar.

Dem steht BV-2017-01 entgegen, die Protokolldaten ausdrücklich auf die Störungsbeseitigung begrenzt
und stichprobenfreie Auswertung vorsieht, sowie BV-2020-02, die für die Kollaborationsplattform jede
Auswertung personenbezogener Nutzungsdaten ausschliesst. Beide Vereinbarungen sind aus gutem Grund so
geschrieben worden, und ich halte nichts davon, sie als Hindernis darzustellen.

Der richtige Weg ist der eingeführte: eine Teilvereinbarung nach der Rahmenvereinbarung BV-2023-01,
mit einer harten Zweckbindung auf die Erkennung und Bearbeitung von Sicherheitsvorfällen, definierten
Aufbewahrungsfristen, protokolliertem Zugriff auf die Auswertung und einem Ausschluss jeder Verwendung
für Führungs- oder Leistungszwecke. Das Muster gibt es im Haus bereits zweimal, zuletzt bei den
Projektkennzahlen im Februar dieses Jahres. Ich empfehle, den Gesamtbetriebsrat früh und nicht erst
mit einem fertigen Beschaffungsvorschlag einzubinden; die Erfahrung mit dem Dashboard spricht dafür,
dass die Diskussion über die Zweckbindung besser vor der Systemauswahl geführt wird als danach.

## 8 Aufwand und Kapazität

Meine Schätzung für die Herstellung eines nachweisfähigen Zustands über 2025 und 2026: einmalig rund
350 bis 450 TEUR, davon der grössere Teil für ein Protokoll- und Auswertungssystem einschliesslich
Einführung, für die externe Prüfung und für die Aufnahme der Anlagennetze; laufend rund 100 bis 140
TEUR im Jahr für Betrieb, Prüfungen und Schulung. Die Schätzung ist grob und wird belastbar erst mit
dem Ergebnis der externen Prüfung. Sie liegt unterhalb der Schwelle der Investitionsrichtlinie
POL-FIN-002; die Betriebskostenbetrachtung nach v1.1 ist trotzdem zu erstellen, weil der laufende
Anteil dauerhaft ist.

Beim Personal wird es deutlicher. Die Aufgabe umfasst nach meiner Rechnung etwa 1,5 zusätzliche
Vollzeitäquivalente über zwei Jahre, davon eine dauerhafte Stelle. Die Informationssicherheit ist bei
LTT seit 2021 eine Einzelfunktion, die neben dem Applikationsbetrieb läuft. Mit dieser Ausstattung kann
ich Richtlinien schreiben, Fragebögen beantworten und Vorfälle nachbereiten. Ich kann damit keinen
Nachweiszustand herstellen und ihn gleichzeitig halten.

Dazu gehört eine Einordnung, die mir wichtig ist. Die Parole "Stabilisieren vor transformieren" und
die Begrenzung auf drei Top-Priority-Change-Initiatives je Business Unit halte ich nach den letzten
drei Jahren für richtig. Die NIS2-Vorbereitung ist aber keine Change-Initiative, die mit anderen
Vorhaben um einen der drei Plätze konkurriert. Sie ist eine Pflichtaufgabe mit gesetzlicher Frist, und
sie liegt bei den zentralen Funktionen, nicht bei den Business Units. Wird sie in die Logik der drei
Initiativen gezwungen, verliert sie gegen jedes Vorhaben mit sichtbarem Nutzen - und zwar bis zu dem
Tag, an dem sie plötzlich sehr dringend wird.

## 9 Vorgeschlagene Schritte

| Nr | Schritt | Vorschlag Verantwortung | Termin |
|---|---|---|---|
| S1 | Betroffenheitsanalyse rechtlich bestätigen, einschliesslich Rotterdam und Brno | ISB mit Recht und Datenschutz | Q2 2025 |
| S2 | Prozess zur Vorfallbehandlung mit Rollen, Eskalation und Fristen beschreiben und in Kraft setzen | ISB | Q2 2025 |
| S3 | Externe Prüfung: Schwachstellenanalyse Bürolandschaft und Bestandsaufnahme der Anlagennetze | IT-Leitung, Beschaffung über strategischen Einkauf | Q3 2025 |
| S4 | Meldeübung an einem fiktiven Fall | ISB mit Geschäftsführung, Recht, Operations, Standort Eisenach | Q3 2025 |
| S5 | Wiederanlauf der drei kritischsten Anwendungen unter Zeitmessung prüfen | IT-Applikationen | Q3 2025 |
| S6 | Sicherheitsanforderungen und Meldeklausel in die Lieferantenbewertung und in die Rahmenverträge aufnehmen | strategischer Einkauf mit ISB | Q3 2025 |
| S7 | Teilvereinbarung nach BV-2023-01 zur Auswertung von Protokolldaten verhandeln | ISB mit HR und Gesamtbetriebsrat | Q3 bis Q4 2025 |
| S8 | Schulungskonzept mit Nachweisführung, gesonderter Teil für die Geschäftsführung | ISB mit HR | Q4 2025 |
| S9 | Beschaffungsvorschlag Protokoll- und Auswertungssystem nach Vorliegen von S3 und S7 | ISB mit IT-Applikationen | Q4 2025 |

Zu S8 gehört ein Hinweis, der in der Richtlinie ausdrücklich steht und im Haus wenig bekannt ist: Die
Geschäftsführung hat die Risikomanagementmassnahmen zu billigen und ihre Umsetzung zu überwachen, sie
ist zur Teilnahme an Schulungen verpflichtet, und sie haftet für Verstösse. Die
Informationssicherheit wird damit vom IT-Thema zu einer Leitungsaufgabe. Ich gehe davon aus, dass das
Audit Committee des Beirats den Umsetzungsstand abfragen wird, sobald das Umsetzungsgesetz in Kraft
ist.

## 10 Offene Punkte und Vorbehalte

- Der Zeitpunkt des Inkrafttretens des deutschen Umsetzungsgesetzes ist offen. Alle Termine in
  Abschnitt 9 sind daran nicht gebunden; sie ergeben sich aus dem Aufwand, nicht aus der Frist.
- Die Einstufung als wichtige Einrichtung beruht auf meiner Lesart der Sektorzuordnung. Eine
  abweichende Einstufung halte ich für unwahrscheinlich, ausschliessen kann ich sie nicht.
- Die Bewertung in Abschnitt 4 ist eine Selbsteinschätzung ohne technische Prüfung. Ich erwarte, dass
  die externe Prüfung nach S3 mindestens eine der drei mit "erfüllt" oder "teilweise" bewerteten
  Zeilen nach unten korrigiert.
- Der Umgang mit den in der Excel Amnesty gemeldeten Dateien ist noch nicht abschliessend festgelegt.
  Für meine Zwecke ist die Meldung selbst schon ein Gewinn: Wir haben mit den rund 430 registrierten
  Dateien und den etwa 60 als geschäftskritisch eingestuften zum ersten Mal eine Liste von
  Anwendungen, die ausserhalb der zentralen Systeme geschäftskritisch sind. Ohne diese Liste hätte ich
  die Verwaltung der Werte nach A9 gar nicht ernsthaft beginnen können. Nach POL-IT-005 bekommen die
  kritischen Dateien Owner und Versionskontrolle; ich schlage vor, denselben Bestand auch in die
  Betrachtung des Wiederanlaufs nach L2 aufzunehmen, weil eine Datei mit Owner immer noch eine Datei
  ohne Sicherung sein kann.
- Für die Bestandsaufnahme der Anlagennetze fehlt mir eine benannte Zuständigkeit zwischen IT,
  Elektrotechnik und Automatisierung sowie Operations. Ich bitte um eine Klärung, bevor S3 vergeben
  wird.
