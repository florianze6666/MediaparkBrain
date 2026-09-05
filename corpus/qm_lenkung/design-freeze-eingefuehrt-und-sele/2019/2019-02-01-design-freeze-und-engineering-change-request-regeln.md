---
doc_id: LTT-20190201-QM-00
titel: Design Freeze und Engineering Change Request
dokumenttyp: SOP
datum: 2019-02-01
verfasser: Bernd Hoffmann
rolle: Leiter Qualitätsmanagement
organisationseinheit: QM
empfaenger: ["-"]
projekt: PRJ-DESIGNFREEZE-2019
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit]
ablageort: qm_lenkung
---

Lahnberg Thermotechnik GmbH & Co. KG
Gelenktes Dokument nach POL-QM-001 Dokumentenlenkung

Dokumentnummer: POL-ENG-001
Titel: Design Freeze und Engineering Change Request
Revision: 1.0, gültig ab 01.02.2019
Ersetzt: keine Vorgängerfassung
Erstellt: 01.02.2019, B. Hoffmann, Leiter Qualitätsmanagement
Geprüft: G. Sattler (PMO), Dr. I. Sommer (Central Engineering), R. Wiesner (Elektrotechnik und Automatisierung)
Freigegeben: Dr. J. Mahlberg, technischer Geschäftsführer
Verteiler: Geschäftsführung, Marktbereiche, Central Engineering, Konstruktion mechanisch, Elektrotechnik und Automatisierung, Technology & Development, Operations Kassel und Eisenach, Arbeitsvorbereitung, Einkauf, Controlling, PMO, Projektleitungen, Qualitätsmanagement
Ablage: QM-Lenkung, Verzeichnis Verfahrensanweisungen Engineering
Nächste turnusmäßige Überprüfung: Februar 2020

---

## 1 Zweck und Anlass

Die Geschäftsführung hat zum 01.01.2019 einen formellen Design-Freeze-Meilenstein in Kundenprojekten
eingeführt. Nach diesem Meilenstein sollen technische Änderungen ausschließlich über einen
Engineering Change Request (ECR) laufen.

Diese Verfahrensanweisung beschreibt, wie der Design Freeze festgelegt, wie ein ECR beantragt,
bewertet, entschieden und umgesetzt wird und welche Nachweise dabei entstehen. Sie regelt außerdem
den Fall, dass eine Änderung nach dem Design Freeze aus kommerziellen Gründen angenommen wird.

Anlass ist eine über die letzten Geschäftsjahre gestiegene Zahl technischer Änderungen in späten
Projektphasen. Der Aufwand dieser Änderungen trifft Konstruktion, Arbeitsvorbereitung, Einkauf und
Montage gleichzeitig und ist heute nicht durchgängig einer Ursache und einem Verursacher zuzuordnen.
Für das Qualitätsmanagement ist das der eigentliche Befund: nicht die Änderung selbst, sondern die
fehlende Nachvollziehbarkeit. Änderungen, die an der Konstruktionsablage vorbei vereinbart und erst
im Fertigungsauftrag sichtbar werden, sind weder auditierbar noch nachkalkulierbar, und sie sind bei
Gewährleistungsfällen im Nachhinein nicht mehr zu rekonstruieren.

Diese Verfahrensanweisung verbietet keine späte Änderung. Sie verlangt, dass jede Änderung nach dem
Design Freeze einen Antrag, eine Bewertung, eine namentliche Entscheidung und einen Eintrag im
Änderungsverzeichnis des Projekts hat.

## 2 Geltungsbereich

Gilt für alle Kundenprojekte der Marktbereiche mit einem Auftragswert über 500.000 EUR sowie für alle
Entwicklungsprojekte ab Gate G3 nach POL-RD-001. Gilt für die Standorte Kassel und Eisenach.

Für Komponenten, die in Eisenach konstruiert oder gefertigt werden, gilt das Verfahren unverändert;
die daraus folgende Pflege der Auftrags- und Stücklistendaten erfolgt im dortigen ERP durch die
Eisenacher Arbeitsvorbereitung.

Nicht anzuwenden auf: Serviceaufträge und Ersatzteile ohne Konstruktionsänderung, Angebotsphase vor
Auftragseingang, redaktionelle Korrekturen an Dokumenten ohne Auswirkung auf Bauteil, Funktion,
Schnittstelle, Kosten oder Termin.

