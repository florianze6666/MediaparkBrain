# Handoff: Kompass — neue UI für MediaparkBrain (Soll v8)

## Overview
Umbau des LLM-Wiki-Frontends (`llm-wiki/app`) von 10+ Seiten auf 4 Hauptseiten + 2 Nebenseiten. Jede Seite: eine Persona, ein Zweck, ein Status, ein nächster Schritt. Wenig Text, Führung durch Struktur (Sektionen, Balken, Score-Chips). Arbeitsname „Kompass“, Logo = Raute im schwarzen Quadrat (`.kp-logo`).

## About the Design Files
`design/Soll-v8-Kompass.html` ist die **Design-Referenz** (statisches HTML, im Browser öffnen). Die Dateien unter `app/` sind **fertige Jinja-Templates + CSS**, die das Design für das bestehende FastAPI/Jinja-Setup umsetzen. Sie ersetzen `layout.html`, `index.html`, `dashboard*.html`, `proposal_*.html`, `upload.html`, `edit.html`, `admin.html`, `ask.html`. Die Templates greifen auf Kontextvariablen zu, die im Kopf jeder Datei dokumentiert sind — die Routen in `main.py` müssen diese Kontexte liefern (siehe „Routen“).

## Fidelity
**Hifi.** Farben, Abstände, Typografie sind final (`kompass.css` → `:root`-Tokens). Systemfont-Stack, keine Webfonts.

## Screens
| Screen | Template | Referenz | Persona | Primäraktion (unten) |
|---|---|---|---|---|
| Dashboard | `dashboard.html` | 8a | PMO / Vorstand | Neuer Antrag |
| Antragsdetail (Neu / Bearbeiten / Ansehen) | `proposal_detail.html` | 8b, 8g | alle | kontextabhängig (`p.primary_action`) |
| Wissen | `knowledge.html` | 8c | alle | Wissen hochladen |
| Hochladen | `upload.html` + `_dropin.html` | 8d | alle | Speichern → Feuerwerk → „Weiteres hochladen“ |
| Grundsätze & Sicherheit | `principles.html` | 8e | alle | Protokoll öffnen |
| Einstellungen | `settings.html` | 8f | alle | Rolle wechseln |
| Berechtigungen (Admin) | `admin_permissions.html` | 8h | Admin | Rechte speichern |

Shell (`layout.html`): Sidebar links (einklappbar, Cookie `kp_collapsed`), Rolle + ⚙ unten links, Suche oben rechts (eine Suche, Ergebnisse getrennt nach Wissen/Projekte), Primärbutton immer am Ende des Inhalts, nie oben rechts.

## Routen — Ist (main.py, Stand 06.09.2026) → Soll
```
GET  /                       → bleibt, rendert dashboard.html statt index.html
GET  /wiki/{slug}            → bleibt, in kp-Shell (layout.html)
GET/POST /wiki/{slug}/edit   → bleibt (Editor in kp-Shell); Link „Bearbeiten“ aus knowledge.html
POST /wiki/{slug}/delete     → bleibt
GET/POST /new                → entfällt, ersetzt durch /upload?target=knowledge (Text-Modalität)
POST /api/extract-document   → umbenennen/erweitern zu /api/prefill (Antwort: {fields, readers})
GET/POST /upload             → bleibt, rendert upload.html
GET  /proposals              → bleibt, rendert dashboard.html (active='proposals')
GET/POST /proposals/new      → bleibt, rendert proposal_detail.html mode='new'
GET  /proposals/evaluate     → entfällt (Bewertung ist Sektion im Detail; Logik aus evaluation.py wandert in proposal_detail-Kontext)
GET  /proposals/{slug}       → bleibt, rendert proposal_detail.html mode='view'
POST /proposals/{slug}/delete→ bleibt (im ···-Menü, nicht als Primäraktion)
GET  /dashboard, /dashboard/projektantraege → entfallen (in /)
GET/POST /ask                → entfällt, Logik hinter GET /search?q=
GET  /admin (+ /admin/users/*, /admin/domains/*, /admin/groups/new) → bleiben als Backend; Frontend wird admin_permissions.html unter /admin/permissions
POST /login, /logout         → bleiben (Rollenwechsel = settings.html → POST /login mit user)
```
Neu: `/proposals/{slug}/message|remind|share|decide`, `/proposals/{slug}/escalations/{id}/approve`, `/search`, `/principles`, `/settings`, `/api/prefill`.

