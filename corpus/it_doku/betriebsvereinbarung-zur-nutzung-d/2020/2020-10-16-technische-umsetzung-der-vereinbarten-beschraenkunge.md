---
doc_id: LTT-20201016-IT-04
titel: Technische Umsetzung der in BV-2020-02 vereinbarten Beschränkungen
dokumenttyp: Management Summary
datum: 2020-10-16
verfasser: Karin Löbner
rolle: Leiterin IT
organisationseinheit: IT
empfaenger: ["-"]
projekt: IP-2020-01
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [bereichsintern, br-management-verhandlung]
ablageort: it_doku
---

Lahnberg Thermotechnik GmbH & Co. KG
Informationstechnik

Management Summary

Betreff: Technische Umsetzung der in BV-2020-02 vereinbarten Beschränkungen
Verfasserin: Karin Löbner, Leiterin IT
Datum: 16.10.2020
Einstufung: intern
Bezug: Betriebsvereinbarung BV-2020-02 vom 06.05.2020; Besprechung vom 06.10.2020

## 1. Ausgangslage

Die Kollaborationsplattform ist seit Anfang April produktiv, die Betriebsvereinbarung dazu wurde am
6. Mai unterzeichnet. Beides war in der damaligen Lage richtig, hat aber zur Folge, dass die
technische Absicherung der vereinbarten Beschränkungen erst im Sommer entstanden ist und in Teilen
bis heute nicht abgeschlossen ist. Nach der Besprechung vom 6. Oktober fasse ich zusammen, was
gesetzt ist, was das Produkt nicht hergibt und was ungeregelt bleibt.

Vorweg eine Klarstellung, weil sie in der Besprechung mehrfach durcheinandergegangen ist: Vereinbart
ist der Ausschluss der Auswertung, nicht der Ausschluss der Datenentstehung. Nutzungsdaten entstehen
beim Betrieb einer solchen Plattform zwangsläufig. Was wir regeln können, ist, wer sie sieht, in
welcher Form sie überhaupt dargestellt werden und wozu sie verwendet werden dürfen.

## 2. Was umgesetzt ist

Seit dem 12. Juni ist im Administrationsbereich von Microsoft 365 die Einstellung aktiv, die
Benutzer-, Gruppen- und Websitenamen in sämtlichen Nutzungsberichten verbirgt. Die Berichte zeigen
seitdem nur noch Platzhalter. Das ist aus meiner Sicht der wirksamste Einzelpunkt, weil er nicht an
einer Berechtigung hängt, sondern schon die Darstellung entpersonalisiert - er wirkt auch auf
Berichte, die Microsoft künftig ergänzt und die ich heute nicht kenne.

Die Rolle, die Nutzungsberichte aufrufen darf, ist auf zwei Personen begrenzt, Frau Faber und mich.
Führungskräfte haben sie nicht und bekommen sie nicht; die Standortadministration in Eisenach hat
sie ebenfalls nicht.

Die persönlichen Auswertungsdienste aus dem Lizenzumfang (MyAnalytics) sind für alle Benutzer
abgeschaltet. Das darüber hinausgehende Auswertungsprodukt des Herstellers (Workplace Analytics) ist
nicht lizenziert; ich werde es nicht beschaffen.

Anwendungen können sich Leserechte auf die Berichtsschnittstelle nicht mehr selbst einholen. Die
Zustimmung durch Benutzer ist deaktiviert, Registrierungen genehmige ich einzeln. Derzeit besteht
keine Registrierung mit Berichtsberechtigung.

Ein Verlauf des Anwesenheitsstatus wird nicht geführt. Das Produkt sieht dafür keinen Bericht vor,
und wir betreiben nichts, was einen solchen Verlauf mitschreiben würde.

## 3. Was technisch entsteht und nicht abstellbar ist

