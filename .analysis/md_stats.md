# Markdown-Statistik MediaparkBrain

**Erhebungsdatum:** 2026-09-05

**Untersuchte Wurzelverzeichnisse** (jeweils rekursiv, relativ zu `D:\dev\prj\hackathon_rag\MediaparkBrain`):

1. `corpus`
2. `test`
3. `test project data`
4. `.test`

Berücksichtigt wurden die Endungen `.md` und `.markdown`. `.venv`, `__pycache__`, `.pytest_cache` und `.git` wurden übersprungen (traten in diesen Bäumen aber nicht auf).

## Status der Wurzelverzeichnisse

| Wurzel | Status |
|---|---|
| `corpus` | existiert, 217 Markdown-Dateien gefunden |
| `test` | existiert, **enthält aber keine Markdown-Dateien** (nur `Dateiupload/Stellungnahme_Betriebsrat_digitale_Unterschrift.docx`) |
| `test project data` | existiert, **enthält aber keine Markdown-Dateien** (nur `.xlsx`-Dateien, keine Unterordner) |
| `.test` | existiert, 2 Markdown-Dateien gefunden |

Keine Datei war unlesbar (kein UTF-8-Decodierfehler aufgetreten) — der Abschnitt „Nicht lesbare Dateien" bleibt daher leer.

## Aggregierte Kennzahlen gesamt

| Kennzahl | Wert |
|---|---|
| Dateien gesamt | 219 |
| Größe gesamt | 2.011.084 Bytes (≈ 1.964,0 KB / ≈ 1,92 MB) |
| Zeilen gesamt | 33.916 |
| Wörter gesamt | 261.705 |

## Kennzahlen je Wurzelverzeichnis

| Wurzel | Dateien | Größe (Bytes) | Größe (KB) | Zeilen | Wörter |
|---|---:|---:|---:|---:|---:|
| corpus | 217 | 1.896.042 | 1.851,6 | 33.310 | 253.411 |
| test | 0 | 0 | 0,0 | 0 | 0 |
| test project data | 0 | 0 | 0,0 | 0 | 0 |
| .test | 2 | 115.042 | 112,3 | 606 | 8.294 |
| **Gesamt** | **219** | **2.011.084** | **1.964,0** | **33.916** | **261.705** |

## Aufschlüsselung innerhalb von `corpus` nach Unterordner (1. Ebene)

| Unterordner | Dateien | Größe (Bytes) | Größe (KB) | Zeilen | Wörter |
|---|---:|---:|---:|---:|---:|
| sharepoint_gf | 47 | 372.340 | 363,6 | 6.551 | 50.032 |
| projektlaufwerk | 36 | 372.259 | 363,5 | 5.802 | 50.207 |
| it_doku | 29 | 255.407 | 249,4 | 4.422 | 33.929 |
| qm_lenkung | 24 | 243.472 | 237,8 | 4.540 | 31.744 |
| einkauf_scm | 21 | 209.861 | 204,9 | 3.597 | 27.552 |
| sharepoint_hr | 18 | 122.985 | 120,1 | 2.604 | 16.362 |
| sharepoint_finance | 14 | 128.445 | 125,4 | 2.364 | 17.369 |
| br_ablage | 15 | 126.395 | 123,4 | 2.287 | 17.040 |
| mailarchiv | 12 | 64.414 | 62,9 | 1.134 | 9.127 |
| (direkt in `corpus/`) | 1 | 464 | 0,5 | 9 | 49 |
| **Summe corpus** | **217** | **1.896.042** | **1.851,6** | **33.310** | **253.411** |

Die direkt in `corpus/` liegende Datei ist `ATTRIBUTION.md`. `sharepoint_gf` und `projektlaufwerk` sind mit Abstand die größten Ablageorte, dicht gefolgt von `it_doku` und `qm_lenkung`; `mailarchiv` ist der kleinste erfasste Ablageort.

## Verteilung der Dateigröße (Bytes, alle 219 Dateien)

| Kennzahl | Bytes | KB |
|---|---:|---:|
| Minimum | 464 | 0,5 |
| Maximum | 57.521 | 56,2 |
| Mittelwert | 9.183 | 9,0 |
| Median | 8.562 | 8,4 |

## Größenklassen-Verteilung

