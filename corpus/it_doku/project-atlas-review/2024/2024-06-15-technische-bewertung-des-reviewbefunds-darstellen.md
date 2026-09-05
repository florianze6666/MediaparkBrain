---
doc_id: LTT-20240615-IT-06
titel: Technische Bewertung der Feststellungen des Project Atlas Review
dokumenttyp: Management Summary
datum: 2024-06-15
verfasser: Dr. Philipp Nowak
rolle: CIO
organisationseinheit: IT
empfaenger: ["-"]
projekt: PRJ-ATLAS-REVIEW
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [management, projektintern]
ablageort: it_doku
---

Lahnberg Thermotechnik GmbH & Co. KG
IT, Büro des CIO
Kassel, 15. Juni 2024

Management Summary

Betreff: Technische Bewertung der Feststellungen des Project Atlas Review
Von: Dr. Philipp Nowak, CIO
Einstufung: intern
Ablage: IT-Dokumentation, Project Atlas Review

## 1. Anlass

Der im Mai vorgelegte Review kommt zu dem Ergebnis, das Programm sei technisch grundsätzlich
umsetzbar; das zentrale Risiko liege nicht bei der Software, sondern in der Organisation. Genannt
werden zu viele parallele Transformationsprojekte, die geringe Verfügbarkeit der Key User, fehlende
Datenverantwortung, unklare Entscheidungsrechte, erhebliche lokale Prozessvarianten, die Überlastung
der Fachabteilungen, eine zu große Programmbreite und eine unzureichende Change-Kommunikation.
Besonders kritisch bewertet wird der Versuch, ERP, PLM, CRM, MES, Service und Projektmanagement
gleichzeitig neu zu ordnen.

Diese Zusammenfassung ordnet den Befund aus Sicht der IT ein und benennt die technischen
Voraussetzungen, unter denen die IT den Anfang Juni beschlossenen Schnitt in Teilprogramme trägt.

## 2. Einordnung des Befunds

Den organisatorischen Kern teile ich. Die drei Feststellungen, die aus meiner Sicht tragen, sind die
fehlende Datenverantwortung, die unklaren Entscheidungsrechte und die Programmbreite. Sie hängen
zusammen: Wo niemand über einen Datenbestand entscheidet, entscheidet am Ende die IT, und zwar über
fachliche Fragen, für die uns die Fachkenntnis fehlt. Das ist seit meinem Amtsantritt im April 2023
die häufigste Eskalation aus dem Teilprojekt Stammdaten.

Bei der Formulierung "technisch umsetzbar" widerspreche ich der Lesart, die sich im Haus eingestellt
hat. Die Reviewer haben die Machbarkeit je Zielsystem beurteilt, nicht den Zustand zwischen den
Systemen. Umsetzbar heißt: Jedes einzelne System lässt sich einführen. Es heißt nicht, dass die
Landschaft nach dem Scope-Schnitt ohne zusätzliche Handarbeit betriebsfähig ist. Genau dieser
Unterschied entscheidet über den Aufwand der nächsten zwei Jahre.

## 3. Was der Scope-Schnitt technisch bedeutet

Weitergeführt werden Finance, Procurement, CRM, Business Intelligence, Projektcontrolling und Teile
des Master Data Managements. Vertagt sind die vollständige PLM-ERP-Integration, die durchgängige
EBOM-MBOM-Automatisierung, der MES-Rollout in Eisenach und die konzernweite Serviceplattform. Aus
IT-Sicht ist das keine Verkleinerung, sondern die Entscheidung für einen Zwischenzustand, der an vier
Stellen dauerhaft von Personen getragen wird:

- Die beiden ERP-Landschaften in Kassel und Eisenach bleiben bis auf Weiteres parallel in Betrieb.
  Ob der Oktobertermin beide Standorte trägt oder Eisenach in einer zweiten Welle folgt, ist nicht
  entschieden; die IT plant vorsorglich für den Parallelbetrieb einschließlich Wartung, Schnittstellen
  und doppelter Stammdatenpflege.
- Die Übergabe zwischen Konstruktions- und Fertigungsstückliste bleibt ein manueller Schritt. Die
  formelle Übergabe ist seit April 2023 in POL-ENG-001 v1.1 geregelt. Ohne die vertagte
  Automatisierung bleibt die Regel richtig und der Vollzug teuer.
- Der Materialstamm bleibt die Bruchstelle. Von den ursprünglich angestrebten 40 Prozent Bereinigung
  sind rund 18 Prozent erreicht. Diese Zahl bestimmt den Aufwand in Finance und Procurement, nicht die
  Zahl im Statusbericht.
- MES und Serviceplattform sind vertagt, nicht gestrichen. Beide stehen in der Zielarchitektur und
  sind in der Betriebs- und Lizenzplanung bis auf Weiteres nicht enthalten. Wer sie als erledigt
  betrachtet, wird die Frage bei der nächsten Planungsrunde erneut vorfinden.

## 4. Voraussetzungen der IT

