# Projektregister

Kanonstufe 2 (Detail-Fork). Verbindliches Register aller Projekte, Programme und Investitionsvorhaben,
auf die sich Korpusdokumente beziehen dürfen. Keine Entität außerhalb dieses Registers verwenden -
wer ein weiteres Projekt braucht, legt einen Entity-Request an.

Grundlage: `canon/annals/*.md` und `source/Fikive_Geschäftsentwicklung.md`. Kein Eintrag widerspricht den
Annalen.

## Nummernschema

| Präfix | Bedeutung | Beispiel |
|---|---|---|
| `KP-JJJJ-NNN` | Kundenprojekt, laufende Nummer je Jahr | KP-2013-042 |
| `IP-JJJJ-NN` | internes Projekt oder Transformationsprogramm | IP-2022-02 |
| `ENT-JJJJ-NN` | Entwicklungsprojekt (Stage-Gate ab 2015) | ENT-2015-01 |
| `INV-JJJJ-NN` | Investitionsprojekt | INV-2024-01 |

Die `PRJ-ID` ist die sprechende Kanonreferenz und in allen anderen Registern zu verwenden. Die
`Projektnummer` ist die in der fiktiven Welt gebräuchliche Nummer und gehört in Dokumententexte.

## Organisatorische Zuordnung nach Zeitraum

Vor 2017 gibt es keine Bereichszuordnung, die Spalte lautet dann `funktional`. Von 2017 bis Q3 2022
gelten die Marktbereiche Process Industry (PI), Energy & Utilities (EU), Commercial Heat (CH). Ab Q4
2022 gelten die vier Business Units Industrial Heat Systems (IHS), District & Geo Energy (DGE),
Compressor Systems (CS), Lifecycle & Service (LS). Ein Projekt, das über den Bruch läuft, trägt beide
Angaben.

---

## Transformations-, Entwicklungs- und Investitionsprojekte

