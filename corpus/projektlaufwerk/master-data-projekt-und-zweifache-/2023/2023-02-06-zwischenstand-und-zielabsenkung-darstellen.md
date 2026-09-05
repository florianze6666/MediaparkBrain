---
doc_id: LTT-20230206-PROG-01
titel: Materialstammbereinigung - Zwischenstand und Absenkung des Reduktionsziels
dokumenttyp: Management Summary
datum: 2023-02-06
verfasser: Oliver Bensch
rolle: Teilprojektleiter ERP und Stammdaten
organisationseinheit: Programm
empfaenger: ["-"]
projekt: IP-2023-02
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [projektintern, management]
ablageort: projektlaufwerk
---

Lahnberg Thermotechnik GmbH & Co. KG
Programm ONE LTT - Teilprojekt ERP und Stammdaten

**Management Summary: Materialstammbereinigung**

Projekt IP-2023-02, Master-Data-Projekt PRJ-MDM-2023
Grundlage: Projektauftrag vom 24.01.2023
Stand: 6. Februar 2023
Verfasser: O. Bensch, Teilprojektleitung ERP und Stammdaten
Einstufung: intern, Ablage Projektakte

## 1. Kernaussage

Die erste konzernweite Auswertung beider Materialstammbestände liegt seit dem 02.02. vor. Sie
bestätigt die im Projektauftrag beschriebene Lage in Umfang und Struktur, sie widerlegt aber die
Erreichbarkeit des dort genannten Reduktionsziels von 40 Prozent. Ich schlage vor, das Ziel auf
25 Prozent der aktiv geführten Materialstämme abzusenken und den Schwerpunkt des Teilprojekts von der
Bestandsbereinigung auf den migrationsrelevanten Kern zu verlagern. Ohne diese Anpassung binden wir
Fachbereichskapazität an Altmaterial, das die Zielarchitektur ohnehin nicht erreicht.

## 2. Ausgangslage

Kassel und Eisenach führen ihre Materialstämme seit 2018 getrennt, in zwei ERP-Systemen mit
unterschiedlicher Nummernsystematik, unterschiedlichen Einheitenschlüsseln und unterschiedlicher
Benennungspraxis. Ein Teil der Eisenacher Materialhistorie liegt ausserhalb des ERP in gewachsenen
Access-Datenbanken und Excel-Listen. Mechanische Stücklisten stehen im PLM, kaufmännische im
jeweiligen ERP; Elektrotechnik und Verfahrenstechnik arbeiten wieder anders. Die Bereinigung ist
deshalb keine Systemarbeit, sondern zu grossen Teilen fachliche Beurteilung durch Menschen, die die
Teile kennen.

Für die Zielarchitektur gilt der Grundsatz "Adopt before adapt". Jede Materialnummer, die wir
mitnehmen, muss auf die Klassifikationssystematik des Standards abgebildet werden. Damit ist nicht
die Zahl der gelöschten Stämme die entscheidende Grösse, sondern die Zahl der Stämme, die in die
Migration gehen.

## 3. Ergebnis der ersten Auswertung

Extraktion durch IT-Applikationen (A. Faber), Auswertung im Teilprojekt.

| Kennzahl | Wert |
|---|---:|
| angelegte Materialnummern gesamt | 183.400 |
| davon Kassel | 131.900 |
| davon Eisenach | 51.500 |
| mit Sperr- oder Auslaufkennzeichen | 37.200 |
| **aktiv geführt** | **146.200** |

Struktur des aktiven Bestands; die Mengen überschneiden sich und dürfen nicht addiert werden:

| Merkmal | Materialnummern |
|---|---:|
| projektspezifische Einmalteile ohne Wiederverwendung | 61.300 |
| ohne Warenbewegung seit mehr als fünf Jahren | 52.800 |
| ohne durchgängige Klassifikation, nur Freitextbenennung | 39.000 |
| maschinell erkannte Dublettencluster (6.100 Cluster) | 14.200 |
| in beiden Systemen doppelt geführte Gleichteile | 7.300 |

Bezogen auf die 146.200 aktiven Stämme entspricht das Ziel aus dem Projektauftrag rund 58.500
Materialnummern, die zu sperren oder zu löschen wären.

## 4. Warum 40 Prozent nicht tragfähig sind

