---
doc_id: LTT-20230617-PROG-06
titel: "Lessons Learned: Erfahrungen aus der Einführung festhalten"
dokumenttyp: Lessons Learned
datum: 2023-06-17
verfasser: Oliver Bensch
rolle: Teilprojektleiter ERP und Stammdaten
organisationseinheit: Programm ONE LTT
empfaenger: ["-"]
projekt: IP-2023-03
geschaeftsbereich: "-"
vertraulichkeit: intern
informationsdomaene: [projektintern]
ablageort: projektlaufwerk
---

# Lessons Learned: Erfahrungen aus der Einführung festhalten

**Gegenstand:** Einführung der durchgängigen EBOM-MBOM-Struktur mit formeller Übergabe zwischen
Konstruktion und Produktion
**Verfasser:** Oliver Bensch, Teilprojektleiter ERP und Stammdaten, ONE LTT
**Stand:** Kassel, 17.06.2023
**Grundlage:** Übergabeprotokolle April und Mai 2023, ECR-Eingang, eigene Auswertung der
Materialstammanlage
**Ablage:** Projektlaufwerk / ONE LTT / Teilprojekt ERP und Stammdaten / Lessons Learned

## 1. Anlass und Abgrenzung

Frau Dr. Hartwig hat um eine Lessons-Learned-Aufstellung gebeten, obwohl die Umstellung noch läuft.
Sauber wäre, den Abschluss abzuwarten. Andererseits sind wir jetzt zehn Wochen im neuen Verfahren,
und die Leute erinnern sich noch daran, was im April tatsächlich passiert ist. In einem halben Jahr
erinnern sie sich an das, was sie inzwischen erzählt haben. Ich schreibe es deshalb jetzt auf.

Das hier ist die Sicht des Teilprojekts ERP und Stammdaten. Die Prozesssicht liegt bei Engineering
und Produktion, die Auswirkungen auf die Fertigung sind in der Management Summary vom 10.06.
dargestellt; die dortigen Zahlen wiederhole ich nicht, ich kommentiere sie unter Punkt 4.

## 2. Was funktioniert hat

Die formelle Übergabe selbst läuft technisch. Der Freigabeschritt, das Statusmodell und die
Übernahme der Struktur in die kaufmännische Welt tun das, was sie sollen. Das war der Teil, vor dem
ich am meisten Respekt hatte, und es ist der Teil, der am wenigsten Ärger gemacht hat.

Wichtiger als die Technik ist aus meiner Sicht das hier: Seit 2014 haben wir mechanische
Stücklisten im PLM, kaufmännische Stücklisten im ERP und die Projektunterlagen auf Netzlaufwerken.
Zwischen dem ersten und dem zweiten gab es neun Jahre lang keinen definierten Punkt, sondern
Gewohnheit. Diesen Punkt gibt es jetzt. Für die Migration ins Zielsystem ist das die Voraussetzung,
nicht ein Komfortgewinn - eine Stückliste, deren Übergabezeitpunkt niemand benennen kann, kann ich
auch nicht sauber übernehmen.

Die Key User in der Arbeitsvorbereitung waren gut vorbereitet. Herr Feld hat seine Leute vorher
durchgesprochen, das hat man in den ersten Wochen gemerkt.

## 3. Was nicht funktioniert hat

**a) Wir haben das Änderungsrecht nach der Übergabe nicht geklärt.** Die Produktion ändert die
technische Stückliste bis heute teilweise informell - Normteil getauscht, Länge angepasst,
Bezeichnung korrigiert. Vor dem 01.04. war das eine Arbeitsweise. Seit dem 01.04. ist es ein
Regelverstoß, ohne dass irgendjemand die Arbeitsweise ersetzt hätte. Wir haben eine Tür zugemacht
und keine zweite aufgemacht. Das ist kein Verhalten der Produktion, das ist ein Fehler in unserem
Einführungsdesign, und er geht auf meine Kappe mit.

**b) Es gibt nur einen Änderungsweg.** Ein falsch bemaßter Rohrbogen läuft durch denselben ECR wie
eine Änderung am Verdichteranschluss. Wir haben bewusst keine Ausnahme für Kleinstfälle vorgesehen,
weil die Beratung darauf bestanden hat, den Standardprozess nicht anzufassen - "Adopt before adapt".
Das Argument ist für die Zielarchitektur richtig. Für den Übergang war es falsch. Der Standardweg
ist nicht zu bürokratisch, er ist für den kleinen Fall schlicht zu lang.

**c) Die Schulung kam zu spät und war zu allgemein.** Wir haben das Verfahren erklärt und nicht die
zehn Fälle, die täglich vorkommen. Wer in der Schulung nicht seinen eigenen Fall gesehen hat, hat in
der ersten Woche danach jemanden angerufen statt das Formular zu benutzen.

**d) Wir haben die Wirkung auf den Materialstamm unterschätzt.** Dazu Punkt 5.

## 4. Zum Anstieg der dokumentierten Engineering Changes

