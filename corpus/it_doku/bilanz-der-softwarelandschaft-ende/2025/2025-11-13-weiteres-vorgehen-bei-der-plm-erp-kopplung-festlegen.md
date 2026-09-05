---
doc_id: LTT-20251113-IT-01
titel: "Architekturentscheidung: Weiteres Vorgehen bei der PLM-ERP-Kopplung festlegen"
dokumenttyp: Architekturentscheidung
datum: 2025-11-13
verfasser: Dr. Philipp Nowak
rolle: CIO
organisationseinheit: IT
empfaenger: ["-"]
projekt: "-"
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [bereichsintern, management]
ablageort: it_doku
---

**Architekturentscheidung AE-IT-2025-04**

Gegenstand: Kopplung von PLM und ERP im Bereich der Stücklisten
Status: entschieden, gültig ab 13.11.2025
Entscheidung getroffen durch: CIO
Fachlich beteiligt: Central Engineering, Konstruktion mechanisch, Arbeitsvorbereitung, Stammdaten, IT-Applikationen
Wiedervorlage: nach Abschluss der Pilotphase, spätestens im dritten Quartal 2026
Ablage: IT-Dokumentation, Architekturentscheidungen 2025

## 1 Anlass

Die Management Summary zur Systemlandschaft vom 14.10.2025 führt die PLM-ERP-Integration erneut unter
den nicht umgesetzten Vorhaben. Das ist die dritte Bestandsaufnahme in Folge mit demselben Eintrag.
In der Applikationsrunde und in den Gesprächen mit Central Engineering wird seither in kurzen
Abständen gefragt, wann die Integration denn nun komme. Ich beantworte diese Frage hier einmal
verbindlich, statt sie weiter offen mitzuführen.

Ich halte vorab fest, was den Kern des Problems ausmacht: Das Zielbild von 2022 sah eine durchgängige
Engineering- und Manufacturing-Stückliste vor. Im Juni 2024 wurde genau dieser Teil zurückgestellt,
zusammen mit dem MES und der konzernweiten Serviceplattform. Zurückgestellt heisst nicht widerrufen,
und deshalb lebt die Erwartung in der Organisation weiter. Solange das nicht korrigiert ist, wird die
IT an einem Auftrag gemessen, den sie seit anderthalb Jahren nicht mehr hat.

## 2 Ausgangslage

Das PLM ist seit 2014 im Einsatz und wird bis heute im Wesentlichen von der mechanischen Konstruktion
genutzt. Die Elektrotechnik arbeitet in EPLAN, die Verfahrenstechnik und die Projektleitung arbeiten
ausserhalb. Diese Aufteilung ist keine Folge der letzten Jahre, sie ist der Zustand seit der
Einführung.

Daraus ergibt sich die bekannte Dreiteilung: konstruktive Stückliste im PLM, kaufmännische Stückliste
und Materialstamm im ERP, Projektunterlagen auf Netzlaufwerken und in SharePoint. Der ERP-Wechsel im
Oktober 2024 hat daran nichts geändert. Er hat die kaufmännische Seite auf ein System gebracht und
das führende System für Materialstamm, Beschaffung und Projektkostenrechnung eindeutig gemacht. Für
den Konstruktionsstand bleibt das PLM führend.

Die formelle Übergabe von der EBOM in die MBOM ist seit April 2023 durch POL-ENG-001 in der Fassung
1.1 vorgeschrieben. Das Werkzeug, das sie tragen sollte, war Teil des zurückgestellten Umfangs. Die
Übergabe findet also seit zweieinhalb Jahren von Hand statt: die Konstruktion stellt frei, die
Arbeitsvorbereitung legt die Fertigungsstückliste im ERP an, geprüft wird im Vier-Augen-Prinzip. Die
Anwendungsbetreuung zählt für die ersten drei Quartale 2025 im Mittel rund 55 solcher Übergaben je
Monat. In etwa jedem achten Fall wird nachträglich korrigiert, überwiegend wegen abweichender
Mengeneinheiten und wegen Positionen, die im ERP unter einem zweiten Materialstamm geführt werden.
Die Materialstammbereinigung ist über die 2023 erreichten Werte nicht wesentlich hinausgekommen; das
ist für die hier zu treffende Entscheidung der eigentlich harte Punkt.

In Eisenach bestehen die lokalen Systeme fort. Verdichterkonstruktion und Gießerei sind an das PLM
nicht angebunden, ein MES gibt es dort nicht. Für die Kopplung, um die es hier geht, ist Eisenach
damit kein Kandidat, sondern eine eigene Aufgabe.

## 3 Geprüfte Optionen

**Option A - Wiederaufnahme des Zielbilds.** Bidirektionale Integration von PLM und ERP,
durchgängige Automatisierung der EBOM-MBOM-Überleitung, Rückmeldung von Fertigungsständen ins PLM,
beide Standorte. Technisch machbar, aber sie setzt bereinigte Materialstämme, harmonisierte
Arbeitspläne und eine geklärte Datenverantwortung je Materialklasse voraus. Keine dieser drei
Voraussetzungen ist heute gegeben. Eine Wiederaufnahme würde denselben Weg noch einmal gehen, den wir
2023 gegangen sind, und sie überschreitet die Schwelle der Investitionsrichtlinie deutlich. Ich
verfolge sie nicht.

**Option B - enge gerichtete Schnittstelle.** Übergabe der freigegebenen mechanischen EBOM in das ERP
in einer Richtung, begrenzt auf plattformkonforme Baugruppen nach POL-ENG-002 in der Fassung 2.0.
Sonderkonstruktion bleibt im manuellen Verfahren. Deckt nach Auswertung der Übergaben des laufenden
Jahres etwa vier von zehn Fällen ab und lässt die Prozessregel unverändert.

