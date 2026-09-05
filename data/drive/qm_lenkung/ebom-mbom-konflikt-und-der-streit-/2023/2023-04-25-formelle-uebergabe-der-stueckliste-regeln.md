---
doc_id: LTT-20230425-QM-01
titel: "SOP: Formelle Übergabe der Stückliste regeln"
dokumenttyp: SOP
datum: 2023-04-25
verfasser: Bernd Hoffmann
rolle: Leiter Qualitätsmanagement
organisationseinheit: QM
empfaenger: ["-"]
projekt: IP-2023-03
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit]
ablageort: qm_lenkung
---

Lahnberg Thermotechnik GmbH & Co. KG
Qualitätsmanagement - gelenktes Dokument nach POL-QM-001 v2.0

**SOP QM-08-03 - Formelle Übergabe der Stückliste (EBOM nach MBOM)**

| | |
|---|---|
| Version | 1.0, Erstausgabe |
| Erstellt | B. Hoffmann, Leiter Qualitätsmanagement, 25.04.2023 |
| Geprüft | M. Gehrke (Konstruktion mechanisch), R. Wiesner (Elektrotechnik und Automatisierung), N. Feld (Arbeitsvorbereitung), O. Bensch (Teilprojekt ERP und Stammdaten) |
| Freigabe | Dr. J. Mahlberg (CTO) |
| Gültig ab | 02.05.2023 |
| Geltungsbereich | Kassel und Eisenach, alle Aufträge und Entwicklungsvorhaben mit Fertigungsanteil |
| Ablage | Dokumentenlenkung QM, digitale Projektakte je Auftrag |
| Nächste Überprüfung | April 2024 |

---

## 1 Zweck und Anlass

Mit POL-ENG-001 v1.1 vom 01.04.2023 ist die durchgängige Struktur von Entwicklungsstückliste (EBOM)
und Fertigungsstückliste (MBOM) verbindlich, einschließlich einer formellen Übergabe zwischen
Konstruktion und Produktion. Diese SOP legt fest, wann übergeben wird, was übergeben wird, wer
gegenzeichnet und wie mit Abweichungen umzugehen ist.

Der sachliche Anlass ist bekannt: Die Fertigungsstückliste wurde in der Vergangenheit teilweise
unmittelbar in der Produktion angepasst, ohne dass die Änderung an den freigegebenen
Konstruktionsstand zurückgebunden wurde. Für die laufende Fertigung war das meist unschädlich, für
Nachbau, Ersatzteilversorgung, Reklamationsbearbeitung und Auditnachweis ist es das nicht: Es lässt
sich nachträglich nicht belegen, welcher Stand tatsächlich gebaut wurde. Die Anforderungen an die
Steuerung von Entwicklungs- und Fertigungsänderungen (ISO 9001, Abschnitte 8.3.6 und 8.5.6) sind auf
dieser Grundlage nicht erfüllbar.

Das Qualitätsmanagement hat diese SOP bewusst kurz gehalten. Aus der Einführung des Design Freeze
2019 ist die Lehre zu ziehen, dass eine Regel ohne praktikablen Ausnahmeweg nicht befolgt, sondern
umgangen wird - und eine umgangene Regel erzeugt keinen Nachweis, sondern nur Ärger. Abschnitt 6.7
regelt den Eilfall deshalb ausdrücklich mit.

## 2 Geltungsbereich und Abgrenzung

Die SOP gilt für alle Kundenaufträge, Plattform- und Entwicklungsvorhaben mit Fertigungsanteil an
den Standorten Kassel und Eisenach.

Sie gilt nicht für Ersatzteillieferungen aus dem Bestand ohne Neuteil, für reine Serviceeinsätze und
für Angebotsphasen vor Auftragseingang.

Die Stücklisten der Elektrotechnik und der Verfahrenstechnik entstehen weiterhin außerhalb des
PLM-Systems. Für sie gilt bis auf Weiteres die Übergangsregelung nach 6.5.

## 3 Mitgeltende Unterlagen

- POL-ENG-001 v1.1, Design Freeze und Engineering Change Request
- POL-QM-001 v2.0, Dokumentenlenkung mit digitaler Projektakte
- POL-IT-006 v1.0, Stammdatenrichtlinie und Materialstammpflege
- POL-PM-001 v1.1, Projektmanagement-Standard
- POL-RD-001 v1.1, Stage-Gate-Prozess G0 bis G5, für Entwicklungsvorhaben ab G4
- Formblatt QM-08-03-F1, Übergabeprotokoll Stückliste
- Formblatt QM-08-03-F2, Zuordnungsliste EBOM zu MBOM

## 4 Begriffe

**EBOM** - Entwicklungsstückliste, funktions- und baugruppenorientiert, geführt im PLM-System
(Teamcenter), Freigabestand mit Revisionsindex.

