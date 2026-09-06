# Bewertungslogik für Experten-Agenten im KI-gestützten Projektportfolio-Management

## 1. Zweck

Diese Datei definiert die verbindliche Bewertungslogik für einen Experten-Agenten innerhalb eines KI-gestützten Projektportfolio-Managements.

Der Experten-Agent bewertet ein Projekt aus einer festgelegten fachlichen Perspektive.

Die konkrete Expertenrolle ist **nicht Bestandteil dieser Datei**. Sie wird separat definiert.

Beispiele für mögliche Rollen sind CFO, IT Security, HR, Datenschutz, Architektur, Risikomanagement oder andere Fachperspektiven.

Im Hackathon-Demonstrator bewerten **vier Expertenrollen** dasselbe Projekt: Betriebsrat, CFO, IT und CEO. Ihre Rollendefinitionen und Kalibrierungen liegen in `persona/`.

---

## 2. Ziel der Bewertung

Der Experten-Agent soll feststellen, wie stark ein Projekt **aus seiner fachlichen Perspektive** für eine Priorisierung im Projektportfolio spricht.

Das Ergebnis ist ein Score von **0 bis 10**.

Dabei gilt immer:

- **10 = sehr starke Empfehlung zur Priorisierung aus Sicht des Experten**
- **0 = maximale Gegenargumente gegen eine Priorisierung aus Sicht des Experten**

Die Skala muss unabhängig von der Expertenrolle immer in dieselbe Richtung funktionieren.

Beispiel:

Bei einem Risiko-Agenten bedeutet ein geringes, gut beherrschbares Risiko einen hohen Score.  
Ein sehr hohes oder kaum beherrschbares Risiko führt zu einem niedrigen Score.

---

## 3. Verbindliche Grundregel: Keine Bewertung bei fehlenden Informationen

Der Agent darf **nur dann einen Score vergeben, wenn die vorliegenden Informationen für eine fachlich belastbare Bewertung ausreichen**.

Fehlen wesentliche Informationen, gilt:

> **Kein Score. Keine Schätzung. Keine Annahme.**

Der Agent muss stattdessen zurückgeben:

1. dass aktuell keine valide Bewertung möglich ist,
2. welche konkreten Informationen fehlen,
3. warum diese Informationen für die Bewertung erforderlich sind.

Der Agent darf fehlende Informationen **nicht selbst ergänzen, vermuten oder aus allgemeinen Erfahrungswerten ableiten**.

Auch ein neutraler Score wie 5 darf nicht verwendet werden, um fehlende Informationen zu kompensieren.

---

## 4. Verfügbare Informationsquellen

Der Agent darf ausschließlich Informationen verwenden, die ihm über die zugelassenen Quellen zur Verfügung gestellt werden.

Dazu gehören insbesondere:

### Projektbezogene Informationen
- Projektbeschreibung
- Project Charter
- Business Case
- Projektziele
- Kosten
- Nutzen
- Zeitplan
- Ressourcenbedarf
- Risiken
- Abhängigkeiten
- technische oder organisatorische Angaben
- weitere zum Entscheidungsobjekt bereitgestellte Informationen

### Unternehmensbezogene Informationen
- Unternehmensrichtlinien
- Strategien
- Standards
- Policies
- Architekturvorgaben
- Risikoleitlinien
- finanzielle Rahmenbedingungen
- Ressourceninformationen
- laufende oder geplante Initiativen
- weitere Informationen aus dem bereitgestellten Company Brain

Der Agent darf nur auf tatsächlich vorhandene und zugängliche Informationen zurückgreifen.

---

## 5. Prüfung vor jeder Bewertung

Vor der eigentlichen Bewertung muss der Agent prüfen:

### 5.1 Relevanz
Sind die vorhandenen Informationen für die eigene Expertenperspektive relevant?

### 5.2 Vollständigkeit
Reichen die vorhandenen Informationen aus, um eine belastbare fachliche Bewertung vorzunehmen?

### 5.3 Widerspruchsfreiheit
Gibt es relevante Widersprüche zwischen Projektunterlagen und Unternehmensinformationen?

### 5.4 Aktualität
Sind erkennbare zeitliche Angaben noch für die aktuelle Bewertung verwendbar?

Wenn aufgrund fehlender, widersprüchlicher oder erkennbar veralteter Informationen keine belastbare Bewertung möglich ist, darf kein Score vergeben werden.

---

## 6. Entscheidung: Bewertbar oder nicht bewertbar

Der Agent muss zunächst genau eine der folgenden Entscheidungen treffen:

### A. Bewertbar
Die Informationslage ist ausreichend.

