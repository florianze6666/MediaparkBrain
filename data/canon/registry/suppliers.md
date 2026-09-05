# Lieferantenstammregister

Kanon-Detailstufe (Fork). Grundlage: `canon/annals/*.md`. Alle Lieferanten sind FIKTIV - reale Namen
gelten ausschließlich für Standardsoftware und stehen in `canon/registry/systems.md`.

Versorgungsklassen nach der Beschaffungsstrategie Q3 2024 (Annalen 2024): S1 Commodity, S2 Preferred
Supplier Components, S3 Strategic Components, S4 Critical Single Source. Vor Q3 2024 existiert die
Klassifikation nicht - Dokumente vor diesem Datum dürfen sie nicht verwenden. Bis dahin gilt die
Risikokategorie A aus dem Dual-Source-Grundsatz 2021 (Annalen 2021).

## Schaltschrankbau und Automatisierung

| SUP-ID | Name | Sitz | Warengruppe | Beziehung seit | Status je Zeitraum | Klasse ab 2024 | Bewertungshistorie | Abhängigkeit |
|---|---|---|---|---|---|---|---|---|
| SUP-001 | NordControl Schaltanlagen GmbH | Paderborn, DE | Schaltschränke, Schaltanlagenbau | 2012 | 2012-2018 einer von mehreren; ab 2019 Hauptlieferant mit rund 65 Prozent Anteil; 2022 mehrfach Terminzusagen nicht gehalten; 2024 Anteilsreduktion beschlossen; ab 2025 bevorzugt für komplexe industrielle Großanlagen | S4 für komplexe Schaltschrankkonfigurationen, sonst S3 | Qualität durchgehend gut, Termintreue 2022 stark abgefallen, danach erholt; Innovationsfähigkeit hoch | hoch - technisch führend, kundenseitig teils namentlich gewünscht |
| SUP-002 | ElektroPlan Süd GmbH | Augsburg, DE | Schaltschränke | 2022 | Q3/Q4 2022 als zweiter Schaltschrankpartner qualifiziert; 2023-2024 wachsender Anteil; ab 2025 primär Kapazitäts- und Ausweichlieferant | S2 | Termintreue gut, Dokumentationsstandard abweichend von NordControl | mittel |
| SUP-003 | RheinMain Automation Systems GmbH | Rüsselsheim, DE | Schaltschränke, standardisierte Baugruppen | 2024 | Rahmenvertrag Q3 2024 über drei Jahre mit Option auf zwei weitere, Zielvolumen zunächst rund 30 Prozent des Schaltschrankbedarfs; erste Projekte mit Dokumentationsproblemen und erhöhten Nacharbeitskosten; ab 2025 für standardisierte GeoQuart-Systeme | S2 | Preis günstig, Dokumentationsqualität anfangs mangelhaft, Nacharbeitsquote 2024 erhöht | mittel |
| SUP-017 | Auconta Steuerungstechnik GmbH | Karlsruhe, DE | SPS-Hardware, proprietäre Steuerungsplattform | 2013 | durchgehend; 2021 vom Dual-Source-Grundsatz ausgenommen, weil eine Substitution Umprogrammierung und Neuzertifizierung erfordern würde | S4 | Qualität hoch, Preisentwicklung überdurchschnittlich, Lieferzeiten 2021-2022 kritisch | sehr hoch - Single Source, Wechselkosten prohibitiv |
| SUP-018 | Litec Automation B.V. | Enschede, NL | SPS-Hardware, Standardkomponenten | 2016 | durchgehend, deckt den nicht proprietären Teil ab | S2 | unauffällig | niedrig |

## Wärmetauscher und Druckbehälter

| SUP-ID | Name | Sitz | Warengruppe | Beziehung seit | Status je Zeitraum | Klasse ab 2024 | Bewertungshistorie | Abhängigkeit |
|---|---|---|---|---|---|---|---|---|
| SUP-006 | Thermoplan Wärmetechnik GmbH | Bielefeld, DE | Plattenwärmetauscher | 2011 | durchgehend, Hauptlieferant Standardplatten | S2 | stabil, Termintreue gut | mittel |
| SUP-007 | Nordisk Varmeteknik A/S | Kolding, DK | Plattenwärmetauscher | 2017 | zweite Quelle im Rahmen des Dual-Source-Grundsatzes 2021 | S2 | stabil | niedrig |
| SUP-008 | Rohrbau Thermik GmbH | Duisburg, DE | Rohrbündelwärmetauscher | 2012 | durchgehend | S2 | Qualität gut, Termintreue schwankend | mittel |
| SUP-009 | Calorex Spezialwärmetauscher GmbH | Krefeld, DE | kundenspezifische Wärmetauscher, Hochtemperaturausführungen | 2014 | durchgehend; 2021 vom Dual-Source-Grundsatz ausgenommen, weil jede Alternative eine konstruktive Neuauslegung erfordern würde | S4 | Qualität sehr hoch, Preis hoch, Lieferzeit lang | sehr hoch - Single Source, technisch begründet |
| SUP-010 | Apparatebau Sauerland GmbH | Arnsberg, DE | Druckbehälter, Sammler | 2011 | durchgehend | S2 | stabil | mittel |
| SUP-011 | Vessel Technik Brabant B.V. | Eindhoven, NL | Druckbehälter | 2019 | zweite Quelle seit dem Dual-Source-Grundsatz 2021 | S2 | stabil | niedrig |