## 3 Begriffe

**Design Freeze.** Projektmeilenstein, zu dem der technische Umfang für die weitere Abwicklung
verbindlich festgelegt ist. Maßgeblich ist der zu diesem Zeitpunkt freigegebene Stand der
Anlagenspezifikation, der Verfahrensschemata, der Aufstellungs- und Rohrleitungsplanung, der
mechanischen Stücklisten im PLM sowie der E-Planung in EPLAN.

**Engineering Change Request (ECR).** Antrag auf Änderung eines nach dem Design Freeze verbindlichen
technischen Standes. Der ECR ist Antrag und Nachweis zugleich; er wird auch dann geführt, wenn die
Änderung bereits gegenüber dem Kunden zugesagt wurde.

**Änderungsklassen.** Die Klasse bestimmt Bewertungstiefe und Entscheidungsebene.

| Klasse | Merkmal | Entscheidung |
|---|---|---|
| A | Änderung an Funktion, Leistungsdaten, Schnittstellen zum Kunden, Sicherheits- oder Abnahmerelevanz; Auswirkung über 50.000 EUR oder auf einen Vertragstermin | Change Board |
| B | Änderung an Bauteilen, Werkstoffen, Zukaufkomponenten oder Fertigungsumfang ohne Auswirkung auf Leistungsdaten; Auswirkung bis 50.000 EUR | Projektleitung gemeinsam mit der zuständigen Konstruktionsleitung |
| C | Änderung ohne Auswirkung auf Kosten, Termin und Funktion, zum Beispiel Korrektur eines Zeichnungsfehlers, Bauteiltausch bei identischer Spezifikation | zuständige Konstruktionsleitung |

Die Einstufung nimmt die Projektleitung im Antrag vor. Bei Zweifel gilt die höhere Klasse.

**Change Board.** Monatliche Sitzung im Anschluss an das Projektreview nach POL-PM-001. Feste
Teilnehmer: Projektleitung des betroffenen Projekts, Central Engineering, PMO, Operations,
Arbeitsvorbereitung, Einkauf, Controlling, Qualitätsmanagement. Der zuständige Marktbereich wird
eingeladen. Bei fristkritischen Anträgen der Klasse A entscheidet das Board im Umlauf.

## 4 Zuständigkeiten

| Rolle | Aufgabe |
|---|---|
| Projektleitung | setzt den Design-Freeze-Termin im Meilensteinplan, stellt den ECR, stuft ein, führt das Änderungsverzeichnis des Projekts |
| Central Engineering | fachliche Verantwortung für den Design Freeze, technische Bewertung, Vollständigkeit des Änderungsstandes |
| Konstruktion mechanisch, Elektrotechnik und Automatisierung | Aufwandsschätzung, Umsetzung, Index- und Stücklistenpflege |
| Arbeitsvorbereitung | Bewertung der Fertigungsauswirkung, Rückmeldung zu bereits gestarteten Fertigungsaufträgen |
| Einkauf | Bewertung von Bestell- und Lieferantenauswirkungen, Stornokosten, Wiederbeschaffungszeiten |
| Controlling | kaufmännische Bewertung, Zuordnung zu Nachtrag oder eigenem Aufwand |
| Marktbereich | Verhandlung des Nachtrags mit dem Kunden |
| PMO | Terminwirkung, Ressourcenwirkung, Einladung und Protokoll des Change Board |
| Qualitätsmanagement | Lenkung dieser Anweisung und der Formblätter, Vollständigkeitsprüfung der Nachweise, Stichproben, Auswertung |
| technischer Geschäftsführer | Freigabe von Ausnahmen nach Abschnitt 7 |

## 5 Festlegung des Design Freeze

5.1 Der Design-Freeze-Termin wird im Kick-off festgelegt und im Meilensteinplan geführt. Er liegt
regelmäßig vor Beginn der Beschaffung langlaufender Komponenten.

5.2 Voraussetzung für den Design Freeze ist die dokumentierte Freigabe der Anlagenspezifikation durch
den Kunden sowie das Vorliegen der im Angebotsreview nach POL-VTR-001 Rev. 2.0 protokollierten
Annahmen zu Wärmequelle und Betriebsbedingungen in bestätigter Form.

