---
doc_id: LTT-20251207-BUIH-05
titel: "Lessons Learned: Parallelnutzung mehrerer Systeme in der Projektabwicklung"
dokumenttyp: Lessons Learned
datum: 2025-12-07
verfasser: Nicole Brandt
rolle: Lead Project Manager Industrial Heat Systems
organisationseinheit: Industrial Heat Systems
empfaenger: [Project Excellence Office]
projekt: "-"
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [projektintern, bereichsintern]
ablageort: projektlaufwerk
---

# Lessons Learned: Parallelnutzung mehrerer Systeme in der Projektabwicklung

**Betrachtungsgegenstand:** Projektabwicklung Industrial Heat Systems, Januar bis November 2025
**Erstellt von:** Nicole Brandt, Lead Project Manager IHS
**Datum:** 07.12.2025
**Grundlage:** Projektleiterrunde IHS vom 02.12.2025, eigene Aufzeichnungen aus der Abwicklung von
Wärmerückgewinnung Stahlwerk USA und Standardanlage Lebensmittelproduktion
**Verteiler:** Project Excellence Office, Leitung Industrial Heat Systems

## 1 Anlass

Das Project Excellence Office sammelt Lessons Learned normalerweise am Projektende. Dieser Beitrag
kommt früher und bezieht sich nicht auf ein Projekt, sondern auf die Art, wie wir dieses Jahr
gearbeitet haben. Auslöser ist die laufende Bewertung des Transformationsstandes und die Eskalation
aus der Produktion vom 23.11.2025 zu weiter bestehenden Medienbrüchen. In beiden Diskussionen werden
zwei verschiedene Fragen vermischt: ob die Systeme laufen, und ob sich mit ihnen ein Projekt führen
lässt.

## 2 Was unstrittig ist

Finance bewertet das Programm zu rund 80 Prozent als erfolgreich. Der Vertrieb sieht im CRM einen
Fortschritt, Supply Chain bewertet die gewonnene Transparenz positiv. Rund 70 Prozent der
angestossenen Veränderungen sind wirksam geworden, häufig anders als ursprünglich geplant.

Ich widerspreche keiner dieser Aussagen. Aus meiner Sicht messen sie den Zustand der Systeme. Was sie
nicht messen, ist der Weg, den eine Information heute innerhalb eines Projekts zurücklegt.

Engineering hält viele der zugesagten Verbesserungen für nicht erreicht, die Produktion meldet
Medienbrüche. Beides ist ebenfalls richtig, und beides widerspricht den 80 Prozent nicht.

## 3 Beobachtung: wo ein Projekt heute geführt wird

Für ein laufendes Anlagenprojekt in unserer Business Unit verteilen sich die Führungsgrössen so:

| Führungsgrösse | Führendes System |
|---|---|
| Kosten, Bestellungen, Abrechnung | ERP (seit 10/2024) |
| Termine, Vorgangsnetz | MS Project |
| Statusbericht, zwölf Kennzahlen | Projekt-Dashboard |
| Änderungen nach Design Freeze | PLM, Engineering Change Request |
| Kundenkontakte, Angebots- und Nachtragsstand | CRM |
| Projektdokumentation | digitale Projektakte |
| Schaltschrankdokumentation | je Lieferant unterschiedlich, per E-Mail und E-CAD-Datei |
| Gesamtsicht auf das Projekt | Excel-Datei des Projektleiters |

Die letzte Zeile ist der eigentliche Befund. Es gibt kein System, in dem ein Projekt vollständig
vorkommt. Die Excel-Datei ist nicht Bequemlichkeit und auch keine Umgehung, sie ist der einzige Ort,
an dem Termin, Kosten, Änderungsstand und Lieferantenlage nebeneinander stehen.

Ich habe im Oktober für ein Projekt vier Wochen lang mitgeschrieben, wie viel Zeit auf reine
Übertragung entfällt: Werte aus einem System herausziehen, prüfen, in ein anderes eintragen,
Abweichung erklären. Es waren zwischen drei und fünf Stunden pro Woche. Die Zahl ist eine
Selbstaufschreibung aus einem Projekt und statistisch nichts wert, aber die anderen Projektleiter in
der Runde vom 02.12. nannten dieselbe Grössenordnung.

Bei den Schaltschränken kommt der Aufwand von aussen dazu. Wir arbeiten seit 2025 planmässig mit drei
Lieferanten - NordControl bei komplexen Grossanlagen, RheinMain Automation Systems bei den
standardisierten Systemen, ElektroPlan Süd als Ausweich. Die Aufteilung ist für die Kapazität richtig.
Für das Projekt bedeutet sie drei Dokumentationsstände, die niemand automatisch zusammenführt.

