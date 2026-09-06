# User Stories MediaparkBrain: Stand der Umsetzung

Stand: 2026-09-06 · Branch `design/kompass` · 136 automatisierte Tests grün (`cd llm-wiki && uv run pytest -q`)

Dieses Dokument listet **alle User Stories, die im laufenden System umgesetzt sind**. Die Stories
aus Paket 1 und 9 stammen aus den Konzeptdokumenten (US-1 bis US-19). Für die Arbeit der anderen
Pakete gab es keine Stories, sie sind hier aus Code, Routen und Tests abgeleitet (US-20 bis US-38).

**Kategorien**

| Kürzel | Kategorie | Was dazugehört |
|--------|-----------|----------------|
| KERN | Kernfunktion | Wiki bedienen, fragen, antworten, Oberfläche |
| WISSEN | Wissen | Dokumente hineinbekommen, Metadaten, Herkunft, Statistik über den Bestand |
| PROJEKT | Use-Case Projektbewertung | Projektvorschlag einreichen, prüfen, bewerten |
| SYSTEM | System | Identität, Rechte, Ablage, Administration, Sicherheit |

**Priorität**

| Stufe | Bedeutung |
|-------|-----------|
| P1 | Demo-kritisch: ohne das funktioniert der Demonstrator aus `PLAN.md` nicht |
| P2 | Wichtig: macht das System glaubwürdig oder sicher |
| P3 | Komfort |

**Testspalte:** `datei::test` = automatisierter Test in `llm-wiki/tests/`. „manuell" = kein
automatisierter Test, Testfall steht beim Eintrag.

---

## Übersicht

