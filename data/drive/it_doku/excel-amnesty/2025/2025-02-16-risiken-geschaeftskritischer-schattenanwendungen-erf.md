---
doc_id: LTT-20250216-IT-03
titel: "Risikoregister: Risiken geschäftskritischer Schattenanwendungen erfassen"
dokumenttyp: Risikoregister
datum: 2025-02-16
verfasser: Sven Bruckner
rolle: Informationssicherheitsbeauftragter
organisationseinheit: IT
empfaenger: "-"
projekt: Excel Amnesty
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [it-security-restricted, projektintern]
ablageort: it_doku
---

**Risikoregister ISB-2025-004 - geschäftskritische Schattenanwendungen**

Fassung 1.0, Stand 16.02.2025
Bearbeitung: S. Bruckner, Informationssicherheitsbeauftragter, IT
Grundlage: Meldeliste der Erhebung Excel Amnesty, Auswertungsstand 07.02.2025
Bezug: POL-IT-002 v3.0 Informationssicherheitsrichtlinie, POL-IT-007 v1.0 NIS2-Vorbereitung,
POL-IT-001 v3.0 Zentrale Benutzerverwaltung und Rollenkonzept, POL-IT-006 v1.0 Stammdatenrichtlinie

## Vorbemerkung

Die Erhebung hat Transparenz geschaffen. Beseitigt hat sie kein einziges Risiko. Dieses Register hält
fest, was mit der Meldeliste sichtbar geworden ist, und ordnet es der Bewertungssystematik der
Informationssicherheitsrichtlinie zu. Es ist keine technische Prüfung der gemeldeten Dateien; eine
solche hat bisher nicht stattgefunden.

Gemeldet wurden mehr als 430 Dateien. Rund 60 davon sind als geschäftskritisch eingestuft worden. Die
Einstufung haben die Fachbereiche selbst vorgenommen, an den Kriterien war ich nicht beteiligt. Ich
behandle die 60 als untere Schranke und nicht als Ergebnis. Erfasst sind Projektkalkulationen,
Lieferterminlisten, Ressourcenpläne, Inbetriebnahmechecklisten, Ersatzteilmatrizen,
Angebotskonfiguratoren und Berechnungstools.

Der Bestand ist nicht neu. Mit der Übernahme in Eisenach sind 2018 lokale Datenbanken und Tabellen in
die LTT gekommen, deren Ablösung seither angekündigt und nie abgeschlossen worden ist. Ein Teil der
jetzt gemeldeten Werkzeuge füllt zudem genau die Lücken, die mit dem Zuschnitt der Programme im Juni
2024 offen geblieben sind, insbesondere zwischen Konstruktion und Fertigung. Das erklärt die Dateien,
es entlastet sie nicht: für die Informationssicherheit ist eine geduldete Anwendung dasselbe wie eine
ungeregelte.

Die Sanktionsfreiheit der Meldung war die Voraussetzung dafür, dass überhaupt gemeldet wurde. Sie gilt
für die Meldung. Sie ist keine Zusage über den weiteren Umgang mit den Dateien, und sie darf nicht dazu
führen, dass die Risiken mit dem Ende der Erhebung als erledigt gelten.

## Bewertungsmaßstab

Eintrittswahrscheinlichkeit W: 1 unwahrscheinlich, 2 möglich, 3 wahrscheinlich, 4 nahezu sicher oder
bereits beobachtet.
Auswirkung A: 1 gering, 2 spürbar, 3 schwerwiegend, 4 kritisch für den betroffenen Prozess.
Risikowert = W mal A. Klassen: 1 bis 3 niedrig, 4 bis 6 mittel, 8 bis 9 hoch, 12 bis 16 sehr hoch.
Schutzziele: V Vertraulichkeit, I Integrität, Vf Verfügbarkeit, N Nachvollziehbarkeit.

## Register - Bewertung