| Klasse | Anzahl Dateien |
|---|---:|
| < 1 KB | 1 |
| 1–10 KB | 159 |
| 10–50 KB | 57 |
| > 50 KB | 2 |
| **Summe** | **219** |

## Top 20 größte Dateien

| # | Pfad | Größe (Bytes) | Größe (KB) | Zeilen | Wörter |
|---:|---|---:|---:|---:|---:|
| 1 | `.test/vertrauchlichkeit.md` | 57.521 | 56,2 | 303 | 4.147 |
| 2 | `.test/vertraulichkeit.md` | 57.521 | 56,2 | 303 | 4.147 |
| 3 | `corpus/it_doku/nis2-vorbereitung/2025/2025-04-22-anforderungen-aus-nis2-und-den-umsetzungsstand-bewer.md` | 18.408 | 18,0 | 264 | 2.439 |
| 4 | `corpus/einkauf_scm/beschaffungsstrategie-mit-versorgu/2024/2024-08-03-s4-positionen-und-ihre-alternativen-erfassen.md` | 16.810 | 16,4 | 245 | 2.252 |
| 5 | `corpus/projektlaufwerk/fehlende-voraussetzungen-fuer-den-/2023/2023-11-06-offene-voraussetzungen-fuer-den-go-live-erfassen.md` | 16.000 | 15,6 | 219 | 2.262 |
| 6 | `corpus/sharepoint_gf/beschluss-des-programms-one-ltt/2022/2022-10-15-digitalisierungsprogramm-zur-beschlussfassung-vorleg.md` | 15.521 | 15,2 | 140 | 2.091 |
| 7 | `corpus/sharepoint_finance/investitionsrichtlinie-mit-npv-irr/2022/2022-08-04-antragsteller-in-npv-und-irr-einweisen.md` | 15.181 | 14,8 | 278 | 2.170 |
| 8 | `corpus/einkauf_scm/dual-source-grundsatz-mit-ausnahme/2021/2021-04-12-dual-source-grundsatz-und-ausnahmen-festlegen.md` | 15.087 | 14,7 | 284 | 1.816 |
| 9 | `corpus/projektlaufwerk/operativer-start-von-one-ltt-mit-g/2023/2023-01-10-umsetzungsphase-des-programms-beauftragen.md` | 14.910 | 14,6 | 256 | 1.879 |
| 10 | `corpus/einkauf_scm/zentralisierung-des-supply-chain-m/2021/2021-04-22-aufbau-von-supply-chain-operations-planning-beauftra.md` | 14.895 | 14,5 | 232 | 1.886 |
| 11 | `corpus/sharepoint_finance/beschluss-des-programms-one-ltt/2022/2022-10-24-programmbudget-beantragen.md` | 14.570 | 14,2 | 262 | 2.002 |
| 12 | `corpus/einkauf_scm/lieferantenbewertung-eingefuehrt/2016/2016-05-14-bewertungskriterien-fuer-lieferanten-festlegen.md` | 14.568 | 14,2 | 282 | 1.885 |
| 13 | `corpus/projektlaufwerk/beschluss-des-programms-one-ltt/2022/2022-11-26-programmrisiken-zum-start-erfassen.md` | 14.314 | 14,0 | 142 | 2.041 |
| 14 | `corpus/projektlaufwerk/verschiebung-des-erp-go-live-und-a/2024/2024-03-10-risiken-nach-der-verschiebung-aktualisieren.md` | 14.305 | 14,0 | 103 | 2.021 |
| 15 | `corpus/einkauf_scm/beschaffungsstrategie-mit-versorgu/2024/2024-07-15-versorgungsklassen-s1-bis-s4-festlegen.md` | 14.130 | 13,8 | 264 | 1.839 |
| 16 | `corpus/qm_lenkung/pmo-gruendung-und-ruecknahme-von-p/2016/2016-08-20-projektstruktur-meilensteine-und-statusbericht-festl.md` | 13.862 | 13,5 | 285 | 1.837 |
| 17 | `corpus/qm_lenkung/ampelsystem-und-seine-entwertung/2023/2023-04-13-ampelkriterien-fuer-den-projektstatus-festlegen.md` | 13.840 | 13,5 | 249 | 1.906 |
| 18 | `corpus/qm_lenkung/design-freeze-eingefuehrt-und-sele/2019/2019-02-01-design-freeze-und-engineering-change-request-regeln.md` | 13.665 | 13,3 | 233 | 1.667 |
| 19 | `corpus/projektlaufwerk/project-atlas-review/2024/2024-05-22-im-review-benannte-risiken-uebernehmen.md` | 13.569 | 13,3 | 208 | 1.896 |
| 20 | `corpus/projektlaufwerk/operativer-start-von-one-ltt-mit-g/2023/2023-02-02-erste-steuerungssitzung-protokollieren.md` | 13.534 | 13,2 | 158 | 1.790 |

