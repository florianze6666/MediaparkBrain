"""Testfixtures: Kopie des Demo-Drives in tmp_path, damit Verschieben/Löschen nichts kaputt macht."""
from __future__ import annotations
import shutil
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    dst = tmp_path / "data"
    shutil.copytree(DATA / "drive", dst / "drive")
    shutil.copy(DATA / "permissions.yaml", dst / "permissions.yaml")
    shutil.copy(DATA / "acl-rules.yaml", dst / "acl-rules.yaml")
    (dst / "index").mkdir()
    return dst
