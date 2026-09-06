"""Phase 0 (Feature-Branch-Plan, Abschnitt 6): Datenzugriff entschaerft.

0.1  stats: EIN git log ueber das Seitenverzeichnis statt eines Subprozesses je
     Seite, Historie nach Pfad gruppiert, Rueckgriff auf den flachen Altpfad,
     Cache am aktuellen Commit.
0.2  access: stat() auf permissions.yaml hoechstens alle _STAT_INTERVAL Sekunden,
     readable_domains einmal je Rechtestand und Nutzer, ohne Verhaltensaenderung.
"""
from __future__ import annotations

import subprocess
import time
from pathlib import Path

import pytest

from app.access import PageMeta

GIT = ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
       "-c", "commit.gpgsign=false"]


def _git(cwd: Path, *args: str) -> None:
    subprocess.run([*GIT, *args], cwd=cwd, check=True, capture_output=True, text=True)


@pytest.fixture
def repo_pages(pages_env, monkeypatch):
    """pages_env als eigenes Git-Repo; MPB_PAGES_DIR zeigt auf <repo>/pages."""
    import app.stats as stats

    repo = pages_env.parent
    _git(repo, "init", "-q")
    stats.clear_history_cache()
    return repo


# ---------------------------------------------------------------------------
# 0.1 gebuendelte Git-Historie
# ---------------------------------------------------------------------------


def test_git_historie_aus_einem_aufruf(repo_pages, pages_env, monkeypatch):
    import app.stats as stats
    import app.wiki as wiki

    calls: list[list[str]] = []
    real_run = subprocess.run

    def spy(cmd, *a, **kw):
        if cmd and cmd[0] == "git" and "log" in cmd:
            calls.append(list(cmd))
        return real_run(cmd, *a, **kw)

    monkeypatch.setattr(stats.subprocess, "run", spy)

    # Feste Autorendaten: %aI hat Sekundenaufloesung, zwei Commits in derselben
    # Sekunde waeren sonst nicht zu ordnen.
    _git(repo_pages, "add", "-A")
    _git(repo_pages, "commit", "-q", "-m", "erste Fassung",
         "--date=2026-09-01T10:00:00+02:00")
    # zweiter Commit nur fuer eine Seite -> is_update dort, sonst nicht
    wiki.save_page("budget-finance", "Budget Finance", "geaendert",
                   PageMeta(erstellt_von="cfo", vertraulichkeit="intern", domaene="finance"))
    _git(repo_pages, "add", "-A")
    _git(repo_pages, "commit", "-q", "-m", "zweite Fassung",
         "--date=2026-09-02T10:00:00+02:00")
    # unversionierte Seite
    wiki.save_page("frisch", "Frisch", "noch nicht committet",
                   PageMeta(erstellt_von="cfo", vertraulichkeit="intern", domaene="finance"))

    s = stats.get_dashboard_stats("cfo")
    assert len(calls) == 1, "genau ein git log fuer alle Seiten"
    assert "--follow" not in calls[0]

    by_slug = {d.slug: d for d in s.recent_documents}
    assert by_slug["budget-finance"].uploaded_by == "Test"
    assert by_slug["budget-finance"].is_update is True
    assert by_slug["oeffentlich"].is_update is False
    assert by_slug["oeffentlich"].uploaded_at is not None
    assert by_slug["frisch"].uploaded_at is None
    assert by_slug["frisch"].uploaded_by == "Unbekannt (noch nicht committet)"
    # neuestes zuerst: die frische Seite (None) sortiert ans Ende
    assert s.recent_documents[0].slug == "budget-finance"
    assert s.recent_documents[-1].slug == "frisch"


def test_verschobene_seite_behaelt_flache_historie(repo_pages, pages_env):
    """Stufe 2: flache Altdatei `<slug>.md` -> `allgemein/<slug>.md`. Die Historie
    des Altpfads gehoert weiter zur Seite, auch ohne --follow."""
    import app.stats as stats

    flat = pages_env / "altseite.md"
    flat.write_text("# Altseite\n\nvor der Migration\n", encoding="utf-8")
    _git(repo_pages, "add", "-A")
    _git(repo_pages, "commit", "-q", "-m", "flach", "--date=2026-09-01T10:00:00+02:00")
    (pages_env / "allgemein").mkdir(exist_ok=True)
    flat.rename(pages_env / "allgemein" / "altseite.md")
    _git(repo_pages, "add", "-A")
    _git(repo_pages, "commit", "-q", "-m", "verschoben", "--date=2026-09-02T10:00:00+02:00")

    s = stats.get_dashboard_stats("mitarbeiter")
    alt = next(d for d in s.recent_documents if d.slug == "altseite")
    assert alt.is_update is True, "flacher Commit + Verschiebe-Commit = zwei Commits"
    assert alt.uploaded_by == "Test"
    assert alt.uploaded_at.isoformat() == "2026-09-02T10:00:00+02:00", "neuester Commit gewinnt"


