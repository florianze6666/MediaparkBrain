---
doc_id: LTT-20251112-IT-A25
titel: Softwareportfolio der LTT-Gruppe 2025
dokumenttyp: Softwareportfolio
datum: 2025-11-12
verfasser: Dr. Philipp Nowak
rolle: CIO
organisationseinheit: IT
empfaenger: "-"
projekt: "-"
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit]
ablageort: it_doku
---

Lahnberg Thermotechnik GmbH & Co. KG
Informationstechnologie

# Softwareportfolio der LTT-Gruppe 2025

| | |
|---|---|
| Dokument-Nr. | LTT-20251112-IT-A25 |
| Version | 1.0 |
| Stand | 12.11.2025 |
| Erstellt | Dr. Philipp Nowak, CIO |
| Mitwirkung | Andrea Faber, Leiterin IT-Applikationen |
| Freigabe | Dr. Philipp Nowak, CIO, 12.11.2025 |
| Einstufung | intern |
| Überprüfung | jährlich sowie bei Aufnahme oder Außerbetriebnahme einer Anwendung |
| Lenkung | nach Dokumentenlenkung POL-QM-001 v2.0 |

## 1 Zweck

Dieses Dokument führt den Bestand der zentral verantworteten Anwendungen der Lahnberg Thermotechnik
auf dem Stand vom 12. November 2025 auf. Es ist die verbindliche Bezugsgröße für Architektur-,
Lizenz-, Betriebs- und Berechtigungsfragen sowie für die Systembeschreibungen nach der
Rahmenvereinbarung BV-2023-01.

Das Portfolio ist eine Bestandsaufnahme. Es enthält keine Bewertung des Bestandes und keine Aussage
über künftige Vorhaben.

## 2 Geltungsbereich und Abgrenzung

Erfasst sind alle Anwendungen, die von der IT zentral verantwortet und betrieben oder zentral
beschafft werden, unabhängig vom Standort. Der Geltungsbereich umfasst die Standorte Kassel und
Eisenach sowie Rotterdam, Brno, Shanghai und Houston.

Nicht erfasst sind:

- Hardware, Netz- und Rechenzentrumskomponenten sowie Steuerungs- und Maschinensoftware in der
  Fertigung,
- lokale Hilfsmittel und Einzeldateien der Fachbereiche. Für sie gilt die Abgrenzung nach der
  Excel- und Schattenanwendungs-Governance POL-IT-005 v1.0; als geschäftskritisch eingestufte
  Schattenanwendungen werden dort mit Owner und Versionskontrolle geführt, nicht in diesem
  Portfolio.

## 3 Systematik

Jede Anwendung wird mit ihrer Kennung aus der IT-Applikationsverwaltung, der Bezeichnung von
Hersteller und Anwendung sowie dem Zeitpunkt der Produktivsetzung bei LTT geführt. Die Gruppierung
folgt dem Einsatzzweck und hat keine steuernde Bedeutung. Einträge ohne Datum sind im Portfolio
geführt, aber nicht produktiv; sie sind in Abschnitt 5 erläutert.

## 4 Anwendungsübersicht

### 4.1 Engineering und Produktentwicklung

| Kennung | Anwendung | Im Einsatz seit |
|---|---|---|
| SYS-PLM | PLM-Plattform der Siemens Digital Industries Software, Marktführer im Segment, breite CAD-Integration | 2014 |
| SYS-CAD | 3D-CAD der Siemens Digital Industries Software, eng an Teamcenter gekoppelt | 2014 |
| SYS-ECAD | E-CAD-Standard der EPLAN GmbH & Co. KG, Monheim, im Schaltanlagenbau weit verbreitet | vor 2011 |
| SYS-SIM | Simulationssoftware der Ansys Inc., Strömung, Thermik, Struktur | 2014 |

### 4.2 Kaufmännische Kernprozesse

| Kennung | Anwendung | Im Einsatz seit |
|---|---|---|
| SYS-S4 | ERP-Suite der SAP SE, Walldorf, Marktführer im Großunternehmenssegment | 10/2024 |
| SYS-ARIBA | Beschaffungsnetzwerk und eProcurement-Lösung der SAP SE | 2024 |
| SYS-CONCUR | Reisekosten- und Ausgabenmanagement der SAP SE | 2024 |

