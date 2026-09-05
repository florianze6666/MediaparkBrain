"""Test-Setup: Seiten in tmp_path, echte permissions.yaml.

Die Env-Variablen werden gesetzt, BEVOR app.main importiert wird, damit der
Seed nicht in llm-wiki/pages/ schreibt. Pfade werden in access/wiki als
Funktionen aufgeloest, daher reicht das Setzen der Env pro Test.
"""
from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PERMISSIONS_FILE = ROOT / "permissions.yaml"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


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
    """Setzt MPB_PAGES_DIR / MPB_PERMISSIONS_FILE und laedt die App-Module frisch."""
    pages = tmp_path / "pages"
    pages.mkdir()
    monkeypatch.setenv("MPB_PAGES_DIR", str(pages))
    monkeypatch.setenv("MPB_PERMISSIONS_FILE", str(PERMISSIONS_FILE))

    import app.access as access
    import app.wiki as wiki

    importlib.reload(access)
    importlib.reload(wiki)

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
    # Altbestand: kein Frontmatter
    (pages / "altbestand.md").write_text(
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
