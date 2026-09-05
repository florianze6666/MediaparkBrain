"""Berechtigungen und Herkunft (Paket 1).

Ein Zugriffsweg: jede Sichtbarkeitsentscheidung laeuft ueber `decide`.
Nutzer, Gruppen und Domaenen sind Daten in permissions.yaml, kein Code.
Vertrag: docs/berechtigungen-und-herkunft.md
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

import yaml
from fastapi import Request

GUEST = "gast"
UNKNOWN_CREATOR = "unbekannt"
COOKIE_NAME = "mpb_user"

VERTRAULICHKEITEN = ("oeffentlich", "intern", "vertraulich", "C-Level", "Betriebsrat-intern")

ALLOW = "ALLOW"
DENY = "DENY"


# ---------------------------------------------------------------------------
# Metadaten einer Seite (YAML-Frontmatter)
# ---------------------------------------------------------------------------


@dataclass
class PageMeta:
    erstellt_von: str = UNKNOWN_CREATOR
    erstellt_am: str = ""
    geaendert_von: str = ""
    geaendert_am: str = ""
    vertraulichkeit: str = "intern"
    domaene: str = "allgemein"
    empfaenger: list[str] = field(default_factory=list)
    ablageort: str = ""
    quelle: str = "wiki"
    doc_id: str = ""
    titel: str = ""
    dokumenttyp: str = ""
    datum: str = ""
    verfasser: str = ""
    rolle: str = ""
    organisationseinheit: str = ""
    projekt: str = ""
    geschaeftsbereich: str = ""
    informationsdomaene: list[str] = field(default_factory=list)
    original_datei: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "PageMeta":
        data = data or {}
        meta = cls()
        for key in meta.__dataclass_fields__:
            if key not in data or data[key] is None:
                continue
            value = data[key]
            if key in ("empfaenger", "informationsdomaene"):
                if isinstance(value, str):
                    value = [v.strip() for v in value.split(",") if v.strip()]
                else:
                    value = [str(v).strip() for v in value if str(v).strip()]
            else:
                value = str(value)
            setattr(meta, key, value)
        if meta.vertraulichkeit not in VERTRAULICHKEITEN:
            meta.vertraulichkeit = "intern"
        if not meta.erstellt_von:
            meta.erstellt_von = UNKNOWN_CREATOR
        return meta

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)



# ---------------------------------------------------------------------------
# Rechte-Datei laden
# ---------------------------------------------------------------------------


def permissions_path() -> Path:
    env = os.environ.get("MPB_PERMISSIONS_FILE")
    if env:
        return Path(env)
    return Path(__file__).resolve().parent.parent / "permissions.yaml"


_cache: dict[str, Any] = {"key": None, "data": None}


def load_permissions() -> dict[str, Any]:
    """Laedt permissions.yaml; wird bei Aenderung der Datei neu eingelesen."""
    path = permissions_path()
    try:
        key = (str(path), path.stat().st_mtime_ns)
    except FileNotFoundError:
        key = (str(path), None)
    if _cache["key"] == key and _cache["data"] is not None:
        return _cache["data"]
    if key[1] is None:
        data = {"gruppen": [], "nutzer": {}, "domaenen": {}}
    else:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    data.setdefault("gruppen", [])
    data.setdefault("nutzer", {})
    data.setdefault("domaenen", {})
    _cache["key"] = key
    _cache["data"] = data
    return data


def list_users() -> list[dict[str, Any]]:
    """Alle Nutzer als Liste von {id, name, gruppen} in Dateireihenfolge."""
    users = load_permissions()["nutzer"]
    return [
        {"id": uid, "name": u.get("name", uid), "gruppen": list(u.get("gruppen") or [])}
        for uid, u in users.items()
    ]


def list_domains() -> list[str]:
    return list(load_permissions()["domaenen"].keys())


def list_confidentiality_levels() -> list[dict[str, Any]]:
    stufen = load_permissions().get("vertraulichkeitsstufen") or {}
    if not stufen:
        return [
            {"id": "intern", "name": "Intern (Standard)"},
            {"id": "C-Level", "name": "C-Level"},
            {"id": "Betriebsrat-intern", "name": "Betriebsrat-intern"},
            {"id": "oeffentlich", "name": "Öffentlich"},
        ]
    return [
        {"id": k, "name": v.get("name", k), "beschreibung": v.get("beschreibung", "")}
        for k, v in stufen.items()
    ]


def default_confidentiality_for_user(user_id: str | None) -> str:
    user = get_user(user_id)
    uid = user["id"]
    stufen = load_permissions().get("vertraulichkeitsstufen") or {}
    for k, v in stufen.items():
        if uid in v.get("standard_fuer_rollen", []):
            return k
    if uid in ("ceo", "cfo"):
        return "C-Level"
    if uid == "betriebsrat":
        return "Betriebsrat-intern"
    return "intern"


def get_user(user_id: str | None) -> dict[str, Any]:
    """Nutzer nach ID; unbekannte IDs (und None) werden zum Gast."""
    users = load_permissions()["nutzer"]
    uid = user_id if user_id in users else GUEST
    u = users.get(uid, {"name": "Gast (nicht angemeldet)", "gruppen": []})
    return {"id": uid, "name": u.get("name", uid), "gruppen": list(u.get("gruppen") or [])}


def user_groups(user_id: str | None) -> list[str]:
    return get_user(user_id)["gruppen"]


def user_name(user_id: str | None) -> str:
    if user_id == UNKNOWN_CREATOR or not user_id:
        return UNKNOWN_CREATOR
    users = load_permissions()["nutzer"]
    if user_id in users:
        return users[user_id].get("name", user_id)
    return user_id


# ---------------------------------------------------------------------------
# Entscheidungsregel
# ---------------------------------------------------------------------------


def decide(user_id: str | None, meta: PageMeta) -> str:
    """Genau die Regeln aus dem Konzeptdokument + SSOT Vertraulichkeitsstufen."""
    # 1. oeffentlich -> ALLOW, auch fuer Gast
    if meta.vertraulichkeit == "oeffentlich":
        return ALLOW

    user = get_user(user_id)
    groups = set(user["gruppen"])

    # 2. Gast (keine Gruppen) -> DENY
    if user["id"] == GUEST or not groups:
        return DENY

    # 3. keine Gruppe aus domaenen[domaene].lesen -> DENY (unbekannte Domaene ebenso)
    domain = load_permissions()["domaenen"].get(meta.domaene)
    if not domain:
        return DENY
    readers = set(domain.get("lesen") or [])
    if not (groups & readers):
        return DENY

    # 4. Vertraulichkeitsstufen-Rechte aus permissions.yaml pruefen
    perm_stufen = load_permissions().get("vertraulichkeitsstufen") or {}
    if meta.vertraulichkeit in perm_stufen:
        stufe_info = perm_stufen[meta.vertraulichkeit]
        allowed_groups = set(stufe_info.get("leseberechtigt") or [])
        if allowed_groups and not (groups & allowed_groups):
            return DENY

    # 5. vertraulich und weder Ersteller noch Empfaenger (ID oder Gruppe) -> DENY
    if meta.vertraulichkeit == "vertraulich":
        recipients = set(meta.empfaenger)
        is_creator = meta.erstellt_von == user["id"]
        is_recipient = user["id"] in recipients or bool(groups & recipients)
        if not (is_creator or is_recipient):
            return DENY

    # 6. sonst ALLOW
    return ALLOW



def is_allowed(user_id: str | None, meta: PageMeta) -> bool:
    return decide(user_id, meta) == ALLOW


# ---------------------------------------------------------------------------
# Aktueller Nutzer (Simulation per Cookie, bis ein echtes Login existiert)
# ---------------------------------------------------------------------------


def current_user(request: Request) -> str:
    raw = request.cookies.get(COOKIE_NAME)
    return get_user(raw)["id"]
