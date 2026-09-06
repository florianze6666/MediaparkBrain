"""Vorbereitete Bewertungslaeufe fuer die Phase-4-Tests.

Schreibt die Dateien, die der Orchestrator unter qmd/laeufe/<lauf_id>/ hinterlaesst
(Kapitel-17-Zeile je Rolle, Protokoll, bewertungen.jsonl, zusammenfassung.json,
gate.json, informationsanforderung.json), ohne Orchestrator, ohne qmd, ohne API.
Wird von den Tests direkt und vom Stub-Orchestrator als Subprozess benutzt.
"""
from __future__ import annotations

import json
from pathlib import Path

ROLLEN = ("betriebsrat", "cfo", "it", "ceo")
FELDER = ("rolle", "status", "score", "begruendung", "fehlende_informationen",
          "praezedenz", "entscheidungsrelevanter_hinweis", "quellen")
BEWERTET = "BEWERTET"
FEHLT = "INFORMATION FEHLT"
FEHLER = "FEHLER"

# Exit-Codes wie der echte Orchestrator: 0 alle gueltig, 1 eine Rolle ohne Zeile, 3 Gate.
EXIT = {"vier": 0, "fehlt": 0, "fehler": 1, "alle_ohne": 0, "gate": 3}

# Szenario -> Rolle -> (status, score, luecken)
SZENARIEN: dict[str, dict[str, tuple]] = {
    "vier": {
        "betriebsrat": (BEWERTET, 3, []),
        "cfo": (BEWERTET, 2, []),
        "it": (BEWERTET, 7, []),
        "ceo": (BEWERTET, 8, []),
    },
    "fehlt": {
        "betriebsrat": (BEWERTET, 3, []),
        "cfo": (BEWERTET, 2, []),
        "it": (FEHLT, None, ["Hosting-Modell (Cloud oder On-Premise)", "Anbindung an SYS-S4 oder proALPHA"]),
        "ceo": (BEWERTET, 8, []),
    },
    "fehler": {
        "betriebsrat": (BEWERTET, 3, []),
        "cfo": (BEWERTET, 2, []),
        "it": (BEWERTET, 7, []),
        "ceo": (FEHLER, None, []),
    },
    "alle_ohne": {
        "betriebsrat": (FEHLT, None, ["Datenkatalog"]),
        "cfo": (FEHLT, None, ["Zahlungsreihe je Jahr"]),
        "it": (FEHLT, None, ["Hosting-Modell (Cloud oder On-Premise)"]),
        "ceo": (FEHLT, None, ["zurücktretende Initiative nach POL-ORG-001"]),
    },
}

QUELLE = "corpus/projektlaufwerk/glaswerk-nord-margenverlust-durch-/2013/2013-09-25-erfahrungen-aus-der-abwicklung-festhalten.md"
ZITAT = "Kalkuliert und ausgelegt haben wir auf 420 °C am Auskoppelpunkt als Dauerwert."


def zeile(rolle: str, status: str, score, luecken: list[str]) -> dict:
    return {
        "rolle": rolle,
        "status": status,
        "score": score,
        "begruendung": f"Begründung der Rolle {rolle}: „{ZITAT}“ – Regelbezug POL-FIN-002 v1.1.",
        "fehlende_informationen": list(luecken),
        "praezedenz": "Glaswerk Nord 2013 (KP-2013-042)" if status == BEWERTET else None,
        "entscheidungsrelevanter_hinweis": (
            f"Hinweis {rolle}: vor Freigabe Messprotokoll vorlegen." if status == BEWERTET and score <= 3 else None
        ),
        "quellen": [QUELLE] if status == BEWERTET else [],
    }


def protokoll(lauf_id: str, rolle: str, fehler: dict | None = None) -> dict:
    return {
        "rolle": rolle,
        "lauf_id": lauf_id,
        "modell": "stub-modell",
        "zeitpunkt": "2026-09-06T06:00:00+00:00",
        "prompt_version": "deadbeef1234",
        "rag_abfragen": [
            {"runde": 1, "frage": f"Was geschah bei Glaswerk Nord 2013 ({rolle})?",
             "treffer": [{"datei": QUELLE.removeprefix("corpus/"), "score": 0.71}]},
            {"runde": 2, "frage": "Welche Regel gilt für Investitionsvorlagen?", "treffer": []},
        ],
        "dokumente_im_kontext": [{"datei": QUELLE.removeprefix("corpus/"), "score": 0.71, "namensbezug": True}],
        "zitate": [] if fehler else [{"datei": QUELLE.removeprefix("corpus/"), "cited_text": ZITAT}],
        "essay": None if fehler else f"Essay der Rolle {rolle}.\n\nScore: X/10 steht hier nicht, das Feld gilt.",
        "zeiten_s": {"gesamt": 12.3},
        "technischer_fehler": fehler,
    }