| ID | Story (Kurzform) | Kategorie | Prio | Paket / PR | Tests |
|----|------------------|-----------|------|------------|-------|
| US-20 | Wiki-Seiten anlegen, bearbeiten, löschen | KERN | P1 | #11 | test_frontmatter::test_save_und_get_roundtrip, test_ablage::test_domaenenwechsel_ueber_editor_verschiebt |
| US-21 | Frage stellen, Antwort aus Wiki-Inhalten mit Quellen | KERN | P1 | #11 | test_leak_ask (5), manuell |
| US-22 | Ladeanzeige während der Antwort | KERN | P3 | #13 | manuell |
| US-23 | Markenpalette, Badge und Sound beim Speichern, Sprachausgabe bei Antwort | KERN | P3 | #20 | manuell |
| US-24 | Seitenliste nach Domäne gruppiert | KERN | P3 | #25 | manuell |
| US-1 | Herkunft (angelegt von, wann) auf jeder Seite | WISSEN | P1 | Paket 1, #18 | test_access_routes::test_neue_seite_traegt_aktuellen_nutzer |
| US-3 | Autor wird automatisch gesetzt, nicht editierbar | WISSEN | P1 | Paket 1 | test_frontmatter::test_bearbeiten_setzt_geaendert_und_erhaelt_ersteller |
| US-4 | Vertraulichkeit wählbar (öffentlich, intern, vertraulich) | WISSEN | P1 | Paket 1 | test_decide (11) |
| US-5 | Domäne wählbar, Domänen folgen den Korpus-Ablageorten | WISSEN | P1 | Paket 1 | test_decide::test_matrix_intern_aus_dokument |
| US-9 | Zuletzt geändert von / am | WISSEN | P2 | Paket 1 | test_frontmatter::test_bearbeiten_setzt_geaendert_und_erhaelt_ersteller |
| US-10 | Herkunftsbox als erstes Element auf Seite, Vorschlag, Liste | WISSEN | P1 | Paket 9, #25 | test_proposals::test_vorschlag_traegt_nutzer_und_rolle, test_altbestand_zeigt_herkunft_unbekannt |
| US-25 | Datei hochladen (PDF, DOCX, XLSX, MD, TXT), Text wird Wiki-Seite | WISSEN | P1 | Paket 2, #24 | test_upload_routes::test_upload_docx_and_search, test_extractors (4) |
| US-26 | Kopfdaten automatisch per Sprachmodell, mit Fallback ohne Key | WISSEN | P2 | Paket 2 | test_upload_routes::test_api_extract_document_prepopulate |
| US-27 | Upload aus dem Editor heraus, Felder werden vorbefüllt | WISSEN | P3 | Paket 2 | test_upload_routes::test_api_extract_document_prepopulate |
| US-28 | Korpus-Stufen (C-Level, Betriebsrat-intern) werden auf das Rechtemodell übersetzt | WISSEN | P2 | Paket 2, Review #24 | test_upload_routes::test_betriebsrat_intern_normalization, test_upload_c_level_confidentiality_isolation |
| US-29 | PDF mit Textlayer strukturiert einlesen (Folien, Fließtext, Tabellen), ohne Textlayer ablehnen | WISSEN | P2 | Paket 8, #27 | test_pdf_ingest (13) · **nicht an Upload angebunden** |
| US-30 | Dashboard: Anzahl Dateien und Ordner, letzte Änderungen mit Autor | WISSEN | P2 | Paket 6, #30 | test_ablage::test_stats_total_folders_und_git_history |
| US-31 | Projektvorschlag einreichen mit Beschreibung und Dateien | PROJEKT | P1 | Paket 4, #17 #21 | test_proposals (9) |
| US-11 | Vorschlag trägt Einreicher und Rolle | PROJEKT | P1 | Paket 9 | test_proposals::test_vorschlag_traegt_nutzer_und_rolle, test_rolle_ist_snapshot |
| US-12 | Vorschläge unterliegen denselben Rechten wie Seiten | PROJEKT | P1 | Paket 9 | test_proposals::test_finance_vorschlag_nur_fuer_finance, test_gast_darf_nicht_einreichen |
| US-32 | Gleicher Projektname wird abgelehnt | PROJEKT | P2 | Paket 4, #17 | test_proposals::test_doppelter_name_bleibt_409 |
| US-33 | Gleiche Datei (Hash) wird als Dublette erkannt, nur .md als Projektdatei | PROJEKT | P2 | #29 | manuell |
| US-34 | Letzte drei Vorschläge in vier Expertendimensionen bewerten | PROJEKT | P1 | Paket 4/10, #29 | manuell · **ungefiltert, ohne Wiki-Wissen** |
| US-35 | Projektanträge-Dashboard: Titel, Dokumentanzahl, Beantragt von, Datum, Status | PROJEKT | P2 | Paket 6, #30 | manuell |
| US-2 | Als Nutzer wählen, als wer ich arbeite | SYSTEM | P1 | Paket 1 | test_access_routes::test_login_setzt_cookie_und_leitet_zurueck |
| US-6 | Seitenliste zeigt nur erlaubte Seiten | SYSTEM | P1 | Paket 1 | test_access_routes::test_mitarbeiter_sieht_finance_nicht, test_ceo_liest_br_nicht |
| US-7 | Suche und Sprachmodell sehen nur erlaubte Seiten (Vorfilter) | SYSTEM | P1 | Paket 1 | test_leak_ask (5) |
| US-8 | Verbotene URL liefert 404, nicht unterscheidbar von „gibt es nicht" | SYSTEM | P1 | Paket 1 | test_access_routes::test_verbotene_und_fehlende_seite_nicht_unterscheidbar |
| US-13 | Admin pflegt Nutzer und Gruppen in der Oberfläche | SYSTEM | P1 | Paket 9 | test_admin::test_nutzer_anlegen_und_entfernen, test_gruppe_vergeben_gilt_sofort_und_wird_protokolliert |
| US-14 | Admin pflegt Domänen, Lesegruppen und Gruppen | SYSTEM | P2 | Paket 9 | test_admin::test_domaene_anlegen_pflegen_entfernen, test_gruppe_anlegen |
| US-15 | Jede Rechteänderung wird protokolliert | SYSTEM | P2 | Paket 9 | test_admin::test_save_permissions_roundtrip_und_changelog_format |
| US-16 | Admin-Dashboard ist für Nicht-Admins unsichtbar, Admin liest keine Inhalte | SYSTEM | P1 | Paket 9 | test_admin::test_nicht_admin_bekommt_404_ueberall, test_admin_liest_keine_finance_seite |
| US-17 | Seiten liegen physisch im Ordner ihrer Domäne, vertrauliche im Unterordner | SYSTEM | P1 | Paket 9 | test_ablage (15) |
| US-18 | Der Agent öffnet nur Ordner, die ich lesen darf (Ordner ist die Wahrheit) | SYSTEM | P1 | Paket 9 | test_ablage::test_us18_* (3), test_security_fixes::test_oeffentlich_in_finance_sehen_nur_finance_leser |
| US-19 | Flache Altdateien werden beim Start einsortiert | SYSTEM | P2 | Paket 9 | test_ablage::test_migration_flacher_dateien_idempotent |
| US-36 | Schreiben nur, wo man lesen darf (Editor, Vorschlag, Upload) | SYSTEM | P1 | Paket 9 Review, #24 | test_security_fixes::test_new_in_fremder_domaene_403_und_keine_datei, test_upload_routes::test_foreign_domain_write_forbidden |
| US-37 | Identität ist ein signierter Cookie, Fälschung ergibt Gast | SYSTEM | P1 | Paket 9 Review | test_security_fixes::test_roher_cookie_ist_gast, test_manipulierte_signatur_ist_gast |
| US-38 | Path-Traversal über URL und Dateinamen ist unmöglich | SYSTEM | P1 | Paket 9 Review, #24 | test_security_fixes::test_ungueltige_slugs_sind_404, test_upload_routes::test_upload_path_traversal_prevention |