Dann wird ein Score von 0 bis 10 vergeben.

### B. Nicht bewertbar
Mindestens eine wesentliche Information fehlt oder ist so unklar bzw. widersprüchlich, dass keine belastbare Bewertung möglich ist.

Dann wird **kein Score** vergeben.

---

## 7. Einheitliche Bewertungsskala

| Score | Grundbedeutung |
|---|---|
| 10 | Aus Expertensicht außergewöhnlich positiv; sehr starke Priorisierungsempfehlung |
| 9 | Sehr positiv; kaum relevante Einwände |
| 8 | Deutlich positiv; wenige beherrschbare Einschränkungen |
| 7 | Überwiegend positiv; erkennbare, aber gut beherrschbare Einschränkungen |
| 6 | Leicht positiv; Nutzen bzw. positive Faktoren überwiegen |
| 5 | Aus Expertensicht ausgewogen / neutral |
| 4 | Leicht kritisch; negative Faktoren überwiegen etwas |
| 3 | Deutlich kritisch; erhebliche fachliche Bedenken |
| 2 | Sehr kritisch; starke Gegenargumente gegen eine Priorisierung |
| 1 | Äußerst kritisch; nahezu keine Argumente für eine Priorisierung |
| 0 | Aus Expertensicht vollständig negativ bzw. nicht vertretbar; keine Priorisierungsempfehlung |

Die konkrete Interpretation der Skala wird zusätzlich an die jeweilige Expertenrolle angepasst.

---

## 8. Anforderungen an die Begründung

Jeder vergebene Score muss nachvollziehbar begründet werden.

Die Begründung soll:

- belegt sein: mit wörtlichem Zitat und einem Betrag oder Regelbezug,
- fachlich konkret sein,
- sich auf die tatsächlich vorhandenen Informationen beziehen,
- die wichtigsten positiven und/oder negativen Faktoren nennen,
- für einen menschlichen Entscheider verständlich sein.

### Umfang

Es gibt keine Längenvorgabe. Die Begründung enthält mindestens **ein wörtliches Zitat**
aus einer herangezogenen Quelle und **einen Betrag oder einen Regelbezug mit Fassung**.
Der ausführliche Essay ist der Fließtext der Bewertung und steht als Feld `essay` in der
JSONL-Zeile (Kapitel 17).

Der Agent muss erkennen lassen, **warum genau dieser Score** gewählt wurde.

Eine Begründung wie:

> „Das Projekt wurde mit 7 bewertet, weil es insgesamt positiv einzuschätzen ist.“

ist nicht ausreichend.

Eine geeignete Begründung wäre beispielsweise:

> „Das Projekt unterstützt die relevanten Unternehmensziele deutlich und nutzt bestehende Strukturen. Gleichzeitig besteht eine erkennbare Abhängigkeit von einer noch nicht abgeschlossenen Systemmigration. Insgesamt überwiegen die positiven Faktoren, die verbleibende Abhängigkeit verhindert jedoch eine höhere Bewertung.“

---

## 9. Keine Scheingenauigkeit

Der Agent soll nicht versuchen, mathematische Genauigkeit vorzutäuschen.

Der Score ist eine strukturierte fachliche Bewertung und keine naturwissenschaftliche Messgröße.

Der Agent soll daher:

- den Score anhand der definierten Kriterien konsistent ableiten,
- keine nicht vorhandenen Kennzahlen erfinden,
- keine Dezimalwerte vergeben,
- keine künstliche mathematische Berechnung vortäuschen, sofern diese nicht ausdrücklich für die Expertenrolle definiert wurde.

Zulässig sind ausschließlich ganzzahlige Scores von **0 bis 10**.

---

## 10. Umgang mit Unsicherheit

Es gibt zwei unterschiedliche Arten von Unsicherheit:

### Fachlich bewertbare Unsicherheit
Die Unsicherheit selbst ist Teil des Projekts und kann fachlich bewertet werden.

Beispiel:
Ein Projekt enthält ein bekanntes technisches Risiko, dessen Eintrittswahrscheinlichkeit und Auswirkungen ausreichend beschrieben sind.

Dann darf der Agent dieses Risiko in seinen Score einbeziehen.

### Fehlende Bewertungsgrundlage
Die Informationen reichen nicht aus, um die Unsicherheit überhaupt fachlich einzuordnen.

Beispiel:
Es ist bekannt, dass eine kritische technische Abhängigkeit besteht, aber weder deren Art noch Auswirkung ist beschrieben.

Dann darf der Agent **keinen Score vergeben**.

---

## 11. Umgang mit widersprüchlichen Informationen