Anmeldeprotokolle im Identitätsdienst (Azure Active Directory), Aufbewahrung 30 Tage. Zweck:
Störungsbeseitigung und Erkennung fehlgeschlagener Anmeldeversuche. Das Überwachungsprotokoll von
Microsoft 365 zeichnet Administrationsvorgänge und Zugriffe auf, Aufbewahrung 90 Tage. Und
schliesslich die Inhalte selbst: Chatverläufe liegen in den Postfächern, Dateien in SharePoint.

Diese drei Bestände sind personenbezogen. Sie sind nicht Gegenstand der Berichtsfunktionen und
werden von uns nicht ausgewertet, aber sie existieren. Ich halte das ausdrücklich fest, damit
niemand später den Eindruck hat, die IT habe etwas verschwiegen.

## 4. Was nicht geregelt ist

a) Inhaltssuche. Microsoft 365 enthält im Security- und Compliance-Bereich eine Funktion (eDiscovery),
mit der sich Chat- und Postfachinhalte über den gesamten Mandanten durchsuchen lassen. Sie ist für
rechtliche Auseinandersetzungen gedacht und in BV-2020-02 nicht erwähnt. Abschalten kann ich sie
nicht, ich kann die Rolle nur vergeben oder nicht vergeben; derzeit hat sie niemand. Ich möchte nicht
in die Lage kommen, eine solche Suche auf mündliche Bitte hin durchzuführen. Notwendig ist eine
Regelung, wer sie beauftragen darf, in welcher Form und unter wessen Beteiligung. Bis dahin führe ich
sie ausschliesslich auf schriftliche Weisung der Geschäftsführung und nur gemeinsam mit Frau Kroll
aus.

b) Aufbewahrung. Für Chatnachrichten ist keine Löschfrist gesetzt, sie bleiben unbegrenzt liegen.
Das ist weder im Sinn der Vereinbarung noch im Sinn des Datenschutzes. Die Frage ist nicht technisch;
sie hängt davon ab, was das Haus aufbewahren will.

c) Eisenach. Die Plattform ist der erste Dienst, den beide Standorte gemeinsam nutzen - alles andere
ist getrennt. Aus der Aufbauphase im Frühjahr bestehen dort lokale Administratorkonten, die noch
nicht vollständig zurückgenommen sind. Eine Rückmeldung, welche davon noch gebraucht werden, steht
aus.

d) Datenschutz-Folgenabschätzung. Sie ist im April unterblieben. Frau Kroll und ich holen das nach;
einen Termin für den Abschluss kann ich noch nicht nennen.

## 5. Aufwand

Für die Nacharbeit unter Punkt 4 rechne ich bis Jahresende mit etwa zwölf Personentagen, überwiegend
bei den Applikationen. Sie sind in der Planung 2020 nicht enthalten und gehen zu Lasten der Arbeiten
am Berechtigungskonzept.

Hinzu kommt ein dauerhafter Punkt, den ich für 2021 anmelden werde. Der Hersteller ändert den
Funktionsumfang der Plattform laufend und ohne unser Zutun. Eine Auswertungsfunktion, die es heute
nicht gibt, kann in sechs Monaten vorhanden und voreingestellt aktiv sein. Wer zusagt, dass nicht
ausgewertet wird, sagt zu, das regelmässig zu prüfen. Ich schlage eine halbjährliche Durchsicht der
Einstellungen vor, gemeinsam mit Frau Kroll und mit kurzem Vermerk an den Betriebsrat. Aufwand je
Durchgang zwei bis drei Tage. Ohne diese Durchsicht ist die Zusage nach einigen
Produktaktualisierungen nur noch eine Behauptung.

## 6. Vorschlag

1. Schriftliche Regelung zur Inhaltssuche, vor Jahresende.
2. Entscheidung über Aufbewahrungsfristen für Chatverläufe durch Geschäftsführung und Personal.
3. Halbjährliche technische Durchsicht, Ergebnis als Vermerk an den Betriebsrat.
4. Rückführung der Eisenacher Administratorkonten bis 30.11.

Die Punkte 1 und 2 sind keine Entscheidungen der IT. Ich bereite sie vor und setze sie um; treffen
muss sie jemand anderes.

Karin Löbner