5.3 Der Design Freeze wird von der Projektleitung und Central Engineering gemeinsam erklärt und im
Projektstatusbericht des Folgemonats vermerkt. Der eingefrorene Stand wird als Dokumentenliste mit
Index festgehalten und im Projektordner abgelegt.

5.4 Ein Projekt ohne erklärten Design Freeze wird im Projektreview als offener Punkt geführt.

## 6 Ablauf des Engineering Change Request

6.1 **Antrag.** Antragsberechtigt sind Projektleitung, Central Engineering, Konstruktion,
Arbeitsvorbereitung, Operations, Einkauf und Marktbereich. Der Antrag erfolgt auf dem Formblatt
FB-ENG-001-01 mit Kennzeichen ECR-<Projektnummer>-<lfd. Nr.>. Anzugeben sind: Auslöser und Herkunft
der Änderung, betroffene Dokumente und Baugruppen mit Index, Beschreibung des Ist- und des
Soll-Standes, vorgeschlagene Klasse, Dringlichkeit.

Als Herkunft ist eine der folgenden Angaben zu wählen: Kundenanforderung, Fehler in der eigenen
Auslegung, Lieferantenbedingt, Normen- oder Genehmigungsauflage, Optimierung ohne äußeren Anlass.
Diese Angabe ist auswertungsrelevant und darf nicht offen bleiben.

6.2 **Technische Bewertung.** Central Engineering bewertet innerhalb von fünf Arbeitstagen
Machbarkeit, Auswirkung auf Leistungsdaten und Schnittstellen sowie den Konstruktionsaufwand.
Betroffene Fachbereiche werden beteiligt; für E-Technik ist die Bewertung wegen der getrennten
Planungsstände in EPLAN gesondert einzuholen und nicht aus der mechanischen Bewertung abzuleiten.

6.3 **Kaufmännische und terminliche Bewertung.** Arbeitsvorbereitung, Einkauf, Operations und
Controlling melden innerhalb von fünf Arbeitstagen Mehr- oder Minderaufwand, Materialkosten,
Stornokosten, Wiederbeschaffungszeiten und Auswirkung auf die Projekttermine. Bereits gestartete
Fertigungsaufträge und bereits bestellte Zukaufteile sind ausdrücklich zu benennen.

6.4 **Entscheidung.** Die Entscheidung erfolgt nach Klasse gemäß Abschnitt 3 und wird auf dem
Formblatt mit Datum und Namen vermerkt. Zulässige Ergebnisse: freigegeben, freigegeben mit Auflagen,
zurückgestellt, abgelehnt. Bei Kostenwirkungen ist zusätzlich die Unterschriftenregelung nach
POL-FIN-001 einzuhalten. Wird die Änderung als Nachtrag gegenüber dem Kunden geltend gemacht, ist der
Verhandlungsstand im ECR zu vermerken; ein noch nicht beauftragter Nachtrag ist kein
Umsetzungshindernis, aber im Statusbericht als offenes kommerzielles Risiko zu führen.

6.5 **Umsetzung und Nachweis.** Erst nach Entscheidung werden Zeichnungen, Stücklisten und
E-Planung geändert und mit neuem Index freigegeben. Die Projektleitung schließt den ECR ab, wenn
alle betroffenen Dokumente den neuen Index tragen und die Änderung in den Fertigungs- und
Bestelldaten nachgeführt ist. Ein ECR ohne Abschluss bleibt offen und erscheint in der monatlichen
Auswertung.

6.6 **Sofortmaßnahmen.** Erfordert eine Situation auf der Baustelle oder im Prüffeld eine sofortige
technische Entscheidung, wird sie getroffen und innerhalb von drei Arbeitstagen als ECR nachgereicht.
Die Nachreichung ist verpflichtend und nicht ersetzbar durch einen Vermerk im Montagebericht.

## 7 Änderungen nach dem Design Freeze auf Kundenwunsch

Die Geschäftsführung hat entschieden, dass Änderungswünsche strategisch wichtiger Kunden auch nach
dem Design Freeze angenommen werden können. Diese Anweisung ändert daran nichts und regelt
ausschließlich das Verfahren.

