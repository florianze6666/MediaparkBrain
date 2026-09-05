---
doc_id: LTT-20260305-PEO-01
titel: "Projektvorschlag IP-2026-02: KI-Wissensassistent für Projektdokumentation und Projektkommunikation"
dokumenttyp: Projektvorschlag
datum: 2026-03-05
verfasser: Gerd Sattler
rolle: Leiter Project Excellence Office
organisationseinheit: PEO
empfaenger: [Geschäftsführung, Portfolio-Board, Gesamtbetriebsrat]
projekt: IP-2026-02
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit, projektintern, management]
ablageort: projektlaufwerk
---

# Projektvorschlag IP-2026-02

**An:** Geschäftsführung, Portfolio-Board; nachrichtlich Gesamtbetriebsrat (Unterrichtung nach BV-2023-01)
**Von:** Gerd Sattler, Leiter Project Excellence Office; Mitzeichnung Dr. Philipp Nowak (CIO)
**Datum:** 5. März 2026
**Einstufung:** intern
**Betreff:** Einführung eines KI-gestützten Wissensassistenten mit Zugriff auf Projektlaufwerk, SharePoint-Bibliotheken, Mailarchiv und Teams

## 1. Projektname

KI-Wissensassistent LTT (Arbeitstitel „Wissensassistent"), Projektnummer IP-2026-02.

## 2. Beschreibung des Vorhabens

Aufbau eines unternehmensinternen Wissensassistenten auf Basis eines RAG-Verfahrens (Retrieval Augmented Generation). Der Assistent durchsucht die bestehenden Ablagen — Projektlaufwerk, SharePoint-Bibliotheken der Bereiche, QM-Lenkung, IT-Dokumentation, Einkauf, Mailarchiv und Teams-Kanäle — und beantwortet Fragen von Projektleitern, Engineering und Führungskräften mit Quellenangabe. Neue Dokumente werden fortlaufend eingelesen. Zugriffe folgen den bestehenden Berechtigungen der Ablagen: Wer ein Dokument im SharePoint nicht öffnen darf, bekommt es auch über den Assistenten nicht.

Zwei Umsetzungsoptionen werden parallel geprüft:

- **Option A:** SaaS-Plattform eines Anbieters mit EU-Hosting, Anbindung an Microsoft 365 über Standardkonnektoren (Angebot vom 12.02.2026, Anbieter im Auswahlverfahren, zwei Kandidaten).
- **Option B:** Eigenentwicklung auf einer LLM-API mit EU-Region, betrieben im bestehenden Azure-Mandanten.

Der Vorschlag empfiehlt Option A für den Piloten und behält Option B als Rückfalloption.

## 3. Zielsetzung

1. Die Suchzeit bei Projektübernahmen und Angebotsvorbereitung um mindestens 25 Prozent senken (Ausgangswert nach Erhebung PEO Q4 2025: durchschnittlich 4,2 Stunden je Woche und Wissensarbeiter).
2. Geschäftskritisches Wissen aus Einzeldateien und Mailverläufen auffindbar machen — Fortsetzung der Excel Amnesty.
3. Entscheidungsvorlagen für das Portfolio-Board mit belegbaren Quellen aus der eigenen Historie unterlegen.

## 4. Fachlicher und organisatorischer Nutzen

- Projektleiter finden Vorgängerprojekte, Lessons Learned und Lieferantenbewertungen ohne Umweg über Kollegen.
- Engineering findet Design-Freeze-Entscheidungen und Änderungshistorien über Systemgrenzen hinweg (PLM, ERP, Netzlaufwerk).
- Das Portfolio-Board erhält Vorlagen mit Verweisen auf frühere Entscheidungen und deren Ausgang.
- Onboarding neuer Projektleiter verkürzt sich; die Abhängigkeit von einzelnen Wissensträgern sinkt.

## 5. Betroffene Geschäftsprozesse

Projektabwicklung (Übernahme, Statusberichte, Lessons Learned), Angebotsreview, Portfolio- und Investitionsentscheidungen, Lieferantenbewertung, Dokumentenlenkung nach QM.

## 6. Betroffene Organisationseinheiten

Project Excellence Office, alle vier Business Units, Central Engineering, IT, Einkauf, Controlling, Vertrieb. Betriebsrat und Datenschutz sind nach BV-2023-01 zu beteiligen.

## 7. Business Case

Siehe Anlage `2026-03-05-business-case-ki-wissensassistent.xlsx` (Kurzfassung als Markdown daneben). Kernannahmen: 250 Nutzer im Pilot- und Rollout-Umfang, 4,2 Stunden Suchaufwand je Woche, Reduktion um 25 Prozent, kalkulatorischer Stundensatz 62 EUR, 46 produktive Wochen.

## 8. Erwartete Kosten

| Position | Einmalig | Jährlich |
|---|---:|---:|
| Implementierung extern (Anbindung, Berechtigungskonzept, Pilot) | 260.000 EUR | |
| Interner Aufwand (IT, PEO, Key User, Datenschutz) | 160.000 EUR | |
| Plattformlizenz Option A (250 Nutzer) | | 96.000 EUR |
| Betrieb, Support, Modellkosten | | 55.000 EUR |
| Schulung und Change | 35.000 EUR | 10.000 EUR |
| **Summe** | **455.000 EUR** | **161.000 EUR** |

Gesamtkosten über drei Jahre: rund 938.000 EUR. Die Schwelle für eine Investitionsvorlage mit NPV und IRR (2 Mio EUR) wird nicht erreicht.

## 9. Erwarteter wirtschaftlicher Nutzen

Eingesparte Suchzeit: 250 Nutzer × 4,2 h × 25 % × 46 Wochen × 62 EUR = rund 748.000 EUR je Jahr. Kumuliert über drei Jahre rund 2,24 Mio EUR gegen Kosten von 0,94 Mio EUR. Payback rechnerisch im zweiten Jahr. Nicht monetär bewertet: geringere Fehlerquote bei Angeboten, kürzeres Onboarding.

## 10. Geplante Laufzeit und Einführungszeitraum

Beschluss April 2026. Pilot Juli bis Dezember 2026 mit PEO und BU Industrial Heat Systems (rund 60 Nutzer). Evaluation nach BV-2023-01 im Januar 2027. Rollout auf 250 Nutzer ab Februar 2027.

## 11. Bekannte technische Abhängigkeiten

Microsoft 365 (SharePoint, Teams, Exchange) als Quelle; Entra ID für Identität und Gruppen; Digital Core (SAP Finance) für Projektkennzahlen nur lesend über bestehende BI-Schnittstelle; Konnektor zum Projektlaufwerk. Die Berechtigungen der Quellen müssen maschinell lesbar und im Assistenten durchgesetzt sein — das ist Voraussetzung für den Pilotstart, nicht Ergebnis des Piloten.

## 12. Bekannte organisatorische Abhängigkeiten

Rahmenvereinbarung BV-2023-01 (Systembeschreibung, Datenkatalog, Teilvereinbarung vor Produktivsetzung, Evaluation nach zwölf Monaten). BV-2020-02 zur Kollaborationsplattform schließt jede Auswertung personenbezogener Nutzungsdaten aus — der Assistent darf keine Nutzungsstatistik je Person erzeugen. Beteiligung der Datenschutzbeauftragten. Lieferantenbewertung nach NIS2-Vorbereitung durch die Informationssicherheit. Begrenzung auf drei Top-Priority-Change-Initiatives je Business Unit („Stabilisieren vor transformieren").

## 13. Risikoanalyse

Siehe Anlage `2026-03-05-risikoregister-ki-wissensassistent.md`. Die drei höchsten Risiken: fehlerhafte Berechtigungsdurchsetzung (Datenleck über den Assistenten), Mitbestimmungskonflikt über Nutzungsdaten, Anbieterabhängigkeit bei Option A.

## 14. Begründung

Die Erhebung zum Wissensmanagementproblem 2025 hat gezeigt, dass Projektwissen auf mindestens vier Systeme verteilt ist und bei Übernahmen nicht auffindbar war. Die Excel Amnesty hat über 430 geschäftskritische Einzeldateien sichtbar gemacht, deren Inhalt weiterhin nur den Ownern bekannt ist. LTT hat mit generativer KI keine eigene Erfahrung; die Marktbeobachtung der IT vom September 2025 empfiehlt einen begrenzten Piloten mit klarem Berechtigungskonzept, bevor ein breiter Einsatz erwogen wird. Dieser Vorschlag folgt dieser Empfehlung.

## 15. Anbieter-, Produkt- und Projektinformationen

Zwei SaaS-Anbieter im Auswahlverfahren, beide mit EU-Hosting und ISO-27001-Nachweis nach eigener Angabe; Prüfung durch die Informationssicherheit steht aus. Referenzen aus dem Maschinenbau liegen für einen der beiden vor. Angebotsunterlagen im Einkaufsordner unter IP-2026-02.
