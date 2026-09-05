---
doc_id: LTT-2021-0512-SCM-001
titel: "Risikoregister: Verbleibende Single-Source-Positionen erfassen"
dokumenttyp: Risikoregister
datum: 2021-05-12
verfasser: Petra Ehlers
rolle: Leiterin strategischer Einkauf
organisationseinheit: SCM
empfaenger: ["-"]
projekt: IP-2021-01
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [bereichsintern, projektintern]
ablageort: einkauf_scm
---

# Risikoregister: Verbleibende Single-Source-Positionen erfassen

Teilregister zum Beschaffungsrisikoregister, Fassung 1.0, Stand 12. Mai 2021.
Erstellt: Strategischer Einkauf, P. Ehlers. Bezug: POL-SCM-001, Dual-Source-Grundsatz für
Komponenten der Risikokategorie A, Fassung vom 12. April 2021; POL-EK-001 v2.0,
Lieferantenbewertung mit dem zusätzlichen Kriterium Versorgungssicherheit; POL-SCM-005 v2.0,
Sicherheitsbestände.
Verteiler: U. Damm (Supply Chain & Operations Planning), H. Zeller (Operations),
Dr. I. Sommer (Central Engineering), B. Hoffmann (QM), D. Anselm (Controlling),
A. Puhl (Standort Eisenach); nachrichtlich Dr. J. Mahlberg.
Fortschreibung: monatlich in der Supply-Chain-Runde, vollständige Neubewertung halbjährlich.

## 1 Anlass und Abgrenzung

Der Dual-Source-Grundsatz vom 12. April 2021 verlangt für Komponenten der Risikokategorie A zwei
qualifizierte Lieferanten. Er nimmt kundenspezifische Wärmetauscher, proprietäre SPS-Hardware,
bestimmte Frequenzumrichter und komplexe Schaltschrankkonfigurationen ausdrücklich aus.

Dieses Teilregister erfasst, was nach dieser Regel offen bleibt. Es ist keine Bewertung der Regel,
sondern die Bestandsaufnahme der Positionen, die auch nach ihrer Umsetzung nur eine Quelle haben
werden. Zwölf Positionen sind aufgenommen; sie decken das Beschaffungsvolumen der Risikokategorie A
nach heutiger Einstufung weitgehend ab.

Abgegrenzt sind: Positionen unterhalb der Risikokategorie A, Fremdmontage- und Bauleistungen,
Ingenieurdienstleistungen sowie sämtliche Positionen des indirekten Bedarfs.

Datenbasis ist das Beschaffungsjahr 2020. Für Eisenach liegen die Volumina im dortigen ERP in
abweichender Materialgruppenstruktur; sie wurden von Hand zugeordnet und sind entsprechend gerundet.
Eine belastbare gemeinsame Auswertung ist erst nach Zusammenführung der Warengruppenschlüssel im
Rahmen von PRJ-SCM-ZENTRAL-2021 möglich.

## 2 Bewertungsmaßstab

Auswirkung (A) und Eintrittswahrscheinlichkeit (E) werden auf einer Skala von 1 bis 4 bewertet,
die Risikozahl (RZ) ist ihr Produkt.

| Stufe | Auswirkung bei Ausfall der Quelle | Eintrittswahrscheinlichkeit innerhalb von 24 Monaten |
|---|---|---|
| 1 | Umplanung ohne Terminwirkung | unwahrscheinlich |
| 2 | Verzug einzelner Projekte bis vier Wochen | denkbar |
| 3 | Verzug mehrerer Projekte, Vertragsstrafen möglich | wahrscheinlich, Anzeichen vorhanden |
| 4 | Lieferunfähigkeit einer Produktlinie | wahrscheinlich, bereits eingetreten oder angekündigt |

Ab RZ 9 ist eine Maßnahme zu benennen und zu terminieren. Ab RZ 12 ist die Position monatlich zu
berichten.

Die Eintrittswahrscheinlichkeit stützt sich auf die Liefertreuewerte 2020 nach POL-EK-001 und auf die
seit dem vierten Quartal 2020 von mehreren Lieferanten verlängerten Lieferzeitzusagen für
Leistungselektronik und Steuerungskomponenten.

## 3 Register

