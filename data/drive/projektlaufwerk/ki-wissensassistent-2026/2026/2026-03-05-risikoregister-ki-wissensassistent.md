---
doc_id: LTT-20260305-PEO-02
titel: "Risikoregister IP-2026-02 KI-Wissensassistent"
dokumenttyp: Risikoregister
datum: 2026-03-05
verfasser: Gerd Sattler
rolle: Leiter Project Excellence Office
organisationseinheit: PEO
empfaenger: [Geschäftsführung, Portfolio-Board, Gesamtbetriebsrat]
projekt: IP-2026-02
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit, projektintern]
ablageort: projektlaufwerk
---

# Risikoregister IP-2026-02, Stand 5. März 2026

Skala: Eintrittswahrscheinlichkeit und Auswirkung je 1 (gering) bis 5 (hoch).

| Nr | Risiko | W | A | Maßnahme | Owner |
|---|---|:-:|:-:|---|---|
| R-01 | Assistent gibt Inhalte aus, die der Fragende in der Quelle nicht sehen dürfte (fehlerhafte Berechtigungsdurchsetzung) | 3 | 5 | Berechtigungen beim Einlesen übernehmen, Vorfilter vor der Suche, Freigabe der Informationssicherheit vor Pilotstart, Leak-Tests als Abnahmekriterium | Nowak, Bruckner |
| R-02 | Mitbestimmungskonflikt: Nutzungsdaten des Assistenten sind personenbeziehbar (vgl. CRM 2023, Dashboard 2024) | 4 | 4 | Keine personenbezogene Nutzungsstatistik; Datenkatalog vor Pilot; Teilvereinbarung nach BV-2023-01 | Sattler, Kirchner |
| R-03 | Abhängigkeit vom SaaS-Anbieter (Option A), Preissteigerung nach Pilot | 3 | 3 | Exit-Klausel, Datenexport im Vertrag, Option B als Rückfall | Ehlers |
| R-04 | Antworten enthalten veraltete Regelungen (z. B. Policies vor NIS2-Vorbereitung) | 4 | 3 | Datum und Gültigkeit je Treffer anzeigen, Widerspruchshinweis, QM-Lenkung als bevorzugte Quelle | Hoffmann |
| R-05 | Übertragung interner Dokumente an einen LLM-Dienst außerhalb der EU | 2 | 5 | Nur EU-Hosting, Auftragsverarbeitung, Prüfung durch Datenschutz | Kroll |
| R-06 | Geringe Nutzung, weil Antworten nicht vertrauenswürdig erscheinen | 3 | 3 | Quellenpflicht je Antwort, Pilot mit Key Usern, Feedbackschleife | Sattler |
| R-07 | Belastung der Key User parallel zu Digital Core (vgl. Atlas Review 2024) | 4 | 3 | Pilot nur mit PEO und einer BU; Zeitbudget je Key User | Sattler |
| R-08 | Schattenwissen wird nicht erfasst, weil Dateien außerhalb der Ablagen liegen | 3 | 2 | Kopplung an die Excel-Governance, Owner-Meldung | Nowak |
