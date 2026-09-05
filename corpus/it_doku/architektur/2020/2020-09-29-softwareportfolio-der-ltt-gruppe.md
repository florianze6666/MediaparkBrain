---
doc_id: LTT-20200929-IT-A20
titel: Softwareportfolio der LTT-Gruppe 2020
dokumenttyp: Softwareportfolio
datum: 2020-09-29
verfasser: Karin Löbner
rolle: Leiterin IT
organisationseinheit: IT
empfaenger: []
projekt: "-"
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit]
ablageort: it_doku
---

# Softwareportfolio der LTT-Gruppe 2020

Gelenktes Dokument der IT nach POL-QM-001 Dokumentenlenkung

| | |
|---|---|
| Dokumentnummer | LTT-20200929-IT-A20 |
| Version | 1.0 |
| Gültig ab | 29.09.2020 |
| Erstellt | K. Löbner, Leiterin IT |
| Geprüft | Qualitätsmanagement, Dokumentenlenkung |
| Freigegeben | Geschäftsführung |
| Ablage | IT-Dokumentation |
| Turnus | jährlich, nächste Überprüfung 30.09.2021 |

## 1 Zweck und Geltungsbereich

Dieses Dokument führt die Anwendungssysteme der LTT-Gruppe mit Stand vom 29.09.2020 auf. Es gilt für die Lahnberg Thermotechnik GmbH & Co. KG mit den Standorten Kassel, Rotterdam, Brno, Shanghai und Houston sowie für die Rothenberg Verdichtertechnik GmbH in Eisenach.

Das Portfolio ist die Bezugsliste für die Vergabe von Berechtigungen nach POL-IT-001, für Betrachtungen nach der Informationssicherheitsrichtlinie POL-IT-002 und für die Bearbeitung von Beschaffungs- und Änderungsanträgen an die IT.

## 2 Systemübersicht

| Kennung | Anwendung | Hersteller | Produktiv seit | Geltungsbereich |
|---|---|---|---|---|
| SYS-ERP-KS | ERP-Suite, auf mittelständische Fertigung ausgerichtet, im deutschen Maschinenbau verbreitet | proALPHA Business Solutions GmbH, Weilerbach | 2006 | Kassel |
| SYS-ERP-EA | ERP für mittelständische Fertigungsbetriebe, historisch aus dem Bäurer-COM-Umfeld | Infor Deutschland GmbH | 2017 | Eisenach |
| SYS-PLM | PLM-Plattform, Marktführer im Segment, breite CAD-Integration | Siemens Digital Industries Software | 2014 | Kassel |
| SYS-CAD | 3D-CAD, eng an Teamcenter gekoppelt | Siemens Digital Industries Software | 2014 | Kassel |
| SYS-ECAD | E-CAD-Standard, im Schaltanlagenbau weit verbreitet | EPLAN GmbH & Co. KG, Monheim | 2010 | Kassel |
| SYS-SIM | Simulationssoftware für Strömung, Thermik und Struktur | Ansys Inc. | 2014 | Kassel |
| SYS-PROJ | Projektplanungswerkzeug | Microsoft Corporation | 2010 | Kassel |
| SYS-EXCEL | Tabellenkalkulation | Microsoft Corporation | 2010 | Gruppe |
| SYS-ACCESS | Desktop-Datenbank | Microsoft Corporation | 2017 | Eisenach |
| SYS-TEAMS | Kollaborationsplattform innerhalb Microsoft 365 | Microsoft Corporation | 2020 | Gruppe |
| SYS-SP | Dokumenten- und Intranetplattform | Microsoft Corporation | 2020 | Gruppe |
| SYS-VPN | Netzwerk- und VPN-Lösung | Fortinet Inc. | 2010 | Kassel |
| SYS-ZEIT | Zeitwirtschaft und Workforce Management | ATOSS Software SE, München | 2010 | Kassel |
| SYS-IAM | Identitäts- und Zugriffsdienst | Microsoft Corporation | 2019 | Kassel |

