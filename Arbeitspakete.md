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
| 1 | Berechtigungen und Herkunft von Dokumenten | Anselm | ✅ Fertig |
| 2 | Datei-Upload und Überführung in die Wissensdatenbank | Ekkehardt | 🟡 In Arbeit |
| 3 | Funktionsbeschreibung des Systems | Florian | 🟡 In Arbeit |
| 4 | Bewertungslogik: Gab es das Projekt schon? | Marc | 🟡 In Arbeit |
| 5 | Upload-Feedback: pinker Rahmen und Sound | Oxana | 🟡 In Arbeit |
| 6 | Statistik: Wie viele Dokumente sind drin? | Antje | 🟡 In Arbeit |
| 7 | Ablage-Zuordnung hochgeladener Dateien | Frank | ⬜ Offen |
| 8 | PDF-Einlesen: Inhalt hochgeladener PDFs durchsuchbar machen | Florian | 🟡 In Arbeit |
| 9 | Erweitertes Berechtigungsmanagement: Herkunft überall, Admin-Dashboard, getrennte Ablage | Anselm | ✅ Fertig |
| 10 | Quellenzitat zu jeder Antwort im „Frag das Wiki“ | Florian | 🟡 In Arbeit |
| 19 | Belegzitate zu jeder Bewertung in der Projektbewertung | Florian | ⬜ Offen |

**Backlog (noch ohne Verantwortlichen, zum Abholen):**

| Nr | Paket | Bereich | Zustand |
|----|-------|---------|---------|
| 11 | Projektanzeige zusammenführen: eine Ansicht mit Dokumentanzahl | Oberfläche | ⬜ Offen |
| 12 | Versionierung von Dokumenten und Projektanträgen | Enterprise | ⬜ Offen |
| 13 | Projektprüfung gegen das Unternehmenswissen | Kernfunktionalität | ⬜ Offen |
| 14 | Zurücklernen: Wissensdatenbank lernt aus Projekten, Entscheidungen und Überarbeitungen | Kernfunktionalität | ⬜ Offen |
| 15 | Semantische Suche statt Stichwortsuche | Workflow und Kernprozess | ⬜ Offen |
| 16 | Nachforderungsprozess bei Projektentscheidungen | Workflow und Kernprozess | ⬜ Offen |
| 17 | Serverinstallation mit Frontend | Enterprise | ⬜ Offen |
| 18 | SharePoint-Schnittstelle | Enterprise | ⬜ Offen |

---

## 1. Berechtigungen und Herkunft von Dokumenten — Anselm