**MBOM** - Fertigungsstückliste, fertigungs- und dispositionsorientiert, geführt im jeweils führenden
ERP-System des Fertigungsstandorts. In Kassel ist das die proALPHA-Umgebung, in Eisenach die
Infor-Umgebung. Bis zur Ablösung im Rahmen von ONE LTT bleibt es bei dieser Zweiteilung.

**Übergabepunkt** - der Zeitpunkt, zu dem die Konstruktion einen definierten EBOM-Stand an die
Arbeitsvorbereitung übergibt und die Verantwortung für die Fertigungsstruktur dort entsteht.

**ECR** - Engineering Change Request nach POL-ENG-001.

## 5 Verantwortlichkeiten

| Stelle | Aufgabe |
|---|---|
| Konstruktion mechanisch (M. Gehrke) | vollständige EBOM im Freigabestand, Zeichnungssatz, Kennzeichnung der Langläufer |
| Elektrotechnik und Automatisierung (R. Wiesner) | E-Stückliste nach 6.5, Abgleich der Schnittstellenpositionen |
| Arbeitsvorbereitung (N. Feld) | Vollständigkeitsprüfung, Aufbau der MBOM, Arbeitspläne, Zuordnungsliste |
| Projektleitung des Auftrags | Termin des Übergabepunkts, Eskalation bei Terminkonflikt, Führung der offenen Punkte |
| Operations (H. Zeller) | Fertigungsfreigabe erst gegen vorliegendes Übergabeprotokoll |
| Teilprojekt ERP und Stammdaten (O. Bensch) | Anlage und Prüfung der Materialstämme nach POL-IT-006, Dublettenklärung |
| Standort Eisenach (A. Puhl, für BU Compressor Systems Dr. F. Steinbach) | gleiche Rollen im Infor-Umfeld |
| Qualitätsmanagement (B. Hoffmann) | Stichproben, Nachweisführung, Auslegungsentscheidungen, Auditvorbereitung |

## 6 Ablauf

### 6.1 Voraussetzung

Der Übergabepunkt liegt nach dem Design Freeze des Auftrags. Ohne erreichten Design Freeze findet
keine reguläre Übergabe statt, sondern allenfalls eine Teilübergabe nach 6.7.

### 6.2 Inhalt des Übergabepakets

Die Konstruktion stellt bereit:

1. EBOM im Freigabestand mit Revisionsindex, gezogen aus dem PLM,
2. zugehörigen Zeichnungssatz und Stücklistenanhänge,
3. Werkstoff-, Norm- und Zukaufteilangaben je Position,
4. Kennzeichnung der Langläufer und der bereits beschafften Positionen,
5. Materialnummern nach POL-IT-006; fehlt eine Nummer oder besteht Dublettenverdacht, wird die
   Position gekennzeichnet und an das Teilprojekt Stammdaten gegeben. Eine neue Materialnummer wird
   in dieser Lage nicht auf Zuruf angelegt,
6. Liste der offenen Punkte und der kundenseitigen Änderungsvorbehalte.

### 6.3 Übergabeprotokoll

Die Übergabe wird auf Formblatt QM-08-03-F1 dokumentiert und in der digitalen Projektakte abgelegt.
Das Protokoll trägt zwei Namen: die übergebende und die übernehmende Stelle.

Die Arbeitsvorbereitung prüft innerhalb von zwei Arbeitstagen. Geprüft wird ausschließlich auf
Vollständigkeit nach 6.2, nicht auf technische Richtigkeit der Konstruktion. Diese Begrenzung ist
beabsichtigt: Der Übergabepunkt soll die Durchlaufzeit nicht um eine zweite technische Prüfung
verlängern. Bleibt die Rückmeldung aus, gilt das Paket nach Ablauf der Frist als übernommen; der
Vorgang wird im Statusbericht des Auftrags vermerkt.

### 6.4 Aufbau der MBOM

Die Arbeitsvorbereitung bildet die MBOM im führenden ERP-System des Fertigungsstandorts.
Strukturabweichungen gegenüber der EBOM sind zulässig und ausdrücklich erwünscht, soweit sie
fertigungstechnisch begründet sind - Fertigungsbaugruppen, Zerlegung von Kaufteilsätzen,
Montageeinheiten, Konservierung und Verpackung.

Jede Abweichung wird auf Formblatt QM-08-03-F2 als Zuordnung EBOM-Position zu MBOM-Position
festgehalten. Ohne diese Zuordnungsliste ist die Durchgängigkeit, um die es bei der Maßnahme geht,
nicht gegeben; das Formblatt ist der eigentliche Nachweis, nicht das Übergabeprotokoll.

### 6.5 Übergangsregelung Elektro- und Verfahrenstechnik

