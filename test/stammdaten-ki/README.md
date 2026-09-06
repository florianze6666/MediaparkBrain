# Testfall IP-2026-09: KI-gestützte Stammdaten-Standardisierung

**Stand:** 2026-09-06 · **Zweck:** zweites Projektobjekt in der Welt der Lahnberg Thermotechnik,
das alle vier Rollen bewerten können und das die vier Perspektiven auseinanderzieht. Anders als
der Eisenach-Fall, der nur die CFO-Spur anspricht, trägt dieser Antrag je Rolle eine eigene
Erinnerungsspur aus der Persona und je Rolle eine eigene Falle.

Ablage nur hier unter `test/stammdaten-ki/`. Nichts davon liegt in `project_proposals/`, wo die
Wiki-App liest.

| Datei | Inhalt |
|---|---|
| `ki-stammdaten-standardisierung-charter.md` | Projektsteckbrief nach dem Aufbau des Eisenach-Paars, alle fünfzehn Mindestangaben aus PLAN.md Abschnitt 2 als Überschriften |
| `ki-stammdaten-standardisierung-businesscase.md` | Investition, Zahlungsreihe, laufende Kosten, Nutzen, Wirtschaftlichkeit, Sensitivität, Alternativen, Finanzierung, Nutzenverantwortung, Ressourcen, Nachschau |
| `golden_dataset.json` | je Rolle Spur, Präzedenz, Falle, sieben Korpuspfade, Kern, Mindestzahl, Collections, erwartete Richtung |
| `kollisionspruefung.py` | prüft, dass Antrag und Golden-Dokumente kein seltenes Token teilen; Exit 1 bei Kollision |
| `stichprobe.json` | Ergebnis der vier Abfragen aus Abschnitt 4, mit Pfaden und Scores |

## 1. Der Antrag in einem Absatz

Eine SaaS-Plattform eines erfundenen Anbieters legt sich als Harmonisierungsschicht über die drei
kaufmännischen Systeme und das PLM: Klassenzuordnung, Dublettenerkennung, Golden-Record-Vorschläge
mit automatischer Freigabe ab einer Konfidenzschwelle, dazu ein Datenqualitäts-Cockpit mit
Kennzahlen je Bearbeiter. Investition 1,54 Mio EUR, Subskription volumenabhängig, Amortisation in
der Charter auf den Bruttonutzen gerechnet. Strategisch reizvoll, weil es den Engpass Engineering
entlastet und über alle Business Units wirkt; kaufmännisch fragwürdig, weil Nutzen und Deckung
nicht tragen; technisch mit offenen Vorbedingungen; für die Beschäftigten ein ungeregelter Eingriff.

Der Antrag ist aus den Personas und der Chronik entstanden, nicht aus Korpusdokumenten. Die
Korpusdokumente wurden erst danach gelesen, um das Golden Dataset zu wählen (Schranke A-2 der
Fit-Gap-Analyse). Alle Zahlen sind erfunden und in sich stimmig: 1.540.000 Investition,
385.000 je Jahr zahlungswirksam, 620.000 Fehlerkosten, 3.900 Stunden Produktivität.

## 2. Spur und Falle je Rolle

**Betriebsrat.** Spur: „Ob ein Pflichtfeld ausgefüllt ist, hängt an einer Person." Das Cockpit
führt Vollständigkeit, Durchlaufzeit und Rückstand je Bearbeiter mit Filter, Export und
unbegrenzter Historisierung, während der Antrag keine Mitbestimmungspflicht sieht und die
Team-Ebene nur organisatorisch zusichert. Präzedenz ist das Projekt-Dashboard vom November 2024
und die Teilvereinbarung über Leistungsdaten vom 19.08.2023, die Pflegestände ausdrücklich als
Leistungsdaten führt.

**CFO.** Spur: „Fortschreiben ist nicht schätzen, Vorausgesetztes ist nicht bepreist." Der
Antrag verneint die Vorlagepflicht wegen einer Investitionssumme unter 2 Mio EUR, obwohl nach
Abschnitt 3 der Investitionsrichtlinie das Gesamtvolumen über die Laufzeit zählt; Data Stewards
und Key User sind unterstellt, der Nutzen hat keinen Verantwortlichen, die Amortisation steht in
der Charter auf 20 Monate und zahlungswirksam auf 6,6 Jahre. Präzedenz ist die Programmvorlage von
2022 mit dem Befund des Audit Committee vom Mai 2024.

