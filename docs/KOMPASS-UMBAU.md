# Kompass-Umbau: neue Oberfläche über der bestehenden Logik

Stand: 2026-09-06 · Branch `design/kompass` · 136 Tests grün (`cd llm-wiki && uv run pytest -q`)

Das Design-Handoff `frontend/design_handoff_kompass/` ist an die laufende Anwendung angeschlossen.
Die Handoff-Dateien bleiben unverändert dort liegen (Referenz); übernommen wurden Kopien nach
`llm-wiki/app/static/kompass.css` und `llm-wiki/app/templates/kompass/`.

**Zwei Regeln haben den Umbau bestimmt:**

1. **Nichts Bestehendes kaputt machen.** Alle bisherigen Routen sind erreichbar und funktionieren.
   Die alten Templates bleiben für sie zuständig.
2. **Rechte bleiben exakt wie sie sind.** Jede neue Route liest über `access.current_user`,
   `wiki.list_pages(user)`, `proposals.list_proposals(user)`, `wiki.search_snippets(q, user)` und
   `require_page` / `require_proposal` / `require_author` / `require_writable` / `require_admin`.
   Keine Sonderlogik, keine zweite Prüfstelle. Alle Security-Tests sind unverändert grün.

---

## Was neu ist

| Datei | Zweck |
|---|---|
| `app/static/kompass.css` | Design-Tokens und Layout der Kompass-Shell (Kopie aus dem Handoff, unverändert) |
| `app/templates/kompass/*.html` | Shell + Seiten aus dem Handoff, plus drei ergänzte Seiten (siehe unten) |
| `app/kompass.py` | View-Models: reine Funktionen, die aus Seiten, Vorschlägen und Rechten die dicts bauen, die die Templates erwarten |
| `app/evaluation_cache.py` | Ergebnis-Cache der Experten-Bewertung unter `data/evaluations/<slug>.json` |
| `tests/test_kompass.py` | 14 Tests, davon 8 mit Marker `security` |

Ergänzte Templates, die es im Handoff nicht gab:
`kompass/page.html` (Wissensseite in der Kompass-Shell), `kompass/search.html` (Suchergebnisse),
`kompass/log.html` (Protokoll unter `/admin/log`).

Änderungen an den übernommenen Handoff-Templates (bewusst klein gehalten):

- `layout.html`: Cache-Buster `?v=1` am Stylesheet.
- `dashboard.html`: KPI-Block hängt an `show_kpis` (auf `/proposals` aus, auf `/` an).
- `proposal_detail.html`: Herkunftszeile in der Grundinfo (US-10), Domäne/Vertraulichkeit im
  Neu-Modus, Knopf „Felder speichern“, Knopf „Bewertung starten“ / „Neu bewerten“, eine
  zusätzliche Zeile „Begründung“ in der Rollen-Detailansicht (sonst wäre der Bewertungstext des
  Modells nirgends sichtbar).

---

## Routen: was neu ist, was bleibt

### Neu (rendern `kompass/*`)

| Route | Template | Anmerkung |
|---|---|---|
| `GET /` | `dashboard.html` | ersetzt die alte Startseite; `?sort=name\|completeness\|score\|submitted\|deadline` |
| `GET /proposals` | `dashboard.html` | `active='proposals'`, ohne KPIs |
| `GET /proposals/new` | `proposal_detail.html` `mode='new'` | `require_author` |
| `POST /proposals` | – | legt an, Redirect auf das Detail; Dublettenprüfung wie bisher (Name + Datei-Hash) |
| `GET /proposals/{slug}` | `proposal_detail.html` `mode='view'` | ersetzt `proposal_view.html` |
| `POST /proposals/{slug}` | – | Pflichtfelder speichern (`require_writable`) |
| `POST /proposals/{slug}/evaluate` | – | Bewertung starten, Ergebnis in den Cache, Redirect `#bewertung` |
| `POST /proposals/{slug}/message` | – | Dialogeintrag (`kind`: message \| escalation \| internal) |
| `POST /proposals/{slug}/remind` | – | Vermerk „Erinnerung vermerkt für …“ |
| `POST /proposals/{slug}/share` | – | Vermerk „Statuslink: /proposals/{slug}“ |
| `POST /proposals/{slug}/decide` | – | `approve\|defer\|reject`; 409, solange nicht alle vier Rollen bewertet haben |
| `POST /proposals/{slug}/escalations/{id}/approve` | – | 404 (es gibt keine Eskalationen) |
| `GET /proposals/{slug}/files/{name}` | – | Datei aus `upload_dir`, nur mit `require_proposal` |
| `GET /knowledge` | `knowledge.html` | `?sort=&dir=&dept=` |
| `GET /knowledge/{slug}` | `page.html` | `require_page` |
| `GET /knowledge/share` / `/knowledge/edit` | – | Redirect auf `/knowledge` bzw. `/new` |
| `POST /api/prefill?target=knowledge\|proposal` | – | multipart `files` oder JSON `{text}`; `require_author` |
| `GET /search?q=` | `search.html` | zwei Listen (Wissen / Projekte), Link „Frage ans Wiki stellen“ → `/ask` |
| `GET /principles` | `principles.html` | |
| `GET /admin/log` | `log.html` | nur admin, sonst 404 |
| `GET /settings` | `settings.html` | |
| `POST /switch-user` | – | wie `/login`, signierter Cookie |
| `POST /settings/mail` | – | Cookie `kp_mail`, 204 |
| `GET/POST /admin/permissions` | `admin_permissions.html` | nur admin, sonst 404 |
| `GET /admin/roles/new`, `/admin/roles/{key}` | – | Redirect auf `/admin` (Nutzerverwaltung bleibt dort) |

