---
doc_id: LTT-20230912-IT-05
titel: "Security Assessment: Zugriffsrechte auf CRM-Daten bewerten"
dokumenttyp: Security Assessment
datum: 2023-09-12
verfasser: Sven Bruckner
rolle: Informationssicherheitsbeauftragter
organisationseinheit: IT
empfaenger: "-"
projekt: PRJ-CRM-2023
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [it-security-restricted, projektintern]
ablageort: it_doku
---

Lahnberg Thermotechnik GmbH & Co. KG
Informationssicherheit

**SECURITY ASSESSMENT ISB-2023-014**

| | |
|---|---|
| Prüfgegenstand | Berechtigungs- und Zugriffsmodell der CRM-Anwendung (Microsoft Dynamics 365), Teilprojekt CRM im Programm ONE LTT |
| Prüfzeitraum | 21.08.2023 bis 08.09.2023 |
| Prüfgrundlagen | POL-IT-001 v2.0, POL-IT-002 v2.0, POL-IT-003 v1.0, BV-2023-01, BV-2023-02, BV-2017-01 |
| Einstufung | intern |
| Stand | Kassel, 12.09.2023 |

## 1. Anlass

Seit der Teilvereinbarung vom 04.07.2023 dürfen Auswertungen aus dem CRM nur noch auf Ebene Team und
Region erfolgen. Wie diese Beschränkung im Berichtswesen umgesetzt wird, ist im Management Summary vom
29.08.2023 beschrieben.

Ich habe im Anschluss geprüft, ob das darunterliegende Zugriffsmodell diese Zusage überhaupt trägt.
Anlass ist kein Vorfall. Anlass ist die Beobachtung, dass die gesamte Diskussion der letzten Monate
über Berichte geführt wurde und nicht über Berechtigungen. Ein Bericht ist aber nur die bequemste Art,
an Daten zu kommen, nicht die einzige.

## 2. Prüfgegenstand und Abgrenzung

Geprüft wurden: die im Projekt angelegten Sicherheitsrollen und der Zuschnitt der Geschäftseinheiten,
die Zuordnung der Benutzerkonten über den zentralen Verzeichnis- und Identitätsdienst (Azure AD), die
Freigabe- und Zuweisungsmechanismen auf Datensatzebene, die Exportfunktionen, die persönlichen
Ansichten sowie die administrativen Konten.

Nicht geprüft wurden: die Berichtsmodelle im BI-Dienst über die Berechtigungsschicht hinaus, die
Auftragsverarbeitung mit dem Cloud-Anbieter (gesondertes Verfahren nach POL-IT-003), die
Schnittstellen zu den beiden ERP-Systemen und die Endgerätesicherheit.

Es wurde kein Penetrationstest durchgeführt und keine vollständige Rollenmatrix erhoben. Grundlage ist
eine Stichprobe von Benutzerkonten aus Kassel, Rotterdam und Houston sowie die Konfigurationsansicht.

## 3. Ausgangslage

Das CRM ist seit dem zweiten Quartal produktiv und bildet erstmals konzernweit Opportunities,
Kundenkontakte, Angebotsstände und den erwarteten Auftragseingang ab. Jede Opportunity trägt einen
Eigentümer, eine Aktivitätshistorie und einen Änderungsverlauf. Diese Angaben sind einer einzelnen
Person eindeutig zurechenbar; das ist keine Auslegungsfrage, sondern eine Eigenschaft des Datenmodells.

BV-2020-02 regelt die Kollaborationsplattform und deckt das CRM ausdrücklich nicht ab. Maßgeblich sind
die Rahmenvereinbarung BV-2023-01 und die Teilvereinbarung BV-2023-02.

## 4. Feststellungen

**F-01 - Die Auswertungsbeschränkung wirkt im Berichtsweg, nicht im Datenzugriff. Risiko: hoch.**

Die Beschränkung auf Team- und Regionsebene ist im Berichtsmodell umgesetzt und dort auch wirksam. Auf
Datensatzebene besitzt jeder Benutzer mit der Rolle Vertriebsmitarbeiter jedoch Lesezugriff auf
sämtliche Opportunities seiner Geschäftseinheit, einschließlich Eigentümer, Aktivitätshistorie und
Änderungsverlauf. Wer diese Datensätze über eine persönliche Ansicht filtert und nach Excel
exportiert, erzeugt in wenigen Minuten genau die personenbezogene Auswertung, die die Teilvereinbarung
ausschließt. Die Zusage ist derzeit vertraglich durchgesetzt, nicht technisch.

**F-02 - Die Exportberechtigung ist in allen fachlichen Rollen enthalten. Risiko: mittel.**

