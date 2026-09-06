# Testdaten: 30 fiktive IT-Projektanträge (VELTRAX Group SE)

Alle 30 Dateien in diesem Ordner sind **erfunden** (Konzern, Gesellschaften, Personen, Zahlen) und dienen als Testkorpus
für Completeness Check, Dublettenerkennung und Bewertung. Aufbau angelehnt an die vier Beispiel-Proposals (Project Charter + IT Business Case).

- Generiert am 2026-09-06, Formate: 10× DOCX (Project Charter), 10× XLSX (IT Business Case), 10× PDF (Formular PA-03)
- Business-Case-Logik: Capex linear über 5 Jahre ab Go-Live abgeschrieben (10 % Anlauf im Startjahr), Nutzen 50 % im Go-Live-Jahr, danach 100 %,
  Tax 26,9 %, WACC 5,8 %, ROI = EBIT gesamt / Kosten gesamt, Payback = Monate bis kumulierter EBIT ≥ 0.
- Dateinamen absichtlich uneinheitlich (verschiedene Präfixe, Versionskürzel, Kopien) wie in realen Ablagen.

## Lösungsschlüssel: eingebaute Fehler

| # | Code | Datei | Format | Eingebaute Fehler |
|---|------|-------|--------|-------------------|
| 1 | ORBIT | `__Project_Charter_ORBIT_GroupFinance.docx` | DOCX | vollständig, ohne gezielte Fehler (kann trotzdem Lücken/Unschärfen enthalten wie echte Anträge) |
| 2 | PULSE | `Business_Case_PULSE_GroupHR_final_final (2).xlsx` | XLSX | Summary: hart codierter Total-Wert »Costs« weicht um 40.000 € von der Zeilensumme ab (Formel vs. Zahl); Dateiname »final_final (2)«. |
| 3 | BEACON | `Projektantrag_BEACON_GroupITSecurity.docx` | DOCX | Go-Live FY 2026 liegt VOR Start FY 2027; Länderangabe unspezifisch (»alle Landesgesellschaften«). |
| 4 | VANTAGE | `Antrag_VANTAGE.pdf` | PDF | Länder im Kopf (CORP; DE; FR; ES) widersprechen dem Rollout-Plan im Text (DE, NL, PL, CZ). |
| 5 | KEYSTONE | `__Business_Case_KEYSTONE_GroupITSecurity.xlsx` | XLSX | vollständig, ohne gezielte Fehler (kann trotzdem Lücken/Unschärfen enthalten wie echte Anträge) |
| 6 | NEXUS | `Business_Case_NEXUS_CorporateIT.xlsx` | XLSX | Projektnummer BC-2026-0533.1 doppelt vergeben (identisch mit CATALYST). |
| 7 | MERIDIAN | `Projektantrag_MERIDIAN_CorporateCommunications_Entwurf.docx` | DOCX | Sponsor leer, PM »tbd«, Metriken nicht messbar (»soll besser werden«), Geschäftsprozesse/Org-Abhängigkeiten/Risiken leer; Dateiname »_Entwurf«. |
| 8 | SUMMIT | `Antrag_SUMMIT_v0.3_DRAFT.pdf` | PDF | Als ENTWURF v0.3 markiert (nicht freigegeben); Finanzübersicht mischt T€ und € (z. B. »450 €« statt »450 T€«). |
| 9 | CATALYST | `__Business_Case_CATALYST_SharedServicesFinance.xlsx` | XLSX | Projektnummer doppelt (siehe NEXUS); Nutzen in allen Jahren 0, trotzdem ROI 2,41 und Payback 18 Monate ausgewiesen. |
| 10 | HARBOR | `Project_Charter_HARBOR_Logistics.docx` | DOCX | Antragsdatum 31.02.2026 (ungültig); Copy-Paste-Bezug auf »Veltrax Retail/Duisburg« in einem Logistics-Antrag für PL/CZ. |
| 11 | LATTICE | `Project_Charter_LATTICE_CorporateIT.pdf` | PDF | vollständig, ohne gezielte Fehler (kann trotzdem Lücken/Unschärfen enthalten wie echte Anträge) |
| 12 | SENTRY | `Antrag_SENTRY.pdf` | PDF | Kein Business Case im Dokument, nur Verweis auf Anhang »__Business_Case_SENTRY_Corporate.xlsx«, der nicht existiert. |
| 13 | TRIDENT | `__Business_Case_TRIDENT_GroupProcurement.xlsx` | XLSX | EBIT-Zeile enthält #REF! (2029/2030); Payback »n/a«; Kennzahlen dadurch nicht nachvollziehbar. |
| 14 | QUARTZ | `Project_Charter_QUARTZ_Industrial.docx` | DOCX | vollständig, ohne gezielte Fehler (kann trotzdem Lücken/Unschärfen enthalten wie echte Anträge) |
| 15 | ECHO | `Project_Charter_ECHO_FinancialServices.pdf` | PDF | Deutsch/Englisch gemischt; Nutzenanteile summieren sich auf 115 %. |
| 16 | GRANITE | `IT_Business_Case_GRANITE.xlsx` | XLSX | vollständig, ohne gezielte Fehler (kann trotzdem Lücken/Unschärfen enthalten wie echte Anträge) |
| 17 | FLUX | `Projektantrag_neu.docx` | DOCX | Titel ist Platzhalter »[Projektname eintragen]«, Projektnummer BC-2026-0000.0, Dateiname »Projektantrag_neu.docx«; Projektname FLUX nur im Fließtext. |
| 18 | HALO | `PA-03_HALO_Retail.pdf` | PDF | vollständig, ohne gezielte Fehler (kann trotzdem Lücken/Unschärfen enthalten wie echte Anträge) |
| 19 | TANGENT | `BC_2026_TANGENT_CorporateIT.xlsx` | XLSX | Business Case über alle Jahre negativ (EBIT < 0, Hardware 2,6 Mio. €), im Text und in »Recommendation« trotzdem »positiver Business Case, Freigabe empfohlen«. |
| 20 | SPARK | `PA_2026_SPARK_CorporateIT.docx` | DOCX | Risikoliste enthält Lorem-ipsum-Rest; Vertraulichkeit leer; Anbieter (Copilot Studio/Azure OpenAI) genannt, aber SaaS-/Lizenzkosten 0. |
| 21 | ANVIL | `Projektantrag_ANVIL_Industrial.pdf` | PDF | vollständig, ohne gezielte Fehler (kann trotzdem Lücken/Unschärfen enthalten wie echte Anträge) |
| 22 | RELAY | `Business_Case_RELAY_Logistics.xlsx` | XLSX | Sponsor auf Sheet »Summary« (»Dr. Kerstin Albrecht (COO Logistics)«) und »Project Description« (»Kristin Albrecht (COO Logistik)«) unterschiedlich geschrieben. |
| 23 | MOSAIC | `Projektantrag_MOSAIC_CorporateIT.docx` | DOCX | vollständig, ohne gezielte Fehler (kann trotzdem Lücken/Unschärfen enthalten wie echte Anträge) |
| 24 | CANOPY | `Antrag_CANOPY.pdf` | PDF | Go-Live FY 2025 liegt vor Antragsdatum 2026 und vor Start 2026; im Text »STRENG VERTRAULICH«, Feld Vertraulichkeit aber leer. |
| 25 | LUMEN | `__Business_Case_LUMEN_CorporateIT.xlsx` | XLSX | vollständig, ohne gezielte Fehler (kann trotzdem Lücken/Unschärfen enthalten wie echte Anträge) |
| 26 | VERTEX | `Project_Charter_VERTEX_Retail.docx` | DOCX | »Kick-off war bereits Q3/2025« widerspricht Start FY 2026; Recurrent-Kosten enden 2029 mit Begründung »Lizenz entfällt, da abgeschrieben« – bei SaaS unplausibel. |
| 27 | PIVOT | `Project_Charter_PIVOT_Logistics.pdf` | PDF | vollständig, ohne gezielte Fehler (kann trotzdem Lücken/Unschärfen enthalten wie echte Anträge) |
| 28 | OASIS | `IT_Business_Case_OASIS.xlsx` | XLSX | Währung auf Summary »USD«, Upload-Sheet: 2026-Spalte USD, ab 2027 EUR – Zahlen nicht vergleichbar. |
| 29 | CINDER | `__Project_Charter_CINDER_GroupFinance.docx` | DOCX | vollständig, ohne gezielte Fehler (kann trotzdem Lücken/Unschärfen enthalten wie echte Anträge) |
| 30 | HALO-FS | `__Business_Case_HALO_FinancialServices_Kopie.xlsx` | XLSX | Nahezu identische Kopie von HALO (Retail) durch Financial Services mit gleicher Projektnummer BC-2026-0590.1, abweichenden Nutzen-Zahlen und Retail-Org-Einheiten im FS-Antrag; Dateiname »_Kopie«. |

## Querbezüge (absichtlich)

- Abhängigkeitsnetz: ORBIT ← MOSAIC; HALO/RELAY ← NEXUS; BEACON ← SENTRY; SUMMIT ← LATTICE/KEYSTONE; LUMEN ← SUMMIT; ANVIL ← QUARTZ/VANTAGE; ECHO/HALO ← VERTEX.
- Ressourcenkonflikt SAP CoE: ORBIT, CINDER, CATALYST, TRIDENT, HARBOR greifen auf dasselbe Team zu.
- Zwei Sponsoren tragen je mehrere Anträge (CFO: ORBIT, CATALYST, CANOPY, CINDER; CIO: NEXUS, FLUX, TANGENT, SPARK, OASIS).

Generator: `gen_proposals.py` (python-docx, openpyxl, LibreOffice für PDF) – nicht Teil des Repos.
