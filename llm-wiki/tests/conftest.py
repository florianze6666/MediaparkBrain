"""Test-Setup: Seiten, Vorschlaege, permissions.yaml und Changelog in tmp_path.

permissions.yaml wird pro Test als Kopie nach tmp gelegt, damit Admin-Tests
(Stufe 2) schreiben koennen, ohne die echte Datei anzufassen.
MPB_SECRET ist ein fester Testwert; Cookies werden ueber `as_user(uid)` erzeugt
(korrekt signiert) - rohe `mpb_user=<uid>`-Werte gelten seit dem Security-Fix als Gast.
Die Env-Variablen werden gesetzt, BEVOR app.main importiert wird, damit der
Seed nicht in llm-wiki/pages/ schreibt. Pfade werden in access/wiki/proposals
als Funktionen aufgeloest, daher reicht das Setzen der Env pro Test.
"""
from __future__ import annotations

import importlib
import os
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PERMISSIONS_FILE = ROOT / "permissions.yaml"
TEST_SECRET = "pytest-secret-nicht-fuer-produktion"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Vor dem ersten Import von app.access setzen, damit Signaturen deterministisch sind.
os.environ.setdefault("MPB_SECRET", TEST_SECRET)


def as_user(uid: str) -> dict[str, str]:
    """Cookie-Dict fuer den TestClient: korrekt signierter Identitaets-Cookie."""
    import app.access as access

    return {access.COOKIE_NAME: access.sign_user(uid)}


FINANCE_TEXT = (
    "Budgetantrag KI-Wissensassistent: Lizenzen 48.000 EUR, externe Entwicklung "
    "95.000 EUR, Gesamt 220.000 EUR, Kostenstelle 4711, Projektnummer P-2026-031."
)
BR_TEXT = (
    "Betriebsratssitzung: Leistungskontrolle nach BetrVG, Loeschfrist 30 Tage, "
    "Betriebsvereinbarung vor Rollout."
)
PUBLIC_TEXT = "Willkommen im Wiki. Diese Seite darf jeder lesen, auch der Gast."
CONFIDENTIAL_TEXT = "Vertrauliche Projektnotiz fuer die PMO-Leitung: Lieferant wechselt."
LEGACY_TEXT = "Altbestand ohne Frontmatter. Diese Notiz stammt aus der Zeit vor Paket 1."


@pytest.fixture
def pages_env(tmp_path, monkeypatch):
    """Setzt MPB_PAGES_DIR / MPB_PERMISSIONS_FILE / MPB_PROPOSALS_DIR /
    MPB_CHANGELOG_FILE und laedt die App-Module frisch."""
    pages = tmp_path / "pages"
    pages.mkdir()
    perms = tmp_path / "permissions.yaml"
    shutil.copy(PERMISSIONS_FILE, perms)
    monkeypatch.setenv("MPB_PAGES_DIR", str(pages))
    monkeypatch.setenv("MPB_PERMISSIONS_FILE", str(perms))
    monkeypatch.setenv("MPB_CHANGELOG_FILE", str(tmp_path / "permissions-changelog.md"))
    monkeypatch.setenv("MPB_PROPOSALS_DIR", str(tmp_path / "project_proposals"))
    monkeypatch.setenv("MPB_SECRET", TEST_SECRET)

    import app.access as access
    import app.wiki as wiki
    import app.proposals as proposals

    importlib.reload(access)
    importlib.reload(wiki)
    importlib.reload(proposals)

    from app.access import PageMeta

    wiki.save_page(
        "budget-finance",
        "Budget Finance",
        FINANCE_TEXT,
        PageMeta(erstellt_von="cfo", erstellt_am="2026-09-01T10:00:00",
                 vertraulichkeit="intern", domaene="finance"),
    )
    wiki.save_page(
        "br-protokoll",
        "BR Protokoll",
        BR_TEXT,
        PageMeta(erstellt_von="betriebsrat", erstellt_am="2026-09-02T10:00:00",
                 vertraulichkeit="intern", domaene="br"),
    )
    wiki.save_page(
        "oeffentlich",
        "Oeffentliche Testseite",
        PUBLIC_TEXT,
        PageMeta(erstellt_von="system", erstellt_am="2026-09-03T10:00:00",
                 vertraulichkeit="oeffentlich", domaene="allgemein"),
    )
    wiki.save_page(
        "vertraulich-projekt",
        "Vertrauliche Projektnotiz",
        CONFIDENTIAL_TEXT,
        PageMeta(erstellt_von="projektmanager", erstellt_am="2026-09-04T10:00:00",
                 vertraulichkeit="vertraulich", domaene="projekt",
                 empfaenger=["pmo-leitung"]),
    )
    # Altbestand: kein Frontmatter, liegt bereits im Domaenenordner allgemein/
    (pages / "allgemein" / "altbestand.md").write_text(
        f"# Altbestand\n\n{LEGACY_TEXT}\n", encoding="utf-8"
    )
    return pages


@pytest.fixture
def client(pages_env, monkeypatch):
    """FastAPI TestClient mit frisch importiertem app.main (Seed landet in tmp)."""
    from fastapi.testclient import TestClient

    import app.main as main

    importlib.reload(main)
    return TestClient(main.app, follow_redirects=False)