### Bleibt unverändert erreichbar (alte Templates)

`GET /wiki/{slug}`, `GET/POST /wiki/{slug}/edit`, `POST /wiki/{slug}/delete`, `GET/POST /new`,
`GET/POST /ask`, `GET /dashboard`, `GET /dashboard/projektantraege`, `GET /admin` samt
`/admin/users/*`, `/admin/domains/*`, `/admin/groups/new`, `GET /proposals/evaluate`,
`POST /proposals/new`, `POST /proposals/{slug}/delete`, `POST /api/extract-document`,
`POST /login`, `POST /logout`, `POST /upload` mit den alten Feldnamen (`file`, `vertraulichkeit`,
`domaene`).

Zwei Sonderfälle:

- **Alte Startseite:** die Wiki-Seite „start“ in der alten Shell liegt weiterhin unter
  `/wiki/start` — dieselbe Route wie jede andere Wiki-Seite, kein Sonderweg.
- **Alte Upload-Maske:** `/upload` zeigt jetzt die Kompass-Maske, die alte Maske liegt unter
  `/upload?classic=1`. (Abweichung vom Auftrag, begründet unten.)

`proposal_view.html`, `proposal_list.html`, `proposal_new.html`, `index.html`, `dashboard*.html`,
`admin.html`, `ask.html`, `edit.html`, `upload.html` bleiben als Dateien liegen; gelöscht wurde
nichts.

---

## Kontext-Mapping je Template

Gemeinsam über `kctx(request, active, **extra)` in `main.py`:
`current_user` (`{key, display_name, initials}`), `visible_domains` (`access.readable_domains`),
`active`, `collapsed` (Cookie `kp_collapsed`), `q`.

| Template | Kontext | Quelle |
|---|---|---|
| `dashboard.html` | `proposals`, `kpi`, `knowledge_count`, `show_kpis` | `kompass.dashboard_rows(user, sort)`, `kompass.kpi(user, rows)`, `wiki.list_pages(user)` |
| `proposal_detail.html` | `mode`, `p`, `can_edit`, `fill_fields`, `fill_endpoint`, im Neu-Modus `domains`, `confidentiality_levels`, `default_*` | `kompass.proposal_vm(proposal, user, mode)`, `access.can_write`, `access.readable_domains` |
| `knowledge.html` | `stats`, `docs`, `graph`, `cloud`, `sort`, `dir`, `dept` | `kompass.knowledge_vm(user, sort, dir, dept)` |
| `page.html` | `page`, `content_html`, `herkunft` | `require_page`, `render_markdown`, `page.meta` |
| `upload.html` | `target`, `fill_fields`, `fill_endpoint`, `readers`, `saved` | `kompass.KNOWLEDGE_FIELDS`, Lesegruppen der Standarddomäne |
| `search.html` | `q`, `snippets`, `hits` | `wiki.search_snippets(q, user)`, `proposals.list_proposals(user)` |
| `principles.html` | `stats` | `kompass.principles_stats(user)` |
| `settings.html` | `users`, `mail_reminders` | `access.list_users()`, Cookie `kp_mail` |
| `admin_permissions.html` | `domains`, `groups`, `roles`, `changelog` | `kompass.permissions_matrix()` |
| `log.html` | `changelog` | `access.read_changelog(50)` |