### 4.3 Vertrieb und Service

| Kennung | Anwendung | Im Einsatz seit |
|---|---|---|
| SYS-CRM | CRM-Anwendung der Microsoft Corporation innerhalb der Dynamics-365-Familie | 04/2023 |
| SYS-FSM | Servicelösung der SAP SE für Außendiensteinsätze | nicht produktiv |

### 4.4 Fertigung

| Kennung | Anwendung | Im Einsatz seit |
|---|---|---|
| SYS-MES | MES der Siemens Digital Industries Software für diskrete Fertigung | nicht produktiv |

### 4.5 Information und Auswertung

| Kennung | Anwendung | Im Einsatz seit |
|---|---|---|
| SYS-BI | BI- und Reporting-Dienst der Microsoft Corporation | 2023 |
| SYS-DWH | Datenplattform der Microsoft Corporation für Analyse und Data Warehousing | 10/2023 |

### 4.6 Zusammenarbeit und Arbeitsplatz

| Kennung | Anwendung | Im Einsatz seit |
|---|---|---|
| SYS-TEAMS | Kollaborationsplattform der Microsoft Corporation innerhalb Microsoft 365 | 2020 |
| SYS-SP | Dokumenten- und Intranetplattform der Microsoft Corporation | 2020 |
| SYS-PROJ | Projektplanungswerkzeug der Microsoft Corporation | vor 2011 |
| SYS-ACCESS | Desktop-Datenbank der Microsoft Corporation | vor 2018 |

### 4.7 Infrastrukturnahe Dienste und Zeitwirtschaft

| Kennung | Anwendung | Im Einsatz seit |
|---|---|---|
| SYS-IAM | Identitäts- und Zugriffsdienst der Microsoft Corporation, bis Juli 2023 unter dem Namen Azure Active Directory geführt | 2019 |
| SYS-VPN | Netzwerk- und VPN-Lösung der Fortinet Inc. | vor 2011 |
| SYS-ZEIT | Zeitwirtschaft und Workforce Management der ATOSS Software SE, München | vor 2011 |

## 5 Geführte, nicht produktive Anwendungen

SYS-MES und SYS-FSM waren Bestandteil des im November 2022 beschlossenen Programmumfangs. Mit dem
Zuschnitt der Teilprogramme im Juni 2024 wurden der MES-Rollout in Eisenach und die konzernweite
Serviceplattform zurückgestellt. Beide Anwendungen sind im Portfolio geführt, jedoch weder
produktiv gesetzt noch im Betrieb.

## 6 Mitgeltende Regelungen

| Regelung | Version |
|---|---|
| POL-IT-001 Zentrale Benutzerverwaltung und Rollenkonzept | v3.0 |
| POL-IT-002 Informationssicherheitsrichtlinie mit Bezug auf die NIS2-Anforderungen | v3.0 |
| POL-IT-003 Cloud- und SaaS-Richtlinie mit Anbieterbewertung, Exit-Fähigkeit und Datenhaltungsvorgaben | v2.0 |
| POL-IT-004 Remote-Zugriff und mobiles Arbeiten | v1.1 |
| POL-IT-005 Excel- und Schattenanwendungs-Governance | v1.0 |
| POL-IT-006 Stammdatenrichtlinie und Materialstammpflege | v1.0 |
| POL-IT-007 NIS2-Vorbereitung | v1.0 |
| POL-QM-001 Dokumentenlenkung mit digitaler Projektakte | v2.0 |

Für Anwendungen mit Bezug zu personenbezogenen Daten gilt zusätzlich die Rahmenvereinbarung
BV-2023-01 vom 16.03.2023 mit den zu ihr geschlossenen Teilvereinbarungen.

## 7 Fortschreibung

Aufnahme, Änderung und Außerbetriebnahme eines Eintrags erfolgen über die IT-Applikationsverwaltung
und bedürfen der Freigabe durch den CIO. Die Fortschreibung dieses Dokuments verantwortet die
Leitung IT-Applikationen.

## 8 Änderungsverzeichnis

| Version | Datum | Bearbeitung | Inhalt |
|---|---|---|---|
| 1.0 | 12.11.2025 | Nowak | Bestand zum 12.11.2025 |