| PRJ-ID | Projektnummer | Name | Art | Bereich | Start | Ende | Status | Volumen | Leitung | Besonderheit |
|---|---|---|---|---|---|---|---|---|---|---|
| PRJ-PLM-2014 | IP-2014-01 | Einführung PLM/PDM | Transformation | funktional | 2014 | 2015 | abgeschlossen, Teilerfolg | rund 1,2 Mio | Leitung Konstruktion (offen, P-xx) | überwiegend nur von der mechanischen Konstruktion genutzt; Ursprung der Dreiteilung PLM/ERP/Netzlaufwerk |
| PRJ-PLATTFORM-M1 | ENT-2015-01 | Modulplattform M1, erste standardisierte Wärmepumpenplattform | Entwicklung | funktional | 2015 | 2017 | abgeschlossen | rund 2,5 Mio | Leitung Technology & Development (offen, P-xx) | Vorläufer der späteren Produktlinie ProcessLift; löst TOLERANZ-2015-A |
| PRJ-STAGEGATE-2015 | IP-2015-01 | Einführung Stage-Gate G0 bis G5 | Transformation | funktional | 2015 | 2016 | abgeschlossen, selektiv umgangen | rund 0,2 Mio | Geschäftsführung | Kundenprojekte umgehen die Gates regelmäßig, es entsteht verdeckte Produktentwicklung |
| PRJ-PMO-2016 | IP-2016-01 | Aufbau Project Management Office | Transformation | funktional | 2016 | 2017 | abgeschlossen, Teilrückbau | rund 0,6 Mio | PMO-Leitung (offen, P-xx) | mehrere Pflichtformulare nach etwa einem Jahr wieder abgeschafft |
| PRJ-MATRIX-2017 | IP-2017-01 | Einführung der Marktbereichsmatrix | Transformation | PI/EU/CH | 2017 | 2018 | abgeschlossen | rund 0,3 Mio | Geschäftsführung | Doppelunterstellung der Projektleiter, Ressourcenkonflikte |
| PRJ-ROTHENBERG | IP-2018-01 | Integration Rothenberg Verdichtertechnik | Transformation | funktional | 2018 | 2021 | teilweise abgeschlossen | Kaufpreis rund 24 Mio, Integrationsaufwand rund 1,5 Mio | Geschäftsführung | IT-Harmonisierung bewusst ausgeklammert, Motto "Erst Geschäft integrieren, dann IT"; löst TOLERANZ-2018-A |
| PRJ-MAKE-2019 | INV-2019-01 | Make-Strategie, vertikale Integration | Investition | funktional | 2019 | 2021 | abgeschlossen | rund 12,0 Mio über drei Jahre | Operations-Leitung (offen, P-xx) | CNC, Prüfstände, Schweißtechnik, Laserschneiden, Blechbearbeitung, Gießereimodernisierung; löst TOLERANZ-2019-A |
| PRJ-DESIGNFREEZE-2019 | IP-2019-01 | Design Freeze und Engineering-Change-Request-Prozess | Transformation | PI/EU/CH | 2019 | 2020 | abgeschlossen, selektiv umgangen | rund 0,2 Mio | PMO und Engineering | Vertrieb akzeptiert bei strategischen Kunden weiterhin Änderungen nach Design Freeze |
| PRJ-TEAMS-2020 | IP-2020-01 | Teams-Einführung und Remote-Fähigkeit | Transformation | konzernweit | Q1 2020 | Q4 2020 | erfolgreich | rund 0,4 Mio | IT-Leitung (offen, P-xx) | unter Zeitdruck ohne vollständigen Prozessentwurf gelungen; wird später als Gegenbeispiel zu ONE LTT zitiert |
| PRJ-SCTASKFORCE-2020 | IP-2020-02 | Supply Chain Task Force | Transformation | funktional | Q1 2020 | Q2 2021 | abgeschlossen | rund 0,3 Mio | Einkaufsleitung (offen, P-xx) | Umstellung von Kostenorientierung auf Versorgungssicherheit, Sicherheitsbestände von vier auf zwölf Wochen |
| PRJ-SCM-ZENTRAL-2021 | IP-2021-01 | Zentralisierung Supply Chain und Operations Planning | Transformation | funktional | Q1 2021 | Q2 2022 | abgeschlossen | rund 0,8 Mio | Leitung Supply Chain (offen, P-xx) | Eisenacher Einkauf verliert lokale Entscheidungsfreiheit |
| PRJ-SOP-2021 | IP-2021-02 | Einführung Sales and Operations Planning | Transformation | funktional | Q3 2021 | Q2 2022 | teilweise erfolgreich | rund 0,4 Mio | Supply Chain und Operations | Engineering-Kapazitäten nicht abgebildet, daraus entsteht das S&OP-Paradox |
| PRJ-HANSERA-2022 | IP-2022-01 | Gesellschafterwechsel Hansera Industrieholding SE | Transformation | konzernweit | Q1 2022 | Q3 2022 | abgeschlossen | 60 Prozent der Anteile, Unternehmenswert rund 150 Mio | Gesellschafter | neuer Beirat mit drei Ausschüssen; löst TOLERANZ-2022-A teilweise |
| PRJ-BU-REORG-2022 | IP-2022-02 | Reorganisation in vier Business Units | Transformation | IHS/DGE/CS/LS | Q4 2022 | Q4 2023 | abgeschlossen | rund 0,5 Mio | Kessler | alte Marktsegment-Zuständigkeiten überleben faktisch, Doppelunterstellungen bleiben |
| PRJ-ONELTT | IP-2022-03 | ONE LTT, Digitalisierungsprogramm (Vorläufername Project Atlas) | Transformationsprogramm | konzernweit | Beschluss 11/2022, operativer Start 01/2023 | Scope-Schnitt 06/2024, Programm als solches beendet Q3 2024 | teilweise gescheitert | 14,8 Mio geplant, ab 03/2024 rund 19,0 Mio erwartet | Programmleitung (offen, P-xx) | zentraler Präzedenzfall der Firmengeschichte; Greenfield, "Adopt before adapt"; Process Owner ohne disziplinarische Autorität |
| PRJ-MDM-2023 | IP-2023-01 | Master-Data-Projekt, Materialstammbereinigung | Transformation | konzernweit | Q1 2023 | Q2 2024 | Teilerfolg | Teil des ONE-LTT-Budgets | Teilprojektleitung (offen, P-xx) | Ziel 40 Prozent, abgesenkt auf 25 Prozent, erreicht rund 18 Prozent von über 180.000 Materialnummern |
| PRJ-EBOM-MBOM-2023 | IP-2023-02 | Durchgängige EBOM-MBOM-Struktur | Transformation | konzernweit | Q2 2023 | 06/2024 vertagt | nicht abgeschlossen | Teil des ONE-LTT-Budgets | Teilprojektleitung (offen, P-xx) | dokumentierte Engineering Changes steigen massiv, Deutungskonflikt zwischen Geschäftsführung und Qualitätsmanagement |
| PRJ-CRM-2023 | IP-2023-03 | CRM-Einführung | Transformation | konzernweit | Q2 2023 | Q4 2023 | 70-Prozent-Erfolg | rund 1,8 Mio | Vertriebsleitung und IT (offen, P-xx) | erstmals konzernweite Pipeline-Sicht, Datenqualität uneinheitlich, Pflege oft erst vor dem Forecast-Meeting |
| PRJ-FOUNDRY2025 | IP-2023-04 | Foundry 2025, Teil-Outsourcing der Gießerei | Transformation | CS | Q2 2023 | Stopp Q1 2024 | gestoppt | Zielvolumen 35 Prozent des Gussvolumens | Operations und Einkauf (offen, P-xx) | höhere Ausschussquoten, längere Reaktionszeiten, Transportkosten, größere Mindestlosgrößen; Lieferant siehe `suppliers.md` |
| PRJ-ATLAS-REVIEW | IP-2024-01 | Project Atlas Review, unabhängige Programmprüfung | Transformation | konzernweit | Q1 2024 Beauftragung | Q2 2024 (Mai) | abgeschlossen | rund 0,25 Mio | Beirat, Audit Committee | zentrales Risiko liegt in der Organisation, nicht in der Software; Grundlage des Scope-Schnitts |
| PRJ-REORG-2024 | IP-2024-02 | Reorganisation nach dem Digitalisierungsprogramm | Transformation | IHS/DGE/CS/LS | Q3 2024 | Q1 2025 | abgeschlossen | rund 0,4 Mio | Kessler | Teilrückbau der Zentralisierung, Projektverantwortung wandert in die Business Units, hybride Strukturen |
| PRJ-PEO-2024 | IP-2024-03 | Umbau des PMO zum Project Excellence Office | Transformation | konzernweit | Q3 2024 | Q4 2024 | abgeschlossen | rund 0,2 Mio | PEO-Leitung (offen, P-xx) | Statusbericht von über 30 auf zwölf Kennzahlen reduziert |
| PRJ-DASHBOARD-2024 | IP-2024-04 | Digitales Projekt-Dashboard | Transformation | konzernweit | Q4 2024 | Q2 2025 | teilweise erfolgreich | rund 0,5 Mio | IT und PEO | verlangt zusätzliche Datenpflege, die Entlastung durch den reduzierten Statusbericht bleibt begrenzt |
| PRJ-SCM-S1S4-2024 | IP-2024-05 | Beschaffungsstrategie mit Versorgungsklassen S1 bis S4 | Transformation | konzernweit | Q3 2024 | laufend | teilweise umgesetzt | rund 0,3 Mio | Leitung Supply Chain (offen, P-xx) | echte Second Source erfordert bei mehreren Komponenten konstruktive Änderungen und neue Zertifizierungen |
| PRJ-GIESSEREI-INV-2024 | INV-2024-01 | Modernisierung der Gießerei Eisenach | Investition | CS | Q3 2024 | laufend bis 2026 | laufend | rund 8,0 Mio | Standortleitung Eisenach (offen, P-xx) | Beiratsbeschluss; Energiekosten, Ausbeute, automatisierte Formtechnik, Wärmerückgewinnung; dient zugleich als eigene Referenzanlage |
| PRJ-DIGITALCORE | IP-2024-06 | Digital Core | Transformation | konzernweit | Q3 2024 | laufend | laufend | Nachfolgebudget aus ONE LTT | IT-Leitung (offen, P-xx) | Finance, Procurement, Business Intelligence, Projektcontrolling, Teile des Master Data Managements |
| PRJ-ENGBACKBONE | IP-2024-07 | Engineering Backbone | Transformation | konzernweit | Q3 2024 | laufend | laufend | Nachfolgebudget aus ONE LTT | Central Engineering (offen, P-xx) | PLM-ERP-Integration und EBOM-MBOM auf reduziertem Umfang |
| PRJ-SERVICETRANSFORM | IP-2024-08 | Service Transformation | Transformation | LS | Q3 2024 | laufend | laufend | Nachfolgebudget aus ONE LTT | Leitung Lifecycle and Service (offen, P-xx) | konzernweite Serviceplattform bleibt zunächst vertagt |
| PRJ-EXCELAMNESTY | IP-2025-01 | Excel Amnesty | Transformation | konzernweit | Q1 2025 | Q4 2025 | erfolgreich | rund 0,3 Mio | IT-Leitung (offen, P-xx) | über 430 gemeldete Dateien, rund 60 als geschäftskritisch eingestuft; führt zur Excel-Governance |

