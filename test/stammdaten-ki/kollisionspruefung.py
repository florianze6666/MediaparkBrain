"""Kollisionspruefung: teilt der Antrag seltene Tokens mit einem Golden-Dokument?

Lehre aus dem Eisenach-Fall (.plans/Feature_Branch.md, Abschnitt 4): Der Antrag nannte
420 Grad C, und genau dieser Wert steht in zwei Zieldokumenten. Eine reine Wortsuche
findet das Ziel dann schon, und der Fall prueft schwaecher auf Semantik, als er soll.

Geprueft wird deshalb: Jedes Token, das im Antrag (Charter plus Business Case) UND in
einem Golden-Dokument vorkommt UND im gesamten Korpus selten ist (hoechstens
SELTEN_AB Dokumente), ist eine Kollision. Haeufige Tokens (Richtlinienkennungen, die in
Dutzenden Dokumenten stehen, Jahreszahlen, Allerweltswoerter) zaehlen nicht, weil sie
kein einzelnes Zieldokument bevorzugen.

Tokenklassen:
  - Zahlen in deutscher Schreibweise (1.540.000, 0,3, 99,5, 840.000), ohne Jahreszahlen
  - Kennungen wie INV-2024-01, POL-FIN-002, BV-2023-01, SYS-S4, IP-2026-09
  - Grossgeschriebene Woerter ab fuenf Zeichen (Eigennamen, Fachbegriffe)

Whitelist: bewusst gewollte Bezuege mit Begruendung je Eintrag. Ein Eintrag ohne
Begruendung ist ein Fehler.

Aufruf aus dem Projektwurzelverzeichnis:
    python test/stammdaten-ki/kollisionspruefung.py            # Exit 1 bei Kollision
    python test/stammdaten-ki/kollisionspruefung.py --selten 5 # strengere Schwelle
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HIER = Path(__file__).resolve().parent
ROOT = HIER.parent.parent
CORPUS = ROOT / "corpus"

ANTRAG = [
    HIER / "ki-stammdaten-standardisierung-charter.md",
    HIER / "ki-stammdaten-standardisierung-businesscase.md",
]
GOLDEN_JSON = HIER / "golden_dataset.json"

SELTEN_AB = 3  # Token gilt als selten, wenn es in hoechstens so vielen Korpusdokumenten steht

# Gewollte Bezuege. Schluessel ist das Token, Wert die Begruendung.
WHITELIST: dict[str, str] = {
    "Nachschau": "Pflichtbegriff aus POL-FIN-002 Abschnitt 9; die Vorlage folgt dem Formblatt der Richtlinie, die Regelwerk ist und keine Erinnerungsspur, und die der CFO ohnehin ueber ihre Kennung findet.",
    "Nullvariante": "Pflichtbegriff aus POL-FIN-002 Abschnitt 5 Nummer 3, gleiche Begruendung wie Nachschau.",
    "Ressourcenbedarf": "Pflichtbegriff aus POL-FIN-002 Abschnitt 5 Nummer 8, gleiche Begruendung wie Nachschau.",
    "Investitionsvolumens": "Teil der Ueberschrift aus POL-FIN-002 Abschnitt 5 Nummer 8, gleiche Begruendung wie Nachschau.",
    "Aufwandsanteil": "Pflichtbegriff aus POL-FIN-002 Abschnitt 3 und Abschnitt 5 Nummer 4 (Zahlungsreihe getrennt nach aktivierungspflichtigem Anteil und Aufwandsanteil), gleiche Begruendung wie Nachschau.",
}

RE_ZAHL = re.compile(r"(?<![\w,.])(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+,\d+|\d+)(?![\w,.])")
RE_KENNUNG = re.compile(r"\b(?:INV|IP|POL|BV|SV|AE|SYS|PRJ|GBR|AC|BEIR|LTT|HR|IT|EV|AA)-[A-Z0-9][A-Z0-9-]*\b")
RE_WORT = re.compile(r"\b[A-ZÄÖÜ][a-zäöüß]{4,}(?:-[A-ZÄÖÜa-zäöü][a-zäöüß]+)*\b")
RE_JAHR = re.compile(r"^(19|20)\d{2}$")


def lies(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def tokens(text: str) -> set[str]:
    out: set[str] = set()
    for m in RE_ZAHL.finditer(text):
        z = m.group(1)
        if RE_JAHR.match(z):
            continue
        if z.isdigit() and int(z) < 10:
            continue  # Aufzaehlungen, Nummern von Abschnitten
        out.add(z)
    out.update(RE_KENNUNG.findall(text))
    out.update(RE_WORT.findall(text))
    return out


def vorkommt(token: str, text: str) -> bool:
    """Ganzes Token, nicht Teilstring: 'Reserve' trifft nicht 'Reserven', '1,2' nicht '1,25'."""
    if token[0].isdigit():
        muster = r"(?<![\d.,])" + re.escape(token) + r"(?![\d.,])"
    else:
        muster = r"(?<![\w-])" + re.escape(token) + r"(?![\w-])"
    return re.search(muster, text) is not None


def kontext(text: str, token: str, breite: int = 70) -> str:
    i = text.find(token)
    if i < 0:
        return ""
    a, b = max(0, i - breite), min(len(text), i + len(token) + breite)
    return " ".join(text[a:b].split())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selten", type=int, default=SELTEN_AB)
    ap.add_argument("--zeige-haeufige", action="store_true",
                    help="auch geteilte, aber haeufige Tokens auflisten (nur Information)")
    args = ap.parse_args()

    for tok, grund in WHITELIST.items():
        if not grund or not grund.strip():
            sys.exit(f"FEHLER: Whitelist-Eintrag {tok!r} ohne Begruendung.")

    antrag_text = "\n".join(lies(p) for p in ANTRAG)
    antrag_tokens = tokens(antrag_text)

    golden = json.loads(lies(GOLDEN_JSON))
    rollen = golden["rollen"]
    golden_pfade: dict[str, list[str]] = defaultdict(list)  # pfad -> rollen
    for rolle, eintrag in rollen.items():
        for rel in eintrag["golden"]:
            golden_pfade[rel].append(rolle)

    # Haeufigkeit jedes Antrag-Tokens im gesamten Korpus (Dokumente, nicht Vorkommen)
    korpus_dateien = sorted(CORPUS.rglob("*.md"))
    haeufigkeit: dict[str, int] = defaultdict(int)
    korpus_text: dict[str, str] = {}
    for f in korpus_dateien:
        rel = f.relative_to(CORPUS).as_posix()
        t = lies(f)
        korpus_text[rel] = t
        for tok in antrag_tokens:
            if vorkommt(tok, t):
                haeufigkeit[tok] += 1

    fehlend = [rel for rel in golden_pfade if rel not in korpus_text]
    if fehlend:
        print("FEHLER: Golden-Pfade nicht im Korpus:")
        for rel in fehlend:
            print("  -", rel)
        return 2

    kollisionen: list[tuple[str, str, int, str, str]] = []
    haeufige: list[tuple[str, str, int]] = []
    for rel in golden_pfade:
        t = korpus_text[rel]
        for tok in sorted(antrag_tokens):
            if not vorkommt(tok, t):
                continue
            n = haeufigkeit[tok]
            if n <= args.selten:
                if tok in WHITELIST:
                    continue
                kollisionen.append((rel, tok, n, kontext(antrag_text, tok), kontext(t, tok)))
            else:
                haeufige.append((rel, tok, n))

    print(f"Antrag: {len(antrag_tokens)} Tokens; Golden-Dokumente: {len(golden_pfade)}; "
          f"Korpus: {len(korpus_dateien)} Dateien; selten = hoechstens {args.selten} Dokumente\n")

    seltene_im_korpus = sorted((tok, haeufigkeit[tok]) for tok in antrag_tokens
                               if 0 < haeufigkeit[tok] <= args.selten)
    print(f"Seltene Antrag-Tokens, die irgendwo im Korpus stehen ({len(seltene_im_korpus)}), "
          "nur zur Information:")
    for tok, n in seltene_im_korpus:
        print(f"  {tok!r:32} in {n} Dokument(en)")

    if args.zeige_haeufige:
        print("\nGeteilte, aber haeufige Tokens (kein Befund):")
        for rel, tok, n in haeufige:
            print(f"  {tok!r:32} {n:3d} Dok.  {rel}")

    print()
    if not kollisionen:
        print("KEINE KOLLISION: Antrag und Golden-Dokumente teilen kein seltenes Token.")
        if WHITELIST:
            print("Whitelist:")
            for tok, grund in WHITELIST.items():
                print(f"  {tok!r}: {grund}")
        return 0

    print(f"KOLLISION: {len(kollisionen)} seltene Token(s) geteilt.\n")
    for rel, tok, n, k_antrag, k_doc in kollisionen:
        print(f"- {tok!r} (in {n} Korpusdokumenten) mit {rel}  [Rollen: {', '.join(golden_pfade[rel])}]")
        print(f"    Antrag:  …{k_antrag}…")
        print(f"    Golden:  …{k_doc}…")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