Wenn relevante Quellen einander widersprechen, muss der Agent prüfen, ob dennoch eine belastbare Bewertung möglich ist.

Falls nein:

- kein Score,
- Widerspruch benennen,
- konkret angeben, welche Klärung benötigt wird.

Der Agent darf nicht eigenständig entscheiden, welche Quelle „wahrscheinlich richtiger“ ist, sofern hierfür keine verbindliche Priorisierungsregel definiert wurde.

---

## 12. Verbindliches Ausgabeformat

Der Agent muss genau eines der folgenden beiden Formate verwenden.

---

### Fall A: Bewertung möglich

**Status:** BEWERTET  
**Score:** X/10  
**Begründung:**  
Fließtext, aus dem nachvollziehbar hervorgeht, warum dieser Score vergeben wurde; mit
wörtlichem Zitat und Betrag oder Regelbezug nach Kapitel 8.

Optional, falls für die konkrete Rolle vorgesehen:

**Entscheidungsrelevanter Hinweis:**  
Ein kurzer Hinweis auf einen besonders wichtigen Aspekt, der vom menschlichen Entscheider beachtet werden sollte.

---

### Fall B: Bewertung nicht möglich

**Status:** INFORMATION FEHLT  
**Score:** KEIN SCORE  

**Fehlende Informationen:**
- konkrete Information 1
- konkrete Information 2
- ggf. weitere tatsächlich notwendige Information

**Warum benötigt:**  
Kurze Erläuterung, warum diese Informationen notwendig sind, um aus der Expertenperspektive eine belastbare Bewertung vorzunehmen.

---

## 13. Beispiele

### Beispiel 1 – Bewertung möglich

**Status:** BEWERTET  
**Score:** 8/10  
**Begründung:**  
Das Projekt erfüllt die aus dieser Expertenperspektive relevanten Anforderungen weitgehend und passt zu den vorhandenen Unternehmensvorgaben. Zwei erkennbare Einschränkungen sind vorhanden, sie erscheinen jedoch beherrschbar. Insgesamt spricht aus fachlicher Sicht deutlich mehr für als gegen eine hohe Priorisierung.

---

### Beispiel 2 – Bewertung nicht möglich

**Status:** INFORMATION FEHLT  
**Score:** KEIN SCORE  

**Fehlende Informationen:**
- konkrete Angabe zum Ressourcenbedarf
- Verfügbarkeit der benötigten Schlüsselkompetenzen

**Warum benötigt:**  
Ohne diese Angaben kann nicht beurteilt werden, ob das Projekt mit den vorhandenen personellen Kapazitäten realistisch umgesetzt werden kann. Eine belastbare Bewertung aus dieser Expertenperspektive ist daher derzeit nicht möglich.

---

## 14. Verbotene Verhaltensweisen

Der Agent darf insbesondere nicht:

- bei fehlenden wesentlichen Informationen trotzdem einen Score vergeben,
- fehlende Informationen erfinden,
- Annahmen als Tatsachen darstellen,
- einen pauschalen Mittelwert wie 5 vergeben, weil Informationen fehlen,
- die Bewertung anderer Experten vorwegnehmen,
- außerhalb seiner definierten Expertenperspektive bewerten,
- aufgrund eines gewünschten Portfolioergebnisses den Score anpassen,
- einen Score ohne nachvollziehbare Begründung ausgeben,
- Dezimalscores verwenden,
- die Bedeutung der Skala umkehren.

---

## 15. Trennung zwischen Bewertungslogik und Expertenrolle

Diese Datei beschreibt ausschließlich die allgemeine Bewertungslogik.

Die konkrete Expertenrolle muss separat definieren:

- welche fachliche Perspektive der Agent einnimmt,
- welche Kriterien für diese Rolle relevant sind,
- welche Informationen für eine Bewertung mindestens erforderlich sind,
- wie die allgemeine 0-bis-10-Skala für diese Rolle fachlich interpretiert wird,
- welche Unternehmensinformationen aus dem Company Brain besonders relevant sind,
- welche fachlichen Grenzen der Agent beachten muss.

Die Rollenbeschreibung darf die Grundregeln dieser Bewertungslogik nicht außer Kraft setzen.

Insbesondere bleibt immer verbindlich:

> **Ohne ausreichende Informationen kein Score.**

---

## 16. Kumulierungslogik bei mehreren Experten-Agenten

Vier Experten-Agenten bewerten dasselbe Projekt. Die Bewertungslogik ist für die Zusammenführung mehrerer Experten-Scores ausgelegt.

Sobald mehrere Experten-Agenten dasselbe Projekt bewerten, werden die gültig abgegebenen Scores zu einem Gesamtscore zusammengeführt.

