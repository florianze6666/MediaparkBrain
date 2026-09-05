---
doc_id: LTT-20250419-IT-00
titel: Owner und Versionskontrolle für kritische Tabellen
dokumenttyp: SOP
datum: 2025-04-19
verfasser: Andrea Faber
rolle: Leiterin IT-Applikationen
organisationseinheit: IT
empfaenger: ["-"]
projekt: Excel Amnesty
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [unternehmensweit]
ablageort: qm_lenkung
---

# SOP-IT-014 - Owner und Versionskontrolle für kritische Tabellen

Gelenktes Dokument nach POL-QM-001 v2.0

| | |
|---|---|
| Dokumentnummer | SOP-IT-014 |
| Version | 1.0 |
| Erstellt am | 19.04.2025 |
| Gültig ab | 01.05.2025 |
| Ersteller | Andrea Faber, Leiterin IT-Applikationen |
| Geprüft | Bernd Hoffmann, Leiter Qualitätsmanagement |
| Freigegeben | Dr. Philipp Nowak, CIO |
| Nächste Überprüfung | 30.04.2026 |

**Geltungsbereich:** alle Organisationseinheiten der LTT an den Standorten Kassel und Eisenach. Für
Brno, Rotterdam, Houston und Shanghai gilt diese SOP ab Vorliegen der englischen Fassung; bis dahin
melden diese Standorte über die jeweilige Standortleitung an IT-Applikationen.

**Mitgeltende Unterlagen:** POL-IT-005 v1.0 (Excel- und Schattenanwendungs-Governance),
POL-IT-001 v3.0 (Zentrale Benutzerverwaltung und Rollenkonzept), POL-IT-006 v1.0
(Stammdatenrichtlinie), POL-QM-001 v2.0 (Dokumentenlenkung), BV-2023-01 (Rahmenvereinbarung
Einführung und Änderung von IT-Systemen).

---

## 1. Zweck

Diese SOP regelt, wie eine als geschäftskritisch eingestufte Tabelle betrieben wird, solange sie
betrieben wird: wer sie verantwortet, wo sie liegt, wie Änderungen nachvollziehbar bleiben und wer
Zugriff hat. Sie setzt POL-IT-005 in ein Verfahren um.

In der Meldephase der Excel Amnesty sind mehr als 430 Dateien gemeldet worden, rund 60 davon sind
als geschäftskritisch eingestuft. Die Auswertung der Meldungen hat einen einfachen Befund ergeben:
Der überwiegende Teil dieser Dateien wird von genau einer Person gepflegt, und in mehreren Fällen war
zum Zeitpunkt der Meldung nicht eindeutig zu klären, welche der kursierenden Fassungen die gültige
ist. Das ist das eigentliche Risiko, nicht das Werkzeug.

Diese SOP verbietet Excel nicht und schränkt die Nutzung von Tabellen für die persönliche
Arbeitsorganisation nicht ein.

## 2. Geltungsbereich und Abgrenzung

Diese SOP gilt für alle Tabellen, die nach Abschnitt 4 als geschäftskritische Schattenanwendung
eingestuft sind, unabhängig vom Speicherort und unabhängig davon, ob eine Überführung in ein
zentrales System vorgesehen ist.

Nicht Gegenstand dieser SOP sind:

- lokale Hilfsmittel im Sinne von Abschnitt 3,
- Auswertungen, die vollständig aus einem zentralen System erzeugt und dort auch berichtet werden,
- die Entscheidung, welche der eingestuften Dateien in ein zentrales System überführt wird. Diese
  Entscheidung wird je Datei im Rahmen der Excel Amnesty getroffen und ist zum Stand dieser SOP
  nicht abgeschlossen. Bis zu einer Entscheidung gilt die Datei als geschäftskritische
  Schattenanwendung und wird nach dieser SOP betrieben.

## 3. Begriffe

