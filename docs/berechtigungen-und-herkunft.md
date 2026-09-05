# Paket 1: Berechtigungen und Herkunft von Dokumenten

Verantwortlich: Anselm · Stand: 2026-09-05 · Bezug: `Arbeitspakete.md` Paket 1, `PLAN.md` Abschnitt 4

## Kurzfassung

Jede Wiki-Seite trägt Metadaten im Dateikopf: wer sie angelegt hat, wann, wie vertraulich sie ist und
zu welcher Informationsdomäne sie gehört. Wer eine Seite sehen darf, entscheidet eine einzige Funktion
(`decide`) auf Basis dieser Metadaten und einer Rechte-Datei. Die Entscheidung greift **vor** der Suche:
Was der Fragende nicht sehen darf, bekommt auch das Sprachmodell nicht zu sehen. Personen und Gruppen
sind Daten in `permissions.yaml`, nicht Code.

Bis ein echtes Login existiert, wählt man in der Seitenleiste, als welcher Nutzer man arbeitet. Das ist
bewusst eine Simulation für den Demonstrator.

## User Stories

| Nr | Als … | möchte ich … | damit … | Fertig wenn |
|----|-------|--------------|---------|-------------|
| US-1 | Leser | auf jeder Wiki-Seite sehen, wer sie angelegt hat und wann | ich die Herkunft einer Information einschätzen kann | Seite zeigt „Angelegt von … am …" |
| US-2 | Nutzer | in der Seitenleiste wählen, als wer ich arbeite | das System meine Rechte kennt, solange es kein Login gibt | Auswahl bleibt über Seitenwechsel erhalten (Cookie); Standard ist „Gast" |
| US-3 | Autor | dass mein Name beim Anlegen automatisch gesetzt wird | Herkunft nicht fälschbar oder vergessbar ist | Feld ist nicht editierbar, kommt aus dem aktuellen Nutzer |
| US-4 | Autor | beim Anlegen und Bearbeiten die Vertraulichkeit festlegen (öffentlich, intern, vertraulich) | sensible Inhalte nicht jeder sieht | Auswahl im Formular, Standard „intern" |
| US-5 | Autor | die Seite einer Informationsdomäne zuordnen (allgemein, projekt, finance, hr, it) | Rechte über die Domäne geregelt werden können | Auswahl im Formular, Standard „allgemein" |
| US-6 | Leser | in der Seitenliste nur Seiten sehen, die ich sehen darf | ich nicht erfahre, was es an verbotenen Inhalten gibt | Seiten anderer Domänen fehlen in der Liste komplett |
| US-7 | Fragender | bei „Frag das Wiki" nur Quellen aus erlaubten Seiten bekommen | das Sprachmodell nichts verrät, was ich nicht lesen dürfte | Vorfilter vor der Trefferauswahl; Test beweist, dass kein verbotener Text im Kontext landet |
| US-8 | Leser | beim direkten Aufruf einer verbotenen URL eine 404 bekommen | ich nicht einmal die Existenz der Seite erkenne | `/wiki/<slug>` liefert 404 statt Umleitung; Bearbeiten und Löschen ebenso |
| US-9 | Leser | bei bearbeiteten Seiten zusätzlich sehen, wer zuletzt geändert hat und wann | Herkunft auch nach Änderungen nachvollziehbar bleibt | „Zuletzt geändert von … am …" erscheint nur, wenn es eine Änderung gab |

## Datenmodell

### Metadaten im Seitenkopf (YAML-Frontmatter in `llm-wiki/pages/<slug>.md`)

```yaml
---
erstellt_von: pmo-leiterin        # Nutzer-ID aus permissions.yaml; "unbekannt" bei Altbestand
erstellt_am: 2026-09-05T18:30:00  # ISO 8601, lokale Zeit
geaendert_von: cfo                # nur wenn nach dem Anlegen geändert
geaendert_am: 2026-09-05T19:02:00
vertraulichkeit: intern           # oeffentlich | intern | vertraulich
domaene: allgemein                # allgemein | projekt | finance | hr | it
empfaenger: []                    # nur bei "vertraulich": Nutzer-IDs oder Gruppen, die lesen dürfen
ablageort: ""                     # Paket 7 (Frank) befüllt das
quelle: wiki                      # wiki | upload   (Paket 2, Ekkehardt, setzt "upload")
---
# Titel der Seite

Inhalt …
```

