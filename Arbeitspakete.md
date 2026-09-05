# Arbeitspakete MediaparkBrain

Stand: 2026-09-05 · Basis: `PLAN.md` und das LLM-Wiki unter `llm-wiki/`

**Zustände:** Jedes Paket ist in genau einem von drei Zuständen. Wer den Zustand ändert, ändert ihn in
der Tabelle und im Paket-Abschnitt und stellt einen kurzen PR.

| Zustand | Bedeutung |
|---------|-----------|
| ⬜ Offen | Noch niemand dran |
| 🟡 In Arbeit | Branch existiert, wird gebaut |
| ✅ Fertig | PR gemerged, „Fertig wenn"-Kriterien erfüllt |

Jedes Paket hat genau einen Verantwortlichen. Wer ein Paket anfängt, arbeitet auf einem eigenen Branch
(`<name>/<thema>`) und stellt einen PR nach `main`. Kleine PRs, oft mergen. Gemeinsame Basis ist das
LLM-Wiki (FastAPI, Markdown-Seiten in `llm-wiki/pages/`, Fragen über `/ask`). Wer eine Schnittstelle
braucht, die ein anderes Paket liefert, spricht das kurz ab und baut solange gegen einen Platzhalter.

| Nr | Paket | Verantwortlich | Zustand |
|----|-------|----------------|---------|
| 1 | Berechtigungen und Herkunft von Dokumenten | Anselm | 🟡 In Arbeit |
| 2 | Datei-Upload und Überführung in die Wissensdatenbank | Ekkehardt | ⬜ Offen |
| 3 | Funktionsbeschreibung des Systems | Florian | ⬜ Offen |
| 4 | Bewertungslogik: Gab es das Projekt schon? | Marc | ⬜ Offen |
| 5 | Upload-Feedback: pinker Rahmen und Sound | Oxana | ⬜ Offen |
| 6 | Statistik: Wie viele Dokumente sind drin? | Antje | ⬜ Offen |
| 7 | Ablage-Zuordnung hochgeladener Dateien | Frank | ⬜ Offen |

---

## 1. Berechtigungen und Herkunft von Dokumenten — Anselm

**Zustand:** 🟡 In Arbeit (PR offen, Konzept: `docs/berechtigungen-und-herkunft.md`)

**Ziel:** Das System weiß, wer ein Dokument eingebracht hat und wer es sehen darf. Grundlage für
Abschnitt 4 in `PLAN.md` (Zugriffsrechte und Informationsgrenzen).

**Umfang**
- Jedes Dokument bekommt beim Speichern Metadaten: Hochgeladen von, Zeitpunkt, Vertraulichkeit,
  Informationsdomäne.
- Anzeige „Hochgeladen von …" auf der Dokumentseite im Wiki.
- Zugriffsregel, die vor der Suche greift: Treffer, die der Fragende nicht sehen darf, werden gar nicht
  erst an das LLM gegeben.
- Rollen- und Berechtigungskonzept als Dokument im Repo.

**Fertig wenn**
- Ein hochgeladenes Dokument zeigt seinen Uploader an.
- Zwei Testnutzer mit unterschiedlichen Rechten bekommen auf dieselbe Frage unterschiedliche Quellen.

**Schnittstellen:** Liefert das Metadaten-Schema, das Paket 2 beim Upload befüllt und Paket 7 für den
Ablageort nutzt.

---

## 2. Datei-Upload und Überführung in die Wissensdatenbank — Ekkehardt

**Zustand:** ⬜ Offen

**Ziel:** Nutzer laden Dateien (PDF, DOCX, XLSX, MD, TXT) hoch, der Inhalt landet durchsuchbar im Wiki.

**Umfang**
- Upload-Formular im Wiki (Seite `/upload`).
- Extraktion des Textes je Dateityp, Umwandlung in eine Markdown-Seite unter `llm-wiki/pages/`.
- Originaldatei wird aufbewahrt, Ablageort kommt aus Paket 7.
- Metadaten aus Paket 1 werden beim Upload gesetzt (mindestens: Uploader, Zeitpunkt).

**Fertig wenn**
- Ein Project Charter aus `test project data/` lässt sich hochladen und taucht danach als Quelle unter
  „Frag das Wiki" auf.

**Schnittstellen:** Paket 5 hängt sich an das Upload-Erfolgsereignis, Paket 6 zählt die Ergebnisse.

---

## 3. Funktionsbeschreibung des Systems — Florian

**Zustand:** ⬜ Offen

**Ziel:** Jeder im Team und jeder Zuschauer versteht in fünf Minuten, was das System macht.

**Umfang**
- Dokument `docs/FUNKTIONSWEISE.md`: Wie werden Dateien verarbeitet, wie läuft eine Frage durch das
  System, wo sitzen die vier Experten-Agenten und der Orchestrator.
- Ein Ablaufdiagramm (Text oder Bild) vom Upload bis zur Stellungnahme.
- Abgleich mit `PLAN.md`: Was ist im Hackathon umgesetzt, was ist Zielbild.

