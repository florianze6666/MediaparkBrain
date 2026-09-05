---
doc_id: LTT-20230411-PROG-00
titel: Einführung einer durchgängigen EBOM-MBOM-Struktur mit formeller Übergabe
dokumenttyp: Entscheidungsvorlage
datum: 2023-04-11
verfasser: Oliver Bensch
rolle: Teilprojektleiter ERP und Stammdaten
organisationseinheit: Programm ONE LTT
empfaenger: [Programmleitung ONE LTT]
projekt: IP-2023-03
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [projektintern, unternehmensweit]
ablageort: projektlaufwerk
---

**Programm ONE LTT - Teilprojekt ERP und Stammdaten**

**Entscheidungsvorlage IP-2023-03/02**

Vorlage an: Programmleitung ONE LTT
Erstellt von: Oliver Bensch, Teilprojektleiter ERP und Stammdaten
Datum: 11. April 2023
Betreff: Verbindliche Anwendung der durchgängigen EBOM-MBOM-Struktur mit formeller Übergabe (PRJ-EBOM-MBOM-2023)
Entscheidungsbedarf bis: 26. April 2023, wegen der Design Freezes im Mai
Mitzeichnung erbeten: Konstruktion mechanisch (M. Gehrke), Operations (H. Zeller), Arbeitsvorbereitung (N. Feld), IT-Applikationen (A. Faber)
Anlagen: Auswertung ECR-Eingang 03.04. bis 06.04.2023 (Anlage 1), Übergabeprotokoll Muster (Anlage 2)

---

## 1 Beschlussvorschlag

Die Programmleitung möge beschließen:

**B1 - Geltungsbereich.** Die formelle Übergabe nach POL-ENG-001 v1.1 gilt ab dem 02.05.2023 verbindlich für alle Kundenprojekte, deren Design Freeze nach diesem Termin liegt, sowie für alle Entwicklungsprojekte ab Gate G4. Projekte mit bereits erfolgtem Design Freeze werden bis zum Abschluss im bisherigen Verfahren geführt.

**B2 - Führende Systeme.** Die EBOM wird in Teamcenter geführt, die MBOM im jeweiligen ERP. Eine parallele MBOM-Pflege im PLM findet nicht statt. Für Eisenach gilt derselbe Grundsatz mit dem dortigen ERP der Infor bis zur Migration in die Zielarchitektur.

**B3 - Änderungen nach Übergabe.** Nach der Übergabe wird die MBOM ausschließlich über Engineering Change Requests geändert. Die bisher teilweise informelle Anpassung durch Arbeitsvorbereitung und Fertigung entfällt. Für Anpassungen ohne Auswirkung auf Funktion, Abnahmefähigkeit und Termin und mit einer Kostenwirkung unter 2.500 EUR wird eine vereinfachte Stufe ECR-B eingeführt, über die die Leitung Arbeitsvorbereitung innerhalb von zwei Arbeitstagen entscheidet.

**B4 - Stammdatenvorbehalt.** Eine Übergabe ist nur zulässig, wenn alle Positionen der EBOM den Anforderungen der Stammdatenrichtlinie POL-IT-006 entsprechen. Gesperrte, dublettenverdächtige und nicht klassifizierte Materialien blockieren die Übergabe. Ausnahmen erteilt die Teilprojektleitung ERP und Stammdaten schriftlich und befristet.

**B5 - Kapazität.** Für die Erstpflege der MBOM in laufenden Projekten werden der Arbeitsvorbereitung bis zum 31.12.2023 1,5 Vollzeitäquivalente aus dem Programmbudget zur Verfügung gestellt.

## 2 Ausgangslage

Die Trennung der Datenhaltung besteht seit der PLM-Einführung 2014 unverändert: mechanische Stücklisten in Teamcenter, kaufmännische Stücklisten im ERP, Projektunterlagen auf Netzlaufwerken. Elektrotechnik und Verfahrenstechnik arbeiten weiterhin außerhalb des PLM, die Schaltanlagendokumentation entsteht in EPLAN. Eine vollständige Erzeugnisstruktur eines Projekts liegt damit bis heute in keinem System vor; sie wird bei Bedarf aus drei Quellen zusammengetragen.