## Routen (main.py) — Soll
```
GET  /                                dashboard.html   (ersetzt index + dashboard_proposals)
GET  /proposals                       dashboard.html   (gleiche Tabelle, ohne KPIs, active='proposals')
GET  /proposals/new                   proposal_detail.html mode='new'  (+ fill_fields, fill_endpoint=/api/prefill?target=proposal)
POST /proposals                       anlegen -> redirect /proposals/{slug}
GET  /proposals/{slug}                proposal_detail.html mode='view'
POST /proposals/{slug}                Felder speichern (Vollständigkeit) -> Bewertung neu anstoßen für Rollen ohne Score
POST /proposals/{slug}/message        Dialog (kind: message|escalation|internal)
POST /proposals/{slug}/remind         Erinnerung an Einreicher / Verantwortlichen
POST /proposals/{slug}/share          Statuslink erzeugen
POST /proposals/{slug}/decide         decision=approve|defer|reject, nur wenn rated_count==4 und keine offene Eskalation
POST /proposals/{slug}/escalations/{id}/approve
GET  /knowledge                       knowledge.html  (?sort=&dir=&dept=&filter=)
GET  /knowledge/{slug}                bestehende Seitenansicht (page.html) in kp-Shell
GET  /upload?target=knowledge         upload.html
POST /upload                          speichern -> upload.html saved=True
POST /api/prefill?target=knowledge|proposal   multipart files ODER JSON {text}
                                      -> {"fields": {key: value}, "readers": "gf, finance"}
GET  /search?q=                       zwei Ergebnislisten (Wissen / Projekte), kp-Shell
GET  /principles                      principles.html
GET  /settings, POST /switch-user     settings.html (bestehender Rollenwechsel)
GET  /admin/permissions               admin_permissions.html (nur admin; Link in Einstellungen)
POST /admin/permissions               changes = JSON {"gruppe/domäne": ""|"r"|"rw"} -> permissions.yaml + changelog
```
Entfallen: `/ask` (in Suche integriert), `/proposals/evaluate` (Sektion Bewertung im Detail), `/dashboard`, `/admin` (ersetzt durch `/admin/permissions`).

## Datenmapping
- `proposal.roles[].key` = BR | CFO | IT | CEO; `state`: ok (≥7), warn (4–6), bad (0–3), none (kein Score), running.
- `completeness` aus den 15 Pflichtfeldern (PLAN.md §2); `state`: ok ≥ 13, warn ≥ 8, bad darunter.
- `total` = Mittel der vorhandenen Scores, `total_state` wie oben; `rated_count` < 4 → `decision_enabled=False`.
- `status_sentence`: ein Satz, vom Orchestrator gesetzt (z. B. „Betriebsrat wartet auf HR-Freigabe.“). Kein generischer Status.
- `next_step` + `next_owner`: aus offener Eskalation > fehlender Vollständigkeit > Entscheidung > „Warten“.
- Rolle expandiert (8g): `criteria`, `sources[]`, `improve`, `missing`, `conflict` — aus `evaluation.py` je Dimension.
- Wissensgraph: `x,y` in Prozent (0–100), Kanten als id-Paare; `locked=True` wenn Leser keine Rechte (blass, kein Link-Ziel).
- Wortwolke: Top-14 Begriffe, `weight` 1–6.

## Interaktionen
- Drop-In (`_dropin.html`): Drag & Drop, Datei-Dialog, Text/Link-Prompt, Web-Speech-Diktat. Nach Antwort von `/api/prefill` füllen sich Felder nacheinander (600 ms je Feld, Schimmer `kp-fill`, Einblenden `kp-in`), Fortschrittsbalken, dann Status grün. Klick auf ein gefülltes Feld → editierbar. „Korrigieren“ öffnet alle.
- Nach erfolgreichem Speichern: Feuerwerk (`kp-burst`, 1,4 s) + Primärbutton „Weiteres Wissen hochladen“.
- Bewertung: Rollen-Karten togglen ihr Detail; „alle ausklappen“ öffnet alle (8g). Rechte Sprungnavigation markiert die sichtbare Sektion (IntersectionObserver).
- Sidebar-Collapse: 208 px ↔ 64 px, Labels ausgeblendet.

## Design Tokens
Farben: bg #e8e8ed · Fläche #fff · Fläche-2 #f5f5f7 · Linie #e5e5ea / #f0f0f2 · Text #1d1d1f · Text-2 #3a3a3c · gedämpft #6e6e73 / #8e8e93 · Akzent #0071e3 (Hover #0058b0) · ok #34c759 · warn #ff9f0a · bad #ff3b30.
Radien 7 / 9 / 12 / 14 px. Schatten Karte 0 1px 2px rgba(0,0,0,.06). Typo: Systemfont; H1 26 px/600/−0.02em; Body 14 px; Sub 12–13 px; KPI 30 px/600; Sektionstitel 12 px uppercase 0.05em.

## Files
- `design/Soll-v8-Kompass.html` — Referenz (alle Screens, 8a–8g)
- `app/static/kompass.css`
- `app/templates/kompass/{layout,dashboard,proposal_detail,_dropin,upload,knowledge,principles,settings,admin_permissions}.html`

Ältere Richtungen zum Vergleich liegen in `design/` (v3–v7).
