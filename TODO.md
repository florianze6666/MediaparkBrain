# TODO — Mediapark Brain (zentrale Liste)

Format: `- [ ] Punkt — Kontext — wer/wann`. Erledigtes nach unten in „Erledigt" verschieben.

## Konzept

- [ ] **Personas und ihre Bewertungskriterien in separate MD-Dateien auslagern** — je Rolle eine
      Datei (`roles/<rolle>/ROLE.md` + `criteria.md`), damit Rollen als Plugins wachsen können und
      das Berechtigungskonzept personenfrei bleibt. Beschluss Anselm 2026-09-05. — Anselm
- [ ] Weitere Rollen nach den ersten vier (CEO, CFO, Betriebsrat, IT Security) — Kandidaten:
      Datenschutz, Einkauf, QM. Erst wenn die vier laufen.
- [ ] Portfolio-Formel: Gewichtung der drei Scores zum Gesamtwert je Projekt (P1 98, P2 91 …).
- [ ] LLM-Datenresidenz (EU-Region) — Anforderung des Demo-Kunden LTT; für die Demo klären, was
      wir zusagen.
- [ ] „HybridClaw": Was ist das (Laufzeit? Framework?) — Florian.
- [ ] Betriebsvereinbarungen liegen nur als Register im Kanon, nicht als Volltext im Korpus —
      Sync mit Eckhards Generator abwarten oder zwei BV-Volltexte selbst ergänzen.

## Technik

- [ ] Frontend-Entscheidung: htmx + Jinja (kein Build) für die Demo; React nur, wenn ein
      Frontend-Mensch da ist.
- [ ] Dockerfile + Fly.io-URL nach der ersten lokalen Demo.
- [ ] Graph-Adapter (SharePoint) als zweite `DriveSource` — nach der Demo.
- [ ] Embeddings/Hybrid-Suche — nach der Demo; BM25 reicht für 136 Dokumente.

## Erledigt

- [x] Konzeptphase: Architektur, Berechtigungskonzept, Rollen, Projektbeschreibung, Testkonzept,
      Deployment, Democompany — 2026-09-05
- [x] LTT-Korpus (136 Dokumente) + Kanon ins Repo, Sidecars, permissions.yaml, acl-rules.yaml — 2026-09-05
- [x] 2026-Projektvorschlag IP-2026-02 als Demo-Fall — 2026-09-05
