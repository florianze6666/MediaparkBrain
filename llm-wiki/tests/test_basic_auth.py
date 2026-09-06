"""Passwortschutz vor der App (app/basic_auth.py).

Der Rollen-Login (/login) fragt bewusst kein Passwort ab. Fuer den Betrieb
auf einer oeffentlich erreichbaren Adresse liegt deshalb ein Basic-Auth
davor, das ueber MPB_BASIC_AUTH_USER/-PASS aktiviert wird. Ohne die beiden
Variablen bleibt die App unveraendert erreichbar (lokale Entwicklung).
"""
from __future__ import annotations

import base64
import importlib

import pytest

pytestmark = pytest.mark.security

USER = "demo"
PASSWORD = "geheim-nur-fuer-tests"


def _auth_header(user: str, password: str) -> dict[str, str]:
    token = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("ascii")
    return {"Authorization": f"Basic {token}"}


@pytest.fixture
def guarded_client(pages_env, monkeypatch):
    """TestClient mit aktivem Basic-Auth."""
    from fastapi.testclient import TestClient

    monkeypatch.setenv("MPB_BASIC_AUTH_USER", USER)
    monkeypatch.setenv("MPB_BASIC_AUTH_PASS", PASSWORD)

    import app.basic_auth as basic_auth
    import app.main as main

    importlib.reload(basic_auth)
    importlib.reload(main)
    return TestClient(main.app, follow_redirects=False)


def test_ohne_header_401_mit_challenge(guarded_client):
    resp = guarded_client.get("/")
    assert resp.status_code == 401
    assert resp.headers["www-authenticate"].startswith("Basic realm=")


def test_richtige_zugangsdaten_kommen_durch(guarded_client):
    resp = guarded_client.get("/", headers=_auth_header(USER, PASSWORD))
    assert resp.status_code == 200


@pytest.mark.parametrize("user,password", [
    (USER, "falsch"),
    ("fremder", PASSWORD),
    ("", ""),
])
def test_falsche_zugangsdaten_bleiben_draussen(guarded_client, user, password):
    resp = guarded_client.get("/", headers=_auth_header(user, password))
    assert resp.status_code == 401


@pytest.mark.parametrize("header", [
    "Basic kein-base64!!",
    "Basic " + base64.b64encode(b"ohne-doppelpunkt").decode("ascii"),
    "Bearer " + base64.b64encode(f"{USER}:{PASSWORD}".encode()).decode("ascii"),
    "Basic",
])
def test_kaputte_header_werden_abgewiesen(guarded_client, header):
    resp = guarded_client.get("/", headers={"Authorization": header})
    assert resp.status_code == 401


def test_schutz_gilt_auch_fuer_static_und_post(guarded_client):
    assert guarded_client.get("/static/style.css").status_code == 401
    # Ohne Schutz wuerde /login einen Identitaets-Cookie ausstellen.
    resp = guarded_client.post("/login", data={"user": "admin", "next": "/"})
    assert resp.status_code == 401
    assert "set-cookie" not in resp.headers


def test_ohne_env_kein_schutz(client, monkeypatch):
    """Standardfall lokal: keine Variablen gesetzt, App wie bisher erreichbar."""
    monkeypatch.delenv("MPB_BASIC_AUTH_USER", raising=False)
    monkeypatch.delenv("MPB_BASIC_AUTH_PASS", raising=False)
    assert client.get("/").status_code == 200


def test_cookie_secure_folgt_env(pages_env, monkeypatch):
    """Hinter TLS bekommt der Identitaets-Cookie das Secure-Flag, lokal nicht."""
    from fastapi.testclient import TestClient

    def cookie_header(value: str | None, pfad: str, daten: dict) -> str:
        # Leerer String statt delenv: app.main ruft beim Reload load_dotenv()
        # auf und wuerde eine geloeschte Variable aus der echten llm-wiki/.env
        # nachfuellen - dort steht produktiv MPB_COOKIE_SECURE=1. Leer heisst
        # laut access.cookie_secure() ohnehin "aus".
        monkeypatch.setenv("MPB_COOKIE_SECURE", value or "")
        import app.access as access
        import app.main as main

        importlib.reload(access)
        importlib.reload(main)
        client = TestClient(main.app, follow_redirects=False)
        resp = client.post(pfad, data=daten)
        assert resp.status_code == 303
        return resp.headers["set-cookie"]

    # /login und /switch-user setzen denselben Identitaets-Cookie. Ginge das
    # Flag nur an einer der beiden Stellen, wuerde ein Rollenwechsel den
    # Schutz still wieder abraeumen.
    for pfad, daten in [("/login", {"user": "cfo", "next": "/"}),
                        ("/switch-user", {"user": "cfo"})]:
        assert "Secure" in cookie_header("1", pfad, daten), pfad
        assert "Secure" not in cookie_header(None, pfad, daten), pfad
