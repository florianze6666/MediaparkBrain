---
doc_id: LTT-20250207-IT-02
titel: Excel Amnesty - Ergebnis der Erhebung
dokumenttyp: Management Summary
datum: 2025-02-07
verfasser: Andrea Faber
rolle: Leiterin IT-Applikationen
organisationseinheit: IT
empfaenger: "-"
projekt: Excel Amnesty
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [bereichsintern, projektintern, management]
ablageort: it_doku
---

# Management Summary: Excel Amnesty - Ergebnis der Erhebung

Von: Andrea Faber, Leiterin IT-Applikationen (IT)
Datum: 7. Februar 2025
Einstufung: intern
Bezug: Rundschreiben vom 26.01.2025, Aufruf zur sanktionsfreien Meldung geschäftskritischer Excel-Dateien

## Kurzfassung

Das Meldefenster ist geschlossen. Eingegangen sind 437 Meldungen, davon haben wir 58 Dateien als
geschäftskritisch eingestuft. Das ist mehr, als wir erwartet hatten, und es ist genau das Ergebnis,
für das die Erhebung gedacht war: Wir haben zum ersten Mal eine Liste statt einer Vermutung.

Meine Empfehlung: aus dieser Liste kein Ablöseprogramm machen. Für 2025 schlage ich vor, für die 58
kritischen Dateien Eigentümerschaft, Sicherung und Versionskontrolle herzustellen und die
Systemlücken zu dokumentieren, die hinter ihnen stehen. Ablösung ist die Folgefrage, nicht die
Sofortmaßnahme.

## Ausgangslage

Der Aufruf ging am 26.01.2025 an alle Beschäftigten in Kassel und Eisenach, mit der ausdrücklichen
Zusage, dass eine Meldung weder zur sofortigen Abschaltung noch zu einer Bewertung der meldenden
Person führt. Diese Zusage war die Voraussetzung dafür, dass überhaupt gemeldet wurde. Ich halte
sie für den eigentlichen Wert der Aktion und komme darauf unter Punkt 5 der Empfehlungen zurück.

## Ergebnis der Erhebung

- **437 gemeldete Dateien.** Sie lassen sich auf rund 300 unterschiedliche Werkzeuge zurückführen;
  der Rest sind Kopien, Jahres- und Projektstände desselben Tools auf verschiedenen Laufwerken.
- **58 davon geschäftskritisch.** Kriterium war eng gefasst: Ein Ausfall oder ein unbemerkter Fehler
  wirkt unmittelbar auf einen Termin, einen Preis oder eine Abnahme.
- **Gemeldete Kategorien:** Projektkalkulationen, Lieferterminlisten, Ressourcenpläne,
  Inbetriebnahmechecklisten, Ersatzteilmatrizen, Angebotskonfiguratoren, Berechnungstools.

Drei Beobachtungen halte ich für wichtiger als die Zahlen selbst.

**Erstens die Verteilung über den Projektverlauf.** Die kritischen Dateien häufen sich an den beiden
Enden: in der Angebotsphase und in der Inbetriebnahme. Das sind die Bereiche, in denen unsere
Systemunterstützung am dünnsten ist. In der Mitte, also dort, wo ERP und PLM greifen, wurde kaum
etwas gemeldet. Die Dateien stehen also nicht neben den Systemen, sondern dort, wo die Systeme
aufhören.

**Zweitens das Alter.** Ein Teil der Angebotskonfiguratoren und Berechnungstools ist älter als das
jeweilige Zielsystem, einige laufen seit vor 2018 unverändert. Sie haben zwei ERP-Landschaften und
den Wechsel des Programmzuschnitts überlebt, weil sie nie Gegenstand einer Entscheidung waren.

**Drittens die Eigentümerfrage.** Bei rund einem Drittel der 58 kritischen Dateien ist kein
Verantwortlicher benannt; in vier Fällen ist der Ersteller nicht mehr im Unternehmen. Mehrere Tools
enthalten Makros und feste Verknüpfungen auf Netzlaufwerkspfade, und in mindestens sechs Fällen
werden Daten manuell aus dem ERP exportiert und wieder eingelesen. Jeder dieser Medienbrüche ist
eine Stelle, an der ein Zahlenstand entstehen kann, den niemand mehr zuordnet.

## Bewertung

Die Zahl ist kein Befund über Disziplin. Sie ist das Ergebnis von fünfzehn Jahren pragmatischer
Problemlösung in einem Projektgeschäft, das sich schneller verändert hat als seine Systeme. Wer
darin ein Fehlverhalten der Fachbereiche sieht, wird die 58 Dateien nicht loswerden, sondern nur die
nächste Meldung.

