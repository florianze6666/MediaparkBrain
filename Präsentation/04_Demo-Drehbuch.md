# Demo-Drehbuch (Live oder Screenshot)

Live-Demo nur, wenn Beamer und Netz stabil sind. Sonst Screenshots aus `screenshots/`. Beides ist
vorbereitet. Server vorher starten und **einmal jeden Schritt durchklicken**, damit das Sprachmodell
warm ist.

```bash
cd ~/dev/Mediapark-Team/llm-wiki && uv run uvicorn app.main:app --port 8010
```

Browser auf 150 Prozent Zoom, Seitenleiste bleibt sichtbar. Vorher die Rolle wählen, damit während
des Pitches nur ein Wechsel nötig ist.

| Wow | Klick | Was man sieht | Fallback |
|-----|-------|---------------|----------|
| 1 | Als **CFO**: „Wissen hochladen", Business-Case-Excel aus `test project data/` wählen, Domäne Finance, hochladen | Nach wenigen Sekunden die Seite mit Herkunftsbox oben, Badge, Sound | `01_upload.png`, `02_seite_mit_herkunft.png` |
| 2 | Als **CFO**: „Frag das Wiki", Frage **wörtlich** „Budgetfreigabe Q4: Wie hoch ist das Gesamtbudget für den KI-Wissensassistenten, und wer hat es freigegeben?" | Antwort mit Zahl und Quelle „Budgetfreigabe Q4" | `03_frage_cfo.png` |
| 2 | Rolle auf **Mitarbeiter**, dieselbe Frage | „Dazu findet sich nichts im Wiki." | `04_frage_mitarbeiter.png` |
| 2 | Optional, wenn Zeit: als **Admin** unter `/admin` dem Mitarbeiter Finance geben, zurück zu Mitarbeiter, Frage erneut | Jetzt die Antwort, Protokollzeile im Admin | `05_admin.png` |
| 3 | Als **CFO**: „Projektvorschläge" → „Bewerten" | Drei Anträge, vier Expertenspalten mit Score und Begründung | `06_bewertung.png` |
| 3 | „Dashboards" → Projektanträge | Tabelle: Titel, Dokumente, Beantragt von, Datum, Status | `07_projektuebersicht.png` |

## Die Frage muss genau so lauten

Die Suche ist eine Stichwortsuche (Backlog Paket 15). Allgemeine Fragen („Wie hoch ist das Budget?")
treffen Füllwörter auf anderen Seiten und die Budgetseite fällt aus den fünf Treffern. Mit dem Wort
„Budgetfreigabe" im Satz liegt sie sicher auf Platz eins. Getestet am 2026-09-06:

> Budgetfreigabe Q4: Wie hoch ist das Gesamtbudget für den KI-Wissensassistenten, und wer hat es freigegeben?

CFO: „220.000 EUR, Freigabe durch Controlling unter Vorbehalt eines Zwischenberichts", mit Zitat.
Mitarbeiter: „Im bereitgestellten Kontext findet sich keine Information."

Vor dem Pitch keine Test-Seiten mit langen Texten im Wiki anlegen, die verschieben das Ranking.

## Bekannte Stolpersteine

- Die Bewertungsseite ruft für drei Anträge je vier Sprachmodell-Aufrufe ab. Das dauert 20 bis 40
  Sekunden. **Vor dem Pitch einmal aufrufen**, dann ist sie im Kopf, und im Pitch den Screenshot nehmen.
- Sprachausgabe („Yeah, Yeah!") ist im Raum entweder ein Lacher oder peinlich. Vorher entscheiden,
  Ton am Laptop entsprechend an oder aus.
- Wenn das Sprachmodell nicht antwortet: Die App zeigt dann rohe Wiki-Ausschnitte statt einer
  Antwort. Das ist erkennbar am Hinweistext. Dann sofort auf Screenshots wechseln.
- Nutzerwahl ist ein Cookie. Nach einem Server-Neustart ohne `MPB_SECRET` ist man wieder Gast.
  Das Secret steht in der `.env`, also nur relevant, wenn jemand die Datei löscht.
