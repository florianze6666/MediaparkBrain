# Richtlinienregister

Kanonstufe 2 (Detail-Fork). Verbindliche Liste aller Richtlinien, Prozessvorgaben und Standards mit
Version und Gültigkeitszeitraum. Ein Dokument darf sich nur auf eine Richtlinie berufen, die zu seinem
Datum in der genannten Version gilt. Wer sich auf eine abgelöste Version beruft, ohne das kenntlich zu
machen, erzeugt einen Anachronismus.

Grundlage: `canon/annals/*.md`. Nichts in diesem Register widerspricht den Annalen.

## Lesart der Spalten

`gültig ab` ist der Zeitpunkt des Inkrafttretens. `abgelöst` nennt die Nachfolgeversion oder die
Richtlinie, die sie ersetzt; ein leeres Feld bedeutet, die Version gilt Ende 2025 weiterhin.
`Durchsetzung` bewertet, wie konsequent die Regel in der Praxis befolgt wird - diese Spalte ist Teil des
Kanons, weil die Lücke zwischen Regel und Praxis ein wiederkehrendes Muster des Unternehmens ist.

---

## Vertrieb und Angebot

| Policy-ID | Titel | Version | gültig ab | abgelöst | Eigentümer | Geltungsbereich | Durchsetzung |
|---|---|---|---|---|---|---|---|
| POL-VTR-001 | Technische Angebotsreview für Projekte über 500.000 EUR | v1.0 | 2013 | v2.0 | Vertrieb und System Engineering | alle Kundenprojekte | anfangs konsequent |
| POL-VTR-001 | Technische Angebotsreview, erweitert um Wärmequellendaten und Annahmenprotokoll | v2.0 | 2019 | - | Vertrieb und System Engineering | alle Kundenprojekte | überwiegend befolgt, bei Termindruck verkürzt |

Die Regel entsteht als direkte Reaktion auf das Projekt Glaswerk Nord (PRJ-GLASWERK-NORD, 2013), dessen
Marge durch eine zu optimistisch angenommene Wärmequellentemperatur aufgebraucht wurde.

## Entwicklung und Engineering

| Policy-ID | Titel | Version | gültig ab | abgelöst | Eigentümer | Geltungsbereich | Durchsetzung |
|---|---|---|---|---|---|---|---|
| POL-RD-001 | Stage-Gate-Prozess G0 bis G5 | v1.0 | 2015 | v1.1 | Technology and Development | Produktentwicklung | bei formellen Entwicklungsprojekten gut, bei Kundenprojekten regelmäßig umgangen |
| POL-RD-001 | Stage-Gate-Prozess, ergänzt um Plattformkonformitätsprüfung | v1.1 | 2018 | - | Technology and Development | Produktentwicklung | unverändert selektiv |
| POL-ENG-001 | Design Freeze und Engineering Change Request | v1.0 | 2019 | v1.1 | Engineering und Qualitätsmanagement | alle Projekte ab Design Freeze | formal verbindlich, bei strategischen Kunden regelmäßig durchbrochen |
| POL-ENG-001 | Design Freeze und ECR, ergänzt um formelle EBOM-MBOM-Uebergabe | v1.1 | Q2 2023 | - | Engineering und Qualitätsmanagement | alle Projekte | Zahl dokumentierter Changes steigt massiv, Deutung umstritten |
| POL-ENG-002 | Plattform- und Modulstandard der Modulplattform M1 | v1.0 | 2015 | v2.0 | Technology and Development | Anlagenkonfiguration | erodiert durch verdeckte Produktentwicklung |
| POL-ENG-002 | Plattform- und Modulstandard, Produktlinien ProcessLift und GeoQuart | v2.0 | 2021 | - | Central Engineering | Anlagenkonfiguration | teilweise befolgt |

## Projekt- und Portfoliomanagement

