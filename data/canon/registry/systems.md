# Systemregister LTT 2011-2025

Kanon-Detailstufe, geschrieben von einem Kanon-Detail-Fork. Grundlage: `canon/annals/*.md`.

## Die zwei Spalten - strikte Trennung

Die Spalte **reale Produkteigenschaft** enthält ausschließlich Nachprüfbares: Hersteller,
Funktionsklasse, Marktposition. Diese Angaben sind wahr und extern recherchierbar; genau dafür stehen
sie hier, denn der IT- und Security-Agent des Planspiels soll zu Zertifizierungen, Schwachstellen und
Herstellerangaben tatsächlich recherchieren können.

Die Spalte **fiktive LTT-Konfiguration** enthält alles, was LTT damit erlebt hat: Version, Module,
Probleme, Zufriedenheit, Betriebskosten. Das ist vollständig erfunden.

Ein Dokument darf reale Herstellerangaben als Sachverhalt nennen und jede Bewertung nur als
LTT-Erfahrung. Einem realen Produkt eine erfundene Eigenschaft zuzuschreiben, die als Herstellerangabe
gelesen werden könnte, ist untersagt.

## Registertabelle

| SYS-ID | System | reale Produkteigenschaft | fiktive LTT-Konfiguration | eingeführt | abgelöst | Standort/Geltung | Datenobjekte |
|---|---|---|---|---|---|---|---|
| SYS-ERP-KS | proALPHA ERP | ERP-Suite der proALPHA Business Solutions GmbH, Weilerbach; auf mittelständische Fertigung ausgerichtet, im deutschen Maschinenbau verbreitet | seit 2006 im Einsatz, über die Jahre stark angepasst; Projektabrechnung über selbstgebaute Zusatzfelder, Servicehistorie nur rudimentär | 2006 | nicht abgelöst, ab 2024 als Bestandssystem neben SAP-Finance | Kassel, ab 2018 auch kaufmännische Konsolidierung | Aufträge, kaufmännische Stücklisten, Materialstamm, Bestellungen, Kalkulation |
| SYS-ERP-EA | Infor COM | ERP der Infor Deutschland GmbH für mittelständische Fertigungsbetriebe, historisch aus dem Bäurer-COM-Umfeld | von Rothenberg übernommen, Stand älter als Kassel; keine Schnittstelle zum Kasseler ERP außer nächtlichem Dateiexport | vor 2018 bei Rothenberg | nicht abgelöst, MES-Rollout und Harmonisierung 2024 vertagt | Eisenach | Verdichteraufträge, Fertigungsaufträge, lokaler Materialstamm |
| SYS-PDM | PROCAD PRO.FILE | PDM/PLM-System der PROCAD GmbH & Co. KG, Karlsruhe; Dokumenten- und Artikelverwaltung für den Mittelstand | einfache Installation, nur Zeichnungsverwaltung; wird 2014 durch Teamcenter abgelöst, Altbestand bleibt bis 2019 lesend verfügbar | vor 2011 | 2014 abgelöst, Lesezugriff bis 2019 | Kassel | Zeichnungen, Dokumentenstände |
| SYS-PLM | Siemens Teamcenter | PLM-Plattform der Siemens Digital Industries Software; Marktführer im Segment, breite CAD-Integration | 2014 eingeführt, überwiegend von der mechanischen Konstruktion genutzt; Elektrotechnik, Verfahrenstechnik und Projektmanagement bleiben außen vor. EBOM liegt hier, MBOM im ERP - die Kopplung bleibt bis 2025 unvollständig | 2014 | nicht abgelöst | Kassel, ab 2021 teilweise Eisenach | EBOM, Zeichnungen, Änderungsaufträge, Freigabestände |
| SYS-CAD | Siemens NX | 3D-CAD der Siemens Digital Industries Software, eng an Teamcenter gekoppelt | Standard der mechanischen Konstruktion seit 2014; Altmodelle aus der Zeit davor teilweise nicht migriert | 2014 | nicht abgelöst | Kassel, Eisenach | 3D-Modelle, Baugruppen |
| SYS-ECAD | EPLAN Electric P8 | E-CAD-Standard der EPLAN GmbH & Co. KG, Monheim; im Schaltanlagenbau weit verbreitet | Grundlage der Schaltschrankdokumentation; die drei Schaltschranklieferanten nutzen unterschiedliche Bibliotheken und Makrostände, was den internen Abgleichaufwand ab 2022 erhöht | vor 2011 | nicht abgelöst | Kassel | Stromlaufpläne, Klemmenpläne, Betriebsmittelkennzeichnung |
| SYS-SIM | Ansys | Simulationssoftware der Ansys Inc.; Strömung, Thermik, Struktur | wenige Lizenzen in Technology & Development, Engpass bei parallelen Auslegungen | 2014 | nicht abgelöst | Kassel | Simulationsmodelle, Auslegungsrechnungen |
| SYS-PROJ | Microsoft Project | Projektplanungswerkzeug der Microsoft Corporation | Terminplanung der Projektleiter, Dateien liegen auf Projektlaufwerken; keine Kopplung an ERP-Kosten, deshalb parallele Excel-Kalkulationen | vor 2011 | nicht abgelöst | konzernweit | Terminpläne, Meilensteine |
| SYS-EXCEL | Microsoft Excel | Tabellenkalkulation der Microsoft Corporation | trägt einen erheblichen Teil der Projektsteuerung; 2025 in der Excel Amnesty erfasst, mehr als 430 Dateien gemeldet, rund 60 als geschäftskritisch eingestuft | vor 2011 | nicht abgelöst, ab 2025 mit Ownern und Versionskontrolle | konzernweit | Kalkulationen, Ressourcenpläne, Lieferterminlisten, Konfiguratoren |
| SYS-ACCESS | Microsoft Access | Desktop-Datenbank der Microsoft Corporation | mehrere lokale Anwendungen in Eisenach, insbesondere Produktionsplanung und Gießerei; 2025 weiterhin in Betrieb | vor 2018 | nicht abgelöst | Eisenach | lokale Planungs- und Prüfdaten |
| SYS-TEAMS | Microsoft Teams | Kollaborationsplattform der Microsoft Corporation innerhalb Microsoft 365 | im Frühjahr 2020 unter Zeitdruck als Standardkommunikationsplattform eingeführt; gilt intern als die einzige große Softwareeinführung, die ohne vollständigen Prozessentwurf gelang | 2020 (H1) | nicht abgelöst | konzernweit | Chats, Besprechungen, Dateien in Kanälen |
| SYS-SP | Microsoft SharePoint Online | Dokumenten- und Intranetplattform der Microsoft Corporation | ab 2020 zusammen mit Teams; Ablagestruktur wächst ungesteuert, eine einheitliche Dokumentenablage wird bis 2025 nicht erreicht | 2020 (H1) | nicht abgelöst | konzernweit | Dokumentenbibliotheken, Projektakten |
| SYS-VPN | Fortinet FortiGate | Netzwerk- und VPN-Lösung der Fortinet Inc. | 2020 kurzfristig für VPN-basierte Inbetriebnahme und Remote-Service erweitert; Fernzugriff auf Kundenanlagen läuft seither hierüber | vor 2011, 2020 erweitert | nicht abgelöst | konzernweit | Fernzugriffe, Sitzungsprotokolle |
| SYS-ZEIT | ATOSS Time Control | Zeitwirtschaft und Workforce Management der ATOSS Software SE, München | Zeiterfassung an beiden Standorten; die Auswertungstiefe ist durch Betriebsvereinbarung begrenzt, personenbezogene Leistungsauswertungen sind ausgeschlossen | vor 2011, 2019 auf Terminal- und Weberfassung erweitert | nicht abgelöst | Kassel, Eisenach | Zeitbuchungen, Abwesenheiten, Projektzeiten |
| SYS-CRM | Microsoft Dynamics 365 Sales | CRM-Anwendung der Microsoft Corporation innerhalb der Dynamics-365-Familie | 2023 eingeführt, erstmals konzernweite Pipeline-Sicht; Pflichtfelder gelten als bürokratisch, einzelne Key Account Manager pflegen erst kurz vor dem Forecast-Meeting. Gilt intern als 70-Prozent-Erfolg | 2023 (Q2/Q3) | nicht abgelöst | konzernweit | Opportunities, Kundenkontakte, Angebotsstatus, Forecast |
| SYS-BI | Microsoft Power BI | BI- und Reporting-Dienst der Microsoft Corporation | Grundlage des Management-Reportings ab 2023; das Projekt-Dashboard von 2024 setzt darauf auf und verlangt zusätzliche Datenpflege | 2023 | nicht abgelöst | konzernweit | Kennzahlen, Managementberichte, Projekt-Dashboard |
| SYS-DWH | Microsoft Azure Synapse Analytics | Datenplattform der Microsoft Corporation für Analyse und Data Warehousing | zentrales Data Warehouse aus dem ONE-LTT-Zielbild; nur für Finance und Vertrieb befüllt, Engineering-Daten fehlen bis 2025 | 2023 (Q4) | nicht abgelöst, unvollständig | konzernweit | konsolidierte Kennzahlen |
| SYS-S4 | SAP S/4HANA | ERP-Suite der SAP SE, Walldorf; Marktführer im Großunternehmenssegment | Zielsystem von ONE LTT ab 2022, Greenfield-Ansatz unter dem Leitsatz Adopt before adapt. Der für April 2024 geplante Big-Bang-Go-live wird im März auf Oktober verschoben und im Juni 2024 vollständig aufgegeben. Produktiv gehen ausschließlich Finance und Procurement | 2024 (Q4, nur Finance und Procurement) | nicht abgelöst, Umfang reduziert | konzernweit für Finance und Procurement | Hauptbuch, Konsolidierung, Bestellungen |
| SYS-ARIBA | SAP Ariba | Beschaffungsnetzwerk und eProcurement-Lösung der SAP SE | elektronischer Bestellprozess ab 2024 produktiv und intern als Erfolg bewertet; das geplante Lieferantenportal mit Selbstauskunft und Zertifikatsverwaltung wird nicht vollständig ausgerollt | 2024 | nicht abgelöst, teilweise umgesetzt | konzernweit | Bestellungen, Lieferantenstammdaten, Ausschreibungen |
| SYS-MES | Siemens Opcenter Execution | MES der Siemens Digital Industries Software für diskrete Fertigung | im ONE-LTT-Zielbild vorgesehen, Rollout Eisenach im Juni 2024 vertagt; nie produktiv, es existieren nur Konzeptunterlagen und ein Testsystem | nie produktiv | - | geplant für Eisenach | keine |
| SYS-FSM | SAP Field Service Management | Servicelösung der SAP SE für Außendiensteinsätze | mobile Serviceplattform aus dem ONE-LTT-Zielbild; im Juni 2024 vertagt. Serviceberichte laufen weiterhin über Formulare und das Kasseler ERP | nie produktiv | - | geplant konzernweit | keine |
| SYS-CONCUR | SAP Concur | Reisekosten- und Ausgabenmanagement der SAP SE | 2024 eingeführt, unstrittig und ohne größere Reibung; wird 2025 als Beispiel dafür zitiert, dass kleine abgegrenzte Einführungen gelingen | 2024 | nicht abgelöst | konzernweit | Reisekostenabrechnungen |
| SYS-IAM | Microsoft Entra ID | Identitäts- und Zugriffsdienst der Microsoft Corporation; bis Juli 2023 unter dem Namen Azure Active Directory geführt | zentrale Benutzerverwaltung; die Zusammenführung der Eisenacher Konten gelingt erst 2024. Rollen- und Berechtigungskonzepte waren 2023/2024 ein Kernproblem des ERP-Programms | 2019 als Azure AD, 2024 konsolidiert | nicht abgelöst | konzernweit | Benutzerkonten, Gruppen, Rollen |

