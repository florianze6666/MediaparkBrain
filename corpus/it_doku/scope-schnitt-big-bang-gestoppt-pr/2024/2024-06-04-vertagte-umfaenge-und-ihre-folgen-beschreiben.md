---
doc_id: LTT-20240604-IT-05
titel: Vertagte Umfänge nach dem Neuschnitt von ONE LTT und ihre Folgen
dokumenttyp: Management Summary
datum: 2024-06-04
verfasser: Dr. Philipp Nowak
rolle: CIO
organisationseinheit: IT
empfaenger: ["-"]
projekt: ONE LTT
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [management, projektintern]
ablageort: it_doku
---

Management Summary

Betreff: Vertagte Umfänge nach dem Neuschnitt von ONE LTT und ihre Folgen für die Systemlandschaft
Verfasser: Dr. Philipp Nowak, CIO, IT
Datum: 04.06.2024
Bezug: Neuschnitt ONE LTT (Juni 2024); Project Atlas Review (Mai 2024); Budgetübersicht des Controllings vom 29.05.2024
Einstufung: intern
Ablage: IT-Dokumentation, Programmakte ONE LTT

## 1. Sachstand

Anfang Juni ist der geplante Big-Bang-Go-live gestoppt und ONE LTT in Teilprogramme zerlegt worden.
Weitergeführt werden Finance, Procurement, CRM, Business Intelligence, Projektcontrolling und Teile
des Master Data Managements. Vertagt sind die vollständige PLM-ERP-Integration, die durchgängige
EBOM-MBOM-Automatisierung, der MES-Rollout in Eisenach und die konzernweite Serviceplattform.

Diese Zusammenfassung beschreibt nicht die Entscheidung, sondern das, was mit den vertagten Umfängen
tatsächlich passiert, solange nichts weiter entschieden wird. Der im März auf rund 19 Mio EUR
erhöhte Aufwand bezog sich auf den vollen Umfang; die kaufmännische Wirkung des Neuschnitts ist in
der Budgetübersicht des Controllings vom 29. Mai dargestellt und nicht Gegenstand dieses Papiers.

## 2. Was die vier vertagten Umfänge im Betrieb bedeuten

**PLM-ERP-Integration.** Stücklisten und Artikelstämme werden weiterhin zwischen der Siemens-PLM-
Plattform und der kaufmännischen Welt von Hand überführt. Die Doppelpflege bleibt, mit ihr die
bekannten Abweichungen zwischen dem, was die Konstruktion freigegeben hat, und dem, was der Einkauf
sieht. Für den Oktobertermin schrumpft die geplante Integration auf eine schmale Übergabe. Welches
Verfahren dabei offiziell gilt und wer es verantwortet, ist noch nicht festgelegt. Bis dahin läuft
die Materialstammbereinigung in einer Landschaft weiter, in der die führende Quelle für
Engineering-Daten nicht entschieden ist. Wir haben 2023 gesehen, wohin das führt: das Reduktionsziel
wurde von 40 auf 25 Prozent gesenkt, erreicht wurden rund 18 Prozent.

**EBOM-MBOM-Automatisierung.** Die formelle Übergabe zwischen Konstruktion und Produktion ist seit
April 2023 über POL-ENG-001 in der Fassung v1.1 verbindlich. Diese Pflicht bleibt bestehen, die
Automatisierung fällt weg. Das Ergebnis ist ein verbindlicher Prozess ohne Werkzeug: Der Aufwand
bleibt bei Konstruktion und Arbeitsvorbereitung, und Änderungen nach dem Design Freeze bleiben über
den Systemschnitt hinweg schwer nachverfolgbar. Aus meiner Sicht ist das der Umfang, dessen
Vertagung im Tagesgeschäft am schnellsten spürbar wird, weil er täglich anfällt.

**MES-Rollout Eisenach.** Der Standort arbeitet weiter mit der gewachsenen Werkzeugkette aus lokalen
Datenbanken und Tabellen. Damit bleibt auch die seit 2018 getrennte Systemwelt zwischen Kassel und
Eisenach so, wie sie ist. Zu beachten ist, dass der weitere Ausbau des Guss-Outsourcings Anfang des
Jahres gestoppt wurde: Die Fertigungsumfänge bleiben am Standort, der Bedarf an Feinsteuerung und
belastbaren Rückmeldedaten verschwindet also nicht, er wird nur nicht adressiert. Für das
weitergeführte Teilprogramm Business Intelligence heisst das konkret, dass Fertigungsdaten aus
Eisenach im konzernweiten Berichtswesen vorerst fehlen. Das sollte offen benannt werden, bevor die
ersten Auswertungen verteilt sind.

