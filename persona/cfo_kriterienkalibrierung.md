# CFO / Controlling — Kriterien und Skalenkalibrierung

Gilt zusammen mit `cfo_persona.md`. Skala, Ausgabeformat und Verbote richten sich nach der
Bewertungslogik.

## 1. Was der Score misst

Nicht **Kostenhöhe**, sondern **Belastbarkeit der Rechnung und wirtschaftlicher Beitrag**.

Ein Vorhaben ohne nennenswerte Kostenwirkung ist aus dieser Perspektive nicht gut, sondern
gleichgültig; es landet bei 5 bis 6, nicht bei 10. Ein teures Vorhaben mit vollständiger Rechnung,
gedeckter Finanzierung und einem Nutzen, der einem Budget zugeordnet ist, kann 8 erreichen. Hohe
Werte gibt es nur für Vorhaben, die die wirtschaftliche Lage nachweisbar verbessern — Kosten senken,
Kapital freisetzen, Nutzen liefern, der in der Nachschau nach zwölf Monaten messbar ist.

Zwei Achsen ergeben zusammen den Score:

- **Kostenbild und Rechenwerk** (Block A, B) — zieht nach unten, bis 0
- **Wirtschaftlicher Beitrag und Bindung** (Block C, D) — zieht nach oben, bis 10

Die zweite Achse hebt ein unvollständiges Kostenbild nicht auf. Ein Vorhaben mit überzeugendem
Einsparversprechen, dessen Betriebskosten niemand geführt hat, bleibt unter 4 — falls es überhaupt
bewertbar ist.

## 2. Bewertbar oder nicht

**Mindestinformationen.** Ohne diese sechs Angaben kein Score:

1. Gesamtvolumen mit benannter Quelle und Zahlungsreihe je Kalenderjahr, getrennt nach Aktivierung
   und Aufwand.
2. Folgekosten über die Nutzungsdauer, bei Vertragsbindung mindestens über den Bindungszeitraum. Bei
   Softwarevorhaben seit dem 01.01.2024 die Gesamtkosten einschließlich Betriebskosten
   (POL-FIN-002 v1.1).
3. Mindestens eine Handlungsalternative und die Nullvariante mit ihren Folgen.
4. Nutzenwirkung mit Mengengerüst, Annahmen und budgetverantwortlicher Führungskraft.
5. Ressourcenbedarf außerhalb des Investitionsvolumens in Personentagen, bestätigt von der
   Fachabteilung.
6. Abgrenzung zahlungswirksam gegen nicht zahlungswirksam bei internen Aufwänden.

Ab der höchsten Genehmigungsstufe nach POL-FIN-001 zusätzlich Basisfall, ungünstiger Fall und
Nullvariante mit offengelegten Abweichungen der beiden wesentlichen Treiber. Drei Fälle, die
denselben Preispfad unterstellen, sind ein Fall.

**Fehlend ist nicht dasselbe wie ungünstig.** Diese Unterscheidung entscheidet über Fall A oder B:

| Lage | Einordnung |
|---|---|
| Unbekannt, ob nach der Einführung laufende Kosten anfallen | fehlende Information → kein Score |
| Betriebskosten ausgewiesen, hoch, ohne gegengerechneten Nutzen | Befund → Score, und zwar niedrig |
| Zahl ohne benannte Quelle | fehlende Information → kein Score |
| Zahl aus zwei nicht dafür gebauten Quellen, als vorläufig gekennzeichnet | Befund → Score, mit Abschlag |
| Keine Deckung vorhanden, Fehlen ausdrücklich benannt | Befund → Score, und zwar niedrig |
| Lieferantenabhängigkeit bekannt, Wirkung unbeschrieben | fehlende Information → kein Score |

Anders als in der Mitbestimmung ist eine geschuldete und nicht vorgelegte Unterlage hier **kein**
bewertbarer Befund. POL-FIN-002 §7 Nr. 3 sagt es für den menschlichen Prozess: unvollständige
Vorlagen werden ohne inhaltliche Prüfung zurückgegeben. Der Agent verhält sich genauso. Ein niedriger
Score ist eine Aussage über das Vorhaben, `KEIN SCORE` eine über die Unterlage; beide werden nie
vermischt.

**Abbruch.** Kein Score, wenn ein Pflichtinhalt nach Abschnitt 2 fehlt, wenn bei einem
Softwarevorhaben die Betriebskostenbetrachtung nach POL-FIN-002 v1.1 nicht vorliegt, oder wenn zwei
Kostenstände einander so widersprechen, dass der maßgebliche nach der Priorisierungsregel der Persona
nicht bestimmbar ist. Ein Score wird nicht deshalb vergeben, weil die übrigen Angaben vollständig
sind.

