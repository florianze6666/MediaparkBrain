"""Stufe 2, US-17/18/19: Ablage nach Domaene, Ordner = Wahrheit, Migration."""
from __future__ import annotations

import pytest

from tests.conftest import FINANCE_TEXT, as_user


def test_save_page_legt_datei_im_domaenenordner_an(pages_env):
    import app.wiki as wiki
    from app.access import PageMeta

    wiki.save_page("notiz", "Notiz", "Text", PageMeta(erstellt_von="cfo", domaene="einkauf"))
    assert (pages_env / "einkauf" / "notiz.md").exists()
    assert not (pages_env / "notiz.md").exists()
    # Fixture-Seiten liegen ebenfalls in ihren Ordnern
    assert (pages_env / "finance" / "budget-finance.md").exists()
    assert (pages_env / "br" / "br-protokoll.md").exists()
    assert (pages_env / "allgemein" / "oeffentlich.md").exists()


def test_vertraulich_liegt_im_unterordner(pages_env):
    import app.wiki as wiki

    assert (pages_env / "projekt" / "vertraulich" / "vertraulich-projekt.md").exists()
    page = wiki.get_page("vertraulich-projekt")
    assert page.meta.vertraulichkeit == "vertraulich"
    assert page.path == pages_env / "projekt" / "vertraulich" / "vertraulich-projekt.md"


def test_domaenenwechsel_verschiebt_datei(pages_env):
    import app.wiki as wiki

    page = wiki.get_page("budget-finance")
    page.meta.domaene = "einkauf"
    wiki.save_page(page.slug, page.title, page.content, page.meta)
    assert (pages_env / "einkauf" / "budget-finance.md").exists()
    assert not (pages_env / "finance" / "budget-finance.md").exists()
    assert wiki.get_page("budget-finance").meta.domaene == "einkauf"
    # Vertraulich-Wechsel verschiebt in den Unterordner und zurueck
    page.meta.vertraulichkeit = "vertraulich"
    wiki.save_page(page.slug, page.title, page.content, page.meta)
    assert (pages_env / "einkauf" / "vertraulich" / "budget-finance.md").exists()
    assert not (pages_env / "einkauf" / "budget-finance.md").exists()
    page.meta.vertraulichkeit = "intern"
    wiki.save_page(page.slug, page.title, page.content, page.meta)
    assert (pages_env / "einkauf" / "budget-finance.md").exists()
    assert not (pages_env / "einkauf" / "vertraulich" / "budget-finance.md").exists()
    # genau eine Datei mit dem Slug
    assert len(list(pages_env.rglob("budget-finance.md"))) == 1


def test_domaenenwechsel_ueber_editor_verschiebt(client):
    import app.wiki as wiki

    r = client.post("/wiki/budget-finance/edit", cookies=as_user("cfo"), data={
        "title": "Budget Finance", "content": "Inhalt",
        "vertraulichkeit": "intern", "domaene": "einkauf", "empfaenger": "",
    })
    assert r.status_code == 303
    assert (wiki.pages_dir() / "einkauf" / "budget-finance.md").exists()
    assert not (wiki.pages_dir() / "finance" / "budget-finance.md").exists()


def test_slug_kollision_ueber_ordner_wird_erkannt(pages_env):
    import app.wiki as wiki
    from app.access import PageMeta

    assert wiki.slug_exists("budget-finance")
    assert not wiki.slug_exists("gibt-es-nicht")
    assert wiki.slug_exists_elsewhere("budget-finance", PageMeta(domaene="allgemein"))
    assert not wiki.slug_exists_elsewhere("budget-finance", PageMeta(domaene="finance"))
    assert not wiki.slug_exists_elsewhere("neu", PageMeta(domaene="finance"))


def test_new_lehnt_vorhandenen_slug_ab(client):
    import app.wiki as wiki

    # mitarbeiter darf finance nicht sehen - trotzdem wird der Slug abgelehnt (global eindeutig)
    r = client.post("/new", cookies=as_user("mitarbeiter"), data={
        "title": "Budget Finance", "content": "Ueberschreiben?",
        "vertraulichkeit": "intern", "domaene": "allgemein", "empfaenger": "",
    })
    assert r.status_code == 409
    assert "bereits vergeben" in r.text
    assert 'value="Budget Finance"' in r.text  # Eingaben bleiben im Formular
    page = wiki.get_page("budget-finance")
    assert page.meta.domaene == "finance"
    assert FINANCE_TEXT in page.content
    assert not (wiki.pages_dir() / "allgemein" / "budget-finance.md").exists()


