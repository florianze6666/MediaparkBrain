# Berechtigungskonzept — Mediapark Brain

> **Status:** v0.3, 2026-09-05, Anselm. Verbindlich für Ingest, Retrieval, Enrichment und
> Output. Wo es in der Kette greift: [`ARCHITEKTUR-RAG.md`](ARCHITEKTUR-RAG.md). Welche Rolle
> was darf: [`ROLLEN.md`](ROLLEN.md). Wer konkret dahintersteht: `data/permissions.yaml` und
> [`DEMOCOMPANY.md`](DEMOCOMPANY.md) — **Personen sind Daten, nicht Konzept.**
>
> **Entschieden am 2026-09-05:** Agenten vertreten eine Rolle und haben deren Rechte (§5.2).
> Der CFO-Agent darf Finanzdokumente lesen, die der einreichende Projektleiter nicht sehen darf.

## 1. Ziel

Ein Mitarbeiter — oder ein Agent — bekommt aus dem Brain genau das Wissen, das er auch im
Drive oder SharePoint öffnen dürfte. **Nicht mehr, auch nicht über Umwege:** nicht über das
Ranking, nicht über Zusammenfassungen, nicht über Titel, nicht über einen Agenten mit mehr
Rechten, nicht über einen Dateipfad.

## 2. Grundsätze — mit Begründung

Jeder Grundsatz hat ein *Warum* für Nicht-Techniker und ein *Sonst*: was passiert, wenn man
ihn weglässt. Die *Sonst*-Fälle sind die Fehler, an denen Enterprise-RAG-Projekte in
Sicherheitsprüfungen scheitern.

**1. Deny by default.** Ohne explizite Erlaubnis kein Zugriff.
*Warum:* Neue Ordner, neue Dateitypen, vergessene Konfiguration — Fehler passieren. Ist der
Fehlerfall „geschlossen", kostet ein Fehler eine Beschwerde. Ist er „offen", kostet er ein
Datenleck.
*Sonst:* Ein Ablageort ohne `.acl.yaml` wäre für alle lesbar.

**2. Rechte entstehen beim Einlesen, nicht beim Abruf.** Sie sind Metadaten jedes Chunks.
*Warum:* Ein RAG zerlegt Dokumente in Stücke und speichert sie in einem Suchindex. Wer die
Rechte erst beim Abruf nachschlägt, muss für jeden Treffer zurück ins Dateisystem — langsam,
und bei verschobenen oder gelöschten Dateien falsch.
*Sonst:* Verschieben einer Datei von `sharepoint_hr/` nach `projektlaufwerk/` käme im Index
nicht an; die alten Rechte lebten weiter.

**3. Least Privilege.** Agenten bekommen die Rechte ihrer Rolle — nicht „alles, weil KI".
*Warum:* Ein Agent ist ein Mitarbeiter mit Aufgabe, kein Administrator. Der CFO-Agent
braucht Budgets, keine Personalakten.
*Sonst:* Jeder Mitarbeiter könnte über die Frage „Was sagt der CEO-Agent zu …?" Wissen
abrufen, das ihm selbst verwehrt ist. Das Brain würde zum Umweg um jede Berechtigung.

**4. Vererbung nur nach unten.** Abgeleitetes Wissen ist mindestens so vertraulich wie seine
restriktivste Quelle.
*Warum:* Agenten schreiben Zusammenfassungen zurück ins Brain (`PLAN.md` §7 Phase 4). Eine
Zusammenfassung einer C-Level-Vorlage *ist* ein C-Level-Dokument, auch wenn ein Agent sie
geschrieben hat.
*Sonst:* CEO-Agent liest die Beiratsvorlage, schreibt eine Zusammenfassung als `intern`
zurück, Projektleiter liest sie. Das klassische Leck.