**Option C - Verzicht.** Fortschreibung des manuellen Verfahrens, dafür strengere Prüf- und
Protokollpflichten. Billig, ehrlich und für die Arbeitsvorbereitung die schlechteste Antwort. Der
Aufwand bleibt, wo er heute liegt, nämlich bei den Kollegen, die ihn seit 2023 zusätzlich tragen.

## 4 Entscheidung

Wir setzen Option B um, mit folgendem Schnitt:

- Richtung ausschliesslich vom PLM in das ERP. Keine Rückschreibung, kein Abgleich in beide
  Richtungen. Das PLM bleibt führend für den Konstruktionsstand, das ERP für Materialstamm und
  Fertigungsstückliste.
- Umfang sind die mechanischen Stücklisten plattformkonformer Module der Produktlinien ProcessLift
  und GeoQuart. Alles, was als Sonderkonstruktion geführt wird, läuft weiter über die manuelle
  Übergabe nach POL-ENG-001.
- Standort Kassel. Eisenach ist nicht Teil dieser Entscheidung.
- EPLAN und die verfahrenstechnische Auslegung bleiben ausserhalb.
- Keine Beschaffung einer eigenen Integrationsplattform. Umgesetzt wird auf der mit der ERP-Suite
  bereits lizenzierten Integrationsschicht. Damit bleiben wir innerhalb der Cloud- und
  SaaS-Richtlinie und erzeugen keine zusätzliche Abhängigkeit.
- Zwei Pilotprojekte, je eines aus Industrial Heat Systems und District und Geo Energy, danach
  Entscheidung über die Ausweitung.

Zugleich stelle ich fest, dass das Zielbild einer vollständig durchgängigen Engineering- und
Manufacturing-Stückliste in der Fassung von 2022 nicht länger die Architekturvorgabe der IT ist. Wer
gegen dieses Zielbild plant, plant gegen eine Vorgabe, die seit Juni 2024 nicht mehr gilt. Ich bitte
Central Engineering und das Project Excellence Office, das in ihren Unterlagen entsprechend
nachzuziehen.

## 5 Was hiermit ausdrücklich nicht entschieden ist

Damit aus dieser Entscheidung nicht mehr gelesen wird, als in ihr steht:

- Anbindung Eisenach und die MES-Frage. Offen, und sie gehört fachlich zu Compressor Systems und zur
  Standortleitung, nicht in eine Schnittstellenentscheidung der IT.
- Harmonisierung der Arbeitspläne. Offen, ohne sie bleibt die Überleitung auch im automatisierten Fall
  auf die Stückliste beschränkt.
- Einheitliche Dokumentenablage. Offen, wird im Rahmen der digitalen Projektakte weitergeführt.
- Rückführung von Fertigungsrückmeldungen ins PLM. Nicht vorgesehen.
- Ablösung lokaler Excel-Lösungen im Engineering. Läuft über die Excel-Governance nach POL-IT-005 und
  nicht über diese Schnittstelle.

## 6 Konsequenzen

Aufwand nach heutiger Schätzung rund 120 interne Personentage, überwiegend in der
Anwendungsbetreuung und in der Konstruktion, dazu externe Unterstützung im niedrigen sechsstelligen
Bereich. Das liegt klar unterhalb der Schwelle der Investitionsrichtlinie, eine Investitionsvorlage mit
NPV und Szenarioanalyse ist daher nicht erforderlich. Die Betriebskosten führe ich nach POL-FIN-002 in
der Fassung 1.1 im Applikationsbudget 2026 mit, sie sind gering, weil keine neue Lizenz hinzukommt.

Die Entlastung ist begrenzt und ich sage das lieber vorher als hinterher: Bei etwa vier von zehn
Übergaben entfällt die manuelle Anlage, bei den übrigen bleibt alles wie bisher. Wer sich von dieser
Massnahme das Ende der Doppelpflege verspricht, wird enttäuscht werden.

Bedingung für den Start der Pilotphase ist die Benennung der Datenverantwortung je Materialklasse nach
POL-IT-006. Ohne sie schreibt die Schnittstelle die vorhandenen Dubletten schneller fort, als wir sie
heute von Hand bereinigen. Ich mache den Start davon abhängig.

Mitbestimmung: Die Schnittstelle verarbeitet Stücklisten- und Materialdaten. Personenbezogene Daten
entstehen nach meiner Einschätzung nicht; die im PLM geführten Bearbeiterkennungen werden nicht
übertragen. Eine Teilvereinbarung nach BV-2023-01 halte ich deshalb nicht für erforderlich. Die
Unterrichtung des Gesamtbetriebsrats erfolgt trotzdem mit der Systembeschreibung, bevor die
Pilotphase beginnt. Das ist mir nach den Erfahrungen mit dem Projekt-Dashboard im vergangenen Jahr
wichtig, auch wenn ich die Sachlage hier anders bewerte.

## 7 Nächste Schritte

| Schritt | Verantwortlich | Termin |
|---|---|---|
| Systembeschreibung und Datenkatalog erstellen | Andrea Faber | 12.12.2025 |
| Datenverantwortung je Materialklasse benennen | Oliver Bensch mit Central Engineering | 16.01.2026 |
| Abgrenzung plattformkonform gegen Sonderkonstruktion festschreiben | Martin Gehrke | 16.01.2026 |
| Unterrichtung Gesamtbetriebsrat | CIO | vor Pilotstart |
| Pilotstart mit zwei Projekten | Andrea Faber | Februar 2026 |
| Auswertung und Entscheidung über Ausweitung | CIO | nach Pilotabschluss |

Rückfragen zur fachlichen Abgrenzung bitte an Central Engineering, Rückfragen zur technischen
Umsetzung an die IT-Applikationen.

Nowak
