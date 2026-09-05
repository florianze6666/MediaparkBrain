# Template: Dokumentkopf eines Korpusdokuments

Verbindlich fuer jedes `.md` unter `corpus/`. Das YAML-Frontmatter steht ganz oben, ohne Leerzeile
davor, in **genau dieser Feldfolge**. Darunter folgt der realistische Dokumentkopf im Fliesstext.

SSOT: die Feldfolge und die erlaubten Werte stammen aus `CLAUDE.md`. Aendert sich dort etwas, gilt
CLAUDE.md, nicht diese Datei.

## 1. Frontmatter

```yaml
---
doc_id: LTT-2024-0814-IT-007
titel: Reduktion des Integrationsumfangs PLM/ERP
dokumenttyp: Architekturentscheidung
datum: 2024-08-14
verfasser: <Name aus canon/registry/people.md>
rolle: <Rolle dieser Person zum Dokumentdatum>
organisationseinheit: IT
empfaenger: [Geschäftsführung]
projekt: ONE LTT
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [it-security-restricted, projektintern]
ablageort: it_doku
---
```

## 2. Erlaubte Werte je Feld

| Feld | Regel |
|---|---|
| `doc_id` | `LTT-<JJJJ>-<MMTT>-<EINHEIT>-<NNN>`, identisch mit der Manifestzeile |
| `titel` | Klartext, wie ihn der Verfasser gewaehlt haette. Keine Generatorsprache |
| `dokumenttyp` | einer der Typen aus CLAUDE.md, Abschnitt "Dokumenttypen sollen heterogen sein" |
| `datum` | ISO `JJJJ-MM-TT`, identisch mit der Manifestzeile |
| `verfasser` | Name **aus** `canon/registry/people.md`. Kein erfundener Name |
| `rolle` | die Rolle dieser Person **zum Dokumentdatum**, nicht ihre spaetere |
| `organisationseinheit` | Einheit des Verfassers zum Datum |
| `empfaenger` | YAML-Liste. Rollen oder Namen aus dem Register. `[]` wenn ohne Adressat |
| `projekt` | Projektname aus `canon/registry/projects.md` oder `"-"` |
| `geschaeftsbereich` | Business Unit oder `"-"`. Vor 2022 existieren die vier BUs noch nicht |
| `vertraulichkeit` | **nur** `intern`, `C-Level`, `Betriebsrat-intern` |
| `informationsdomaene` | YAML-Liste aus: `unternehmensweit`, `bereichsintern`, `projektintern`, `management`, `c-level-beirat`, `hr-sensitiv`, `it-security-restricted`, `br-intern`, `br-management-verhandlung` |
| `ablageort` | **nur** `sharepoint_gf`, `sharepoint_finance`, `sharepoint_hr`, `projektlaufwerk`, `mailarchiv`, `br_ablage`, `qm_lenkung`, `it_doku`, `einkauf_scm` |

## 3. Dokumentkopf im Fliesstext

Direkt unter dem Frontmatter, in der Form, die der Dokumenttyp im Jahr des Dokuments haette. Das
Frontmatter ist Metadatenschicht fuer das Retrieval, der Fliesstextkopf ist Teil des Dokuments.

Beispiel fuer eine Entscheidungsvorlage:

```
# Reduktion des Integrationsumfangs PLM/ERP

**Lahnberg Thermotechnik GmbH & Co. KG** - Informationstechnologie
Vorlage zur Entscheidung

Von:       Andrea Faber, Leiterin IT-Applikationen
An:        Geschäftsführung
Kopie:     Programmleitung ONE LTT
Datum:     14. August 2024
Az.:       IT-2024-0814
Einstufung: intern
```

Beispiel fuer eine E-Mail im `mailarchiv`:

```
Von:      andrea.faber@lahnberg-thermotechnik.de
An:       markus.heine@lahnberg-thermotechnik.de
Cc:       ...
Datum:    Mittwoch, 14. August 2024, 17:42
Betreff:  AW: Integrationsumfang PLM/ERP - kurzfristige Einschätzung
```

Beispiel fuer ein Protokoll:

```
# Steering Committee ONE LTT - Protokoll der 14. Sitzung

Ort:        Kassel, Raum Fulda / Teams
Datum:      14. August 2024, 09:00 - 11:30 Uhr
Teilnehmer: ...
Protokoll:  ...
Verteiler:  ...
```

Die Einstufung erscheint im Fliesstextkopf **nur**, wenn sie nicht `intern` ist - `C-Level` und
`Betriebsrat-intern` werden im Dokument sichtbar markiert, `intern` ist der stille Normalfall und
steht nur im Frontmatter. Eine E-Mail traegt ohnehin keine Einstufungszeile; dort genuegt das
Frontmatter.

## 4. Was nie im Dokument steht

Kein Feld aus dem Manifest, das die Entstehung beschreibt: `herkunft`, `cluster`, `kohorte`,
`zweck`, `dokumentabsicht`, `faktenkern`, `episode_id`. Ein Dokument, das seinen eigenen
Entstehungsgrund vermerkt, ist unrealistisch und verraet den Generator.
