"""Regressionstests zur Ordnerablage nach Domaene (Review zu PR #28).

Jeder Test hier haelt genau einen der vier Befunde fest. Die Suite lief vor
den Korrekturen vollstaendig gruen - deshalb diese Ergaenzung.
"""
from __future__ import annotations

import pytest

from app import wiki
from app.access import PageMeta


# ---------------------------------------------------------------------------
# Befund 1: domaene ist Verzeichnisname und kam ungeprueft aus dem Formular
# ---------------------------------------------------------------------------


@pytest.mark.security
def test_domaene_kann_nicht_aus_dem_seitenverzeichnis_herausfuehren(pages_env):
    """"../../ausserhalb" darf keine Datei neben dem Seitenverzeichnis anlegen."""
    wiki.save_page("exploit", "Exploit", "Inhalt", PageMeta(domaene="../../ausserhalb"))

    ziel = (wiki.pages_dir() / "allgemein" / "exploit.md").resolve()
    assert ziel.exists(), "Seite muss in der Standarddomaene landen"
    assert not (pages_env.parent.parent / "ausserhalb").exists()
    # Nichts liegt ausserhalb des Seitenverzeichnisses
    for f in ziel.parent.parent.rglob("*.md"):
        assert wiki.pages_dir().resolve() in f.resolve().parents


@pytest.mark.security
def test_unbekannte_domaene_faellt_auf_allgemein_zurueck(pages_env):
    wiki.save_page("frei", "Frei", "Inhalt", PageMeta(domaene="gibtsnicht"))
    assert wiki.get_page("frei").meta.domaene == "allgemein"


def test_bekannte_domaene_bleibt_erhalten(pages_env):
    wiki.save_page("zahlen", "Zahlen", "Inhalt", PageMeta(domaene="finance"))
    assert (wiki.pages_dir() / "finance" / "zahlen.md").exists()
    assert wiki.get_page("zahlen").meta.domaene == "finance"


def test_lesen_normalisiert_die_domaene_nicht(pages_env):
    """`decide` wertet eine unbekannte Domaene als DENY - das muss so bleiben.

    Wuerde beim Lesen still auf "allgemein" normalisiert, waere aus einer
    Sperre eine Freigabe geworden.
    """
    from app.access import decide, DENY

    (wiki.pages_dir() / "handverlesen.md").write_text(
        "---\nerstellt_von: cfo\nvertraulichkeit: intern\ndomaene: gibtsnicht\n---\n"
        "# Handverlesen\n\nInhalt.\n",
        encoding="utf-8",
    )
    page = wiki.get_page("handverlesen")
    assert page.meta.domaene == "gibtsnicht"
    assert decide("cfo", page.meta) == DENY


# ---------------------------------------------------------------------------
# Befund 2: der Slug wurde als Glob-Muster an rglob weitergereicht
# ---------------------------------------------------------------------------


@pytest.mark.security
@pytest.mark.parametrize("muster", ["*", "alph?", "[ab]*", "**", "budget-*"])
def test_glob_metazeichen_treffen_keine_fremde_seite(pages_env, muster):
    wiki.save_page("alpha", "Alpha", "Inhalt A", PageMeta(domaene="allgemein"))
    assert wiki.get_page(muster) is None


@pytest.mark.security
def test_loeschen_mit_muster_loescht_nichts(pages_env):
    wiki.save_page("alpha", "Alpha", "Inhalt A", PageMeta(domaene="allgemein"))
    vorher = sorted(p.name for p in wiki.pages_dir().rglob("*.md"))

    wiki.delete_page("*")

    assert sorted(p.name for p in wiki.pages_dir().rglob("*.md")) == vorher


def test_gueltiger_slug_wird_weiterhin_gefunden(pages_env):
    wiki.save_page("alpha", "Alpha", "Inhalt A", PageMeta(domaene="finance"))
    seite = wiki.get_page("alpha")
    assert seite is not None and seite.title == "Alpha"


