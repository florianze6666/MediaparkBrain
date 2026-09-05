---
doc_id: LTT-20221126-IT-04
titel: "Risikoregister: Programmrisiken zum Start erfassen"
dokumenttyp: Risikoregister
datum: 2022-11-26
verfasser: Karin Löbner
rolle: Leiterin IT
organisationseinheit: IT
empfaenger: []
projekt: IP-2022-03
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [projektintern, management]
ablageort: projektlaufwerk
---

# Risikoregister Programm ONE LTT

Vorgang: IP-2022-03, intern geführt unter dem Programmnamen Project Atlas
Version: 0.1, Erstaufnahme
Stand: 26.11.2022
Aufgestellt von: K. Löbner, Leiterin IT
Grundlage: Projektauftrag Programm ONE LTT vom 10.11.2022; Projektmanagement-Standard POL-PM-001 v1.1, Abschnitt Risiko-Register
Bewertungsrunde: 24.11.2022, Besprechungsraum Fulda. Teilnehmer A. Faber (IT-Applikationen), S. Bruckner (Informationssicherheit), G. Sattler (PMO). U. Damm terminlich verhindert, Rückmeldung angekündigt
Verteiler: Geschäftsführung (Kessler, Heine, Mahlberg), PMO, Controlling, Standortleitung Eisenach
Fortschreibung: monatlich; Übergang in die Verantwortung der Programmleitung, sobald diese benannt ist

## 1. Vorbemerkung

Der Projektauftrag ist beschlossen, das Budget mit 14,8 Mio EUR über drei Jahre festgelegt. Die
Programmleitung ist noch nicht benannt, und der Umsetzungsansatz wird derzeit festgelegt. Der
PM-Standard verlangt das Risiko-Register zum Kick-off. Ich lege es vorher an, weil ein Teil dieser
Risiken davon abhängt, wie der Umsetzungsansatz ausfällt, und weil eine Liste, die erst nach dieser
Festlegung entsteht, sie nicht mehr beeinflussen kann.

Die Sicht ist die der IT. Ich nehme Risiken aus Markt, Auftragsabwicklung und Personal nur dort auf,
wo sie unmittelbar auf die Umsetzung durchschlagen. Controlling, PMO und die vier Business Units
müssen ergänzen; Abschnitt 5 nennt die Lücken, die ich selbst sehe.

Bewertung: E Eintrittswahrscheinlichkeit 1 bis 5, A Auswirkung 1 bis 5, R = E mal A. Ab R gleich oder
über 15 ist eine Maßnahme mit Termin und Verantwortlichem verbindlich. Alle Einträge stehen mit dieser
Erstaufnahme auf "offen"; ein Statusfeld führe ich ab Version 0.2.

Acht von zwanzig Einträgen liegen über der Schwelle. Das ist für eine Erstaufnahme viel. Ich habe die
Bewertungen aus der Runde vom 24.11. nicht nach unten korrigiert.

Das Register liegt als Arbeitsdatei im Programmordner auf dem Projektlaufwerk; diese Fassung ist der
Ausdruck des Standes vom 26.11.

## 2. Programmumfang, auf den sich die Bewertung bezieht

Nach Projektauftrag umfasst ONE LTT: ERP, CRM, PLM-Integration, Projektportfolio, Beschaffung, MES,
Data Warehouse, Reporting und Serviceplattform. Das sind neun Vorhaben, von denen sieben in Systeme
eingreifen, die heute im Betrieb sind, und zwei Systeme betreffen, die es bei uns noch nicht gibt
(CRM, MES). Die Bewertung unten unterstellt keinen Umsetzungsansatz, weil keiner festgelegt ist. Wo
die Bewertung davon abhängt, ist es vermerkt.

## 3. Register

### A - Steuerung und Kapazität