---

## Kundenprojekte

| PRJ-ID | Projektnummer | Name | Bereich | Start | Ende | Status | Volumen | Kunde | Besonderheit |
|---|---|---|---|---|---|---|---|---|---|
| PRJ-WRG-STAHL-2012 | KP-2012-018 | Wärmerückgewinnung Stahlverarbeitung | funktional | 2012 | 2013 | abgeschlossen | rund 0,9 Mio | CUS-001 | erstes industrielles Wärmerückgewinnungsprojekt, Referenz für das neue Geschäftsfeld |
| PRJ-GLASWERK-NORD | KP-2013-042 | Wärmerückgewinnung Glashütte, intern "Glaswerk Nord" | funktional | 2013 | 2014 | abgeschlossen, Marge praktisch aufgebraucht | rund 1,4 Mio | CUS-007 | zu optimistisch angenommene Wärmequellentemperatur; löst TOLERANZ-2013-A für Projektnummer und Auftragswert; Auslöser der Angebotsreviewpflicht ab 500.000 EUR |
| PRJ-CAMPUS-2013 | KP-2013-071 | Erste modulare Großwärmepumpe, Gewerbe- und Forschungsstandort | funktional | 2013 | 2015 | abgeschlossen | rund 2,2 Mio | CUS-028 | erste modulare Anlage, Ausgangspunkt für die spätere Plattformarbeit |
| PRJ-GIESSEREI-WRG-2016 | KP-2016-033 | Abwärmenutzung Gießerei | funktional | 2016 | 2017 | abgeschlossen | rund 1,8 Mio | CUS-011 | erstes Projekt mit vollständigem PMO-Berichtswesen |
| PRJ-PAPIER-DE-2017 | KP-2017-055 | Prozesswärme Papierfabrik Oesterreich | PI | 2017 | 2018 | abgeschlossen | rund 2,6 Mio | CUS-015 | erstes größeres Projekt nach der Internationalisierung |
| PRJ-FOOD-NL-2018 | KP-2018-021 | Prozesskälte und Wärmerückgewinnung Lebensmittelproduktion Niederlande | PI | 2018 | 2019 | abgeschlossen | rund 1,9 Mio | CUS-017 | Betreuung über den neuen Standort Rotterdam |
| PRJ-CHEMIE-RHEIN-2019 | KP-2019-014 | Hochtemperatur-Wärmepumpe Chemiestandort | PI | 2019 | 2020 | abgeschlossen | rund 3,4 Mio | CUS-014 | erstes Projekt mit formellem Design-Freeze-Meilenstein, mehrere späte Engineering Changes |
| PRJ-STAHL-SE-2019 | KP-2019-062 | Wärmerückgewinnung Stahlwerk Schweden | PI | 2019 | 2021 | abgeschlossen | rund 4,1 Mio | CUS-004 | Inbetriebnahme durch die Pandemie verzögert, erste Remote-Unterstützung |
| PRJ-GLAS-CZ-2020 | KP-2020-009 | Abwärmenutzung Glasproduktion Tschechien | PI | 2020 | 2021 | abgeschlossen | rund 2,8 Mio | CUS-010 | erste vollständig virtuelle Werkabnahme (Remote-FAT) |
| PRJ-FOOD-US-2020 | KP-2020-037 | Prozesswärme Lebensmittelwerk USA | PI | 2020 | 2022 | abgeschlossen | rund 3,2 Mio | CUS-019 | Inbetriebnahme mehrfach verschoben, Betreuung über Houston |
| PRJ-QUARTIER-KS-2021 | KP-2021-011 | Quartierswärmeversorgung mit Erdsondenfeld | EU | 2021 | 2023 | abgeschlossen | rund 5,6 Mio | CUS-020 | erstes größeres Quartiersprojekt, Vorläufer der Produktlinie GeoQuart |
| PRJ-GIESSEREI-CN-2021 | KP-2021-048 | Prozesswärme Chemiestandort China | PI | 2021 | 2022 | abgeschlossen | rund 2,4 Mio | CUS-013 | Betreuung über Shanghai, lokale Beschaffungsanteile |
| PRJ-STAHL-ENERGIE-2022 | KP-2022-007 | Großanlage Wärmerückgewinnung Stahl | PI, ab Q4 2022 IHS | 2022 | 2024 | abgeschlossen | rund 7,8 Mio | CUS-002 | im Energiekrisenboom beschleunigt, Schaltschranktermine mehrfach kritisch |
| PRJ-PAPIER-DE-2022 | KP-2022-053 | Prozesswärme Papierfabrik Niederlande | PI, ab Q4 2022 IHS | 2022 | 2023 | abgeschlossen | rund 3,1 Mio | CUS-015 | erste Anlage mit Schaltschränken des Zweitlieferanten, erhöhter Engineering-Aufwand durch abweichende Standards |
| PRJ-GIESSEREI-DE-2023 | KP-2023-016 | Abwärmenutzung Gießerei Deutschland | IHS | 2023 | 2024 | abgeschlossen | rund 2,9 Mio | CUS-011 | Projektabwicklung während der ONE-LTT-Umstellung, doppelte Datenpflege |
| PRJ-QUARTIER-DK-2023 | KP-2023-044 | Wärmenetzanbindung Dänemark | DGE | 2023 | 2025 | abgeschlossen | rund 9,2 Mio | CUS-022 | robustes Auslandsgeschäft trotz schwacher deutscher Nachfrage |
| PRJ-CHEMIE-NL-2023 | KP-2023-078 | Hochtemperatur-Prozesswärme Schweiz | IHS | 2023 | 2024 | abgeschlossen | rund 3,6 Mio | CUS-018 | Anlage im oberen Temperaturbereich der Produktlinie ProcessLift |
| PRJ-OEM-VERDICHTER-2023 | KP-2023-091 | OEM-Verdichterlieferung, Rahmenabruf | CS | 2023 | 2025 | laufend | rund 4,5 Mio | CUS-029 | Kunde ist zugleich Wettbewerber im Wärmepumpenmarkt, bewusst beibehalten |
| PRJ-QUARTIER-STADTWERK-2024 | KP-2024-005 | Quartierssystem Stadtwerk Deutschland | DGE | 2024 | 2026 | laufend | rund 6,4 Mio | CUS-021 | Entscheidung zunächst vertagt, Auftrag nach politischer Klärung erteilt |
| PRJ-WAERMENETZ-A-2024 | KP-2024-072 | Wärmenetz Großprojekt A | DGE | Q4 2024 | 2026 | laufend | rund 11,0 Mio | CUS-023 | eines der beiden Projekte, nach deren Gewinn die Einstellungsbremse aufgehoben wurde |
| PRJ-WAERMENETZ-B-2024 | KP-2024-076 | Wärmenetz Großprojekt B | DGE | Q4 2024 | 2027 | laufend | rund 8,7 Mio | CUS-024 | zweites der beiden Wärmenetzprojekte aus Q4 2024 |
| PRJ-STAHL-US-2025 | KP-2025-013 | Wärmerückgewinnung Stahlwerk USA | IHS | 2025 | 2026 | laufend | rund 5,2 Mio | CUS-006 | größtes US-Projekt bisher, Betreuung über Houston |
| PRJ-FOOD-DE-2025 | KP-2025-041 | Standardanlage Lebensmittelproduktion | IHS | 2025 | 2026 | laufend | rund 2,1 Mio | CUS-016 | weitgehend konfiguriertes ProcessLift-Projekt, geringer Sonderanteil |
| PRJ-RETROFIT-2025 | KP-2025-058 | Retrofit und Leistungserhöhung Bestandsanlage | LS | 2025 | 2025 | abgeschlossen | rund 1,3 Mio | CUS-001 | Retrofit einer Anlage aus 2012, Servicehistorie nur unvollständig verfügbar |

