---
doc_id: LTT-20240502-IT-02
titel: "Projektauftrag: Teilprogramme beauftragen"
dokumenttyp: Projektauftrag
datum: 2024-05-02
verfasser: Dr. Philipp Nowak
rolle: CIO
organisationseinheit: IT
empfaenger: "-"
projekt: ONE LTT
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [projektintern, management]
ablageort: projektlaufwerk
---

# Projektauftrag ONE LTT - Überführung in Teilprogramme

Programm: ONE LTT (PRJ-ONELTT)
Auftraggeber: Dr. Philipp Nowak, CIO
Fassung: 1.0 vom 02.05.2024
Verteiler: Programmleitung ONE LTT, benannte Teilprogrammleitungen, IT-Applikationen, Controlling,
Supply Chain, Vertrieb, Qualitätsmanagement, Standortleitung Eisenach
Status: freigegeben für die Umsetzungsvorbereitung. Der Zuschnitt des Gesamtprogramms wird derzeit
bewertet; dieser Auftrag steht insoweit unter dem Vorbehalt der Entscheidung der Geschäftsführung.

## 1. Anlass

Der für April vorgesehene Go-live wurde im März auf Oktober verschoben, und die Beratung hat den
erwarteten Programmaufwand von 14,8 auf rund 19 Mio. EUR angehoben. Der vom Beirat verlangte Project
Atlas Review liegt seit dieser Woche vor. Sein Kernbefund ist, dass das Programm technisch
grundsätzlich umsetzbar ist und das wesentliche Risiko nicht in der Software liegt, sondern in der
Organisation: zu viele parallele Transformationsvorhaben, geringe Verfügbarkeit der Key User,
fehlende Datenverantwortung, unklare Entscheidungsrechte, erhebliche lokale Prozessvarianten,
Überlastung der Fachabteilungen, zu große Programmbreite, unzureichende Change-Kommunikation.

Ich teile diesen Befund in der Sache, nicht in jeder Formulierung. Dass wir erhebliche lokale
Prozessvarianten haben, ist kein Ergebnis des Programms, sondern seine Ausgangslage - Kassel und
Eisenach arbeiten seit 2018 in getrennten Systemlandschaften, und diese Trennung war eine bewusste
Entscheidung. Für meinen Verantwortungsbereich ziehe ich aus dem Review vor allem eine Folgerung:
ein Vorhaben, das an der Aufnahmefähigkeit der Fachbereiche scheitert, wird nicht dadurch besser,
dass die IT es termingerecht bereitstellt. Die Programmbreite ist die Form, in der dieses Risiko bei
uns operativ wirksam wird, und sie ist der Teil, den wir selbst gestalten können.

Der bisherige Schnitt sieht einen gemeinsamen Stichtag für nahezu den gesamten Umfang vor. Diesen
Schnitt lege ich mit diesem Auftrag für die IT-seitige Umsetzung nicht weiter zugrunde.

## 2. Gegenstand und Ziel

ONE LTT wird in eigenständige Teilprogramme überführt. Jedes Teilprogramm erhält ein eigenes
Ergebnis, eine eigene Leitung, eine eigene Steuerung, eine eigene Datenverantwortung und einen
eigenen Termin. Es gibt keinen gemeinsamen Stichtag mehr, an dem alles gleichzeitig produktiv geht.

Ziel ist nicht, weniger zu erreichen, sondern das Erreichbare in eine Reihenfolge zu bringen, die
die Fachbereiche tragen können. Die Zielarchitektur bleibt unverändert.

## 3. Weitergeführte Teilprogramme