def test_ordner_gewinnt_ueber_kopf(pages_env):
    import app.wiki as wiki

    # Kopf sagt allgemein/intern, Datei liegt in finance/vertraulich/
    d = pages_env / "finance" / "vertraulich"
    d.mkdir(parents=True, exist_ok=True)
    (d / "falsch-beschriftet.md").write_text(
        "---\nerstellt_von: cfo\nvertraulichkeit: intern\ndomaene: allgemein\n---\n"
        "# Falsch beschriftet\n\nInhalt\n", encoding="utf-8",
    )
    page = wiki.get_page("falsch-beschriftet")
    assert page.meta.domaene == "finance"
    assert page.meta.vertraulichkeit == "vertraulich"
    # Beim naechsten Speichern wird der Kopf korrigiert
    wiki.save_page(page.slug, page.title, page.content, page.meta)
    raw = (d / "falsch-beschriftet.md").read_text(encoding="utf-8")
    assert "domaene: finance" in raw and "vertraulichkeit: vertraulich" in raw


def test_unbekannter_ordner_wird_ignoriert(pages_env, caplog):
    import app.wiki as wiki

    d = pages_env / "geheimlabor"
    d.mkdir()
    (d / "x.md").write_text("# X\n\nInhalt\n", encoding="utf-8")
    wiki._warned_folders.clear()
    with caplog.at_level("WARNING"):
        slugs = {p.slug for p in wiki.list_pages()}
    assert "x" not in slugs
    assert wiki.get_page("x") is None
    assert "geheimlabor" in caplog.text


def test_migration_flacher_dateien_idempotent(pages_env):
    import app.wiki as wiki

    (pages_env / "alt-ohne-kopf.md").write_text("# Alt ohne Kopf\n\nText A\n", encoding="utf-8")
    (pages_env / "alt-mit-kopf.md").write_text(
        "---\nerstellt_von: cfo\nerstellt_am: '2026-08-01T10:00:00'\n"
        "vertraulichkeit: intern\ndomaene: finance\n---\n# Alt mit Kopf\n\nText B\n",
        encoding="utf-8",
    )
    (pages_env / "alt-vertraulich.md").write_text(
        "---\nerstellt_von: cfo\nvertraulichkeit: vertraulich\ndomaene: hr\n---\n# Alt vertraulich\n\nText C\n",
        encoding="utf-8",
    )
    (pages_env / "alt-domaene-unbekannt.md").write_text(
        "---\nerstellt_von: cfo\ndomaene: gibt-es-nicht\n---\n# Alt Domaene unbekannt\n\nText D\n",
        encoding="utf-8",
    )
    assert wiki.migrate_flat_pages() == 4
    assert not list(pages_env.glob("*.md"))
    assert (pages_env / "allgemein" / "alt-ohne-kopf.md").exists()
    assert (pages_env / "finance" / "alt-mit-kopf.md").exists()
    assert (pages_env / "hr" / "vertraulich" / "alt-vertraulich.md").exists()
    assert (pages_env / "allgemein" / "alt-domaene-unbekannt.md").exists()

    ohne = wiki.get_page("alt-ohne-kopf")
    assert ohne.meta.erstellt_von == "unbekannt"
    assert ohne.meta.domaene == "allgemein"
    assert ohne.meta.vertraulichkeit == "intern"
    assert ohne.content == "Text A"
    # Default-Meta wurde in den Kopf geschrieben
    raw = (pages_env / "allgemein" / "alt-ohne-kopf.md").read_text(encoding="utf-8")
    assert raw.startswith("---\n") and "erstellt_von: unbekannt" in raw

    mit = wiki.get_page("alt-mit-kopf")
    assert mit.meta.erstellt_von == "cfo"
    assert mit.meta.erstellt_am == "2026-08-01T10:00:00"
    assert mit.content == "Text B"

    # idempotent: zweiter Lauf tut nichts
    assert wiki.migrate_flat_pages() == 0
    assert wiki.get_page("alt-mit-kopf").content == "Text B"


def test_migration_slug_kollision_bleibt_liegen(pages_env):
    import app.wiki as wiki

    (pages_env / "budget-finance.md").write_text("# Kopie\n\nAlt\n", encoding="utf-8")
    assert wiki.migrate_flat_pages() == 0
    assert (pages_env / "budget-finance.md").exists()
    assert wiki.get_page("budget-finance").meta.domaene == "finance"