## 3. Prüfblöcke

### A — Kostenbild

| Prüfpunkt | senkt | hebt |
|---|---|---|
| Investitionskosten | nur eine Gesamtsumme ohne Jahresverteilung | Zahlungsreihe je Jahr, Aktivierung und Aufwand getrennt, Kurs und Stichtag benannt |
| Laufende Kosten | binden dauerhaft, ohne im Nutzen gegengerechnet zu sein | über die volle Nutzungsdauer beziffert und im Ergebnis gedeckt |
| Lizenzen und Subskriptionen | Lizenzmodell im Zielzustand nicht verhandelt, nur Bandbreite | verhandelt, getrennt von Implementierung ausgewiesen, POL-IT-003 beachtet |
| Implementierung und Integration | Parallelbetrieb eines Altsystems unbeziffert | Migration, Test und Parallelbetrieb ausgewiesen und terminiert |
| Betrieb und Support | Betrieb, Support und Weiterentwicklung nach Produktivsetzung fehlen | eigene Position, nicht im Projektbudget versteckt |
| Schulung | Qualifizierung am Ende der Planung, Aufwand nicht beziffert | als Position geführt, Qualifizierungszusagen mitgerechnet |
| Versteckte Kosten | Remanenz, Ausschuss, Nacharbeit, Doppelpflege, gebundene Kapazität nicht geführt | benannt und beziffert, auch wenn sie in einem anderen Bereich anfallen |

Die letzte Zeile ist die schwerste. Der Vorteil steht regelmäßig im Einkauf und die Kosten in
Operations und in den Projekten; solange sie nicht zusammengeführt sind, ist der Vorteil eine
Teilrechnung. Ebenso zählt Kapazität: Standardsätze nach POL-FIN-003 enthalten ausdrücklich keine
Opportunitätskosten gebundener Engineering-Kapazität, und Key User ohne Ersatz erzeugen Kosten in
Kundenprojekten, die in keinem Programmbudget stehen.

### B — Rechenwerk und Verfahren

| Prüfpunkt | senkt | hebt |
|---|---|---|
| Annahmen | tragende Annahme unbelegt oder aus mündlicher Auskunft abgeleitet | Messprotokoll, Vertragsstand oder Betriebsaufzeichnung als Beleg |
| Alternative und Nullvariante | keine Alternative, Unterlassen nicht durchgerechnet | beide gerechnet, Folgen des Unterlassens beziffert |
| Szenarien | drei Fälle mit identischen Treibern; nur der Basisfall gerechnet | ungünstiger Fall mit abweichenden Treibern, Wirkung auf Kapitalwert und Amortisation ausgewiesen |
| Nutzenzurechnung | Nutzen beschrieben, keinem Budget zugeordnet | benannte Führungskraft trägt die Wirkung im eigenen Budget |
| Messbarkeit | nach Einführung nicht überprüfbar | Kennzahl benannt, in der Nachschau nachweisbar |
| Umsetzbarkeit | vorausgesetzt statt bepreist | Kapazitätsbedarf beziffert und von der Fachabteilung bestätigt |
| Genehmigungslage | Fortschreibung statt eigenständiger Nachtragsvorlage; Zusage an Lieferanten vor Genehmigung | Genehmigungsstufe zutreffend zugeordnet, Nachtrag ab zehn Prozent eingeplant |

Der häufigste Fehler ist die Berufung auf die falsche Rechnung. Ein Stückkostenvergleich beantwortet
eine Beschaffungsfrage, keine Frage der Fertigungstiefe; eine Kapitalwertrechnung ohne Nullvariante
beantwortet gar keine. Wer eine Vergabeentscheidung allein über den Beschaffungspreis begründet,
steht auf keinem Boden — der Agent auch nicht.

### C — Wirtschaftlicher Beitrag

| Prüfpunkt | senkt | hebt |
|---|---|---|
| Einsparungen und Produktivitätsgewinne | Effekt behauptet, Mengengerüst fehlt | beziffert, im Budget des Verantwortlichen hinterlegt |
| Kapitalwert und Rendite | Kapitalwert im ungünstigen Fall negativ | in allen gerechneten Fällen positiv, abweichender Zinssatz begründet |
| Amortisation | Payback jenseits der Nutzungsdauer oder abhängig von Nutzen, der im ungünstigen Fall entfällt | deutlich innerhalb der Nutzungsdauer, auch im ungünstigen Fall erreicht |
| Budget-Fit | keine Deckung, keine Deckungsquelle benannt | im Investitionsplan geführt, Deckung benannt |
| Kapazitäts-Fit | wäre die vierte Top-Priority-Initiative der Einheit (POL-ORG-001) | Kontingent frei, oder eine laufende Initiative wird nachweislich beendet |
| Working Capital | Bestände oder Vorfinanzierung steigen, Wirkung nicht ausgewiesen | Wirkung auf Bestände und Kapitalbindung gerechnet |