### Kompass-Oberfläche (Design-Handoff v8, siehe `docs/KOMPASS-UMBAU.md`)

| ID | Story (Kurzfassung) | Kategorie | Prio | Herkunft | Test |
|----|---------------------|-----------|------|----------|------|
| US-39 | Startseite ist ein Dashboard: je Antrag Status, Vollständigkeit, vier Rollen-Scores, nächster Schritt | PROJEKT | P1 | Kompass 8a | test_kompass::test_dashboard_und_antragsliste_filtern_nach_rechten, test_dashboard_rows_zeigt_nur_lesbares_und_keine_erfundenen_werte |
| US-40 | Ein Antrag, eine Seite: Grundinfo, Herkunft, Status, Vollständigkeit, Bewertung, Dialog, Dokumente, Versionen, Entscheidung | PROJEKT | P1 | Kompass 8b/8g | test_proposals::test_finance_vorschlag_nur_fuer_finance |
| US-41 | Vollständigkeit misst die 15 Pflichtfelder aus PLAN.md §2 und zeigt, welche fehlen | PROJEKT | P1 | Kompass 8b | test_kompass::test_completeness_zaehlt_die_fuenfzehn_pflichtfelder |
| US-42 | Bewertung wird auf Knopfdruck gestartet und gespeichert; ohne Ergebnis bleibt der Score leer | PROJEKT | P1 | Kompass 8g | test_kompass::test_evaluate_schreibt_cache |
| US-43 | Entscheiden erst, wenn alle vier Rollen bewertet haben; Entscheidung steht mit Name und Zeit im Dialog | PROJEKT | P1 | Kompass 8b | test_kompass::test_decide_ohne_vier_scores_ist_409, test_decide_mit_vier_scores_setzt_status |
| US-44 | Erinnerung und Statuslink hinterlassen einen sichtbaren Vermerk (kein Mailversand) | PROJEKT | P3 | Kompass 8a | test_kompass::test_remind_hinterlaesst_vermerk_statt_mail |
| US-45 | Antragsdokumente sind nur herunterladbar, wer den Antrag sehen darf | SYSTEM | P1 | Kompass 8b | test_kompass::test_antragsdatei_nur_mit_recht_und_ohne_traversal |
| US-46 | Wissensseite: Bestand, Graph, Wortwolke und Tabelle - alles nur aus lesbaren Seiten | WISSEN | P1 | Kompass 8c | test_kompass::test_knowledge_zeigt_finance_nur_dem_berechtigten, test_knowledge_detail_404_fuer_verbotene |
| US-47 | Eine Suche, zwei Listen (Wissen / Projekte), beide nach Rechten gefiltert | KERN | P1 | Kompass 8c | test_kompass::test_suche_findet_finance_nur_fuer_finance |
| US-48 | Hochladen füllt die Kopfdaten aus der Datei vor; jedes Feld bleibt korrigierbar | WISSEN | P2 | Kompass 8d | test_kompass::test_prefill_ist_fuer_gast_verboten |
| US-49 | Grundsätze-Seite zeigt echte Zahlen (abgelehnte Zugriffe, offene Felder) und 0, wo nichts gemessen wird | SYSTEM | P2 | Kompass 8e | manuell |
| US-50 | Berechtigungsmatrix: Gruppe × Domäne umschalten, jede Änderung wird protokolliert | SYSTEM | P1 | Kompass 8h | test_kompass::test_admin_permissions_nur_admin_und_roundtrip |

