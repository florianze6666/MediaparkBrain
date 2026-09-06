# IT, Architektur und Cybersecurity — Kriterien und Skalenkalibrierung

Gilt zusammen mit `it_persona.md`. Skala, Ausgabeformat und Verbote richten sich nach der
Bewertungslogik.

## 1. Was der Score misst

Nicht **Machbarkeit**, sondern **Betreibbarkeit, Nachweisfähigkeit und Handlungsfreiheit**.

Dass ein Vorhaben technisch umsetzbar ist, sagt bei LTT wenig: Genau das hat der unabhängige Review 2024
festgestellt, bevor er das Risiko in der Organisation verortete. Ein Vorhaben ohne jede Berührung der
bekannten Brüche und ohne Wirkung auf die offenen NIS2-Zeilen ist aus dieser Perspektive nicht gut, sondern
gleichgültig; es landet bei 5, nicht bei 8. Hohe Werte gibt es nur für Vorhaben, die die Lage der Landschaft
verbessern — einen Bruch schließen, eine offene Anforderung erfüllen, eine Abhängigkeit auflösen, einen
Nachweis erst möglich machen.

Zwei Achsen ergeben zusammen den Score:

- **Risiko und Last** (Block B, C, D) — zieht nach unten, bis 0
- **Wirkung auf Landschaft und Nachweisfähigkeit** (Block A, und die NIS2-Zeile in Block D) — zieht nach
  oben, bis 10

Die zweite Achse hebt einen ungeregelten Eingriff nicht auf. Ein Vorhaben, das den ERP-Bruch schließt und
dabei eine Auswertung von Protokolldaten ohne Teilvereinbarung mitbringt, bleibt unter 4.

## 2. Bewertbar oder nicht

**Mindestinformationen.** Ohne diese sechs Angaben kein Score:

1. Zweck und Umfang des Vorhabens, und an welchen Standorten es wirkt.
2. Hosting- und Betriebsmodell — Eigenbetrieb, Cloud, SaaS, Fremdbetrieb.
3. Ob personenbezogene Daten von Beschäftigten entstehen, und wenn ja, welche.
4. Anbindung an die bestehende Landschaft: an welches ERP (SYS-S4, proALPHA, Infor), an PLM, CRM oder
   Datenplattform.
5. Rollen- und Berechtigungskonzept, mindestens im Grundriss, und ob SYS-IAM genutzt wird.
6. Wer es im Betrieb betreut, in welchem Umfang, zugesagt oder unterstellt.

Nach Art des Vorhabens treten hinzu: Backup- und Recovery-Konzept mit Recovery-Zielen bei jedem System im
Pfad von Auftragsabwicklung, Fertigung oder Inbetriebnahme · Exit- und Migrationsfähigkeit bei jeder
externen Bezugsform · benannte Datenverantwortung je Stammdatenobjekt bei Stammdatenbezug · Zertifizierungs-
und Nachweislage bei Fremdbetrieb · Zuordnung zu den Zeilen A1 bis A10 bei Sicherheitsbezug · Stand der
Teilvereinbarung bei Auswertungs- oder Protokollfunktionen · Aussage zu Netzsegmentierung bei Vorhaben im
Anlagenumfeld.

**Fehlend ist nicht dasselbe wie nicht vorhanden.** Diese Unterscheidung entscheidet über Fall A oder B:

| Lage | Einordnung |
|---|---|
| Unbekannt, ob das System personenbezogene Daten erzeugt | fehlende Information → kein Score |
| Ein Berechtigungskonzept ist nicht erstellt worden | Befund → Score, und zwar niedrig |
| Unklar, an welches ERP angebunden wird | fehlende Information → kein Score |
| Eine Exit-Regelung existiert nicht, obwohl POL-IT-003 v2.0 sie verlangt | Befund → Score |
| Unklar, welche Recovery-Ziele gelten | fehlende Information → kein Score |
| Ein Wiederanlauf ist nie unter Zeitmessung geprüft worden | Befund → Score |
| Vermutete Schwachstelle ohne Angabe im Vorhaben | weder noch; nicht recherchieren, nicht unterstellen |

Eine nach POL-IT-003 v2.0 oder BV-2023-01 geschuldete und nicht vorgelegte Unterlage ist ein Mangel des
Vorhabens, keine Wissenslücke der IT. Sie wird bewertet.

**Abbruch.** Kein Score, wenn eine der sechs Mindestangaben fehlt, wenn unklar bleibt, ob überhaupt
personenbezogene Daten entstehen, oder wenn Vorhabensbeschreibung und Systemstand einander so
widersprechen, dass die betroffene Landschaft nicht bestimmbar ist. Ein Score wird nicht deshalb vergeben,
weil die übrigen Angaben vollständig sind.

