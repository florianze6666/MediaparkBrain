"""Berechtigungen und Herkunft (Paket 1).

Ein Zugriffsweg: jede Sichtbarkeitsentscheidung laeuft ueber `decide`.
Nutzer, Gruppen und Domaenen sind Daten in permissions.yaml, kein Code.
Vertrag: docs/berechtigungen-und-herkunft.md (Stufe 1),
docs/berechtigungen-stufe-2-admin-und-ablage.md (Stufe 2: Admin, Changelog).
"""
from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import re
import secrets
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from fastapi import Request

log = logging.getLogger(__name__)

GUEST = "gast"
UNKNOWN_CREATOR = "unbekannt"
COOKIE_NAME = "mpb_user"
ADMIN_GROUP = "admin"
# Die Lobby: pages/allgemein/ darf jeder betreten, auch der Gast. Innerhalb
# entscheidet weiterhin `decide` pro Seite (Gast sieht dort nur oeffentlich).
LOBBY_DOMAIN = "allgemein"

# IDs fuer Nutzer, Gruppen und Domaenen (Domaene = Ordnername unter pages/)
ID_RE = re.compile(r"^[a-z0-9-]{2,40}$")

VERTRAULICHKEITEN = ("oeffentlich", "intern", "vertraulich")

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
        meta.vertraulichkeit, meta.empfaenger = normalize_confidentiality(
            meta.vertraulichkeit, meta.empfaenger
        )
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


def changelog_path() -> Path:
    env = os.environ.get("MPB_CHANGELOG_FILE")
    if env:
        return Path(env)
    return permissions_path().parent / "permissions-changelog.md"


_cache: dict[str, Any] = {"key": None, "data": None}


def clear_cache() -> None:
    _cache["key"] = None
    _cache["data"] = None


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


def normalize_confidentiality(
    vertraulichkeit: str,
    empfaenger: list[str] | None = None,
) -> tuple[str, list[str]]:
    """Uebersetzt Korpus-Stufen (z.B. C-Level, Betriebsrat-intern) auf das
    Rechtemodell (vertraulichkeit + empfaenger) gemaess permissions.yaml."""
    stufen = load_permissions().get("vertraulichkeitsstufen") or {}
    empf = list(empfaenger or [])
    if vertraulichkeit in stufen:
        cfg = stufen[vertraulichkeit]
        target_vert = cfg.get("vertraulichkeit", vertraulichkeit)
        default_empf = cfg.get("empfaenger") or []
        for e in default_empf:
            if e not in empf:
                empf.append(e)
        return target_vert, empf
    if vertraulichkeit not in VERTRAULICHKEITEN:
        vertraulichkeit = "intern"
    return vertraulichkeit, empf


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


def readable_domains(user_id: str | None) -> list[str]:
    """Domaenenordner, die der Nutzer betreten darf (Ordner-Schranke, US-18).

    Immer dabei: die Lobby `allgemein` (auch fuer den Gast). Dazu jede Domaene,
    deren Lesegruppen sich mit den Gruppen des Nutzers schneiden (Regel 3 auf
    Ordnerebene). Reihenfolge wie in permissions.yaml.

    Der Ordner ist die einzige Wahrheit: `wiki.list_pages(user)` betritt NUR
    diese Ordner; ein Label `oeffentlich` in einem fremden Ordner oeffnet ihn nicht.
    """
    groups = set(user_groups(user_id))
    out: list[str] = []
    for dom, spec in load_permissions()["domaenen"].items():
        readers = set((spec or {}).get("lesen") or [])
        if dom == LOBBY_DOMAIN or (groups & readers):
            out.append(dom)
    if LOBBY_DOMAIN not in out:
        out.insert(0, LOBBY_DOMAIN)
    return out


def is_admin(user_id: str | None) -> bool:
    """Gruppe admin verwaltet Rechte, liest aber nichts zusaetzlich (decide unveraendert)."""
    return ADMIN_GROUP in user_groups(user_id)


# ---------------------------------------------------------------------------
# Entscheidungsregel
# ---------------------------------------------------------------------------