| ID | Position | Aktuelle Quelle | Status Zweitquelle | Volumen 2020 | WBZ | A | E | RZ |
|---|---|---|---|---:|---:|---:|---:|---:|
| SCM-R-01 | Schaltschränke, komplexe Konfigurationen ab 1 MW Anlagenleistung | SUP-001 NordControl Schaltanlagen GmbH | Ausnahme nach POL-SCM-001 | 5,4 Mio EUR | 14 Wo | 4 | 3 | 12 |
| SCM-R-02 | Frequenzumrichter für drehzahlgeregelte Verdichterantriebe über 250 kW | SUP-014 Vectron Drive Systems GmbH | Ausnahme nach POL-SCM-001; SUP-015 Baltic Power Electronics OUE bemustert bisher nur Kleinantriebe | 2,1 Mio EUR | 22 Wo | 4 | 4 | 16 |
| SCM-R-03 | SPS-Hardware und zugehörige Steuerungsplattform | Herstellergebunden, Bezug über SUP-017 Auconta Steuerungstechnik GmbH | Ausnahme nach POL-SCM-001, Zweitquelle technisch ausgeschlossen | 1,4 Mio EUR | 16 Wo | 4 | 3 | 12 |
| SCM-R-04 | Kundenspezifische Wärmetauscher, Hochtemperatur und Sonderwerkstoffe | SUP-009 Calorex Spezialwärmetauscher GmbH | Ausnahme nach POL-SCM-001 | 3,2 Mio EUR | 18 Wo | 3 | 3 | 9 |
| SCM-R-05 | Plattenwärmetauscher der Modulplattform M1 | SUP-006 Thermoplan Wärmetechnik GmbH, SUP-007 Nordisk Varmeteknik A/S | erfüllt | 2,6 Mio EUR | 10 Wo | 3 | 1 | 3 |
| SCM-R-06 | Elektromotoren ab Baugröße 315 | SUP-012 Kramer Elektromaschinen GmbH, SUP-013 Motori Adriatica S.p.A. | erfüllt für Kassel, Eisenach bezieht nur SUP-012 | 1,9 Mio EUR | 12 Wo | 3 | 2 | 6 |
| SCM-R-07 | Industriearmaturen Standard | SUP-021 Armaturenwerk Vogtland GmbH, SUP-022 Valvo Nord A/S | erfüllt seit Januar 2021 | 0,9 Mio EUR | 8 Wo | 2 | 2 | 4 |
| SCM-R-08 | Sicherheitsarmaturen für Ammoniakkreisläufe mit Baumusterprüfung | SUP-021 Armaturenwerk Vogtland GmbH | keine Zweitquelle mit gleicher Zulassung ermittelt | 0,4 Mio EUR | 20 Wo | 4 | 2 | 8 |
| SCM-R-09 | Gussteile Verdichtergehäuse | Gießerei Eisenach, ergänzend SUP-005 Werragrund Guss GmbH | konzernintern gebunden, siehe 4.4 | 2,3 Mio EUR | 15 Wo | 3 | 2 | 6 |
| SCM-R-10 | Druckbehälter und Apparate | SUP-010 Apparatebau Sauerland GmbH, SUP-011 Vessel Technik Brabant B.V. | formal erfüllt, SUP-011 bisher zwei Aufträge | 2,8 Mio EUR | 16 Wo | 3 | 2 | 6 |
| SCM-R-11 | Messtechnik und Sensorik Prozesswärme | SUP-023 Messtechnik Ostwestfalen GmbH, SUP-024 Sensoria Instruments AG | erfüllt, Prüfmittelfreigabe QM offen | 0,7 Mio EUR | 9 Wo | 2 | 2 | 4 |
| SCM-R-12 | Bohrleistungen Erdsondenfelder | SUP-027 Geobohr Mitteldeutschland GmbH, SUP-028 Aardwarmte Boortechniek B.V. | regional gebunden, je Region faktisch eine Quelle | 1,1 Mio EUR | 24 Wo | 3 | 3 | 9 |

Die Bewertung von SCM-R-11 ist noch nicht mit dem Qualitätsmanagement abgestimmt.

## 4 Erläuterungen zu den kritischen Positionen

### 4.1 SCM-R-02, Frequenzumrichter über 250 kW

Die höchste Risikozahl des Registers. Vectron liefert seit 2012, technisch beanstandungsfrei. Die
zugesagte Wiederbeschaffungszeit ist seit dem vierten Quartal 2020 von zehn auf zweiundzwanzig Wochen
gestiegen, für zwei Baugrößen liegen uns nur noch Rahmenzusagen ohne feste Termine vor.