Die Fertigung und die Arbeitsvorbereitung ändern die technische Stückliste bisher teilweise informell. Positionen werden zusammengefasst, Halbzeuge getauscht, Zukaufteile durch verfügbare Alternativen ersetzt. Das ist im Tagesgeschäft eingespielt und funktioniert, weil die Beteiligten sich kennen. Es führt aber dazu, dass die gebaute Anlage und die dokumentierte Anlage auseinanderlaufen, und zwar ohne Nachweis, an welcher Stelle.

Für das Teilprojekt ERP und Stammdaten ist das kein Randthema, sondern die Grundlage der Migration. Wir bereinigen derzeit einen Bestand von mehr als 180.000 Materialnummern mit Dubletten, projektspezifischen Einmalteilen, unterschiedlichen Benennungslogiken und Altmaterial ohne Sperrstatus, mit dem Ziel, die Zahl aktiver Materialstämme um 40 Prozent zu senken. Eine bereinigte Materialbasis nützt wenig, wenn die Struktur darüber weiterhin an zwei Stellen und in zwei Ausprägungen entsteht.

Mit POL-ENG-001 v1.1 gilt die formelle Übergabe seit dem 01.04.2023. PRJ-EBOM-MBOM-2023 ist gestartet. Was fehlt, ist die Festlegung, für welche Projekte sie tatsächlich gilt und was nach der Übergabe erlaubt bleibt. Genau darüber wird derzeit in jeder Projektbesprechung neu verhandelt.

## 3 Sachstand seit dem 03.04.2023

In den vier Arbeitstagen vom 03. bis 06.04.2023 sind 47 Engineering Change Requests eingegangen. Im ersten Quartal lag der Eingang im Mittel bei neun je Woche. 37 der 47 Vorgänge betreffen Änderungen, die vor dem 01.04. ohne eigenen Vorgang abgewickelt worden wären.

Ich halte fest, weil die Zahl bereits unterschiedlich gelesen wird: Das ist kein Anstieg der Änderungen, sondern ein Anstieg der dokumentierten Änderungen. Der Umfang der Eingriffe in die Stückliste war vorher derselbe, er war nur nicht sichtbar. Wer die Kennzahl als Verschlechterung liest, misst die Wirkung der Maßnahme als ihren Schaden.

Die Rückmeldungen fallen erwartungsgemäß auseinander. Aus der Konstruktion wird der Aufwand für Erstellung und Pflege der Übergabeprotokolle kritisiert; das Verfahren gilt dort als zusätzliche Bürokratie in einem Jahr, in dem ohnehin mehr als 80 größere Kundenprojekte parallel laufen und die Konstrukteure der Engpass sind. Die Arbeitsvorbereitung und Operations bewerten dieselbe Regelung als überfällig, weil die Fertigung seit Jahren mit Ständen arbeitet, deren Herkunft im Zweifel nicht mehr rekonstruierbar ist. Beide Bewertungen sind für sich nachvollziehbar. Sie lassen sich nicht auflösen, indem man das Verfahren offenlässt.

## 4 Begründung des Vorschlags

**Zielarchitektur.** Das Programm folgt dem Leitsatz, den Standard möglichst unverändert zu nutzen. Der Standard trennt Entwicklungs- und Fertigungsstückliste. Führen wir beide weiterhin vermischt, bleiben nur zwei Wege: Anpassung des Standards, was dem Programmansatz widerspricht und im Budget nicht hinterlegt ist, oder eine Migration, deren Ausgangsdaten die Zielstruktur nicht abbilden. Die Entscheidung, die jetzt ansteht, ist also nicht, ob wir EBOM und MBOM trennen, sondern ob wir es vor oder nach der Migration tun.

**Stammdaten.** Die Übergabe ist die einzige Stelle im Prozess, an der die Datenqualität eines Projekts vollständig geprüft werden kann. Ohne den Vorbehalt aus B4 transportieren wir die Dubletten, die wir gerade entfernen, über die MBOM wieder in den produktiven Bestand.

**Erfahrung mit dem Design Freeze.** Der Design Freeze gilt seit 2019 formal. In der Praxis werden bei strategisch wichtigen Kunden weiterhin Änderungen danach akzeptiert, und die Zahl verspäteter Engineering Changes ist seither gestiegen. Eine Regel, die formal gilt und deren Ausnahme niemand genehmigen muss, wird zur Ausnahme. Deshalb schlage ich einen engen Geltungsbereich mit hartem Vorbehalt vor und nicht einen weiten mit Ermessensspielraum. Lieber weniger Projekte im Verfahren, aber dort ohne Umgehung.