**Zustand:** ✅ Fertig (PR #18 gemerged; Konzept und Schnittstellen: `docs/berechtigungen-und-herkunft.md`)

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

**Zustand:** 🟡 In Arbeit


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

**Zustand:** 🟡 In Arbeit

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

**Zustand:** 🟡 In Arbeit (PR #17 und #21 gemerged: Einreichung mit Namens-Dublettenprüfung)

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

**Zustand:** 🟡 In Arbeit (PR #20 gemerged: Markenpalette, Badge und Sound beim Speichern)

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

**Zustand:** 🟡 In Arbeit (Dashboard gemerged, nutzt Rechtefilter)

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

## 8. PDF-Einlesen: Inhalt hochgeladener PDFs durchsuchbar machen — Florian

**Zustand:** 🟡 In Arbeit

**Ziel:** Wer im Datei-Upload ein PDF hochlädt, findet dessen **Inhalt** anschließend unter „Frag das
Wiki" wieder — nicht nur den Dateinamen.

**Ausgangslage:** Unter `/proposals/new` lassen sich bereits Dateien hochladen, sie landen aber
unverändert als Bytes in `project_proposals/uploads/<slug>/`. Es findet **keine Textextraktion** statt,
und die erzeugte Markdown-Datei listet nur die Dateinamen. Da `search_snippets()` ausschließlich
`llm-wiki/pages/` durchsucht, ist der Inhalt eines hochgeladenen PDFs heute für keine Frage
auffindbar (siehe `docs/FUNKTIONSWEISE.md`, Abschnitt 4.6).

**Technologieentscheidung: Textlayer zuerst, OCR nur als Notfall.**
Digital erzeugte PDFs — Exporte aus Word, Excel, PowerPoint, also praktisch alle Projektunterlagen —
enthalten den Text bereits exakt. OCR würde diese Seiten rastern und den Text neu erraten: man
ersetzt exakte Daten durch eine Schätzung. Bei Fließtext fällt das kaum auf, bei einem Business Case
schon: OCR verwechselt 0/O und 1/l und liest „450 T€" gern als „45O TE" — genau die Zahlen, auf die
der CFO-Agent seinen Score stützt. OCR ist deshalb ausdrücklich **Stufe 2** und nur dann zu bauen,
wenn tatsächlich gescannte PDFs auftauchen.

**Umfang**
- Textextraktion mit **pdfplumber** (reines pip-Paket, keine Systeminstallation; liefert
  Wortpositionen, Schriftgrößen und `extract_tables()`).
- Beide PDF-Bauformen bedienen, nach den Regeln in `docs/FUNKTIONSWEISE.md` Abschnitt 6:
  aus Folien exportiert (Seite = Abschnitt, Überschrift mitnehmen) und als Fließtext gesetzt
  (Seitenumbrüche zusammenfügen, Kopf-/Fußzeilen entfernen).
- Tabellen als Markdown-Tabellen übernehmen, nicht als Textwand.
- **Leerprüfung:** Kam kein oder kaum Text heraus (Bild-PDF, Scan), wird die Datei **nicht** still als
  leere Seite gespeichert, sondern mit klarer Meldung als Informationslücke ausgewiesen
  (`PLAN.md` §7, Phase 5).
- Ergebnis als Markdown-Seite unter `llm-wiki/pages/` **mit Frontmatter nach Paket 1** — erst dadurch
  wird der Inhalt abfragbar und unterliegt dem Rechtefilter.
- Seitenzahl als Belegstelle mitführen, damit eine Aussage im Original nachprüfbar bleibt.

**Fertig wenn**
- Ein PDF wird hochgeladen; eine Frage nach einem Detail daraus liefert unter „Frag das Wiki" einen
  Absatz aus genau diesem PDF als Quelle.
- Ein PDF ohne Textlayer wird mit verständlicher Meldung abgelehnt und hinterlässt keine leere Seite.

**Nicht im Umfang:** OCR, Bilderkennung, Diagrammauswertung. Wo eine Aussage nur im Bild steckt,
bleibt sie eine benannte Informationslücke.

**Schnittstellen:** Setzt auf dem Upload-Weg aus Paket 2 auf und liefert dessen PDF-Parser. Nutzt das
Frontmatter-Schema aus Paket 1 und den Ablageort aus Paket 7. Paket 6 zählt die Ergebnisse.

---

## 9. Erweitertes Berechtigungsmanagement — Anselm

**Zustand:** ✅ Fertig (PR #25 gemerged; Konzept, Schnittstellen und Sicherheitsbetrachtung: `docs/berechtigungen-stufe-2-admin-und-ablage.md`)

**Ziel:** Herkunft und Rechte ziehen sich durch das ganze System, nicht nur durch Wiki-Seiten.

**Umfang**
- Herkunftsbox als Hauptinformation auf jedem Dokument und jedem Projektvorschlag: wer, welche Rolle, wann.
- Projektvorschläge bekommen dieselben Metadaten und dieselbe Rechteprüfung wie Wiki-Seiten.
- Admin-Dashboard `/admin`: Nutzer, Gruppen, Domänenrechte pflegen, mit Änderungsprotokoll.
- Wiki-Dateien physisch nach Domäne und Vertraulichkeit getrennt abgelegt; der Agent öffnet nur Ordner, die der Nutzer lesen darf.

**Fertig wenn**
- Eine Datei ohne Kopf in `pages/finance/` findet der Mitarbeiter nicht, der CFO schon.
- Ein Admin gibt dem Mitarbeiter im Dashboard die Gruppe `finance`, danach sieht er Finance sofort.
- Ein Vorschlag zeigt oben „Eingebracht von … in der Rolle …".

**Schnittstellen:** Paket 7 legt Ablageorte künftig als Domänen im Admin-Dashboard an. Paket 4 liest Vorschläge nur gefiltert.

---

## 10. Quellenzitat zu jeder Antwort im „Frag das Wiki" — Florian

**Zustand:** 🟡 In Arbeit

**Ziel:** Keine Aussage ohne Beleg. Zu jedem Fakt, den das Wiki liefert, steht **darüber** eine
Zitatbox mit dem wörtlichen Satz aus dem Originaldokument, aus dem dieser Fakt stammt.

**Ausgangslage:** Heute liefert `/ask` einen Fließtext von Claude und darunter, getrennt davon, eine
Liste der gefundenen Ausschnitte. Wer die Antwort liest, sieht nicht, welcher Satz welche Aussage
trägt — und ob überhaupt einer.

**Umfang**
- Die Antwort wird **strukturiert** statt als ein Textblock: eine Liste von Fakten, jeder mit
  wörtlichem Zitat, Seitentitel und Link auf die Wiki-Seite. Dafür gibt `llm.ask_llm()` ein
  festes Format zurück, statt freien Text.
- **Darstellung:** Über jedem Fakt eine abgesetzte Zitatbox — typografische Anführungszeichen,
  Serifenschrift, linker Balken, gedämpfter Hintergrund. Darunter, in der normalen Schrift, die
  daraus abgeleitete Aussage. So ist auf einen Blick zu unterscheiden, was **im Dokument steht**
  und was das Modell **daraus macht**.
- Quellenangabe an jeder Box: Seitentitel als Link auf `/wiki/<slug>`, dazu die Belegstelle
  (bei eingelesenen PDFs die Seitenzahl aus Paket 8).
- **Zitatprüfung im Code:** Ein Zitat wird nur angezeigt, wenn es **wörtlich** im übergebenen
  Kontext vorkommt. Erfundene oder umformulierte Zitate werden verworfen, der zugehörige Fakt
  wird als „ohne Beleg" gekennzeichnet statt still ausgegeben. Das ist der eigentliche Wert des
  Pakets: Es macht Halluzinationen sichtbar, statt sie hübsch zu rahmen.
- Fakten ohne Beleg werden nicht unterschlagen, sondern ausdrücklich als Informationslücke
  ausgewiesen (`PLAN.md` §7, Phase 5).

**Fertig wenn**
- Eine Frage an das Wiki liefert mehrere Fakten, jeder mit einer Zitatbox darüber, die den
  wörtlichen Satz und einen Link zur Quellseite zeigt.
- Ein Zitat, das nicht wörtlich in der Wissensbasis steht, erscheint nicht als Beleg.
- Die Zitate stammen ausschließlich aus Seiten, die der Fragende sehen darf — der Rechtefilter aus
  Paket 1 bleibt wirksam, auch für die Zitattexte.

**Schnittstellen:** Nutzt die Treffer aus `wiki.search_snippets()`, die Paket 1 bereits nach Rechten
filtert. Die Seitenzahl als Belegstelle kommt aus Paket 8. Für die Experten-Agenten aus `PLAN.md` §8
ist das die Vorarbeit: deren `assessment` soll später genauso belegt sein.

---

## Backlog: Pakete 11 bis 18 (noch ohne Verantwortlichen)

Stand 2026-09-05 abends, gesammelt von Anselm. Wer eines übernimmt, trägt sich in der Tabelle ein,
setzt den Zustand auf „In Arbeit" und ergänzt Umfang und „Fertig wenn" nach dem Muster der Pakete 1 bis 10.

### 11. Projektanzeige zusammenführen — offen

**Ziel:** Es gibt nur noch eine Ansicht für Projektanträge, nicht mehrere nebeneinander (Liste,
Dashboard, Projektanträge-Dashboard). Sie zeigt pro Projekt die Anzahl der zugehörigen Dokumente.

**Fertig wenn:** Ein Klick in der Seitenleiste führt zu genau einer Projektübersicht; die alten
Ansichten sind entfernt oder leiten dorthin um.

### 12. Versionierung — offen

**Ziel:** Änderungen an Wissensdokumenten und Projektanträgen sind nachvollziehbar und
wiederherstellbar: wer hat wann was geändert, was stand vorher da.

**Umfang:** Versionshistorie pro Dokument in der Oberfläche, Diff zwischen zwei Ständen,
Wiederherstellen einer alten Version. Git im Hintergrund reicht für den Demonstrator, muss aber in der
Oberfläche sichtbar werden. Herkunftsbox (Paket 9) zeigt die Versionsnummer.

**Fertig wenn:** Eine Seite dreimal bearbeiten, die Historie zeigt drei Stände mit Autor und Zeit, ein
alter Stand lässt sich per Klick zurückholen.

### 13. Projektprüfung gegen das Unternehmenswissen — offen

**Ziel:** Die Kernfunktion aus `PLAN.md`: Ein Projektantrag wird nicht isoliert bewertet, sondern
gegen die Wissensdatenbank geprüft. Die Experten-Agenten holen sich Belege aus dem Wiki, nicht aus
dem Allgemeinwissen des Sprachmodells.

**Umfang:** Die Bewertung (Paket 4, Marcs Bewertungslogik) bekommt als Kontext die gefilterten
Treffer aus `wiki.search_snippets(query, user)`, mit der Rolle des Agenten als Nutzer. Jede Aussage
in der Stellungnahme verweist auf ein Wiki-Dokument (Paket 10). Fehlen Belege, sagt der Agent das,
statt zu raten.

**Fertig wenn:** Der CFO-Agent begründet seine Bewertung eines Antrags mit der Budgetseite aus
Finance; der Betriebsrat-Agent findet dieselbe Seite nicht und sagt, dass ihm die Finanzdaten fehlen.

**Abhängigkeiten:** Paket 4, 9, 10. Rechte: Agent = Nutzer der Rolle, siehe
`docs/berechtigungen-und-herkunft.md`.

### 14. Zurücklernen — offen

**Ziel:** Die Wissensdatenbank wächst aus dem Prozess selbst: Eingereichte Projekte, getroffene
Entscheidungen und Überarbeitungen fließen als neue Wissensdokumente zurück ins Wiki.

**Umfang:** Nach einer Entscheidung entsteht automatisch ein Wissensdokument (Projekt, Ergebnis,
Begründung, Datum) in der passenden Domäne mit Herkunft „System, aus Entscheidung zu Projekt X".
Überarbeitungen eines Antrags aktualisieren dieses Dokument (Paket 12). Nächste Anträge finden
frühere Entscheidungen als Belege.

**Fertig wenn:** Nach der Entscheidung über Projekt A findet die Prüfung von Projekt B die Entscheidung
zu A als Quelle.

**Abhängigkeiten:** Paket 13, 12.

### 15. Semantische Suche — offen

**Ziel:** Die Suche versteht Bedeutung, nicht nur Wortgleichheit. Heute ist es Stichwortabgleich
nach dem Karpathy-Light-Prinzip; „Budgetfreigabe" findet „Finanzierungszusage" nicht.

**Umfang:** Embeddings pro Absatz, Vektorsuche, Kombination mit der Stichwortsuche (hybrid). Die
Rechteprüfung bleibt **vor** der Suche: Es werden nur Absätze aus lesbaren Ordnern eingebettet und
durchsucht, kein gemeinsamer Index über alle Domänen. Leak-Tests aus Paket 1 und 9 gelten weiter.

**Fertig wenn:** Eine Frage mit anderen Wörtern als im Dokument findet den richtigen Absatz; die
Security-Tests bleiben grün.

### 16. Nachforderungsprozess — offen

**Ziel:** Fehlen einem Agenten Informationen, endet die Prüfung nicht mit „nicht bewertbar", sondern
mit einer Nachforderung an den Einreicher, wie in `PLAN.md` Abschnitt 4 (Eskalation) und Abschnitt 2
(Completeness Check) vorgesehen.

**Umfang:** Nachforderung als Objekt: was fehlt, warum, für welches Kriterium, an wen. Der Einreicher
sieht offene Nachforderungen zu seinem Antrag, kann ergänzen (Text oder Upload, Paket 2), die
Prüfung läuft danach erneut. Status pro Antrag: eingereicht, Nachforderung offen, bewertet.

**Fertig wenn:** Ein Antrag ohne Kostenangabe erzeugt eine Nachforderung des CFO-Agenten; nach
Ergänzung wird er bewertet.

**Abhängigkeiten:** Paket 13.

### 17. Serverinstallation mit Frontend — offen

**Ziel:** Das System läuft nicht nur auf Laptops, sondern auf einem Server, erreichbar für alle
Beteiligten, mit Login.

**Umfang:** Container-Image, Deployment (Ziel laut Konzept: Azure Container Apps oder Fly.io für die
Demo), echtes Login statt Nutzerauswahl (Schnittstelle `access.current_user`), HTTPS, Secrets als
Umgebungsvariablen, persistente Ablage für `pages/` und `uploads/`.

**Fertig wenn:** Eine URL, ein Login, das Wiki läuft mit allen Rechten wie lokal.

### 18. SharePoint-Schnittstelle — offen

**Ziel:** Dokumente kommen direkt aus SharePoint in die Wissensdatenbank, statt per Hand
hochgeladen zu werden. Die Ablageorte des Korpus (`sharepoint_finance`, `sharepoint_hr`, …) sind
dafür schon als Domänen angelegt.

**Umfang:** Anbindung über Microsoft Graph, Abgleich pro Bibliothek, Zuordnung Bibliothek → Domäne
(Paket 7), Übernahme der SharePoint-Berechtigungen als Lesegruppen, regelmäßiger Sync,
Herkunft „Quelle: SharePoint, Pfad …" in der Herkunftsbox.

**Fertig wenn:** Eine Datei in der Finance-Bibliothek erscheint nach dem Sync in `pages/finance/`
und ist nur für Finance-Leser sichtbar.

**Abhängigkeiten:** Paket 2, 7, 17.

---

## Bekannte Lücken (Stand 2026-09-05 abends)

Transparent festgehalten, damit niemand denkt, es sei fertig. Details und Testfälle in
`docs/USER-STORIES.md`, Abschnitt „Bekannte Lücken".

| Nr | Lücke | Risiko | Gehört zu |
|----|-------|--------|-----------|
| L-1 | `/proposals/evaluate` liest Vorschläge **ungefiltert**: ein Mitarbeiter sieht die Bewertung von Finance-Vorschlägen | Rechte | Paket 4 (Marc), Einzeiler `list_proposals(user)` plus Security-Test |
| L-2 | Bewertung nutzt nur den Vorschlagstext, **kein Wiki-Wissen**, Agent hat keine Rolle als Nutzer | Kernfunktion fehlt | Paket 13 (Backlog) |
| L-3 | `pdf_ingest.py` ist fertig und getestet, aber **nicht an den Upload angebunden**; der Upload nutzt weiter pypdf roh aus `extractors.py` | Doppelte Module | Paket 8 (Florian) und 2 (Ekkehardt) |
| L-4 | **Keine Tests** für Hash-Dublette, Bewertung, Projektanträge-Dashboard | Regressionen unbemerkt | Paket 4, 6 |
| L-5 | Login ist eine **Auswahl**, kein Login; Cookie ist signiert, aber jeder darf jede Rolle wählen | Nur für Demo tragbar | Paket 17 (Backlog) |
| L-6 | Zwei offene Doppelarbeiten: Franks PR #28 baut die Domänenordner, die Paket 9 schon hat | Merge-Konflikt, verlorene Arbeit | Paket 7 (Frank), Entscheidung im Team |

---

---

## 19. Belegzitate zu jeder Bewertung in der Projektbewertung — Florian

**Zustand:** ⬜ Offen

**Ziel:** Dasselbe Prinzip wie Paket 10, eine Ebene höher: Zu **jeder** der vier Experten-Bewertungen
werden die Textstellen angezeigt, die zu genau diesem Score geführt haben — wörtlich aus den
Projektunterlagen. Nicht mehr als die **fünf relevantesten** je Bewertung.

**Ausgangslage:** `evaluation.evaluate_proposal` liefert je Rolle Status, Score, Begründung und
fehlende Informationen. Die Begründung ist Fließtext: Wer den Score anzweifelt, kann nicht
nachsehen, worauf er beruht. Bei einer Portfolio-Entscheidung über sechsstellige Beträge ist das
zu wenig — `PLAN.md` §10 verlangt ausdrücklich „die wesentlichen Informationsquellen".

**Umfang**
- Das Ausgabeschema je Rolle bekommt ein Feld `belege`: eine Liste von wörtlichen Zitaten aus dem
  Projekttext, jeweils mit Herkunft (Dateiname, bei PDFs die Seitenzahl aus Paket 8).
- **Höchstens fünf Belege je Rolle**, nach Relevanz für genau diese Bewertung geordnet — der
  Beleg, der den Score am stärksten trägt, steht oben. Fünf sind lesbar; eine vollständige
  Fundstellenliste liest niemand.
- **Zitatprüfung wie in Paket 10:** Ein Beleg wird nur angezeigt, wenn er wörtlich im
  Projekttext vorkommt. Die Prüffunktion aus Paket 10 wird wiederverwendet, nicht neu gebaut.
- Darstellung in `proposal_evaluation.html` wie im Wiki: Zitatbox über der Begründung,
  typografische Anführungszeichen, Serifenschrift, linker Balken.
- Status **INFORMATION FEHLT** braucht keine Belege — dort steht ja gerade nichts. Die bereits
  vorhandene Liste `fehlende_informationen` bleibt, wie sie ist.

**Fertig wenn**
- Jede der vier Rollenbewertungen zeigt bis zu fünf wörtliche Belegzitate mit Herkunft.
- Ein Beleg, der nicht wörtlich in den Projektunterlagen steht, erscheint nicht.
- Eine Bewertung mit Status INFORMATION FEHLT zeigt keine Belege, sondern weiter die fehlenden
  Informationen.

**Schnittstellen:** Nutzt die Zitatprüfung aus Paket 10 und den Projekttext aus
`evaluation._project_text`. Die Seitenzahl als Belegstelle kommt aus Paket 8. Für `PLAN.md` §8
ist das der letzte Baustein: Damit ist das `assessment` jedes Experten-Agenten belegt.

---

## Reihenfolge und Abhängigkeiten

1. Paket 1 legt das Metadaten-Schema früh fest (erste Stunde), damit 2, 6 und 7 dagegen bauen.
2. Paket 2 und 7 arbeiten eng zusammen: Upload schreibt, Ablage bestimmt wohin.
3. Paket 5 und 6 hängen an Paket 2, können aber mit Testdaten sofort starten.
4. Paket 4 ist unabhängig und kann sofort auf `project_proposals/` losgehen.
5. Paket 3 läuft parallel und sammelt laufend ein.
6. Paket 8 hängt am Upload-Weg aus Paket 2, lässt sich aber vorher eigenständig entwickeln und erst
   am Ende einhängen. Testmaterial fehlt allerdings: `test project data/` enthält nur DOCX und XLSX,
   **kein einziges PDF** — als Erstes braucht es also PDF-Exporte dieser Unterlagen.

## Gemeinsame Regeln

- Eigener Branch, PR nach `main`, Vier-Augen-Review (siehe PR #7).
- `.env` bleibt lokal. API-Key in `llm-wiki/.env` eintragen, Vorlage ist `.env.example`.
- Start lokal: `cd llm-wiki && uv run uvicorn app.main:app --reload --port 8000`
- Keine echten Personendaten in Code oder Testdaten.
