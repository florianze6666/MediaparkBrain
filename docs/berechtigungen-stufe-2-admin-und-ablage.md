# Paket 8: Erweitertes Berechtigungsmanagement (Stufe 2)

Verantwortlich: Anselm · Stand: 2026-09-05 · Baut auf `docs/berechtigungen-und-herkunft.md` (Stufe 1) auf

## Kurzfassung

Stufe 1 hat Metadaten, Rollen und die Entscheidungsregel `decide` ins Wiki gebracht. Stufe 2 zieht
das durch das ganze System:

1. **Herkunft ist Hauptinformation.** Jedes Wissensdokument und jeder eingereichte Projektvorschlag
   zeigt an erster Stelle, wer ihn eingebracht hat und in welcher Rolle. Vorschläge bekommen dieselben
   Metadaten und dieselbe Rechteprüfung wie Wiki-Seiten.
2. **Admin-Dashboard.** Nutzer, Gruppen und Domänenrechte werden in der Oberfläche gepflegt, nicht
   mehr nur in der Datei. Jede Änderung wird protokolliert.
3. **Getrennte Ablage.** Wiki-Dateien liegen physisch nach Domäne und Vertraulichkeit getrennt. Der
   Ordner ist die Wahrheit: Was in `pages/finance/` liegt, ist Finance, egal was im Dateikopf steht.
   Die Suche für den Agenten öffnet nur die Ordner, die der Nutzer lesen darf.

## User Stories

| Nr | Als … | möchte ich … | damit … | Fertig wenn |
|----|-------|--------------|---------|-------------|
| US-10 | Leser | auf jedem Dokument und jedem Vorschlag ganz oben eine Herkunftsbox sehen: Name, Rolle, Datum, Domäne, Vertraulichkeit | Herkunft nicht Kleingedrucktes ist, sondern das Erste, was ich lese | Herkunftsbox steht über dem Inhalt, auf Wiki-Seite, Vorschlagsseite und in der Vorschlagsliste |
| US-11 | Einreicher | dass mein Projektvorschlag automatisch meinen Nutzer und meine Rolle trägt | jeder weiß, wer den Vorschlag verantwortet | Vorschlag speichert `eingereicht_von` und `rolle` (Anzeigename zum Zeitpunkt der Einreichung) |
| US-12 | Leser | dass Vorschläge denselben Rechten unterliegen wie Wiki-Seiten | ein Finance-Vorschlag nicht von jedem gelesen oder gelöscht werden kann | Liste gefiltert, verbotener Vorschlag 404, Gast kann nicht einreichen (403) |
| US-13 | Admin | eine Seite, auf der ich Nutzer anlegen, ihre Gruppen ändern und Nutzer entfernen kann | ich Rechte vergeben kann, ohne die Datei zu editieren | Änderung greift sofort, ohne Neustart |
| US-14 | Admin | Domänen und ihre Lesegruppen pflegen und neue Gruppen anlegen | neue Ablageorte (Paket 7) ohne Code angebunden werden | Neue Domäne erscheint im Editor und bekommt einen Ordner |
| US-15 | Admin | dass jede Rechteänderung mit Zeit, Admin und Änderung protokolliert wird | Rechtevergabe nachvollziehbar ist | Eintrag in `permissions-changelog.md`, sichtbar im Admin-Dashboard |
| US-16 | Nicht-Admin | dass das Admin-Dashboard für mich nicht existiert | ich nicht einmal weiß, dass es da ist | `/admin` liefert 404 für alle ohne Gruppe `admin`; Link nur für Admins sichtbar |
| US-17 | Autor | dass meine Seite physisch im Ordner ihrer Domäne liegt, vertrauliche Seiten in einem Unterordner | Dateien verschiedener Rechte sich nicht stören und man im Dateisystem sieht, was wohin gehört | `pages/<domaene>/<slug>.md` bzw. `pages/<domaene>/vertraulich/<slug>.md`; Domänenwechsel im Editor verschiebt die Datei |
| US-18 | Fragender | dass der Agent nur Ordner öffnet, die ich lesen darf | selbst eine falsch beschriftete Datei in einem fremden Ordner nie in meinen Kontext gelangt | Test: Datei ohne Kopf in `pages/finance/` wird für Mitarbeiter nicht gefunden, für CFO schon |
| US-19 | Betreiber | dass vorhandene flache Dateien beim Start automatisch einsortiert werden | der Umbau ohne Handarbeit läuft | Idempotente Migration: Altbestand ohne Kopf landet in `pages/allgemein/` |

## Datenmodell

### Ablage der Wiki-Seiten

```
llm-wiki/pages/
  allgemein/            start.md, vier-experten-agenten.md, …
  projekt/
  finance/              budgetfreigabe-q4.md
  finance/vertraulich/  …
  br/                   betriebsratsprotokoll-juli.md
  …
```

- Der **Ordner bestimmt die Domäne** und ob eine Seite vertraulich ist. Weicht der Dateikopf ab,
  gilt der Ordner, und der Kopf wird beim nächsten Speichern korrigiert.
