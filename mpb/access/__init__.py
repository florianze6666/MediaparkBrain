"""Berechtigungen — der Kern. Konzept: docs/BERECHTIGUNGSKONZEPT.md.

Öffentliche Schnittstelle (wird von knowledge, merge, escalation benutzt):

    perms = load_permissions(path)                      -> Permissions
    principal = perms.principal("P-003") / perms.principal("agent:cfo")
    rules = load_acl_rules(path)                        -> AclRules
    acl = resolve_acl(source_path, head, sidecar, rules, perms)   -> ACL      (Konzept §6, Ingest)
    decision = decide(principal, acl, grants=None)      -> Decision (Konzept §7)

Implementierung in: permissions.py, rules.py, acl.py, decide.py. Diese Datei exportiert nur.
"""
from mpb.access.permissions import Permissions, load_permissions          # noqa: F401
from mpb.access.rules import AclRules, load_acl_rules                     # noqa: F401
from mpb.access.acl import resolve_acl, read_sidecar                      # noqa: F401
from mpb.access.decide import decide                                      # noqa: F401