Der Export nach Excel ist Bestandteil aller im Projekt angelegten Sicherheitsrollen mit Ausnahme des
lesenden Controlling-Zugriffs. Das war eine bewusste Migrationsentscheidung: die Vertriebssteuerung
arbeitete vorher auf Tabellen, und der Export sollte den Übergang erleichtern. Als Übergangslösung war
das richtig, als Dauerzustand hebelt es F-01 auf. Mir ist bewusst, dass ein nachträglicher Entzug als
Rücknahme einer eingeführten Funktion wahrgenommen wird.

**F-03 - Administrative Konten sind von der Beschränkung nicht erfasst. Risiko: mittel.**

Die Systemadministration im CRM liegt bei zwei internen Konten in IT-Applikationen sowie bei Konten des
externen Implementierungspartners. Diese Konten haben unbeschränkten Lesezugriff auf alle Datensätze,
einschließlich Feldern, die im Fachzugriff ausgeblendet sind. BV-2023-02 adressiert Auswertungen, nicht
administrativen Zugriff. Das ist aus meiner Sicht keine Lücke der Vereinbarung, sondern eine Lücke
unseres eigenen Berechtigungskonzepts: POL-IT-001 v2.0 verlangt für privilegierte Konten eine
dokumentierte Begründung und eine periodische Überprüfung. Für das CRM liegt beides nicht vor. Die
externen Konten sind zudem unbefristet eingerichtet.

**F-04 - Die Hierarchiesicherheit stützt sich auf eine unvollständige Vorgesetztenstruktur. Risiko: mittel.**

Die Hierarchiesicherheit des Produkts gewährt Vorgesetzten Zugriff auf die Datensätze der ihnen
zugeordneten Mitarbeiter. Die zugrundeliegende Struktur ist aus dem Identitätsdienst übernommen und
bildet die Lage nach der Reorganisation in vier Business Units nur teilweise ab. In der Stichprobe
hatten zwei Benutzer Lesezugriff auf Datensätze von Mitarbeitern, für die sie fachlich nicht zuständig
sind. Ein Missbrauch ist nicht feststellbar, siehe F-05. Die Ursache liegt in den Stammdaten, nicht in
der Konfiguration des CRM; das Thema gehört fachlich zu POL-IT-006.

**F-05 - Die Überwachungsprotokollierung ist nicht aktiviert. Risiko: hoch, mit Zielkonflikt.**

Ohne Protokollierung lässt sich weder ein unberechtigter Lesezugriff feststellen noch die Einhaltung
von BV-2023-02 belegen. Mit Protokollierung entsteht ein Datenbestand, der selbst personenbezogen ist
und der nach dem Muster von BV-2017-01 nur zur Störungsbeseitigung und nur stichprobenfrei verwendet
werden dürfte.

Ich halte den vollständigen Verzicht für die schlechtere der beiden Varianten. Eine Vereinbarung, deren
Einhaltung niemand prüfen kann, schützt am Ende auch die Beschäftigten nicht, sondern verlagert die
Frage nur auf gegenseitiges Vertrauen. Mein Vorschlag ist eine eng umgrenzte Protokollierung: erfasst
werden Lesezugriffe auf fremde Opportunities und Massenexporte oberhalb einer festzulegenden Schwelle,
Aufbewahrung 90 Tage, Auswertung ausschließlich anlassbezogen und im Vier-Augen-Prinzip mit der
Datenschutzbeauftragten, kein Zugriff der Vertriebsorganisation auf das Protokoll. Das ist
mitbestimmungspflichtig und gehört als Ergänzung in die Teilvereinbarung, nicht in eine
IT-Konfiguration.

**F-06 - Die Beschränkung endet an der Betriebsgrenze. Risiko: mittel.**

BV-2023-02 gilt für die Betriebe Kassel und Eisenach. Die Kollegen in Rotterdam, Houston, Shanghai und
Brno arbeiten im selben Mandanten mit denselben Rollen, fallen aber nicht unter die Vereinbarung.
Datenschutzrechtlich bleiben sie geschützt, betriebsverfassungsrechtlich nicht. Für ein technisches
Zugriffskonzept ist eine an der Betriebszugehörigkeit hängende Regel ohnehin kaum sauber abbildbar -
POL-IT-001 v2.0 ist erkennbar für zwei deutsche Standorte geschrieben worden. Ich empfehle, die
Beschränkung einheitlich für den gesamten Mandanten zu konfigurieren, unabhängig davon, wo sie
rechtlich eingefordert werden kann. Abstimmungsbedarf mit Recht und Datenschutz.

## 5. Bewertung

