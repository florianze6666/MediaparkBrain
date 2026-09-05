---
doc_id: LTT-20140426-GF-01
titel: "Architekturentscheidung: Abgrenzung von PLM und ERP festlegen"
dokumenttyp: Architekturentscheidung
datum: 2014-04-26
verfasser: Dr. Jens Mahlberg
rolle: technischer Geschäftsführer
organisationseinheit: GF
empfaenger: []
projekt: IP-2014-01
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit, projektintern]
ablageort: it_doku
---

Lahnberg Thermotechnik GmbH & Co. KG
Technische Geschäftsführung

**Entscheidung der technischen Geschäftsführung Nr. 2014-02**
**Abgrenzung von PLM und ERP**

Az. TGF-2014-02
Kassel, 26. April 2014
Projekt IP-2014-01, Einführung PLM/PDM
Geltungsbereich: Konstruktion mechanisch, Elektrotechnik und Automatisierung, System Engineering,
Technology & Development, Fertigung, Einkauf, kaufmännische Verwaltung
Status: entschieden, gültig ab sofort. Gelenktes Dokument nach POL-QM-001.

---

## 1. Ausgangslage

Die Systeme stehen seit Januar. Die mechanische Konstruktion arbeitet seither produktiv im Teamcenter
und konstruiert im zugehörigen 3D-CAD (NX); der Projektauftrag vom 13. März 2014 hat die weitere
Einführung in das Projekt IP-2014-01 überführt. Das läuft technisch besser, als ich erwartet hatte.

Was nicht läuft, ist die Abgrenzung. Wir haben heute drei Ablagen für dieselbe Anlage. Die
Konstruktionsstückliste liegt im Teamcenter, die kaufmännische Stückliste im proALPHA, alles übrige
auf den Netzlaufwerken. Die Elektrotechnik zeichnet in EPLAN und liefert ihren Zeichnungssatz an
niemanden ab, der ihn systematisch führt. System Engineering rechnet in Excel. Die Projektleiter
führen ihre Termin- und Kostenlisten ohnehin selbst.

Solange jeder Bereich für sich arbeitet, fällt das nicht auf. Es fällt auf, sobald jemand von außen
fragt, welcher Stand gilt. Beim Angebotsreview ab 500.000 EUR nach POL-VTR-001 ist das inzwischen
jedes Mal der Fall: die Unterlage wird zusammengesucht, nicht abgerufen. Bei Glaswerk Nord war die
Anlage technisch in Ordnung, verloren gegangen ist die Marge an einer Wärmequellentemperatur, die
angenommen und nirgends niedergeschrieben wurde. Ein Review kann nur prüfen, was ihm vorliegt.

Ich entscheide deshalb jetzt die Abgrenzung, und zwar mit dem, was wir haben. Auf ein durchgängiges
Datenmodell zu warten, hiesse, ein Jahr zu warten. Das tue ich nicht.

## 2. Entscheidung

**2.1** Führende Quelle für die mechanische Produktstruktur ist das Teamcenter. Die dort freigegebene
Konstruktionsstückliste ist ab sofort die einzige gültige. Parallel geführte Stücklisten in Excel
werden nicht mehr fortgeschrieben.

**2.2** Führende Quelle für die kaufmännische Stückliste bleibt das proALPHA. Das ist mit Herrn
Bergmann so abgestimmt und steht hier nicht zur Diskussion. Übergabepunkt ist die Freigabe der
Konstruktionsstückliste, nicht ein beliebiger Konstruktionsstand. Eine Rückschreibung vom ERP in das
PLM findet nicht statt.

**2.3** Sachnummern werden weiterhin im proALPHA vergeben. Das PLM übernimmt sie und erzeugt keine
eigenen Nummernkreise. Wir haben nicht die Zeit, zwei Nummernsysteme zu pflegen.

