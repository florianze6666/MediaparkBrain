---
doc_id: LTT-20230421-IT-01
titel: "Software-Evaluation CRM: Auswahl der CRM-Lösung für ONE LTT"
dokumenttyp: Software-Evaluation
datum: 2023-04-21
verfasser: Andrea Faber
rolle: Leiterin IT-Applikationen
organisationseinheit: IT
empfaenger: "-"
projekt: PRJ-CRM-2023
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [projektintern, bereichsintern]
ablageort: it_doku
---

# Software-Evaluation CRM

Lahnberg Thermotechnik GmbH & Co. KG, IT / Applikationen, Kassel

| | |
|---|---|
| Dokument-ID | LTT-20230421-IT-01 |
| Stand | Version 1.0 vom 21.04.2023 |
| Erstellt | Andrea Faber, Leiterin IT-Applikationen |
| Mitgewirkt | Jana Ostermann (Vertrieb), Ralf Steinke (Key Account Management), Maike Jansen (Vertrieb Benelux), Oliver Bensch (Teilprojekt ERP und Stammdaten), Sven Bruckner (Informationssicherheit), Sabine Kroll (Datenschutz), Dieter Anselm (Controlling) |
| Bezug | Projektauftrag PRJ-CRM-2023 vom 13.04.2023; Programm ONE LTT |
| Ablage | Projektakte PRJ-CRM-2023, gelenkt nach POL-QM-001 v2.0 |
| Verteiler | CIO, Programmleitung ONE LTT, Leitung Vertrieb, Controlling |

## 1. Anlass und Abgrenzung

Die Auswahl der CRM-Lösung wurde von Januar bis März 2023 im Teilprojekt Vertrieb des Programms ONE LTT
durchgeführt. Die Entscheidung ist Anfang April in der Programmlenkung bestätigt worden, der
Projektauftrag vom 13.04.2023 setzt die Einführung auf. Dieses Dokument hält die Bewertung fest, die der
Entscheidung zugrunde lag, und gehört als Entscheidungsgrundlage in die Projektakte.

Dass die Evaluation der Beauftragung nachläuft, ist dem Programmtakt geschuldet und nicht der Sache
angemessen. Ich halte das hier ausdrücklich fest, weil die Bewertung sonst später als nachträgliche
Begründung gelesen wird. Die Punktwerte in Abschnitt 5 stammen aus den Bewertungsrunden im Februar und
März und sind unverändert übernommen.

Nicht Gegenstand dieses Dokuments sind der Einführungsplan, der Schulungsumfang und die
Teilvereinbarung nach BV-2023-01. Sie werden im Teilprojekt bearbeitet.

## 2. Ausgangslage

Der Vertrieb arbeitet heute mit Outlook, Excel und persönlichen Notizen. Eine gemeinsame Sicht auf
Interessenten, laufende Angebote und den erwarteten Auftragseingang existiert nicht. Kunden- und
Interessentendaten liegen doppelt vor, weil Kassel und Eisenach mit unterschiedlichen ERP-Systemen
arbeiten und beide eigene Adressbestände führen.

Für das monatliche Forecast-Meeting werden die Zahlen in den Tagen davor zusammengetragen. Der Stand
kommt überwiegend aus persönlichen Listen der Key Account Manager; die Sorgfalt unterscheidet sich je
Key Account erheblich. Das Controlling gleicht Abweichungen im Nachgang aus, was Aufwand erzeugt und die
Nachvollziehbarkeit nicht verbessert.

Seit Jahresbeginn steht der Berichtsdienst der Microsoft-Plattform zur Verfügung. Er ist für die
Vertriebszahlen bisher ohne Nutzen, weil ihm die Quelle fehlt. Ein Bericht ist nicht besser als das
System, aus dem er liest.

Zielbild der Auswahl: erstmals eine konzernweite Sicht auf Pipeline, Kundenkontakte, Angebotsstatus und
erwarteten Auftragseingang, in einem System, aus dem Vertrieb, Controlling und Business Units denselben
Stand entnehmen.

## 3. Anforderungen

| Nr. | Anforderung | Einstufung |
|---|---|---|
| A1 | Gemeinsame Kunden- und Interessentenstruktur über beide Standorte | Muss |
| A2 | Verfolgung von Angeboten und Opportunities mit Wahrscheinlichkeit und erwartetem Auftragstermin | Muss |
| A3 | Anbindung an beide ERP-Systeme, Kunden- und Auftragsdaten zunächst nur lesend Richtung CRM | Muss |
| A4 | Auswertung über den vorhandenen Berichtsdienst, keine eigene Berichtswelt | Muss |
| A5 | Anmeldung über den vorhandenen Identitätsdienst, Rollen nach POL-IT-001 v2.0 | Muss |
| A6 | Nutzung im Standard nach dem Programmleitsatz Adopt before adapt, Erweiterungen nur mit Programmentscheid | Muss |
| A7 | Betrieb ohne zusätzliche Serverinfrastruktur, Cloud-Nutzung nach POL-IT-003 | Muss |
| A8 | Nachweise nach POL-IT-002 v2.0, Behandlung personenbezogener Daten nach BV-2023-01 | Muss |
| A9 | Mobiler Zugriff für Außendienst und Auslandsstandorte | Soll |
| A10 | Übernahme bestehender Kontaktdaten aus Outlook und den Excel-Listen | Soll |

