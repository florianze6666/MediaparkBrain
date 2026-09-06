---
expert_role: "CFO / Controlling-Agent"
bewertungslogik: "Bewertungslogik_Experten-Agent.md"
information_source: "project_proposals/*.md only (corpus excluded — proposals reference a different fictional company than the Lahnberg Thermotechnik corpus)"
evaluated_projects:
  - m-companion
  - m-invoice-coni-company1
  - m-invoice-coni-company2
  - max-marketing-automation
date: 2026-09-05
---

# CFO-Bewertung: Projektportfolio

Bewertung der vier vorgeschlagenen Projekte aus Sicht des **CFO-/Controlling-Agenten**
(Rollenkriterien gemäß PLAN.md §6.2), nach der in
[Bewertungslogik_Experten-Agent.md](../Bewertungslogik_Experten-Agent.md)
definierten allgemeinen Bewertungslogik.

**Informationsgrundlage:** Ausschließlich die jeweiligen Dateien in `project_proposals/`.
Der `corpus/`-Wissensbestand (Lahnberg Thermotechnik GmbH) wurde bewusst **nicht**
herangezogen, da die Projektvorschläge ein anderes, nicht näher benanntes fiktives
Unternehmen ("Company 1" / "Company 2") betreffen und keine Verbindung zur
Lahnberg-Thermotechnik-Wissensbasis erkennbar ist.

---

## M:COMPANION

*Quelle: [project_proposals/m-companion.md](../project_proposals/m-companion.md)*

**Status:** BEWERTET
**Score:** 8/10

**Begründung:**
Der Business Case ist finanziell stark: ROI 3,16, Payback ≈ 20 Monate, ab Jahr 2
durchgehend positive Discounted EVA. Kosten- und Nutzenpositionen sind vollständig und
granular aufgeschlüsselt (6 One-off-, 3 Recurrent-Positionen; 5 benannte
Umsatz-/Einsparungstreiber). Der Nutzen hängt jedoch an einer Adoptionsannahme (80 %
Nutzung der Einkaufsliste), was ein moderates Realisierungsrisiko darstellt.

**Entscheidungsrelevanter Hinweis:**
Budget-Fit (verfügbares Budget/Budgetgrenzen) und Vendor-Lock-in-Risiko sind in den
Quelldokumenten nicht angegeben und daher nicht in diesen Score eingeflossen.

---

## M:INVOICE – CONI (Company 1)

*Quelle: [project_proposals/m-invoice-coni-company1.md](../project_proposals/m-invoice-coni-company1.md)*

**Status:** BEWERTET
**Score:** 7/10

**Begründung:**
Solider, aber weniger starker Business Case als M:Companion: ROI 2,51, Payback ≈ 23
Monate, durchgehend positive EVA ab Jahr 2. Kosten- und Nutzenaufstellung ist vollständig
granular. Etwas geringere Kapitalrendite und längerer Payback als die anderen drei
Projekte mindern die Priorisierungsstärke leicht.

**Entscheidungsrelevanter Hinweis:**
Budget-Fit und Vendor-Lock-in-Risiko fehlen in den Quelldokumenten.

---

## M:INVOICE – CONI (Company 2)

*Quelle: [project_proposals/m-invoice-coni-company2.md](../project_proposals/m-invoice-coni-company2.md)*

**Status:** BEWERTET
**Score:** 6/10

**Begründung:**
Gleiches Produkt- und Nutzenprofil wie die Company-1-Variante, jedoch höhere
Gesamtkosten (1.487 T€ vs. 1.315 T€) bei identischem Nutzen, wodurch ROI (2,33) und
Payback (≈ 24 Monate) schwächer ausfallen. Kosten-/Nutzenpositionen sind vollständig
dokumentiert.

**Entscheidungsrelevanter Hinweis:**
Beide CONI-Varianten tragen dieselbe Projekt-Nummer (BC-2026-0412.1) und nahezu
identischen Charter-Text — aus CFO-Sicht sollte vor einer Portfolio-Entscheidung geklärt
werden, ob dies zwei getrennt zu finanzierende Vorhaben sind oder eine Dopplung.
Budget-Fit und Vendor-Lock-in-Risiko fehlen zudem in den Quelldokumenten.

---

## MAX – Marketing Automation

*Quelle: [project_proposals/max-marketing-automation.md](../project_proposals/max-marketing-automation.md)*

**Status:** BEWERTET
**Score:** 9/10

**Begründung:**
Mit Abstand der stärkste Business Case: ROI 8,64, Payback ≈ 16 Monate, größter
absoluter Nutzen (10,23 Mio. € über 10 Jahre) und höchste kumulierte Discounted EVA
(4,32 Mio. €) aller vier Projekte. Kosten und Nutzen sind vollständig granular
aufgeschlüsselt.

**Entscheidungsrelevanter Hinweis:**
Budget-Fit und Vendor-Lock-in-Risiko fehlen in den Quelldokumenten. Zudem ist der im
Fließtext beschriebene Länder-Rollout-Plan inkonsistent zur "Affected Countries"-Liste
im Charter-Kopf (siehe Projektdokument) — finanziell nicht relevant, aber als
Klarstellungsbedarf zu vermerken.

---

## Zusammenfassung

| Projekt | Status | Score | ROI | Payback |
|---|---|---:|---:|---:|
| M:COMPANION | BEWERTET | 8/10 | 3,16 | ≈ 20 Monate |
| M:INVOICE – CONI (Company 1) | BEWERTET | 7/10 | 2,51 | ≈ 23 Monate |
| M:INVOICE – CONI (Company 2) | BEWERTET | 6/10 | 2,33 | ≈ 24 Monate |
| MAX – Marketing Automation | BEWERTET | 9/10 | 8,64 | ≈ 16 Monate |

Alle vier Projekte waren aus CFO-Sicht bewertbar (Kosten, Nutzen, ROI, Payback, EVA
vollständig vorhanden). Kein Projekt musste als **INFORMATION FEHLT** eingestuft
werden — Budget-Fit und Vendor-Lock-in fehlen zwar durchgängig, wurden aber als
nicht-blockierende Hinweise behandelt, da die übrigen CFO-Kernkriterien (Kosten, Nutzen,
Business-Case-Kennzahlen) vollständig und belastbar vorlagen.

**Gesamtscore (Kumulierungslogik §16, MVP mit einem Experten):** Da bislang nur der
CFO-Agent bewertet hat, entspricht der "Gesamtscore" je Projekt aktuell dem
Einzel-CFO-Score. Sobald weitere Experten-Agenten (Betriebsrat, IT/Security,
CEO/Strategie) bewerten, ist der arithmetische Durchschnitt aller gültigen Scores gemäß
§16 zu bilden.
