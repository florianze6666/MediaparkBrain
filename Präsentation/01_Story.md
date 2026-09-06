# Die Story (Version 1)

## Ein Satz

Antje braucht sechs Wochen, bis fünf Fachbereiche einen Projektantrag bewertet haben, und trägt den
Vorstandsbericht von Hand zusammen. Wir haben ihr in einem Tag ein System gebaut, das das in Minuten
macht und dabei jedem nur das zeigt, was er sehen darf.

## Warum diese Story

Enterprise AI scheitert selten am Modell. Sie scheitert an drei Dingen: Wer darf was sehen? Ist das
Wissen überhaupt nutzbar? Und traut der Vorstand dem Ergebnis? Antjes Alltag macht alle drei sichtbar,
ohne dass wir etwas erklären müssen. Anselms Firmenbrain-Geschichte ist der Beleg, dass das Problem
nicht Antje-spezifisch ist: Jeder, der ein Brain baut, landet bei der Rechtefrage.

## Der Hook für dieses Publikum

Im Raum sitzen Teams, die heute Spiele, Augmented Reality und Vibe-Coding gezeigt haben. Wir sind der
Enterprise-Track. Das klingt nach dem langweiligsten Pitch des Tages, bis der erste Satz fällt:

> „Ihr habt heute Dinge gesehen, die Spaß machen. Wir zeigen euch etwas, das ein Konzern morgen
> einsetzen darf. Und warum das schwerer ist, als es aussieht."

Dann sofort Antje. Nicht als Persona, sondern als Mensch im Team, der das Problem jahrelang hatte.

## Leitstory: Antje Baumann, Portfolio-Managerin bei Metro

Antje sitzt im Team. Sie war drei Jahre Strategic IT Portfolio Manager bei METRONOM, der
IT-Tochter von Metro, davor bei Metrosystems, heute berät sie Unternehmen zu KI-PMO. Sie hat den
Prozess, den wir hier zeigen, nicht recherchiert, sondern gelebt. Das ist der Beleg, dass der Use Case
nicht ausgedacht ist: So werden Projektportfolios in Konzernen gesteuert, mit Millionenbudgets.

So sah ein Projektantrag bei ihr aus (Version 1 nach Antjes Schilderung, Version 2 nach dem
Interview mit ihren Worten und Zahlen):

1. Ein Bereich reicht einen Projektvorschlag ein: Charter, Business Case, Excel.
2. Antje prüft auf Vollständigkeit und trägt ihn in **die** Excel ein: vierzig Spalten, hundert Zeilen,
   eine Datei, die niemand außer ihr versteht.
3. Fünf Fachbereiche müssen Stellung nehmen: Controlling, IT, Datenschutz, Betriebsrat, Strategie.
   Jeder in seinem Tempo, jeder in seinem Format, jeder mit seinen Rückfragen.
4. Nach Wochen liegen fünf Stellungnahmen vor. Antje macht daraus ein Scoring.
5. Der Vorstand will wissen: Welches Projekt steht wo? Antje baut den Bericht. Von Hand. Jedes Quartal.

Öffentlicher Benchmark: Dauert die Prüfung vom Antrag bis zur Entscheidung länger als zehn
Arbeitstage, erzeugt der Prozess Reibung statt Steuerung. Bei Antje sind es Wochen.

**Der Schmerz in einem Satz:** Das Wissen für die Entscheidung ist da. Es liegt nur in fünf Köpfen,
zehn SharePoints und einer Excel, und keiner darf alles davon sehen.

## Nebenstory: Anselm und das Firmenbrain (ein Satz, nicht mehr)

Anselm hat für sein Unternehmen ein Brain gebaut: Wissen als Markdown, Skills, ein Assistent, der
alles kennt. Es funktionierte, bis die Frage kam: Darf der Assistent das Gehaltsdokument lesen, wenn
der Praktikant fragt? Kein Brain der Welt beantwortet das. Ein Rechtekonzept schon.

Das war der Punkt, an dem aus „Wissen sammeln" die Aufgabe „Wissen sicher verwertbar machen" wurde.
Genau diese Aufgabe hat das Team im Hackathon gelöst.

## Mission

Hackathon-Thema: **Enterprise AI**. Unsere Gruppe: ein **Wissensmanagement-System für KI**, das ein
Konzern wirklich einsetzen könnte. Drei Anforderungen, die „Enterprise" von „Demo" unterscheiden:

1. **Rechte und Berechtigungen:** Jeder sieht nur, was er darf. Auch die KI.
2. **Informationssicherheit über Zugriffsebenen:** Betriebsrat, Finance, Geschäftsführung getrennt.
3. **Wissen nützlich und externalisierbar:** Aus Dateien wird durchsuchbares, belegbares Wissen.

## Drei Wow-Momente (Reihenfolge im Pitch)

### Wow 1: Wissen hochladen, und es ist sofort richtig einsortiert

