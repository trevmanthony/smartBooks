"""Tests for asynchronous pipeline."""

# pylint: disable=wrong-import-position, import-outside-toplevel

from pathlib import Path
import sqlite3
import asyncio
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from pipeline import AsyncPipeline, StubLLMClient, StubOCRClient


def test_pipeline_stub_run():
    """Pipeline should combine stub components."""
    pl = AsyncPipeline(StubOCRClient(), StubLLMClient())
    result = asyncio.run(pl.run(b"data"))
    assert result == "processed: stub text"


def test_process_endpoint(tmp_path, monkeypatch):
    """/process should schedule pipeline task."""
    import importlib
    import app as app_module
    import config as config_module

    importlib.reload(config_module)
    importlib.reload(app_module)
    client_env = TestClient(app_module.app)

    pdf = tmp_path / "proc.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    with sqlite3.connect(config_module.settings.db_path) as conn:
        conn.execute(
            "INSERT INTO files(filename, content) VALUES(?, ?)",
            ("proc.pdf", pdf.read_bytes()),
        )
        conn.commit()
        file_id = conn.execute(
            "SELECT id FROM files WHERE filename='proc.pdf'"
        ).fetchone()[0]

    called = False

    async def fake_run(data: bytes) -> None:
        nonlocal called
        called = True
        assert data == b"%PDF-1.4"

    with monkeypatch.context() as m:
        m.setattr(app_module.__name__ + ".pipeline.run", fake_run)
        response = client_env.post(f"/process/{file_id}")
    assert response.status_code == 200
    assert called