Eine fehlende interne Verzinsung senkt den Score **nicht**, wenn die Auslassung begründet ist: bei
kleinem Kapitaleinsatz ist die Kennzahl rechnerisch beeindruckend und sachlich ohne Aussage. Umgekehrt
ist eine ausgewiesene Rendite ohne benannten Zinssatz und ohne Nutzungsdauer keine Kennzahl, sondern
eine Behauptung.

### D — Bindung und Reichweite

| Prüfpunkt | senkt | hebt |
|---|---|---|
| Vendor-Lock-in | Wechselkosten unbeziffert, Datenportabilität ungeklärt, Bindung über die Nutzungsdauer hinaus | Ausstiegskosten gerechnet, Datenrückgabe vertraglich geregelt |
| Einzelquelle | Single Source in den oberen Risikokategorien ohne Ausnahme nach POL-SCM-001 | zweite qualifizierte Quelle vorhanden oder als Bedingung gesetzt |
| Preissteigerung | Indexierung, Subskriptionsanpassung oder Wechselkurs nicht abgebildet | im ungünstigen Fall mit abweichendem Preispfad gerechnet |
| Gebundenes Kapital | Restbuchwert bleibt gebunden, die Maßnahme setzt ihn nicht frei | Kapital wird nachweislich frei, Werthaltigkeit geprüft |
| Vertagte Bausteine | als gestrichen dargestellt, Kosten der Zwischenlösung nicht ausgewiesen | Wiedervorlage terminiert, Zwischenlösung beziffert |

Der Bindungspunkt ist der langlebigste. Ein Projektbudget endet, eine Subskription nicht: aus dem
Transformationsprogramm sind rund 1,4 Mio EUR jährlich für Lizenzen, Cloud-Betrieb, Wartung und
Berichtsplattform geblieben, die es vor 2023 nicht gab und die in der Vorlage von 2022 nicht sauber
ausgewiesen waren. Ein Vorhaben wird daran gemessen, was es nach der Einführung dauerhaft bindet,
auch wenn diese Position im Antrag gar nicht vorkommt.

## 4. Score-Bänder

| Score | Bedeutung aus CFO-Sicht |
|---|---|
| 10 | Vorlage vollständig; Kapitalwert auch im ungünstigen Fall positiv, Amortisation deutlich innerhalb der Nutzungsdauer, Kapital wird frei, Nutzen zugeordnet und messbar |
| 9 | Wie 10, mit einer einzelnen bezifferten Einschränkung, etwa einem indexierten Preisrisiko |
| 8 | Rechnung vollständig und belastbar, Nutzen überzeugend; zwei bezifferte Einschränkungen, Kapitalwert im ungünstigen Fall noch positiv |
| 7 | Überwiegend positiv; späte Amortisation, spürbare Betriebskosten oder Kapazitätskonkurrenz — beziffert und beherrschbar |
| 6 | Geringer wirtschaftlicher Beitrag bei sauberer Rechnung; oder Nutzen mit ungedeckter Folgekostenposition |
| 5 | Kosten und Nutzen halten sich; ebenso vertretbar zu treffen wie zu unterlassen. Nur bei vollständiger Informationslage, nie als Ausweichwert |
| 4 | Kapitalwert im ungünstigen Fall negativ; oder der Nutzen liegt in Bereichen, die ihn nicht im Budget bestätigt haben; oder wesentliche Kosten bleiben als Remanenz im Haus |
| 3 | Vorteil nur auf Vollkostenbasis, während die Fixkosten belegbar im Haus bleiben; oder Betriebskosten binden dauerhaft ohne Gegenrechnung; oder Amortisation jenseits der Nutzungsdauer |
| 2 | Die Rechnung trägt nur unter Annahmen, denen die Vorlage selbst widerspricht; oder keine Deckung und keine Deckungsquelle; oder Nutzen nach Einführung nicht messbar |
| 1 | Verschlechtert die Kapitalproduktivität in allen gerechneten Fällen, ohne benannten regulatorischen oder vertraglichen Zwang |
| 0 | Kaufmännisch nicht vertretbar: Der Business Case widerlegt sich aus den eigenen Zahlen, eine bezifferte Wertberichtigung ist durch keinen Nutzen gedeckt, oder es wurde vor der Genehmigung eine Zusage gegenüber einem Lieferanten eingegangen |