Der Wechsel scheitert nicht am Einkauf. Die Parametersätze der Verdichterregelung sind auf die
Vectron-Baureihe abgestimmt; ein anderes Fabrikat verlangt eine erneute Abnahme der Regelung auf den
Eisenacher Prüfständen und eine Anpassung der Applikationssoftware. Diesen Aufwand kann der Einkauf
weder beauftragen noch abschätzen. Baltic Power Electronics ist seit Januar 2021 gelistet und hat
zwei Kleinantriebe bemustert; für die Leistungsklasse über 250 kW liegt keine Bemusterung vor.

Solange die Position als Ausnahme geführt wird, ist die Bestandsreichweite die einzige wirksame
Maßnahme. Sie ist mit POL-SCM-005 v2.0 reduziert worden.

### 4.2 SCM-R-01, komplexe Schaltschränke

NordControl fertigt rund fünfundsechzig Prozent unserer Schaltschränke. Die Zusammenarbeit ist gut,
das ist nicht der Punkt. Der Punkt ist, dass unsere Schaltplanstruktur in EPLAN über Jahre an die
Fertigungsweise von NordControl angepasst wurde. Auconta und Litec Automation fertigen für uns
kleinere Standardschränke und Benelux-Projekte; beide müssten für die komplexen Konfigurationen einen
eigenen Makrobestand aufbauen, den wir liefern müssten und heute nicht gepflegt vorhalten.

Die Abhängigkeit ist seit 2019 bekannt und war auch damals eine bewusste Entscheidung. Sie ist es
weiterhin. Neu ist nur, dass sie jetzt in einem Register steht.

### 4.3 SCM-R-03, SPS-Hardware

Hier gibt es nichts zu qualifizieren. Ein Wechsel der Steuerungsplattform bedeutet die Neuerstellung
des gesamten Applikationsbestands einschließlich der Bibliotheken aus der Elektrotechnik. Die Position
bleibt dauerhaft Einzelquelle. Ich schlage vor, sie im Register zu belassen und ausschließlich über
Bestand und über eine schriftliche Ersatzteilzusage des Herstellers zu behandeln, nicht über
Zweitquellensuche.

### 4.4 SCM-R-09, Gussteile Verdichtergehäuse

Die Position ist der Vollständigkeit halber aufgenommen, obwohl sie von POL-SCM-001 nicht erfasst
wird: Die Hauptquelle ist unsere eigene Gießerei in Eisenach. Aus Sicht der Versorgungssicherheit ist
das eine Einzelquelle wie jede andere, mit dem Unterschied, dass wir sie selbst steuern und dass
Werragrund Guss nur einen Teil des Spektrums abdeckt. Eine breitere externe Absicherung würde die
Auslastungszusagen für Eisenach berühren und ist deshalb nicht im Einkauf zu entscheiden. Ich bitte um
eine Festlegung, ob konzerninterne Einzelquellen in diesem Register weitergeführt werden sollen.

### 4.5 SCM-R-12, Bohrleistungen

Für die Quartiersprojekte der Produktlinie GeoQuart bestehen zwei qualifizierte Bohrunternehmen, die
sich aber regional nicht überschneiden. Für PRJ-QUARTIER-KS-2021 steht damit nur Geobohr zur
Verfügung. Formal ist der Grundsatz erfüllt, praktisch nicht. Der Fall zeigt, dass die Zählung
qualifizierter Lieferanten allein nicht ausreicht; die Verfügbarkeit für das konkrete Projekt gehört
mitbewertet.

## 5 Maßnahmen