| Policy-ID | Titel | Version | gültig ab | abgelöst | Eigentümer | Geltungsbereich | Durchsetzung |
|---|---|---|---|---|---|---|---|
| POL-PM-001 | Projektmanagement-Standard: Projektstrukturplan, Meilensteinplan, Statusbericht, Risikoregister, Change Request, Kick-off, Monatsreview | v1.0 | 2016 | v1.1 | PMO | alle Projekte ab 250.000 EUR | anfangs vollständig, dann als Bürokratie empfunden |
| POL-PM-001 | Projektmanagement-Standard nach Abschaffung mehrerer Pflichtformulare | v1.1 | 2017 | v2.0 | PMO | alle Projekte ab 250.000 EUR | gut akzeptiert |
| POL-PM-001 | Projektmanagement-Standard, Statusbericht auf zwölf Kennzahlen reduziert | v2.0 | Q3 2024 | - | Project Excellence Office | alle Projekte ab 250.000 EUR | positiv aufgenommen, Entlastung durch das neue Dashboard teilweise aufgehoben |
| POL-PM-002 | Projektampel und Eskalationsstufen | v1.0 | Q2 2023 | v1.1 | PMO | alle Projekte | Aussagekraft sinkt, weil zu viele Projekte gelb sind |
| POL-PM-002 | Projektampel, verschärfte Definition von Gelb und Rot | v1.1 | Q4 2023 | - | PMO, ab Q3 2024 Project Excellence Office | alle Projekte | Zahl roter Projekte steigt stark, einzelne Business Units mildern Bewertungen informell ab |
| POL-PM-003 | Zentrale Ressourcenplanung | v1.0 | 2017 | v2.0 | PMO | Engineering und Inbetriebnahme | eingeschränkt, Abteilungsleiter führen eigene Excel-Planung weiter |
| POL-PM-003 | Ressourcenplanung im Rahmen des Projektcontrollings | v2.0 | 2024 | - | Project Excellence Office | Engineering und Inbetriebnahme | teilweise erfolgreich |
| POL-ORG-001 | Begrenzung auf drei Top-Priority-Change-Initiatives je Business Unit | v1.0 | Q1 2025 | - | Geschäftsführung | alle Business Units | konsequent, weil an die Budgetfreigabe gekoppelt |

## Einkauf und Supply Chain

| Policy-ID | Titel | Version | gültig ab | abgelöst | Eigentümer | Geltungsbereich | Durchsetzung |
|---|---|---|---|---|---|---|---|
| POL-EK-001 | Lieferantenbewertung nach Qualität, Preis, Termintreue, Innovationsfähigkeit | v1.0 | 2016 | v2.0 | Einkauf | A-Lieferanten | jährlich, uneinheitliche Tiefe |
| POL-EK-001 | Lieferantenbewertung, erweitert um Versorgungssicherheit | v2.0 | 2021 | v3.0 | Supply Chain and Operations Planning | alle qualifizierten Lieferanten | verbessert |
| POL-EK-001 | Lieferantenbewertung, erweitert um Financial Health Check | v3.0 | Q3 2024 | - | Supply Chain and Operations Planning | alle qualifizierten Lieferanten | strategischer Einkauf meldet rund 85 Prozent Compliance, interne Audits kommen auf rund 70 Prozent |
| POL-SCM-001 | Dual-Source-Grundsatz für Komponenten der Risikokategorie A | v1.0 | 2021 | POL-SCM-003 | Supply Chain | Risikokategorie A | Ausnahmen für kundenspezifische Wärmetauscher, proprietäre SPS-Hardware, bestimmte Frequenzumrichter, komplexe Schaltschrankkonfigurationen |
| POL-SCM-002 | Sales and Operations Planning, monatlicher Prozess | v1.0 | Q3 2021 | v1.1 | Supply Chain und Operations | konzernweit | Transparenz über Auftragsbestand steigt, Engineering-Kapazitäten fehlen |
| POL-SCM-002 | Sales and Operations Planning mit Engineering-Kapazitätssicht | v1.1 | 2024 | - | Supply Chain und Operations | konzernweit | teilweise umgesetzt |
| POL-SCM-003 | Versorgungsklassen S1 Commodity, S2 Preferred Supplier Components, S3 Strategic Components, S4 Critical Single Source; Mindestbestand, Second-Source-Roadmap, technische Substitutionsanalyse, Business-Continuity-Plan, jährlicher Financial-Health-Check; Management-Review für S4 | v1.0 | Q3 2024 | - | Supply Chain | konzernweit | nur teilweise konsequent, echte Second Source erfordert bei mehreren Komponenten konstruktive Änderungen und neue Zertifizierungen |
| POL-SCM-004 | Lieferantenpolitik "Resilience where failure stops the project, competition where substitution is feasible" | v1.0 | 2025 | - | Supply Chain und Geschäftsführung | konzernweit | Zielbild, Umsetzungsgrad umstritten |
| POL-SCM-005 | Sicherheitsbestände für kritische Komponenten | v1.0 | Q1 2020 | v2.0 | Supply Chain Task Force | kritische Komponenten | Erhöhung von vier auf zwölf Wochen, bei Frequenzumrichtern und SPS-Komponenten darüber hinaus |
| POL-SCM-005 | Sicherheitsbestände, reduziert zugunsten des Working Capital | v2.0 | 2021 | v3.0 | Supply Chain und Finance | kritische Komponenten | Gegenstand des dauerhaften Pendelns zwischen Lean und Resilience |
| POL-SCM-005 | Sicherheitsbestände nach Versorgungsklasse | v3.0 | Q3 2024 | - | Supply Chain | nach S1 bis S4 differenziert | an POL-SCM-003 gekoppelt |