| Nr. | Teilprogramm | Gegenstand | Fachliche Leitung |
|---|---|---|---|
| TP-1 | Finance | Rechnungswesen, Kostenrechnung, Abschlussfähigkeit auf der neuen ERP-Basis | Dieter Anselm |
| TP-2 | Procurement | Beschaffungsprozess, Lieferantenportal, Anbindung des Beschaffungsnetzwerks der SAP SE (seit Januar in Betrieb) | Petra Ehlers |
| TP-3 | CRM | Ausbau der seit April 2023 produktiven CRM-Anwendung, Angebots- und Forecast-Prozess | Jana Ostermann |
| TP-4 | Business Intelligence | Datenplattform und Managementberichte auf Basis des BI-Dienstes | Andrea Faber |
| TP-5 | Projektcontrolling | Projektkosten, Projektmarge, Ressourcensicht nach POL-PM-003 v2.0 und POL-FIN-003 | Tobias Kern |
| TP-6 | Stammdaten | Materialstamm, Geschäftspartner, Kontenrahmen, Pflegeprozess nach POL-IT-006 | Oliver Bensch |

TP-6 wird auf den Umfang begrenzt, der für TP-1 bis TP-5 tatsächlich benötigt wird. Die vollständige
konzernweite Bereinigung des Materialstamms ist damit nicht abgeschlossen und bleibt als Aufgabe
bestehen; sie wird künftig im Regelbetrieb geführt und nicht als Programmleistung.

Der Termin im Oktober bleibt die Zielmarke für TP-1 und für den Stammdatenumfang, der dafür
notwendig ist. Für TP-2 bis TP-5 legen die Teilprogrammleitungen bis zum 28.06.2024 eigene Termine
vor. Ein Termin, der nur deshalb gehalten wird, weil er einmal genannt wurde, hilft uns nicht.

## 4. Vertagte Vorhaben

| Vorhaben | Begründung | Wiedervorlage |
|---|---|---|
| Integration PLM und ERP | Umfang und Datenqualität in den Produktdaten sind derzeit nicht belastbar geschätzt | Q1 2025 |
| Automatisierung der EBOM-MBOM-Überleitung (PRJ-EBOM-MBOM-2023) | die formelle Übergabe nach POL-ENG-001 v1.1 bleibt vorerst manuell | Q1 2025 |
| MES-Rollout Eisenach | setzt eine stabile ERP-Basis am Standort voraus | Q2 2025 |
| Konzernweite Serviceplattform | ohne Stammdaten- und Projektbasis kein tragfähiger Nutzen | Q2 2025 |

Vertagt heißt vertagt. Ich lege Wert darauf, dass diese vier Vorhaben mit Datum in der
Programmdokumentation bleiben und zum genannten Zeitpunkt bewertet werden. Meine Sorge ist nicht
theoretisch: Wenn die PLM-ERP-Integration liegen bleibt, bleibt auch die Systemgrenze bestehen, die
seit 2014 quer durch unsere Produktdaten verläuft, und wir pflegen die mechanische Stückliste und
die kaufmännische Stückliste weiter getrennt. Das ist eine bewusst getroffene Zwischenentscheidung
und kein gelöstes Problem.

## 5. Steuerung, Entscheidungsrechte, Datenverantwortung

- Jedes Teilprogramm erhält einen eigenen Lenkungskreis mit monatlicher Taktung. Teilnehmer sind die
  fachliche Leitung, die IT-Applikationen, das Controlling und der jeweils betroffene Fachbereich.
- Entscheidungen innerhalb des beauftragten Umfangs trifft der Lenkungskreis des Teilprogramms.
  Alles, was Umfang, Termin oder Aufwand eines anderen Teilprogramms berührt, geht an die
  Programmleitung. Genehmigungen richten sich unverändert nach POL-FIN-001 v2.0.
- Je Datenobjekt wird eine namentlich benannte Datenverantwortung festgelegt: Materialstamm,
  Geschäftspartner, Kundenstamm, Kontenrahmen, Projektstruktur. Ohne diese Benennung startet das
  betreffende Teilprogramm nicht. Der Review hat die fehlende Datenverantwortung ausdrücklich
  benannt, und ich habe keine Absicht, diesen Punkt ein zweites Mal zu lesen.
- Die Statusberichterstattung erfolgt je Teilprogramm nach POL-PM-002 v1.1. Ich erwarte, dass die
  Zerlegung die Statusbilder zunächst verschlechtert, weil jedes Teilprogramm seine Probleme künftig
  selbst ausweist, statt sie im Programmdurchschnitt zu verlieren. Das ist beabsichtigt.