**Fertig wenn**
- Ein Teammitglied, das nicht am Code war, kann das System anhand des Dokuments korrekt erklären.

**Schnittstellen:** Holt sich von jedem Paket zwei Sätze zur Funktionsweise.

---

## 4. Bewertungslogik: Gab es das Projekt schon? — Marc

**Zustand:** ⬜ Offen

**Ziel:** Ein neuer Projektvorschlag wird gegen die vorhandenen Projekte abgeglichen. Das System sagt:
„Das gab es schon", mit Verweis auf das bestehende Projekt.

**Umfang**
- Eingabemaske für einen Projektvorschlag (Titel, Kurzbeschreibung, optional Datei).
- Abgleich gegen `project_proposals/*.md` und die Wiki-Seiten: erst Volltext-Ähnlichkeit, dann
  LLM-Urteil mit Begründung.
- Ergebnis: Ampel (neu / ähnlich / gab es schon) plus die gefundenen Treffer mit Link.

**Fertig wenn**
- `m-invoice-coni-company2` als neuer Vorschlag eingegeben wird als Dublette von
  `m-invoice-coni-company1` erkannt; ein frei erfundenes Projekt wird als neu erkannt.

**Schnittstellen:** Nutzt die Suche aus dem Wiki; ist Vorstufe für die Experten-Agenten aus `PLAN.md`.

---

## 5. Upload-Feedback: pinker Rahmen und Sound — Oxana

**Zustand:** ⬜ Offen

**Ziel:** Ein erfolgreicher Upload ist unübersehbar und unüberhörbar.

**Umfang**
- Nach erfolgreichem Upload: pinker Rahmen um die Seite oder den Upload-Bereich, ein kurzer Sound.
- Sound als lokale Datei unter `llm-wiki/app/static/`, kein externer Dienst.
- Kein Feedback bei fehlgeschlagenem Upload, dafür eine klare Fehlermeldung.

**Fertig wenn**
- Upload klappt, Rahmen erscheint, Sound spielt, beides verschwindet nach wenigen Sekunden.

**Schnittstellen:** Braucht das Upload-Erfolgsereignis aus Paket 2. Bis dahin gegen einen Testbutton bauen.

---

## 6. Statistik: Wie viele Dokumente sind drin? — Antje

**Zustand:** ⬜ Offen

**Ziel:** Auf einen Blick sehen, wie groß die Wissensbasis ist.

**Umfang**
- Seite `/stats` oder Kachel auf der Startseite: Anzahl Dokumente gesamt, nach Dateityp, nach
  Ablageort (Paket 7), Datum des letzten Uploads.
- Zahlen kommen aus dem Dateisystem bzw. den Metadaten, nicht aus einer eigenen Zählung.

**Fertig wenn**
- Nach einem Upload erhöht sich der Zähler ohne Neustart des Servers.

**Schnittstellen:** Liest Metadaten aus Paket 1 und die Ablageorte aus Paket 7.

---

## 7. Ablage-Zuordnung hochgeladener Dateien — Frank

**Zustand:** ⬜ Offen

**Ziel:** Jede hochgeladene Datei landet an einem nachvollziehbaren Ort, so wie im Demo-Korpus unter
`corpus/` (Ablageorte wie Projektlaufwerk, Finance, HR).

**Umfang**
- Regel oder Auswahl beim Upload: Zu welchem Ablageort gehört die Datei?
- Verzeichnisstruktur unter `corpus/` oder einem neuen Datenordner, die den Ablageort abbildet.
- Der Ablageort wird in den Metadaten gespeichert und auf der Dokumentseite angezeigt.

**Fertig wenn**
- Ein hochgeladenes Dokument liegt im richtigen Ordner und die Wiki-Seite zeigt den Ablageort.

**Schnittstellen:** Paket 1 leitet aus dem Ablageort Rechte ab, Paket 6 zählt danach.

---

## Reihenfolge und Abhängigkeiten

1. Paket 1 legt das Metadaten-Schema früh fest (erste Stunde), damit 2, 6 und 7 dagegen bauen.
2. Paket 2 und 7 arbeiten eng zusammen: Upload schreibt, Ablage bestimmt wohin.
3. Paket 5 und 6 hängen an Paket 2, können aber mit Testdaten sofort starten.
4. Paket 4 ist unabhängig und kann sofort auf `project_proposals/` losgehen.
5. Paket 3 läuft parallel und sammelt laufend ein.

## Gemeinsame Regeln

- Eigener Branch, PR nach `main`, Vier-Augen-Review (siehe PR #7).
- `.env` bleibt lokal. API-Key in `llm-wiki/.env` eintragen, Vorlage ist `.env.example`.
- Start lokal: `cd llm-wiki && uv run uvicorn app.main:app --reload --port 8000`
- Keine echten Personendaten in Code oder Testdaten.