Seiten ohne Frontmatter (Altbestand) gelten als `erstellt_von: unbekannt`, `vertraulichkeit: intern`,
`domaene: allgemein`. Sie werden beim nächsten Speichern mit Metadaten versehen.

### Rechte-Datei `llm-wiki/permissions.yaml`

```yaml
gruppen: [alle, projekt, finance, hr, it, leitung]

nutzer:
  gast:          {name: "Gast (nicht angemeldet)", gruppen: []}
  mitarbeiter:   {name: "Mitarbeiter",             gruppen: [alle]}
  pmo-leiterin:  {name: "PMO-Leiterin",            gruppen: [alle, projekt]}
  cfo:           {name: "CFO",                     gruppen: [alle, finance, leitung]}
  hr-leitung:    {name: "HR-Leitung",              gruppen: [alle, hr, leitung]}
  it-admin:      {name: "IT-Administration",       gruppen: [alle, it]}

domaenen:
  allgemein: {lesen: [alle]}
  projekt:   {lesen: [alle]}
  finance:   {lesen: [finance, leitung]}
  hr:        {lesen: [hr, leitung]}
  it:        {lesen: [it, leitung]}
```

Nutzer sind Rollen, keine echten Personen. Neue Nutzer, Gruppen oder Domänen: Datei ändern, kein Code.

### Entscheidungsregel `decide(nutzer, metadaten) -> ALLOW | DENY`

1. `vertraulichkeit == oeffentlich` → ALLOW, auch für Gast.
2. Nutzer ist Gast (keine Gruppen) → DENY.
3. Nutzer hat keine Gruppe aus `domaenen[domaene].lesen` → DENY.
4. `vertraulichkeit == vertraulich` und Nutzer ist weder `erstellt_von` noch in `empfaenger` (als ID
   oder über eine seiner Gruppen) → DENY.
5. Sonst ALLOW.

Das Label verschärft nur: eine vertrauliche Seite ist nie für mehr Leute sichtbar als eine interne
derselben Domäne. Der Ersteller sieht seine Seite immer, außer er ist Gast.

### Wo die Regel greift (ein Zugriffsweg, keine Ausnahmen)

| Stelle | Verhalten bei DENY |
|--------|--------------------|
| Seitenliste in der Seitenleiste | Seite fehlt |
| `/wiki/<slug>` | 404 |
| `/wiki/<slug>/edit` (GET und POST) | 404 |
| `/wiki/<slug>/delete` | 404 |
| Suche und „Frag das Wiki" | Seite wird **vor** der Trefferauswahl ausgeschlossen, nicht danach |

## Schnittstellen für andere Pakete

- **Paket 2 (Upload):** `wiki.save_page(slug, title, content, meta)` mit `meta.quelle = "upload"` und
  `meta.erstellt_von = <aktueller Nutzer>`. Der aktuelle Nutzer kommt aus `access.current_user(request)`.
- **Paket 7 (Ablage):** `meta.ablageort` ist vorgesehen und wird angezeigt, sobald befüllt. Sinnvoll:
  Ablageort → Domäne ableiten (z. B. `sharepoint_hr/…` → `hr`).
- **Paket 6 (Statistik):** `wiki.list_pages(user=None)` liefert ungefiltert alle Seiten mit Metadaten.
- **Paket 4 (Bewertung):** Abgleich nur über `wiki.search_snippets(query, user)`, nie über den Rohbestand.

## Nicht in diesem Paket

Echtes Login, Passwörter, Rechte auf Absatzebene, Rechte für die Experten-Agenten (Agent vertritt
Rolle, siehe `PLAN.md` Abschnitt 4). Das kommt, wenn der Demonstrator steht.
