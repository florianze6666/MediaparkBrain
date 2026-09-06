"""Kompass-Oberflaeche: Rechte bleiben, wo sie waren - nur die Seiten sind neu.

Die Sichtbarkeitsaussagen sind dieselben wie in test_access_routes/
test_security_fixes, nur an der neuen Stelle: Seitenliste unter /knowledge,
Antragsliste unter / und /proposals, Suche unter /search.
"""
from __future__ import annotations

import re

import pytest

from tests.conftest import as_user


def knowledge_slugs(html: str) -> set[str]:
    return set(re.findall(r'href="/knowledge/([a-z0-9-]+)"', html)) - {"share", "edit"}


def _submit(client, user: str, name: str, domaene: str = "projekt", files=None):
    return client.post(
        "/proposals/new",
        cookies=as_user(user),
        data={"project_name": name, "description": "Beschreibung",
              "domaene": domaene, "vertraulichkeit": "intern", "empfaenger": ""},
        files=files or {},
    )


# ---------------------------------------------------------------------------
# Wissen
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_knowledge_zeigt_finance_nur_dem_berechtigten(client):
    r = client.get("/knowledge", cookies=as_user("cfo"))
    assert r.status_code == 200
    assert "budget-finance" in knowledge_slugs(r.text)
    assert "Budget Finance" in r.text

    r = client.get("/knowledge", cookies=as_user("mitarbeiter"))
    assert r.status_code == 200
    assert "budget-finance" not in knowledge_slugs(r.text)
    assert "Budget Finance" not in r.text


@pytest.mark.security
def test_knowledge_detail_404_fuer_verbotene(client):
    m = as_user("mitarbeiter")
    r = client.get("/knowledge/budget-finance", cookies=m)
    assert r.status_code == 404
    # Fehlend und verboten sehen gleich aus (US-8)
    assert r.text == client.get("/knowledge/gibt-es-nicht", cookies=m).text
    assert client.get("/knowledge/budget-finance", cookies=as_user("cfo")).status_code == 200


@pytest.mark.security
def test_suche_findet_finance_nur_fuer_finance(client):
    r = client.get("/search?q=Budget", cookies=as_user("cfo"))
    assert r.status_code == 200
    assert "Budget Finance" in r.text

    r = client.get("/search?q=Budget", cookies=as_user("mitarbeiter"))
    assert r.status_code == 200
    assert "Budget Finance" not in r.text
    assert "budget-finance" not in knowledge_slugs(r.text)


# ---------------------------------------------------------------------------
# Antraege
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_dashboard_und_antragsliste_filtern_nach_rechten(client):
    assert _submit(client, "cfo", "Kostenprogramm", domaene="finance").status_code == 303
    for url in ("/", "/proposals"):
        r = client.get(url, cookies=as_user("cfo"))
        assert r.status_code == 200 and "Kostenprogramm" in r.text, url
        r = client.get(url, cookies=as_user("mitarbeiter"))
        assert r.status_code == 200, url
        assert "Kostenprogramm" not in r.text and "kostenprogramm" not in r.text, url


@pytest.mark.security
def test_antragsdatei_nur_mit_recht_und_ohne_traversal(client):
    r = _submit(client, "cfo", "Kostenprogramm", domaene="finance",
                files={"files": ("plan.md", b"# Plan\n\nInhalt", "text/markdown")})
    assert r.status_code == 303

    ok = client.get("/proposals/kostenprogramm/files/plan.md", cookies=as_user("cfo"))
    assert ok.status_code == 200
    assert b"Inhalt" in ok.content

    # Kein Leserecht -> 404, genau wie der Antrag selbst
    assert client.get("/proposals/kostenprogramm/files/plan.md",
                      cookies=as_user("mitarbeiter")).status_code == 404
    # Traversal im Dateinamen fuehrt nirgendwohin
    for name in ("../../permissions.yaml", "..%2f..%2fpermissions.yaml", "../plan.md"):
        r = client.get(f"/proposals/kostenprogramm/files/{name}", cookies=as_user("cfo"))
        assert r.status_code == 404, name


