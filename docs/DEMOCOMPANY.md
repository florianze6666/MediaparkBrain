# Demo-Firma: Lahnberg Thermotechnik GmbH & Co. KG (LTT)

> **Status:** v0.1, 2026-09-05, Anselm. Beschreibt die Situation, in der das System demonstriert
> wird. **Dieses Dokument darf sich ändern** — Personen, Gruppen und Ablageorte sind Daten
> (`data/permissions.yaml`, `data/drive/*/.acl.yaml`), das Berechtigungskonzept ist davon
> unabhängig.

## 1. Woher die Firma kommt

Korpus und Kanon stammen aus dem Repository
[Eckhard-Siegmann/startplatz_hackathon](https://github.com/Eckhard-Siegmann/startplatz_hackathon)
(MIT-Lizenz, Kopie unter `data/LICENSE-democompany.txt`, Quell-Commit in
`data/DEMOCOMPANY-SOURCE.md`, Aktualisierung per `scripts/sync_democompany.sh`).

Es ist eine vollständig fiktive Firma: Wärmepumpen- und Verdichtertechnik, Stammsitz Kassel,
Werk Eisenach (2018 übernommen), Auslandsstandorte Brno, Rotterdam, Houston, Shanghai; 720
Mitarbeiter (2025); seit 2022 zu 60 Prozent im Besitz einer Industrieholding mit Beirat. Die
Wissensbasis umfasst **136 interne Dokumente von 2011 bis 2025** (Stand des Snapshots, der
Generator läuft weiter), verfasst aus der Perspektive ihres jeweiligen Datums — ein Dokument
von 2023 weiß nichts vom Scheitern des ERP-Programms 2024.

Die Firmenchronik und die Register (Personen, Projekte, Systeme, Lieferanten, Kunden,
Betriebsvereinbarungen, Organigramme je Jahr) liegen unter `data/canon/`. **Der Kanon ist
Ground Truth für uns, nicht Teil des RAG.** Er steht in keinem Ablageort und wird nicht
indexiert.

Softwareprodukte tragen reale Namen (proALPHA, SAP, Microsoft Teams …), damit der IT-Agent
extern recherchieren kann. Die LTT-Erfahrungen damit sind erfunden.

## 2. Die neun Ablageorte — unsere Domänen

Jedes Korpusdokument liegt in genau einem Ablageort. Das ist die Zugriffsdomäne.

| Ablageort (Ordner) | Domäne | Was liegt dort | Dokumente | Site-Mitglieder | Owner |
|---|---|---|---:|---|---|
| `sharepoint_gf/` | `gf` | Entscheidungsvorlagen, Vorstandsmemos, Beiratsunterlagen, Organigramme, Policies | 34 | `grp-management` | P-002 Kessler |
| `sharepoint_finance/` | `finance` | Budgetübersichten, Investitionsanträge, Controlling | 11 | `grp-finance`, `grp-gf` | P-003 Heine |
| `sharepoint_hr/` | `hr` | Personalplanung, Einstellungsbremse, Qualifizierung | 9 | `grp-hr`, `grp-gf` | P-032 Kirchner |
| `br_ablage/` | `betriebsrat` | Betriebsratsinformationen, interne Willensbildung | 5 | `grp-betriebsrat` | P-061 Marquardt |
| `it_doku/` | `it` | Architektur, Softwareportfolio, NIS2-Vorbereitung, Excel Amnesty | 19 | `grp-it`, `grp-management`, `grp-projekte` | P-021 Nowak |
| `einkauf_scm/` | `einkauf` | Beschaffungsstrategie, Lieferantenbewertungen, Stammlisten | 10 | `grp-einkauf`, `grp-management`, `grp-projekte` | P-024 Damm |
| `qm_lenkung/` | `qm` | SOPs, Arbeitsanweisungen, Auditberichte | 14 | `grp-qm`, `grp-management`, `grp-projekte`, `grp-it`, `grp-engineering` | P-031 Hoffmann |
| `projektlaufwerk/` | `projekte` | Projektaufträge, Risikoregister, Steering-Protokolle, Lessons Learned, **der 2026-Vorschlag** | 25 + 3 | `grp-projekte`, `grp-management`, `grp-finance`, `grp-it` | P-040 Sattler |
| `mailarchiv/` | `mail` | Eskalationsmails | 9 | **niemand** — nur Verfasser und Empfänger | P-021 Nowak |

Dazu `_brain/` für zurückgeschriebenes Agentenwissen (`ARCHITEKTUR-RAG.md` §10).

## 3. Der Dokumentkopf — und was der Ingest daraus macht

Jedes Dokument trägt einen YAML-Kopf. Vier Felder entscheiden über Rechte:

```yaml
vertraulichkeit: C-Level                    # intern | C-Level | Betriebsrat-intern
informationsdomaene: [c-level-beirat]       # was der Verfasser wusste
empfaenger: [Beirat]                        # Verteiler
ablageort: sharepoint_gf                    # = Ordner
```

Die Ableitung steht als Konfiguration in `data/acl-rules.yaml` und als Regel in
`BERECHTIGUNGSKONZEPT.md` §6. Kurz:

| Kopf sagt | Ergebnis |
|---|---|
| `vertraulichkeit: intern` | lesbar für die Site-Mitglieder des Ablageorts |
| `vertraulichkeit: C-Level` | `confidential`, nur `grp-c-level` (Geschäftsführung + Beirat) |
| `vertraulichkeit: Betriebsrat-intern` | `confidential`, nur `grp-betriebsrat` |
| `informationsdomaene` enthält `hr-sensitiv` | **`restricted`** — namentlich, Existenz verborgen (1 Dokument) |
| … enthält `it-security-restricted` | `confidential`, nur `grp-it-security` (2 Dokumente) |
| `informationsdomaene` ist **genau** `[unternehmensweit]` und `intern` | **veröffentlicht** — firmenweit lesbar (27 Dokumente: Organigramme, Policies, SOPs) |
| `empfaenger` / `verfasser` | wer im Verteiler steht, darf lesen — auch über Site-Grenzen |
| `ablageort: mailarchiv` | ausschließlich Verfasser und Empfänger |

Verteilung im Snapshot: 18 × C-Level, 5 × Betriebsrat-intern, 1 × hr-sensitiv, 2 × it-security-
restricted, 9 Mails, 27 veröffentlicht, Rest `intern` in der jeweiligen Site.

## 4. Personen und Gruppen

Vollständig in `data/permissions.yaml`, Herkunft `data/canon/registry/people.md`. Die
Personen, die in der Demo sprechen:

| P-ID | Person | Rolle | Vertreten durch Agent |
|---|---|---|---|
| P-002 | Dr. Eva Kessler | CEO (seit 10/2022) | `agent:ceo` |
| P-003 | Markus Heine | CFO (seit 10/2022) | `agent:cfo` |
| P-021 | Dr. Philipp Nowak | CIO (seit 04/2023); mit P-023 Bruckner (Informationssicherheit) | `agent:it` |
| P-061 | Silke Marquardt | Vorsitzende Gesamtbetriebsrat | `agent:betriebsrat` |
| P-040 | Gerd Sattler | Leiter Project Excellence Office — **reicht den Vorschlag ein** | — |
| P-032 | Susanne Kirchner | Leiterin Personal — Owner `hr`, gibt HR-Eskalationen frei | — |
| P-075 | Sabine Kroll | Datenschutzbeauftragte | — |
| P-900 | Max Mustermann | Projektingenieur ohne Leitungsfunktion — die Persona für „normaler Mitarbeiter fragt das Brain" | — |

Ein Agent **vertritt** eine Person (`represents: P-003`) und erbt exakt deren Gruppen. Damit ist
„der CFO-Agent darf, was der CFO darf" keine Konfiguration, sondern eine Konsequenz.

Wichtige Gruppen: `grp-gf` (Kessler, Heine, Mahlberg), `grp-c-level` (GF + Beirat),
`grp-management` (GF, BU-Leitungen, Zentralfunktionen), `grp-betriebsrat` (Marquardt, Rühl,
Kaya, Ohlert), `grp-it-security` (Nowak, Bruckner), `grp-hr-leitung` (Kirchner), `grp-alle`.

## 5. Was das für die vier Agenten heißt

| Agent | Sieht | Sieht nicht — und das ist richtig so |
|---|---|---|
| `ceo` (Kessler) | `gf` inkl. C-Level, `finance` inkl. C-Level, `it`, `einkauf`, `qm`, `projekte`, `hr` (intern) | `betriebsrat/`, `hr-sensitiv`, `it-security-restricted` im Detail, fremde Mails |
| `cfo` (Heine) | wie CEO, dazu `finance` als Site-Mitglied | wie CEO |
| `it` (Nowak) | `it` inkl. Security-Details, `qm`, `projekte`, `gf` (intern), Mails an ihn | C-Level-Vorlagen, `finance`, `hr`, `betriebsrat/` |
| `betriebsrat` (Marquardt) | `betriebsrat/`, alles Veröffentlichte, Dokumente mit dem Gesamtbetriebsrat im Verteiler (der 2026-Vorschlag!) | `gf`, `finance`, `hr`, `it`, `projekte` als Sites — **eskaliert**, was sie braucht |

Das ist der Demo-Kern: Der Betriebsrat-Agent hat die *schmalste* Sicht und den *größten*
Bedarf an Eskalation. Genau so ist Mitbestimmung.

## 6. Der Fall 2026: IP-2026-02 KI-Wissensassistent

Der Projektvorschlag, den die vier Agenten bewerten, liegt unter
`data/drive/projektlaufwerk/ki-wissensassistent-2026/2026/` — Vorschlag (15 Pflichtfelder nach
`PLAN.md` §2), Risikoregister, Business Case (`.md` + `.xlsx`). Verfasser Gerd Sattler (PEO),
Mitzeichnung Nowak, Verteiler GF, Portfolio-Board, Gesamtbetriebsrat.

Warum dieses Projekt: Der Kanon führt „generative KI mit Zugriff auf Projektkommunikation" als
**bewusste Leerstelle** (`data/canon/blind_spots.md`, BS-01) — LTT kennt das Thema, hat aber
keine eigene Erfahrung. Die Agenten müssen genau diese Unterscheidung treffen. Und die
Historie liefert alles, was sie brauchen:

| Agent | findet | und schließt daraus |
|---|---|---|
| Betriebsrat | BV-2023-01 (Rahmenvereinbarung IT-Systeme), BV-2020-02 (kein Auswerten von Nutzungsdaten), Konflikte CRM 2023 und Dashboard 2024 | Teilvereinbarung vor Pilot, Datenkatalog, keine Nutzungsstatistik je Person; `risk_score` hoch, wenn das im Vorschlag fehlt |
| CFO | Investitionsregel ab 2 Mio (nicht erreicht), Budgetlage nach ONE LTT (19 statt 14,8 Mio), Business-Case-Annahme „25 % Reduktion" ohne Beleg | rechnet Sensitivität nach, prüft gegen Bereichsbudget — braucht dafür `sharepoint_finance` |
| IT | NIS2-Vorbereitung 2025, Cloud-Strategie (BS-07: Kernsysteme nie migriert), Marktbeobachtung generative KI 09/2025, Excel Amnesty | SaaS mit EU-Hosting passt zur Linie; Berechtigungsdurchsetzung ist Pilot-Voraussetzung; Lieferantenprüfung offen |
| CEO | Strategie „Stabilisieren vor transformieren", max. drei Change-Initiativen je BU, Atlas Review (Risiko liegt in der Organisation) | strategisch passend, aber Kapazitätskonflikt mit Digital Core; `strategy_score` hoch, `risk_score` mittel |

Der Zielkonflikt, den der Orchestrator sichtbar macht: CEO und IT sehen Strategiefit und
Machbarkeit, der Betriebsrat sieht den dritten Datenkonflikt in Folge, der CFO glaubt die 25
Prozent nicht.

## 7. Grenzen des Snapshots

- 136 von geplanten 266 Dokumenten; der Generator läuft. `scripts/sync_democompany.sh` holt
  den neuen Stand, unsere Sidecars und 2026-Dokumente bleiben.
- Betriebsvereinbarungen existieren als Register im Kanon, nicht alle als Volltext im Korpus.
  Der Betriebsrat-Agent zitiert dann das Register nicht — er eskaliert oder benennt die Lücke.
- `empfaenger` enthält teils Rollen- oder Einheitsnamen; die Auflösung steht in
  `permissions.yaml` unter `aliases`. Unbekannte Namen werden ignoriert (Deny by default) und
  im Ingest-Log gemeldet.