**Konzernweite Serviceplattform.** Disposition und Einsatzrückmeldung bleiben bei den heutigen
Mitteln, also Tabellen und der bestehenden Dokumentenablage. Die Vorarbeit aus der Anbieterbewertung
liegt vor und ist gegen die im Januar in Kraft getretene Cloud- und SaaS-Richtlinie POL-IT-003 v2.0
geprüft worden. Diese Vorarbeit sollte gesichert und nicht verworfen werden; sie verliert ihren Wert
in etwa zwei Jahren, nicht in zwei Monaten. Ein Interimsverfahren ist mit der Servicedisposition
(Frau Sandmann) und der Leitung Lifecycle & Service abzustimmen.

## 3. Der gemeinsame Punkt

Vier Umfänge sind vertagt, keiner ist abgesagt. In der Organisation wird beides gleich gelesen,
solange keine Wiedervorlage mit Datum existiert. Genau das ist mein Anliegen: Ein Zwischenzustand,
den niemand beschreibt, ist kein Zwischenzustand, sondern ein unbeschriebener Dauerzustand, für den
die IT später die Verantwortung zugeschrieben bekommt.

Deshalb halte ich drei Dinge für notwendig:

1. Je vertagtem Umfang ein benannter fachlicher Verantwortlicher und ein dokumentiertes
   Interimsverfahren, fertig vor dem Go-live-Termin im Oktober. Das ist wenig Arbeit, wenn es jetzt
   gemacht wird.
2. Besetzung der Datenverantwortung. Die Stammdatenrichtlinie POL-IT-006 gilt seit April 2023 und
   beschreibt Regeln; die Verantwortung für die Inhalte liegt in der Praxis weiterhin bei der
   IT-Applikationsbetreuung. Das Review hat die fehlende Datenverantwortung ausdrücklich benannt.
   Sie ist keine Frage des Programmumfangs und wird durch den Neuschnitt nicht kleiner.
3. Wiedervorlage mit festem Termin. Jeder vertagte Umfang wird zu einem gesetzten Zeitpunkt erneut
   mit Aufwand und Nutzen bewertet. Andernfalls entscheidet der Kalender, und das Ergebnis heisst
   erfahrungsgemäss "nicht mehr aktuell".

## 4. Bewertung aus IT-Sicht

Der Neuschnitt ist richtig. Die Programmbreite war das im Mai benannte Risiko, und sie ist jetzt
kleiner. Ich möchte aber vor einem Kurzschluss warnen: Wir haben den Umfang reduziert, nicht das
Problem. Die vier vertagten Themen sind genau die Stellen, an denen unsere Systemlandschaft seit 2018
auseinanderläuft. Sie kommen zurück, und sie kommen mit Zinsen zurück.

Ebenso wichtig: Die Ursachen, die das Review benannt hat, liegen nicht im vertagten Umfang. Unklare
Entscheidungsrechte, fehlende Datenverantwortung, geringe Verfügbarkeit der Key User und die
Belastung der Fachabteilungen wirken auf den weitergeführten Teil unverändert. Ein kleineres Programm
mit denselben Rahmenbedingungen ist ein kleineres Programm, kein sicheres. Die Verfügbarkeit der Key
User wird sich nicht von selbst verbessern; die Einstellungsbremse in District & Geo Energy und die
Auslastung im Engineering sprechen dagegen. Ich bitte darum, die zugesagten Key-User-Zeiten für die
Restlaufzeit verbindlich zu hinterlegen, statt sie monatlich neu zu verhandeln.

Für die Teilprogramme kursieren die Arbeitsbegriffe Digital Core, Engineering Backbone und Service
Transformation. Welcher Zuschnitt daraus wird und wo die vertagten Umfänge künftig geführt werden,
ist nicht entschieden; auch die Verteilung der Projektverantwortung wird derzeit neu bewertet. Die
Interimsverfahren sollten trotzdem nicht auf diese Klärung warten.

## 5. Grenzen dieser Einschätzung

Ob der Oktobertermin für den verbleibenden Umfang trägt, lässt sich vor der Integrationstestphase
nicht seriös sagen. Die Aussagen zu Aufwand und Budget sind der Darstellung des Controllings zu
entnehmen. Die Bewertung der fachlichen Folgen in Konstruktion, Fertigung und Service gebe ich aus
IT-Perspektive wieder; die betroffenen Bereiche werden sie in Teilen anders gewichten.