| ID | Risiko | E | A | R | Maßnahme | Verantwortlich | Termin |
|---|---|---:|---:|---:|---|---|---|
| R-01 | Der Programmumfang von neun Vorhaben übersteigt die Umsetzungskapazität des Hauses, wenn er überwiegend parallel gefahren wird. Folge: alle Vorhaben verzögern sich gleichzeitig, ohne dass eines fertig wird | 4 | 5 | 20 | Umfang in eine begründete Reihenfolge bringen und je Vorhaben einen frühesten Start festlegen; Entscheidung Teil der Festlegung des Umsetzungsansatzes | Programmleitung, bis dahin GF | mit Umsetzungsansatz |
| R-02 | Programmleitung nicht benannt, Umsetzungsansatz offen. Ausschreibungsunterlagen, Terminplan und Budgetzuordnung hängen daran und können bis dahin nicht erstellt werden | 3 | 4 | 12 | Benennung und Freistellung der Programmleitung; Zwischenzeit nicht mit Vorarbeiten füllen, die später verworfen werden müssen | GF | offen |
| R-03 | Key-User aus Vertrieb, Konstruktion, Arbeitsvorbereitung und Fertigung stehen wegen des seit September stark gestiegenen Auftragseingangs nicht im geplanten Umfang zur Verfügung | 4 | 4 | 16 | Benannte Key-User je Vorhaben mit fester Stundenzusage; Zusage durch die jeweilige Bereichsleitung, nicht durch das Programm | PMO (Sattler) mit Bereichsleitungen | 31.01.2023 |
| R-04 | Die IT kann Betrieb und Programm nicht parallel tragen. Aus dem laufenden Betrieb sind dauerhaft höchstens zwei Personen freistellbar, und auch das nur mit Verzicht an anderer Stelle | 4 | 4 | 16 | Personelle Verstärkung oder ausdrückliche Entscheidung, welche Betriebs- und Weiterentwicklungsthemen 2023 ruhen; Vorlage durch mich | Löbner | 15.12.2022 |

### B - Fachliche Passung

| ID | Risiko | E | A | R | Maßnahme | Verantwortlich | Termin |
|---|---|---:|---:|---:|---|---|---|
| R-05 | Unser Geschäft ist überwiegend Einzel- und Auftragsfertigung mit hohem Montage- und Inbetriebnahmeanteil. Standardsoftware bildet das nur teilweise ab. Folge: umfangreiches Customizing, danach eingeschränkte Releasefähigkeit und dauerhaft höhere Betriebskosten | 4 | 4 | 16 | Vor der Ausschreibung eine Liste der Prozesse, bei denen wir uns dem Standard anpassen, und derjenigen, bei denen wir es nicht tun; Entscheidung durch GF, nicht durch das Projektteam | Löbner, Sattler | 28.02.2023 |
| R-06 | Nutzen eines MES in Kassel ist unklar. In Eisenach mit mechanischer Bearbeitung und Prüfständen ist die Datenlage tragfähig, in Kassel überwiegt Baugruppenmontage mit kleinen Losen. Folge: Erfassungsaufwand ohne belastbaren Gegenwert | 3 | 3 | 9 | Getrennte Betrachtung Kassel und Eisenach vor der Ausschreibung | Faber mit Zeller, Puhl | 31.03.2023 |
| R-07 | Das PLM wird seit der Einführung 2014 im Wesentlichen von der mechanischen Konstruktion genutzt. Eine PLM/ERP-Integration setzt voraus, dass Elektrotechnik und Verfahrenstechnik ebenfalls darin arbeiten. Diese Ausweitung ist nicht beschlossen und ist kein IT-Thema | 4 | 3 | 12 | Klärung mit Gehrke und Wiesner, ob die Ausweitung Bestandteil des Programms ist; wenn nein, Integrationsumfang entsprechend kleiner schneiden | Löbner | 31.01.2023 |
| R-08 | Für CRM gibt es kein Vorsystem. Vertriebsdaten liegen heute in Tabellen und im ERP, ein beschriebener Vertriebsprozess über die Marktbereiche hinweg existiert nicht. Ein CRM ohne vorherige Prozessbeschreibung bildet die heutige Uneinheitlichkeit nur ab | 3 | 3 | 9 | Prozessaufnahme Vertrieb vor Auswahl | Vertrieb (Ostermann) mit Faber | 30.04.2023 |

### C - Daten und Integration