## 4. Betrachtete Lösungen

In die Shortlist aufgenommen wurden drei Lösungen:

- **L1 - CRM-Modul der proALPHA-Suite.** Erweiterung des in Kassel eingesetzten ERP.
- **L2 - CRM-Komponente der Infor-Anwendung.** Erweiterung des in Eisenach eingesetzten ERP.
- **L3 - Microsoft Dynamics 365, Vertriebsmodul.** Eigenständige Anwendung innerhalb der bereits
  genutzten Microsoft-Plattform.

Reine CRM-Spezialanbieter wurden in der Marktsichtung betrachtet und nicht in die Shortlist übernommen.
Sie erfüllen A3 nur über zusätzliche Integrationsprojekte, und der Programmleitsatz spricht gegen eine
vierte eigenständige Systemwelt neben den beiden ERP und dem PLM.

Die Bewertung erfolgte in zwei Runden: Anforderungsabgleich anhand der Herstellerunterlagen, danach je
eine halbtägige Vorführung mit einem Fallbeispiel aus dem laufenden Anlagengeschäft, an der Vertrieb,
Controlling und IT gemeinsam teilgenommen haben.

## 5. Bewertung

Punkte 1 bis 5, 5 ist der beste Wert. Die Gewichtung wurde vor den Vorführungen festgelegt.

| Kriterium | Gewicht | L1 | L2 | L3 |
|---|---:|---:|---:|---:|
| Integration in die bestehende Systemlandschaft (Identitätsdienst, Kollaborationsplattform, Berichtsdienst) | 25 % | 3 | 2 | 5 |
| Abdeckung des Angebots- und Opportunity-Prozesses im Standard | 20 % | 3 | 3 | 4 |
| Anbindung an beide ERP-Systeme, Stammdatenfähigkeit | 20 % | 4 | 3 | 3 |
| Betrieb, Support und Aufwand für die Anwenderunterstützung | 15 % | 3 | 2 | 4 |
| Kosten über fünf Jahre | 10 % | 5 | 4 | 3 |
| Datenschutz, Informationssicherheit, Vertragslage | 10 % | 4 | 4 | 3 |
| **Gewichtete Summe** | | **3,50** | **2,80** | **3,85** |

Kosten über fünf Jahre, indexiert auf die günstigste Lösung: L1 = 100, L2 = 115, L3 = 140. Enthalten
sind Lizenzen, Einführungsaufwand einschließlich externer Unterstützung und der geschätzte Betriebs- und
Betreuungsaufwand meiner Abteilung. Nicht enthalten ist der Aufwand des Vertriebs für Datenpflege, weil
er sich nicht seriös schätzen lässt; er ist real und trägt niemand als Position.

Anmerkungen zu den Einzelwerten:

- **L1** ist bei der Anbindung an das Kasseler ERP unschlagbar und bei den Kosten ebenfalls. Der
  Vertriebsprozess wird jedoch aus dem Auftragsdenken heraus abgebildet: Eine Opportunity ohne Angebot
  ist dort ein Fremdkörper. Für Eisenach müsste eine zweite Anbindung gebaut werden, die niemand
  betreiben will.
- **L2** verliert deutlich bei der Integration. Die Anwendung ist an ihre eigene Umgebung gebunden, der
  Zugriff für Kassel wäre ein Sonderweg. Für ein System, das Standard sein soll, ist das der falsche
  Ausgangspunkt.
- **L3** gewinnt über die Integration und über den Betrieb. Anmeldung, Berechtigungen, mobiler Zugriff
  und Auswertung liegen in einer Umgebung, die wir seit 2020 betreiben und die die Anwender kennen. Der
  Preis dafür sind die höchsten Fünfjahreskosten und eine ERP-Anbindung, die in beide Richtungen gebaut
  werden muss.

Der Abstand zwischen L3 und L1 beträgt 0,35 Punkte. Das ist kein Erdrutsch. Verschiebt man die
Gewichtung der ERP-Anbindung um zehn Prozentpunkte zulasten der Integration, drehen sich die Plätze. Die
Entscheidung hängt damit sichtbar an der Frage, ob die Zielarchitektur mit einem ERP kommt oder mit
zweien. Das Programm beantwortet diese Frage mit einem ERP; unter dieser Annahme ist L3 richtig.

## 6. Ergebnis

Ausgewählt wurde L3, Microsoft Dynamics 365 mit dem Vertriebsmodul. Bestätigt in der Programmlenkung
Anfang April 2023, beauftragt mit dem Projektauftrag vom 13.04.2023.