## Top 10 kleinste Dateien

| # | Pfad | Größe (Bytes) | Größe (KB) | Zeilen | Wörter |
|---:|---|---:|---:|---:|---:|
| 1 | `corpus/ATTRIBUTION.md` | 464 | 0,5 | 9 | 49 |
| 2 | `corpus/einkauf_scm/stammdaten/2018/2018-11-06-lieferantenstammliste.md` | 3.186 | 3,1 | 78 | 438 |
| 3 | `corpus/sharepoint_hr/fuehrungswechsel-von-albrecht-zu-k/2022/2022-09-30-wechsel-in-der-geschaeftsfuehrung-bekanntgeben.md` | 3.349 | 3,3 | 75 | 428 |
| 4 | `corpus/einkauf_scm/stammdaten/2021/2021-08-24-lieferantenstammliste.md` | 3.384 | 3,3 | 88 | 493 |
| 5 | `corpus/sharepoint_hr/organisation/2011/2011-03-14-organigramm-lahnberg-thermotechnik.md` | 3.519 | 3,4 | 103 | 399 |
| 6 | `corpus/it_doku/architektur/2016/2016-10-11-softwareportfolio-der-ltt-gruppe.md` | 4.008 | 3,9 | 107 | 533 |
| 7 | `corpus/mailarchiv/das-wissensmanagementproblem-2025/2025/2025-08-03-suchaufwand-bei-projektuebernahme-melden.md` | 4.243 | 4,1 | 76 | 624 |
| 8 | `corpus/sharepoint_hr/betriebsvereinbarung-zur-nutzung-d/2020/2020-12-07-belegschaft-ueber-die-neue-vereinbarung-informieren.md` | 4.263 | 4,2 | 83 | 578 |
| 9 | `corpus/mailarchiv/crm-einfuehrung-als-70-prozent-erf/2023/2023-06-06-aufwand-der-pflichtfelder-im-kundenkontakt-melden.md` | 4.477 | 4,4 | 85 | 666 |
| 10 | `corpus/sharepoint_hr/organisation/2025/2025-03-18-standortuebersicht-der-ltt-gruppe.md` | 4.477 | 4,4 | 109 | 592 |

Es gibt keine leeren oder nahezu leeren Dateien (< 1 KB) außer `corpus/ATTRIBUTION.md`, die aber bewusst nur ein kurzer Attributionshinweis ist.

## Nicht lesbare Dateien

Keine — alle 219 gefundenen Markdown-Dateien konnten als UTF-8 gelesen werden.

## Beobachtungen

Die beiden mit Abstand größten Dateien im gesamten Bestand liegen nicht im Corpus, sondern in `.test/`: `vertrauchlichkeit.md` und `vertraulichkeit.md` sind byteidentisch groß (je 57.521 Bytes, 303 Zeilen, 4.147 Wörter) und unterscheiden sich im Dateinamen nur durch einen Buchstabendreher — das sieht nach einer versehentlichen Dublette (Tippfehler-Kopie) statt zwei inhaltlich unterschiedlichen Dokumenten aus. Innerhalb von `corpus` verteilt sich das Volumen recht gleichmäßig auf die großen Ablageorte `sharepoint_gf` und `projektlaufwerk` (je ca. 363 KB), während `mailarchiv` mit nur 63 KB deutlich abfällt. Die Größenklassen zeigen ein klares Übergewicht kleiner bis mittelgroßer Dateien: 159 von 219 Dateien (73 %) liegen zwischen 1 und 10 KB, nur zwei Dateien überschreiten 50 KB (eben die beiden `.test`-Dubletten), und mit `ATTRIBUTION.md` (464 Bytes) gibt es genau eine Datei unter 1 KB. Die Verzeichnisse `test` und `test project data` enthalten aktuell überhaupt keine Markdown-Dateien (nur eine `.docx`- bzw. mehrere `.xlsx`-Dateien), tragen also nichts zur Markdown-Statistik bei.