---

## Hinweise zur Auflösung offener Referenzen

- Personenreferenzen sind als `(offen, P-xx)` markiert. Sie werden gegen `canon/registry/people.md`
  aufgelöst, sobald dieses vorliegt. Bis dahin ist die Rollenbezeichnung verbindlich, nicht die Person.
- Kundenreferenzen mit dreistelliger Nummer sind auf `canon/registry/customers.md` aufgelöst und dort verbindlich
  definiert. Bei Abweichung in Name, Branche oder Land gilt `customers.md`.
- Das Präfix für Entwicklungsprojekte lautet `ENT-JJJJ-NN`. `EP-NN` ist reserviert für die
  Entscheidungsepisoden in `manifest/clusters.jsonl` und darf hier nicht verwendet werden.
- Der Gießereilieferant aus PRJ-FOUNDRY2025 ist in `canon/registry/suppliers.md` geführt.

## Aufgelöste Toleranzen

| Toleranz | Auflösung |
|---|---|
| TOLERANZ-2013-A | Projektnummer KP-2013-042, Auftragswert rund 1,4 Mio EUR. Kundenname in `customers.md`. |
| TOLERANZ-2015-A | Die erste Plattform heißt Modulplattform M1; die Produktlinienbezeichnung ProcessLift entsteht später. |
| TOLERANZ-2018-A | Kaufpreis Rothenberg rund 24 Mio EUR, Erwerb von 100 Prozent der Anteile, zusätzlicher Integrationsaufwand rund 1,5 Mio EUR. |
| TOLERANZ-2019-A | Make-Strategie mit rund 12,0 Mio EUR über 2019 bis 2021, Aufteilung in `finance.md`. |
| TOLERANZ-2022-A | Unternehmenswert beim Hansera-Einstieg rund 150 Mio EUR für 100 Prozent, erworben werden 60 Prozent. Die Ausgestaltung des Mitarbeiterbeteiligungsprogramms bleibt offen. |
