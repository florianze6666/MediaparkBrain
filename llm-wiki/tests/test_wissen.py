"""Phase 5: Wissen erweitern (UC-03) und zuruecksetzen (UC-01), Antraege im Index (I-3).

Import und Reset laufen als Subprozess; hier ersetzen Stubs die Skripte aus
qmd/ingest/ (MPB_IMPORT_CMD, MPB_RESET_CMD). Korpus, Jobs, Antraege und Laeufe liegen
unter tmp_path (conftest). Kein Test ruft qmd, die API oder den echten Korpus.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pytest

from tests.conftest import as_user
from tests.test_proposals import _submit

IMPORT_STUB = '''
import json, os, sys, time
from pathlib import Path
args = sys.argv[1:]
aufruf = Path(os.environ["MPB_STUB_AUFRUFE"])
with aufruf.open("a", encoding="utf-8") as fh:
    fh.write(json.dumps({"skript": "import", "args": args, "cwd": os.getcwd(),
                         "corpus": os.environ.get("MPB_CORPUS_DIR"),
                         "proposals": os.environ.get("MPB_PROPOSALS_DIR")}) + "\\n")
n = int(os.environ.get("MPB_STUB_N", "2"))
langsam = os.environ.get("MPB_STUB_LANGSAM") == "1"
print(f"Wissen: {n} Dateien", flush=True)
for i in range(1, n + 1):
    print(f"Sicht: {i} von {n} datei{i}.md", flush=True)
    if langsam:
        time.sleep(0.6)
print("Index: qmd update", flush=True)
print("Einbettung: 50 %", flush=True)
print("Einbettung: 100 %", flush=True)
if os.environ.get("MPB_STUB_FEHLER") == "1":
    print("FEHLER: qmd embed, Exit 1", flush=True)
    sys.exit(1)
print(f"Fertig: Wissen {n} von {n} verarbeitet, Index 7 Dokumente, 9 Vektoren", flush=True)
'''

RESET_STUB = '''
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
with Path(os.environ["MPB_STUB_AUFRUFE"]).open("a", encoding="utf-8") as fh:
    fh.write(json.dumps({"skript": "reset", "args": args, "cwd": os.getcwd()}) + "\\n")
print(f"Reset: {args[0]}: Deleted 3 documents", flush=True)
print(f"Fertig: {args[0]} zurueckgesetzt, Index 7 -> 4 Dokumente, 9 -> 5 Vektoren", flush=True)
'''


@pytest.fixture
def wissen_env(client, tmp_path, monkeypatch):
    import app.wissen as wissen

    imp = tmp_path / "stub_import.py"
    imp.write_text(IMPORT_STUB, encoding="utf-8")
    rst = tmp_path / "stub_reset.py"
    rst.write_text(RESET_STUB, encoding="utf-8")
    aufrufe = tmp_path / "aufrufe.jsonl"
    qmd = tmp_path / "qmd"
    qmd.mkdir()
    monkeypatch.setenv("MPB_QMD_DIR", str(qmd))
    monkeypatch.setenv("MPB_LAEUFE_DIR", str(tmp_path / "laeufe"))
    monkeypatch.setenv("MPB_IMPORT_CMD", f'"{sys.executable}" "{imp}"')
    monkeypatch.setenv("MPB_RESET_CMD", f'"{sys.executable}" "{rst}"')
    monkeypatch.setenv("MPB_STUB_AUFRUFE", str(aufrufe))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")  # Kopfdaten ueber den deterministischen Rueckfall
    for k in ("MPB_STUB_N", "MPB_STUB_LANGSAM", "MPB_STUB_FEHLER"):
        monkeypatch.delenv(k, raising=False)
    wissen._PROZESSE.clear()
    return {"client": client, "tmp": tmp_path, "aufrufe": aufrufe,
            "corpus": tmp_path / "corpus", "jobs": tmp_path / "jobs"}


def _aufrufe(env) -> list[dict]:
    f = env["aufrufe"]
    if not f.exists():
        return []
    return [json.loads(z) for z in f.read_text(encoding="utf-8").splitlines() if z.strip()]


def _warte(job_id: str, timeout: float = 15.0):
    import app.wissen as wissen

    ende = time.time() + timeout
    while time.time() < ende:
        j = wissen.job_fuer(job_id)
        if j is not None and not j.laeuft:
            return j
        time.sleep(0.1)
    raise AssertionError(f"Job {job_id} nicht fertig geworden")


def _job_id(location: str) -> str:
    assert location.startswith("/wissen/jobs/"), location
    return location.rsplit("/", 1)[1]


def _upload(client, uid: str, dateien: list[tuple[str, bytes]]):
    files = [("files", (name, data, "application/octet-stream")) for name, data in dateien]
    return client.post("/wissen/upload", cookies=as_user(uid), files=files)


# ---------------------------------------------------------------------------
# UC-03: Upload -> corpus/erweiterung -> Import mit Fortschritt
# ---------------------------------------------------------------------------


def test_upload_zwei_dateien_landen_im_korpus_und_starten_import(wissen_env):
    client, corpus = wissen_env["client"], wissen_env["corpus"]
    r = _upload(client, "projektmanager", [
        ("Richtlinie Stammdaten.md", "# Richtlinie Stammdaten\n\nJedes Materialstammobjekt hat einen Verantwortlichen.\n".encode()),
        ("notiz.txt", "Kurze Notiz zur Datenpflege in Eisenach.".encode()),
    ])
    assert r.status_code == 303, r.text
    job_id = _job_id(r.headers["location"])
    erweiterung = corpus / "erweiterung"
    dateien = sorted(p.name for p in erweiterung.glob("*.md"))
    assert len(dateien) == 2
    text = (erweiterung / "richtlinie-stammdaten.md").read_text(encoding="utf-8")
    kopf = text.split("---")[1]
    for feld in ("doc_id:", "titel:", "dokumenttyp:", "datum:", "verfasser:", "rolle:",
                 "organisationseinheit:", "empfaenger:", "projekt:", "geschaeftsbereich:",
                 "vertraulichkeit: intern", "informationsdomaene:", "ablageort: erweiterung",
                 "quelle: upload", "erstellt_von: projektmanager", "original_datei: Richtlinie Stammdaten.md"):
        assert feld in kopf, feld
    assert kopf.index("titel:") < kopf.index("vertraulichkeit:") < kopf.index("ablageort:")
    assert "Jedes Materialstammobjekt hat einen Verantwortlichen." in text
    assert "# Richtlinie Stammdaten" in text
    # Original bleibt erhalten, getrennt vom Korpus
    uploads = Path(client.app.state.__dict__.get("uploads", "")) if False else None  # noqa: F841
    import app.wiki as wiki
    assert (wiki.uploads_dir() / "erweiterung" / "Richtlinie_Stammdaten.md").exists()

    job = _warte(job_id)
    assert job.fertig and job.exit_code == 0
    aufruf = _aufrufe(wissen_env)[0]
    assert aufruf["skript"] == "import" and aufruf["args"] == ["wissen", "--ablageort", "erweiterung"]
    assert aufruf["corpus"] == str(corpus)
    assert Path(aufruf["cwd"]) == wissen_env["tmp"] / "qmd"
    r = client.get(f"/wissen/jobs/{job_id}", cookies=as_user("projektmanager"))
    assert r.status_code == 200
    assert "Fertig: Wissen 2 von 2" in r.text and "fertig" in r.text
    assert 'href="/wissen/upload" class="btn btn-proposal">OK' in r.text
    assert "richtlinie-stammdaten.md" in r.text


def test_fortschritt_waehrend_des_laufs_sichtbar(wissen_env, monkeypatch):
    client = wissen_env["client"]
    monkeypatch.setenv("MPB_STUB_LANGSAM", "1")
    monkeypatch.setenv("MPB_STUB_N", "3")
    r = _upload(client, "projektmanager", [("a.md", b"# A\n\nText A"), ("b.md", b"# B\n\nText B"), ("c.md", b"# C\n\nText C")])
    assert r.status_code == 303
    job_id = _job_id(r.headers["location"])
    gesehen = set()
    for _ in range(40):
        r = client.get(f"/wissen/jobs/{job_id}", cookies=as_user("projektmanager"))
        for n in (1, 2, 3):
            if f"Sicht: {n} von 3" in r.text:
                gesehen.add(n)
        if "Fertig:" in r.text:
            break
        time.sleep(0.15)
    assert gesehen, "kein Zwischenstand n von N gesehen"
    job = _warte(job_id)
    assert job.fertig
    # Zweiter Upload waehrend eines Laufs wird abgewiesen (ein Job zugleich)
    monkeypatch.setenv("MPB_STUB_LANGSAM", "1")
    r1 = _upload(client, "projektmanager", [("d.md", b"# D\n\nText D")])
    assert r1.status_code == 303
    r2 = _upload(client, "cfo", [("e.md", b"# E\n\nText E")])
    assert r2.status_code == 409 and "läuft gerade" in r2.text
    _warte(_job_id(r1.headers["location"]))


def test_vertraulichkeit_kommt_aus_der_rolle(wissen_env):
    client, corpus = wissen_env["client"], wissen_env["corpus"]
    assert _upload(client, "betriebsrat", [("protokoll.md", b"# Protokoll\n\nSitzung.")]).status_code == 303
    _warte(_job_id_letzter(wissen_env))
    assert "vertraulichkeit: Betriebsrat-intern" in (corpus / "erweiterung" / "protokoll.md").read_text(encoding="utf-8")
    assert "Einstufung: Betriebsrat-intern" in (corpus / "erweiterung" / "protokoll.md").read_text(encoding="utf-8")
    assert _upload(client, "ceo", [("memo.md", b"# Memo\n\nZielbild.")]).status_code == 303
    _warte(_job_id_letzter(wissen_env))
    assert "vertraulichkeit: C-Level" in (corpus / "erweiterung" / "memo.md").read_text(encoding="utf-8")
    # gleicher Titel noch einmal: eindeutiger Slug statt Ueberschreiben
    assert _upload(client, "ceo", [("memo.md", b"# Memo\n\nZweite Fassung.")]).status_code == 303
    _warte(_job_id_letzter(wissen_env))
    assert (corpus / "erweiterung" / "memo-2.md").exists()
    assert "Zielbild." in (corpus / "erweiterung" / "memo.md").read_text(encoding="utf-8")


def _job_id_letzter(env) -> str:
    import app.wissen as wissen
    return wissen.letzte_jobs(1)[0].job_id


def test_gast_leere_datei_und_fehlende_datei(wissen_env):
    client, corpus = wissen_env["client"], wissen_env["corpus"]
    r = client.post("/wissen/upload", files=[("files", ("x.md", b"# X", "text/plain"))])
    assert r.status_code == 403
    r = _upload(client, "projektmanager", [("leer.md", b"")])
    assert r.status_code == 400 and "leer" in r.text
    r = client.post("/wissen/upload", cookies=as_user("projektmanager"))
    assert r.status_code in (400, 422)
    assert not (corpus / "erweiterung").exists() or not list((corpus / "erweiterung").glob("*.md"))
    assert _aufrufe(wissen_env) == []
    r = client.get("/wissen/upload", cookies=as_user("projektmanager"))
    assert r.status_code == 200 and "erweiterung" in r.text and "intern" in r.text


def test_fehlgeschlagener_import_bleibt_sichtbar(wissen_env, monkeypatch):
    client = wissen_env["client"]
    monkeypatch.setenv("MPB_STUB_FEHLER", "1")
    r = _upload(client, "projektmanager", [("a.md", b"# A\n\nText")])
    job = _warte(_job_id(r.headers["location"]))
    assert job.status == "fehler" and job.exit_code == 1
    r = client.get(f"/wissen/jobs/{job.job_id}", cookies=as_user("projektmanager"))
    assert "abgebrochen" in r.text and "FEHLER: qmd embed" in r.text


def test_fremder_job_ist_unsichtbar_admin_sieht_ihn(wissen_env):
    client = wissen_env["client"]
    r = _upload(client, "projektmanager", [("a.md", b"# A\n\nText")])
    job_id = _job_id(r.headers["location"])
    _warte(job_id)
    assert client.get(f"/wissen/jobs/{job_id}", cookies=as_user("cfo")).status_code == 404
    assert client.get(f"/wissen/jobs/{job_id}").status_code == 404
    assert client.get(f"/wissen/jobs/{job_id}", cookies=as_user("admin")).status_code == 200
    assert client.get("/wissen/jobs/..", cookies=as_user("admin")).status_code == 404


# ---------------------------------------------------------------------------
# UC-01: Reset, getrennt, nur admin, nur mit RESET
# ---------------------------------------------------------------------------


def test_reset_wissen_verlangt_admin_und_bestaetigung(wissen_env):
    client = wissen_env["client"]
    r = client.post("/admin/reset/wissen", cookies=as_user("cfo"), data={"bestaetigung": "RESET"})
    assert r.status_code == 404
    r = client.post("/admin/reset/wissen", cookies=as_user("admin"), data={"bestaetigung": "ja"})
    assert r.status_code == 303 and "reset-bestaetigung" in r.headers["location"]
    assert _aufrufe(wissen_env) == []
    r = client.get("/admin?meldung=reset-bestaetigung", cookies=as_user("admin"))
    assert "RESET" in r.text and "Unternehmenswissen zurücksetzen" in r.text
    r = client.post("/admin/reset/wissen", cookies=as_user("admin"), data={"bestaetigung": "RESET"})
    assert r.status_code == 303
    job = _warte(_job_id(r.headers["location"]))
    assert job.fertig and job.art == "reset-wissen"
    aufruf = _aufrufe(wissen_env)[-1]
    assert aufruf["skript"] == "reset" and aufruf["args"] == ["wissen"]
    r = client.get(f"/wissen/jobs/{job.job_id}", cookies=as_user("admin"))
    assert "Fertig: wissen zurueckgesetzt" in r.text
    import app.access as access
    assert any("Unternehmenswissen zurückgesetzt" in z for z in access.read_changelog(5))


def test_reset_antraege_loescht_dateien_uploads_laeufe_und_index(wissen_env, tmp_path):
    client = wissen_env["client"]
    import app.bewertung as bewertung
    import app.proposals as proposals

    assert _submit(client, "projektmanager", "Antrag Eins").status_code == 303
    r = client.post("/proposals/new", cookies=as_user("cfo"),
                    data={"project_name": "Antrag Zwei", "description": "Mit Datei"},
                    files=[("files", ("bc.md", b"# BC\n\nBusiness Case", "text/plain"))])
    assert r.status_code == 303
    assert len(proposals.list_proposals()) == 2
    assert (proposals.uploads_dir() / "antrag-zwei" / "bc.md").exists()
    lauf = bewertung.laeufe_dir() / "antrag-eins-20260906-060000"
    lauf.mkdir(parents=True)
    (lauf / "wiki.json").write_text("{}", encoding="utf-8")

    r = client.post("/admin/reset/antraege", cookies=as_user("admin"), data={"bestaetigung": "RESET"})
    assert r.status_code == 303
    job = _warte(_job_id(r.headers["location"]))
    assert job.fertig and job.art == "reset-antraege"
    assert proposals.list_proposals() == []
    assert not (proposals.uploads_dir()).exists() or not any(proposals.uploads_dir().iterdir())
    assert not lauf.exists()
    aufruf = _aufrufe(wissen_env)[-1]
    assert aufruf["skript"] == "reset" and aufruf["args"] == ["antraege"]
    # Der Korpus und die Wissens-Collections sind nicht angefasst worden
    assert all(a["args"] != ["wissen"] for a in _aufrufe(wissen_env))
    r = client.get("/admin", cookies=as_user("admin"))
    assert "Projektanträge: <strong>0</strong>" in r.text and "Projektanträge zurücksetzen" in r.text


def test_korpus_import_mit_fortschritt(wissen_env, monkeypatch):
    client, corpus = wissen_env["client"], wissen_env["corpus"]
    (corpus / "it_doku").mkdir(parents=True)
    for i in range(3):
        (corpus / "it_doku" / f"d{i}.md").write_text(f"# D{i}\n\nText", encoding="utf-8")
    monkeypatch.setenv("MPB_STUB_N", "3")
    r = client.get("/admin", cookies=as_user("admin"))
    assert "Korpus importieren (3 Dokumente)" in r.text
    assert client.post("/admin/import/corpus", cookies=as_user("cfo")).status_code == 404
    r = client.post("/admin/import/corpus", cookies=as_user("admin"))
    assert r.status_code == 303
    job = _warte(_job_id(r.headers["location"]))
    assert job.fertig and job.art == "import-corpus"
    assert _aufrufe(wissen_env)[-1]["args"] == ["wissen"]
    r = client.get(f"/wissen/jobs/{job.job_id}", cookies=as_user("admin"))
    assert "Fertig: Wissen 3 von 3" in r.text and 'href="/admin"' in r.text
    r = client.get("/admin", cookies=as_user("admin"))
    assert "Unternehmenswissen aus corpus/ importieren" in r.text


def test_zweiter_job_waehrend_eines_laufs_wird_abgewiesen(wissen_env, monkeypatch):
    client = wissen_env["client"]
    monkeypatch.setenv("MPB_STUB_LANGSAM", "1")
    monkeypatch.setenv("MPB_STUB_N", "3")
    r = client.post("/admin/import/corpus", cookies=as_user("admin"))
    job_id = _job_id(r.headers["location"])
    r = client.post("/admin/reset/wissen", cookies=as_user("admin"), data={"bestaetigung": "RESET"})
    assert r.status_code == 303 and "job-aktiv" in r.headers["location"]
    r = client.get("/admin", cookies=as_user("admin"))
    assert "Es läuft gerade der Job" in r.text
    _warte(job_id)
    assert [a["skript"] for a in _aufrufe(wissen_env)] == ["import"]


# ---------------------------------------------------------------------------
# I-3: Einreichen legt den Antrag im Hintergrund in die Collection antraege
# ---------------------------------------------------------------------------


def test_einreichen_startet_antrags_import_wenn_aktiv(wissen_env, monkeypatch):
    client = wissen_env["client"]
    monkeypatch.setenv("MPB_INDEX_ANTRAEGE", "1")
    assert _submit(client, "projektmanager", "Antrag Index").status_code == 303
    import app.wissen as wissen
    jobs = wissen.letzte_jobs(1)
    assert jobs and jobs[0].art == "import-antraege"
    job = _warte(jobs[0].job_id)
    assert job.fertig
    aufruf = _aufrufe(wissen_env)[-1]
    assert aufruf["args"] == ["antraege"]
    assert aufruf["proposals"].endswith("project_proposals")


def test_einreichen_ohne_index_bleibt_still(wissen_env):
    client = wissen_env["client"]
    assert _submit(client, "projektmanager", "Antrag Still").status_code == 303
    import app.wissen as wissen
    assert wissen.letzte_jobs(1) == []
    assert _aufrufe(wissen_env) == []