- Die Programmleitung ONE LTT bleibt bei Dr. Simone Hartwig und verantwortet die Schnittstellen
  zwischen den Teilprogrammen, den gemeinsamen Terminplan und die Berichterstattung an die
  Geschäftsführung.

## 6. Ressourcen

Bis zum 28.06.2024 legt jede Teilprogrammleitung vor:

1. die namentlich benannten Key User mit dem vereinbarten Freistellungsanteil, bestätigt durch die
   jeweilige Fachbereichsleitung,
2. die Aufwandsabgrenzung des Teilprogramms als Anteil an der aktuellen Gesamtschätzung von rund
   19 Mio. EUR, getrennt nach interner Leistung, Beratung und Lizenz- beziehungsweise Betriebskosten,
3. den Terminplan bis zur Produktivsetzung.

Eine Freistellungszusage ohne Prozentangabe nehme ich nicht an. Zusätzliche externe Kapazität ist
über eine Investitionsvorlage nach POL-FIN-002 v1.1 zu beantragen; die dort seit Januar geforderte
Betrachtung der Betriebskosten über die Laufzeit ist in jedem Teilprogramm mitzuführen und nicht
erst zum Abschluss zu erstellen.

## 7. Mitbestimmung

Jedes Teilprogramm durchläuft das gestufte Verfahren der Rahmenvereinbarung BV-2023-01
eigenständig: Unterrichtung vor Beginn, Systembeschreibung mit Datenkatalog, Teilvereinbarung vor
Produktivsetzung, Qualifizierungszusage, Evaluation nach zwölf Monaten. Für das CRM gilt zusätzlich
die bestehende Teilvereinbarung BV-2023-02.

Die Zerlegung erhöht die Zahl der Verfahren, sie ersetzt sie nicht. Der Gesamtbetriebsrat hat im
März darauf hingewiesen, dass die Qualifizierungszusage unabhängig vom verschobenen Termin
fortbesteht, und nach dem Stand der Schulungsplanung gefragt. Die Teilprogrammleitungen stimmen ihre
Qualifizierungsplanung bis zum 28.06.2024 mit der Personalabteilung ab, damit wir auf diese Frage
eine belastbare Antwort geben können.

## 8. Risiken dieses Zuschnitts

- Mit sechs Teilprogrammen entstehen Schnittstellen, die vorher programmintern waren. Insbesondere
  hängen TP-1, TP-2 und TP-5 vom Fortschritt in TP-6 ab.
- Die Zahl der Vorhaben, die auf einen Fachbereich zugreifen, sinkt durch die Zerlegung nicht. Sie
  wird nur anders geschnitten. Wenn die Freistellungen nach Abschnitt 6 nicht kommen, haben wir das
  Problem des Reviews unverändert, nur in kleineren Einheiten.
- Vertagte Vorhaben werden erfahrungsgemäß leiser, je länger sie vertagt sind. Abschnitt 4 ist
  deshalb mit Datum versehen.
- Der Oktober bleibt eng. Er ist erreichbar, wenn TP-1 und TP-6 Vorrang vor allem anderen haben, und
  das bedeutet, dass TP-3 und TP-4 in den kommenden Monaten langsamer vorankommen werden, als es
  ihre Fachbereiche erwarten.

## 9. Freigabe

Ich beauftrage die Teilprogramme TP-1 bis TP-6 in dem oben beschriebenen Umfang und bitte die
benannten Leitungen, die Unterlagen nach Abschnitt 6 bis zum 28.06.2024 vorzulegen. Die vier in
Abschnitt 4 aufgeführten Vorhaben werden bis zur jeweiligen Wiedervorlage nicht weiter bearbeitet.

Änderungen an diesem Auftrag erfolgen schriftlich über die Programmleitung.

Kassel, 02.05.2024

Dr. Philipp Nowak
CIO