def schreibe(d: Path, szenario: str, lauf_id: str | None = None) -> int:
    """Schreibt einen fertigen Lauf nach d. Liefert den Exit-Code des Orchestrators."""
    d.mkdir(parents=True, exist_ok=True)
    lauf_id = lauf_id or d.name
    if szenario == "gate":
        fehlend = [
            {"angabe": "Business Case", "grund": "keine Ueberschrift"},
            {"angabe": "Risikoanalyse", "grund": "keine Ueberschrift"},
            {"angabe": "Bekannte technische Abhaengigkeiten", "grund": "als Informationsluecke markiert",
             "ueberschrift": "antrag.md: Technische Abhängigkeiten"},
        ]
        gefunden = {"Projektname": "antrag.md: Projektname", "Beschreibung des Vorhabens": "antrag.md: Beschreibung"}
        (d / "gate.json").write_text(json.dumps({"bestanden": False, "dateien": [], "gefunden": gefunden,
                                                 "fehlend": fehlend}, ensure_ascii=False, indent=2), encoding="utf-8")
        (d / "informationsanforderung.json").write_text(json.dumps({
            "zeitpunkt": "2026-09-06T06:00:00+00:00", "dateien": [], "status": "INFORMATIONSANFORDERUNG",
            "fehlende_angaben": fehlend, "vorhandene_angaben": gefunden,
            "hinweis": "Die fachliche Bewertung startet erst, wenn alle Mindestangaben aus PLAN.md Abschnitt 2 vorliegen (FR-08).",
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        return EXIT["gate"]

    rollen = SZENARIEN[szenario]
    (d / "gate.json").write_text(json.dumps({"bestanden": True, "dateien": [], "gefunden": {}, "fehlend": []}),
                                 encoding="utf-8")
    gueltig: list[dict] = []
    technische_fehler: list[dict] = []
    for rolle in ROLLEN:
        status, score, luecken = rollen[rolle]
        if status == FEHLER:
            tf = {"art": "max_tokens", "details": "Zug A zweimal an der Token-Grenze abgeschnitten (Z4)"}
            (d / f"{rolle}.protokoll.json").write_text(json.dumps(protokoll(lauf_id, rolle, tf), ensure_ascii=False, indent=2),
                                                        encoding="utf-8")
            technische_fehler.append({"rolle": rolle, "fehler": f"{tf['art']}: {tf['details']}",
                                      "protokoll": str(d / f"{rolle}.protokoll.json")})
            continue
        z = zeile(rolle, status, score, luecken)
        (d / f"{rolle}.jsonl").write_text(json.dumps(z, ensure_ascii=False) + "\n", encoding="utf-8")
        (d / f"{rolle}.protokoll.json").write_text(json.dumps(protokoll(lauf_id, rolle), ensure_ascii=False, indent=2),
                                                    encoding="utf-8")
        gueltig.append(z)

    with (d / "bewertungen.jsonl").open("w", encoding="utf-8") as fh:
        for z in gueltig:
            fh.write(json.dumps(z, ensure_ascii=False) + "\n")

    scores = [z["score"] for z in gueltig if z["status"] == BEWERTET]
    bewertet = [z for z in gueltig if z["status"] == BEWERTET]
    konflikte = []
    for i, a in enumerate(bewertet):
        for b in bewertet[i + 1:]:
            abstand = abs(a["score"] - b["score"])
            if abstand >= 4:
                konflikte.append({"rolle_a": a["rolle"], "rolle_b": b["rolle"],
                                  "score_a": a["score"], "score_b": b["score"], "abstand": abstand})
    luecken = [f"{z['rolle']}: {l}" for z in gueltig if z["status"] == FEHLT for l in z["fehlende_informationen"]]
    zusammenfassung = {
        "lauf_id": lauf_id,
        "zeitpunkt": "2026-09-06T06:00:00+00:00",
        "gesamtstatus": BEWERTET if scores else FEHLT,
        "gesamtscore": round(sum(scores) / len(scores), 1) if scores else None,
        "anzahl_bewertet": len(scores),
        "anzahl_gueltige_zeilen": len(gueltig),
        "rollen": gueltig,
        "fehlende_informationen": luecken,
        "spanne": (max(scores) - min(scores)) if scores else None,
        "konflikte": konflikte,
        "technische_fehler": technische_fehler,
        "zeilenfehler": [],
    }
    (d / "zusammenfassung.json").write_text(json.dumps(zusammenfassung, ensure_ascii=False, indent=2), encoding="utf-8")
    return EXIT[szenario]