**Lokales Hilfsmittel.** Eine Tabelle, deren Ergebnis ausschließlich von der erstellenden Person oder
innerhalb eines Teams verwendet wird und deren Verlust die Arbeit dieser Person oder dieses Teams
verzögert, aber keinen Prozess außerhalb davon anhält. Lokale Hilfsmittel unterliegen keiner Melde-,
Owner- oder Versionspflicht.

**Geschäftskritische Schattenanwendung.** Eine Tabelle, die eine Funktion erfüllt, die fachlich in
einem zentralen System liegen müsste oder ein solches System ersetzt, und deren Ausfall,
Fehlberechnung oder Versionsverwechslung einen Geschäftsprozess außerhalb der erstellenden Einheit
beeinträchtigt. Typische Kategorien aus der Meldephase: Projektkalkulationen, Lieferterminlisten,
Ressourcenpläne, Inbetriebnahmechecklisten, Ersatzteilmatrizen, Angebotskonfiguratoren,
Berechnungstools.

**Owner.** Die namentlich benannte Person, die fachlich für Inhalt, Richtigkeit und Aktualität einer
geschäftskritischen Schattenanwendung einsteht. Der Owner ist keine IT-Rolle.

**Gültige Fassung.** Diejenige Fassung, die am festgelegten Ablageort liegt. Jede andere Kopie ist
eine Arbeitskopie ohne Verbindlichkeit.

## 4. Einstufung

### 4.1 Kriterien

Die Einstufung erfolgt anhand von fünf Kriterien:

| Nr. | Kriterium |
|---|---|
| K1 | Das Ergebnis der Datei geht in eine Entscheidung oder eine Zusage außerhalb der erstellenden Einheit ein. |
| K2 | Ein Ausfall der Datei oder ihres Betreuers verzögert einen laufenden Prozess um mehr als fünf Arbeitstage. |
| K3 | Das Ergebnis fließt in ein Angebot, einen Auftrag, eine Bestellung, eine Abnahme oder eine Rechnung ein. |
| K4 | Für die Funktion existiert im vorhandenen zentralen System eine Standardfunktion, die nicht genutzt wird. |
| K5 | Die Datei enthält personenbezogene Daten oder Daten, die einer Person eindeutig zurechenbar sind. |

Trifft mindestens eines der Kriterien K1 bis K3 zu, ist die Datei eine geschäftskritische
Schattenanwendung. K4 ist kein Einstufungskriterium, sondern kennzeichnet die Datei für die Prüfung
nach Abschnitt 9. K5 löst das Verfahren nach Abschnitt 8 aus.

### 4.2 Verfahren

1. Die Einstufung schlägt der Fachbereich vor, in dem die Datei geführt wird.
2. IT-Applikationen prüft den Vorschlag auf Vollständigkeit und auf Doppelmeldungen und trägt das
   Ergebnis in das Verzeichnis kritischer Tabellen ein.
3. Bei unterschiedlicher Auffassung entscheidet die Leitung der betroffenen Organisationseinheit
   gemeinsam mit der Leiterin IT-Applikationen. Kommt keine Einigung zustande, entscheidet der CIO.
4. Eine Neubewertung erfolgt bei jeder wesentlichen Änderung des Anwendungszwecks, mindestens jedoch
   im Rahmen der halbjährlichen Überprüfung nach Abschnitt 10.

Neu entstehende Dateien werden vom Fachbereich vor der ersten produktiven Nutzung gemeldet. Eine
nachträgliche Meldung ist ausdrücklich zulässig und wird nicht sanktioniert; die Amnestieregelung aus
der Meldephase gilt fort.

## 5. Owner und Vertretung

### 5.1 Benennung

Für jede geschäftskritische Schattenanwendung benennt die Leitung der verantwortlichen
Organisationseinheit schriftlich einen Owner und eine Vertretung. Owner und Vertretung sind
verschiedene Personen und gehören dem Fachbereich an, der die Datei nutzt.

