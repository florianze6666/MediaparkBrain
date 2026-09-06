"""Stufe 2, US-11/12: Vorschlaege tragen Einreicher + Rolle und folgen decide."""
from __future__ import annotations

import pytest

from tests.conftest import as_user

pytestmark = pytest.mark.security

LEGACY_RAW = (
    "# Altes Projekt\n\n"
    "Eingereicht am: 2026-08-01 10:00 UTC\n\n"
    "## Beschreibung\n\nAlte Beschreibung\nmit zwei Zeilen\n\n"
    "## Hochgeladene Dateien\n\n- charter.docx\n- case.xlsx\n"
)


def _submit(client, user, name, domaene="projekt", vertraulichkeit="intern", empfaenger=""):
    return client.post("/proposals/new", cookies=as_user(user), data={
        "project_name": name, "description": "Beschreibung von " + name,
        "domaene": domaene, "vertraulichkeit": vertraulichkeit, "empfaenger": empfaenger,
    })


def test_gast_darf_nicht_einreichen(client):
    assert client.get("/proposals/new").status_code == 403
    r = client.post("/proposals/new", data={"project_name": "X", "description": "Y"})
    assert r.status_code == 403
    import app.proposals as proposals
    assert proposals.list_proposals() == []


def test_vorschlag_traegt_nutzer_und_rolle(client):
    import app.proposals as proposals

    r = _submit(client, "projektmanager", "Neues Portal")
    assert r.status_code == 303 and r.headers["location"] == "/proposals/neues-portal"
    p = proposals.get_proposal("neues-portal")
    assert p.meta.erstellt_von == "projektmanager"
    assert p.rolle == "Projektmanager (Einreicher)"
    assert p.meta.domaene == "projekt"
    assert p.meta.vertraulichkeit == "intern"
    assert p.meta.quelle == "proposal"
    assert p.meta.erstellt_am and "T" in p.meta.erstellt_am
    assert p.description == "Beschreibung von Neues Portal"
    raw = p.path.read_text(encoding="utf-8")
    assert raw.startswith("---\n")
    assert "eingereicht_von: projektmanager" in raw
    assert "rolle: Projektmanager (Einreicher)" in raw
    assert "domaene: projekt" in raw
    # Marcs Format bleibt nach dem Kopf erhalten
    assert "# Neues Portal\n\nEingereicht am:" in raw
    assert "## Beschreibung" in raw and "## Hochgeladene Dateien" in raw


def test_finance_vorschlag_nur_fuer_finance(client):
    r = _submit(client, "cfo", "Kostenprogramm", domaene="finance")
    assert r.status_code == 303
    slug = "kostenprogramm"

    # mitarbeiter: nicht in Liste, 404 auf Ansicht und Loeschen
    m = as_user("mitarbeiter")
    r = client.get("/proposals", cookies=m)
    assert r.status_code == 200
    assert "Kostenprogramm" not in r.text and slug not in r.text
    r404 = client.get(f"/proposals/{slug}", cookies=m)
    assert r404.status_code == 404
    assert r404.text == client.get("/wiki/gibt-es-nicht", cookies=m).text  # gleiche 404-Seite
    assert client.post(f"/proposals/{slug}/delete", cookies=m).status_code == 404
    assert client.get("/proposals/gibt-es-nicht", cookies=m).status_code == 404

    # cfo sieht ihn, inkl. Herkunftsbox mit Rolle
    c = as_user("cfo")
    r = client.get("/proposals", cookies=c)
    assert "Kostenprogramm" in r.text
    assert "Eingebracht von" in r.text and "CFO / Controlling" in r.text
    r = client.get(f"/proposals/{slug}", cookies=c)
    assert r.status_code == 200
    assert "Eingebracht von" in r.text
    assert "Rolle <strong>CFO / Controlling</strong>" in r.text
    assert "Quelle: Projektvorschlag" in r.text

    import app.proposals as proposals
    assert proposals.get_proposal_for(slug, "mitarbeiter") is None
    assert proposals.get_proposal_for(slug, "cfo") is not None
    assert [p.slug for p in proposals.list_proposals("mitarbeiter")] == []
    assert [p.slug for p in proposals.list_proposals("cfo")] == [slug]

    # Vorschlag existiert noch (Loeschversuch des Mitarbeiters war 404), cfo darf loeschen
    assert proposals.get_proposal(slug) is not None
    assert client.post(f"/proposals/{slug}/delete", cookies=c).status_code == 303
    assert proposals.get_proposal(slug) is None