def test_evaluate_schreibt_cache(client, monkeypatch):
    """Ohne LLM-Key liefert die Bewertung ein Fehlerergebnis - auch das wird
    gespeichert, damit die Oberflaeche 'Lauf war da, kein Score' zeigen kann."""
    import app.evaluation_cache as cache

    monkeypatch.setenv("LLM_API_KEY", "")
    assert _submit(client, "projektmanager", "Testprojekt").status_code == 303
    assert cache.load("testprojekt") is None

    r = client.post("/proposals/testprojekt/evaluate", cookies=as_user("projektmanager"))
    assert r.status_code == 303
    assert (cache.evaluations_dir() / "testprojekt.json").exists()
    data = cache.load("testprojekt")
    assert data is not None and "error" in data

    # Kein Score aus einem Fehlerergebnis - vier leere Rollen
    import app.kompass as kompass
    assert all(r["score"] is None and r["state"] == "none" for r in kompass.role_scores(data))


def test_decide_ohne_vier_scores_ist_409(client):
    assert _submit(client, "projektmanager", "Testprojekt").status_code == 303
    r = client.post("/proposals/testprojekt/decide",
                    cookies=as_user("projektmanager"), data={"decision": "approve"})
    assert r.status_code == 409

    import app.proposals as proposals
    assert proposals.get_proposal("testprojekt").status == proposals.DEFAULT_STATUS


def test_decide_mit_vier_scores_setzt_status(client):
    import app.evaluation_cache as cache
    import app.proposals as proposals

    assert _submit(client, "projektmanager", "Testprojekt").status_code == 303
    cache.store("testprojekt", {
        key: {"status": "BEWERTET", "score": 8, "begruendung": "b",
              "fehlende_informationen": []}
        for key in ("betriebsrat", "cfo", "it", "ceo")
    })
    r = client.post("/proposals/testprojekt/decide",
                    cookies=as_user("projektmanager"), data={"decision": "approve"})
    assert r.status_code == 303
    p = proposals.get_proposal("testprojekt")
    assert p.status == "freigegeben"
    assert any("Entscheidung: freigegeben" in e["text"] for e in p.dialog)


def test_remind_hinterlaesst_vermerk_statt_mail(client):
    import app.proposals as proposals

    assert _submit(client, "projektmanager", "Testprojekt").status_code == 303
    r = client.post("/proposals/testprojekt/remind", cookies=as_user("projektmanager"))
    assert r.status_code == 303
    dialog = proposals.get_proposal("testprojekt").dialog
    assert dialog and dialog[-1]["kind"] == "internal"
    assert dialog[-1]["text"].startswith("Erinnerung vermerkt für")


# ---------------------------------------------------------------------------
# Vorbefuellung und Berechtigungen
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_prefill_ist_fuer_gast_verboten(client, monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "")  # Fallback statt echtem Modellaufruf
    r = client.post("/api/prefill?target=knowledge", json={"text": "Irgendein Text"})
    assert r.status_code == 403
    r = client.post("/api/prefill?target=proposal", json={"text": "Irgendein Text"},
                    cookies=as_user("projektmanager"))
    assert r.status_code == 200
    fields = r.json()["fields"]
    assert fields["description"] == "Irgendein Text"
    # Ohne Beleg im Text bleibt jedes Pflichtfeld leer - nichts geraten.
    assert fields["zielsetzung"] is None and fields["kosten"] is None


