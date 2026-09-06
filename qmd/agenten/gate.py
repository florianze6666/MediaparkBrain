"""Completeness Gate (FR-08) gegen die fuenfzehn Mindestangaben aus PLAN.md Abschnitt 2.

Regel (08_orchestrator.md Abschnitt 4): Fuer jede Angabe muss eine Ueberschrift
existieren, mit oder ohne Nummerierung, und der Abschnitt darf nicht mit
"Informationsluecke" markiert sein. Ein Antrag darf aus mehreren Dateien bestehen
(Steckbrief plus Business Case); geprueft wird die Vereinigung ihrer Abschnitte.

Aufruf aus qmd/:
    uv run python agenten/gate.py <antrag.md> [<antrag2.md> ...]
Exit 0 bestanden, Exit 3 nicht bestanden (wie der Orchestrator).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# (Bezeichnung, Muster auf der normalisierten Ueberschrift)
MINDESTANGABEN: list[tuple[str, str]] = [
    ("Projektname", r"projektname"),
    ("Beschreibung des Vorhabens", r"beschreibung"),
    ("Zielsetzung", r"zielsetzung|\bziele?\b"),
    ("Fachlicher und organisatorischer Nutzen",
     r"(fachlich|organisatorisch)\w*.*nutzen|nutzen.*(fachlich|organisatorisch)"),
    ("Betroffene Geschaeftsprozesse", r"geschaeftsprozess"),
    ("Betroffene Organisationseinheiten", r"organisationseinheit"),
    ("Business Case", r"business.?case|wirtschaftlichkeit"),
    ("Erwartete Kosten", r"kosten|investition"),
    ("Erwarteter wirtschaftlicher Nutzen", r"wirtschaftlich\w*.*nutzen|nutzenrechnung|einsparung"),
    ("Geplante Laufzeit / Einfuehrungszeitraum", r"laufzeit|einfuehrungszeitraum|zeitplan"),
    ("Bekannte technische Abhaengigkeiten", r"technisch\w*.*abhaengigkeit"),
    ("Bekannte organisatorische Abhaengigkeiten", r"organisatorisch\w*.*abhaengigkeit"),
    ("Risikoanalyse", r"risiko"),
    ("Begruendung des Vorteils fuer die Organisation", r"begruendung"),
    ("Anbieter-, Produkt- oder Projektinformationen",
     r"anbieter|produktinformation|projektinformation"),
]

LUECKEN_MARKER = re.compile(r"informationsluecke")
UEBERSCHRIFT = re.compile(r"^(#{1,3})\s+(.+?)\s*$")
NUMMERIERUNG = re.compile(r"^\s*\d+(\.\d+)*[.)]?\s*")

_UMLAUTE = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "Ä": "ae", "Ö": "oe", "Ü": "ue"})


def normalisiere(text: str) -> str:
    return text.translate(_UMLAUTE).lower()


@dataclass
class Abschnitt:
    datei: str
    ueberschrift: str
    ebene: int
    text: str


@dataclass
class GateErgebnis:
    bestanden: bool
    gefunden: dict[str, str] = field(default_factory=dict)      # Angabe -> Ueberschrift
    fehlend: list[dict] = field(default_factory=list)            # {angabe, grund, ueberschrift?}
    dateien: list[str] = field(default_factory=list)

    def als_dict(self) -> dict:
        return {
            "bestanden": self.bestanden,
            "dateien": self.dateien,
            "gefunden": self.gefunden,
            "fehlend": self.fehlend,
        }


def abschnitte(pfad: Path) -> list[Abschnitt]:
    """Zerlegt eine Markdown-Datei in Abschnitte ab Ueberschriften der Ebenen 1 bis 3.
    Ein Abschnitt reicht bis zur naechsten Ueberschrift gleicher oder hoeherer Ebene."""
    zeilen = pfad.read_text(encoding="utf-8", errors="replace").splitlines()
    koepfe: list[tuple[int, int, str]] = []  # (zeilenindex, ebene, text)
    im_frontmatter = False
    for i, z in enumerate(zeilen):
        if i == 0 and z.strip() == "---":
            im_frontmatter = True
            continue
        if im_frontmatter:
            if z.strip() == "---":
                im_frontmatter = False
            continue
        m = UEBERSCHRIFT.match(z)
        if m:
            koepfe.append((i, len(m.group(1)), m.group(2)))
    out: list[Abschnitt] = []
    for k, (start, ebene, titel) in enumerate(koepfe):
        ende = len(zeilen)
        for start2, ebene2, _ in koepfe[k + 1:]:
            if ebene2 <= ebene:
                ende = start2
                break
        out.append(Abschnitt(
            datei=pfad.name,
            ueberschrift=NUMMERIERUNG.sub("", titel).strip(),
            ebene=ebene,
            text="\n".join(zeilen[start + 1:ende]),
        ))
    return out


def pruefe(pfade: list[Path]) -> GateErgebnis:
    alle: list[Abschnitt] = []
    for p in pfade:
        if not p.exists():
            raise FileNotFoundError(f"Antragsdatei fehlt: {p}")
        alle.extend(abschnitte(p))

    ergebnis = GateErgebnis(bestanden=True, dateien=[str(p) for p in pfade])
    for angabe, muster in MINDESTANGABEN:
        rx = re.compile(muster)
        treffer = [a for a in alle if rx.search(normalisiere(a.ueberschrift))]
        if not treffer:
            ergebnis.fehlend.append({"angabe": angabe, "grund": "keine Ueberschrift"})
            continue
        offen = [a for a in treffer if not LUECKEN_MARKER.search(normalisiere(a.text))]
        if offen:
            ergebnis.gefunden[angabe] = f"{offen[0].datei}: {offen[0].ueberschrift}"
        else:
            ergebnis.fehlend.append({
                "angabe": angabe,
                "grund": "als Informationsluecke markiert",
                "ueberschrift": f"{treffer[0].datei}: {treffer[0].ueberschrift}",
            })
    ergebnis.bestanden = not ergebnis.fehlend
    return ergebnis


def informationsanforderung(ergebnis: GateErgebnis, zeitpunkt: str) -> dict:
    """Rueckfrage an den Einreicher (FR-08): was fehlt, bevor ein Agent startet."""
    return {
        "zeitpunkt": zeitpunkt,
        "dateien": ergebnis.dateien,
        "status": "INFORMATIONSANFORDERUNG",
        "fehlende_angaben": ergebnis.fehlend,
        "vorhandene_angaben": ergebnis.gefunden,
        "hinweis": "Die fachliche Bewertung startet erst, wenn alle Mindestangaben aus "
                   "PLAN.md Abschnitt 2 vorliegen (FR-08).",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Completeness Gate gegen PLAN.md Abschnitt 2")
    ap.add_argument("antrag", nargs="+", help="eine oder mehrere Antragsdateien")
    ap.add_argument("--json", action="store_true", help="Ergebnis als JSON")
    args = ap.parse_args(argv)
    erg = pruefe([Path(a) for a in args.antrag])
    if args.json:
        print(json.dumps(erg.als_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"Gate: {'BESTANDEN' if erg.bestanden else 'NICHT BESTANDEN'} "
              f"({len(erg.gefunden)} von {len(MINDESTANGABEN)} Angaben vorhanden)")
        for f in erg.fehlend:
            print(f"  fehlt: {f['angabe']} ({f['grund']})")
    return 0 if erg.bestanden else 3


if __name__ == "__main__":
    sys.exit(main())