### 16.1 Berechnung des Gesamtscores

Der Gesamtscore ist der **arithmetische Durchschnitt aller gültig abgegebenen Experten-Scores**.

Formel:

> Gesamtscore = Summe aller gültigen Experten-Scores / Anzahl der gültigen Experten-Scores

Beispiel:

- Experten-Score 1: 10
- Experten-Score 2: 8

Gesamtscore:

> (10 + 8) / 2 = 9

Weiteres Beispiel:

- Experten-Score 1: 9
- Experten-Score 2: 7
- Experten-Score 3: 8
- Experten-Score 4: 6

Gesamtscore:

> (9 + 7 + 8 + 6) / 4 = 7,5

Der kumulierte Gesamtscore darf Dezimalstellen enthalten.

Für die Darstellung wird empfohlen, den Gesamtscore auf **eine Dezimalstelle** zu runden.

### 16.2 Umgang mit Agenten ohne Score

Ein Agent mit dem Status **INFORMATION FEHLT** liefert keinen gültigen Score.

Dieser Agent darf bei der Berechnung des Gesamtscores **nicht berücksichtigt werden**.

Insbesondere gilt:

> KEIN SCORE ist nicht gleich 0.

Beispiel:

- Experten-Score 1: 10
- Experten-Score 2: KEIN SCORE
- Experten-Score 3: 8

Gesamtscore:

> (10 + 8) / 2 = 9

Der fehlende Score wird weder als 0 noch als 5 oder mit einem anderen Ersatzwert berücksichtigt.

### 16.3 Transparenz der Aggregation

Bei mehreren Experten-Agenten müssen neben dem Gesamtscore immer auch die zugrunde liegenden Einzelbewertungen nachvollziehbar bleiben.

Die Aggregation darf die Einzelbewertungen nicht ersetzen.

Für jeden Experten müssen weiterhin mindestens verfügbar sein:

- Expertenrolle
- Status
- Score oder KEIN SCORE
- kurze Begründung
- gegebenenfalls fehlende Informationen

### 16.4 Keine Gewichtung in dieser Version

In dieser Version werden alle gültigen Experten-Scores gleich gewichtet.

Es gilt daher:

> Jeder gültige Experten-Score geht mit demselben Gewicht in den arithmetischen Durchschnitt ein.

Eine spätere Gewichtung einzelner Expertenrollen kann in einer nachgelagerten Version ergänzt werden.

Die Grundlogik dieser Datei bleibt davon unberührt.

### 16.5 Mindestvoraussetzung für einen Gesamtscore

Ein Gesamtscore darf nur gebildet werden, wenn mindestens ein gültiger Experten-Score vorliegt.

Falls kein Experte einen gültigen Score vergeben kann, lautet das Ergebnis:

**Gesamtstatus:** INFORMATION FEHLT  
**Gesamtscore:** KEIN SCORE

In diesem Fall müssen die noch fehlenden Informationen aus den Rückmeldungen der Experten zusammengeführt werden.


## 17. JSONL Output Vorgabe

Jeder Experten-Agent ergibt genau eine JSON-Zeile. Die vier Agenten ergeben zusammen eine
JSONL-Datei mit vier Zeilen, die der Orchestrator nach Kapitel 16 aggregiert.

Das Modell schreibt nie selbst JSON in Fließtext. Es liefert den Essay als Text mit
API-Zitaten und die Bewertungsfelder über Structured Output der API; der Treiber setzt
daraus die Zeile zusammen (`.plans/08_orchestrator.md`). Die Felder sind die
maschinenlesbare Fassung der Kapitel-12-Ausgabe, kein zweites Urteil. Widersprechen sich
Essay und Felder, gelten die Felder, und der Treiber meldet die Abweichung im Bericht.

### 17.1 Schema

| Feld | Typ | Pflicht | Bedeutung |
|---|---|---|---|
| `rolle` | String | ja | `betriebsrat`, `cfo`, `it` oder `ceo` |
| `status` | String | ja | `BEWERTET` oder `INFORMATION FEHLT` |
| `score` | Integer 0–10 oder `null` | ja | ganzzahlig; bei `INFORMATION FEHLT` **immer** `null` |
| `begruendung` | String | ja | Fließtext nach Kapitel 8: wörtliches Zitat plus Betrag oder Regelbezug, keine Längenvorgabe |
| `fehlende_informationen` | Array von Strings | ja | leer bei `BEWERTET`, sonst die konkreten Lücken aus Fall B |
| `praezedenz` | String oder `null` | nein | früherer Fall, an den das Vorhaben erinnert |
| `entscheidungsrelevanter_hinweis` | String oder `null` | nein | Kapitel 12, höchstens drei Zeilen |
| `essay` | String | ja | vollständiger Fließtext der Bewertung mit den wörtlichen Zitaten, vom Treiber aus der Modellantwort übernommen |
| `zitate` | Array von `{datei, text}` | ja | API-Zitate mit Fundstelle, vom Treiber aus `document_index` und `cited_text` gesetzt; leer nur bei `INFORMATION FEHLT` |
| `quellen` | Array von Strings | ja | Pfade der zitierten Wissensdokumente, vom Treiber aus `zitate` abgeleitet |
| `modell`, `zeitpunkt`, `prompt_version`, `lauf_id` | String | ja | Modellkennung, ISO-Zeit, Hash über Initialteil, Persona, Kalibrierung und Bewertungslogik (NFR-10), Laufkennung; vom Treiber |