Die Zahl ist seit April stark gestiegen, und sie wird gerade unterschiedlich gelesen. Engineering
liest sie als Beleg dafür, dass wir Bürokratie erzeugt haben. Die Produktion liest sie als Beleg
dafür, dass endlich sichtbar wird, was ohnehin die ganze Zeit passiert ist.

Ich halte die zweite Lesart im Kern für richtig, aber nicht vollständig. Ein großer Teil dieser
Änderungen ist nicht neu, sondern nur neu aufgeschrieben; früher wurden sie in der AV am Bildschirm
erledigt und tauchten nirgends auf. Wer den Anstieg für eine Verschlechterung hält, hat vorher nicht
gewusst, was in seinen eigenen Projekten passiert.

Ehrlicherweise gehört dazu aber auch: Ein Teil des Anstiegs ist echter neuer Aufwand. Wo die
Produktion früher eine Abweichung einfach gefertigt hat und die Konstruktionsstückliste danach nie
wieder angefasst wurde, muss die Abweichung jetzt zurückgeführt werden. Das ist Arbeit, die es
vorher nicht gab. Sie ist notwendig, aber sie ist real, und man sollte sie nicht wegreden.

Belastbar trennen kann ich die beiden Anteile nicht. Wir haben keinen Vorher-Wert für das, was
informell erledigt wurde - definitionsgemäß nicht. Genau deshalb streiten wir jetzt über die Deutung
einer Zahl, zu der es keinen Vergleichsmaßstab gibt.

Eine Erfahrung dazu, die älter ist als dieses Teilprojekt: Wir haben 2019 schon einmal eine Regel
eingeführt, die formal gilt und bei wichtigen Kunden umgangen wird - den Design Freeze. Der
Unterschied ist, dass der Design Freeze keine Systemwirkung hatte. Die formelle Übergabe hat eine.
Wer sie umgeht, erzeugt eine MBOM, die nicht zur Fertigung passt, und diese Struktur nehmen wir
später ins Zielsystem mit. Ein umgangener Design Freeze kostete Marge im laufenden Projekt. Eine
umgangene Übergabe kostet uns Datenqualität, die wir in der Migration bezahlen.

## 5. Auswirkungen auf Materialstamm und Migration

Wir haben konzernweit über 180.000 Materialnummern und das Ziel, die aktiven Materialstämme um
zunächst 40 Prozent zu reduzieren. Die formelle Übergabe arbeitet dagegen, solange sie nicht
geregelt ist: Jede übergebene Struktur legt Materialstämme an. Im Mai waren es aus den Übergaben
1.180 Stück, davon 412 projektspezifische Einmalteile, die mit hoher Wahrscheinlichkeit nie wieder
verwendet werden.

Das ist kein Argument gegen die Übergabe. Es ist ein Argument dafür, dass uns eine Regel fehlt, wann
ein Einmalteil überhaupt eine eigene Nummer bekommt und wann es als Position ohne Stamm geführt
wird. Die Stammdatenrichtlinie regelt seit April die Pflege, nicht die Entstehung. Das ist die
Lücke, und sie ist meine.

## 6. Was ich beim nächsten Rollout anders machen würde

1. Das Änderungsrecht nach der Übergabe klären, bevor die Übergabe scharf geschaltet wird. Nicht
   danach, nicht parallel.
2. Einen zweiten, kurzen Weg für Kleinständerungen vorsehen, mit klarer Abgrenzung, was klein ist.
   Lieber eine Ausnahme, die wir kontrollieren, als ein Telefonat, von dem wir nichts erfahren.
3. Die Anlageregel für Einmalteile vor der Umstellung schreiben.
4. Vorher festlegen, woran wir Erfolg messen wollen. Der teuerste Fehler auf dieser Liste ist nicht
   die fehlende Ausnahmeregel, sondern dass wir eine Kennzahl produziert haben, die niemand
   einordnen kann.
5. Nicht zwei Einführungen in dasselbe Quartal legen. Die Key User in der AV und im Vertrieb sind
   nicht dieselben, das Team von Frau Faber und das Programmteam schon. Im April und Mai haben
   dieselben fünf Leute die CRM-Einführung und uns bedient.

## 7. Offene Punkte

- Änderungsrecht an der MBOM nach der Übergabe: offen mit Herrn Feld und Herrn Gehrke, aus meiner
  Sicht eine Entscheidung für das Programmteam, nicht für die Teilprojekte.
- Ausnahmeregelung für Kleinständerungen: gehört fachlich zu Frau Dr. Sommer, ECR-seitig zur
  bestehenden Regelung.
- Anlageregel Einmalteile: Fortschreibung der Stammdatenrichtlinie, liegt bei mir.
- Herr Gehrke widerspricht meiner Darstellung unter Punkt 4 in Teilen; er sieht den Anteil des
  echten Mehraufwands höher als ich. Ich halte das hier fest, ohne es aufzulösen.

Diese Aufstellung ist ein Zwischenstand. Für Eisenach steht die Umstellung nach meinem Kenntnisstand
noch aus; ich schlage vor, die Punkte 1 bis 3 vorher abzuarbeiten und diese Liste danach
fortzuschreiben.

O. Bensch