| ID | Risiko | E | A | R | Maßnahme | Verantwortlich | Termin |
|---|---|---:|---:|---:|---|---|---|
| R-09 | Artikel-, Stücklisten-, Kunden- und Lieferantenstämme aus Kassel und Eisenach sind nie abgeglichen worden. Umfang der Dubletten, Schlüsselkonflikte und der Migrationsaufwand sind heute nicht schätzbar. Folge: der Aufwand fällt zu spät auf und trifft den Termin | 5 | 4 | 20 | Stammdatenaufnahme über beide Standorte als eigenständige Vorarbeit, vor der ersten Ausschreibung, mit eigenem Aufwandsansatz | Faber, Damm, Puhl | Start 09.01.2023 |
| R-10 | Zwei ERP-Landschaften seit 2018. Ein Migrationspfad für Eisenach ist nie festgelegt worden; die Entscheidung von damals lautete, das Geschäft zuerst zu integrieren. Sie ist bis heute nicht revidiert worden | 4 | 4 | 16 | Der Umsetzungsansatz muss die Behandlung Eisenachs ausdrücklich enthalten, einschließlich der Frage, ob Eisenach zuerst, zuletzt oder gleichzeitig umgestellt wird | GF, Programmleitung | mit Umsetzungsansatz |
| R-11 | In Eisenach und in mehreren Fachbereichen in Kassel laufen lokale Datenbank- und Tabellenlösungen, die produktiv genutzt, aber nicht inventarisiert sind. Bei einer Ablösung fallen Anforderungen erst beim Abschalten auf | 4 | 3 | 12 | Inventar der lokalen Anwendungen je Bereich, mit Nutzer, Zweck und Datenquelle | Faber | 28.02.2023 |
| R-12 | Reihenfolgeabhängigkeit: Data Warehouse und Reporting liefern erst dann belastbare Zahlen, wenn die Vorsysteme stehen. Werden sie parallel begonnen, entstehen Auswertungen auf Datenständen, die sich noch ändern | 4 | 3 | 12 | Abhängigkeiten zwischen den neun Vorhaben in einer Übersicht darstellen und dem Umsetzungsansatz beilegen | Löbner | 20.12.2022 |

### D - Kommerziell

| ID | Risiko | E | A | R | Maßnahme | Verantwortlich | Termin |
|---|---|---:|---:|---:|---|---|---|
| R-13 | Es ist nicht definiert, ob die 14,8 Mio EUR die internen Aufwände enthalten. Bei diesem Umfang liegen die internen Personalaufwände in einer Größenordnung, die die Aussage des Budgets verändert | 4 | 4 | 16 | Verbindliche Abgrenzung durch das Controlling, schriftlich, vor der ersten Teilvorlage | Anselm, Heine | 31.01.2023 |
| R-14 | Lizenz-, Subskriptions- und Betriebskosten nach Produktivsetzung sind laufender Aufwand und fallen ab 2024 im IT-Budget an, nicht im Programmbudget. Ohne vorherige Aufstockung verdrängen sie den Betrieb der Bestandssysteme | 4 | 4 | 16 | Mehrjährige Betriebskostenschätzung je Vorhaben, Fortschreibung des IT-Budgetrahmens ab 2024 | Löbner mit Anselm | 28.02.2023 |
| R-15 | Teilvorhaben ab 2 Mio EUR benötigen je eine Investitionsvorlage mit NPV, IRR und Szenarien nach der seit Juli geltenden Richtlinie. Für Integrations- und Stammdatenvorhaben ist der Nutzen schwer zu quantifizieren, weil er erst über die abnehmenden Vorhaben wirkt | 3 | 3 | 9 | Frühzeitige Abstimmung der Nutzenlogik mit dem Controlling, damit Vorlagen nicht in der Vorprüfung scheitern | Löbner, Anselm | 31.03.2023 |
| R-16 | Ein Programm dieser Breite ist ohne externen Implementierungspartner nicht zu leisten. Die Beratungskapazität für 2023 ist knapp, und ein einziger Partner über alle neun Vorhaben erzeugt eine Abhängigkeit, aus der wir während der Laufzeit nicht herauskommen | 3 | 4 | 12 | Vergabe nicht als Gesamtpaket; Ausstiegs- und Übergaberegelungen sowie Dokumentationspflichten in die Verträge; Beteiligung des strategischen Einkaufs von Beginn an | Ehlers, Damm | mit erster Vergabe |

### E - Organisation, Recht, Betrieb