Die IT trägt den Schnitt unter den folgenden Bedingungen. Sie gelten je Teilprogramm, nicht pauschal
für das Programm.

1. **Interimsarchitektur wird beschrieben und befristet.** Für jede vertagte Integration beschreibt
   die IT bis Ende Juli den Zwischenstand: welche Schnittstelle, welcher manuelle Schritt, wer führt
   ihn aus, bis wann gilt er. Ein Zwischenstand ohne Enddatum ist ein Zielzustand.
2. **Keine Produktivsetzung ohne benannte Datenverantwortung.** Für Material, Kunde, Lieferant und
   Projekt jeweils eine namentlich benannte Verantwortung mit Entscheidungsbefugnis über Anlage,
   Änderung und Sperre. POL-IT-006 beschreibt das Verfahren seit April 2023, benennt aber keine
   Personen. Solange das so bleibt, ist die Feststellung des Reviews nicht abgestellt, sondern nur
   dokumentiert.
3. **Key-User-Kapazität verbindlich in Personentagen.** Die Verfügbarkeit ist am 6. Juni gesondert
   eskaliert worden. Eine Zusage in Prozent einer Stelle ist bisher regelmäßig an der Projektlast der
   Fachabteilung gescheitert. Ich bitte um Zusagen in Tagen je Monat und Person, gegengezeichnet vom
   abgebenden Bereich.
4. **Abweichung nur mit Eigentümer und Enddatum.** Lokale Prozessvarianten werden nicht pauschal
   abgeschafft. Jede beibehaltene Variante erhält einen fachlichen Eigentümer, eine Begründung und ein
   Datum der erneuten Prüfung. Andernfalls wandert sie in eine Excel-Lösung neben dem System, und wir
   haben sie im nächsten Vorhaben unverändert vor uns.
5. **Entscheidungsrechte vor Zuschnitt.** Solange die Verteilung der Projektverantwortung neu bewertet
   wird, sollte kein Teilprogramm mit einem Zuschnitt starten, der vom Ergebnis dieser Bewertung
   abhängt.
6. **Rollen, Berechtigungen und Cloud-Dienste gegen den geltenden Standard.** Jedes Teilprogramm
   liefert sein Rollenmodell gegen POL-IT-001 v3.0, nicht daneben. Für Cloud-Dienste gilt POL-IT-003
   v2.0 einschließlich des Nachweises der Exit-Fähigkeit; für die seit Januar produktiven Dienste in
   Beschaffung und Reisekosten ist er zu erbringen, für alle weiteren vor Vertragsabschluss.
7. **Mitbestimmung folgt dem Schnitt.** BV-2023-01 verlangt eine Teilvereinbarung vor jeder
   Produktivsetzung. Der Schnitt in Teilprogramme vervielfacht die Zahl der Produktivsetzungen und
   damit die Zahl der Teilvereinbarungen. Die Qualifizierungszusage besteht unabhängig vom Termin; die
   Frage nach dem Stand der Schulungsplanung liegt seit März vor. Das ist einzuplanen und nicht
   nachzuholen.

## 5. Wirtschaftliche Folge

Der erwartete Aufwand ist im März von 14,8 auf rund 19 Mio EUR fortgeschrieben worden. Der
Scope-Schnitt senkt den Umsetzungsaufwand. Er senkt den Betriebsaufwand nicht im gleichen Maß:
Parallelbetrieb, manuelle Übergaben und doppelte Stammdatenpflege sind laufende Kosten, keine
Projektkosten. Ich halte es für erforderlich, diese Position in der nächsten Vorlage getrennt
auszuweisen. Die Investitionsrichtlinie verlangt seit Januar ohnehin eine TCO- und
Betriebskostenbetrachtung für Softwarevorhaben; sie sollte hier nicht auf die verbleibenden
Teilprogramme beschränkt werden, sondern das einschließen, was durch die Vertagung an Betrieb
entsteht.

## 6. Offene Punkte

- Zuschnitt der Teilprogramme: Die Arbeitstitel Digital Core, Engineering Backbone und Service
  Transformation sind in Diskussion, eine Entscheidung liegt nicht vor. Jeder der drei Schnitte
  erzeugt eine andere Schnittstellenlast. Ich bitte darum, ihn nicht vor Punkt 5 der Voraussetzungen
  festzuschreiben.
- Beschreibung der Interimsarchitektur bis 31. Juli, verantwortlich IT-Applikationen (Frau Faber).
- Benennung der Datenverantwortlichen: Vorschlag aus dem Programm, Entscheidung Geschäftsführung.
- Abstimmung mit der Programmleitung (Frau Dr. Hartwig) und dem Teilprojekt ERP und Stammdaten
  (Herr Bensch) in der kommenden Woche.

Eine Bemerkung zum Schluss. Der Satz, das Programm sei technisch umsetzbar, ist im Haus mehrfach als
Entlastung der IT gelesen worden. Als solche nehme ich ihn nicht an. Er ist eine Aussage über
Software und keine über den Zustand, in dem wir nach dem Schnitt arbeiten werden.

Dr. Philipp Nowak
CIO