| Nr | Bezug | Maßnahme | Verantwortlich | Termin | Stand |
|---|---|---|---|---|---|
| M-01 | SCM-R-02 | Aufwandsschätzung für die Requalifizierung der Verdichterregelung auf ein zweites Umrichterfabrikat | Dr. K. Ludwig (T&D), R. Wiesner (Elektrotechnik) | 30.09.2021 | angefragt |
| M-02 | SCM-R-02 | Bemusterung Baltic Power Electronics in der Leistungsklasse über 250 kW, sofern M-01 wirtschaftlich darstellbar | Strategischer Einkauf | offen, abhängig von M-01 | nicht begonnen |
| M-03 | SCM-R-02, SCM-R-03 | Überprüfung der Bestandsreichweite für die Positionen mit Ausnahmestatus, getrennt von der allgemeinen Bestandsvorgabe | U. Damm, D. Anselm | 30.06.2021 | in Abstimmung |
| M-04 | SCM-R-01 | Bewertung des Aufwands für einen zweiten Makrobestand in EPLAN für komplexe Schaltschrankkonfigurationen | R. Wiesner | 31.10.2021 | angefragt |
| M-05 | SCM-R-03 | Schriftliche Ersatzteil- und Abkündigungszusage über SUP-017 einholen, Mindestlaufzeit sieben Jahre | Strategischer Einkauf | 31.07.2021 | in Bearbeitung |
| M-06 | SCM-R-08 | Marktrecherche Sicherheitsarmaturen mit gleichwertiger Baumusterprüfung | Strategischer Einkauf, QM | 30.11.2021 | nicht begonnen |
| M-07 | SCM-R-09 | Grundsatzentscheidung zur Behandlung konzerninterner Einzelquellen im Register | U. Damm | 30.06.2021 | offen |
| M-08 | SCM-R-12 | Aufnahme der projektbezogenen Verfügbarkeit als zusätzliches Merkmal in die Lieferantenbewertung nach POL-EK-001 | Strategischer Einkauf | 31.12.2021 | Entwurf |
| M-09 | alle | Zusammenführung der Warengruppenschlüssel Kassel und Eisenach als Voraussetzung einer belastbaren Volumenbewertung | PRJ-SCM-ZENTRAL-2021 | offen | in Planung |

## 6 Einschätzung des Erstellers

Zwei Feststellungen, die ich nicht in die Tabelle schreiben kann.

Erstens: Die vier Ausnahmen des Dual-Source-Grundsatzes tragen zusammen rund zwölf Millionen Euro
Beschaffungsvolumen und vier der fünf höchsten Risikozahlen dieses Registers. Der Grundsatz wirkt
dort, wo wir ohnehin zwei Quellen hatten, und nimmt die Positionen aus, für die er geschrieben wurde.
Das ist kein Vorwurf an die Regel: Die Ausnahmen sind technisch begründet und mir waren sie bei der
Abstimmung bekannt. Es heißt aber, dass die Regel allein das Risiko nicht senkt, und dass die
Entlastung, die im April angenommen worden ist, so nicht eintreten wird.

Zweitens: Die Ausnahmepositionen waren bisher über Sicherheitsbestände abgedeckt. Diese Bestände sind
nach der Neufassung von POL-SCM-005 zugunsten des Working Capital zurückgenommen worden. Damit sind
im Abstand weniger Wochen zwei Maßnahmen reduziert worden, die dasselbe Risiko abdecken sollten. Für
die Positionen SCM-R-02 und SCM-R-03 halte ich das für nicht vertretbar und bitte um eine gesonderte
Reichweitenvorgabe; das ist Gegenstand von M-03.

Der Einkauf kann Zweitquellen suchen, bewerten und verhandeln. Qualifizieren kann er sie nicht. Jede
der offenen Positionen hängt an Konstruktions-, Software- oder Prüfaufwand in Central Engineering, in
der Elektrotechnik oder in Technology & Development. Ohne verbindliche Kapazitätszusage aus diesen
Bereichen bleibt dieses Register bis zur nächsten Fassung unverändert, und ich werde im Herbst
dieselben zwölf Zeilen vorlegen.

Die in Vorbereitung befindliche Einführung eines Sales-&-Operations-Planning-Verfahrens wird für die
Bedarfsvorschau der langlaufenden Positionen vorausgesetzt. Ob sie den Vorlauf liefert, den eine
Wiederbeschaffungszeit von zweiundzwanzig Wochen verlangt, kann ich heute nicht beurteilen.

## 7 Offene Punkte

- Einstufungskriterien der Risikokategorie A sind bisher nicht schriftlich festgelegt; die Zuordnung
  in diesem Register beruht auf der Arbeitsliste der Supply Chain Task Force von 2020.
- Volumina Eisenach manuell zugeordnet, Abweichung nach oben und unten möglich.
- Bewertung SCM-R-11 mit QM abzustimmen.
- Behandlung konzerninterner Einzelquellen ungeklärt, siehe M-07.