| ID | Risiko | E | A | R | Maßnahme | Verantwortlich | Termin |
|---|---|---:|---:|---:|---|---|---|
| R-17 | MES, Projektportfolio und Serviceplattform erzeugen personenbezogene Daten über Arbeitsleistung, Zeiten und Einsätze. Diese Systeme sind mitbestimmungspflichtig. Wird der Gesamtbetriebsrat erst zur Produktivsetzung beteiligt, verschiebt sich der Termin, und zwar unabhängig davon, wie gut die Technik ist | 3 | 4 | 12 | Beteiligung von Datenschutz und Gesamtbetriebsrat vor der Ausschreibung, nicht vor dem Go-live; Zweckbindung der erhobenen Daten bereits in die Anforderungsunterlagen aufnehmen | Kirchner, Kroll, Löbner | 28.02.2023 |
| R-18 | Neun Systeme mit steigendem Cloud-Anteil vergrößern Angriffsfläche und Berechtigungsverwaltung. Das Rollenmodell nach POL-IT-001 v2.0 ist für den heutigen Systembestand gebaut, nicht für diesen. Beurteilung nach Cloud- und SaaS-Richtlinie POL-IT-003 ist je Vorhaben erforderlich | 3 | 4 | 12 | Sicherheitsbeurteilung als fester Bestandteil jeder Auswahlentscheidung, nicht als nachgelagerte Prüfung; Rollenmodell mit dem ersten Vorhaben überarbeiten | Bruckner | je Auswahlentscheidung |
| R-19 | Rotterdam, Brno, Shanghai und Houston kommen im Programmumfang nicht vor. Sie arbeiten heute mit lokalen Lösungen an den Kasseler Systemen vorbei. Bleiben sie außen vor, entsteht die dritte Landschaft neben Kassel und Eisenach | 3 | 2 | 6 | Klärung, ob die Auslandsstandorte im Umfang enthalten sind; wenn nein, ausdrücklich als Abgrenzung im Programmauftrag vermerken | Programmleitung | 31.03.2023 |
| R-20 | Der Betrieb läuft während der gesamten Umstellung weiter, einschließlich Werkabnahmen, Remote-FAT und der digitalen Projektakte nach POL-QM-001 v2.0. Bei hohem Auftragsbestand kollidieren Umstellungsfenster mit Abnahme- und Versandterminen | 3 | 3 | 9 | Umstellungsfenster mit der Auftragsplanung abstimmen, nicht umgekehrt; Abstimmung im monatlichen S&OP | Zeller, Damm | ab Terminplanung |

## 4. Was ich vor der Festlegung des Umsetzungsansatzes für notwendig halte

Das ist meine Einschätzung, keine Beschlusslage.

1. Die Stammdatenaufnahme (R-09) beginnt vor jeder Ausschreibung. Sie ist die einzige Vorarbeit, die
   unabhängig vom gewählten Ansatz in jedem Fall gebraucht wird, und sie ist die Position, bei der
   ich die größte Abweichung zwischen Schätzung und Wirklichkeit erwarte.
2. Das Inventar der lokalen Anwendungen (R-11) beginnt gleichzeitig. Ohne dieses Inventar kennen wir
   den abzulösenden Bestand nicht und schreiben gegen ein unvollständiges Bild aus.
3. Die Abgrenzung des Budgets (R-13) und die Betriebskosten nach Produktivsetzung (R-14) müssen
   geklärt sein, bevor die erste Investitionsvorlage geschrieben wird. Beides betrifft mein Budget
   unmittelbar, und beides lässt sich später nicht mehr sauber nachziehen.
4. Ich halte eine Reihenfolge für tragfähiger als Gleichzeitigkeit. Wir haben zwei ERP-Landschaften,
   ein nur teilweise genutztes PLM und keine abgeglichenen Stammdaten. Neun Vorhaben, die alle
   gleichzeitig auf diese Ausgangslage treffen, teilen sich dieselben Menschen und dieselben Daten.
   Welche Reihenfolge richtig ist, ist damit nicht gesagt.
5. Datenschutz und Gesamtbetriebsrat werden vor der Ausschreibung eingebunden (R-17). Bei der
   Einführung der Kollaborationsplattform 2020 war die Zustimmung binnen zwei Wochen möglich, weil
   die Zweckbindung der Daten vollständig geregelt war. Diesen Weg halte ich für den schnelleren.

## 5. Nicht bewertet

Die folgenden Bereiche kann ich nicht beurteilen und habe sie deshalb weggelassen, nicht weil ich sie
für unkritisch halte:

- Nutzenannahmen und Wirtschaftlichkeitsrechnung des Programms (Controlling)
- Auswirkungen auf Angebots- und Abwicklungsprozesse der vier Business Units
- Personalgewinnung und Qualifizierung für die neuen Systeme (Personal)
- Markt- und Auftragsentwicklung 2023 bis 2025 als Rahmenbedingung des Terminplans
- Vertragsrechtliche Risiken der Vergaben

## 6. Weiteres Vorgehen

Rückmeldungen und Ergänzungen bitte bis 09.12.2022 an mich oder an Frau Faber. Die Abhängigkeitsübersicht
nach R-12 lege ich bis zum 20.12. bei. Version 0.2 stelle ich in der ersten Programmsitzung vor und
übergebe das Register anschließend an die Programmleitung.

K. Löbner