@pytest.mark.security
def test_admin_permissions_nur_admin_und_roundtrip(client):
    import app.access as access

    for user in ("mitarbeiter", "cfo", "gast"):
        c = as_user(user)
        assert client.get("/admin/permissions", cookies=c).status_code == 404
        assert client.post("/admin/permissions", cookies=c,
                           data={"changes": '{"alle/br": "rw"}'}).status_code == 404
    # nichts geschrieben
    assert "alle" not in access.load_permissions()["domaenen"]["br"]["lesen"]

    a = as_user("admin")
    assert client.get("/admin/permissions", cookies=a).status_code == 200

    # br ist fuer cfo gesperrt - hier liest selbst die Leitung nicht mit ...
    # (die Domaene hr taugt fuer diesen Test nicht: cfo ist in Gruppe leitung
    #  und darf hr laut permissions.yaml ohnehin lesen)
    from app.access import PageMeta
    br_meta = PageMeta(erstellt_von="betriebsrat", vertraulichkeit="intern", domaene="br")
    assert access.decide("cfo", br_meta) == access.DENY

    # ... bis der Admin die Gruppe finance in die Domaene br eintraegt
    r = client.post("/admin/permissions", cookies=a,
                    data={"changes": '{"finance/br": "rw"}'})
    assert r.status_code == 303
    assert "finance" in access.load_permissions()["domaenen"]["br"]["lesen"]
    assert access.decide("cfo", br_meta) == access.ALLOW
    assert any("Domäne br" in line and "finance" in line for line in access.read_changelog(5))

    # und wieder zurueck ('' = kein Recht)
    r = client.post("/admin/permissions", cookies=a, data={"changes": '{"finance/br": ""}'})
    assert r.status_code == 303
    assert access.decide("cfo", br_meta) == access.DENY


# ---------------------------------------------------------------------------
# View-Models (reine Funktionen, ohne TestClient)
# ---------------------------------------------------------------------------


def test_completeness_zaehlt_die_fuenfzehn_pflichtfelder(pages_env):
    import app.kompass as kompass
    import app.proposals as proposals
    from app.access import PageMeta

    p = proposals.save_proposal(
        "Leerer Antrag", "", [],
        PageMeta(erstellt_von="projektmanager", domaene="projekt"),
    )
    comp = kompass.completeness(p)
    assert comp["total"] == 15
    # Nur der Projektname steht fest -> 1 von 15
    assert comp["done"] == 1 and comp["pct"] == 7 and comp["state"] == "bad"
    assert {m["key"] for m in comp["missing"]} == {
        k for k, _ in kompass.PFLICHTFELDER
    } - {"projektname"}

    felder = {k: "x" for k, _ in kompass.PFLICHTFELDER}
    p2 = proposals.save_proposal(
        "Voller Antrag", "Beschreibung", [],
        PageMeta(erstellt_von="projektmanager", domaene="projekt"),
        felder=felder,
    )
    comp2 = kompass.completeness(proposals.get_proposal(p2.slug))
    assert comp2["done"] == 15 and comp2["pct"] == 100 and comp2["state"] == "ok"
    assert comp2["missing"] == []


def test_dashboard_rows_zeigt_nur_lesbares_und_keine_erfundenen_werte(pages_env):
    import app.kompass as kompass
    import app.proposals as proposals
    from app.access import PageMeta

    proposals.save_proposal(
        "Kostenprogramm", "Sparen", [],
        PageMeta(erstellt_von="cfo", erstellt_am="2026-09-01T09:00:00",
                 vertraulichkeit="intern", domaene="finance"),
        rolle="CFO / Controlling",
    )
    assert [r["name"] for r in kompass.dashboard_rows("cfo")] == ["Kostenprogramm"]
    assert kompass.dashboard_rows("mitarbeiter") == []

    row = kompass.dashboard_rows("cfo")[0]
    # Keine Bewertung im Cache -> kein Score, kein Ersatzwert
    assert row["total"] is None and row["total_state"] == "none"
    assert [r["key"] for r in row["roles"]] == ["BR", "CFO", "IT", "CEO"]
    assert all(r["score"] is None and r["state"] == "none" for r in row["roles"])
    # Was es nicht gibt, steht als Gedankenstrich da
    assert row["deadline"] == kompass.MISSING and row["deadline_urgent"] is False
    assert row["owner"] == "Eingebracht von CFO / Controlling"
    assert row["status_sentence"].startswith("Warten auf")
    assert row["next_anchor"] == "vollstaendigkeit"


def test_kpi_ohne_gremiumstermin_zeigt_gedankenstrich(pages_env, monkeypatch):
    import app.kompass as kompass

    monkeypatch.delenv("MPB_BOARD_DATE", raising=False)
    kpi = kompass.kpi("cfo", [])
    assert kpi["days_to_board"] == kompass.MISSING
    assert kpi["board_date"] == kompass.MISSING

    monkeypatch.setenv("MPB_BOARD_DATE", "2026-12-24")
    assert kompass.kpi("cfo", [])["board_date"] == "24.12."