- Slugs sind **global eindeutig** (URL bleibt `/wiki/<slug>`). `get_page(slug)` sucht über alle
  Ordner. Beim Anlegen wird ein Slug abgelehnt, der in einem anderen Ordner existiert.
- `save_page` legt die Datei in den Zielordner; wechselt Domäne oder Vertraulichkeit, wird die Datei
  verschoben (alte gelöscht).
- **Migration beim Start** (`wiki.migrate_flat_pages()`): jede `pages/*.md` auf oberster Ebene wird
  anhand ihres Kopfes einsortiert, ohne Kopf nach `allgemein/`. Läuft bei jedem Start, ist idempotent.
- `list_pages(user)` liest **nur Ordner**, deren Domäne der Nutzer lesen darf, und wendet danach
  `decide` pro Seite an (Vertraulichkeit, Empfänger). `search_snippets(query, user)` nutzt genau diese
  Liste. Zwei Schranken, dieselbe Regel.

### Metadaten für Projektvorschläge (Frontmatter in `project_proposals/<slug>.md`)

```yaml
---
eingereicht_von: projektmanager     # Nutzer-ID
rolle: Projektmanager (Einreicher)  # Anzeigename zum Zeitpunkt der Einreichung (Snapshot)
eingereicht_am: 2026-09-05T20:10:00
vertraulichkeit: intern
domaene: projekt                    # Standard für Vorschläge
empfaenger: []
---
# Projektname

Eingereicht am: …
## Beschreibung
…
```

- Vorschläge bleiben in `project_proposals/` (Marc liest sie dort für die Bewertung). Der Kopf steht
  vor dem bisherigen Format, der bisherige Parser überspringt ihn.
- Altbestand ohne Kopf: `eingereicht_von: unbekannt`, `domaene: projekt`, `intern`.
- Rechte: `access.decide(user, meta)` mit denselben Feldern wie bei Seiten. Liste, Ansicht, Löschen
  wie beim Wiki (fehlt/verboten → 404). Einreichen nur für angemeldete Nutzer.

### Herkunftsbox (ein Template-Partial für alles)

`templates/_herkunft.html`, oben auf Wiki-Seite und Vorschlagsseite, kompakt in der Vorschlagsliste:

> **Eingebracht von** CFO / Controlling (`cfo`) · **Rolle** CFO / Controlling · 05.09.2026 16:27 ·
> Domäne **finance** · **intern** · zuletzt geändert von … · Quelle: Upload

Bei Altbestand: „Herkunft unbekannt (Altbestand)" in derselben Box.

### Rechte-Datei und Admin

`permissions.yaml` bekommt die Gruppe `admin` und den Nutzer `admin` (Name „Administrator",
Gruppen `[alle, admin]`). **Admin heißt nicht Leserecht:** `decide` bleibt unverändert, der Admin
liest keine Finance- oder BR-Seiten, er verwaltet nur Rechte. Das ist Gewaltenteilung und ein
Demo-Punkt.

`/admin` (nur Gruppe `admin`, sonst 404):

- **Nutzer:** Tabelle id, Name, Gruppen als Checkboxen. Speichern pro Zeile. Neuer Nutzer (id, Name,
  Gruppen). Entfernen (nicht `gast`, nicht sich selbst).
- **Domänen:** Tabelle Domäne → Lesegruppen als Checkboxen. Neue Domäne (legt `pages/<domaene>/`
  an). Entfernen nur, wenn ihr Ordner leer ist.
- **Gruppen:** Liste, neue Gruppe.
- **Protokoll:** die letzten 20 Einträge aus `permissions-changelog.md`.

Schreiben: `access.save_permissions(data, changed_by, change_note)` schreibt `permissions.yaml`
(Kopfkommentar bleibt, Reihenfolge bleibt) und hängt eine Zeile an `permissions-changelog.md`:
`- 2026-09-05T20:15 · admin · Nutzer mitarbeiter: Gruppen [alle] → [alle, finance]`.
Der mtime-Cache aus Stufe 1 sorgt dafür, dass die Änderung sofort gilt.

## Schnittstellen

- **Paket 2 (Upload):** unverändert `wiki.save_page(slug, title, content, meta)`; die Ablage in den
  Domänenordner passiert darin. Für Vorschläge `proposals.save_proposal(..., meta)`.
- **Paket 6 (Statistik):** `total_folders` = Anzahl Domänenordner, die der Nutzer lesen darf.
  `wiki.list_pages()` ohne Nutzer bleibt ungefiltert.
- **Paket 7 (Ablage):** Ein Ablageort aus dem Korpus ist ab jetzt einfach eine Domäne mit Ordner.
  Frank kann Domänen im Admin-Dashboard anlegen.
- **Paket 4 (Bewertung):** Vorschläge über `proposals.list_proposals(user)` lesen, nie ungefiltert.

## Nicht in diesem Paket

Echtes Login und Passwörter. Rechte auf Absatzebene. Rechte für Upload-Dateien in
`project_proposals/uploads/` (die folgen dem Vorschlag, werden aber nicht separat geprüft).