Die Einführung erfolgt im Standard. Erweiterungen am Datenmodell und zusätzliche Felder werden nicht
über die IT beauftragt, sondern über den Programmentscheid nach A6. Eine gesonderte Investitionsvorlage
nach POL-FIN-002 ist nicht erforderlich, weil das Teilprojekt innerhalb des bewilligten Programmbudgets
geführt wird.

## 7. Auflagen und Risiken aus Sicht der IT-Applikationen

**R1 - Pflichtfelder gegen Vertriebszeit.** Der Standard bringt einen Pflichtfeldsatz mit. Reduzieren
wir ihn, verlieren wir die Vergleichbarkeit über die Business Units, und der Forecast bleibt so
uneinheitlich wie heute. Behalten wir ihn, kostet jede Opportunity Pflegezeit, die im Vertrieb derzeit
niemand eingeplant hat. Ich empfehle, die Disziplin nicht über die IT zu erzwingen, sondern über den
Forecast-Prozess: Was im System nicht steht, geht nicht in den Forecast ein. Ohne diese Kopplung wird
gepflegt, wenn Zeit ist, und das sind erfahrungsgemäß die Tage vor dem Forecast-Meeting. Die
Entscheidung darüber gehört in den Vertrieb und in das Controlling, nicht in mein Haus.

**R2 - Stammdaten.** Das CRM setzt auf Kundenstämmen auf, die im Master-Data-Projekt derzeit bearbeitet
werden. Der Schwerpunkt dort liegt auf den Materialstämmen, die Kundenstämme laufen mit. Werden die
Kontakte aus Outlook und den Excel-Listen vor der Bereinigung übernommen, importieren wir die Dubletten
in ein neues System und haben sie dort dauerhaft. Abzustimmen mit dem Teilprojekt ERP und Stammdaten;
maßgeblich ist POL-IT-006.

**R3 - Mitbestimmung ist der kritische Pfad, nicht die Technik.** Das CRM ist das erste System, das das
gestufte Verfahren der Rahmenvereinbarung BV-2023-01 vom 16.03.2023 vollständig durchläuft:
Unterrichtung, Systembeschreibung mit Datenkatalog, Teilvereinbarung vor Produktivsetzung,
Qualifizierungszusage, Evaluation nach zwölf Monaten. Aus der Vereinbarung zur Kollaborationsplattform
von 2020 ist bekannt, dass die Zweckbindung der entscheidende Punkt ist und nicht die Geschwindigkeit.
Ein CRM erzeugt Daten, aus denen sich Aktivität einzelner Personen ablesen lässt; wer diese Frage nicht
vorher klärt, klärt sie hinterher unter Termindruck. Ich empfehle, den Datenkatalog von uns vorzulegen,
statt ihn erfragen zu lassen, und die Auswertungslogik von Anfang an auf Vorgänge zu beziehen, nicht auf
Bearbeiter. Fachlich zuständig für die Abstimmung sind Datenschutz und Informationssicherheit; die
Systembeschreibung liefern wir.

**R4 - Doppelte Schnittstelle bis zur ERP-Konsolidierung.** Solange beide ERP-Systeme bestehen, laufen
zwei Anbindungen. Der Aufwand liegt bei meiner Abteilung und ist im Teilprojektplan bisher nicht als
eigene Position sichtbar. Ich bitte, ihn dort aufzunehmen, bevor die Ressourcenplanung des Programms
fortgeschrieben wird.

**R5 - Erwartungshaltung.** Das System liefert eine vollständige Pipeline-Struktur. Es liefert keine
belastbare Pipeline. Transparenz über den Prozess ist nicht Transparenz über den Markt. Die
Aussagekraft der Forecast-Zahlen hängt an der Pflegedisziplin und an der Qualität der Einschätzungen,
nicht an der Auswahlentscheidung. Das gehört in die Kommunikation zum Projektstart, damit später nicht
das System für Zahlen haftbar gemacht wird, die jemand eingetragen hat.

## 8. Nächste Schritte

| Schritt | Verantwortlich | Termin |
|---|---|---|
| Systembeschreibung und Datenkatalog für die Unterrichtung nach BV-2023-01 | IT-Applikationen | 12.05.2023 |
| Abstimmung Kundenstammbereinigung mit dem Teilprojekt ERP und Stammdaten | IT-Applikationen, Teilprojekt Stammdaten | Mai 2023 |
| Festlegung des Pflichtfeldsatzes und Kopplung an den Forecast-Prozess | Vertrieb, Controlling | Juni 2023 |
| Berechtigungskonzept nach POL-IT-001 v2.0 | IT-Applikationen, Informationssicherheit | Juni 2023 |
| Aufnahme des Doppelbetriebs der Schnittstellen in die Programmplanung | Programmleitung | mit der nächsten Fortschreibung |

Kassel, 21.04.2023

Andrea Faber
Leiterin IT-Applikationen
