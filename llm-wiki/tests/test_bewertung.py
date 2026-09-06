"""Phase 4: Bewertungslaeufe ueber den Orchestrator (UC-04, UC-05, AE-04).

Der Orchestrator wird durch einen Stub ersetzt (MPB_ORCHESTRATOR_CMD), der als
Subprozess die Dateien eines fertigen Laufs schreibt (tests/laufdaten.py). Kein Test
ruft die API oder qmd.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pytest

from tests import laufdaten
from tests.conftest import as_user
from tests.test_proposals import _submit

TESTS_DIR = Path(__file__).resolve().parent

STUB = '''
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, os.environ["MPB_STUB_HELPER_DIR"])
import laufdaten
args = sys.argv[1:]
lauf = args[args.index("--lauf") + 1]
antraege = [args[i + 1] for i, a in enumerate(args) if a == "--antrag"]
d = Path(os.environ["MPB_LAEUFE_DIR"]) / lauf
d.mkdir(parents=True, exist_ok=True)
(d / "stub_args.json").write_text(json.dumps({"antraege": antraege, "cwd": os.getcwd()}), encoding="utf-8")
szenario = os.environ.get("MPB_STUB_SZENARIO", "vier")
if szenario == "langsam":
    (d / "gate.json").write_text('{"bestanden": true, "dateien": [], "gefunden": {}, "fehlend": []}', encoding="utf-8")
    time.sleep(2.5)
    szenario = "vier"
print("Stub-Orchestrator:", szenario, lauf)
sys.exit(laufdaten.schreibe(d, szenario, lauf))
'''


@pytest.fixture
def lauf_env(client, tmp_path, monkeypatch):
    """Stub-Orchestrator und Laeufe-Verzeichnis unter tmp; Prozessregister leer."""
    import app.bewertung as bewertung

    stub = tmp_path / "stub_orchestrator.py"
    stub.write_text(STUB, encoding="utf-8")
    laeufe = tmp_path / "laeufe"
    qmd = tmp_path / "qmd"
    qmd.mkdir()
    monkeypatch.setenv("MPB_LAEUFE_DIR", str(laeufe))
    monkeypatch.setenv("MPB_QMD_DIR", str(qmd))
    monkeypatch.setenv("MPB_ORCHESTRATOR_CMD", f'"{sys.executable}" "{stub}"')
    monkeypatch.setenv("MPB_STUB_HELPER_DIR", str(TESTS_DIR))
    monkeypatch.delenv("MPB_STUB_SZENARIO", raising=False)
    bewertung._PROZESSE.clear()
    return {"laeufe": laeufe, "qmd": qmd, "client": client}


def _warte_bis_fertig(slug: str, lauf_id: str, timeout: float = 20.0):
    import app.bewertung as bewertung

    ende = time.time() + timeout
    while time.time() < ende:
        l = bewertung.lauf_fuer(slug, lauf_id)
        if l is not None and not l.laeuft and l.beendet_am:
            return l
        time.sleep(0.1)
    raise AssertionError(f"Lauf {lauf_id} nicht fertig geworden")


def _lauf_id_aus(location: str) -> str:
    assert "?lauf=" in location, location
    return location.split("?lauf=", 1)[1]


def _startzeit(lauf_id: str) -> str:
    """ISO-Zeit aus dem Zeitstempel in der Lauf-ID (…-JJJJMMTT-HHMMSS…)."""
    import re
    m = re.search(r"(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2})", lauf_id)
    j, mo, tg, h, mi, se = m.groups()
    return f"{j}-{mo}-{tg}T{h}:{mi}:{se}"


def _vorbereiteter_lauf(laeufe: Path, slug: str, szenario: str, lauf_id: str | None = None,
                        antraege: list[str] | None = None) -> str:
    """Schreibt einen fertigen Lauf samt wiki.json direkt, ohne Subprozess."""
    lauf_id = lauf_id or f"{slug}-20260906-060000-{szenario}"
    d = laeufe / lauf_id
    code = laufdaten.schreibe(d, szenario, lauf_id)
    (d / "wiki.json").write_text(json.dumps({
        "lauf_id": lauf_id, "slug": slug, "antraege": antraege or [slug], "dateien": [],
        "gestartet_von": "projektmanager", "gestartet_am": _startzeit(lauf_id),
        "beendet_am": _startzeit(lauf_id).replace("T06", "T07"), "exit_code": code, "cmd": ["stub"],
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return lauf_id


# ---------------------------------------------------------------------------
# Start ueber die Route, Stub als Subprozess
# ---------------------------------------------------------------------------


def test_start_lauf_vier_rollen_und_ergebnis(lauf_env):
    client, laeufe = lauf_env["client"], lauf_env["laeufe"]
    assert _submit(client, "projektmanager", "Abwaerme Test").status_code == 303
    r = client.post("/proposals/abwaerme-test/evaluate", cookies=as_user("projektmanager"))
    assert r.status_code == 303
    lauf_id = _lauf_id_aus(r.headers["location"])
    assert lauf_id.startswith("abwaerme-test-")

    # Waehrend des Laufs: Seite zeigt den Stand (der Stub ist schnell, deshalb nur der Zustand danach)
    l = _warte_bis_fertig("abwaerme-test", lauf_id)
    assert l.fertig and l.exit_code == 0
    d = laeufe / lauf_id
    assert (d / "wiki.json").exists() and (d / "orchestrator.log").exists()
    stub_args = json.loads((d / "stub_args.json").read_text(encoding="utf-8"))
    assert stub_args["antraege"] == [str(laeufe.parent / "project_proposals" / "abwaerme-test.md")]
    assert Path(stub_args["cwd"]).resolve() == lauf_env["qmd"].resolve()
    assert "Stub-Orchestrator: vier" in (d / "orchestrator.log").read_text(encoding="utf-8")

    r = client.get(f"/proposals/abwaerme-test/evaluation?lauf={lauf_id}", cookies=as_user("projektmanager"))
    assert r.status_code == 200
    html = r.text
    # Kapitel 16 darueber
    assert "Gesamtscore: 5,0/10" in html
    assert "Gesamtstatus <strong>BEWERTET</strong>" in html
    assert "4 von 4 Rollen mit Score" in html
    assert "Spanne der Scores:</strong> 6" in html
    assert "cfo 2 gegen ceo 8" in html
    # Kapitel 17 je Rolle, alle acht Felder sichtbar
    for name in ("Betriebsrat / Employee Interests", "CFO / Controlling",
                 "IT / Architektur / Cybersecurity", "CEO / Strategie"):
        assert name in html
    assert "3/10" in html and "2/10" in html and "7/10" in html and "8/10" in html
    assert "Präzedenz:</strong> Glaswerk Nord 2013" in html
    assert "Entscheidungsrelevanter Hinweis:</strong> Hinweis cfo" in html
    assert laufdaten.QUELLE in html
    # Beleg aus dem Protokoll, nicht als Feld
    assert "Beleg: Essay, Zitate, Abfragen" in html
    assert laufdaten.ZITAT in html
    assert "Essay der Rolle cfo." in html
    assert "2 Abfragen an die Wissensbasis" in html
    assert 'risk-neutral">KEIN SCORE' not in html and "Technische Fehler" not in html


def test_lauf_seite_zeigt_fortschritt_waehrend_des_laufs(lauf_env, monkeypatch):
    client = lauf_env["client"]
    monkeypatch.setenv("MPB_STUB_SZENARIO", "langsam")
    assert _submit(client, "projektmanager", "Langsam").status_code == 303
    r = client.post("/proposals/langsam/evaluate", cookies=as_user("projektmanager"))
    lauf_id = _lauf_id_aus(r.headers["location"])
    # Der Stub schreibt gate.json und schlaeft dann; bis dahin zeigt die Seite die Gate-Phase.
    gate = lauf_env["laeufe"] / lauf_id / "gate.json"
    ende = time.time() + 5
    while not gate.exists() and time.time() < ende:
        time.sleep(0.05)
    assert gate.exists(), "Stub hat gate.json nicht geschrieben"
    r = client.get(f"/proposals/langsam/evaluation?lauf={lauf_id}", cookies=as_user("projektmanager"))
    assert r.status_code == 200
    assert "Lauf läuft" in r.text and 'http-equiv="refresh"' in r.text
    assert "läuft gerade" in r.text and "wartet" in r.text
    assert "Gesamtscore" not in r.text
    # Zweiter Start waehrend des Laufs: abgewiesen, kein zweites Verzeichnis (A-5, Z1)
    r2 = client.post("/proposals/langsam/evaluate", cookies=as_user("projektmanager"))
    assert r2.status_code == 303 and "fehler=laeuft" in r2.headers["location"]
    assert len([d for d in lauf_env["laeufe"].iterdir() if d.is_dir()]) == 1
    r3 = client.get(r2.headers["location"], cookies=as_user("projektmanager"))
    assert "Es läuft bereits ein Bewertungslauf" in r3.text
    l = _warte_bis_fertig("langsam", lauf_id)
    assert l.fertig
    r = client.get(f"/proposals/langsam/evaluation", cookies=as_user("projektmanager"))
    assert "Gesamtscore: 5,0/10" in r.text and 'http-equiv="refresh"' not in r.text


def test_gate_durchfall_zeigt_informationsanforderung(lauf_env, monkeypatch):
    client, laeufe = lauf_env["client"], lauf_env["laeufe"]
    monkeypatch.setenv("MPB_STUB_SZENARIO", "gate")
    assert _submit(client, "projektmanager", "Unvollstaendig").status_code == 303
    r = client.post("/proposals/unvollstaendig/evaluate", cookies=as_user("projektmanager"))
    lauf_id = _lauf_id_aus(r.headers["location"])
    l = _warte_bis_fertig("unvollstaendig", lauf_id)
    assert l.status == "gate" and l.exit_code == 3
    r = client.get(f"/proposals/unvollstaendig/evaluation", cookies=as_user("projektmanager"))
    html = r.text
    assert "Informationsanforderung: der Antrag ist unvollständig" in html
    assert "Kein Agent wurde gestartet" in html
    assert "Business Case" in html and "Risikoanalyse" in html
    assert "als Informationsluecke markiert" in html
    assert "Vorhanden: 2 von 5 Mindestangaben" in html
    assert "Gesamtscore" not in html and "eval-role" not in html
    assert not (laeufe / lauf_id / "zusammenfassung.json").exists()


# ---------------------------------------------------------------------------
# Vorbereitete Laeufe: die Darstellung nach AE-04
# ---------------------------------------------------------------------------


def test_information_fehlt_kein_score_ist_nicht_null(lauf_env):
    client, laeufe = lauf_env["client"], lauf_env["laeufe"]
    assert _submit(client, "projektmanager", "Fehlt").status_code == 303
    _vorbereiteter_lauf(laeufe, "fehlt", "fehlt")
    r = client.get("/proposals/fehlt/evaluation", cookies=as_user("projektmanager"))
    html = r.text
    assert "Gesamtscore: 4,3/10" in html          # (3 + 2 + 8) / 3, IT zaehlt nicht
    assert "3 von 4 Rollen mit Score" in html
    assert "KEIN SCORE" in html
    assert "Status: <strong>INFORMATION FEHLT</strong>" in html
    assert "Fehlende Informationen (16.5)" in html
    assert "it: Hosting-Modell (Cloud oder On-Premise)" in html
    assert "it: Anbindung an SYS-S4 oder proALPHA" in html
    assert "Technische Fehler" not in html


def test_technischer_fehler_bleibt_sichtbar(lauf_env):
    client, laeufe = lauf_env["client"], lauf_env["laeufe"]
    assert _submit(client, "projektmanager", "Fehler").status_code == 303
    _vorbereiteter_lauf(laeufe, "fehler", "fehler")
    r = client.get("/proposals/fehler/evaluation", cookies=as_user("projektmanager"))
    html = r.text
    assert "Gesamtscore: 4,0/10" in html          # (3 + 2 + 7) / 3
    assert "3 von 4 Rollen mit Score" in html
    assert "Technische Fehler" in html
    assert "<strong>ceo</strong>: max_tokens: Zug A zweimal an der Token-Grenze abgeschnitten (Z4)" in html
    assert html.count("technischer Fehler") >= 1
    assert "Keine gültige Bewertung dieser Rolle." in html


def test_alle_vier_ohne_score(lauf_env):
    client, laeufe = lauf_env["client"], lauf_env["laeufe"]
    assert _submit(client, "projektmanager", "Leer").status_code == 303
    _vorbereiteter_lauf(laeufe, "leer", "alle_ohne")
    r = client.get("/proposals/leer/evaluation", cookies=as_user("projektmanager"))
    html = r.text
    assert "Gesamtscore: KEIN SCORE" in html and "KEIN SCORE/10" not in html
    assert "Gesamtstatus <strong>INFORMATION FEHLT</strong>" in html
    assert "0 von 4 Rollen mit Score" in html
    assert html.count('risk-badge risk-neutral">KEIN SCORE') == 4
    assert "Spanne der Scores" not in html
    assert "ceo: zurücktretende Initiative nach POL-ORG-001" in html


def test_uebersicht_zeigt_letzten_lauf_und_startknopf(lauf_env):
    client, laeufe = lauf_env["client"], lauf_env["laeufe"]
    assert _submit(client, "projektmanager", "Erster").status_code == 303
    assert _submit(client, "projektmanager", "Zweiter").status_code == 303
    _vorbereiteter_lauf(laeufe, "erster", "vier")
    r = client.get("/proposals/evaluate", cookies=as_user("projektmanager"))
    assert r.status_code == 200
    html = r.text
    assert "Erster" in html and "Zweiter" in html
    assert "noch nicht bewertet" in html
    assert "5,0/10" in html
    assert 'action="/proposals/zweiter/evaluate"' in html
    assert "Bewerten" in html


def test_fruehere_laeufe_und_lauf_parameter(lauf_env):
    client, laeufe = lauf_env["client"], lauf_env["laeufe"]
    assert _submit(client, "projektmanager", "Mehrfach").status_code == 303
    alt = _vorbereiteter_lauf(laeufe, "mehrfach", "alle_ohne", lauf_id="mehrfach-20260905-100000")
    neu = _vorbereiteter_lauf(laeufe, "mehrfach", "vier", lauf_id="mehrfach-20260906-100000")
    # ohne Parameter: der neueste
    r = client.get("/proposals/mehrfach/evaluation", cookies=as_user("projektmanager"))
    assert "Gesamtscore: 5,0/10" in r.text and "Frühere Läufe" in r.text and alt in r.text
    # mit Parameter: der alte
    r = client.get(f"/proposals/mehrfach/evaluation?lauf={alt}", cookies=as_user("projektmanager"))
    assert "Gesamtscore: KEIN SCORE" in r.text
    # fremder oder fehlender Lauf: 404
    assert client.get("/proposals/mehrfach/evaluation?lauf=gibt-es-nicht",
                      cookies=as_user("projektmanager")).status_code == 404
    assert client.get("/proposals/mehrfach/evaluation?lauf=..%2F..%2Fetc",
                      cookies=as_user("projektmanager")).status_code == 404


# ---------------------------------------------------------------------------
# Rechte: wer den Antrag nicht lesen darf, sieht auch keine Bewertung (404)
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_ohne_leserecht_kein_ergebnis_und_kein_start(lauf_env):
    client, laeufe = lauf_env["client"], lauf_env["laeufe"]
    assert _submit(client, "cfo", "Finanzplan", domaene="finance").status_code == 303
    _vorbereiteter_lauf(laeufe, "finanzplan", "vier")
    ma = as_user("mitarbeiter")
    assert client.get("/proposals/finanzplan/evaluation", cookies=ma).status_code == 404
    assert client.get("/proposals/finanzplan/evaluation?lauf=finanzplan-20260906-060000-vier",
                      cookies=ma).status_code == 404
    assert client.post("/proposals/finanzplan/evaluate", cookies=ma).status_code == 404
    assert client.post("/proposals/finanzplan/evaluate").status_code == 404  # Gast ebenso
    r = client.get("/proposals/evaluate", cookies=ma)
    assert r.status_code == 200 and "Finanzplan" not in r.text
    assert len([d for d in laeufe.iterdir() if d.is_dir()]) == 1
    # Der CFO sieht alles
    r = client.get("/proposals/finanzplan/evaluation", cookies=as_user("cfo"))
    assert r.status_code == 200 and "Gesamtscore: 5,0/10" in r.text
    # Ein fremder Lauf laesst sich nicht ueber einen lesbaren Antrag erreichen
    assert _submit(client, "projektmanager", "Offen").status_code == 303
    assert client.get("/proposals/offen/evaluation?lauf=finanzplan-20260906-060000-vier",
                      cookies=as_user("projektmanager")).status_code == 404


@pytest.mark.security
def test_gast_liest_oeffentlich_startet_aber_nicht(lauf_env):
    client = lauf_env["client"]
    assert _submit(client, "projektmanager", "Public", domaene="allgemein",
                   vertraulichkeit="oeffentlich").status_code == 303
    r = client.get("/proposals/public/evaluation")
    assert r.status_code == 200 and "noch nicht bewertet" in r.text
    assert "Bewertung starten" not in r.text
    assert client.post("/proposals/public/evaluate").status_code == 403


# ---------------------------------------------------------------------------
# Projektklammer: Dateien mit derselben project_id gehen zusammen in den Lauf
# ---------------------------------------------------------------------------


def test_projektklammer_ueber_project_id(lauf_env):
    import app.proposals as proposals

    client, laeufe = lauf_env["client"], lauf_env["laeufe"]
    d = proposals.proposals_dir()
    d.mkdir(parents=True, exist_ok=True)
    kopf = ("---\neingereicht_von: projektmanager\nrolle: PM\neingereicht_am: 2026-09-01T10:00:00\n"
            "vertraulichkeit: intern\ndomaene: projekt\nempfaenger: []\nproject_id: IP-2026-07\n---\n")
    (d / "klammer-charter.md").write_text(kopf + "# Klammer Charter\n\n## 1. Projektname\n\nX\n", encoding="utf-8")
    (d / "klammer-businesscase.md").write_text(kopf + "# Klammer Business Case\n\n## 1. Investition\n\nY\n", encoding="utf-8")
    (d / "fremd.md").write_text(kopf.replace("IP-2026-07", "IP-2026-99") + "# Fremd\n", encoding="utf-8")
    # Upload-Datei zum Charter
    up = proposals.uploads_dir() / "klammer-charter"
    up.mkdir(parents=True)
    (up / "anhang.md").write_text("# Anhang\n", encoding="utf-8")
    (up / "bild.png").write_bytes(b"\x89PNG")

    r = client.post("/proposals/klammer-charter/evaluate", cookies=as_user("projektmanager"))
    lauf_id = _lauf_id_aus(r.headers["location"])
    l = _warte_bis_fertig("klammer-charter", lauf_id)
    assert set(l.antraege) == {"klammer-charter", "klammer-businesscase"}
    stub_args = json.loads((laeufe / lauf_id / "stub_args.json").read_text(encoding="utf-8"))
    namen = [Path(p).name for p in stub_args["antraege"]]
    assert namen == ["klammer-charter.md", "klammer-businesscase.md", "anhang.md"]
    # Der Lauf ist auch vom Business Case aus erreichbar
    r = client.get("/proposals/klammer-businesscase/evaluation", cookies=as_user("projektmanager"))
    assert r.status_code == 200 and lauf_id in r.text and "Projektklammer aus 2 Dateien" in r.text


def test_orchestrator_nicht_startbar_wird_als_abbruch_gezeigt(lauf_env, monkeypatch):
    client, laeufe = lauf_env["client"], lauf_env["laeufe"]
    monkeypatch.setenv("MPB_ORCHESTRATOR_CMD", str(laeufe.parent / "gibt-es-nicht.exe"))
    assert _submit(client, "projektmanager", "Kaputt").status_code == 303
    r = client.post("/proposals/kaputt/evaluate", cookies=as_user("projektmanager"))
    assert r.status_code == 303
    r = client.get(r.headers["location"], cookies=as_user("projektmanager"))
    assert r.status_code == 200
    assert "Lauf abgebrochen" in r.text and "Exit-Code -1" in r.text