---

## Ehrlich statt schön: was Stub ist und was fehlt

Die Oberfläche zeigt an keiner Stelle eine erfundene Zahl. Wo Daten fehlen, steht „–“ oder 0.

| Feld in der Oberfläche | Zustand | Grund |
|---|---|---|
| „Zugriffe“ je Dokument | `–` | Es gibt kein Zugriffs-Logging pro Seite. |
| „Deadline“ je Antrag | `–`, nie dringend | Der Vorschlag hat kein Deadline-Feld. |
| „Tage bis Gremium“ | `–` | Nur gesetzt, wenn `MPB_BOARD_DATE` (ISO-Datum) in der Umgebung steht. |
| „aus N Dokumenten Unternehmenswissen“ | `0` | Die Bewertung liest nur die Antragsunterlagen, kein Wiki-Wissen (bekannte Lücke, USER-STORIES „Bewertung ohne Wissensbasis“). Deshalb ist `sources` je Rolle leer. |
| „% belegt“ / „überholt“ auf der Grundsatzseite | `0` | Kein Quellennachweis, kein Gültigkeitsdatum im Dokumentkopf. |
| „wartet auf Freigabe“ (Eskalationen) | `0`, Route 404 | Eskalationen sind nicht gebaut; Agenten fragen heute nicht nach. |
| „automatische Entscheidungen“ | `0` | Es gibt keine — und soll auch keine geben. |
| „Zugriffe heute abgelehnt“ | echter Zähler | `access.deny_count()`, gezählt in `access.decide`; **seit Prozessstart**, nicht seit Mitternacht (ein Neustart setzt ihn zurück). |
| „Einträge heute“ | echte Zahl | Zeilen in `permissions-changelog.md` mit heutigem Datum. |
| Erinnerung (🔔) | Stub, aber sichtbar | Kein Mailversand. Es entsteht ein Dialogeintrag „Erinnerung vermerkt für …“. |
| Statuslink (↗) | Stub, aber sichtbar | Kein Kurzlink-Dienst. Es entsteht ein Dialogeintrag mit der Antragsadresse; wer sie öffnet, sieht den Antrag nur mit Recht. |
| „stale_year“ (überholt) | `None` | Kein Feld dafür im Dokumentkopf. |
| Wortwolke, Wissensgraph | echt, aber grob | Wortwolke: Top-14 Wörter ab 5 Zeichen aus lesbaren Seiten. Graph: Domänen in einer Reihe, je lesbarer Domäne bis zu drei Dokumente darunter, Positionen deterministisch. Nicht lesbare Domänen bleiben blass sichtbar (gesperrt ≠ nicht vorhanden), ohne ihre Dokumente. |

Abgeleitete Werte, die im Code kommentiert sind:

- `status_sentence` — aus Status, fehlenden Pflichtfeldern und Anzahl Bewertungen
  („Warten auf 3 Pflichtfelder“, „4 Rollen bewertet, Entscheidung offen“, „Entschieden: freigegeben“).
- `next_step` / `next_owner` — Vollständigkeit vor Bewertung vor Entscheidung.
- `step` (1–5) — aus Status, Vollständigkeit und Anzahl Bewertungen.
- „Konflikt mit anderen Rollen“ — Abstand von 3 oder mehr Punkten zum höchsten bzw. niedrigsten
  Score der anderen Rollen; das ist der einzige Konflikt, den die Daten hergeben.
- „Versionen“ — Commits der Antragsdatei (`git log`). Ungetrackte Datei → leere Liste.

---

## Bewertungs-Cache

`evaluation.evaluate_proposal` ruft das LLM und braucht bis zu einer Minute. Ohne Cache wäre jede
Seitenansicht ein Modelllauf. Deshalb:

- `POST /proposals/{slug}/evaluate` führt den Lauf aus und legt das Ergebnis unter
  `data/evaluations/<slug>.json` ab (Pfad über `MPB_DATA_DIR` überschreibbar, Tests nutzen tmp).
- `GET /proposals/evaluate` (alte Route) bleibt und schreibt zusätzlich in denselben Cache.
- Dashboard und Antragsdetail lesen **ausschließlich** aus dem Cache. Steht dort nichts, ist der
  Score leer (`state='none'`), nicht geschätzt.
