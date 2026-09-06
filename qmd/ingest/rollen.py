"""Rollen-zu-Collections-Bruecke.

Der Agent einer Rolle erbt die Vertraulichkeitsklassen dieser Rolle, nicht ihre
Domaenen. Das Wiki-Rechtemodell (Domaene x Gruppe, Empfaenger je Seite) gilt
fuer Menschen an der Oberflaeche; fuer Agenten am qmd-Index gilt allein die
Klasse. Beide lesen dieselbe Quelle: llm-wiki/permissions.yaml.

Ableitung, ohne zweite Tabelle:
    Gruppen der Rolle      -> permissions.yaml, nutzer.<id>.gruppen
    Empfaenger je Stufe    -> permissions.yaml, vertraulichkeitsstufen.<stufe>.empfaenger
    Stufe -> Collection    -> build_view.KLASSE_AUS_ROHSTUFE, dieselbe Tabelle wie der Ingest

Regel: `intern` bekommt jede Rolle mit mindestens einer Gruppe. Eine
ausgeschlossene Collection (`br`, `clevel`) kommt dazu, wenn die Rolle selbst
oder eine ihrer Gruppen in der Empfaengerliste der zugehoerigen Stufe steht.
Das spiegelt Regel 4 von access.decide (Empfaenger als ID oder Gruppe) und
laesst Regel 3 (Domaene) bewusst weg.

Faellt zu: Eine unbekannte Rolle, eine Rolle ohne Gruppen (Gast) und eine
Stufe ohne Klassenzuordnung ergeben einen Fehler, keine leere Liste. Eine leere
Liste waere gefaehrlich, weil `qmd query` ohne `-c` die Standard-Collection
`intern` durchsucht und der Aufruf von aussen wie gewollt aussaehe.

Aufruf:
    python ingest/rollen.py          Tabelle Rolle -> Collections fuer alle Rollen
    python ingest/rollen.py cfo      Collections einer Rolle, eine je Zeile
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_view import KLASSEN, KLASSE_AUS_ROHSTUFE, PERMISSIONS_FILE, load_yaml  # noqa: E402

BASIS = "intern"


class RollenFehler(ValueError):
    """Rolle kann keinem Collection-Satz zugeordnet werden. Absichtlich laut."""


def collections_for_role(user_id: str, permissions: dict | None = None) -> list[str]:
    """Collections, die ein Agent dieser Rolle mit `-c` nennen darf.

    Reihenfolge wie build_view.KLASSEN, damit Protokolle vergleichbar bleiben.
    """
    perms = permissions if permissions is not None else load_yaml(PERMISSIONS_FILE)
    nutzer = perms.get("nutzer") or {}
    if user_id not in nutzer:
        raise RollenFehler(f"Rolle {user_id!r} steht nicht in {PERMISSIONS_FILE.name}.")
    gruppen = set((nutzer[user_id] or {}).get("gruppen") or [])
    if not gruppen:
        raise RollenFehler(
            f"Rolle {user_id!r} hat keine Gruppen und damit keinen Zugriff auf den Index."
        )

    klassen = {BASIS}
    for stufe, cfg in (perms.get("vertraulichkeitsstufen") or {}).items():
        klasse = KLASSE_AUS_ROHSTUFE.get(stufe)
        if klasse is None:
            raise RollenFehler(
                f"Stufe {stufe!r} aus {PERMISSIONS_FILE.name} fehlt in "
                "build_view.KLASSE_AUS_ROHSTUFE; erst dort eintragen."
            )
        if klasse == BASIS:
            continue
        empfaenger = set((cfg or {}).get("empfaenger") or [])
        if user_id in empfaenger or (gruppen & empfaenger):
            klassen.add(klasse)
    return [k for k in KLASSEN if k in klassen]


def tabelle(permissions: dict) -> list[tuple[str, str]]:
    """(Rolle, Collections oder Fehlertext) fuer jede Rolle in Dateireihenfolge."""
    zeilen = []
    for uid in (permissions.get("nutzer") or {}):
        try:
            zeilen.append((uid, ", ".join(collections_for_role(uid, permissions))))
        except RollenFehler as e:
            zeilen.append((uid, f"kein Zugriff: {e}"))
    return zeilen


def main(argv: list[str]) -> int:
    perms = load_yaml(PERMISSIONS_FILE)
    if len(argv) > 1:
        try:
            print("\n".join(collections_for_role(argv[1], perms)))
        except RollenFehler as e:
            print(f"FEHLER: {e}", file=sys.stderr)
            return 2
        return 0
    print(f"Quelle: {PERMISSIONS_FILE}\n")
    print(f"{'Rolle':<16} Collections")
    print("-" * 44)
    for uid, cols in tabelle(perms):
        print(f"{uid:<16} {cols}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
