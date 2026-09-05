---
doc_id: LTT-20231106-PROG-00
titel: Risikoregister ONE LTT - offene Voraussetzungen für den Go-live
dokumenttyp: Risikoregister
datum: 2023-11-06
verfasser: Dr. Simone Hartwig
rolle: Programmleiterin ONE LTT
organisationseinheit: Programm
empfaenger: "-"
projekt: ONE LTT
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [projektintern, management]
ablageort: projektlaufwerk
---

# Risikoregister ONE LTT

| | |
|---|---|
| Programm | ONE LTT (PRJ-ONELTT) |
| Registerstand | 06.11.2023, Fassung 2023-11 |
| Vorfassung | 04.09.2023 (Fassung 2023-09) |
| Geführt von | Dr. Simone Hartwig, Programmleitung |
| Zuarbeit | Teilprojektleitungen, IT-Applikationen, PMO |
| Grundlage | POL-PM-001 v1.1, POL-PM-002 v1.0 in der seit 01.10.2023 geltenden Auslegung |
| Fortschreibung | monatlich, nächste Fassung zum Monatsreview am 04.12.2023 |
| Verteiler | Steering Committee ONE LTT, Teilprojektleitungen, PMO, Leitung IT-Applikationen |

## 1 Zweck und Abgrenzung

Das Register führt die Risiken, die den Produktivstart des konzernweiten ERP mit den angeschlossenen
Bausteinen zum Halbjahreswechsel 2024 gefährden. Es ersetzt die Fassung vom 04.09.2023 vollständig.

Anlass für die vorgezogene Überarbeitung ist die Bestandsaufnahme in der Woche vom 30.10. Sie hat
ergeben, dass mehrere Voraussetzungen, die im Programmplan als bis Ende 2023 erledigt geführt werden,
zum jetzigen Zeitpunkt nicht vorliegen: Materialstämme, Stücklisten, Arbeitspläne,
Projektstrukturen, Rollen und Berechtigungen, die PLM-Schnittstellen, die Datenmigration und die
Servicehistorien. Das ist keine Liste von Einzelbefunden mehr, sondern ein Muster, und es betrifft
durchgehend Daten und Entscheidungen, die nicht im Programm entstehen, sondern in der Linie.

Nicht Gegenstand dieses Registers sind die kaufmännischen Projektrisiken der Kundenprojekte; sie
laufen weiter über die Risikoregister der Business Units. Ebenfalls nicht enthalten sind Risiken des
Regelbetriebs der bestehenden Systeme, soweit sie ohne Bezug zum Cutover sind.

## 2 Bewertungsmaßstab

Eintrittswahrscheinlichkeit (EW) und Auswirkung (A) je 1 bis 5, Risikowert als Produkt.

Die Einstufung folgt POL-PM-002 in der seit 01.10.2023 geltenden Auslegung. Danach gilt ein
Sachverhalt als

- **gelb**, sobald ein geplanter Zwischenstand ohne genehmigten Nachholplan überschritten ist,
- **rot**, sobald ein Zwischenstand betroffen ist, der auf dem Cutover-Pfad liegt, oder sobald eine
  beschlossene Maßnahme länger als vier Wochen ohne benannten Verantwortlichen offen steht.

Die Verschärfung wirkt sich hier deutlich aus. Sieben der unten geführten Positionen wären nach der
bis September angewandten Auslegung gelb gewesen; sie stehen jetzt auf Rot, ohne dass sich der
Sachverhalt selbst verschlechtert hätte. Ich halte das für richtig so, weise aber darauf hin, weil
der Vergleich mit der Septemberfassung sonst einen Absturz suggeriert, den es in dieser Form nicht
gegeben hat.

Trend gegenüber 04.09.2023: `+` verbessert, `=` unverändert, `-` verschlechtert, `n` neu.

## 3 Register

| ID | Risiko | Ursache | Wirkung bei Eintritt | EW | A | Wert | Stufe | Trend | Verantwortlich | Termin |
|---|---|---|---|---:|---:|---:|---|---|---|---|
| R-01 | Materialstämme nicht migrationsfähig | Bereinigung hinter Plan, Dubletten und Einmalteile weiterhin aktiv, uneinheitliche Benennung | Cutover nicht durchführbar, Bestandsführung und Disposition fehlerhaft | 4 | 5 | 20 | rot | = | O. Bensch | 31.01.2024 |
| R-02 | EBOM-MBOM-Struktur nur in Teilen aufgebaut | Übergabe Konstruktion/Produktion erst für Neuprojekte etabliert, Altprojekte ohne MBOM | Fertigungsaufträge im Zielsystem nicht ableitbar | 4 | 5 | 20 | rot | - | M. Gehrke, N. Feld | 15.03.2024 |
| R-03 | Arbeitspläne unvollständig, besonders Eisenach | Zeitgerüste historisch in lokalen Datenbanken und Tabellen, nie systemseitig gepflegt | Vorkalkulation und Kapazitätsplanung im Zielsystem ohne Basis | 4 | 4 | 16 | rot | - | H. Zeller, N. Feld | 15.03.2024 |
| R-04 | Kein einheitlicher Projektstrukturstandard | Vier Business Units mit unterschiedlicher Gliederungstiefe, Einigung mehrfach vertagt | Projektkostentransparenz wird nicht erreicht, eines der Kernziele des Programms | 4 | 4 | 16 | rot | - | G. Sattler | 15.12.2023 |
| R-05 | Rollen- und Berechtigungskonzept nicht final | Rollenmodell nach POL-IT-001 v2.0 bildet die Zielarchitektur nicht ab, Abhängigkeit von Teilvereinbarung nach BV-2023-01 | Keine Freigabe für die Integrationstests, kein Produktivsetzen | 4 | 5 | 20 | rot | = | A. Faber, S. Bruckner | 31.01.2024 |
| R-06 | PLM-Schnittstellen nicht spezifiziert | Übergabepunkt PLM nach ERP offen, Elektrotechnik arbeitet weiterhin außerhalb des PLM | Stücklistendurchgängigkeit bleibt unterbrochen, manuelle Nacherfassung | 4 | 4 | 16 | rot | = | A. Faber, R. Wiesner | 29.02.2024 |
| R-07 | Datenmigration ohne belastbaren Probelauf | Bisher nur Teilextrakte, keine vollständige Testmigration über beide ERP-Landschaften | Cutover-Dauer und Fehlerquote unbekannt, Rückfall erst spät erkennbar | 5 | 5 | 25 | rot | - | O. Bensch | 29.02.2024 |
| R-08 | Servicehistorien nicht strukturiert verfügbar | Anlagendokumentation in Netzlaufwerken, Serviceberichte teils in Papierform | Serviceplattform startet ohne Historie, Nutzen für Lifecycle & Service entfällt zunächst | 4 | 3 | 12 | gelb | = | M. Aurich, E. Sandmann | 30.04.2024 |
| R-09 | Process Owner ohne Weisungsbefugnis | Rolle im Programm eingesetzt, disziplinarisch aber nicht verankert | Standards werden nicht gesetzt, Entscheidungen wandern in die Programmleitung | 5 | 5 | 25 | rot | - | S. Hartwig, Eskalation GF | 30.11.2023 |
| R-10 | Key User stehen nicht im geplanten Umfang zur Verfügung | Auslastung in Engineering und Projektleitung, Zusagen werden kurzfristig zurückgezogen | Tests und Schulung verzögern sich, Fachwissen fehlt in der Konfiguration | 4 | 4 | 16 | rot | - | S. Kirchner, BU-Leitungen | 15.12.2023 |
| R-11 | Teilvereinbarungen nach BV-2023-01 nicht verhandelt | Verfahren für ERP, Fertigungssteuerung und Serviceplattform noch nicht begonnen | Produktivsetzung ohne Teilvereinbarung nicht zulässig | 3 | 5 | 15 | gelb | = | S. Kirchner, S. Kroll | 31.01.2024 |
| R-12 | Beratungsaufwand über Plan | Nacharbeit an Stammdaten und Prozessen bindet externe Kapazität länger als kalkuliert | Budgetüberschreitung, Nachbewilligung nach POL-FIN-002 erforderlich | 3 | 4 | 12 | gelb | - | D. Anselm | Forecast 12/2023 |
| R-13 | Parallelbetrieb und Rückfallebene ungeklärt | Beide bestehenden ERP-Landschaften laufen bis zum Cutover produktiv, Abschaltszenario nicht beschrieben | Im Störungsfall kein definierter Rückfall, Auftragsabwicklung gefährdet | 3 | 5 | 15 | gelb | n | A. Faber | 29.02.2024 |
| R-14 | Fit-Gap-Liste wächst gegen den Standardansatz | Anforderungen aus den Business Units werden nachgemeldet, Verzicht wird nicht entschieden | Zusätzlicher Konfigurations- und Testaufwand, Verlust des Standardnutzens | 4 | 3 | 12 | gelb | - | S. Hartwig | laufend |

R-07 ist seit dem 25.09.2023 nicht aktualisiert worden; die Teilprojektleitung war in dieser Zeit
überwiegend in der Stammdatenbereinigung gebunden. Die Bewertung stammt aus meiner eigenen
Einschätzung vom 02.11. und ist mit dem Verantwortlichen noch nicht abgestimmt.

## 4 Erläuterung der roten Positionen

### R-01 und R-07 Stammdaten und Migration

Die Ausgangslage ist bekannt: mehr als 180.000 Materialnummern über beide Standorte, darin
Dubletten, projektspezifische Einmalteile, mehrere Benennungslogiken, unterschiedliche Einheiten und
Altmaterial ohne Sperrstatus. Das ursprüngliche Ziel, den Bestand aktiver Materialstämme um
40 Prozent zu reduzieren, haben wir im Sommer nach unten korrigiert, weil die Prüfung je Position
mehr Fachzeit bindet als angenommen und die Fachbereiche diese Zeit nicht haben. Die Korrektur war
richtig, sie hat aber nichts daran geändert, dass die verbleibende Menge weiterhin bearbeitet werden
muss.

Kritischer als der Bereinigungsstand ist für mich der fehlende Probelauf. Wir haben bisher
Teilextrakte migriert und daraus Fehlerquoten je Objektart abgeleitet. Eine vollständige
Testmigration über beide ERP-Landschaften einschließlich der lokalen Datenbanken in Eisenach hat
nicht stattgefunden. Damit kennen wir weder die tatsächliche Dauer des Cutover-Fensters noch die
Zahl der Objekte, die manuell nachgezogen werden müssen. Solange dieser Wert nicht gemessen ist,
ist jede Aussage zur Machbarkeit des Termins eine Annahme, und Annahmen dieser Art haben wir hier im
Haus schon teuer bezahlt.

Ich beantrage deshalb, den vollständigen Migrationsprobelauf vorzuziehen und ihn nicht erst nach
Abschluss der Bereinigung anzusetzen. Ein Probelauf auf unbereinigtem Bestand liefert eine
schlechtere Datenqualität, aber eine belastbare Zeitmessung, und die Zeitmessung ist im Moment die
wertvollere Information.

### R-02 und R-03 Stücklisten und Arbeitspläne

Die durchgängige EBOM-MBOM-Struktur ist seit April eingeführt und für Neuprojekte etabliert. Die
formelle Übergabe zwischen Konstruktion und Produktion funktioniert dort, wo sie von Anfang an
gefahren wurde. Der Bestand ist das Problem: für laufende Projekte, die vor der Umstellung begonnen
haben, existiert keine fertigungsseitige Stückliste in der Zielstruktur, und niemand hat bisher
entschieden, ob diese Projekte nachgezogen oder im Altsystem ausgelaufen werden.

Bei den Arbeitsplänen ist die Lage in Eisenach deutlich schwieriger als in Kassel. Zeitgerüste sind
dort historisch in lokalen Datenbanken und Tabellen gepflegt worden, teilweise als Erfahrungswerte
einzelner Meister. Diese Werte sind fachlich gut, sie sind nur nirgends in einer Form hinterlegt,
die man migrieren kann. Der Aufwand, sie zu erheben, ist bisher nicht seriös geschätzt.

Beide Punkte sind keine IT-Themen. Sie werden in der Linie gelöst oder gar nicht.

### R-04 Projektstrukturen

Ein einheitlicher Projektstrukturstandard über die vier Business Units ist seit Juni Gegenstand von
vier Abstimmungsrunden gewesen und in jeder Runde vertagt worden. Die Positionen sind nachvollziehbar
und unvereinbar: Industrial Heat Systems und District & Geo Energy planen anlagenbezogen mit tiefer
Gliederung, Compressor Systems in Serienlogik mit flacher Struktur, Lifecycle & Service braucht eine
Struktur, die über die Anlagenlebensdauer stabil bleibt.

Ohne diesen Standard bekommen wir keine vergleichbare Projektkostentransparenz, und
Projektkostentransparenz ist eines der Ziele, mit denen das Programm im November 2022 begründet
wurde. Ich sehe hier keine fachliche Lösung mehr, sondern eine Entscheidung, die getroffen werden
muss, auch gegen einen Teil der Beteiligten.

### R-05 und R-06 Berechtigungen und Schnittstellen

Das Rollenmodell aus POL-IT-001 v2.0 ist 2021 für zwei getrennte Systemlandschaften geschnitten
worden. Es lässt sich auf die Zielarchitektur nicht abbilden, weil dort Rollen quer über
Business Units und Standorte greifen. Der Entwurf für das neue Berechtigungskonzept liegt vor, ist
aber nicht abgenommen, und er hängt an zwei Stellen von der Teilvereinbarung nach BV-2023-01 ab,
weil er festlegt, wer welche personenbezogenen Auswertungen sehen kann. Ohne Abnahme kein
Integrationstest.

Bei den Schnittstellen ist der Übergabepunkt vom PLM in das ERP weiterhin nicht spezifiziert. Erschwerend
kommt hinzu, dass die Elektrotechnik nach wie vor außerhalb des PLM arbeitet. Die Zielarchitektur
setzt eine durchgängige Stückliste voraus; heute endet die Durchgängigkeit an der Grenze zwischen
mechanischer und elektrischer Konstruktion. Diese Grenze ist älter als das Programm, aber sie wird
jetzt zum Cutover-Thema.

### R-09 Process Owner ohne Mandat

Das ist aus meiner Sicht die Position, die die anderen erklärt.

Wir haben Process Owner für die Kernprozesse benannt und ihnen die Aufgabe gegeben, Standards zu
setzen, wo heute unterschiedliche Arbeitsweisen bestehen. Diese Rolle ist mit keiner
disziplinarischen Befugnis hinterlegt. Ein Process Owner, der eine Vereinheitlichung durchsetzen
soll, verhandelt faktisch mit Abteilungsleitungen, die ihm nicht unterstellt sind und deren
Zielvereinbarungen von der Vereinheitlichung nicht berührt werden. Das Ergebnis ist berechenbar: es
wird nicht widersprochen, es wird verschoben. Die Entscheidungen laufen dann bei mir auf, und die
Programmleitung entscheidet über Fachfragen, die sie nicht entscheiden sollte.

Ich habe das im Steering Committee am 12.09. und am 17.10. angesprochen. Beim ersten Mal wurde eine
Klärung zugesagt, beim zweiten Mal auf die Zielvereinbarungsrunde verwiesen. Beides ist keine
Antwort auf die Frage, wer eine Standardentscheidung gegen den Willen eines Fachbereichs treffen
darf.

### R-10 Key User

Die zugesagten Kapazitäten aus den Fachbereichen werden regelmäßig kurzfristig zurückgezogen,
begründet mit Terminen in Kundenprojekten. Bei über achtzig größeren Projekten parallel ist das
nachvollziehbar; es ist nur mit dem Programmplan nicht vereinbar. Aus Engineering und Projektleitung
ist im Oktober eine steigende Zahl von Überlastungsanzeigen gemeldet worden. Ich erwähne das hier
nicht, um die Bereiche zu entlasten, sondern weil eine Planung, die auf Zusagen beruht, die niemand
halten kann, keine Planung ist.

## 5 Was das für den Termin bedeutet

Ich schlage ausdrücklich nicht vor, den Produktivstart jetzt zu verschieben.

Für eine Terminentscheidung fehlt uns die belastbare Messung aus dem Migrationsprobelauf, und eine
Verschiebung, die auf Schätzungen beruht, verlieren wir ein zweites Mal. Was ich vorschlage, ist eine
Entscheidung über die Voraussetzungen: Mandat, Kapazität, Reihenfolge. Wenn diese Entscheidungen bis
Mitte Dezember vorliegen, halte ich den Termin für offen im Sinne von noch erreichbar. Wenn sie
nicht vorliegen, ist die Frage im Februar nicht mehr, ob wir verschieben, sondern um wie viel.

Zur Einordnung gegenüber der Septemberfassung: die Zahl der roten Positionen ist von zwei auf zehn
gestiegen. Sieben davon gehen auf die verschärfte Auslegung zurück, eine ist neu bewertet. Der
Sachstand hat sich in zwei Monaten verschlechtert, aber nicht um diesen Faktor.

## 6 Entscheidungsbedarf

| Nr | Entscheidung | Adressat | benötigt bis |
|---|---|---|---|
| E-1 | Mandat der Process Owner: Weisungsrecht in Standardfragen oder ein benanntes Gremium mit Letztentscheid | Geschäftsführung | 30.11.2023 |
| E-2 | Verbindliche Freistellung der Key User mit fester Stundenzusage je Bereich und Quartal | Geschäftsführung, BU-Leitungen | 15.12.2023 |
| E-3 | Projektstrukturstandard: Festlegung durch die Geschäftsführung, nachdem vier Abstimmungsrunden ergebnislos geblieben sind | Geschäftsführung, PMO | 15.12.2023 |
| E-4 | Vorziehen des vollständigen Migrationsprobelaufs vor Abschluss der Bereinigung | Steering Committee | 04.12.2023 |
| E-5 | Umgang mit laufenden Altprojekten: Nachziehen in die Zielstruktur oder Auslaufen im Altsystem | Steering Committee, BU-Leitungen | 15.01.2024 |
| E-6 | Start des Verfahrens nach BV-2023-01 für ERP, Fertigungssteuerung und Serviceplattform | HR, Recht und Datenschutz | 30.11.2023 |

Zu E-6 eine Anmerkung aus Erfahrung: beim CRM hat das Verfahren von der ersten Befassung im Mai bis
zur Teilvereinbarung Anfang Juli gedauert, und das bei einem System mit vergleichsweise
überschaubarem Datenkatalog. Für drei Systeme gleichzeitig sollten wir mit mehr rechnen. Wenn wir im
Januar beginnen, ist die Teilvereinbarung nicht der kritische Pfad, sondern der Termin selbst.

## 7 Pflege des Registers

Meldungen an die Programmleitung, Aufnahme neuer Positionen jederzeit, Bewertung im Monatsreview.
Positionen werden erst geschlossen, wenn der Verantwortliche den Wegfall der Ursache bestätigt; ein
abgelaufener Termin schließt nichts.

Für R-07 wird die Bewertung nach Abstimmung mit der Teilprojektleitung in der Fassung 2023-12
bestätigt oder korrigiert.
