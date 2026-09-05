"""Wissensschicht (das RAG). Konzept: docs/ARCHITEKTUR-RAG.md.

Öffentliche Schnittstelle:

    source = LocalFolderSource(drive_dir)                         # sources.py, Protocol DriveSource
    report = scan(source, catalog, index, perms, rules)           # ingest.py — 5 Fälle, ACL vor Index
    client = KnowledgeService(catalog, index, perms, audit)       # retrieval.py, erfüllt RetrievalClient
    client.retrieve(query, ctx, k) -> RetrievalResult
    client.enrich(content, ctx, derived_from, titel) -> doc_id

Agenten bekommen NUR `client` (mpb.types.RetrievalClient), nie Pfade.
"""
from mpb.knowledge.sources import DriveSource, LocalFolderSource, SourceItem   # noqa: F401
from mpb.knowledge.retrieval import KnowledgeService                           # noqa: F401
from mpb.knowledge.ingest import scan                                          # noqa: F401
