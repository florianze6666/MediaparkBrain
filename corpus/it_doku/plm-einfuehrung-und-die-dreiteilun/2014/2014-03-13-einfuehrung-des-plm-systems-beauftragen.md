---
doc_id: LTT-20140313-GF-00
titel: "Projektauftrag: Einführung des PLM-Systems"
dokumenttyp: Projektauftrag
datum: 2014-03-13
verfasser: Dr. Jens Mahlberg
rolle: technischer Geschäftsführer
organisationseinheit: GF
empfaenger: [Konstruktion mechanisch, Elektrotechnik und Automatisierung, Technology & Development, Controlling, Geschäftsführung]
projekt: IP-2014-01
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit, projektintern]
ablageort: it_doku
---

Lahnberg Thermotechnik GmbH & Co. KG, Kassel
Geschäftsführung Technik

# Projektauftrag IP-2014-01 - Einführung PLM/PDM

| | |
|---|---|
| Projekt-Nr. | IP-2014-01 |
| Projektbezeichnung | Einführung PLM/PDM |
| Auftraggeber | Dr. Jens Mahlberg, technische Geschäftsführung |
| Projektleitung | Martin Gehrke, Leiter Konstruktion mechanisch |
| Ausgestellt am | 13. März 2014 |
| Verteiler | Geschäftsführung, Konstruktion mechanisch, Elektrotechnik und Automatisierung, Technology & Development, Controlling, EDV |

## 1. Ausgangslage

Die Lizenzentscheidung für Teamcenter ist im Januar gefallen, die Ablösung unseres bisherigen PDM
damit beschlossen. Die Testinstallation steht. Was fehlt, ist ein Auftrag, der sagt, was wir bis zum
Jahresende tatsächlich produktiv haben wollen, und was nicht. Diesen Auftrag erteile ich hiermit.

Der Anlass ist bekannt. Zeichnungssätze und Konstruktionsstücklisten liegen heute teils im PDM, teils
in Projektordnern auf dem Netzlaufwerk, in mehreren Fassungen und ohne verlässliche Kennzeichnung des
freigegebenen Standes. In der Montage sind im vergangenen Jahr wiederholt Teile nach einem Stand
gefertigt worden, der in der Konstruktion längst überholt war. Bei jeder Nachkalkulation kostet es
uns Tage, den Zeichnungsstand zu rekonstruieren, auf dem eine Baugruppe tatsächlich beruht.

Hinzu kommt die Angebotsseite. Seit der technischen Angebotsreview für Projekte über 500.000 EUR
müssen wir nachweisen können, auf welchen Auslegungsdaten ein Angebot beruht. Nach dem Verlauf bei
Glaswerk Nord halte ich das für die wichtigere Lehre: nicht die Annahme war das Problem, sondern dass
sie nirgends nachvollziehbar abgelegt war. Für die Auslegungsunterlagen selbst löst dieses Projekt
das noch nicht - dazu unten Abschnitt 3.2 -, aber der Zeichnungs- und Stücklistenteil gehört
abgeräumt, bevor wir über den Rest reden.

Die mechanische Konstruktion arbeitet mit NX. Die enge Kopplung an Teamcenter war für die Auswahl
ausschlaggebend; wir kaufen hier keine Integrationsaufgabe ein, sondern nutzen eine, die der
Hersteller mitbringt. Genau darauf ist der Umfang dieses Projekts zugeschnitten.

## 2. Ziel

Zum 1. Oktober 2014 führt die mechanische Konstruktion ihre Zeichnungen, Modelle und
Konstruktionsstücklisten produktiv in Teamcenter. Für jedes Bauteil und jede Baugruppe ist der
freigegebene Stand eindeutig erkennbar, die Änderung ist datiert und einem Bearbeiter zugeordnet, und
die Konstruktionsstückliste wird von dort an das ERP übergeben.

Erfolg messe ich an drei Punkten: kein freigegebener Zeichnungsstand mehr außerhalb des Systems,
Übergabe der Konstruktionsstückliste an proALPHA ohne manuelle Nacherfassung, und ein Änderungsdienst,
der ohne Zuruf funktioniert.

## 3. Umfang

### 3.1 Enthalten

- Aufbau der Artikel-, Dokument- und Stücklistenstruktur in Teamcenter für die mechanische
  Konstruktion, einschließlich der standardisierten Baugruppen für Pumpengruppen,
  Rohrleitungssegmente und Wärmetauscherstationen.
- Freigabe- und Änderungsverfahren für Zeichnungen und Konstruktionsstücklisten, abgebildet nach der
  seit Januar geltenden Dokumentenlenkung POL-QM-001. Das Verfahren wird nicht neu erfunden, es wird
  im System abgebildet.
- Anbindung NX an Teamcenter im vom Hersteller vorgesehenen Umfang.
- Übergabe der Konstruktionsstückliste an das ERP proALPHA, in eine Richtung.
- Übernahme der Altdaten aus dem bisherigen PDM, beschränkt auf freigegebene Stände der laufenden und
  der seit 2012 abgewickelten Projekte. Ältere Bestände bleiben, wo sie sind.
- Schulung der Konstrukteure am Arbeitsplatz.

### 3.2 Nicht enthalten

Diese Abgrenzung ist der eigentliche Inhalt dieses Auftrags, deshalb steht sie hier ausdrücklich:

- **Kaufmännische Stücklisten und Artikelstamm bleiben im ERP führend.** proALPHA wird nicht
  angefasst. Wir bekommen damit zwei Stücklistenwelten, die über eine Schnittstelle zusammenhängen und
  nicht über ein gemeinsames Datenmodell. Das ist mir bewusst, und ich nehme es für dieses Jahr in
  Kauf.
