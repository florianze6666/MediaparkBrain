"""Konfiguration aus Umgebung/.env. Einziges Modul, das os.environ liest."""
from __future__ import annotations
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MPB_", env_file=".env", extra="ignore")

    data_dir: Path = Path("./data")
    llm_provider: str = "mock"            # mock | anthropic
    model_agent: str = "claude-sonnet-5"
    model_fast: str = "claude-haiku-4-5-20251001"
    chunk_tokens: int = 600
    chunk_overlap: float = 0.1
    retrieval_k: int = 8
    escalation_ttl_minutes: int = 60

    @property
    def drive_dir(self) -> Path: return self.data_dir / "drive"
    @property
    def index_dir(self) -> Path: return self.data_dir / "index"
    @property
    def permissions_file(self) -> Path: return self.data_dir / "permissions.yaml"
    @property
    def acl_rules_file(self) -> Path: return self.data_dir / "acl-rules.yaml"
    @property
    def audit_file(self) -> Path: return self.data_dir / "audit.jsonl"
    @property
    def roles_dir(self) -> Path: return Path(__file__).resolve().parent.parent / "roles"


def get_settings() -> Settings:
    return Settings()
