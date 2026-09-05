"""Gemeinsame Datentypen und Protokolle — die Verträge zwischen den Modulen.

Dieses Modul kennt kein anderes mpb-Modul. Jedes andere Modul kennt dieses.
Konzepte: docs/BERECHTIGUNGSKONZEPT.md (ACL, decide), docs/ARCHITEKTUR-RAG.md (Chunks, Retrieval),
docs/ARCHITEKTUR-SYSTEM.md (Modulschnitt), PLAN.md §8 (Assessment-Schema).
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Iterable, Literal, Protocol

# --------------------------------------------------------------------------- Klassifikation

Classification = Literal["internal", "confidential", "restricted"]
CLASS_ORDER: dict[str, int] = {"internal": 0, "confidential": 1, "restricted": 2}


def max_classification(*levels: str) -> Classification:
    """Höchste Stufe aus einer Liste; leere Liste -> internal."""
    best = "internal"
    for lv in levels:
        if CLASS_ORDER.get(lv, 0) > CLASS_ORDER[best]:
            best = lv
    return best  # type: ignore[return-value]


class Decision(str, Enum):
    ALLOW = "allow"  # Inhalt darf geliefert werden
    DENY = "deny"    # nur Metadaten-Stub, eskalierbar
    HIDE = "hide"    # Existenz verborgen, nur Zähler


# --------------------------------------------------------------------------- Principals & ACL

@dataclass(frozen=True)
class Principal:
    """Wer zugreift. `groups` ist vollständig aufgelöst (rekursiv, inkl. grp-alle)."""
    id: str                       # "P-003" oder "agent:cfo"
    groups: frozenset[str]
    kind: Literal["user", "agent"] = "user"
    content_access: bool = True   # False nur für agent:orchestrator
    represents: str | None = None  # bei Agenten: die vertretene Person

    def matches(self, allow: Iterable[str]) -> bool:
        allow = set(allow)
        if self.id in allow or (self.represents and self.represents in allow):
            return True
        return bool(self.groups & allow)


@dataclass(frozen=True)
class ACL:
    """Berechnete Rechte eines Dokuments (BERECHTIGUNGSKONZEPT.md §6)."""
    domain: str
    classification: Classification
    allow: frozenset[str]          # Gruppen und/oder Principal-IDs
    published: bool = False
    owner: str | None = None       # Approver für Eskalationen

    @property
    def acl_hash(self) -> str:
        payload = json.dumps(
            {"d": self.domain, "c": self.classification, "a": sorted(self.allow), "p": self.published},
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()[:16]


@dataclass
class RequestContext:
    """Zwei Identitäten pro Anfrage (Konzept §5.3)."""
    user: str
    agent: str | None = None
    purpose: Literal["evaluation", "chat"] = "evaluation"
    run_id: str = "adhoc"

    @property
    def acting(self) -> str:
        """Wessen Rechte den Inhaltszugriff bestimmen."""
        return f"agent:{self.agent}" if (self.purpose == "evaluation" and self.agent) else self.user


# --------------------------------------------------------------------------- Wissen

@dataclass
class DocumentHead:
    """Dokumentkopf (YAML-Frontmatter im LTT-Format). Unbekannte Felder landen in `extra`."""
    doc_id: str | None = None
    titel: str | None = None
    dokumenttyp: str | None = None
    datum: str | None = None
    verfasser: str | None = None
    rolle: str | None = None
    organisationseinheit: str | None = None
    empfaenger: list[str] = field(default_factory=list)
    projekt: str | None = None
    vertraulichkeit: str | None = None
    informationsdomaene: list[str] = field(default_factory=list)
    ablageort: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Document:
    """Ergebnis der Extraktion, vor dem Chunking."""
    source_path: str
    text: str
    head: DocumentHead
    content_hash: str
    suffix: str
    pages: list[str] | None = None    # bei PDF/XLSX: Text je Seite/Blatt


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    source_path: str
    text: str
    chunk_index: int
    # ACL (Kopie der Dokument-ACL, damit der Index ohne Rückfrage filtern kann)
    domain: str
    classification: Classification
    allow: list[str]
    published: bool
    acl_hash: str
    # Metadaten
    titel: str | None = None
    doc_date: str | None = None
    dokumenttyp: str | None = None
    projekt: str | None = None
    verfasser: str | None = None
    content_hash: str = ""
    version: int = 1
    status: Literal["active", "superseded", "deleted"] = "active"
    page: int | None = None
    topics: list[str] = field(default_factory=list)

    @property
    def acl(self) -> ACL:
        return ACL(self.domain, self.classification, frozenset(self.allow), self.published)


@dataclass
class AllowedHit:
    chunk_id: str
    doc_id: str
    titel: str | None
    source_path: str
    excerpt: str
    doc_date: str | None
    freshness: Literal["aktuell", "überholt", "unbestimmt"]
    classification: Classification
    score: float
    domain: str = ""
    allow: list[str] = field(default_factory=list)   # fuer die Output-Klassifikation (Konzept §10)
    dokumenttyp: str | None = None
    projekt: str | None = None


@dataclass
class DeniedStub:
    """Metadaten ohne Inhalt — der Auslöser für Eskalationen."""
    doc_id: str
    titel: str | None
    domain: str
    classification: Classification
    reason: str
    owner: str | None


@dataclass
class Conflict:
    topic: str
    newer: str   # doc_id
    older: str   # doc_id


@dataclass
class RetrievalResult:
    allowed: list[AllowedHit] = field(default_factory=list)
    denied: list[DeniedStub] = field(default_factory=list)
    conflicts: list[Conflict] = field(default_factory=list)
    hidden_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class RetrievalClient(Protocol):
    """Der EINZIGE Weg zu Inhalten (Konzept §2.8). Agenten bekommen genau dieses Objekt injiziert."""

    def retrieve(self, query: str, ctx: RequestContext, k: int = 8) -> RetrievalResult: ...

    def enrich(self, content: str, ctx: RequestContext, derived_from: list[str], titel: str) -> str: ...


# --------------------------------------------------------------------------- Use Case: Projekte, Gate, Assessments

@dataclass
class Project:
    project_id: str
    run_id: str
    title: str
    source_path: str                 # Pfad im Drive (uploads/<run_id>/...)
    doc_id: str | None = None
    fields: dict[str, str] = field(default_factory=dict)   # die 15 Pflichtfelder aus PLAN.md §2
    status: Literal["uploaded", "incomplete", "ready", "evaluating", "waiting_escalation", "assessed"] = "uploaded"
    missing: list[str] = field(default_factory=list)


@dataclass
class GateResult:
    ok: bool
    missing: list[str] = field(default_factory=list)
    fields: dict[str, str] = field(default_factory=dict)


@dataclass
class Assessment:
    """PLAN.md §8 plus die Felder, die Berechtigung und Nachvollziehbarkeit brauchen."""
    role: str
    project_id: str
    run_id: str
    value_score: int
    risk_score: int
    strategy_score: int
    assessment: str
    cited_chunks: list[str] = field(default_factory=list)
    open_escalations: list[str] = field(default_factory=list)
    information_gaps: list[str] = field(default_factory=list)
    classification: Classification = "internal"
    allow: list[str] = field(default_factory=lambda: ["grp-alle"])
    status: Literal["ok", "failed"] = "ok"
    error: str | None = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat(timespec="seconds") + "Z")

    def to_jsonl(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


@dataclass
class Escalation:
    escalation_id: str
    run_id: str
    requested_by: str
    on_behalf_of: str
    doc_id: str
    domain: str
    classification: Classification
    needed_information: str
    reason: str
    purpose: str
    affected_criteria: list[str]
    required_level: Classification
    approver: str | None
    status: Literal["open", "approved", "rejected", "expired"] = "open"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat(timespec="seconds") + "Z")
    expires_at: str | None = None


@dataclass
class ProjectResult:
    project_id: str
    assessments: dict[str, Assessment]                  # role -> Assessment
    conflicts: list[dict[str, Any]] = field(default_factory=list)   # {"roles": [a,b], "metric": ..., "delta": ...}
    total: float | None = None


@dataclass
class Run:
    run_id: str
    user: str
    status: Literal["created", "ingested", "gated", "evaluating", "merged", "done", "failed"] = "created"
    projects: list[str] = field(default_factory=list)   # project_ids
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat(timespec="seconds") + "Z")


# --------------------------------------------------------------------------- LLM

@dataclass
class Completion:
    text: str
    model: str
    usage: dict[str, int] = field(default_factory=dict)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)


class LLMProvider(Protocol):
    def complete(
        self,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        model: str | None = None,
        max_tokens: int = 2048,
    ) -> Completion: ...


# --------------------------------------------------------------------------- Audit

@dataclass
class AuditEvent:
    op: str
    user: str
    agent: str | None
    run_id: str
    query: str | None = None
    allow: int = 0
    deny: int = 0
    hide: int = 0
    denied_docs: list[str] = field(default_factory=list)
    detail: dict[str, Any] = field(default_factory=dict)
    ts: str = field(default_factory=lambda: datetime.utcnow().isoformat(timespec="seconds") + "Z")

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)
