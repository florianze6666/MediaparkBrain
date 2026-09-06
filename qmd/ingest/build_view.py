"""Baut aus corpus/ eine nach Domaenen getrennte Sicht unter qmd/view/.

Warum ueberhaupt eine Sicht?
    corpus/ ist nach Ablageorten organisiert (br_ablage, sharepoint_gf, ...),
    das Rechtemodell des Wikis kennt aber Domaenen (br, gf, ...). QMD wiederum
    filtert ausschliesslich ueber Collections und liest kein Frontmatter. Erst
    eine Ordnerstruktur, die den Domaenen entspricht, laesst sich auf
    Collections abbilden und damit auf access.readable_domains(user).

Was hier NICHT passiert:
    corpus/ wird ausschliesslich gelesen. Die Sicht besteht aus Hardlinks, es
    wird nichts kopiert, verschoben oder veraendert. Faellt Hardlinking aus,
    wird kopiert (1,8 MB) und das gemeldet.

Vertraulichkeit:
    Die Uebersetzung der Korpus-Stufen (C-Level, Betriebsrat-intern, ...) auf
    das Rechtemodell spiegelt access.normalize_confidentiality
    (llm-wiki/app/access.py:161). Sie ist hier nachgebaut statt importiert,
    damit dieses Teilprojekt eigenstaendig bleibt und llm-wiki nicht braucht.
    Gelesen wird dieselbe permissions.yaml, es gibt also nur eine Wahrheit.

Aufruf:
    python ingest/build_view.py --dry-run    nur berichten, nichts anlegen
    python ingest/build_view.py              Sicht neu aufbauen
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

QMD_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = QMD_DIR.parent
# Pfade sind per Umgebung ueberschreibbar, damit Tests und Wiki-Jobs gegen ein
# Temp-Verzeichnis laufen koennen (Phase 5). Vorgabe bleibt das Projekt.
CORPUS_DIR = Path(os.environ.get("MPB_CORPUS_DIR") or PROJECT_DIR / "corpus")
PERMISSIONS_FILE = Path(os.environ.get("MPB_PERMISSIONS_FILE")
                        or PROJECT_DIR / "llm-wiki" / "permissions.yaml")
MAPPING_FILE = QMD_DIR / "ingest" / "mapping.yaml"
VIEW_DIR = Path(os.environ.get("MPB_VIEW_DIR") or QMD_DIR / "view")

# access.py:38 - die drei Werte, die das Rechtemodell intern kennt
VERTRAULICHKEITEN = ("oeffentlich", "intern", "vertraulich")
VERTRAULICH_DIR = "vertraulich"

# Klassenmodus (AE: drei Collections). Die Klasse ergibt sich aus der ROHEN
# Stufe im Frontmatter. Wichtig: nicht aus der normalisierten Stufe, denn
# normalize_confidentiality macht aus "C-Level" UND "Betriebsrat-intern"
# gleichermassen "vertraulich" - danach waeren die beiden Klassen nicht mehr
# unterscheidbar, und genau ihre Trennung ist der Zweck.
KLASSE_AUS_ROHSTUFE = {
    "Betriebsrat-intern": "br",
    "C-Level": "clevel",
    "intern": "intern",
    "oeffentlich": "intern",
    "": "intern",
}
KLASSEN = ("intern", "br", "clevel")
# Vierte Collection (Phase 5, Fit-Gap I-3): Projektantraege, getrennt ruecksetzbar,
# nie Teil einer Agentenabfrage (rollen.py kennt nur KLASSEN).
ANTRAEGE = "antraege"
MANIFEST = VIEW_DIR / "_manifest.json"
MANIFEST_ANTRAEGE = VIEW_DIR / "_manifest_antraege.json"
UNKNOWN = "unbekannt"


# ---------------------------------------------------------------------------
# Laden
# ---------------------------------------------------------------------------


def load_yaml(path: Path) -> dict:
    if not path.exists():
        sys.exit(f"FEHLER: {path} fehlt.")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def split_frontmatter(raw: str) -> tuple[dict, bool]:
    """YAML-Kopf einer Korpusdatei. Zweiter Wert sagt, ob ueberhaupt einer da war.

    Spiegelt wiki.split_frontmatter_raw (llm-wiki/app/wiki.py:119): fehlt das
    schliessende ---, gilt die Datei als kopflos statt als Fehler.
    """
    lines = raw.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, False
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            try:
                data = yaml.safe_load("\n".join(lines[1:i])) or {}
            except yaml.YAMLError:
                return {}, False
            return (data, True) if isinstance(data, dict) else ({}, False)
    return {}, False


def as_list(value) -> list[str]:
    """Empfaenger robust zu einer Liste. Spiegelt PageMeta.from_dict (access.py:80).
    Der Korpus benutzt "-" als Platzhalter fuer "keine", das faellt hier weg.
    """
    if value is None:
        return []
    if isinstance(value, str):
        items = [v.strip() for v in value.split(",")]
    else:
        items = [str(v).strip() for v in value]
    return [i for i in items if i and i != "-"]


def normalize_confidentiality(vertraulichkeit: str, empfaenger: list[str],
                              stufen: dict) -> tuple[str, list[str]]:
    """Nachbau von access.normalize_confidentiality (access.py:161)."""
    empf = list(empfaenger)
    if vertraulichkeit in stufen:
        cfg = stufen[vertraulichkeit] or {}
        target = cfg.get("vertraulichkeit", vertraulichkeit)
        for e in cfg.get("empfaenger") or []:
            if e not in empf:
                empf.append(e)
        return target, empf
    if vertraulichkeit not in VERTRAULICHKEITEN:
        return "intern", empf
    return vertraulichkeit, empf


# ---------------------------------------------------------------------------
# Analyse
# ---------------------------------------------------------------------------


def plan_entries(mapping: dict, stufen: dict, endungen: set[str],
                 klassen_modus: bool = False) -> tuple[list[dict], list[str], list[str]]:
    """Ermittelt fuer jede Korpusdatei ihr Ziel. Aendert nichts.

    Rueckgabe: (eintraege, warnungen, fehler). Im Klassenmodus fuehrt eine
    unbekannte Vertraulichkeitsstufe zu einem FEHLER statt zu einer Warnung:
    sie stillschweigend nach `intern` zu schieben waere genau der Leak-Vektor,
    den die drei Klassen verhindern sollen.
    """
    fehler: list[str] = []
    ablageorte = mapping["ablageorte"]
    fallback = mapping.get("fallback_domaene", "allgemein")
    entries: list[dict] = []
    warnungen: list[str] = []

    for src in sorted(CORPUS_DIR.rglob("*")):
        if not src.is_file() or src.suffix.lower() not in endungen:
            continue
        rel = src.relative_to(CORPUS_DIR)
        parts = rel.parts

        # Der ORDNER ist die Wahrheit, nicht der Dateikopf. Dieselbe Regel wie
        # in wiki._load (llm-wiki/app/wiki.py:205).
        if len(parts) > 1 and parts[0] in ablageorte:
            ablageort = parts[0]
            domaene = ablageorte[ablageort]
            unterpfad = Path(*parts[1:])
        else:
            ablageort = ""
            domaene = fallback
            unterpfad = Path(parts[-1])

        head, hatte_kopf = split_frontmatter(src.read_text(encoding="utf-8", errors="replace"))

        kopf_ablageort = str(head.get("ablageort") or "").strip()
        if ablageort and kopf_ablageort and kopf_ablageort != ablageort:
            warnungen.append(
                f"{rel}: Kopf sagt ablageort={kopf_ablageort!r}, Ordner sagt "
                f"{ablageort!r}. Der Ordner gewinnt."
            )

        roh_stufe = str(head.get("vertraulichkeit") or "intern").strip() or "intern"
        vertraulichkeit, empfaenger = normalize_confidentiality(
            roh_stufe, as_list(head.get("empfaenger")), stufen
        )
        unbekannt = roh_stufe not in stufen and roh_stufe not in VERTRAULICHKEITEN
        if unbekannt and klassen_modus:
            fehler.append(f"{rel}: unbekannte Vertraulichkeit {roh_stufe!r}.")
        elif unbekannt:
            warnungen.append(
                f"{rel}: unbekannte Vertraulichkeit {roh_stufe!r}, wird zu 'intern'."
            )
        klasse = KLASSE_AUS_ROHSTUFE.get(roh_stufe, "intern")
        if not hatte_kopf:
            warnungen.append(f"{rel}: kein Frontmatter, Standardwerte greifen (intern).")

        if klassen_modus:
            # Klasse ganz oben, darunter die Herkunft wie in corpus/, damit der
            # Pfad die Provenienz weiter traegt und Namen nicht kollidieren.
            ziel = VIEW_DIR / klasse / (ablageort or "_wurzel") / unterpfad
        else:
            ziel = VIEW_DIR / domaene
            if vertraulichkeit == "vertraulich":
                ziel = ziel / VERTRAULICH_DIR
            ziel = ziel / unterpfad

        ziel_str = (str(ziel.relative_to(QMD_DIR)) if ziel.is_relative_to(QMD_DIR)
                    else str(ziel)).replace("\\", "/")
        entries.append({
            "quelle": str(rel).replace("\\", "/"),
            "ziel": ziel_str,
            "ablageort": ablageort,
            "domaene": domaene,
            "klasse": klasse,
            "vertraulichkeit_roh": roh_stufe,
            "vertraulichkeit": vertraulichkeit,
            "empfaenger": empfaenger,
            "erstellt_von": str(head.get("verfasser") or UNKNOWN).strip() or UNKNOWN,
            "titel": str(head.get("titel") or src.stem).strip(),
            "hatte_frontmatter": hatte_kopf,
        })
    return entries, warnungen, fehler


def check_domains(mapping: dict, permissions: dict) -> list[str]:
    """Jede Zieldomaene muss in permissions.yaml existieren, sonst waere die
    Sicht nicht auf Collections und damit nicht auf Rechte abbildbar."""
    bekannt = set((permissions.get("domaenen") or {}).keys())
    ziele = set(mapping["ablageorte"].values()) | {mapping.get("fallback_domaene", "allgemein")}
    return [f"Domaene {d!r} steht nicht in permissions.yaml" for d in sorted(ziele - bekannt)]


# ---------------------------------------------------------------------------
# Schreiben
# ---------------------------------------------------------------------------


def ziel_abs(e: dict) -> Path:
    z = Path(e["ziel"])
    return z if z.is_absolute() else QMD_DIR / z


def zielordner(entries: list[dict]) -> list[Path]:
    """Die obersten Ordner unter VIEW_DIR, die diese Eintraege belegen (Klassen
    oder Domaenen). Nur sie werden beim Bau ersetzt; andere Sichten wie
    view/antraege (Phase 5) bleiben unberuehrt."""
    namen = sorted({ziel_abs(e).relative_to(VIEW_DIR).parts[0] for e in entries})
    return [VIEW_DIR / n for n in namen]


def build(entries: list[dict], fortschritt=None) -> tuple[int, int]:
    """Legt die Sicht neu an. Rueckgabe: (Hardlinks, Kopien).

    Ersetzt nur die Zielordner der uebergebenen Eintraege (zielordner), nicht das
    ganze VIEW_DIR. `fortschritt(n, gesamt, quelle)` wird je Datei gerufen, damit
    ein Aufrufer "n von N" anzeigen kann (NFR-11).
    """
    for d in zielordner(entries):
        if d.exists():
            shutil.rmtree(d)
    verlinkt = kopiert = 0
    gesamt = len(entries)
    for i, e in enumerate(entries, 1):
        src = CORPUS_DIR / e["quelle"]
        dst = ziel_abs(e)
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(src, dst)
            verlinkt += 1
        except OSError:
            shutil.copy2(src, dst)
            kopiert += 1
        if fortschritt is not None:
            fortschritt(i, gesamt, e["quelle"])
    return verlinkt, kopiert


def schreibe_manifest(entries: list[dict], warnungen: list[str],
                      verlinkt: int, kopiert: int, pfad: Path = None) -> Path:
    """Manifest mit Rechteinformation je Datei; zweite Schranke hinter der
    Collection (qmd-Plan, Abschnitt 5)."""
    pfad = pfad or MANIFEST
    pfad.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "quelle": str(CORPUS_DIR),
        "dateien": len(entries),
        "hardlinks": verlinkt,
        "kopien": kopiert,
        "warnungen": warnungen,
        "eintraege": entries,
    }
    pfad.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return pfad


# ---------------------------------------------------------------------------
# Bericht
# ---------------------------------------------------------------------------


def report_klassen(entries: list[dict]) -> None:
    """Kreuztabelle Klasse mal Rohstufe. Eine Fehlzuordnung faellt hier sofort auf."""
    kreuz: dict[str, Counter] = defaultdict(Counter)
    for e in entries:
        kreuz[e["klasse"]][e["vertraulichkeit_roh"]] += 1
    stufen = sorted({e["vertraulichkeit_roh"] for e in entries})
    print()
    print(f"{len(entries)} Dateien auf drei Klassen verteilt")
    print()
    kopf = f"{'Klasse':<10}{'gesamt':>8}" + "".join(f"{s[:18]:>20}" for s in stufen)
    print(kopf); print("-" * len(kopf))
    for k in KLASSEN:
        c = kreuz.get(k)
        if not c:
            print(f"{k:<10}{0:>8}"); continue
        print(f"{k:<10}{sum(c.values()):>8}" + "".join(f"{c[s]:>20}" for s in stufen))
    print("-" * len(kopf))
    ges = Counter()
    for c in kreuz.values():
        ges.update(c)
    print(f"{'Summe':<10}{sum(ges.values()):>8}" + "".join(f"{ges[s]:>20}" for s in stufen))


def report(entries: list[dict], warnungen: list[str]) -> None:
    je_domaene: dict[str, Counter] = defaultdict(Counter)
    for e in entries:
        je_domaene[e["domaene"]][e["vertraulichkeit"]] += 1

    print(f"\n{len(entries)} Dateien aus corpus/ zugeordnet\n")
    print(f"{'Domaene':<12}{'gesamt':>8}{'oeffentl.':>11}{'intern':>9}{'vertraul.':>11}")
    print("-" * 51)
    for dom in sorted(je_domaene):
        c = je_domaene[dom]
        print(f"{dom:<12}{sum(c.values()):>8}{c['oeffentlich']:>11}"
              f"{c['intern']:>9}{c['vertraulich']:>11}")
    gesamt = Counter()
    for c in je_domaene.values():
        gesamt.update(c)
    print("-" * 51)
    print(f"{'Summe':<12}{sum(gesamt.values()):>8}{gesamt['oeffentlich']:>11}"
          f"{gesamt['intern']:>9}{gesamt['vertraulich']:>11}")

    stufen_roh = Counter(e["vertraulichkeit_roh"] for e in entries)
    print("\nKorpus-Stufen wie im Frontmatter vorgefunden:")
    for k, n in stufen_roh.most_common():
        print(f"  {k:<22}{n:>4}")

    if warnungen:
        print(f"\n{len(warnungen)} Hinweise:")
        for w in warnungen[:15]:
            print(f"  - {w}")
        if len(warnungen) > 15:
            print(f"  ... und {len(warnungen) - 15} weitere (siehe Manifest)")


def main() -> int:
    ap = argparse.ArgumentParser(description="Baut qmd/view/ aus corpus/.")
    ap.add_argument("--dry-run", action="store_true",
                    help="nur berichten, nichts anlegen oder loeschen")
    ap.add_argument("--klassen", action="store_true",
                    help="drei Klassen (intern/br/clevel) statt neun Domaenenordner")
    args = ap.parse_args()

    permissions = load_yaml(PERMISSIONS_FILE)
    mapping = load_yaml(MAPPING_FILE)
    stufen = permissions.get("vertraulichkeitsstufen") or {}
    endungen = {e.lower() for e in mapping.get("endungen", [".md"])}

    fehler = check_domains(mapping, permissions)
    if fehler:
        for f in fehler:
            print(f"FEHLER: {f}", file=sys.stderr)
        return 2

    if not CORPUS_DIR.is_dir():
        print(f"FEHLER: {CORPUS_DIR} fehlt.", file=sys.stderr)
        return 2

    entries, warnungen, fehler = plan_entries(mapping, stufen, endungen, args.klassen)
    if not entries:
        print("FEHLER: keine Markdown-Dateien in corpus/ gefunden.", file=sys.stderr)
        return 2
    if fehler:
        print(f"ABBRUCH: {len(fehler)} Datei(en) mit unbekannter Vertraulichkeitsstufe.",
              file=sys.stderr)
        for f in fehler[:10]:
            print(f"  - {f}", file=sys.stderr)
        print("Neue Stufen gehoeren zuerst in permissions.yaml und in "
              "KLASSE_AUS_ROHSTUFE.", file=sys.stderr)
        return 3

    if args.klassen:
        report_klassen(entries)
    report(entries, warnungen)

    if args.dry_run:
        print("\n--dry-run: nichts angelegt, nichts geloescht.")
        return 0

    verlinkt, kopiert = build(entries)
    manifest = schreibe_manifest(entries, warnungen, verlinkt, kopiert)
    print(f"\nSicht gebaut: {verlinkt} Hardlinks, {kopiert} Kopien")
    print(f"Manifest: {manifest}")
    if kopiert:
        print("Hinweis: Hardlinking war nicht ueberall moeglich, es wurde kopiert.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