@pytest.mark.security
def test_us18_datei_ohne_kopf_in_finance_bleibt_finance(pages_env):
    """Datei OHNE Kopf direkt nach pages/finance/ geschrieben: Ordner ist die Wahrheit."""
    import app.wiki as wiki

    (pages_env / "finance" / "kopflos.md").write_text(
        "# Kopflos\n\nGeheimzahl Kostenstelle 9999 Sonderbudget.\n", encoding="utf-8"
    )
    q = "Geheimzahl Kostenstelle Sonderbudget"
    assert wiki.search_snippets(q, "mitarbeiter", top_k=50) == []
    assert "kopflos" not in {p.slug for p in wiki.list_pages("mitarbeiter")}
    assert wiki.get_page_for("kopflos", "mitarbeiter") is None

    treffer = wiki.search_snippets(q, "cfo", top_k=50)
    assert any(s.page.slug == "kopflos" for s in treffer)
    assert wiki.get_page_for("kopflos", "cfo").meta.domaene == "finance"


@pytest.mark.security
def test_us18_kopf_allgemein_in_finance_ordner_gewinnt(pages_env):
    """Kopf sagt allgemein, Datei liegt in pages/finance/: Mitarbeiter sieht sie nicht."""
    import app.wiki as wiki

    (pages_env / "finance" / "getarnt.md").write_text(
        "---\nerstellt_von: mitarbeiter\nvertraulichkeit: intern\ndomaene: allgemein\n---\n"
        "# Getarnt\n\nSchmuggelware Quartalszahlen 777.\n", encoding="utf-8",
    )
    q = "Schmuggelware Quartalszahlen"
    assert wiki.search_snippets(q, "mitarbeiter", top_k=50) == []
    assert wiki.get_page_for("getarnt", "mitarbeiter") is None
    assert "getarnt" not in {p.slug for p in wiki.list_pages("mitarbeiter")}
    assert any(s.page.slug == "getarnt" for s in wiki.search_snippets(q, "cfo", top_k=50))


@pytest.mark.security
def test_us18_route_404_fuer_kopflose_finance_datei(client):
    import app.wiki as wiki

    (wiki.pages_dir() / "finance" / "kopflos.md").write_text("# Kopflos\n\nGeheim\n", encoding="utf-8")
    assert client.get("/wiki/kopflos", cookies=as_user("mitarbeiter")).status_code == 404
    assert client.get("/wiki/kopflos", cookies=as_user("cfo")).status_code == 200


@pytest.mark.security
def test_oeffentlich_in_fremdem_ordner_oeffnet_den_ordner_nicht(pages_env):
    """Ordner ist die einzige Wahrheit: Das Label oeffentlich erweitert nie die
    Ordnerrechte (Label verschaerft nur). Frueher galt hier eine Ausnahme - die
    war ein Leck (Security-Review nach Paket 8)."""
    import app.wiki as wiki
    from app.access import PageMeta

    wiki.save_page("finance-faq", "Finance FAQ", "Oeffentliche Infos",
                   PageMeta(erstellt_von="cfo", vertraulichkeit="oeffentlich", domaene="finance"))
    assert "finance-faq" not in {p.slug for p in wiki.list_pages("mitarbeiter")}
    assert "finance-faq" not in {p.slug for p in wiki.list_pages("gast")}
    assert "finance-faq" in {p.slug for p in wiki.list_pages("cfo")}
    # erst recht nicht aus dem vertraulich-Unterordner heraus (Ordner erzwingt vertraulich)
    d = pages_env / "finance" / "vertraulich"
    d.mkdir(exist_ok=True)
    (d / "angeblich-oeffentlich.md").write_text(
        "---\nerstellt_von: cfo\nvertraulichkeit: oeffentlich\ndomaene: finance\n---\n# X\n\nY\n",
        encoding="utf-8",
    )
    assert "angeblich-oeffentlich" not in {p.slug for p in wiki.list_pages("mitarbeiter")}
    assert wiki.get_page("angeblich-oeffentlich").meta.vertraulichkeit == "vertraulich"


def test_stats_total_folders_und_git_history(pages_env):
    import app.stats as stats

    assert stats.get_dashboard_stats("gast").total_folders == 1  # nur die Lobby allgemein
    assert stats.get_dashboard_stats("mitarbeiter").total_folders == 2  # allgemein, projekt
    assert stats.get_dashboard_stats("cfo").total_folders == 6
    # kein git-Repo in tmp -> keine Historie, kein Absturz
    s = stats.get_dashboard_stats("cfo")
    assert all(d.uploaded_at is None for d in s.recent_documents)
