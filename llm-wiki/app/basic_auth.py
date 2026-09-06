from __future__ import annotations

import base64
import binascii
import hmac
import logging
import os

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

log = logging.getLogger(__name__)

_REALM = "MediaparkBrain"


def _credentials() -> tuple[str, str] | None:
    """Zugangsdaten aus MPB_BASIC_AUTH_USER / MPB_BASIC_AUTH_PASS.

    Fehlt eines von beiden, ist der Schutz aus - dann laeuft die App wie
    bisher (lokale Entwicklung, Tests). Der Schutz liegt VOR dem
    Rollen-Login aus access.py und ersetzt ihn nicht: er entscheidet nur,
    wer die App ueberhaupt erreicht, nicht wer welche Domaene liest.
    """
    user = os.environ.get("MPB_BASIC_AUTH_USER", "").strip()
    password = os.environ.get("MPB_BASIC_AUTH_PASS", "")
    if not user or not password:
        return None
    return user, password


def _unauthorized() -> Response:
    return Response(
        "401 Unauthorized",
        status_code=401,
        headers={"WWW-Authenticate": f'Basic realm="{_REALM}", charset="UTF-8"'},
    )


def _header_matches(header: str, user: str, password: str) -> bool:
    """Prueft einen Authorization-Header gegen die erwarteten Zugangsdaten.
    Vergleich in konstanter Zeit, damit der Header nicht Zeichen fuer
    Zeichen erraten werden kann."""
    scheme, _, encoded = header.partition(" ")
    if scheme.lower() != "basic" or not encoded:
        return False
    try:
        decoded = base64.b64decode(encoded, validate=True).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError):
        return False
    got_user, sep, got_password = decoded.partition(":")
    if not sep:
        return False
    # Beide Vergleiche laufen immer, damit die Dauer nicht verraet, welcher
    # Teil falsch war.
    user_ok = hmac.compare_digest(got_user, user)
    password_ok = hmac.compare_digest(got_password, password)
    return user_ok and password_ok


class BasicAuthMiddleware(BaseHTTPMiddleware):
    """Passwortschutz vor der gesamten App, inklusive /static.

    Gedacht fuer den Betrieb auf einer oeffentlich erreichbaren Adresse:
    der Rollen-Login (/login) fragt bewusst kein Passwort ab, taugt also
    allein nicht als Zugangsschutz.
    """

    async def dispatch(self, request, call_next):
        creds = _credentials()
        if creds is None:
            return await call_next(request)
        header = request.headers.get("authorization", "")
        if not _header_matches(header, *creds):
            return _unauthorized()
        return await call_next(request)