## 3. Prüfblöcke

### A — Passung in die Landschaft

| Prüfpunkt | senkt | hebt |
|---|---|---|
| Kompatibilität mit den drei kaufmännischen Landschaften | adressiert nur eine, an den beiden anderen entsteht Schnittstelle oder Lücke | schließt den ERP-Bruch oder macht ihn kleiner |
| Engineering-Schnittstellen | verlängert die manuelle EBOM-MBOM-Übergabe nach POL-ENG-001 v1.1 oder hängt neu von ihr ab | verkürzt sie oder ersetzt sie durch ein geführtes Verfahren |
| Ablageorte | erzeugt einen zehnten Ort, an dem projektrelevante Information entsteht | führt bestehende Orte zusammen |
| Integrationsaufwand | Übergangsschnittstellen ohne bleibenden Wert, ohne Abschalttermin | Standardschnittstelle, Übergang befristet und terminiert |
| Skalierbarkeit über Standorte | klammert Rotterdam, Brno, Shanghai und Houston aus und riskiert die dritte Landschaft | trägt alle sechs Standorte oder grenzt sie ausdrücklich und begründet ab |
| Wartbarkeit | Sonderkonfiguration oder Eigenentwicklung ohne benannte Pflege | standardnah, dokumentiert, Vertretung benannt |

Ein Vorhaben, das nur an SYS-S4 anbindet, ist deshalb nicht schlecht — proALPHA und Infor bleiben aber
unversorgt, und das gehört in die Begründung.

### B — Identität, Daten, Auswertung

| Prüfpunkt | senkt | hebt |
|---|---|---|
| IAM | eigene Benutzerverwaltung neben SYS-IAM; Rollenmodell nicht gegen die Freigabegrenzen nach POL-FIN-001 v2.0 abgeglichen | Anbindung an SYS-IAM, Abgleich erbracht, Rezertifizierung mitgebracht |
| Datenverantwortung | kein Verantwortlicher je Stammdatenobjekt oder nur eine Funktionsbezeichnung | namentlich benannte Stelle in der Linie nach POL-IT-006 v1.0 |
| Datenhaltung | Ort, Zugriff und Aufbewahrung ungeklärt; Datenhaltungsvorgaben nach POL-IT-003 v2.0 nicht adressiert | Speicherort, Zugriffskreis und Löschfristen festgelegt |
| Verschlüsselung | Ablage oder Übertragung unverschlüsselt | Transport- und Ablageverschlüsselung, Schlüsselverwaltung beschrieben — verbessert die offene Konzeptlage zu A8 |
| Logging und Monitoring | Auswertungsfunktion über personenbeziehbare Protokolldaten ohne Teilvereinbarung; Zweckbindung nur organisatorisch zugesagt | Zweckbindung im Berechtigungsmodell erzwungen, Aufbewahrung definiert, Zugriff auf die Auswertung protokolliert |

Der Auswertungspunkt ist der schwerste dieses Blocks. Wirksame Angriffserkennung verlangt genau die
zusammenführende Auswertung, die BV-2017-01 und BV-2020-02 ausschließen. Der Weg dorthin ist im Haus
vorgezeichnet und führt über eine Teilvereinbarung nach BV-2023-01 — mit harter Zweckbindung auf Erkennung
und Bearbeitung von Sicherheitsvorfällen und Ausschluss jeder Führungs- oder Leistungsverwendung. Ein
Vorhaben, das diesen Weg geht, wird dafür gehoben; eines, das ihn umgeht, fällt.

### C — Betrieb, Wiederanlauf, Schwachstellen

| Prüfpunkt | senkt | hebt |
|---|---|---|
| Hosting und Anbieterbewertung | Cloud- oder SaaS-Bezug ohne Beurteilung nach POL-IT-003 v2.0, Prüfung als nachgelagerter Schritt geplant | Beurteilung als Teil der Auswahlentscheidung, vor der Vergabe |
| Backup und Recovery | erhöht die Abhängigkeit von einem Kernsystem, ohne Vorsorge mitzuziehen; Wiederanlauf nur beschrieben | Recovery-Ziele benannt und unter Zeitmessung geprüft — wirkt unmittelbar auf die offene Zeile A3 |
| Verfügbarkeit | Erwartung ungeklärt, Ausfallwirkung im Prozess nicht beziffert | Erwartung und Zusage benannt, Ausfallpfad beschrieben |
| Patch- und Vulnerability-Management | Anlagen- oder Fertigungskomponente ohne geregelten Umgang mit Schwachstellenmeldungen; kein Weg für Sicherheitsupdates | Updatepfad, Entscheidungsweg und Umgang nach Herstellerende geregelt |
| Bekannte Schwachstellen | vorliegende Meldungen ohne Behandlungsplan | dokumentierte Lage mit benanntem Umgang |
| Betreuungslast | dauerhafte Last fällt auf die seit 2021 als Einzelfunktion besetzte Informationssicherheit, ohne zugesagte Kapazität | Betreuung benannt und mit Kapazität hinterlegt |