IT-Applikationen übernimmt keine Owner-Rolle für fachliche Inhalte. Die Abteilung stellt Ablage,
Zugriffssteuerung, Versionierung und Auskunft über das Verzeichnis; die Richtigkeit einer Kalkulation,
einer Terminliste oder einer Auslegungsformel kann sie nicht beurteilen und verantwortet sie nicht.

Der Zeitbedarf der Owner-Rolle ist von der Führungskraft bei der Kapazitätsplanung zu berücksichtigen.
Auf die entsprechende Anmerkung des Gesamtbetriebsrats vom 13.02.2025 wird verwiesen.

### 5.2 Pflichten des Owners

Der Owner

- hält die Datei am festgelegten Ablageort aktuell und pflegt keine parallele Zweitfassung,
- dokumentiert die fachliche Logik der Datei in einem Blatt "Beschreibung" innerhalb der Datei:
  Zweck, Datenquellen, wesentliche Annahmen, bekannte Einschränkungen,
- führt das Änderungsprotokoll nach Abschnitt 6.3,
- gibt Änderungen an Rechenlogik oder Struktur vor der Freigabe der neuen Fassung der Vertretung zur
  Kenntnis,
- meldet IT-Applikationen unverzüglich einen Wechsel der Zuständigkeit, spätestens vier Wochen vor
  einem geplanten Wechsel,
- bestätigt halbjährlich, dass die Einstufung und die Angaben im Verzeichnis noch zutreffen.

### 5.3 Wechsel und Vakanz

Scheidet ein Owner aus seiner Rolle aus, ohne dass ein Nachfolger benannt ist, übernimmt die
Vertretung kommissarisch für längstens drei Monate. Ist nach drei Monaten kein Owner benannt, meldet
IT-Applikationen die Datei an die Leitung der Organisationseinheit und an das Qualitätsmanagement. Eine
geschäftskritische Schattenanwendung ohne Owner wird nicht weiter genutzt.

## 6. Ablage und Versionskontrolle

### 6.1 Ablageort

Jede geschäftskritische Schattenanwendung liegt in der dafür eingerichteten Bibliothek "Kritische
Tabellen" auf SharePoint, in der Struktur der verantwortlichen Organisationseinheit. Netzlaufwerke,
lokale Laufwerke und persönliche Ablagen sind als Ablageort der gültigen Fassung nicht zulässig.

Die Versionierung der Bibliothek ist aktiviert und wird nicht abgeschaltet. Frühere Fassungen werden
nicht gelöscht.

### 6.2 Benennung

Der Dateiname folgt dem Muster

`<Kürzel Einheit>_<Kurzbezeichnung>_v<Hauptversion>.<Nebenversion>.xlsx`

Beispiel: `IHS_Projektkalkulation_v3.2.xlsx`. Datumsangaben, Namenszusätze wie "final", "neu" oder
"Stand" und Initialen im Dateinamen sind nicht zulässig.

Die Hauptversion wird erhöht, wenn sich Struktur oder Rechenlogik ändern, die Nebenversion bei
inhaltlicher Aktualisierung ohne Strukturänderung.

### 6.3 Änderungsprotokoll

Jede Datei enthält ein Blatt "Änderungen" mit Datum, Version, ändernder Person, Art der Änderung und,
bei Änderungen der Rechenlogik, dem Grund. Das Protokoll wird nicht gekürzt.

### 6.4 Weitergabe

Die Weitergabe an Empfänger außerhalb der zugriffsberechtigten Gruppe erfolgt als schreibgeschützte
Kopie mit Versionsangabe oder als PDF. Eine per E-Mail versandte Datei ist nie die gültige Fassung.
Wird die Datei einem Kunden oder Lieferanten übergeben, gilt zusätzlich POL-QM-001 v2.0.

## 7. Zugriffsrechte