Elektrostücklisten entstehen in der EPLAN-Umgebung und werden nicht im PLM geführt. Bis zu einer
anderen Festlegung werden sie als Anlage zum Übergabeprotokoll beigefügt, als Liste und als
Zeichnungssatz. Die Schnittstellenpositionen zwischen mechanischer und elektrischer Struktur
- Antriebe, Sensorik, Schaltschrankanbindung - werden im Übergabeprotokoll gesondert bestätigt.

Das Qualitätsmanagement hält fest, dass die Durchgängigkeit damit für den elektrotechnischen Anteil
noch nicht erreicht ist. Die Regelung ist eine Übergangslösung und als solche zu behandeln.

### 6.6 Änderungen nach der Übergabe

Nach dem Übergabepunkt werden Änderungen an der Fertigungsstruktur ausschließlich über einen ECR
nach POL-ENG-001 ausgelöst. Eine direkte Änderung der MBOM durch die Fertigung ist nicht zulässig.

Ausgenommen sind fertigungsbedingte Korrekturen ohne Auswirkung auf Funktion, Schnittstellen,
Werkstoff, Prüfumfang und Kundenspezifikation, deren Kostenwirkung 500 EUR je Position nicht
übersteigt. Die Arbeitsvorbereitung darf sie unmittelbar in der MBOM vornehmen und meldet sie
wöchentlich gesammelt an die Konstruktion. Diese Ausnahme ist eng zu verstehen; im Zweifel ist der
ECR der schnellere Weg.

### 6.7 Eilfall und Übergabe unter Vorbehalt

Steht der Fertigungsstart vor dem vollständigen Freigabestand, kann eine Teilübergabe erfolgen,
üblicherweise für Langläufer und Rahmenbaugruppen. Voraussetzung:

- Genehmigung durch die Projektleitung und die Leitung Arbeitsvorbereitung, im Protokoll namentlich,
- Benennung des offenen Umfangs und der erwarteten Nachreichung, spätestens fünf Arbeitstage,
- Information an das Qualitätsmanagement am selben Tag,
- Ausweisung des Vorbehalts im Projektstatusbericht bis zur Auflösung.

Eine Übergabe unter Vorbehalt ist kein Regelverstoß, sondern ein dokumentierter Sonderfall. Eine
undokumentierte Vorabfertigung ist ein Regelverstoß.

## 7 Nachweise und Aufbewahrung

Übergabeprotokoll und Zuordnungsliste gehören zur digitalen Projektakte nach POL-QM-001 v2.0 und
werden zehn Jahre aufbewahrt. ECR-Datensätze verbleiben im PLM und werden aus der Projektakte
referenziert. Die Formblätter sind gelenkte Dokumente; Änderungen daran laufen über das
Qualitätsmanagement.

## 8 Wirksamkeit

Ab Mai 2023 werden monatlich erhoben:

- Anteil der Aufträge mit vollständigem Übergabeprotokoll,
- Anteil der Übergaben unter Vorbehalt und deren Auflösungsdauer,
- Anzahl der ECR nach dem Übergabepunkt, getrennt nach Auslöser: Kunde, Konstruktion, Fertigung,
  Lieferant,
- Stichprobe des Qualitätsmanagements: fünf Aufträge je Monat, davon mindestens einer aus Eisenach.

Zur Einordnung einer Beobachtung aus den ersten Wochen: Die Zahl der dokumentierten Engineering
Changes ist seit dem 01.04. deutlich gestiegen. Das Qualitätsmanagement wertet das nicht als Anstieg
der Änderungshäufigkeit, sondern als Sichtbarwerden von Änderungen, die vorher außerhalb der
Dokumentation stattgefunden haben. Erst mit dieser Datenbasis lässt sich überhaupt beurteilen, wo
Änderungen entstehen und welche davon vermeidbar sind. Wer die Zahl als Verschlechterung liest, liest
sie falsch.

Die Rückmeldung aus der Konstruktion, der Zusatzaufwand stehe in keinem Verhältnis zum Nutzen, ist
uns bekannt und ernst zu nehmen. Sie ist der Grund für die Begrenzung der Prüfung in 6.3, für die
Zwei-Tage-Frist und für die Ausnahme in 6.6. Ob das ausreicht, entscheidet die Auswertung nach sechs
Monaten, nicht die Diskussion darüber.

## 9 Abweichungen und Auslegung

Auslegungsfragen gehen an das Qualitätsmanagement. Getroffene Auslegungsentscheidungen werden als
Anhang zu dieser SOP geführt und bei der nächsten Überarbeitung eingearbeitet. Abweichungen von
dieser SOP bedürfen der Zustimmung des Qualitätsmanagements und der betroffenen Fachbereichsleitung.

## 10 Änderungshistorie

| Version | Datum | Änderung |
|---|---|---|
| 1.0 | 25.04.2023 | Erstausgabe, umsetzt POL-ENG-001 v1.1 |