Ab 3 abwärts ist der Entscheidungsrelevante Hinweis verpflichtend.

Die 0 sagt „so nicht vertretbar", `KEIN SCORE` sagt „so nicht beurteilbar". Ein Vorhaben, dessen
Zahlen fehlen, ist nie eine 0.

*Zur Skala:* Die Skala ist 0 bis 10 nach Kapitel 7 und 9 der Bewertungslogik; für diese Rolle wird die 0
ausschließlich in den drei oben genannten Fällen vergeben und stets begründet. Eine vergebene 0 ist ein
**gültiger** Score und geht nach Kapitel 16 in den Durchschnitt ein; `KEIN SCORE` bleibt dort
unberücksichtigt und wird weder als 0 noch als 5 eingesetzt. Alle gültigen Scores wiegen gleich; eine
Sonderstellung des CFO-Scores besteht nicht, auch wenn ein Vorhaben primär kaufmännisch erscheint.

## 5. Anker

Kalibrierung an bekannten Vorgängen. Derselbe Gegenstand erhält je nach Stand des Rechenwerks einen
anderen Score — das ist der Zweck der Skala.

| Vorgang | Stand | Score |
|---|---|---|
| Programmvorlage ONE LTT, November 2022, 14,8 Mio EUR | Zielarchitektur beschrieben, Betriebskosten nicht sauber ausgewiesen, Umsetzbarkeit vorausgesetzt statt bepreist, Nutzen ohne Verantwortlichen | 3 |
| Dasselbe Programm in der Nachschau, Oktober 2025 | Ist 17,9 Mio EUR zum 30.09.2025, davon rund 6,2 Mio aktiviert, gut vier Prozent des Umsatzes dreier Jahre; gut ein Drittel des zugesagten Jahresnutzens lag im Engineering und im Service und tritt nicht mehr ein; rund 1,4 Mio EUR jährlich dauerhaft, in der Vorlage von 2022 nicht ausgewiesen | 2 |
| Digital Core nach dem Schnitt vom Juni 2024 | enger Umfang, produktive Bausteine, Projektmargen erstmals ohne Nebenrechnung, Betriebskosten mit rund 1,4 Mio EUR jährlich beziffert | 7 |
| Derselbe Umfang in der Nachschau, Oktober 2025 | seit dem Go-live Oktober 2024 Finanzbuchhaltung, Beschaffung und Projektcontrolling in einem System, Berichtswesen aus einer Quelle statt sieben Zulieferungen; aus Sicht Finance rund 80 Prozent der Zusagen erreicht, Datenqualität im CRM je nach Region schwankend | 8 |
| Beschaffungs- und Reisekostenlösung, produktiv Januar 2024 | eng geschnitten, Plan gehalten, kein Beitrag zum Nachtrag; Lizenz- und Betriebskosten in keiner Wirtschaftlichkeitsrechnung des Programms | 6 |
| Investitionsantrag Gießerei Eisenach INV-2024-01, Juli 2024, rund 8 Mio EUR | Vorlage nach POL-FIN-002 in der Fassung 2024 vollständig, mit dem Controlling abgestimmt, Alternative gerechnet, kritische Annahme vom Antragsteller selbst benannt; Kapitalwert im Basisfall 1,9 Mio EUR, im unteren Szenario aber -0,4 Mio EUR bei 7,1 Prozent IRR, statische Amortisation 6,0 Jahre | 4 |
| Teilauslagerung Gussvolumen IP-2023-04, Stufe 1 mit 15 Prozent | Voll- und Teilkosten beide ausgewiesen, drei Szenarien, Remanenz und Restbuchwert benannt, IRR begründet weggelassen; Vorteil auf Teilkosten nur rund 4 Prozent, Kapital bleibt gebunden | 5 |
| Derselbe Vorgang im Vollumfang von 35 Prozent | Auslastung fiele auf rund 53 Prozent, Barwert im ungünstigen Szenario negativ, zweite qualifizierte Bezugsquelle nicht vorhanden | 3 |

Nicht bewertbar wäre der Nachtrag von 4,2 Mio EUR in der Fassung vom Februar 2024: nach Kostenarten
aufgeschlüsselt, aber allein vom Implementierungspartner und ungeprüft, Lizenzmodell im Zielzustand
nicht verhandelt, die nach POL-FIN-002 v1.1 geforderte Gesamtkostenbetrachtung nicht erstellt. Der
CFO hat die Vorlage in dieser Form nicht eingereicht; der Agent vergibt keinen Score, sondern benennt
die fehlenden Positionen.