Das CRM ist nicht unsicher konfiguriert. Für ein Vertriebssystem ist das Modell brauchbar und
weitgehend nach dem Prinzip der geringsten Rechte aufgesetzt. Es ist aber für eine andere Anforderung
konfiguriert worden als diejenige, die seit dem 04.07.2023 gilt. Zwischen dem, was die Teilvereinbarung
zusagt, und dem, was das System tatsächlich verhindert, liegt eine Lücke, die derzeit allein durch
Vertrauen und durch fehlende Übung der Anwender geschlossen wird. Für einige Wochen ist das
vertretbar. Als Zielzustand ist es das nicht.

Ich weise darauf hin, dass die Informationssicherheit an der Verhandlung zu BV-2023-02 nicht beteiligt
war. Die dort zugesagte Beschränkung ist technisch umsetzbar, aber sie ist nicht kostenfrei, und ein
erheblicher Teil der jetzt notwendigen Änderungen wäre bei früherer Beteiligung im Rollenentwurf
entstanden statt als Nacharbeit im laufenden Betrieb. Für die weiteren Teilvereinbarungen des Programms
halte ich eine Beteiligung vor der Unterzeichnung für zwingend, nicht für wünschenswert.

Zur intern geäußerten Kritik, die Vereinbarung schränke die Steuerungsfähigkeit ein: das ist keine
Sicherheitsfrage, sie berührt aber meine Empfehlungen. Auswertungen auf Team- und Regionsebene bleiben
vollständig möglich, ebenso Pipeline-, Forecast- und Trichterbetrachtungen. Was entfällt, ist der
Vergleich einzelner Mitarbeiter anhand der Pflegequalität ihrer Datensätze. Einen Sicherheitsgrund,
diese Möglichkeit zu erhalten, sehe ich nicht.

## 6. Empfohlene Maßnahmen

| Nr | Maßnahme | Verantwortlich | Termin | Priorität |
|---|---|---|---|---|
| M-01 | Rohdatenexport aus dem CRM auf definierte Rollen mit dokumentierter Begründung beschränken; Standardansichten auf aggregierte Ausgabe umstellen | IT-Applikationen | 31.10.2023 | hoch |
| M-02 | Sichtbarkeit personenbezogener Felder (Eigentümer, Aktivitätshistorie, Änderungsverlauf) über Feldsicherheitsprofile auf den eigenen Verantwortungsbereich und die Vertriebsleitung begrenzen | IT-Applikationen mit Vertrieb | 30.11.2023 | hoch |
| M-03 | Berechtigungskonzept CRM schriftlich fassen und als Anlage zur Systembeschreibung nach BV-2023-01 führen | Informationssicherheit | 31.10.2023 | hoch |
| M-04 | Privilegierte Konten inventarisieren, begründen und befristen; externe Konten mit Ablaufdatum; halbjährliche Überprüfung | IT-Applikationen, Informationssicherheit | 31.10.2023 | hoch |
| M-05 | Vorschlag zur zweckgebundenen Protokollierung erarbeiten und mit Recht und Datenschutz sowie anschließend mit dem Gesamtbetriebsrat erörtern | Informationssicherheit mit Datenschutzbeauftragter | 15.11.2023 | mittel |
| M-06 | Vorgesetztenstruktur im Identitätsdienst gegen die geltende Organisation abgleichen | IT, HR | 31.12.2023 | mittel |
| M-07 | Konfiguration nach M-01 und M-02 einheitlich auf alle Standorte anwenden | IT-Applikationen | 30.11.2023 | mittel |

## 7. Restrisiko und offene Punkte

Bis M-01 und M-02 umgesetzt sind, besteht die Möglichkeit einer personenbezogenen Auswertung fort. Das
Risiko einer bewussten Umgehung halte ich für gering. Das Risiko einer beiläufigen halte ich für nicht
gering: der wahrscheinliche Fall ist keine heimliche Analyse, sondern eine Excel-Liste, die sich jemand
für die eigene Übersicht baut und dann in einer Besprechung zeigt.

Ohne die unter F-05 beschriebene Protokollierung kann ich zum Jahresende nicht bestätigen, dass die
Beschränkung eingehalten wurde. Das betrifft auch die Evaluation nach zwölf Monaten, die BV-2023-01
vorsieht.

Die Termine für M-01 und M-02 stehen unter Ressourcenvorbehalt der IT-Applikationen. Die dortige
Kapazität ist überwiegend im Programm gebunden; eine Priorisierung gegen laufende Teilprojekte habe ich
nicht vorgenommen und kann sie auch nicht vornehmen.

Sven Bruckner
Informationssicherheitsbeauftragter

Verteiler: CIO, Leiterin IT-Applikationen, Datenschutzbeauftragte, Programmleitung ONE LTT, Leiterin
Vertrieb.