| ID | Risiko | Schutzziel | W | A | Wert | Klasse |
|---|---|---|---:|---:|---:|---|
| SR-01 | Pflege und Verständnis einer geschäftskritischen Datei liegen bei genau einer Person, ohne Vertretung | Vf, N | 3 | 3 | 9 | hoch |
| SR-02 | Ablageorte sind nicht nach dem Rollenkonzept berechtigt, Schreibzugriff ist faktisch offen | V, I | 3 | 3 | 9 | hoch |
| SR-03 | Angebotskonfiguratoren und Berechnungstools haben keinen freigegebenen Stand, Änderungen sind nicht nachweisbar | I, N | 4 | 3 | 12 | sehr hoch |
| SR-04 | Dateien liegen teilweise auf Endgeräten oder in persönlichen Ablagen ohne Sicherungsnachweis | Vf | 2 | 3 | 6 | mittel |
| SR-05 | Ressourcenpläne führen personenbezogene Daten außerhalb eines geregelten Systems | V | 3 | 3 | 9 | hoch |
| SR-06 | Konfiguratoren und Ersatzteilmatrizen gehen mit internen Kalkulations- und Lieferantenangaben nach außen | V | 3 | 4 | 12 | sehr hoch |
| SR-07 | Berechnungstools enthalten Makros und fest hinterlegte Verbindungen zu Datenquellen | I, V | 2 | 4 | 8 | hoch, vorläufig |
| SR-08 | Stamm- und Termindaten werden manuell aus den führenden Systemen kopiert und laufen auseinander | I | 4 | 2 | 8 | hoch |
| SR-09 | Lieferterminlisten und Ersatzteilmatrizen stützen lieferkettenrelevante Entscheidungen ohne Ausweichverfahren | Vf | 2 | 3 | 6 | mittel |
| SR-10 | Die Meldung war freiwillig, das tatsächliche Mengengerüst ist unbekannt, die Auslandsstandorte sind nicht erfasst | V, I, Vf | 4 | 2 | 8 | hoch |
| SR-11 | Benannte Dateiverantwortliche ohne Zeitbudget bleiben ohne Wirkung | N | 3 | 2 | 6 | mittel |
| SR-12 | Nach Ende der Erhebung entstehen neue, nicht gemeldete Anwendungen | V, I, Vf | 3 | 3 | 9 | hoch |

## Register - Behandlung

| ID | Maßnahme | Verantwortung (Vorschlag) | Termin | Status |
|---|---|---|---|---|
| SR-01 | Verantwortlichen und Vertretung je Datei benennen, im Register führen | P-022 Faber mit den Fachbereichen | 30.04.2025 | offen |
| SR-02 | Die rund 60 Dateien auf gelenkte Ablagen überführen, Rechte nach POL-IT-001 v3.0 vergeben | P-022 Faber | 30.06.2025 | offen |
| SR-03 | Freigabestand, Versionskennzeichnung und Prüfvermerk für Konfiguratoren und Berechnungstools festlegen | P-031 Hoffmann, P-023 Bruckner | 30.06.2025 | in Abstimmung |
| SR-04 | Ablageorte erheben, lokale Ablagen ausschließen, Sicherung nachweisen | P-022 Faber | 30.04.2025 | offen |
| SR-05 | Ressourcenpläne auf personenbezogene Daten sichten, datenschutzrechtlich bewerten | P-075 Kroll, P-023 Bruckner | 31.03.2025 | offen |
| SR-06 | Klassifizierung und Freigaberegel für den Versand nach außen, getrennte Kunden- und Innenfassung | P-023 Bruckner, P-034 Ostermann | 30.06.2025 | offen |
| SR-07 | Zehn Berechnungstools technisch sichten: Makros, Verbindungen, hinterlegte Zugangsdaten | P-023 Bruckner, P-022 Faber | 31.03.2025 | offen, Voraussetzung der Bewertung |
| SR-08 | Führende Quelle je Datenobjekt festlegen, Abgleich mit POL-IT-006 | P-047 Bensch | 30.06.2025 | offen |
| SR-09 | Ausweichverfahren und Wiederherstellungszeit für die lieferkettenrelevanten Listen festlegen, in die NIS2-Vorbereitung einordnen | P-024 Damm, P-023 Bruckner | 30.06.2025 | offen |
| SR-10 | Zweite Melderunde in Eisenach sowie in Brno, Rotterdam, Houston und Shanghai | P-021 Nowak, P-036 Puhl | 30.04.2025 | offen |
| SR-11 | Zeitbudget der Dateiverantwortlichen mit den Bereichsleitungen klären | P-021 Nowak | 31.03.2025 | offen |
| SR-12 | Regelung für neu entstehende Anwendungen mit einem einfachen, meldefreundlichen Weg zur IT | P-023 Bruckner | 30.06.2025 | offen |

## Erläuterungen zu einzelnen Positionen

**SR-03.** Bei den Angebotskonfiguratoren wiegt das Fehlen eines freigegebenen Standes am schwersten.
Die technische Angebotsreview nach POL-VTR-001 v2.0 setzt voraus, dass die Kalkulationsgrundlage
nachvollziehbar ist. Wenn nicht feststellbar ist, welche Fassung eines Konfigurators ein Angebot
erzeugt hat und wer sie zuletzt geändert hat, prüft die Review eine Zahl ohne Herkunft. Mehrere
Meldungen nennen ausdrücklich, dass Kopien der Datei im Umlauf sind. Ich bewerte die Wahrscheinlichkeit
mit 4, weil abweichende Fassungen kein Störfall, sondern der beschriebene Normalzustand sind.