- Auch ein Fehlerergebnis (kein API-Key, unlesbare Antwort) wird gespeichert — dann ist sichtbar,
  dass ein Lauf stattfand, ohne dass ein Score entstand.
- `llm-wiki/data/evaluations/` steht in `.gitignore`.

---

## Datenmodell: was am Vorschlag dazugekommen ist

`app/proposals.py` schreibt zwei optionale Blöcke mehr in den Kopf eines Vorschlags:

- die 15 Pflichtfelder aus `PLAN.md` §2 (`projektname`, `beschreibung`, `zielsetzung`, `nutzen`,
  `geschaeftsprozesse`, `organisationseinheiten`, `business_case`, `kosten`,
  `wirtschaftlicher_nutzen`, `laufzeit`, `technische_abhaengigkeiten`,
  `organisatorische_abhaengigkeiten`, `risikoanalyse`, `begruendung`, `anbieterinformationen`),
- `dialog`: Liste von `{author, kind, text, zeit}`.

Beides wird nur geschrieben, wenn es Inhalt gibt — der Kopf eines alten Vorschlags bleibt Zeichen
für Zeichen wie er war. `proposals.write_proposal(proposal)` schreibt einen vorhandenen Vorschlag
zurück, ohne Einreicher, Zeitpunkt oder Rolle anzufassen (US-11).

---

## Abweichungen vom Auftrag (mit Grund)

1. **`/upload` ohne Parameter zeigt die Kompass-Maske; die alte Maske liegt unter
   `/upload?classic=1`.** Die Kompass-Navigation verlinkt `/upload` ohne Parameter, und der
   bestehende Test `test_upload_form_get` prüft die alte Maske. Statt den Test zu streichen, wurde
   er auf `?classic=1` umgezogen — die alte Maske bleibt damit erreichbar (Prinzip 1), und die
   Aussage des Tests ist unverändert.
2. **`kompass.principles_stats(user)` nimmt einen Parameter.** „Offene Felder“ darf nur über
   Vorschläge gezählt werden, die der Nutzer sehen darf; ohne Nutzer ginge das nicht.
3. **Der Neu-Antrag hat ein Feld für Domäne und Vertraulichkeit**, das im Design nicht vorgesehen
   war. Ohne das könnte niemand mehr einen Antrag in einer anderen Domäne als `projekt` einreichen —
   das wäre ein Funktionsverlust gegenüber der alten Maske, und der Security-Test
   `test_domaenen_select_zeigt_nur_lesbare` prüft genau diese Auswahl auf `/proposals/new`.
4. **Die Antragsansicht zeigt eine Herkunftszeile** („Eingebracht von X (id), Rolle Y“). US-10
   macht Herkunft zur Hauptinformation; das Design hatte nur „Owner“. Ohne die Zeile wäre eine
   bestehende Anforderung samt Test verloren gegangen.
5. **Rollen-Detail zeigt zusätzlich „Begründung“.** Sonst wäre der Bewertungstext des Modells
   nirgends sichtbar — die Felder „Mehr Punkte durch“ und „Fehlt“ tragen ihn nicht.
6. **Tests, die die alte Startseite prüften, sind umgezogen:** Seitenlisten-Prüfungen nach
   `/knowledge` (mit `knowledge_slugs`), Prüfungen auf die alte Shell (Nutzername, Admin-Link,
   Nutzerauswahl) auf `/wiki/oeffentlich` — dieselbe alte Shell, dieselbe Aussage. `/knowledge`
   hat keinen Admin-Link und keine Nutzerauswahl, dort ließen sich diese Aussagen nicht prüfen.
7. **Der Wissens-Upload hat kein Auswahlfeld für die Domäne**, sondern übernimmt die aus dem
   Drop-In vorgeschlagene Domäne als editierbares Textfeld (so das Design). Die Durchsetzung
   bleibt: `require_writable` lehnt eine fremde Domäne mit 403 ab.

---

## Was als Nächstes ansteht

- Bewertung mit Wissensbasis: erst dann sind `sources` und „aus N Dokumenten“ mehr als 0.
- Zugriffsprotokoll je Seite (für „Zugriffe“ und einen tagesgenauen Ablehnungszähler).
- Deadline und Gremiumstermin als echte Felder statt Env-Variable.
- Eskalationen: Agent fragt nach, Mensch gibt frei.
- Filter (`?filter=`) auf der Wissensseite: der Link ist da, die Auswertung fehlt.