Die Jahreszahl bezeichnet die Produktivsetzung im jeweiligen Geltungsbereich. Bei den mit der Rothenberg Verdichtertechnik übernommenen Anwendungen bildet sie den Bestand zum Zeitpunkt der Übernahme ab.

## 3 Zwei Systemlandschaften

Seit der Übernahme der Rothenberg Verdichtertechnik GmbH im Jahr 2018 bestehen zwei weitgehend getrennte Landschaften. Kassel arbeitet mit SYS-ERP-KS und dem PLM, Eisenach mit SYS-ERP-EA sowie einer größeren Zahl lokaler Access-Datenbanken und Excel-Anwendungen. Eisenach führt außerdem einen eigenen Einkauf mit eigenen Stammdaten.

Die Festlegung der Geschäftsführung von 2018, das Geschäft vor der IT zu integrieren und die Systemharmonisierung zurückzustellen, gilt unverändert. Ein Vorhaben zur Zusammenführung der beiden ERP-Bestände ist nicht Bestandteil dieses Portfolios.

Standortübergreifend genutzt werden die Kollaborationsplattform SYS-TEAMS und die Dokumenten- und Intranetplattform SYS-SP; die Betriebsvereinbarung BV-2020-02 gilt für Kassel und Eisenach gleichermaßen.

## 4 Datenhaltung und Systemgrenzen

Die Produktdaten liegen in drei Beständen: mechanische Stücklisten im PLM, kaufmännische Stücklisten im ERP, Projektdokumente auf Netzlaufwerken.

Das PLM wird überwiegend von der mechanischen Konstruktion genutzt. Elektrotechnik, Verfahrenstechnik und Projektmanagement arbeiten außerhalb des PLM; elektrotechnische Unterlagen liegen in SYS-ECAD, Termin- und Kostenplanung der Projekte in SYS-PROJ und SYS-EXCEL.

## 5 Im Jahr 2020 hinzugekommene Anwendungen und Verfahren

| Gegenstand | Kennung | Stand |
|---|---|---|
| Kollaborationsplattform als Standard für die interne Kommunikation | SYS-TEAMS | seit April 2020 produktiv, Regelung in BV-2020-02 vom 06.05.2020 |
| Dokumenten- und Intranetplattform | SYS-SP | produktiv |
| Remote-Zugriff und mobiles Arbeiten über SYS-VPN | POL-IT-004 | Richtlinie in Kraft |
| Werkabnahme und Factory Acceptance Test einschließlich Remote-FAT | POL-QM-002 | gültig ab 01.04.2020 |
| Elektronische Freigabe bestimmter Projektunterlagen | - | im Einsatz |

Die VPN-gestützte Inbetriebnahme und der Remote-Service nutzen die bestehende Netzwerk- und VPN-Lösung; zusätzliche Anwendungen wurden dafür nicht beschafft.

## 6 Im Portfolio geführt, nicht produktiv

| Kennung | Anwendung | Hersteller | Stand |
|---|---|---|---|
| SYS-MES | MES für die diskrete Fertigung | Siemens Digital Industries Software | kein Termin für eine Produktivsetzung hinterlegt |

## 7 Mitgeltende Unterlagen

| Nummer | Titel |
|---|---|
| POL-IT-001 | Zugriffsrechte und Benutzerverwaltung |
| POL-IT-002 | Informationssicherheitsrichtlinie |
| POL-IT-004 | Remote-Zugriff und mobiles Arbeiten |
| POL-QM-001 | Dokumentenlenkung |
| POL-QM-002 | Werkabnahme und Factory Acceptance Test |
| BV-2017-01 | Nutzung betrieblicher IT, Internet und E-Mail |
| BV-2020-02 | Nutzung der Kollaborationsplattform |
| BV-2016-02 | Arbeitszeit und Zeiterfassung, maßgeblich für SYS-ZEIT |

## 8 Pflege des Portfolios

Das Portfolio wird von der IT geführt. Aufnahme, Änderung und Außerbetriebnahme einer Anwendung werden über die Dokumentenlenkung nach POL-QM-001 als neue Version dieses Dokuments wirksam. Die turnusmäßige Überprüfung erfolgt jährlich.