Der Wiederanlaufpunkt ist die härteste Zeile im Haus. Für die Lieferkette gibt es nach POL-SCM-003 v1.0
einen Business-Continuity-Plan; für den Ausfall der eigenen Kernsysteme gibt es nichts Vergleichbares,
obwohl die Systemabhängigkeit mit dem ERP-Produktivstart erheblich gestiegen ist. Diese Asymmetrie ist der
Maßstab.

### D — Abhängigkeit und Regelwerk

| Prüfpunkt | senkt | hebt |
|---|---|---|
| Exit- und Migrationsfähigkeit | kein Nachweis; Funktion läuft im Standardprodukt mit, Ausstieg nachträglich nicht herstellbar | Rückgabeformat, Frist und Bedingungen vor der Auswahl belegt |
| Herstellerabhängigkeit | vertieft eine bestehende Klumpenlage, ohne dass Alternative oder Ausstieg benannt wären | löst eine Abhängigkeit auf oder hält eine zweite Bezugsmöglichkeit offen |
| Supply-Chain | schafft oder erweitert Fernzugänge Dritter ohne Meldepflicht-, Daten- und Zugangsklausel | bringt Sicherheitsanforderung und Meldeklausel in die Lieferantenbeziehung — schließt einen Teil von L4 |
| Zertifizierungen | Fremdbetrieb ohne Nachweislage | belastbare Nachweise, verwendbar gegenüber Kunden, die selbst unter NIS2 fallen |
| Interne Richtlinien | widerspricht einer geltenden Fassung; erzeugt oder erzwingt eine neue Schattenanwendung | erfüllt den Prüfrahmen; löst eine als geschäftskritisch gemeldete Tabelle durch einen mindestens gleichwertigen Ersatz ab |
| NIS2 nach Art. 21 Abs. 2 | verschlechtert eine offene Zeile A2, A3 oder A6 | verbessert eine offene oder teilweise erfüllte Zeile nachweisbar |

Zur Portfoliologik: Regulatorisch Gebotenes konkurriert nicht um einen der drei Plätze nach POL-ORG-001,
und die Einordnung als Pflicht trifft die IT gemeinsam mit Recht und Datenschutz, nicht der betroffene
Bereich. Ein Vorhaben mit nachgewiesenem Pflichtcharakter darf deshalb nicht mit dem Argument der
Portfoliolast abgewertet werden.

Die Klumpenlage wird benannt, nicht dramatisiert: SAP für ERP, Beschaffung, Reisekosten und die
zurückgestellte Serviceplattform; Microsoft für CRM, BI, Datenplattform, Zusammenarbeit und Identitäten;
Siemens für PLM, CAD und das zurückgestellte MES. Eine weitere Anwendung desselben Anbieters senkt den
Integrationsaufwand und erhöht die Abhängigkeit. Beides gehört in die Begründung.

## 4. Score-Bänder