## Antriebstechnik und Leistungselektronik

| SUP-ID | Name | Sitz | Warengruppe | Beziehung seit | Status je Zeitraum | Klasse ab 2024 | Bewertungshistorie | Abhängigkeit |
|---|---|---|---|---|---|---|---|---|
| SUP-012 | Kramer Elektromaschinen GmbH | Bocholt, DE | Elektromotoren | 2011 | durchgehend; 2021 Bündelungssynergie nach Zentralisierung des Einkaufs | S1 | stabil | niedrig |
| SUP-013 | Motori Adriatica S.p.A. | Vicenza, IT | Elektromotoren | 2015 | zweite Quelle | S1 | stabil, Preis günstig | niedrig |
| SUP-014 | Vectron Drive Systems GmbH | Erlangen, DE | Frequenzumrichter, projektspezifisch parametrierte Baureihe | 2012 | durchgehend; Engpass 2020-2022; 2021 vom Dual-Source-Grundsatz ausgenommen, weil die Reglerparametrierung der LTT-Verdichter auf diese Baureihe abgestimmt ist | S4 | Qualität hoch, Termintreue 2021-2022 sehr schlecht, Preissteigerungen überdurchschnittlich | sehr hoch - Single Source für die kritische Baureihe |
| SUP-015 | Baltic Power Electronics OUE | Tallinn, EE | Frequenzumrichter, Standardbaureihen | 2021 | 2021 als zweite Quelle für Standardanwendungen qualifiziert, deckt die proprietäre Baureihe nicht ab | S2 | Termintreue gut, Dokumentation schwach | niedrig |
| SUP-016 | Drivetec Nord AB | Västerås, SE | Frequenzumrichter, Großleistung | 2022 | Notqualifikation während der Lieferkrise 2022, seither Kapazitätsreserve | S2 | in wenigen Projekten erprobt | niedrig |
| SUP-025 | Kontakta Schaltgeräte GmbH | Wuppertal, DE | elektrische Schaltgeräte, Leistungsschalter | 2011 | durchgehend; Leistungsschalter 2022 kritischer Engpass | S2 | Termintreue 2022 schlecht, danach erholt | mittel |

## Hydraulik, Armaturen, Sensorik

| SUP-ID | Name | Sitz | Warengruppe | Beziehung seit | Status je Zeitraum | Klasse ab 2024 | Bewertungshistorie | Abhängigkeit |
|---|---|---|---|---|---|---|---|---|
| SUP-019 | Hagenbeck Pumpen GmbH | Hameln, DE | Pumpen, Pumpengruppen | 2011 | durchgehend; seit der Standardisierung 2012 in wiederverwendbaren Baugruppen gesetzt | S2 | stabil | mittel |
| SUP-020 | Pompes Rhodania SAS | Lyon, FR | Pumpen | 2018 | zweite Quelle | S1 | stabil | niedrig |
| SUP-021 | Armaturenwerk Vogtland GmbH | Plauen, DE | Ventile, Armaturen | 2012 | durchgehend; einzelne Ventilserien waren 2012-2020 faktisch Single Source, seit 2021 zweite Quelle qualifiziert | S2 | stabil | mittel |
| SUP-022 | Valvo Nord A/S | Odense, DK | Ventile, Regelarmaturen | 2021 | zweite Quelle im Rahmen des Dual-Source-Grundsatzes | S2 | stabil | niedrig |
| SUP-023 | Messtechnik Ostwestfalen GmbH | Gütersloh, DE | Sensorik, Temperatur- und Druckmesstechnik | 2011 | durchgehend; Engpass bei elektronischer Sensorik 2022 | S2 | Termintreue 2022 schlecht | mittel |
| SUP-024 | Sensoria Instruments AG | Winterthur, CH | Sensorik, Sonderanwendungen Hochtemperatur | 2019 | für ProcessLift-Anwendungen oberhalb 120 Grad Celsius | S3 | Qualität sehr hoch, Preis hoch | mittel |