7.1 Die Zusage an den Kunden erfolgt durch den Marktbereich im Einvernehmen mit dem technischen
Geschäftsführer. Vor der Zusage ist die technische Bewertung nach 6.2 einzuholen; ist das aus
Terminfristen nicht möglich, ist das im ECR zu vermerken.

7.2 Jede so angenommene Änderung wird als ECR der Klasse A geführt, unabhängig von ihrer
Kostenwirkung, und im Formblatt als Ausnahme nach Abschnitt 7 gekennzeichnet.

7.3 Die Ausnahme wird namentlich gezeichnet. Eine mündliche Zusage ohne nachfolgenden ECR ist keine
zulässige Grundlage für eine Konstruktions- oder Fertigungsänderung.

7.4 Die Konstruktion setzt Änderungen nach dem Design Freeze nur auf Grundlage eines entschiedenen
ECR um. Diese Festlegung ist der Kern der Anweisung. Bei den Entwicklungsgates nach POL-RD-001 ist
seit 2015 zu beobachten, dass Umfänge, die als Projektengineering bezeichnet werden, an der
vorgesehenen Entscheidung vorbeilaufen. Ein Verfahren, das nur solange gilt, wie es niemanden stört,
erzeugt Dokumentation ohne Steuerungswirkung und ist im Audit schwerer zu vertreten als eine
dokumentierte Ausnahme.

## 8 Dokumentation und Ablage

8.1 Der ausgefüllte ECR wird im Projektordner auf dem Projektlaufwerk abgelegt, Verzeichnis
Änderungen, Dateiname entsprechend dem ECR-Kennzeichen.

8.2 Die Projektleitung führt je Projekt ein Änderungsverzeichnis mit ECR-Kennzeichen, Datum, Klasse,
Herkunft, Entscheidung, Kosten- und Terminwirkung sowie Status. Das Verzeichnis wird bis zur
Verfügbarkeit einer Unterstützung im PLM als Tabelle nach Vorlage FB-ENG-001-02 geführt.

8.3 Die geänderten technischen Dokumente werden im führenden System indexiert: mechanische
Stücklisten und Zeichnungen im PLM, E-Planung in EPLAN, kaufmännische Stücklisten und
Fertigungsaufträge im ERP des jeweiligen Standorts. Eine Änderung gilt erst als umgesetzt, wenn alle
betroffenen Systeme nachgeführt sind.

8.4 Aufbewahrung nach POL-QM-001 zusammen mit der Projektakte.

## 9 Auswertung

Das Qualitätsmanagement wertet monatlich aus und berichtet an PMO und technische Geschäftsführung:
Anzahl der ECR je Projekt und Klasse, Anteil der Ausnahmen nach Abschnitt 7, Verteilung der Herkunft
nach 6.1, Anzahl offener ECR älter als 30 Tage, Anzahl nachgereichter Sofortmaßnahmen nach 6.6.

Die Auswertung dient der Beurteilung des Verfahrens, nicht der Bewertung einzelner Mitarbeiter oder
Projektleitungen. Personenbezogene Auswertungen finden nicht statt.

Erste Auswertung: April 2019 für das erste Quartal. Bewertung der Wirksamkeit dieser Anweisung
gemeinsam mit PMO und Central Engineering im dritten Quartal 2019.

## 10 Mitgeltende Unterlagen

- POL-QM-001 Dokumentenlenkung
- POL-PM-001 Projektmanagement-Standard, Rev. 1.1
- POL-VTR-001 Technische Angebotsreview, Rev. 2.0
- POL-RD-001 Stage-Gate-Prozess, Rev. 1.1
- POL-ENG-002 Plattform- und Modulstandard der Modulplattform M1
- POL-FIN-001 Genehmigungsschwellen und Unterschriftenregelung
- POL-FIN-003 Projektcontrolling und Projektmargenberichterstattung
- FB-ENG-001-01 Engineering Change Request
- FB-ENG-001-02 Änderungsverzeichnis Projekt

## 11 Änderungsdienst dieser Anweisung

Änderungen an dieser Anweisung erfolgen über das Qualitätsmanagement nach POL-QM-001. Rückmeldungen
aus der Anwendung werden gesammelt und in die Überprüfung nach Abschnitt 9 eingebracht.

| Rev. | Datum | Änderung | Bearbeiter |
|---|---|---|---|
| 1.0 | 01.02.2019 | Erstausgabe | B. Hoffmann |