Aus der Betreuung von ERP und PLM kenne ich den Ablauf seit 2018: Wir haben mehrfach lokale
Excel-Lösungen abgelöst und die meisten sind zurückgekommen. Nicht, weil die Anwender am Werkzeug
hingen, sondern weil die Funktion im Zielsystem fehlte oder mehr Aufwand kostete als die Datei.
Eine Datei abzuschalten, ohne ihre Funktion zu ersetzen, verlagert sie auf ein anderes Laufwerk und
kostet uns die Sichtbarkeit, die wir gerade erst gewonnen haben.

Gleichzeitig will ich die andere Seite nicht kleiner machen, als sie ist. Wir betreiben faktisch 58
Anwendungen, die wir weder kennen noch dokumentiert haben, für die aber IT-Applikationen gerufen
wird, sobald etwas nicht rechnet. Das ist Support ohne Zuständigkeit. Die Zugriffsrechte dieser
Dateien folgen den Berechtigungen der Netzlaufwerke und nicht dem Rollenkonzept nach POL-IT-001
v3.0; für die Anforderungen aus POL-IT-002 v3.0 und der NIS2-Vorbereitung sind geschäftskritische
Anwendungen ohne bekannten Eigentümer auf Dauer nicht vertretbar.

Ein Punkt braucht frühzeitig eine Abstimmung ausserhalb der IT: Die gemeldeten Ressourcenpläne
enthalten namensbezogene Auslastungs- und Verfügbarkeitsdaten, und zwar heute, in Dateien, die
keiner Betriebsvereinbarung unterliegen. Ordnung schafft hier Schutz und nicht Kontrolle. Die
Erfahrung mit dem Projekt-Dashboard im vergangenen Herbst zeigt aber, dass die Einordnung als Sach-
oder Personendatum nicht nebenbei getroffen wird. Ich schlage vor, den Gesamtbetriebsrat über die
Erhebung und ihr Vorgehen zu unterrichten, bevor wir Dateien in gelenkte Ablagen überführen, und die
Frage einer Teilvereinbarung nach BV-2023-01 offen anzusprechen, statt sie später erklären zu
müssen.

## Empfehlungen

1. **Keine Ablöseinitiative in diesem Jahr.** Die Business Units führen je drei
   Top-Priority-Change-Initiatives. Dieses Thema gehört in keine davon und würde als viertes alles
   Übrige verlangsamen. Es passt zur Parole des Jahres, dass wir hier zuerst stabilisieren.
2. **Eigentümerschaft bis Ende Q2.** Jede der 58 Dateien erhält einen benannten Dateiowner im
   Fachbereich und einen festen Ansprechpartner in IT-Applikationen. Ohne Owner keine Aufnahme in
   die weitere Bearbeitung; Dateien ohne Owner werden mit dem Bereichsleiter geklärt, nicht
   stillschweigend gestrichen.
3. **Risikoklassen statt Gesamtliste.** A: Ausfall stoppt einen laufenden Vorgang. B: Ausfall
   verzögert. C: bequem, kurzfristig ersetzbar. Nur die A-Fälle werden 2025 angefasst. Nach der
   ersten Durchsicht erwarte ich dort etwa zwanzig Dateien.
4. **Sicherung und Versionskontrolle als Betriebsaufgabe.** Die A-Dateien werden auf SharePoint mit
   Versionsverlauf, geregelten Zugriffsrechten und Wiederherstellungspunkt geführt. Das ist Betrieb
   und braucht kein Projekt; Aufwand in IT-Applikationen schätze ich auf rund 25 Personentage bis
   Ende Q2.
5. **Zusage einhalten.** Die Meldeliste ist bereits um die Namen der Meldenden bereinigt.
   Ausgewertet wird nach Funktion und Bereich, nicht nach Person und nicht nach Abteilung im
   Vergleich. Ich bitte darum, das auch dann so zu halten, wenn im Verlauf des Jahres nach
   Verantwortlichen für einzelne Dateien gefragt wird.
6. **Systemlücken dokumentieren.** Aus den A-Fällen entsteht bis Ende Q3 eine priorisierte
   Anforderungsliste an Digital Core und Engineering Backbone. Wer künftig eine Datei ablösen will,
   benennt zuerst die Funktion, die sie erfüllt.

## Offene Punkte

- Die übrigen rund 380 Dateien bleiben zunächst, wo sie sind. Das ist eine Entscheidung und keine
  Nachlässigkeit; wir wissen jetzt, dass es sie gibt.
- Gemeldet wurden ausserdem einzelne Access-Datenbanken, überwiegend in Eisenach. Sie sind in den
  437 nicht enthalten und werden getrennt betrachtet.
- Für die Angebotskonfiguratoren ist ungeklärt, wer fachlich über die hinterlegten Zuschläge und
  Kennwerte entscheidet. Das ist keine IT-Frage, blockiert aber jede weitere Bearbeitung.