def decide(user_id: str | None, meta: PageMeta) -> str:
    """Genau die Regeln aus dem Konzeptdokument."""
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

    # 4. vertraulich und weder Ersteller noch Empfaenger (ID oder Gruppe) -> DENY
    if meta.vertraulichkeit == "vertraulich":
        recipients = set(meta.empfaenger)
        is_creator = meta.erstellt_von == user["id"]
        is_recipient = user["id"] in recipients or bool(groups & recipients)
        if not (is_creator or is_recipient):
            return DENY

    # 5. sonst ALLOW
    return ALLOW



def is_allowed(user_id: str | None, meta: PageMeta) -> bool:
    return decide(user_id, meta) == ALLOW


def can_read(user_id: str | None, meta: PageMeta) -> bool:
    """Ordner-Schranke UND Seitenregel: Der Nutzer darf den Domaenenordner
    betreten (readable_domains) und `decide` erlaubt die Seite.
    Das Label `oeffentlich` erweitert nie die Ordnerrechte (Label verschaerft nur)."""
    return meta.domaene in readable_domains(user_id) and decide(user_id, meta) == ALLOW


def can_write(user_id: str | None, meta: PageMeta) -> bool:
    """Schreiben nur, wo man lesen darf (Write ⊆ Read).

    True nur, wenn die Zieldomaene lesbar ist UND `decide` die Seite mit genau
    diesen Metadaten erlaubt - ein Autor kann eine vertrauliche Seite also nur so
    anlegen, dass er sie selbst noch sieht (als Ersteller automatisch erfuellt).
    Beim Bearbeiten gilt die Pruefung fuer die NEUE Domaene: Verschieben in eine
    fremde Domaene ist verboten.
    """
    return can_read(user_id, meta)


# ---------------------------------------------------------------------------
# Aktueller Nutzer: signierter Identitaets-Cookie (bis ein echtes Login existiert)
# ---------------------------------------------------------------------------


def _load_secret() -> bytes:
    """Secret fuer die Cookie-Signatur aus MPB_SECRET. Fehlt es, gilt ein
    zufaelliges Secret bis zum Neustart (Sessions ueberleben den Neustart nicht)."""
    env = os.environ.get("MPB_SECRET", "").strip()
    if env:
        return env.encode("utf-8")
    log.warning("MPB_SECRET nicht gesetzt, Sessions gelten nur bis zum Neustart")
    return secrets.token_hex(32).encode("utf-8")


_SECRET = _load_secret()


def _signature(uid: str) -> str:
    return hmac.new(_SECRET, uid.encode("utf-8"), hashlib.sha256).hexdigest()


def sign_user(uid: str) -> str:
    """Cookie-Wert `<uid>.<hex-signatur>` (HMAC-SHA256 ueber die Nutzer-ID)."""
    return f"{uid}.{_signature(uid)}"


def verify_user(value: str | None) -> str | None:
    """Nutzer-ID aus einem Cookie-Wert; None bei fehlender, unsignierter oder
    manipulierter Signatur. Vergleich in konstanter Zeit."""
    if not value or "." not in value:
        return None
    uid, sig = value.rsplit(".", 1)
    if not ID_RE.match(uid):
        return None
    if not hmac.compare_digest(_signature(uid), sig):
        return None
    return uid


def current_user(request: Request) -> str:
    """Nutzer aus dem signierten Cookie; ungueltig oder unsigniert -> Gast."""
    return get_user(verify_user(request.cookies.get(COOKIE_NAME)))["id"]


# ---------------------------------------------------------------------------
# Rechte-Datei schreiben (Admin, Stufe 2) + Protokoll
# ---------------------------------------------------------------------------


def _yaml_str(value: str) -> str:
    # JSON-Doppelquotes sind gueltiges YAML, inkl. Umlaute.
    return json.dumps(str(value), ensure_ascii=False)


def _yaml_list(values: list[str]) -> str:
    return "[" + ", ".join(str(v) for v in values) + "]"


_KEY_LINE_RE = re.compile(r"^\s*([A-Za-z0-9_-]+)\s*:.*?(#.*)$")