- **Elektrotechnik und Automatisierung.** Herr Wiesner hat die Aufnahme der EPLAN-Datenhaltung
  angemeldet. Ich stelle sie zurück. Die Kopplung von EPLAN an Teamcenter ist ein eigenes Vorhaben mit
  eigenem Aufwand, und wenn wir es jetzt mit aufnehmen, wird bis Oktober keiner der beiden Bereiche
  produktiv. Wir sprechen darüber, wenn die Konstruktion läuft.
- **Verfahrenstechnische Auslegung und Berechnungsunterlagen**, einschließlich der Rechnungen aus
  Ansys. Sie bleiben auf dem Netzlaufwerk. Mir ist der Widerspruch zu Abschnitt 1 bewusst.
- **Projektdokumentation**: Terminpläne, Protokolle, Kundenspezifikationen und Schriftverkehr bleiben
  in den Projektordnern. MS Project und die Kostenlisten der Projektleiter werden nicht berührt.
- **Technology & Development.** Frau Dr. Ludwig hat für die Versuche mit natürlichen Kältemitteln eine
  versionierte Ablage angefragt. Der Bedarf ist berechtigt; der Bereich ist seit Januar im Aufbau und
  wird bis Oktober nicht auch noch eine Systemeinführung tragen. Zu prüfen nach dem Produktivstart.
- Fertigung, Montage und Service erhalten lesenden Zugriff, sonst nichts.

## 4. Ergebnisse

1. Datenmodell und Freigabeverfahren, dokumentiert und von der Konstruktionsleitung abgenommen.
2. Pilot an einer Baugruppenfamilie, durchgängig von der Konstruktion bis zur Stücklistenübergabe.
3. Übernommene Altdaten mit Protokoll über das, was nicht übernommen wurde.
4. Arbeitsanweisung für Konstrukteure, in die Dokumentenlenkung eingesteuert.
5. Produktivmeldung an die Geschäftsführung.

## 5. Organisation

Projektleitung Martin Gehrke, verantwortlich für Umfang, Termine und Ergebnisse, berichtet an mich.
Aus der Konstruktion sind drei Mitarbeiter fachlich zu benennen, aus der Arbeitsvorbereitung einer.
Die EDV stellt Installation, Betrieb und Datensicherung sicher; die dortige Zuständigkeit ist bis Ende
März schriftlich zu benennen, ich will nicht im Juni klären müssen, wer den Server verantwortet.
Einführungsunterstützung durch den Hersteller wird abgerufen, der kaufmännische Umfang liegt bei Herrn
Bergmann.

Die Elektrotechnik nimmt beratend an den Abstimmungen zum Datenmodell teil. Das ist keine Hintertür in
den Umfang, sondern soll verhindern, dass wir uns die spätere Anbindung verbauen.

## 6. Termine

| Meilenstein | Termin |
|---|---|
| Fachliche Benennung der Projektmitarbeiter, Zuständigkeit EDV | 31.03.2014 |
| Datenmodell und Freigabeverfahren abgenommen | 30.05.2014 |
| Pilot abgeschlossen | 18.07.2014 |
| Altdatenübernahme abgeschlossen | 12.09.2014 |
| Produktivstart mechanische Konstruktion | 01.10.2014 |

Der Produktivstart ist der Termin, an dem ich das Projekt messe. Verschiebt er sich, will ich das im
Juli hören und nicht im September.

## 7. Mittel und Kapazität

Lizenzen, Einführungsunterstützung und Hardware sind in der Investitionsplanung 2014 hinterlegt und
über die kaufmännische Geschäftsführung freigegeben. Die interne Kapazität begrenze ich: je benanntem
Mitarbeiter höchstens ein Tag je Woche, für die Projektleitung höchstens zwei. Wir haben ein volles
Auftragsbuch, und das Projekt darf keinen Liefertermin gefährden. Wenn der Rahmen nicht reicht, ist
der Umfang zu kürzen, nicht die Kapazität zu erhöhen.

## 8. Randbedingungen und Risiken

- Die Datenqualität der Altbestände ist ungeprüft. Ich erwarte, dass ein Teil der Zeichnungsstände
  nicht zweifelsfrei zuzuordnen ist. Solche Fälle werden nicht bereinigt, sondern gekennzeichnet und
  liegen gelassen.
- Wer heute seinen eigenen Ordner auf dem Laufwerk pflegt, wird ihn weiter pflegen, solange es geht.
  Nach dem Produktivstart gilt der Stand im System, sonst nichts. Die Projektleitung hat mir
  Doppelablagen zu melden.
- Die Schnittstelle zum ERP ist der technisch heikelste Punkt des Vorhabens. Sie wird am Pilot
  nachgewiesen, bevor Altdaten übernommen werden.
- Mit drei Datenwelten - PLM, ERP, Netzlaufwerk - bleibt eine Grenze quer durch die Produktdaten
  bestehen. Das ist gewollte Beschränkung dieses Auftrags, kein Versehen.

## 9. Berichtswesen

Monatlich eine Seite an mich: Stand, Abweichung, Entscheidungsbedarf. Bei Terminrisiko sofort. Zum
Produktivstart eine Auswertung des Aufwands gemeinsam mit Herrn Anselm.

## 10. Inkraftsetzung

Der Auftrag tritt mit Datum dieses Schreibens in Kraft. Änderungen am Umfang nach Abschnitt 3 bedürfen
meiner Zustimmung.

Kassel, 13. März 2014

Dr. Jens Mahlberg
Technische Geschäftsführung