**IT.** Spur: „Die Stammdatenrichtlinie POL-IT-006 gilt seit April 2023 und regelt den
Pflegeprozess — nicht, wer im Zweifel entscheidet." Der Antrag bindet an „das führende
ERP-System" an, ohne bei drei Landschaften zu sagen, an welches, legt die Datenverantwortung
„im Projekt" fest und lässt die Plattform ab 95 Prozent Konfidenz in die Quellsysteme
zurückschreiben. Präzedenz ist das Master-Data-Projekt 2023 und die Architekturentscheidung zur
PLM-ERP-Kopplung vom November 2025, die den Start an die Datenverantwortung bindet.

**CEO.** Spur: „eine automatisierte Übergabe ohne geklärte Datenverantwortung nur eine
Uneinigkeit automatisiert". Die Plattform soll die Frage der Datenverantwortung regelbasiert
beantworten, der Antragsteller stuft das Vorhaben ohne Abstimmung als Querschnitt außerhalb von
POL-ORG-001 ein und benennt keine Initiative, die zurücktritt. Präzedenz ist der Neuschnitt vom
Juni 2024 mit der Vertagung des Engineering Backbone und das Portfolio 2025.

Die erwartete Richtung je Rolle steht nur als Status und Tendenz im Golden Dataset, ohne
Scorezahl. Der erwartete Ausgang für IT ist `INFORMATION FEHLT` (an welches ERP, Exit nach
POL-IT-003, Berechtigungskonzept); das ist gewollt, weil der Orchestrator damit die Regel
„KEIN SCORE ist nicht 0" aus Kapitel 16 zeigen kann.

## 3. Kollisionsprüfung

`python test/stammdaten-ki/kollisionspruefung.py` vergleicht ganze Wörter, Zahlen und Kennungen
des Antrags mit jedem der 25 Golden-Dokumente und meldet nur, was im gesamten Korpus in höchstens
drei Dokumenten steht. Ergebnis nach drei Umformulierungsrunden: **keine Kollision, Exit 0.**