**2.4** Produktbezogene Dokumente gehören in das Teamcenter, auch wenn sie nicht aus dem CAD stammen.
Dazu zählen Zeichnungssätze, Datenblätter der Zukaufkomponenten, Berechnungsnachweise einschliesslich
der Ansys-Auswertungen und Abnahmeprotokolle der Werkabnahme. Ein Festigkeits- oder Strömungsnachweis
ist ein Produktdokument und kein Projektdokument.

**2.5** Die dem Angebot zugrunde gelegten Prozessdaten des Kunden und die daraus abgeleiteten
Auslegungsannahmen werden als Auslegungsprotokoll im Teamcenter an der Anlage abgelegt, nicht im
Projektordner. Die Rechnung selbst darf in Excel bleiben; abzulegen ist das Ergebnis mit Datum,
Quelle der Eingangswerte und Verfasser. Fehlt die Quelle, wird das ausdrücklich vermerkt.

**2.6** Die Elektrotechnik bleibt bis auf Weiteres in EPLAN. Der freigegebene Schaltplansatz wird
jedoch als PDF in das Teamcenter eingestellt, damit die Anlagendokumentation an einer Stelle
vollständig ist. Herr Wiesner prüft bis zum 30. September 2014, was eine echte Kopplung kosten würde
und ob sie den Aufwand wert ist.

**2.7** Projektdokumente ohne Produktbezug bleiben vorerst auf dem Netzlaufwerk: Schriftverkehr,
Protokolle, Terminpläne, Nachträge, kaufmännische Vorgänge.

**2.8** Keine Doppelablage. Was im Teamcenter geführt wird, wird nicht zusätzlich auf dem Netzlaufwerk
abgelegt. Wer eine Kopie zum Arbeiten braucht, kennzeichnet sie als solche und löscht sie danach.

## 3. Was damit ausdrücklich nicht entschieden ist

Punkt 2.7 ist die schwächste Stelle dieser Entscheidung, und mir ist das bewusst. Wir haben für
Projektdokumente kein System, in das sie gehören würden, und ich baue jetzt keines nebenher. Damit
bleibt die Trennlinie zwischen Produkt- und Projektunterlage im Zweifel eine Auslegungssache des
Einzelnen. Wer sie nicht entscheiden kann, legt im Teamcenter ab; das ist die teurere, aber die
wiederauffindbare Seite.

Ebenfalls nicht entschieden: die verfahrenstechnische Auslegung selbst, die Projektplanung in MS
Project sowie die Frage, ob wir langfristig eine gemeinsame Struktur über mechanische und
elektrotechnische Daten legen. Das ist eine Grundsatzfrage und keine, die man im laufenden Rollout
mitentscheidet.

Der Betriebsrat ist über die Einführung unterrichtet. Auswertungen über einzelne Mitarbeiter sind aus
dem System nicht vorgesehen; ich habe Herrn Kalb zugesagt, dass wir sie auch nicht einrichten.

## 4. Umsetzung

| Punkt | Zuständig | Termin |
|---|---|---|
| 2.1, 2.4, 2.8 in der Konstruktion durchsetzen und die Altbestände sichten | M. Gehrke | 30.06.2014 |
| 2.2 und 2.3 technisch sauber schalten, gemeinsam mit der IT | IT mit M. Gehrke | 30.06.2014 |
| Gegenprüfung, ob die Nachkalkulation den neuen Übergabepunkt trägt | D. Anselm | 31.07.2014 |
| 2.5 mit System Engineering festlegen, Formblatt für das Auslegungsprotokoll | Dr. K. Ludwig | 31.07.2014 |
| 2.6 Kopplung E-CAD bewerten, Aufwand und Nutzen | R. Wiesner | 30.09.2014 |

Rückmeldung an mich formlos, aber schriftlich. Wo eine der Regeln in der Praxis nicht funktioniert,
will ich das im dritten Quartal hören und nicht im nächsten Jahr aus einem Angebotsreview.

Dr. Jens Mahlberg
Technische Geschäftsführung