## 4 Lessons

**L1 - Eine Erfolgszahl beschreibt den Systemzustand, nicht den Arbeitsplatz.** Beide Bewertungen sind
zutreffend, weil sie unterschiedliche Dinge zählen. Wenn wir das nicht trennen, streiten wir künftig
weiter über Prozentwerte statt über Schnittstellen.

**L2 - Der Bruch entsteht nicht in einem System, sondern zwischen zweien, und für den Zwischenraum ist
keine Rolle benannt.** Für jedes einzelne System gibt es einen Verantwortlichen. Für die Übergabe von
Terminen aus dem Vorgangsnetz in den Statusbericht gibt es keinen. Sie fällt dem Projektleiter zu,
ohne dass das je entschieden worden wäre.

**L3 - Die EBOM-MBOM-Übergabe funktioniert, obwohl sie nicht automatisiert ist.** Sie hat auf beiden
Seiten einen Verantwortlichen, einen definierten Zeitpunkt und ein festgelegtes Format. Das war 2023
der meistkritisierte Teil der Einführung, und es ist heute die einzige Schnittstelle, an der ich nicht
nachtelefoniere. Nicht die Technik hat sie tragfähig gemacht, sondern die benannte Übergabe.

**L4 - Die Excel-Amnestie hat die Dateien sichtbar gemacht, aber nicht ersetzt.** Rund 60 Dateien
gelten seit dem Frühjahr als geschäftskritisch, sie haben nun Owner und Versionsstand. Das ist eine
Verbesserung gegenüber dem Zustand davor. Der Grund ihrer Existenz ist damit nicht beseitigt, und bei
den Projektkalkulationen wird er es auf absehbare Zeit auch nicht.

**L5 - Was 2024 zurückgestellt wurde, ist nicht verschwunden, sondern in die Projekte gewandert.** Der
Scope-Schnitt war für das Programm die richtige Entscheidung; ich habe ihn damals begrüsst. Die
Integrationsarbeit, die er herausgenommen hat, wird jetzt von Hand geleistet, nur ohne Budget und ohne
Ausweis. Sie taucht in keiner Programmbilanz auf, weil sie als Projektaufwand gebucht wird.

## 5 Empfehlungen

1. **Drei Schnittstellen benennen statt zehn zu automatisieren.** Für die drei häufigsten manuellen
   Übertragungen je ein Übergabeblatt nach dem Muster EBOM-MBOM: Verantwortlicher auf beiden Seiten,
   Zeitpunkt, Format. Aufwand gering, Wirkung sofort messbar.
2. **Kein zusätzliches Berichtsformat ohne Wegfall eines bestehenden.** Die Reduktion auf zwölf
   Kennzahlen im vergangenen Jahr war die spürbarste Entlastung seit langem. Das Dashboard hat einen
   Teil davon wieder aufgezehrt.
3. **Den Übertragungsaufwand einmal sauber erheben.** Vier Wochen, freiwillige Selbstaufschreibung,
   Auswertung auf Ebene der Business Unit. Ausdrücklich nicht aus Systemprotokollen und nicht je
   Projektleiter - die Betriebsvereinbarung zu den Projektkennzahlen vom Februar lässt das aus gutem
   Grund nur aggregiert zu, und ich möchte diese Diskussion nicht neu eröffnen. Für die Frage, um die
   es hier geht, reicht der Bereichswert.
4. **Die als geschäftskritisch eingestuften Projektdateien nach Ursache sortieren.** Krücke, weil eine
   Übergabe fehlt - oder Fachlogik, die in kein Zielsystem passt. Die erste Gruppe lässt sich
   abbauen, die zweite braucht einen dauerhaften Platz.

Ein eigenes Vorhaben schlage ich nicht vor. Die drei Plätze für Top-Priority-Change-Initiatives
unserer Business Unit sind belegt, und die Empfehlungen oben brauchen keinen.

## 6 Offene Punkte

- Ob sich die Terminübergabe zwischen Vorgangsnetz und ERP überhaupt technisch schliessen lässt, weiss
  ich nicht. Ich habe in diesem Jahr nicht nachgefragt.
- Ob Eisenach dieselben Brüche sieht, ist offen. Die Rückmeldung aus Compressor Systems steht noch aus.
- Die genannten drei bis fünf Stunden sind eine Schätzung aus einem Projekt und ersetzen Empfehlung 3
  nicht.

Nicole Brandt
Lead Project Manager, Industrial Heat Systems