## Finanzen und Investitionen

| Policy-ID | Titel | Version | gültig ab | abgelöst | Eigentümer | Geltungsbereich | Durchsetzung |
|---|---|---|---|---|---|---|---|
| POL-FIN-001 | Genehmigungsschwellen und Unterschriftenregelung | v1.0 | 2016 | v2.0 | Finance | konzernweit | pragmatisch gehandhabt |
| POL-FIN-001 | Genehmigungsschwellen nach der Hansera-Ordnung | v2.0 | Q3 2022 | - | Finance und Beirat | konzernweit | konsequent, weil an die Beiratsbefassung gekoppelt |
| POL-FIN-002 | Investitionsrichtlinie: strukturierte Investitionsvorlage mit NPV, IRR und Szenarioanalyse ab 2 Mio EUR | v1.0 | Q3 2022 | v1.1 | Finance und Strategy and Investment Committee | Investitionen über 2 Mio EUR | verbindlich |
| POL-FIN-002 | Investitionsrichtlinie, ergänzt um Total Cost of Ownership und Betriebskostenbetrachtung für Softwarevorhaben | v1.1 | 2024 | - | Finance | Investitionen über 2 Mio EUR | verbindlich, Anlass sind die Aufwandsentwicklungen bei ONE LTT |
| POL-FIN-003 | Projektcontrolling und Projektmargenberichterstattung | v1.0 | 2016 | v2.0 | Controlling | Projekte ab 250.000 EUR | uneinheitliche Datenbasis |
| POL-FIN-003 | Projektcontrolling im Digital Core | v2.0 | 2024 | - | Controlling | alle Projekte | teilweise erfolgreich |

## IT, Informationssicherheit und Daten