Entfernt wurden unter anderem die Amortisation „1,6 Jahre" und danach „1,7 Jahre" (beide Werte
stehen in der Budgetübersicht vom Februar 2024, jetzt „rund 20 Monate"), die Position
„1,2 Mio EUR" (Programmbudget 2022, jetzt 1.250.000 EUR), „Stammdatenobjekt" (Audit-Committee-Bericht,
jetzt „Objektart"), „Bearbeiterkennungen" (Architekturentscheidung 2025, jetzt „Kennungen der
Bearbeiter"), „Implementierung", „Investitionsvolumen", „Vertragslaufzeit", „Reserve" und
„Release".

Fünf Begriffe stehen mit Begründung auf der Whitelist, alle aus der Investitionsrichtlinie
POL-FIN-002, deren Formblatt die Vorlage folgt: Nachschau, Nullvariante, Ressourcenbedarf,
Investitionsvolumens, Aufwandsanteil. Die Richtlinie ist Regelwerk, nicht Erinnerungsspur, und
der CFO findet sie ohnehin über ihre Kennung. Wer das strenger will, formuliert die Überschriften
9 und 10 des Business Case um und leert die Whitelist.

## 4. Stichprobe, kein Test

Je Rolle eine paraphrasierte Frage entlang der Spur, mit den Collections der Rolle und `-n 8`,
volle Kette mit Reranking. Ergebnis in `stichprobe.json`.

| Rolle | Golden unter 8 | Kern | Rang 1 | Anmerkung |
|---|---|---|---|---|
| Betriebsrat | 2 von 7 | 1 von 2 | das BR-Protokoll vom 01.12.2024, das die Spur wörtlich trägt | Reranker wegen VRAM übersprungen |
| CFO | 2 von 7 | 1 von 2 | der Audit-Committee-Bericht vom 16.05.2024 | Reranker wegen VRAM übersprungen |
| IT | 2 von 7 | 2 von 2 | die Architekturentscheidung zur PLM-ERP-Kopplung | Reranker lief |
| CEO | 3 von 7 | 1 von 2 | Lessons Learned Engineering 2025, die Neuschnitt-Vorlage auf Rang 3 | erster Versuch mit CUDA-Fehler im Reranker abgestürzt, zweiter lief |

Eine Frage je Rolle sagt nichts über die Mindestabdeckung von vier aus, die ein agentischer Lauf
mit mehreren Abfragen erreichen muss. Sie belegt nur, dass die Spur semantisch erreichbar ist:
in drei von vier Rollen liegt das Dokument, das die Persona-Erinnerung trägt, auf Rang 1. Der
Reranker-Absturz und der VRAM-Ausfall sind die bekannten Mängel M-1 aus
`.plans/.deprecated/07_qmd_maengel.md` und liegen nicht an diesem Testfall; während der Stichprobe
belegte eine andere Session 1,7 GB der GPU.

## 5. Stand der Personas

Die acht Zitate im Golden Dataset (je Rolle Spur und Nebenspur) sind gegen die Persona-Dateien
in diesem Stand geprüft und stehen dort wörtlich, Zeilenumbrüche ausgenommen:

| Datei | Stand |
|---|---|
| `persona/betriebsrats_persona.md` | 06.09.2026 05:51 |
| `persona/cfo_persona.md` | 05.09.2026 23:31 |
| `persona/it_persona.md` | 06.09.2026 05:51 |
| `persona/ceo_persona.md` | 05.09.2026 23:35 |

Betriebsrats- und IT-Persona wurden um 05:51 von einem parallelen Fork geändert, der die
Quellenangaben an das Rechtemodell angepasst hat. Die Spuren dieses Testfalls sind so gewählt,
dass ihr Kern in mindestens einem für die Rolle sichtbaren Korpusdokument steht: der BR-Satz
wörtlich im Protokoll vom 01.12.2024 in `br`, der CFO-Befund im Audit-Committee-Bericht in
`clevel`, die IT-Aussage zu POL-IT-006 in der IT-Zusammenfassung vom 04.06.2024 in `intern`, der
CEO-Satz in der Beiratsvorlage vom 11.06.2024 in `clevel`.

## 6. Was ein Mensch vor Gebrauch prüfen sollte

1. **Kalibrierung.** Die erwartete Richtung ist eine Annahme des Verfassers, keine Freigabe.
   Ob CFO und Betriebsrat tatsächlich im unteren Drittel landen sollen und der CEO im oberen,
   entscheidet der Mensch (Fit-Gap A-4).
2. **IT als `INFORMATION FEHLT`.** Wer für die Demo vier Scores will, ergänzt in der Charter das
   Zielsystem und einen Exit-Nachweis; dann kippt die IT-Erwartung auf „deutlich kritisch".
3. **Plausibilität der Zahlen.** Standardsatz 80 EUR je Stunde, 840.000 Datensätze, sechs Data
   Stewards, 95 Prozent Konfidenz: alles erfunden, in sich stimmig, aber von niemandem aus dem
   Fachbereich gegengelesen.
4. **Whitelist.** Die fünf Richtlinienbegriffe sind ein bewusster Bezug. Wer sie nicht will,
   formuliert um und lässt die Prüfung ohne Whitelist laufen.
5. **Reproduzierbarkeit.** Ein agentischer Lauf braucht nach NFR-03 drei Wiederholungen je Rolle;
   die Stichprobe hier ist eine einzelne Abfrage je Rolle und ersetzt das nicht.
6. **Übernahme nach `project_proposals/`.** Erst nach Freigabe, und dann mit denselben Regeln,
   die für das Eisenach-Paar gelten; die Wiki-App liest dort.

## 7. Neu erzeugen

```
python test/stammdaten-ki/kollisionspruefung.py                # Exit 0 erwartet
python test/stammdaten-ki/kollisionspruefung.py --zeige-haeufige # auch die unkritischen Treffer
```

Die Stichprobe läuft über `qmd query` mit den Umgebungsvariablen aus `qmd/env.ps1` und braucht
eine freie GPU; der Aufruf steht in `stichprobe.json` je Rolle unter `frage` und `collections`.
