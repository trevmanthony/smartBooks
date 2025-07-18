"""Tests for asynchronous pipeline."""

# pylint: disable=wrong-import-position, import-outside-toplevel, import-error, missing-class-docstring, missing-function-docstring, too-few-public-methods, unused-argument, unnecessary-lambda

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
    expected_prompt = (
        "Extract the invoice number, date, and total from this text as JSON.\n"
        "stub text"
    )
    assert result == f"processed: {expected_prompt}"


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

    def fake_delay(data: bytes) -> None:
        nonlocal called
        called = True
        assert data == b"%PDF-1.4"

    with monkeypatch.context() as m:
        m.setattr(app_module.process_file_task, "delay", fake_delay)
        response = client_env.post(f"/process/{file_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "queued"}
    assert called


def test_create_langchain_pipeline(monkeypatch):
    """create_langchain_pipeline should use env vars to configure clients."""
    import pipeline as pl

    cfg = pl.PipelineConfig(
        doc_ai_project_id="proj",
        doc_ai_location="us",
        doc_ai_processor_id="pid",
        o4mini_model_path="/model.bin",
    )

    class FakeDocClient:
        def processor_path(self, p, l, pr):
            assert (p, l, pr) == ("proj", "us", "pid")
            return "name"

        async def process_document(self, request):
            class R:
                class D:
                    text = "ocr text"

                document = D()

            return R()

    class FakeLlama:
        def __init__(self, model_path, n_ctx=2048):
            assert model_path == "/model.bin"

        def invoke(self, prompt):
            return f"{prompt} processed"

    monkeypatch.setattr(
        pl,
        "DOCUMENTAI",
        type(
            "m",
            (),
            {
                "DocumentProcessorServiceAsyncClient": lambda: FakeDocClient(),
                "ProcessRequest": lambda name, raw_document=None, **kw: object(),
                "RawDocument": lambda content, mime_type: object(),
            },
        ),
    )
    monkeypatch.setattr(pl, "LLAMACPP", FakeLlama)

    pipeline = pl.create_langchain_pipeline(cfg)
    result = asyncio.run(pipeline.run(b"data"))
    expected_prompt = (
        "Extract the invoice number, date, and total from this text as JSON.\n"
        "ocr text"
    )
    assert result == f"{expected_prompt} processed"
