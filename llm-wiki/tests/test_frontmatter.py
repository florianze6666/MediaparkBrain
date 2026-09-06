"""Frontmatter: schreiben, lesen, Defaults, Bearbeiten erhaelt Ersteller."""
from __future__ import annotations

import pytest

from tests.conftest import as_user


def test_save_und_get_roundtrip(pages_env):
    import app.wiki as wiki
    from app.access import PageMeta

    meta = PageMeta(
        erstellt_von="cfo", erstellt_am="2026-09-05T18:30:00",
        vertraulichkeit="vertraulich", domaene="finance",
        empfaenger=["leitung", "pmo-leitung"], ablageort="sharepoint_finance/q4",
        quelle="upload",
    )
    wiki.save_page("roundtrip", "Roundtrip Seite", "Absatz eins.\n\nAbsatz zwei.", meta)

    # vertraulich + finance -> pages/finance/vertraulich/ (US-17)
    raw = (pages_env / "finance" / "vertraulich" / "roundtrip.md").read_text(encoding="utf-8")
    assert raw.startswith("---\n")
    assert "erstellt_von: cfo" in raw
    assert "domaene: finance" in raw
    assert "# Roundtrip Seite" in raw
    # Frontmatter steht VOR dem Titel
    assert raw.index("---\n", 4) < raw.index("# Roundtrip Seite")

    page = wiki.get_page("roundtrip")
    assert page.title == "Roundtrip Seite"
    assert page.content == "Absatz eins.\n\nAbsatz zwei."
    assert page.meta.to_dict() == meta.to_dict()


def test_ohne_frontmatter_defaults(pages_env):
    import app.wiki as wiki

    page = wiki.get_page("altbestand")
    assert page.title == "Altbestand"
    assert "---" not in page.content
    assert page.meta.erstellt_von == "unbekannt"
    assert page.meta.vertraulichkeit == "intern"
    assert page.meta.domaene == "allgemein"
    assert page.meta.empfaenger == []
    assert page.meta.quelle == "wiki"


def test_meta_from_dict_robust(pages_env):
    from app.access import PageMeta

    m = PageMeta.from_dict({"erstellt_von": None, "vertraulichkeit": "geheim",
                            "empfaenger": "a, b", "unbekanntes_feld": 1})
    assert m.erstellt_von == "unbekannt"
    assert m.vertraulichkeit == "intern"
    assert m.empfaenger == ["a", "b"]
    assert PageMeta.from_dict(None).domaene == "allgemein"


def test_bearbeiten_setzt_geaendert_und_erhaelt_ersteller(client):
    import app.wiki as wiki

    before = wiki.get_page("budget-finance")
    assert before.meta.geaendert_von == ""

    r = client.post("/wiki/budget-finance/edit", cookies=as_user("ceo"), data={
        "title": "Budget Finance",
        "content": "Neuer Inhalt.",
        "vertraulichkeit": "intern",
        "domaene": "finance",
        "empfaenger": "",
    })
    assert r.status_code == 303

    after = wiki.get_page("budget-finance")
    assert after.content == "Neuer Inhalt."
    assert after.meta.erstellt_von == "cfo"
    assert after.meta.erstellt_am == "2026-09-01T10:00:00"
    assert after.meta.geaendert_von == "ceo"
    assert after.meta.geaendert_am

    r = client.get("/wiki/budget-finance", cookies=as_user("ceo"))
    assert "Zuletzt geändert von" in r.text
    assert "CEO / Strategie" in r.text


def test_altbestand_bekommt_meta_beim_speichern(client):
    import app.wiki as wiki

    r = client.post("/wiki/altbestand/edit", cookies=as_user("mitarbeiter"), data={
        "title": "Altbestand", "content": "ueberarbeitet",
        "vertraulichkeit": "intern", "domaene": "allgemein", "empfaenger": "",
    })
    assert r.status_code == 303
    raw = (wiki.pages_dir() / "allgemein" / "altbestand.md").read_text(encoding="utf-8")
    assert raw.startswith("---\n")
    page = wiki.get_page("altbestand")
    assert page.meta.erstellt_von == "unbekannt"
    assert page.meta.geaendert_von == "mitarbeiter"


def test_list_pages_ungefiltert_vs_gefiltert(pages_env):
    import app.wiki as wiki

    alle = {p.slug for p in wiki.list_pages()}
    assert {"budget-finance", "br-protokoll", "oeffentlich", "vertraulich-projekt", "altbestand"} <= alle
    assert {p.slug for p in wiki.list_pages("gast")} == {"oeffentlich"}
    assert {p.slug for p in wiki.list_pages("mitarbeiter")} == {"oeffentlich", "altbestand"}
    assert wiki.get_page_for("budget-finance", "mitarbeiter") is None
    assert wiki.get_page_for("budget-finance", "cfo") is not None
    assert wiki.get_page_for("gibt-es-nicht", "cfo") is None


def test_yaml_reparatur_rettet_unquotiertes_modell_frontmatter():
    """Modelle liefern je nach Lauf `titel: Sitzung: Thema` oder `rolle: -`.

    Beides ist ungueltiges YAML. Frueher verfiel dadurch der komplette
    generierte Dokumentkopf still zum Fallback, obwohl der Inhalt brauchbar
    war - der Nutzer bekam Titel aus dem Dateinamen statt aus dem Dokument.
    """
    import yaml

    from app.llm_metadata import _yaml_reparieren

    kaputt = (
        "titel: Betriebsratssitzung: Einfuehrung KI\n"
        "rolle: -\n"
        "empfaenger: [br, it]\n"
        "informationsdomaene: []\n"
    )
    with pytest.raises(yaml.YAMLError):
        yaml.safe_load(kaputt)

    daten = yaml.safe_load(_yaml_reparieren(kaputt))
    # Der Doppelpunkt im Titel bleibt erhalten, statt die Zeile zu sprengen.
    assert daten["titel"] == "Betriebsratssitzung: Einfuehrung KI"
    assert daten["rolle"] == "-"
    # Listen bleiben Listen und werden nicht zu Strings quotiert.
    assert daten["empfaenger"] == ["br", "it"]
    assert daten["informationsdomaene"] == []
