"""Regeln 1-5 der Entscheidungsfunktion, einzeln."""
from __future__ import annotations

import pytest


@pytest.fixture
def access(pages_env):
    import app.access as access
    return access


def meta(access, **kw):
    return access.PageMeta(**kw)


def test_regel1_oeffentlich_allow_auch_fuer_gast(access):
    m = meta(access, vertraulichkeit="oeffentlich", domaene="finance")
    assert access.decide("gast", m) == "ALLOW"
    assert access.decide("mitarbeiter", m) == "ALLOW"
    assert access.decide("unbekannte-id", m) == "ALLOW"


def test_regel2_gast_deny_bei_intern(access):
    m = meta(access, vertraulichkeit="intern", domaene="allgemein")
    assert access.decide("gast", m) == "DENY"
    # unbekannte Nutzer-ID wird zum Gast
    assert access.decide("nicht-vorhanden", m) == "DENY"
    assert access.decide(None, m) == "DENY"


def test_regel3_keine_lesegruppe_deny(access):
    finance = meta(access, vertraulichkeit="intern", domaene="finance")
    assert access.decide("mitarbeiter", finance) == "DENY"
    assert access.decide("projektmanager", finance) == "DENY"
    assert access.decide("orchestrator", finance) == "DENY"
    assert access.decide("cfo", finance) == "ALLOW"
    assert access.decide("pmo-leitung", finance) == "ALLOW"  # ueber leitung

    br = meta(access, vertraulichkeit="intern", domaene="br")
    assert access.decide("ceo", br) == "DENY"  # Leitung liest BR nicht
    assert access.decide("cfo", br) == "DENY"
    assert access.decide("betriebsrat", br) == "ALLOW"

    gf = meta(access, vertraulichkeit="intern", domaene="gf")
    assert access.decide("ceo", gf) == "ALLOW"
    assert access.decide("cfo", gf) == "DENY"


def test_regel3_unbekannte_domaene_deny(access):
    m = meta(access, vertraulichkeit="intern", domaene="gibt-es-nicht")
    for uid in ("mitarbeiter", "cfo", "ceo", "betriebsrat"):
        assert access.decide(uid, m) == "DENY"


def test_regel4_vertraulich_ersteller_sieht_eigene_seite(access):
    m = meta(access, vertraulichkeit="vertraulich", domaene="projekt",
             erstellt_von="projektmanager", empfaenger=[])
    assert access.decide("projektmanager", m) == "ALLOW"
    assert access.decide("mitarbeiter", m) == "DENY"
    assert access.decide("pmo-leitung", m) == "DENY"


def test_regel4_vertraulich_empfaenger_als_id(access):
    m = meta(access, vertraulichkeit="vertraulich", domaene="projekt",
             erstellt_von="projektmanager", empfaenger=["pmo-leitung"])
    assert access.decide("pmo-leitung", m) == "ALLOW"
    assert access.decide("mitarbeiter", m) == "DENY"


def test_regel4_vertraulich_empfaenger_als_gruppe(access):
    m = meta(access, vertraulichkeit="vertraulich", domaene="finance",
             erstellt_von="cfo", empfaenger=["leitung"])
    assert access.decide("ceo", m) == "ALLOW"        # Gruppe leitung + Domaene finance
    assert access.decide("hr-leitung", m) == "ALLOW"
    assert access.decide("mitarbeiter", m) == "DENY"  # scheitert schon an Regel 3


def test_regel4_vertraulich_verschaerft_nur(access):
    # Empfaenger ohne Leserecht auf die Domaene bleibt DENY (Regel 3 vor 4)
    m = meta(access, vertraulichkeit="vertraulich", domaene="br",
             erstellt_von="betriebsrat", empfaenger=["ceo"])
    assert access.decide("ceo", m) == "DENY"
    # Ersteller ohne Leserecht auf die Domaene bleibt ebenfalls DENY
    m2 = meta(access, vertraulichkeit="vertraulich", domaene="finance",
              erstellt_von="mitarbeiter", empfaenger=[])
    assert access.decide("mitarbeiter", m2) == "DENY"


def test_regel5_sonst_allow(access):
    m = meta(access, vertraulichkeit="intern", domaene="projekt")
    assert access.decide("mitarbeiter", m) == "ALLOW"
    assert access.decide("betriebsrat", m) == "ALLOW"
    assert access.decide("ceo", m) == "ALLOW"


def test_matrix_intern_aus_dokument(access):
    users = ["gast", "mitarbeiter", "projektmanager", "pmo-leitung", "betriebsrat",
             "cfo", "it-security", "ceo", "hr-leitung", "orchestrator"]
    domains = ["allgemein", "projekt", "finance", "einkauf", "hr", "it", "br", "gf", "mail"]
    expected = {
        "gast":           "---------",
        "mitarbeiter":    "xx-------",
        "projektmanager": "xx-------",
        "pmo-leitung":    "xxxxxx---",
        "betriebsrat":    "xx----x--",
        "cfo":            "xxxxxx---",
        "it-security":    "xxxxxx---",
        "ceo":            "xxxxxx-xx",
        "hr-leitung":     "xxxxxx---",
        "orchestrator":   "xx-------",
    }
    for uid in users:
        row = "".join(
            "x" if access.decide(uid, meta(access, vertraulichkeit="intern", domaene=d)) == "ALLOW" else "-"
            for d in domains
        )
        assert row == expected[uid], f"{uid}: {row} != {expected[uid]}"


def test_get_user_unbekannt_ist_gast(access):
    assert access.get_user("xyz")["id"] == "gast"
    assert access.user_groups("xyz") == []
    assert access.user_groups("cfo") == ["alle", "finance", "einkauf", "leitung"]
    assert [u["id"] for u in access.list_users()][0] == "gast"