## Aufgelöste Toleranzen

| Toleranz | Auflösung |
|---|---|
| TOLERANZ-2011-B | ERP Kassel ist proALPHA ERP (seit 2006), PDM ist PROCAD PRO.FILE. Beide vor 2011 im Einsatz. |
| TOLERANZ-2014-A | Das 2014 eingeführte PLM ist Siemens Teamcenter, zusammen mit Siemens NX als CAD. Einführungsprojekt Q1 bis Q4 2014, produktiv im vierten Quartal. |
| TOLERANZ-2018-B | Das Eisenacher ERP ist Infor COM, übernommen mit Rothenberg, älterer Versionsstand als Kassel. |
| TOLERANZ-2023-B | Das CRM ist Microsoft Dynamics 365 Sales. Das Ziel-ERP von ONE LTT ist SAP S/4HANA. |

## Schatten-IT

Excel und Access sind keine Ausnahme, sondern tragende Infrastruktur. Die Excel Amnesty von 2025 erfasst
mehr als 430 Dateien, rund 60 gelten als geschäftskritisch: Projektkalkulationen, Lieferterminlisten,
Ressourcenpläne, Inbetriebnahmechecklisten, Ersatzteilmatrizen, Angebotskonfiguratoren,
Berechnungstools. Ein Teil wird kontrolliert überführt, der Rest erhält definierte Owner und
Versionskontrolle. Vor 2025 existiert diese Unterscheidung nicht - dort ist Excel schlicht überall.

## Anachronismusfallen bei Produktnamen

Diese Umbenennungen sind real und müssen zeitlich korrekt verwendet werden:

| Bis | Ab | Hinweis |
|---|---|---|
| Office 365 | Microsoft 365 (April 2020) | ein Dokument von 2019 sagt Office 365 |
| Azure Active Directory / Azure AD | Microsoft Entra ID (Juli 2023) | ein Dokument von 2022 sagt Azure AD |
| Microsoft Dynamics CRM | Dynamics 365 (ab 2016) | bei LTT ohnehin erst 2023 relevant |
| SAP ERP / ECC | S/4HANA als Nachfolgelinie | im LTT-Kontext ist ausschließlich S/4HANA gemeint |

Außerdem: Teamcenter, NX, EPLAN P8, proALPHA, Infor COM und ATOSS existieren durchgehend im gesamten
Zeitraum. Power BI ist ab 2015 am Markt, bei LTT aber erst ab 2023 im Einsatz - ein Dokument von 2021
darf es nicht als vorhandenes System nennen.