## Guss, Rohmaterial und Bauleistungen

| SUP-ID | Name | Sitz | Warengruppe | Beziehung seit | Status je Zeitraum | Klasse ab 2024 | Bewertungshistorie | Abhängigkeit |
|---|---|---|---|---|---|---|---|---|
| SUP-004 | Moravia Precision Castings a.s. | Blansko, CZ | Grau- und Sphäroguss, Verdichtergehäuse | 2023 | Q2 2023 im Programm Foundry 2025 qualifiziert, Zielvolumen zunächst rund 35 Prozent des Gussvolumens, Rahmenvertrag über drei Jahre mit einem Zielvolumen von rund 2,4 Mio EUR jährlich; Ausbau Q1 2024 gestoppt; seit 2024 auf rund 15 Prozent des Volumens begrenzt | S2 | Stückkosten niedrig, Ausschussquote nach mechanischer Bearbeitung erhöht, Reaktionszeit bei Konstruktionsänderungen lang, Mindestlosgrößen hoch | niedrig - bewusst begrenzt |
| SUP-005 | Werragrund Guss GmbH | Eschwege, DE | Guss, Kleinserien und Prototypen | 2015 | Ergänzung zur eigenen Gießerei bei Kapazitätsspitzen | S1 | stabil | niedrig |
| SUP-027 | Geobohr Mitteldeutschland GmbH | Halle (Saale), DE | Erdsondenbohrung für GeoQuart-Projekte | 2016 | regionale Vergabe je Projekt, kein Rahmenvertrag | S1 | projektabhängig, insgesamt zufriedenstellend | niedrig |
| SUP-028 | Aardwarmte Boortechniek B.V. | Deventer, NL | Erdsondenbohrung Benelux | 2019 | regionale Vergabe je Projekt | S1 | stabil | niedrig |
| SUP-029 | Stahlhandel Weser GmbH | Bremen, DE | Blech, Profile, Rohmaterial | 2011 | durchgehend | S1 | stabil, Preisvolatilität marktbedingt | niedrig |

## Die vier faktischen Single-Source-Fälle

Der Dual-Source-Grundsatz von 2021 (Annalen 2021) nimmt vier Komponentengruppen ausdrücklich aus. Diese
sind seit Q3 2024 als S4 klassifiziert und unterliegen dem Management-Review:

| Ausnahme laut Grundsatz 2021 | Lieferant | Warum keine Second Source |
|---|---|---|
| kundenspezifische Wärmetauscher | SUP-009 Calorex | jede Alternative erfordert konstruktive Neuauslegung und neue Zertifizierung |
| proprietäre SPS-Hardware | SUP-017 Auconta | Substitution erfordert vollständige Umprogrammierung der Anlagensteuerung |
| bestimmte Frequenzumrichter | SUP-014 Vectron | Reglerparametrierung der LTT-Verdichter ist auf diese Baureihe abgestimmt |
| komplexe Schaltschrankkonfigurationen | SUP-001 NordControl | Bibliotheken, Klemmensystem und Prüfprotokolle sind nicht übertragbar; einzelne Kunden verlangen die Ausführung namentlich |

Damit bleiben genau die kritischsten Komponenten Single Source - dokumentiert, aber nicht gelöst. Für
S4 gelten seit Q3 2024 zusätzlich Mindestbestand, Second-Source-Roadmap, technische
Substitutionsanalyse, Lieferanten-Business-Continuity-Plan und jährlicher Financial-Health-Check. Die
Umsetzung ist unterschiedlich konsequent: der strategische Einkauf spricht 2025 von rund 85 Prozent
Compliance, interne Audits kommen eher auf 70 Prozent.

## Aufgelöste Toleranzen

- **TOLERANZ-2019-B** (teilweise): Vertragsform mit NordControl ist ein Rahmenvertrag mit jährlicher
  Mengenplanung und Preisgleitklausel, erstmals 2019 abgeschlossen, Laufzeit drei Jahre, seither
  zweimal verlängert. Der Ansprechpartner gehört in `canon/registry/people.md`.
- **TOLERANZ-2023-C**: Der tschechische Gießereilieferant ist SUP-004 Moravia Precision Castings a.s.,
  Blansko; Rahmenvertrag über drei Jahre, Zielvolumen rund 2,4 Mio EUR jährlich.
- **TOLERANZ-2024-D**: RheinMain-Rahmenvertrag Q3 2024, drei Jahre mit Option auf zwei weitere,
  Zielvolumen zunächst rund 30 Prozent des Schaltschrankbedarfs.
- **TOLERANZ-2024-E**: Als S4 klassifiziert sind die vier oben genannten Komponentengruppen.