**Zugeständnis.** Die vereinfachte Stufe ECR-B in B3 ist bewusst als Entlastung gedacht. Die Kritik aus der Konstruktion trifft im Kern die Durchlaufzeit, nicht das Prinzip. Wenn jede Klemmenleistenanpassung denselben Weg nimmt wie eine Änderung am Verdichterstrang, verliert das Verfahren innerhalb weniger Monate seine Akzeptanz.

## 5 Geprüfte Alternativen

| Alternative | Bewertung |
|---|---|
| Verschiebung bis nach der ERP-Migration | Verlagert den Aufwand in die Migrationsphase, in der die Organisation am wenigsten Kapazität hat. Die Altstände müssten dann rückwirkend strukturiert werden. Nicht empfohlen. |
| MBOM ebenfalls in Teamcenter führen | Technisch kurzfristig einfacher, weil die Konstruktion in einem System bliebe. Die Struktur wäre in der Zielarchitektur nicht tragfähig und müsste erneut umgebaut werden. Nicht empfohlen. |
| Freiwillige Anwendung, Auswertung nach sechs Monaten | Führt nach der Erfahrung mit dem Design Freeze dazu, dass gerade die kritischen Großprojekte ausgenommen werden. Nicht empfohlen. |

## 6 Auswirkungen

Der zusätzliche Aufwand je Projekt liegt nach den bisherigen vier Übergaben bei zwei bis drei Personentagen in der Konstruktion und drei bis fünf Personentagen in der Arbeitsvorbereitung, letzteres stark abhängig von der Materialstammqualität. Belastbar ist diese Schätzung noch nicht; sie beruht auf vier Vorgängen, davon zwei aus derselben Baureihe.

Die Erstpflege der MBOM in den 14 Projekten, deren Design Freeze noch vor dem Jahresende liegt, ist mit dem heutigen Personalstand der Arbeitsvorbereitung nicht darstellbar. Daher der Antrag unter B5.

Schulungsbedarf besteht für die Key User in Konstruktion, Arbeitsvorbereitung und Projektleitung; zwei Halbtagestermine je Standort, Durchführung im Mai, Vorbereitung durch das Teilprojekt.

## 7 Risiken

| Risiko | Gegenmaßnahme |
|---|---|
| Durchlaufzeit im Änderungsprozess steigt, Termine in laufenden Projekten geraten unter Druck | ECR-B nach B3; wöchentliche Auswertung des Rückstands ab Mai |
| Kapazität der Arbeitsvorbereitung reicht nicht aus | B5; andernfalls Reduktion des Geltungsbereichs auf Projekte über 1 Mio EUR Auftragswert |
| Umgehung über nachträgliche Korrektur der EBOM statt ECR | Übergabestand wird versioniert und schreibgeschützt abgelegt |
| Eisenach führt die MBOM strukturell abweichend | Abstimmung mit dem Standort steht aus, siehe Abschnitt 8 |
| Materialstammbereinigung liegt hinter dem Plan, Vorbehalt B4 blockiert Projekte | befristete Ausnahmen durch das Teilprojekt, Nachweis im Monatsbericht |

## 8 Offene Punkte und Beteiligung

Wie die strukturgleiche Abbildung der MBOM im Eisenacher ERP der Infor technisch erfolgt, ist nicht abschließend geklärt. Ein gemeinsamer Termin mit dem Standort und der Business Unit Compressor Systems ist für die 17. Kalenderwoche vorgesehen. Sollte sich zeigen, dass eine strukturgleiche Abbildung dort nur mit erheblichem Aufwand möglich ist, wäre B2 für Eisenach bis zur Migration auszusetzen. Ich sehe diesen Fall derzeit nicht, kann ihn aber nicht ausschließen.

Ebenfalls offen ist die Behandlung der Elektro- und Verfahrenstechnik. Solange deren Stücklistenanteile außerhalb des PLM entstehen, ist die EBOM bei der Übergabe unvollständig. Dieser Punkt gehört nicht in diese Vorlage, muss aber im Teilprojekt Engineering im zweiten Halbjahr entschieden werden.

Eine Mitbestimmungsrelevanz nach BV-2023-01 besteht nach hiesiger Einschätzung nicht: Es wird kein System eingeführt oder geändert, und es entstehen keine personenbezogenen Auswertungen. Die Datenschutzbeauftragte ist informiert.

## 9 Entscheidung

Zustimmung zu B1 bis B5:

Programmleitung ONE LTT, Datum, Unterschrift

Abweichender Beschluss / Auflagen:
