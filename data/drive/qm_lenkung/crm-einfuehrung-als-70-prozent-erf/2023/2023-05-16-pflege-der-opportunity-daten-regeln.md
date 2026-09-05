---
doc_id: LTT-20230516-SAL-03
titel: Pflege der Opportunity-Daten im CRM
dokumenttyp: SOP
datum: 2023-05-16
verfasser: Jana Ostermann
rolle: Leiterin Vertrieb
organisationseinheit: Vertrieb
empfaenger: ["-"]
projekt: PRJ-CRM-2023
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit, bereichsintern]
ablageort: qm_lenkung
---

**Lahnberg Thermotechnik GmbH & Co. KG - Gelenktes Dokument**

Dokument-Nr.: LTT-20230516-SAL-03
Version: 1.0
Gültig ab: 01.06.2023
Ersteller: Jana Ostermann, Leiterin Vertrieb
Fachliche Prüfung: Dieter Anselm (Controlling), Andrea Faber (IT-Applikationen)
Freigabe: Jana Ostermann, Leiterin Vertrieb
Dokumentenlenkung: Qualitätsmanagement, Ablage nach POL-QM-001 v2.0
Turnusmäßige Überprüfung: bis 31.05.2024

# 1. Zweck

Diese Arbeitsanweisung regelt, wie Verkaufschancen (Opportunities) im CRM angelegt, fortgeschrieben
und abgeschlossen werden. Sie soll sicherstellen, dass die Pipeline und der monatlich berichtete
erwartete Auftragseingang aus einem einzigen Datenbestand stammen und dass dieser Datenbestand zum
Zeitpunkt des Forecast-Meetings belastbar ist.

Anlass ist die Produktivsetzung des CRM (Microsoft Dynamics 365) im Frühjahr 2023 im Rahmen von
PRJ-CRM-2023. Mit ihr besteht erstmals eine konzernweite Sicht auf Opportunity Pipeline,
Kundenkontakte, Angebotsstatus und erwarteten Auftragseingang. Diese Sicht ist nur so gut wie der
Pflegestand der einzelnen Opportunity.

# 2. Geltungsbereich

Für alle Mitarbeiterinnen und Mitarbeiter mit Vertriebsverantwortung in den Business Units
Industrial Heat Systems, District & Geo Energy, Compressor Systems und Lifecycle & Service sowie an
den Standorten Kassel, Eisenach, Rotterdam, Houston, Shanghai und Brno.

Nicht im Geltungsbereich: Angebote und Aufträge, die ausschließlich über Rahmenabrufe abgewickelt
werden (siehe Abschnitt 8), sowie die Abwicklung nach Auftragseingang.

# 3. Begriffe

**Opportunity** - eine konkrete, einem Kunden zugeordnete Verkaufschance mit erwartetem Volumen und
erwartetem Auftragsmonat. Ein allgemeines Interesse ohne Kundenzuordnung ist keine Opportunity.

**Erwarteter Auftragseingang** - das gewichtete Volumen aller Opportunities eines Monats, gewichtet
mit der Wahrscheinlichkeit der jeweiligen Phase nach Abschnitt 5.

**Datenstand** - der Inhalt des CRM zum letzten Arbeitstag eines Monats, 18:00 Uhr. Er ist die
Grundlage des Forecast-Meetings des Folgemonats.

# 4. Zuständigkeiten

| Rolle | Aufgabe |
|---|---|
| Vertriebsmitarbeiter, Key Account Manager | legt die Opportunity an, pflegt sie, schließt sie ab |
| Regionale Vertriebsleitung | prüft den Pflegestand ihrer Region vor dem Datenstand |
| Key User Vertrieb der Region | erste Anlaufstelle bei Fragen zu Feldern und Phasen |
| Commercial Project Management | liefert Angebotswert und Angebotsnummer bei Projekten mit kaufmännischer Begleitung |
| Controlling | konsolidiert den Forecast, führt keine Änderungen an Opportunities durch |
| Leitung Vertrieb | entscheidet über Ausnahmen nach Abschnitt 8 |

Die inhaltliche Verantwortung für eine Opportunity liegt bei der Person, die im Feld "verantwortlicher
Vertriebsmitarbeiter" eingetragen ist. Sie kann nicht an das Controlling, an das Backoffice oder an
den Key User delegiert werden.

# 5. Phasen und Pflichtfelder

| Phase | Bezeichnung | Wahrscheinlichkeit | zusätzlich zu pflegende Felder |
|---|---|---|---|
| A0 | Lead erfasst | 10 % | Kunde, Land, Business Unit, Kurzbezeichnung |
| A1 | Qualifiziert | 25 % | erwartetes Volumen, erwarteter Auftragsmonat, verantwortlicher Vertriebsmitarbeiter |
| A2 | Angebot abgegeben | 50 % | Angebotsnummer, Angebotswert, Angebotsdatum, Wettbewerbssituation |
| A3 | In Verhandlung | 75 % | bestätigter Auftragsmonat, offene kaufmännische Punkte |
| A4 | Auftrag erhalten | 100 % | Auftragsnummer aus dem ERP |
| A9 | Verloren oder nicht weiterverfolgt | 0 % | Verlustgrund, Wettbewerber sofern bekannt |

Die Felder gelten kumulativ: eine Opportunity in A3 trägt auch die Felder aus A0 bis A2.

Der Wechsel nach A2 setzt bei einem Angebotswert über 500.000 EUR die durchgeführte technische
Angebotsreview nach POL-VTR-001 v2.0 voraus. Die Kennung der Angebotsreview ist im Feld "Bemerkung
Angebot" zu vermerken. Ohne diesen Vermerk gilt die Opportunity im Forecast weiterhin als A1.

**Reduzierter Pflichtfeldumfang in A0 und A1.** Über die oben genannten Felder hinaus ist in den
Phasen A0 und A1 kein weiteres Feld auszufüllen, auch wenn das System es derzeit noch als Pflichtfeld
kennzeichnet. Die entsprechende Anpassung der Systemkonfiguration ist bei IT-Applikationen beantragt.
Bis dahin ist es zulässig, in nicht benötigten Textfeldern einen Bindestrich einzutragen.

# 6. Aktualisierungsrhythmus

| Fall | Frist |
|---|---|
| Phasenwechsel | innerhalb von drei Arbeitstagen |
| Opportunities in A2 oder A3 über 250.000 EUR | wöchentlich, spätestens freitags 12:00 Uhr |
| alle übrigen Opportunities | monatlich, spätestens am 25. des Monats |
| Auftragseingang (A4) oder Verlust (A9) | innerhalb von fünf Arbeitstagen nach Kenntnis |
| Verschiebung des erwarteten Auftragsmonats | sofort, spätestens vor dem nächsten Datenstand |

Eine Opportunity, die seit mehr als 90 Tagen unverändert in A1 oder A2 steht, wird durch die
regionale Vertriebsleitung angesprochen und entweder aktualisiert oder nach A9 geschlossen. Eine
Pipeline, die nur wächst, ist kein Qualitätsmerkmal.

# 7. Forecast-Meeting

Das Forecast-Meeting findet monatlich am dritten Arbeitstag statt. Teilnehmer sind die Leitung
Vertrieb, die regionalen Vertriebsleitungen, je eine Vertretung der Business Units und das
Controlling.

Grundlage ist ausschließlich der Datenstand nach Abschnitt 3. Zahlen aus persönlichen Listen,
Tabellen oder Notizen werden im Forecast-Meeting nicht mehr entgegengenommen. Wer eine Abweichung
zum CRM-Stand sieht, korrigiert sie vorher im System, nicht mündlich im Termin.

Ab dem 01.07.2023 ist die aus dem CRM erzeugte Pipeline-Auswertung im Berichtsdienst (Power BI) die
einzige berichtete Pipeline. Parallel geführte Excel-Listen der Regionen sind ab diesem Zeitpunkt
keine Berichtsgrundlage mehr; die Übernahme der Altdaten in das CRM erfolgt bis zum 30.06.2023 durch
die Key User der Regionen.

Der konsolidierte erwartete Auftragseingang wird an den monatlichen Sales-and-Operations-Planning-
Prozess nach POL-SCM-002 v1.0 übergeben. Verspätet gepflegte Opportunities erscheinen dort erst im
Folgemonat.

# 8. Ausnahmen

- Rahmenabrufe aus bestehenden Verträgen werden nicht als Einzel-Opportunity geführt, sondern je
  Kunde und Quartal als Sammelposition.
- Serviceaufträge unter 25.000 EUR werden nicht einzeln erfasst; die Servicedisposition meldet den
  erwarteten Monatswert als Sammelposition an das Controlling.
- Vertrauliche Vorgänge, bei denen der Kunde eine Nennung im System ausdrücklich untersagt hat,
  werden anonymisiert unter der Kundengruppe geführt. Die Freigabe erteilt die Leitung Vertrieb im
  Einzelfall.

Weitere Ausnahmen sind schriftlich bei der Leitung Vertrieb zu beantragen. Eine nicht gepflegte
Opportunity ist keine Ausnahme, sondern eine offene Aufgabe.

# 9. Nicht Gegenstand dieser Anweisung

Auswertungen aus dem CRM erfolgen auf Ebene Business Unit, Region, Kunde und Phase. Eine Auswertung
des Pflegeverhaltens einzelner Mitarbeiterinnen und Mitarbeiter ist nicht vorgesehen und nicht
Zweck dieser Anweisung. Die Rahmenvereinbarung zur Einführung und Änderung von IT-Systemen vom
16.03.2023 bleibt unberührt.

Ebenfalls nicht geregelt sind Kundenstammdaten, Kontaktdaten und Dublettenpflege im CRM. Hierzu ist
eine gesonderte Regelung des Programms angekündigt.

# 10. Mitgeltende Unterlagen

- POL-QM-001 v2.0, Dokumentenlenkung
- POL-VTR-001 v2.0, Technische Angebotsreview
- POL-SCM-002 v1.0, Sales and Operations Planning
- POL-FIN-003 v1.0, Projektcontrolling und Projektmargenberichterstattung
- Schulungsunterlage Vertrieb, Pflichtfelder und Forecast, 06.05.2023

# 11. Anmerkung der Vertriebsleitung

Die Kritik aus dem Vertrieb an der Zahl der Pflichtfelder ist berechtigt, soweit sie die frühen
Phasen betrifft. Ein Lead, den ich nach zwei Telefonaten wieder schließe, rechtfertigt keine
zwanzig Eingaben. Deshalb ist der Umfang in A0 und A1 in dieser Anweisung bewusst klein gehalten.

Ab A2 gilt das Gegenteil. Ein abgegebenes Angebot bindet Engineering-Kapazität, geht in die
Kalkulation und in die Planung ein und muss vollständig im System stehen. Wer erst am Vorabend des
Forecast-Meetings pflegt, liefert keine Prognose, sondern eine nachträgliche Bestätigung.

Den Feldkatalog werde ich im vierten Quartal 2023 gemeinsam mit den regionalen Vertriebsleitungen
und der Programmleitung erneut durchgehen. Bis dahin gilt diese Fassung.

# 12. Änderungshistorie

| Version | Datum | Änderung |
|---|---|---|
| 1.0 | 16.05.2023 | Erstausgabe |