---

## KERN: Kernfunktion

### US-20 · Wiki-Seiten anlegen, bearbeiten, löschen · P1
Als Nutzer möchte ich Seiten mit Titel und Markdown-Inhalt anlegen, ändern und löschen, damit das
Wiki überhaupt Wissen enthält.
Tests: `test_frontmatter::test_save_und_get_roundtrip`, `test_ablage::test_domaenenwechsel_ueber_editor_verschiebt`, `test_ablage::test_new_lehnt_vorhandenen_slug_ab`.

### US-21 · Frage stellen, Antwort mit Quellen · P1
Als Nutzer möchte ich eine Frage in natürlicher Sprache stellen und eine Antwort bekommen, die nur
aus Wiki-Inhalten stammt und ihre Quellen nennt, damit ich der Antwort trauen kann.
Tests: `test_leak_ask` (5 Tests, Rechteseite). Manuell: Frage „Welche vier Experten-Agenten gibt es?"
→ Antwort nennt Betriebsrat, CFO, IT, CEO und unter „Quellen" die Seite „Vier Experten-Agenten".
Ohne API-Key: Antwort zeigt die rohen Wiki-Ausschnitte mit Hinweis.

### US-22 · Ladeanzeige · P3
Als Fragender möchte ich während der Antwortzeit sehen, dass gearbeitet wird.
Manuell: Frage absenden → Vollbild-Overlay mit Spinner erscheint sofort, Button gesperrt, verschwindet
mit der Antwortseite. Zurück-Taste: kein hängendes Overlay.

### US-23 · Markenpalette, Feedback beim Speichern und Antworten · P3
Als Nutzer möchte ich sichtbares und hörbares Feedback beim Speichern und bei neuen Antworten.
Manuell: Seite speichern → Badge „Yeah, Yeah! Gespeichert." und Klatsch-Sound; Antwort auf Frage →
Badge und Sprachausgabe. Links und Buttons in Magenta/Orange/Lila, kein Browser-Blau.

### US-24 · Seitenliste nach Domäne gruppiert · P3
Als Leser möchte ich in der Seitenleiste sehen, zu welcher Domäne eine Seite gehört.
Manuell: Als CFO anmelden → Überschriften ALLGEMEIN und FINANCE in der Seitenleiste; als
Mitarbeiter nur ALLGEMEIN.

## WISSEN: Wissen