def _existing_layout(path: Path) -> tuple[list[str], dict[str, str]]:
    """Kopfkommentar und Zeilenkommentare der bestehenden Datei.

    Zeilenkommentare werden per Abschnitt+Schluessel gemerkt ("domaenen/finance"),
    damit die Zuordnung Ablageort -> Domaene (Paket 7) beim Speichern erhalten bleibt.
    """
    header: list[str] = []
    comments: dict[str, str] = {}
    if not path.exists():
        return header, comments
    section = ""
    in_header = True
    for line in path.read_text(encoding="utf-8").splitlines():
        if in_header:
            if line.startswith("#") or not line.strip():
                header.append(line)
                continue
            in_header = False
        m = _KEY_LINE_RE.match(line)
        if line and not line[0].isspace():
            section = line.split(":", 1)[0].strip()
            if m:
                comments[section] = m.group(2)
            continue
        if m and section:
            comments[f"{section}/{m.group(1)}"] = m.group(2)
    while header and not header[-1].strip():
        header.pop()
    return header, comments


def render_permissions(data: dict[str, Any], header: list[str], comments: dict[str, str]) -> str:
    def with_comment(text: str, key: str, width: int) -> str:
        c = comments.get(key)
        if not c:
            return text
        return f"{text:<{width}} {c}"

    lines = list(header) + ([""] if header else [])
    lines.append(with_comment(f"gruppen: {_yaml_list(data.get('gruppen') or [])}", "gruppen", 0))
    lines.append("")
    lines.append(with_comment("nutzer:", "nutzer", 0))
    users = data.get("nutzer") or {}
    for uid, u in users.items():
        u = u or {}
        key = f"{uid}:"
        text = (
            f"  {key:<16} {{name: {_yaml_str(u.get('name', uid))},"
            f" gruppen: {_yaml_list(list(u.get('gruppen') or []))}}}"
        )
        lines.append(with_comment(text, f"nutzer/{uid}", 60))
    lines.append("")
    lines.append(with_comment("domaenen:", "domaenen", 20))
    for dom, spec in (data.get("domaenen") or {}).items():
        spec = spec or {}
        key = f"{dom}:"
        text = f"  {key:<10} {{lesen: {_yaml_list(list(spec.get('lesen') or []))}}}"
        lines.append(with_comment(text, f"domaenen/{dom}", 42))
    return "\n".join(lines) + "\n"


def save_permissions(data: dict[str, Any], changed_by: str, change_note: str) -> None:
    """Schreibt permissions.yaml (Kopfkommentar und Reihenfolge bleiben) und
    haengt eine Protokollzeile an permissions-changelog.md. Cache wird geleert,
    die Aenderung gilt sofort (kein Neustart)."""
    path = permissions_path()
    header, comments = _existing_layout(path)
    text = render_permissions(data, header, comments)
    # Sicherheitsnetz: was wir schreiben, muss sich wieder lesen lassen.
    parsed = yaml.safe_load(text) or {}
    for key in ("gruppen", "nutzer", "domaenen"):
        if parsed.get(key) != data.get(key):
            raise ValueError(f"permissions.yaml: Abschnitt {key} liesse sich nicht identisch zurücklesen")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    clear_cache()
    append_changelog(changed_by, change_note)


def append_changelog(changed_by: str, change_note: str) -> None:
    path = changelog_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(
            "# Protokoll Rechteänderungen\n\n"
            "Jede Änderung an permissions.yaml über das Admin-Dashboard. "
            "Format: `- Zeit · Admin · Änderung (vorher → nachher)`.\n\n",
            encoding="utf-8",
        )
    stamp = datetime.now().strftime("%Y-%m-%dT%H:%M")
    note = " ".join(change_note.split())
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"- {stamp} · {changed_by} · {note}\n")


def read_changelog(n: int = 20) -> list[str]:
    """Die letzten n Protokollzeilen, neueste zuerst."""
    path = changelog_path()
    if not path.exists():
        return []
    entries = [
        line[2:].strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ")
    ]
    return list(reversed(entries[-n:]))