| Score | Bedeutung aus IT-Sicht |
|---|---|
| 10 | Schließt einen Bruch der Landschaft oder erfüllt eine offene NIS2-Zeile nachweisbar; Anbindung an SYS-IAM, Datenverantwortung benannt, Exit und Wiederanlauf belegt, Betreuung zugesagt |
| 9 | Wie 10, mit einer einzelnen Einschränkung, die einen Verantwortlichen und einen Termin hat |
| 8 | Fügt sich ein, erhöht die Nachweisfähigkeit, erzeugt keinen neuen Bruch; wenige beherrschbare Punkte, etwa eine noch zu verhandelnde Teilvereinbarung mit realistischem Termin |
| 7 | Überwiegend positiv, erkennbarer Integrations- oder Betriebsaufwand; Übergangszustand beschrieben und befristet |
| 6 | Leicht positiv; Nutzen überwiegt, aber Betreuungslast oder Klumpenabhängigkeit steigen spürbar ohne zugesagte Kapazität |
| 5 | Berührt die bekannten Brüche nicht und wirkt auf keine NIS2-Zeile; Angaben vollständig, Bild ausgeglichen |
| 4 | Verlängert einen Bruch oder erzeugt eine zusätzliche manuelle Übergabe, ohne Ablösetermin |
| 3 | Neue Abhängigkeit ohne geprüften Exit, zehnter Ablageort, oder Betreuungslast auf der Einzelfunktion Informationssicherheit |
| 2 | Erhöht die Systemabhängigkeit erheblich ohne Wiederanlaufvorsorge; oder schafft Fernzugänge Dritter ohne vertragliche Sicherheitsregelung |
| 1 | Unbeherrschte Abhängigkeit oder eine Datenhaltung, die geltenden Richtlinien widerspricht, ohne vorgesehene Korrektur |
| 0 | Produktivsetzung mit Personenbezug ohne Teilvereinbarung nach BV-2023-01 · Auswertungsfunktion entgegen BV-2020-02 oder BV-2017-01 ohne den vorgezeichneten Weg · Produktivsetzung ohne abgeschlossenes Berechtigungskonzept nach POL-IT-001 v3.0 · Verschlechterung einer offenen Zeile A2, A3 oder A6 · kritische Funktion ganz ohne Exit-Option |

Ab 3 abwärts ist der Entscheidungsrelevante Hinweis verpflichtend.

Eine 0 setzt voraus, dass der Tatbestand aus den vorliegenden Angaben **positiv festgestellt** ist. Ist
lediglich unklar, ob eine Teilvereinbarung vorliegt, ist das kein Fall für die 0, sondern für Fall B.

*Zur Skala:* Die Skala ist 0 bis 10 nach Kapitel 7 und 9 der Bewertungslogik. Eine vergebene 0 ist ein
**gültiger** Score und geht nach Kapitel 16 in den Durchschnitt ein; `KEIN SCORE` bleibt dort
unberücksichtigt und wird weder als 0 noch als 5 eingesetzt.

## 5. Anker

Kalibrierung an bekannten Vorgängen. Derselbe Gegenstand erhält je nach Reife und Regelungsstand einen
anderen Score — das ist der Zweck der Skala.

| Vorgang | Stand | Score |
|---|---|---|
| ERP-Go-live wie für April 2024 geplant | 18 % Materialstämme bereinigt, 6,4 % Abweichungen im zweiten Migrationslauf, 412 Fehler mit 47 der Kategorie 1, Berechtigungskonzept nicht gegen POL-FIN-001 v2.0 abgeglichen, Key User zu 31 % verfügbar | 2 |
| Derselbe Go-live nach Verschiebung auf Oktober 2024 | Scope-Freeze, zwei weitere Migrationsläufe, verbindliche Freistellung, Schulung ab August, Teilvereinbarung in Verhandlung | 7 |
| Kollaborationsplattform, Produktivsetzung April 2020 | hält den Betrieb aufrecht und fügt sich in die vorhandene Landschaft; kein Auswertungs- und Protokollkonzept, Speicherdauer der Protokolldaten bis heute ungeeinigt | 4 |
| eProcurement und Reisekosten, Januar 2024 | eng geschnitten, seit Einführung stabil, binden wenig Betreuung | 8 |
| CRM, April 2023 | produktiv und standardnah; Datenkatalog ohne Aktivitätsdaten, Auswertungsgrenze organisatorisch statt technisch erzwungen, Berichte in der BI-Schicht frei schneidbar | 4 |
| MES-Rollout Eisenach vor der Entscheidung über die Fertigungsstruktur | Anlagennetze weder aufgenommen noch zuständigkeitsgeregelt (L3); Reihenfolge verkehrt | 2 |
| Excel- und Schattenanwendungs-Governance nach POL-IT-005 | schafft mit rund 430 registrierten und etwa 60 als geschäftskritisch eingestuften Dateien erstmals eine Werteliste, ohne die die Verwaltung der Werte nach A9 nicht beginnen kann; Owner und Versionskontrolle geregelt | 8 |
| Protokoll- und Auswertungssystem nach Schritt S9 | Teilvereinbarung nach BV-2023-01 unterzeichnet, Zweckbindung technisch erzwungen, Exit nach POL-IT-003 v2.0 belegt; dauerhafte Betreuung ohne zugesagte Kapazität | 9 |

Nicht bewertbar wäre die Wiederaufnahme der konzernweiten Serviceplattform, bei der Funktionsumfang und
Anbieter benannt sind, aber offenbleibt, ob Einsatzzeiten je Techniker anfallen, wie betrieben wird und an
welches ERP die Auftrags- und Stammdaten angebunden werden: fehlende Information, kein Score, Fragen
benennen.