def test_rolle_ist_snapshot(client):
    """Die Rolle wird zum Zeitpunkt der Einreichung festgehalten, nicht nachgeschlagen."""
    import app.proposals as proposals

    _submit(client, "cfo", "Snapshot Test")
    p = proposals.get_proposal("snapshot-test")
    raw = p.path.read_text(encoding="utf-8").replace("rolle: CFO / Controlling", "rolle: Ehemals CFO")
    p.path.write_text(raw, encoding="utf-8")
    assert proposals.get_proposal("snapshot-test").rolle == "Ehemals CFO"


def test_altbestand_ohne_kopf_parst_wie_bisher(pages_env):
    import app.proposals as proposals

    d = proposals.proposals_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / "altes-projekt.md").write_text(LEGACY_RAW, encoding="utf-8")
    p = proposals.get_proposal("altes-projekt")
    assert p.project_name == "Altes Projekt"
    assert p.submitted_at == "2026-08-01 10:00 UTC"
    assert p.description == "Alte Beschreibung\nmit zwei Zeilen"
    assert p.files == ["charter.docx", "case.xlsx"]
    assert p.meta.erstellt_von == "unbekannt"
    assert p.meta.domaene == "projekt"
    assert p.meta.vertraulichkeit == "intern"
    assert p.rolle == "unbekannt"
    # Altbestand ist intern/projekt: mitarbeiter sieht ihn, gast nicht
    assert [x.slug for x in proposals.list_proposals("mitarbeiter")] == ["altes-projekt"]
    assert proposals.list_proposals("gast") == []


def test_altbestand_mit_fremdem_kopf_wird_uebersprungen(pages_env):
    """Marcs Vorschlaege haben einen eigenen Kopf (project_id, classification...)."""
    import app.proposals as proposals

    d = proposals.proposals_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / "m-test.md").write_text(
        "---\nproject_id: BC-1\nproject_name: \"M:TEST | Demo\"\nclassification: internal\n---\n\n"
        "# Projektvorschlag\n\n## Projektname\n\nM:TEST\n", encoding="utf-8",
    )
    p = proposals.get_proposal("m-test")
    assert p.project_name == "M:TEST | Demo"
    assert p.meta.erstellt_von == "unbekannt"
    assert p.meta.domaene == "projekt"
    assert p.rolle == "unbekannt"


def test_altbestand_zeigt_herkunft_unbekannt(client):
    import app.proposals as proposals

    d = proposals.proposals_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / "altes-projekt.md").write_text(LEGACY_RAW, encoding="utf-8")
    r = client.get("/proposals/altes-projekt", cookies=as_user("mitarbeiter"))
    assert r.status_code == 200
    assert "Herkunft unbekannt (Altbestand)" in r.text
    r = client.get("/proposals", cookies=as_user("mitarbeiter"))
    assert "Herkunft unbekannt (Altbestand)" in r.text


def test_vertraulicher_vorschlag_nur_ersteller_und_empfaenger(client):
    _submit(client, "projektmanager", "Geheimprojekt", vertraulichkeit="vertraulich",
            empfaenger="pmo-leitung")
    assert client.get("/proposals/geheimprojekt", cookies=as_user("projektmanager")).status_code == 200
    assert client.get("/proposals/geheimprojekt", cookies=as_user("pmo-leitung")).status_code == 200
    assert client.get("/proposals/geheimprojekt", cookies=as_user("mitarbeiter")).status_code == 404
    assert client.get("/proposals/geheimprojekt", cookies=as_user("ceo")).status_code == 404


def test_doppelter_name_bleibt_409(client):
    _submit(client, "projektmanager", "Doppelt")
    r = _submit(client, "cfo", "Doppelt")
    assert r.status_code == 409
    assert "bereits eingereicht" in r.text

FILE_RAW = (
    "---\nproject_id: BC-2026-0001\nproject_name: \"Datei-Antrag\"\nclassification: internal\n---\n\n"
    "# Projektvorschlag\n\n## Beschreibung des vorgeschlagenen Vorhabens\n\nText aus der Datei.\n\n"
    "## Business Case\n\nROI 3,1\n"
)


def test_datei_antrag_ohne_beschreibungsabschnitt_liefert_body(pages_env):
    """Charter, Business Case und Marcs Format haben kein '## Beschreibung':
    dann ist der Body nach der Titelzeile die Beschreibung (Fallback)."""
    import app.proposals as proposals

    proposals.proposals_dir().mkdir(parents=True, exist_ok=True)
    (proposals.proposals_dir() / "datei-antrag.md").write_text(FILE_RAW, encoding="utf-8")
    p = proposals.get_proposal("datei-antrag")
    assert p.project_name == "Datei-Antrag"
    assert "Text aus der Datei." in p.description and "ROI 3,1" in p.description
    assert not p.description.startswith("# ")
    assert p.files == []