### US-1, US-3, US-4, US-5, US-9 · Metadaten und Herkunft (Paket 1) · P1/P2
Siehe `docs/berechtigungen-und-herkunft.md`, Tabelle „User Stories". Tests: `test_decide` (11),
`test_frontmatter` (6), `test_access_routes::test_neue_seite_traegt_aktuellen_nutzer`.

### US-10 · Herkunftsbox als Hauptinformation · P1
Als Leser möchte ich auf jedem Dokument und jedem Vorschlag ganz oben sehen: eingebracht von wem,
in welcher Rolle, wann, Domäne, Vertraulichkeit.
Tests: `test_proposals::test_vorschlag_traegt_nutzer_und_rolle`, `test_altbestand_zeigt_herkunft_unbekannt`.
Manuell: „Budgetfreigabe Q4" als CFO öffnen → Box „Eingebracht von CFO / Controlling, Rolle CFO /
Controlling, Domäne FINANCE, intern" steht über dem Titel.

### US-25 · Datei hochladen, Text wird Wiki-Seite · P1
Als Nutzer möchte ich eine Datei (PDF, DOCX, XLSX, MD, TXT) hochladen, deren Text als Wiki-Seite
in der gewählten Domäne landet, damit Dokumente ohne Abtippen ins Wissen kommen.
Tests: `test_upload_routes::test_upload_docx_and_search` (Project Charter hochladen, danach über
„Frag das Wiki" auffindbar), `test_extractors` (DOCX, XLSX, TXT, PDF).
Manuell: Project Charter aus `test project data/` hochladen → Seite mit Herkunft „Quelle: Upload",
Originaldatei unter `llm-wiki/uploads/<domäne>/`.

### US-26 · Kopfdaten automatisch · P2
Als Nutzer möchte ich, dass Titel, Dokumenttyp, Datum, Verfasser und Klassifikation aus dem Inhalt
vorgeschlagen werden, damit ich sie nicht eintippen muss. Ohne API-Key greift ein Heuristik-Fallback.
Tests: `test_upload_routes::test_api_extract_document_prepopulate`.

### US-27 · Upload aus dem Editor · P3
Als Autor möchte ich beim Anlegen einer Seite eine Datei wählen, deren Inhalt und Kopfdaten das
Formular vorbefüllen, und vor dem Speichern noch korrigieren können.
Tests: wie US-26. Manuell: „Neue Seite" → „Dokument hochladen …" → Felder gefüllt → Speichern.

### US-28 · Korpus-Stufen übersetzt · P2
Als Betreiber möchte ich, dass Dokumente mit den Korpus-Werten `C-Level` oder `Betriebsrat-intern`
im Rechtemodell als `vertraulich` mit den passenden Empfängern landen, damit es nur eine
Entscheidungsregel gibt.
Tests: `test_upload_routes::test_betriebsrat_intern_normalization`, `test_upload_c_level_confidentiality_isolation`
(C-Level-Dokument: Mitarbeiter findet es nicht, CFO schon).

### US-29 · PDF strukturiert einlesen · P2 · **nicht angebunden**
Als Nutzer möchte ich, dass PDFs mit Textlayer als saubere Markdown-Seiten ankommen: Folien als
Abschnitte mit Seitenzahl, Fließtext ohne Seitenumbruch-Brüche, Tabellen als Markdown-Tabellen,
wiederkehrende Fußzeilen entfernt. PDFs ohne Textlayer werden mit verständlicher Begründung abgelehnt.
Tests: `test_pdf_ingest` (13). **Stand:** Modul `pdf_ingest.py` ist fertig und getestet, der
Upload-Weg nutzt aber noch `extractors.extract_pdf` (pypdf, roh). Anbindung fehlt, siehe Lücken.

### US-30 · Dashboard Dateien · P2
Als Nutzer möchte ich sehen, wie viele Dateien und Ordner ich lesen darf und welche zuletzt
geändert wurden, mit Autor und Zeit aus der Git-Historie.
Tests: `test_ablage::test_stats_total_folders_und_git_history`. Manuell: Dashboard als CFO zeigt
mehr Dateien und Ordner als als Mitarbeiter.

## PROJEKT: Use-Case Projektbewertung

### US-31 · Projektvorschlag einreichen · P1
Als Projektmanager möchte ich einen Vorschlag mit Name, Beschreibung und Dateien einreichen, damit
er geprüft werden kann. Ablage in `project_proposals/<slug>.md`, Dateien daneben.
Tests: `test_proposals` (9).

### US-11, US-12 · Vorschlag mit Herkunft und Rechten · P1
Siehe `docs/berechtigungen-stufe-2-admin-und-ablage.md`. Tests: `test_proposals::test_vorschlag_traegt_nutzer_und_rolle`,
`test_rolle_ist_snapshot`, `test_finance_vorschlag_nur_fuer_finance`, `test_gast_darf_nicht_einreichen`,
`test_vertraulicher_vorschlag_nur_ersteller_und_empfaenger`.

### US-32 · Gleicher Projektname abgelehnt · P2
Als Einreicher bekomme ich eine klare Meldung, wenn es einen Vorschlag mit demselben Namen schon gibt.
Tests: `test_proposals::test_doppelter_name_bleibt_409`.

### US-33 · Gleiche Datei als Dublette, nur .md · P2
Als Einreicher bekomme ich eine Meldung, wenn eine hochgeladene Projektdatei byte-identisch zu
einer bereits eingereichten ist, mit Verweis auf den bestehenden Vorschlag. Andere Dateitypen als
`.md` werden als Projektdatei abgelehnt.
Kein automatisierter Test. Manuell: `project_proposals/m-companion.md` als Datei zu einem neuen
Vorschlag „Test X" hochladen → 409 mit Verweis auf „M-Companion"; `.docx` anhängen → Ablehnung.

### US-34 · Bewertung in vier Expertendimensionen · P1 · **mit Einschränkungen**
Als Entscheider möchte ich die letzten drei Vorschläge aus Sicht von Betriebsrat, CFO, IT-Security
und CEO bewertet sehen, mit Score 0 bis 10, Begründung oder „nicht bewertbar, es fehlt X", nach
`Bewertungslogik_Experten-Agent_MVP.md`.
Kein automatisierter Test. Manuell: `/proposals/evaluate` als CFO → drei Vorschläge, je vier
Spalten mit Score und Text; ohne API-Key Hinweis statt Bewertung.
**Einschränkungen:** (1) Die Route liest alle Vorschläge **ungefiltert**, auch solche, die der
Aufrufer nicht sehen darf. (2) Die Bewertung nutzt nur den Vorschlagstext, **kein Wiki-Wissen**
und keine Rolle als Nutzer. Beides ist Backlog Paket 13.

### US-35 · Projektanträge-Dashboard · P2
Als Entscheider möchte ich alle Anträge mit Titel, Anzahl Dokumente, Beantragt von, Datum und
Status in einer Tabelle sehen.
Kein automatisierter Test. Manuell: `/dashboard/projektantraege` als CFO zeigt Finance-Vorschläge,
als Mitarbeiter nicht.

## SYSTEM: System

### US-2, US-6, US-7, US-8 · Identität und Lesefilter (Paket 1) · P1
Siehe `docs/berechtigungen-und-herkunft.md`. Tests: `test_access_routes` (10), `test_leak_ask` (5).

### US-13 bis US-19 · Admin, Ablage, Migration (Paket 9) · P1/P2
Siehe `docs/berechtigungen-stufe-2-admin-und-ablage.md`. Tests: `test_admin` (9), `test_ablage` (15).

### US-36 · Schreiben nur, wo man lesen darf · P1
Als Betreiber möchte ich, dass niemand Seiten, Vorschläge oder Uploads in Domänen ablegen kann,
die er nicht lesen darf, damit kein Text in das Wissen anderer Rollen eingeschleust wird.
Tests: `test_security_fixes::test_new_in_fremder_domaene_403_und_keine_datei`,
`test_edit_verschieben_in_fremde_domaene_403`, `test_proposal_in_fremder_domaene_403`,
`test_domaenen_select_zeigt_nur_lesbare`, `test_upload_routes::test_foreign_domain_write_forbidden`.

### US-37 · Signierter Identitäts-Cookie · P1
Als Betreiber möchte ich, dass ein von Hand gesetzter Cookie `mpb_user=admin` nichts bewirkt.
Tests: `test_security_fixes::test_roher_cookie_ist_gast`, `test_manipulierte_signatur_ist_gast`,
`test_korrekt_signiert_wird_erkannt`, `test_secret_aus_env_und_warnung_ohne_secret`.

### US-38 · Kein Path-Traversal · P1
Als Betreiber möchte ich, dass weder Slugs in der URL noch hochgeladene Dateinamen Dateien außerhalb
der vorgesehenen Ordner erreichen.
Tests: `test_security_fixes::test_ungueltige_slugs_sind_404`,
`test_upload_routes::test_upload_path_traversal_prevention`, `test_guest_cannot_upload_or_extract`.

---

## Testabdeckung

| Testdatei | Tests | deckt ab |
|-----------|-------|----------|
| test_decide.py | 11 | Entscheidungsregel, Rechte-Matrix |
| test_access_routes.py | 10 | Lesefilter auf allen Routen, Login |
| test_leak_ask.py | 5 | Kein verbotener Text im LLM-Kontext |
| test_frontmatter.py | 6 | Metadaten lesen/schreiben, Altbestand |
| test_ablage.py | 15 | Domänenordner, Migration, Ordner-Schranke |
| test_proposals.py | 9 | Vorschläge mit Herkunft und Rechten |
| test_admin.py | 9 | Admin-Dashboard, Protokoll, Gewaltenteilung |
| test_security_fixes.py | 14 | Write ⊆ Read, Cookie-Signatur, Slugs |
| test_upload_routes.py | 8 | Upload, Extraktion, Kopfdaten, Traversal, Normalisierung |
| test_extractors.py | 4 | DOCX, XLSX, TXT, PDF roh |
| test_pdf_ingest.py | 13 | PDF strukturiert (Modul, nicht angebunden) |
| test_kompass.py | 14 | Kompass-Seiten: Rechte, Vollständigkeit, Bewertung, Entscheidung |
| **Summe** | **136** | 54 davon mit Marker `security` |

**Ohne automatisierten Test:** US-22, US-23, US-24 (Oberfläche), US-33 (Hash-Dublette), US-34
(Bewertung), US-35 (Projektanträge-Dashboard).

## Bekannte Lücken (aus dieser Bestandsaufnahme)

1. **`/proposals/evaluate` filtert nicht nach Rechten.** `list_proposals()` ohne Nutzer. Ein
   Mitarbeiter kann die Bewertung von Finance-Vorschlägen sehen. Fix: `list_proposals(user)`, ein
   Security-Test dazu. Gehört zu Paket 4.
2. **Bewertung ohne Wissensbasis.** Die Experten-Agenten bewerten nur den Vorschlagstext. Das
   Zielbild aus `PLAN.md` (Belege aus dem Unternehmenswissen, Agent mit Rechten seiner Rolle) ist
   Backlog Paket 13.
3. **PDF-Parser nicht angebunden.** `pdf_ingest.py` ist fertig, der Upload nutzt weiterhin den rohen
   pypdf-Weg in `extractors.py`. Zwei Module für dieselbe Aufgabe. Gehört zu Paket 8 und 2.
4. **Keine Tests für Hash-Dublette, Bewertung und Projektanträge-Dashboard.**
5. **Login ist eine Auswahl.** Jeder kann jede Rolle wählen. Echtes Login ist Backlog Paket 17.