def test_historie_cache_haengt_am_commit(repo_pages, pages_env, monkeypatch):
    import app.stats as stats

    calls = 0
    real = stats._git_history_all

    def counting(root):
        nonlocal calls
        calls += 1
        return real(root)

    monkeypatch.setattr(stats, "_git_history_all", counting)

    _git(repo_pages, "add", "-A")
    _git(repo_pages, "commit", "-q", "-m", "eins")
    stats.get_dashboard_stats("cfo")
    stats.get_dashboard_stats("cfo")
    stats.get_dashboard_stats("mitarbeiter")
    assert calls == 1, "gleicher HEAD, kein zweiter git-Aufruf"

    (pages_env / "allgemein" / "neu.md").write_text("# Neu\n\nx\n", encoding="utf-8")
    _git(repo_pages, "add", "-A")
    _git(repo_pages, "commit", "-q", "-m", "zwei")
    s = stats.get_dashboard_stats("cfo")
    assert calls == 2, "neuer HEAD, Historie neu gelesen"
    assert next(d for d in s.recent_documents if d.slug == "neu").uploaded_at is not None


def test_ohne_repo_keine_historie_kein_absturz(pages_env):
    import app.stats as stats

    stats.clear_history_cache()
    s = stats.get_dashboard_stats("cfo")
    assert s.total_files > 0
    assert all(d.uploaded_at is None for d in s.recent_documents)


# ---------------------------------------------------------------------------
# 0.2 Rechtefilter
# ---------------------------------------------------------------------------


def test_readable_domains_cache_liefert_kopien_und_trennt_nutzer(pages_env):
    import app.access as access

    cfo = access.readable_domains("cfo")
    cfo.append("br")  # der Aufrufer darf den Cache nicht veraendern
    assert "br" not in access.readable_domains("cfo")
    assert access.readable_domains("mitarbeiter") == ["allgemein", "projekt"]
    assert access.readable_domains("gast") == ["allgemein"]
    assert "finance" in access.readable_domains("cfo")
    assert "finance" not in access.readable_domains("mitarbeiter")


def test_rechteaenderung_ueber_save_wirkt_sofort(pages_env):
    import app.access as access

    assert "finance" not in access.readable_domains("mitarbeiter")
    data = access.load_permissions()
    data["nutzer"]["mitarbeiter"]["gruppen"] = ["alle", "finance"]
    access.save_permissions(data, changed_by="admin", change_note="Test")
    assert "finance" in access.readable_domains("mitarbeiter")
    assert access.can_read(
        "mitarbeiter",
        PageMeta(erstellt_von="cfo", vertraulichkeit="intern", domaene="finance"),
    )


def test_externe_aenderung_wird_nach_dem_intervall_erkannt(pages_env, monkeypatch):
    import app.access as access

    path = access.permissions_path()
    assert "finance" not in access.readable_domains("mitarbeiter")
    text = path.read_text(encoding="utf-8").replace(
        "mitarbeiter:     {name: \"Mitarbeiter\", gruppen: [alle]}",
        "mitarbeiter:     {name: \"Mitarbeiter\", gruppen: [alle, finance]}",
    )
    assert text != path.read_text(encoding="utf-8"), "Testvorlage hat sich geaendert"
    time.sleep(0.02)
    path.write_text(text, encoding="utf-8")
    # innerhalb des Intervalls darf der alte Stand noch gelten ...
    monkeypatch.setattr(access, "_STAT_INTERVAL", 60.0)
    assert "finance" not in access.readable_domains("mitarbeiter")
    # ... nach Ablauf wird die Datei neu gelesen, ohne clear_cache
    monkeypatch.setattr(access, "_STAT_INTERVAL", 0.0)
    assert "finance" in access.readable_domains("mitarbeiter")


def test_anderer_pfad_laedt_sofort(pages_env, tmp_path, monkeypatch):
    """Testisolation: ein neuer MPB_PERMISSIONS_FILE gilt ohne Wartezeit."""
    import app.access as access

    assert "finance" not in access.readable_domains("mitarbeiter")
    other = tmp_path / "andere.yaml"
    other.write_text(
        "gruppen: [alle, finance]\n"
        "nutzer:\n  mitarbeiter: {name: M, gruppen: [alle, finance]}\n"
        "domaenen:\n  allgemein: {lesen: [alle]}\n  finance: {lesen: [finance]}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(access, "_STAT_INTERVAL", 60.0)
    monkeypatch.setenv("MPB_PERMISSIONS_FILE", str(other))
    assert access.readable_domains("mitarbeiter") == ["allgemein", "finance"]