Der Zugriff wird ausschließlich über Gruppen der zentralen Benutzerverwaltung nach POL-IT-001 v3.0
vergeben, nicht über Einzelfreigaben. Der Owner beantragt die Gruppenzugehörigkeit und bestätigt sie
halbjährlich. Schreibrechte erhalten Owner und Vertretung; weitere Schreibberechtigte werden im
Verzeichnis begründet.

## 8. Personenbezogene Daten

Trifft Kriterium K5 zu, informiert der Owner vor der weiteren Nutzung die Datenschutzbeauftragte. Die
Prüfung, ob eine Teilvereinbarung nach BV-2023-01 erforderlich ist, veranlasst IT-Applikationen
gemeinsam mit Recht und Datenschutz. Bis zum Abschluss dieser Prüfung wird die Datei nicht auf einen
größeren Nutzerkreis ausgeweitet und werden keine Auswertungen daraus erstellt, die einzelne Personen
ausweisen.

Dass eine Tabelle keine Namensspalte enthält, ist kein Nachweis dafür, dass K5 nicht zutrifft. Eine
Zuordnung über Projekt-, Auftrags- oder Ressourcennummern kann denselben Bezug herstellen.

## 9. Prüfung auf Überführung in ein zentrales System

Für Dateien, bei denen Kriterium K4 zutrifft, prüft IT-Applikationen gemeinsam mit dem Fachbereich, ob
die Funktion mit vorhandenem Standardumfang in SAP S/4HANA, Teamcenter, Dynamics 365 oder der
Berichtsumgebung abgebildet werden kann. Ergebnis der Prüfung ist eine der drei Aussagen:

1. Überführung mit Standardfunktion möglich - Aufnahme in die Planung der jeweiligen
   Anwendungsbetreuung.
2. Überführung nur mit Erweiterung oder Schnittstellenentwicklung möglich - Vorlage als
   Änderungsantrag; ohne beauftragtes Vorhaben erfolgt keine Entwicklung.
3. Überführung derzeit nicht sinnvoll - die Datei bleibt eine geschäftskritische Schattenanwendung und
   wird nach dieser SOP betrieben.

Die Aussage 3 ist ein zulässiges Ergebnis und keine Ausnahme. Der Grundsatz "Stabilisieren vor
transformieren" gilt auch hier: eine kontrolliert betriebene Tabelle ist einer halbfertigen Ablösung
vorzuziehen.

## 10. Überprüfung

IT-Applikationen führt das Verzeichnis kritischer Tabellen und stellt es der Geschäftsführung sowie
dem Qualitätsmanagement halbjährlich zur Verfügung. Berichtet werden: Anzahl der geführten Dateien,
Anzahl ohne bestätigten Owner, Anzahl mit offener Prüfung nach Abschnitt 8, Anzahl der im
Berichtszeitraum überführten Dateien.

Stichprobenhaft prüft das Qualitätsmanagement im Rahmen der internen Audits Ablage, Benennung und
Änderungsprotokoll von jeweils fünf Dateien.

## 11. Verantwortlichkeiten

| Aufgabe | Verantwortlich | Mitwirkend |
|---|---|---|
| Meldung und Einstufungsvorschlag | Fachbereich | IT-Applikationen |
| Benennung von Owner und Vertretung | Leitung der Organisationseinheit | - |
| Inhalt, Aktualität, Änderungsprotokoll | Owner | Vertretung |
| Verzeichnis, Ablage, Versionierung, Zugriffsgruppen | IT-Applikationen | Fachbereich |
| Prüfung nach Abschnitt 8 | IT-Applikationen | Recht und Datenschutz |
| Prüfung auf Überführung | IT-Applikationen | Fachbereich, Anwendungsbetreuung |
| Audit und Dokumentenlenkung | Qualitätsmanagement | - |
| Entscheidung bei Dissens | CIO | Leitung der Organisationseinheit |

## 12. Änderungshistorie

| Version | Datum | Änderung | Ersteller |
|---|---|---|---|
| 1.0 | 19.04.2025 | Erstausgabe, Umsetzung von POL-IT-005 v1.0 | A. Faber |