Ein CFO zieht ein Excel in das System. Zehn Sekunden später ist es eine Wissensseite: Titel,
Dokumenttyp, Verfasser, Klassifikation automatisch erkannt, Herkunftsbox mit Rolle und Zeit ganz oben,
physisch im Ordner `finance/`. Kein Formular, kein Abtippen.

**Screenshot:** `screenshots/01_upload.png`, `screenshots/02_seite_mit_herkunft.png`

### Wow 2: Dieselbe Frage, zwei Antworten

„Budgetfreigabe Q4: Wie hoch ist das Gesamtbudget für den KI-Wissensassistenten?" Der CFO bekommt 220.000 EUR mit wörtlichem Zitat als Beleg. Der
Mitarbeiter bekommt: „Dazu findet sich nichts." Nicht, weil die KI lügt, sondern weil sie das
Dokument nie gesehen hat. Der Filter sitzt **vor** dem Sprachmodell, nicht danach. Dann ein Klick im
Admin-Dashboard, und der Mitarbeiter sieht es. Sofort, protokolliert.

**Screenshot:** `screenshots/03_frage_cfo.png`, `screenshots/04_frage_mitarbeiter.png`,
`screenshots/05_admin.png`

### Wow 3: Vier Experten bewerten in dreißig Sekunden

Ein Projektantrag geht rein. Betriebsrat, CFO, IT-Security und CEO bewerten ihn: Score von 0 bis 10,
Begründung, oder „nicht bewertbar, es fehlt X". Und die Projektübersicht zeigt Antje alle Anträge mit
Status, Dokumenten und Einreicher. Das ist der Vorstandsbericht, den sie bisher von Hand baute.

**Screenshot:** `screenshots/06_bewertung.png`, `screenshots/07_projektuebersicht.png`

## Learnings (drei, nicht mehr)

1. **Rechte vor der Suche, nicht danach.** Was die KI nie sieht, kann sie nicht verraten. Das ist
   die einzige Architektur, die ein Sicherheitsbeauftragter unterschreibt.
2. **Der Ordner ist die Wahrheit.** Nicht der Dateikopf, nicht das Label. Was in `finance/` liegt,
   ist Finance. Einfach genug, dass es niemand umgehen kann.
3. **Ein Tag, acht Leute, ein Repo.** 38 User Stories, über 100 automatisierte Tests, 45 davon
   Sicherheitstests, jede Änderung per Pull Request mit Review. Das ist Enterprise-Arbeitsweise, nicht
   nur Enterprise-Software.

## Ablauf, 3 Minuten

| Zeit | Folie | Gesprochen (Kern) |
|------|-------|-------------------|
| 0:00 | Titel | „Das ist Antje." |
| 0:10 | Antjes Excel | „Ein Antrag. Fünf Fachbereiche. Sechs Wochen. Und am Ende ein Bericht von Hand." |
| 0:35 | Mission | „Enterprise AI. Wir wollten Wissensmanagement, das ein Konzern einsetzen darf." |
| 0:50 | Anselm-Satz | „Ich hatte ein Firmenbrain. Es scheiterte an einer Frage: Wer darf das sehen?" |
| 1:00 | Wow 1 | Upload, Herkunft, Ordner. |
| 1:30 | Wow 2 | Zwei Antworten. Admin-Klick. |
| 2:05 | Wow 3 | Vier Experten. Projektübersicht. |
| 2:35 | Learnings | Drei Sätze. |
| 2:50 | Schluss | „Von sechs Wochen auf sechs Minuten. Und Antje hat die Belege." |

## Zahlen, die auf Folien dürfen

| Zahl | Bedeutung | Quelle |
|------|-----------|--------|
| 6 Wochen → 6 Minuten | Antrag bis Bewertung. Bewusst drastisch; realistisch eher 6 Wochen → 2 Tage, weil Menschen die Ergebnisse noch lesen und entscheiden müssen. Für V1 so lassen, in V2 mit Antje festlegen | Antjes Schilderung |
| 10 Arbeitstage | Benchmark: darüber ist ein PMO-Prozess Reibung | öffentliche PMO-Quelle |
| 4 | Experten-Rollen, die jeden Antrag bewerten | PLAN.md |
| 9 | getrennte Ablageorte, wie im Konzern | Korpus |
| 216 | Dokumente im Demo-Korpus einer fiktiven Firma | docs/FUNKTIONSWEISE.md |
| 38 / 100+ / 45 | User Stories / Tests / Sicherheitstests | docs/USER-STORIES.md |
| 8 / 2 Tage / 39 PRs | Team / Zeit / Pull Requests | GitHub |

## Offene Punkte für Version 2 (nach Antjes Interview)

- Echte Dauer und Beteiligte in Antjes Prozess, ihre Worte für den Schmerz.
- Ein konkretes Projekt als Beispiel, anonymisiert.
- Was der Vorstand wirklich sehen will.
- Ihr Satz, den sie sagen würde, wenn das System morgen liefe.