**SR-05.** Ressourcenpläne enthalten Namen, Zuordnungen und Auslastungsgrade. Für Systeme mit
personenbezogenen Daten besteht ein geregeltes Verfahren; eine Tabelle auf einem Netzlaufwerk ist im
Sinne dieses Verfahrens kein System, die Daten darin sind aber dieselben. Damit ist die Datei der
weniger regulierte Weg zu derselben Auswertung. Die Frage, ob sachbezogene Kennzahlen über die
Zuordnung zu einer Person personenbeziehbar werden, ist im November 2024 beim Projekt-Dashboard
aufgerufen worden und dort nicht abschließend geklärt. Ich halte die Klärung für vorrangig, weil sie
den Umgang mit allen weiteren Dateien dieser Kategorie bestimmt.

**SR-06.** Konfiguratoren und Ersatzteilmatrizen werden nach Angaben der Meldenden an Kunden und
Lieferanten weitergegeben. Sie enthalten dabei Zuschlagslogik, Stundensätze und die Zuordnung von
Komponenten zu einzelnen Lieferanten. Für Komponenten der Klasse S4 nach POL-SCM-003 ist genau diese
Zuordnung eine Information, die wir nach außen nicht geben wollen. Ein Klassifizierungsvermerk fehlt in
allen mir gemeldeten Fällen. Die Auswirkung bewerte ich mit 4, weil der Abfluss nicht rückholbar ist.

**SR-07.** Diese Bewertung ist vorläufig und beruht ausschließlich auf den Angaben der Meldenden, dass
Berechnungstools Makros und direkte Verbindungen zu Datenquellen enthalten. Fest hinterlegte
Zugangsdaten in solchen Verbindungen erwarte ich vor allem bei den älteren Werkzeugen aus dem Bestand
Eisenach; belegt ist das nicht. Ohne die Sichtung von zehn Dateien bis Ende März ist die Position nicht
belastbar, weder nach oben noch nach unten.

**SR-10.** Die Erhebung war freiwillig, sanktionsfrei und damit erfolgreich. Sie ist trotzdem kein
Inventar. Wer nicht gemeldet hat, ist unsichtbar geblieben, und aus den Standorten Brno, Rotterdam,
Houston und Shanghai liegt mir keine Meldung vor. Die rund 370 nicht als geschäftskritisch eingestuften
Dateien sind aus Sicht der Geschäftsprozesse zu Recht nachrangig; aus Sicht der Vertraulichkeit sind
sie nicht geprüft, weil auch dort personenbezogene und vertrauliche Inhalte liegen können.

**SR-11.** Der Gesamtbetriebsrat hat am 13.02.2025 gebeten, die Zuweisung von Dateiverantwortlichen
nicht als zusätzliche Verpflichtung ohne Zeitbudget auszugestalten. Der Hinweis deckt sich mit meiner
Einschätzung aus anderer Richtung: eine nominelle Verantwortung ohne Zeit erzeugt einen Eintrag im
Register und keine Wirkung im Betrieb. Die Maßnahmen zu SR-01, SR-02 und SR-04 hängen daran.

## Nicht bewertet

- Keine der gemeldeten Dateien ist bisher technisch geöffnet oder untersucht worden. Alle Bewertungen
  beruhen auf der Meldeliste und den Angaben der Meldenden.
- Die fachliche Richtigkeit der Berechnungstools ist nicht Gegenstand dieses Registers und liegt nicht
  in meiner Zuständigkeit.
- Die rund 370 nicht als geschäftskritisch eingestuften Dateien sind nicht bewertet.
- Für die Auslandsstandorte liegt keine Meldung vor, eine Aussage über deren Bestand ist nicht möglich.
- Ob Dateien mit Personalbezug aus dem Personalbereich betroffen sind, konnte ich nicht feststellen.

## Nächste Schritte

Bis 31.03.2025: technische Sichtung von zehn Berechnungstools (SR-07), datenschutzrechtliche Bewertung
der Ressourcenpläne (SR-05), Klärung des Zeitbudgets (SR-11).
Bis 30.04.2025: Verantwortliche und Vertretung benannt (SR-01), Ablageorte erhoben (SR-04), zweite
Melderunde angestoßen (SR-10).

Das Register wird monatlich fortgeschrieben, nächste Fassung am 20.03.2025. Positionen werden nicht
gelöscht, sondern auf erledigt gesetzt und mit dem Datum der Erledigung geführt. Änderungen an der
Bewertung werden mit Begründung vermerkt.