# ---------------------------------------------------------------------------
# Befund 3: Migration ueberschrieb die neuere Datei und liess die Dublette
# ---------------------------------------------------------------------------


FRONTMATTER = "---\nerstellt_von: anselm\nvertraulichkeit: intern\ndomaene: allgemein\nquelle: wiki\n---\n"


def _flache_seite(pages_env, slug: str, text: str) -> None:
    (pages_env / f"{slug}.md").write_text(
        f"{FRONTMATTER}# {slug.title()}\n\n{text}\n", encoding="utf-8"
    )


def test_migration_verschiebt_alte_flache_seite(pages_env):
    _flache_seite(pages_env, "notiz", "Alter Inhalt.")

    wiki.migrate_flat_pages()

    assert not (pages_env / "notiz.md").exists()
    assert (pages_env / "allgemein" / "notiz.md").exists()
    assert "Alter Inhalt." in wiki.get_page("notiz").content


def test_migration_ueberschreibt_die_einsortierte_fassung_nicht(pages_env):
    (pages_env / "allgemein").mkdir(exist_ok=True)
    (pages_env / "allgemein" / "notiz.md").write_text(
        f"{FRONTMATTER}# Notiz\n\nNeue Fassung im Domaenenordner.\n", encoding="utf-8"
    )
    _flache_seite(pages_env, "notiz", "ALTE flache Fassung.")

    wiki.migrate_flat_pages()

    assert "Neue Fassung im Domaenenordner." in wiki.get_page("notiz").content
    # Der alte Inhalt geht nicht verloren, taucht aber nicht als zweite Seite auf
    assert (pages_env / "notiz.md.alt").exists()
    assert not (pages_env / "notiz.md").exists()


def test_migration_erzeugt_keine_doppelten_slugs(pages_env):
    (pages_env / "allgemein").mkdir(exist_ok=True)
    (pages_env / "allgemein" / "notiz.md").write_text(
        f"{FRONTMATTER}# Notiz\n\nNeue Fassung.\n", encoding="utf-8"
    )
    _flache_seite(pages_env, "notiz", "Alte Fassung.")

    wiki.migrate_flat_pages()

    slugs = [p.slug for p in wiki.list_pages()]
    assert slugs.count("notiz") == 1


def test_migration_ist_idempotent(pages_env):
    _flache_seite(pages_env, "notiz", "Inhalt.")

    wiki.migrate_flat_pages()
    erster = sorted(str(p.relative_to(pages_env)) for p in pages_env.rglob("*.md"))
    wiki.migrate_flat_pages()
    zweiter = sorted(str(p.relative_to(pages_env)) for p in pages_env.rglob("*.md"))

    assert erster == zweiter


# ---------------------------------------------------------------------------
# Befund 4: ablageort blieb nach einem Domaenenwechsel auf dem alten Ordner
# ---------------------------------------------------------------------------


def test_ablageort_folgt_dem_domaenenwechsel(pages_env):
    wiki.save_page("budget", "Budget", "Zahlen.", PageMeta(domaene="allgemein"))
    meta = wiki.get_page("budget").meta
    assert meta.ablageort == "allgemein/budget.md"

    meta.domaene = "finance"
    wiki.save_page("budget", "Budget", "Zahlen.", meta)

    seite = wiki.get_page("budget")
    assert seite.meta.ablageort == "finance/budget.md"
    assert seite.meta.ablageort == str(
        seite.path.relative_to(wiki.pages_dir())
    ).replace("\\", "/")
    assert not (pages_env / "allgemein" / "budget.md").exists()


def test_selbst_gesetzter_ablageort_bleibt_erhalten(pages_env):
    """Ein echter Quellsystem-Pfad (Paket 2/7) darf nicht ueberschrieben werden."""
    meta = PageMeta(domaene="hr", ablageort="sharepoint_hr/2024/betriebsvereinbarung.pdf")
    wiki.save_page("bv", "Betriebsvereinbarung", "Inhalt.", meta)

    assert wiki.get_page("bv").meta.ablageort == "sharepoint_hr/2024/betriebsvereinbarung.pdf"