| Policy-ID | Titel | Version | gültig ab | abgelöst | Eigentümer | Geltungsbereich | Durchsetzung |
|---|---|---|---|---|---|---|---|
| POL-IT-001 | Zugriffsrechte und Benutzerverwaltung | v1.0 | 2017 | v2.0 | IT | konzernweit | Kassel und Eisenach getrennt verwaltet |
| POL-IT-001 | Zugriffsrechte, Rollenmodell über beide Standorte | v2.0 | 2021 | v3.0 | IT | konzernweit | unvollständig, weil ERP-Landschaften getrennt bleiben |
| POL-IT-001 | Zentrale Benutzerverwaltung und Rollenkonzept | v3.0 | 2024 | - | IT | konzernweit | erfolgreich umgesetzt |
| POL-IT-002 | Informationssicherheitsrichtlinie | v1.0 | 2019 | v2.0 | IT | konzernweit | Grundschutzniveau |
| POL-IT-002 | Informationssicherheitsrichtlinie, erweitert um Remote-Zugriff und Lieferantenzugänge | v2.0 | 2023 | v3.0 | IT | konzernweit | überwiegend umgesetzt |
| POL-IT-002 | Informationssicherheitsrichtlinie mit Bezug auf die NIS2-Anforderungen | v3.0 | 2025 | - | IT | konzernweit | in Umsetzung, Reifegrad uneinheitlich |
| POL-IT-003 | Cloud- und SaaS-Richtlinie | v1.0 | 2021 | v2.0 | IT | konzernweit | entstanden aus der Teams-Einführung |
| POL-IT-003 | Cloud- und SaaS-Richtlinie mit Anbieterbewertung, Exit-Fähigkeit und Datenhaltungsvorgaben | v2.0 | 2024 | - | IT | konzernweit | verbindlich für Neubeschaffungen |
| POL-IT-004 | Remote-Zugriff und mobiles Arbeiten | v1.0 | Q1 2020 | v1.1 | IT | konzernweit | unter Zeitdruck eingeführt |
| POL-IT-004 | Remote-Zugriff und mobiles Arbeiten, konsolidiert | v1.1 | 2022 | - | IT | konzernweit | etabliert |
| POL-IT-005 | Excel- und Schattenanwendungs-Governance: Unterscheidung zwischen lokalem Hilfsmittel und geschäftskritischer Schattenanwendung, Owner- und Versionspflicht für kritische Dateien | v1.0 | Q2 2025 | - | IT | konzernweit | Ergebnis von Excel Amnesty, rund 60 kritische Dateien betroffen |
| POL-IT-006 | Stammdatenrichtlinie und Materialstammpflege | v1.0 | Q2 2023 | - | IT und Master Data Management | konzernweit | Data Ownership bleibt schwach, Process Owner ohne disziplinarische Autorität |
| POL-IT-007 | NIS2-Vorbereitung: Betroffenheitsanalyse, Meldewege, Lieferkettensicherheit, IT/OT-Segmentierung | v1.0 | 2025 | - | IT | konzernweit | in Arbeit |

## Qualität und Dokumentation

| Policy-ID | Titel | Version | gültig ab | abgelöst | Eigentümer | Geltungsbereich | Durchsetzung |
|---|---|---|---|---|---|---|---|
| POL-QM-001 | Dokumentenlenkung | v1.0 | 2014 | v2.0 | Qualitätsmanagement | konzernweit | Netzlaufwerke bleiben faktisch maßgeblich |
| POL-QM-001 | Dokumentenlenkung mit digitaler Projektakte | v2.0 | 2022 | - | Qualitätsmanagement | konzernweit | teilweise erfolgreich, einheitliche Dokumentenablage bis Ende 2025 nicht erreicht |
| POL-QM-002 | Werkabnahme und Factory Acceptance Test, einschließlich Remote-FAT | v1.0 | Q2 2020 | - | Qualitätsmanagement | alle Anlagenprojekte | aus der Pandemie entstanden, dauerhaft beibehalten |

---

## Zeitliche Sperren

Die folgenden Begriffe und Regelwerke dürfen vor dem genannten Zeitpunkt in keinem Dokument als
geltende Vorgabe erscheinen:

| Begriff | frühestens |
|---|---|
| Stage-Gate G0 bis G5 | 2015 |
| Design Freeze, Engineering Change Request | 2019 |
| Remote-FAT | Q2 2020 |
| Dual-Source-Grundsatz | 2021 |
| Sales and Operations Planning | Q3 2021 |
| Investitionsvorlage mit NPV, IRR, Szenarioanalyse | Q3 2022 |
| Versorgungsklassen S1 bis S4 | Q3 2024 |
| Total Cost of Ownership als Pflichtbestandteil der Investitionsvorlage | 2024 |
| NIS2 | 2024 |
| Excel-Governance nach Excel Amnesty | Q2 2025 |
| Lieferantenpolitik "Resilience where failure stops the project ..." | 2025 |

## Aufgelöste Toleranzen

Die Versionsstände, Eigentümer und Durchsetzungsgrade dieses Registers sind Auflösungen des
Detail-Forks. Kanonisch vorgegeben waren lediglich Existenz und Einführungszeitpunkt der Richtlinien
sowie die Zitate der Lieferantenpolitik 2025 und der Versorgungsklassen. Die Angabe, dass der
strategische Einkauf rund 85 Prozent Compliance meldet und interne Audits auf rund 70 Prozent kommen,
ist kanonisch aus der Chronik.