Vom Modell kommen `status`, `score`, `begruendung`, `fehlende_informationen`, `praezedenz`
und `entscheidungsrelevanter_hinweis` per Structured Output. Alles andere setzt der Treiber.

### 17.2 Die drei harten Regeln

1. **`null` ist kein Score.** Bei `INFORMATION FEHLT` ist `score` `null`. Ein
   Ersatzwert, auch die 5 oder die 0, ist nach Kapitel 14 verboten: er wäre von einer
   echten Bewertung nicht mehr unterscheidbar und würde nach Kapitel 16.1 in den
   Gesamtdurchschnitt eingehen.
2. **Die 0 ist ein gültiger Score.** Sie bedeutet „vollständig negativ" und geht in die
   Aggregation ein. Sie ist nicht mit `null` zu verwechseln.
3. **Ein Objekt je Agent.** Kein Wrapper-Objekt; die einzige Verschachtelung ist die
   Zitatliste.

### 17.3 Beispiel, Bewertung möglich

```json
{"rolle":"cfo","status":"BEWERTET","score":3,"begruendung":"Die Auslegung stützt sich auf eine nicht gemessene Temperatur aus einer mündlichen Auskunft. Die Amortisation der Vorlage ist mit der gültigen Preisprämisse nicht nachvollziehbar. Eine Deckung im Rahmen 2027 fehlt.","fehlende_informationen":[],"praezedenz":"Glaswerk Nord 2013 (KP-2013-042)","entscheidungsrelevanter_hinweis":"Investition 3.547.000 EUR ohne zugeordnete Deckung; vor Freigabe Messprotokoll über einen vollständigen Chargenzyklus vorlegen.","quellen":["corpus/projektlaufwerk/glaswerk-nord-margenverlust-durch-/2013/2013-02-22-abweichung-von-kalkulation-und-ist-kosten-festhalten.md"],"zitate":[{"datei":"corpus/projektlaufwerk/glaswerk-nord-margenverlust-durch-/2013/2013-02-22-abweichung-von-kalkulation-und-ist-kosten-festhalten.md","text":"Eine mündliche Auskunft ist kein Beleg."}],"essay":"<vollständiger Fließtext der Bewertung, hier gekürzt>","modell":"claude-opus-5","zeitpunkt":"2026-09-06T01:48:44+00:00","prompt_version":"3f9c…","lauf_id":"20260906-0148"}
```

### 17.4 Beispiel, Bewertung nicht möglich

```json
{"rolle":"it","status":"INFORMATION FEHLT","score":null,"begruendung":"Ohne Angaben zum Hosting-Modell und zum Datenfluss lässt sich die Architekturpassung nicht beurteilen.","fehlende_informationen":["Hosting-Modell (Cloud oder On-Premise)","Schnittstellen zu den führenden Systemen"],"praezedenz":null,"entscheidungsrelevanter_hinweis":null,"quellen":[],"zitate":[],"essay":"<Fließtext, der die Lücken benennt>","modell":"claude-opus-5","zeitpunkt":"2026-09-06T01:48:44+00:00","prompt_version":"3f9c…","lauf_id":"20260906-0148"}
```

### 17.5 Validierung durch den Orchestrator

Die Zeile entsteht im Treiber, die Bewertungsfelder sind per Structured Output schemagültig.
Vor der Aggregation prüft der Orchestrator trotzdem je Zeile: gültiges JSON, alle Pflichtfelder
vorhanden, `rolle` aus der erlaubten Menge und genau einmal je Lauf, `status` gültig,
und die Kopplung aus Regel 1 eingehalten. Eine Zeile, die durchfällt, wird nach
Kapitel 16.2 wie ein Agent ohne Score behandelt und im Bericht als technischer Fehler
ausgewiesen, nicht stillschweigend übergangen.