**Die Einmalteile sind nicht frei verfügbar.** Von den 61.300 projektspezifischen Einmalteilen sind
rund 38.400 in Anlagen verbaut, für die Gewährleistung läuft oder für die wir Ersatzteile schulden.
Lifecycle & Service (M. Aurich) hat dem Löschen dieser Positionen in der Abstimmung am 01.02.
widersprochen, und ich halte den Widerspruch für berechtigt. Unsere Anlagen laufen zwanzig Jahre und
länger; eine Nummer, die wir heute aus Aufräumgründen entfernen, fehlt uns beim nächsten
Verdichterschaden.

**Die maschinelle Erkennung trägt nur zur Hälfte.** Wegen der uneinheitlichen Benennung arbeitet die
Dublettensuche über Sachmerkmale und Freitext. Von 400 stichprobenweise geprüften Clustern haben sich
219 bestätigt. Alles Weitere ist Einzelfallprüfung durch Konstruktion, Arbeitsvorbereitung, Einkauf
und Service.

**Der Zielwert ist vor der Auszählung entstanden.** Die 40 Prozent stammen aus der
Programmvorbereitung im vierten Quartal und beruhen auf einer Erfahrungsschätzung der externen
Beratung. Eine Auswertung des tatsächlichen Bestands lag damals nicht vor. Das ist kein Vorwurf, aber
wir sollten die Zahl jetzt gegen die Daten stellen und nicht die Daten gegen die Zahl.

**Eisenach braucht mehr Zeit als Kassel.** Ein erheblicher Teil der dortigen Positionen ist nur über
Zeichnungsnummern einer Verdichterbaureihe zuzuordnen. Die Beurteilung hängt an wenigen Personen mit
langer Standortkenntnis. A. Puhl hat für Februar und März zwei Mitarbeiter zugesagt, mehr ist neben
dem laufenden Geschäft nicht darstellbar.

## 5. Vorschlag

1. **Reduktionsziel 25 Prozent** der aktiv geführten Stämme, das sind rund 36.500 Materialnummern,
   Stichtag der Messung 31.10.2023.
2. **Trennung von Sperren und Löschen.** Vorrang hat das Setzen eines belastbaren Sperr- und
   Auslaufstatus. Physisch gelöscht wird nur, was weder Bewegung noch Serviceverpflichtung noch
   Stücklistenverwendung aufweist.
3. **Migrationsfilter statt Vollbereinigung.** In die Migration gehen Materialien mit Bewegung in den
   letzten 36 Monaten, alle Plattform- und Modulteile nach POL-ENG-002 sowie alle Positionen mit
   laufender Serviceverpflichtung. Der Rest bleibt bis zur Abschaltung im Altsystem lesbar.
4. **Benennungs- und Klassifikationsregel vor der Massenbereinigung.** Ohne verbindliche Regel
   erzeugen wir im neuen System dieselbe Freitextlage wie im alten. Entwurf liegt Ende Februar vor,
   Abstimmung mit M. Gehrke, R. Wiesner und N. Feld ist terminiert.

## 6. Aufwand und Voraussetzungen

Nach maschineller Vorfilterung verbleiben rund 21.000 Positionen zur fachlichen Einzelbeurteilung.
Gerechnet mit sechs Minuten je Position ergeben sich etwa 2.100 Stunden oder 265 Personentage. Über
acht Monate verteilt entspricht das rund zwei Vollzeitkräften aus Konstruktion, Arbeitsvorbereitung,
Einkauf und Service.

Diese Kapazität ist derzeit nicht zugesagt. Die Bereiche, aus denen sie kommen müsste, sind dieselben,
die die laufenden Kundenprojekte tragen. Ich kann die Bereinigung nicht gegen die Projektarbeit
priorisieren, und ich werde es auch nicht versuchen. Wenn die Kapazität nicht freigegeben wird, ist
auch das abgesenkte Ziel nicht zu halten; dann brauchen wir eine dritte Entscheidung darüber, was wir
stattdessen weglassen.

## 7. Entscheidungsbedarf

An die Programmleitung (Dr. S. Hartwig):

- Absenkung des Reduktionsziels von 40 auf 25 Prozent und Aufnahme des Stichtags 31.10.2023 in die
  Programmberichterstattung.
- Freigabe von zwei Vollzeitäquivalenten aus Konstruktion, Arbeitsvorbereitung, Einkauf und Service
  für den Zeitraum März bis Oktober.
- Bestätigung, dass Materialien mit laufender Serviceverpflichtung von der Löschung ausgenommen sind.

Ich bitte um Entscheidung bis zum 24.02.2023, damit die Fachbereichsprüfung im März anlaufen kann.
Bis dahin arbeitet das Teilprojekt an der Klassifikationsregel und der Abstimmung der
Nummernüberführung weiter; diese Arbeiten sind von der Zielfrage unabhängig.

O. Bensch