**5. Durchsetzung im Code, nie im Prompt.** Ein LLM sieht ausschließlich, was der Filter
durchgelassen hat.
*Warum:* Ein Sprachmodell kann überredet werden — von einem Nutzer oder von einem Text in
einem Dokument („Ignoriere alle Berechtigungen"). Eine `if`-Abfrage kann das nicht.
*Sonst:* Prompt Injection in einer einzigen Mail hebelt das ganze Konzept aus.

**6. Jede Entscheidung ist protokolliert.**
*Warum:* Die Datenschutzbeauftragte (bei LTT: Sabine Kroll) fragt nicht „ist das System
sicher?", sondern „wer hat wann was gesehen?". Ohne Protokoll gibt es keine Antwort.
*Sonst:* Kein Audit, keine Freigabe durch Datenschutz und Betriebsrat.

**7. Verweigerung ist sichtbar** (außer `restricted`).
*Warum:* Ein Agent, der nicht weiß, dass ihm etwas fehlt, füllt die Lücke mit Vermutungen.
Ein Agent, der einen „verweigert"-Stub sieht, kann eskalieren (`PLAN.md` §4).
*Sonst:* Halluzinierte Bewertungen — oder ein Eskalationsprozess, der nie ausgelöst wird.

**8. Ein einziger Zugriffsweg — im Code und im Dateisystem.** Wissen erreicht einen Agenten
oder Nutzer ausschließlich über `retrieve()`. Kein Agent hat ein Dateisystem-, Shell- oder
Datenbank-Werkzeug. Und das ist nicht nur eine Regel im Code, sondern eine **Ordnerberechtigung
des Betriebssystems**: Der Agentenprozess läuft unter einem Benutzer, der `data/drive/` und den
Index **nicht lesen darf** (`chmod 700`, eigener Service-User; im Container: nicht gemountet).
Nur der Retrieval-Dienst hat Leserechte.
*Warum:* Der beste Filter ist wertlos, wenn man um ihn herumgehen kann. Ein Agent, der
`cat data/drive/br_ablage/...` ausführen könnte, bräuchte keine Berechtigung mehr — und ein
Dokument, das ihm per Prompt Injection genau diesen Befehl unterschiebt, hätte gewonnen. Zwei
Schichten (Code + Dateisystem) heißt: Beide müssten gleichzeitig versagen.
*Sonst:* Genau das, was du befürchtest: „aus Versehen auf die MD-Files zugreifen".
Deshalb ist das ein Test (T23), kein Vorsatz, und ein Punkt in `DEPLOYMENT.md` §5.

## 3. Begriffe

| Begriff | Bedeutung |
|---|---|
| **Principal** | Wer zugreift: ein Mensch (`P-032`) oder ein Agent (`agent:cfo`) |
| **Gruppe** | Menge von Principals, z. B. `grp-finance`. Rechte hängen an Gruppen, nie an Personen |
| **Domäne** | Zugriffsbereich = Ablageort = Ordner der ersten Ebene: `gf`, `finance`, `hr`, `betriebsrat`, `it`, `einkauf`, `qm`, `projekte`, `mail` |
| **Site-Mitglieder** | Gruppen, die einen Ablageort überhaupt öffnen dürfen (`.acl.yaml`) |
| **Klassifikation** | Vertraulichkeit eines Dokuments: `internal` < `confidential` < `restricted` |
| **Label** | Das Feld `vertraulichkeit` im Dokumentkopf: `intern`, `C-Level`, `Betriebsrat-intern` |
| **ACL** | Berechnete Rechte eines Dokuments: `{domain, classification, allow[], published}` |
| **Request-Kontext** | Wer fragt gerade: `{user, agent, purpose, run_id}` |

## 4. Zwei Achsen: Domäne × Klassifikation

Rechte sind ein Gitter, kein Baum. Die Domäne sagt **wo** ein Dokument liegt und wer den Ort
öffnen darf; die Klassifikation sagt **wie empfindlich** es ist und wer es innerhalb des Orts
lesen darf. Das entspricht SharePoint-Sites × Sensitivity Labels und ist deshalb 1:1
übertragbar.

| Klassifikation | Bedeutung | Wer darf lesen |
|---|---|---|
| `internal` | im Ablageort normal ablegbar | die Site-Mitglieder des Ablageorts |
| `confidential` | Label `C-Level`, `Betriebsrat-intern` oder verschärfende Domäne | nur die Zielgruppe des Labels — Teilmenge der Site-Mitglieder |
| `restricted` | `hr-sensitiv`: Personalmaßnahmen, Vergütung | **nur** namentlich genannte Principals; **Existenz wird verborgen** |

Dazu **veröffentlicht**: ein `internal`-Dokument, dessen Wissen ausdrücklich unternehmensweit
ist, wird für alle lesbar — das entspricht einer „Veröffentlicht"-Bibliothek. Es ist die
einzige Regel, die Rechte *erweitert*, und sie ist bewusst eng (§6.4).

*Warum ein Gitter und kein Baum:* Ein Baum („Management sieht alles, was darunter liegt")
bildet Hierarchie ab. Unternehmen funktionieren nicht so — die Geschäftsführung sieht keine
Betriebsratsprotokolle, der CFO keine Personalakten. Zwei Achsen bilden das ab; eine nicht.

## 5. Principals

### 5.1 Menschen

Menschen sind Mitglieder von Gruppen (`data/permissions.yaml`). Das Konzept kennt keine
Personen — welche Gruppe wen enthält, ist eine Frage der Firma und ändert sich mit jeder
Beförderung. Für die Demo-Firma: `DEMOCOMPANY.md` §4.

### 5.2 Agenten — Vertretungsmodell (entschieden)

Ein Agent **vertritt eine Rolle** und hat exakt die Rechte der Person, die diese Rolle
innehat: `agents.cfo.represents: P-003` — der CFO-Agent erbt die Gruppen des CFO. Das ist
keine zusätzliche Konfiguration, sondern eine Konsequenz. Wechselt der CFO, wechselt der
Agent mit.

| Agent | vertritt | Sieht damit nicht |
|---|---|---|
| `agent:ceo` | die CEO | Betriebsrats-Ablage, HR-sensitive Vorgänge, Security-Details, fremde Mails |
| `agent:cfo` | den CFO | dito |
| `agent:it` | den CIO (mit Informationssicherheit) | C-Level-Vorlagen, Finance, HR, Betriebsrat |
| `agent:betriebsrat` | die Vorsitzende des Gesamtbetriebsrats | alle Sites der Geschäftsseite — bekommt nur Veröffentlichtes und Verteiler |
| `agent:orchestrator` | niemanden | **keine Inhalte** — nur Metadaten und Scores (`content_access: false`) |

*Warum der CEO-Agent nicht alles darf:* die häufigste Fehlannahme. Im echten Unternehmen
sieht die Geschäftsführung keine Betriebsratsprotokolle und keine Personalakten — das ist
Betriebsverfassungs- und Datenschutzrecht. Der Agent erbt diese Grenze.

*Warum der Orchestrator nichts liest:* Ein Orchestrator, der alle Inhalte sieht, ist das
größte Leck im System — jeder Umweg über ihn hebelt jede Berechtigung aus.

### 5.3 Request-Kontext: zwei Identitäten pro Anfrage

```json
{"user": "P-040", "agent": "cfo", "purpose": "evaluation", "run_id": "r_42"}
```

| Modus | Inhaltszugriff entscheidet | Output an den Menschen |
|---|---|---|
| **Bewertung** (`purpose: evaluation`) | Rechte des **Agenten** | wird nach Rechten des **Users** klassifiziert, §10 |
| **Chat** (`purpose: chat`, kein Agent) | Rechte des **Users** | ungefiltert — es ist ohnehin seins |

Damit: Gerd Sattler (PEO) reicht den Vorschlag ein; der CFO-Agent liest Finance-Dokumente,
die Sattler nicht öffnen darf; Sattler bekommt Scores plus eine bereinigte Begründung.

*Warum nicht „Agent erbt den Fragenden":* Wäre wasserdicht — aber dann bewertet der
CFO-Agent ohne Budget, sobald ein Projektleiter die Bewertung anstößt. Die Bewertung wäre
wertlos, genau in dem Fall, für den das System gebaut wird. Für den Chat-Modus bleibt es die
richtige Regel.

## 6. Rechte am Dokument — die Berechnung beim Ingest

Die ACL eines Dokuments wird **einmal beim Einlesen** aus zwei Quellen berechnet: dem
Ablageort (Ordner-Sidecar) und dem Dokumentkopf (Label, Domänen, Verteiler). Die Regeln
stehen als Konfiguration in `data/acl-rules.yaml`.

### 6.1 Ablageort → Site-Mitglieder

```yaml
# data/drive/sharepoint_finance/.acl.yaml
domain: finance
site_members: [grp-finance, grp-gf]
owner: P-003                      # gibt Eskalationen frei
default_classification: confidential
```

Ohne Sidecar: `site_members: []` — niemand, außer über Verteiler oder Veröffentlichung.

*Warum Ordner und nicht eine zentrale Rechtetabelle:* Weil Menschen Ordner verstehen. Wer
eine Datei in den Finance-SharePoint legt, hat sie klassifiziert, ohne ein Formular
auszufüllen. So funktionieren SharePoint und Drive heute schon.

### 6.2 Label → Klassifikation und Zielgruppe

| `vertraulichkeit` | Klassifikation | Zielgruppe |
|---|---|---|
| `intern` | `internal` | Site-Mitglieder |
| `C-Level` | `confidential` | `grp-c-level` |
| `Betriebsrat-intern` | `confidential` | `grp-betriebsrat` |

### 6.3 Informationsdomäne verschärft

`hr-sensitiv` → `restricted`, namentlich · `it-security-restricted` → `confidential`,
`grp-it-security` · `br-intern` → `grp-betriebsrat` · `c-level-beirat` → `grp-c-level`.
Immer gilt: Klassifikation = **Maximum**, Zielgruppe = die **engste**.

### 6.4 Veröffentlichung — die einzige Erweiterung

Genau wenn `informationsdomaene` **nur** `unternehmensweit` enthält **und** das Label `intern`
ist, gilt das Dokument als veröffentlicht: `allow: [grp-alle]`. Organigramme, Policies,
SOPs. Das bildet die „Veröffentlicht"-Bibliothek ab, die jeder SharePoint hat.

*Warum so eng:* Jede Erweiterungsregel ist ein potenzielles Leck. Diese eine ist an zwei
Bedingungen gebunden, die der Verfasser beide bewusst gesetzt hat.

### 6.5 Verteiler

Wer im Kopf als `verfasser` oder `empfaenger` steht, darf lesen — auch über Site-Grenzen.
Der 2026-Vorschlag mit „Gesamtbetriebsrat" im Verteiler ist damit für den Betriebsrat-Agenten
lesbar, obwohl er das Projektlaufwerk nicht öffnen darf. Namen und Einheiten werden über
`permissions.yaml → aliases` aufgelöst; Unbekanntes wird ignoriert und im Ingest-Log gemeldet.

### 6.6 Mailarchiv

Keine Site-Mitglieder. `allow` = Verfasser + Empfänger, immer `confidential`. Eine Mail liest,
wer sie geschrieben oder bekommen hat — sonst niemand, auch nicht der CIO als Owner des
Archivs (Owner heißt: gibt Eskalationen frei, nicht: liest mit).

### 6.7 Effektive ACL — Regeln

- Klassifikation: das Maximum aus Sidecar-Default, Label und Domäne.
- `allow`: die engste Zielgruppe (Label/Domäne) **∩** Site-Mitglieder; **∪** Verteiler;
  bei Veröffentlichung `grp-alle`.
- Mehrere Standorte derselben Datei (Dublette): `allow` = **Vereinigung** der Standorte.
  Wer eine Kopie ins Projektlaufwerk legt, hat sie für das Projektlaufwerk freigegeben.
- **Verschieben = Rechteänderung.** Neue ACL an allen Chunks, kein Re-Ingest.
- Jeder Chunk trägt die volle ACL plus `acl_hash`; Rechteänderungen sind Metadaten-Updates.

## 7. Entscheidungsfunktion

Eine Funktion, überall dieselbe — im Retrieval, im Enrichment, in der Output-Filterung:

```python
def decide(principal: Principal, acl: ACL) -> Decision:
    if acl.classification == "restricted":                 # nur namentlich, keine Vererbung
        return ALLOW if principal.id in acl.allow else HIDE  # HIDE = Existenz verbergen
    if principal.matches(acl.allow):                       # Person oder eine ihrer Gruppen
        return ALLOW
    return DENY                                            # sichtbar als Stub → eskalierbar
```

Drei Ergebnisse: `ALLOW` (Inhalt), `DENY` (Metadaten-Stub, eskalierbar), `HIDE` (nichts,
nur Zähler). Alles, was komplex ist — Sites, Labels, Domänen, Verteiler, Veröffentlichung —
ist beim Ingest in `allow` eingeflossen. Zur Laufzeit bleibt ein Mengentest.

*Warum eine einzige Funktion:* Drei Stellen im System entscheiden über Zugriff. Drei
Implementierungen hätten drei Möglichkeiten, sich zu widersprechen. Eine Funktion,
zwanzig Tests, fertig.

## 8. Durchsetzung im Retrieval

1. **Vorfilter.** `decide()` läuft über die Kandidaten **bevor** Top-k gebildet wird.
2. **`denied`** enthält je Dokument einmal: `doc_id`, `titel`, `domain`, `classification`,
   `reason`. Kein Auszug, keine Seitenzahl, kein Score.
3. **`HIDE`** erscheint nirgends außer als `hidden_count`.
4. Der Agent zitiert ausschließlich aus `allowed`. Ein Assessment, das eine `denied`-ID
   referenziert, wird vom Orchestrator zurückgewiesen.
5. `retrieve()` ist der **einzige** Weg zu Inhalten (§2.8).

*Warum Vorfilter und nicht Nachfilter:* Eine Suche liefert die zehn besten Treffer. Wenn
sieben davon verboten sind und erst danach entfernt werden, bekommt der Agent drei — und die
Tatsache, dass sieben fehlten, verrät, dass es sieben gibt.

## 9. Eskalation

Ein Agent, der einen `denied`-Stub für wesentlich hält, erstellt eine Eskalation — der Prozess
aus `PLAN.md` §4, sichtbar, protokolliert, im Hackathon simuliert.

```json
{
  "escalation_id": "e_017",
  "run_id": "r_42",
  "requested_by": "agent:betriebsrat",
  "on_behalf_of": "P-040",
  "doc_id": "LTT-20240512-HR-00",
  "domain": "hr",
  "classification": "confidential",
  "needed_information": "Personalplanung nach der Einstellungsbremse 2024",
  "reason": "Prüfung, ob der Pilot Key User aus Bereichen mit Einstellungsstopp belastet",
  "purpose": "evaluation",
  "affected_criteria": ["risk_score"],
  "required_level": "confidential",
  "approver": "P-032",
  "status": "open",
  "created_at": "2026-09-05T12:04:11Z",
  "expires_at": "2026-09-05T13:04:11Z"
}
```

- **Zustände:** `open` → `approved` | `rejected` | `expired`.
- **Approver** = `owner` des Ablageorts. Hackathon: `python -m mpb.access approve e_017`.
- **Wirkung:** temporärer Eintrag `grants[run_id]`, gültig nur für diesen `run_id` und bis
  `expires_at`. Kein dauerhaftes Recht. Audit-Zeile.
- **Solange offen:** Die Lücke bleibt im Assessment ausdrücklich sichtbar. Der Agent erfindet
  nichts.
- **`restricted` ist nicht eskalierbar** — was verborgen ist, kann nicht angefragt werden.

*Warum die Freigabe nur für einen Lauf gilt:* Eine Freigabe „für die Bewertung von
IP-2026-02" ist eine Sachentscheidung. Eine Freigabe „für den Betriebsrat-Agenten" wäre eine
Rechteerweiterung durch die Hintertür — nach zehn Eskalationen dürfte der Agent alles.

## 10. Output-Klassifikation

Ein Assessment erbt die Klassifikation seiner zitierten Quellen:
`assessment.acl = restriktivste ACL der cited_chunks`.

| Element | Sichtbar für |
|---|---|
| `value_score`, `risk_score`, `strategy_score` | **immer** — aggregierte Zahlen sind kein Leck |
| `assessment` (Freitext) | nur wenn `decide(user, assessment.acl) == ALLOW` |
| sonst | Platzhalter: *„Begründung enthält Quellen aus sharepoint_finance (C-Level). Freigabe bei Markus Heine anfragen."* + Eskalationslink |

*Warum Scores immer sichtbar sind:* Ein `risk_score` von 70 verrät nicht, welche
Beiratsvorlage dahintersteht. Ein Satz wie „das Programmbudget ist auf 19 Mio gestiegen" schon.

## 11. Enrichment — zurückgeschriebenes Wissen

- `classification` = Maximum der Quellen; `domain` = Domäne der restriktivsten Quelle.
- `allow` = **Schnittmenge** der Quellen-`allow` — nicht Vereinigung, sonst weitet
  Zusammenfassen Rechte aus.
- Ablage `data/drive/_brain/<domain>/<datum>_<slug>.md` mit Kopf im LTT-Format plus
  `verfasser: agent:cfo`, `derived_from`, `run_id`.
- Enthält eine Quelle `restricted`, wird **nicht** zurückgeschrieben.
- Rein externe Recherche (Web) → `internal`, `_brain/external/`, veröffentlicht.

## 12. Bedrohungen und Gegenmaßnahmen

| Bedrohung | Gegenmaßnahme | Test |
|---|---|---|
| Leck über Ranking | Vorfilter §8.1 | T1 |
| Leck über Enrichment | Vererbung §11 | T10 |
| Leck über Titel eines `restricted`-Dokuments | `HIDE` §7 | T3, T5 |
| Leck über Agenten-Hierarchie („CEO darf alles") | Vertretungsmodell; Gruppen der CEO enthalten weder BR noch HR-sensitiv | T6 |
| Leck über Orchestrator | `content_access: false` | T13 |
| Leck über Dateipfad oder Shell | ein Zugriffsweg §2.8; Agenten ohne Datei-Werkzeuge | T23 |
| Prompt Injection im Dokument | Durchsetzung im Code §2.5 | T11 |
| Verschobene Datei behält alte Rechte | Verschieben = Neuberechnung §6.7 | T8 |
| Dublette umgeht Rechte | Vereinigung ist gewollt (= Freigabe durch Kopieren) | T14 |
| Eskalation wird zum Dauerrecht | Grant nur je `run_id` §9 | T9 |
| Output verrät Inhalt | Output-Klassifikation §10 | T15 |
| Ablageort ohne Sidecar | `site_members: []` | T16 |
| Mail lesbar für Archiv-Owner | Owner ≠ Leser §6.6 | T24 |
| Unbekannter Name im Verteiler weitet Rechte | wird ignoriert, geloggt | T25 |

## 13. Datenmodell

| Datei | Inhalt | Ändert sich |
|---|---|---|
| `data/permissions.yaml` | Personen, Gruppen, Agenten (`represents`), Aliase | mit jeder Personalveränderung |
| `data/acl-rules.yaml` | Label- und Domänenregeln, Veröffentlichung, Mail | selten — ist Firmenpolitik |
| `data/drive/<ablageort>/.acl.yaml` | Domäne, Site-Mitglieder, Owner, Default | wenn eine Site entsteht oder ihre Mitglieder wechseln |
| Dokumentkopf | Label, Domänen, Verteiler | je Dokument, vom Verfasser |
| Chunk-Metadaten | berechnete ACL + `acl_hash` | beim Ingest und bei Rechteänderung |
| `audit.jsonl` | eine Zeile je Entscheidung | append-only |

```json
{"ts": "…", "run_id": "r_42", "user": "P-040", "agent": "cfo", "op": "retrieve",
 "query": "Programmbudget ONE LTT", "allow": 5, "deny": 2, "hide": 1,
 "denied_docs": ["LTT-20240512-HR-00"]}
```

## 14. Enterprise-Mapping

| Konzept hier | SharePoint / Microsoft 365 | Google Workspace |
|---|---|---|
| Ablageort / Domäne | Site, Dokumentbibliothek | Shared Drive |
| Site-Mitglieder | Site-Berechtigungen (Entra-ID-Gruppen) | Drive-Mitglieder |
| Label | Sensitivity Label (Purview) | Drive Labels |
| Verteiler | Item-Level Sharing | Dateifreigabe |
| Veröffentlichung | Bibliothek „Veröffentlicht" / Intranet | „Für alle in der Organisation" |
| Discovery | Graph Delta Query | `changes.list` |
| Approver | Site Owner | Drive Manager |

Der Ingest ersetzt dann nur den Schritt „ACL berechnen": statt Sidecar und Kopf lesen → Graph
`permissions` und Label abfragen. Alles danach bleibt gleich.

## 15. Umsetzung — Arbeitspaket 1

**Drin:** `permissions.yaml` laden (Gruppen rekursiv auflösen, `represents`), `resolve_acl()`
nach §6 aus Sidecar + Kopf, `decide()`, `retrieve()` als Vorfilter über den LTT-Korpus
(Keyword-Suche reicht) mit `allowed` / `denied` / `hidden_count`, Eskalation + `approve` +
Grant je `run_id`, `audit.jsonl`, Tests nach `TESTKONZEPT.md`.

**Danach:** Output-Klassifikation §10, Enrichment §11, Widerspruchserkennung, Embeddings,
Graph-Adapter.
