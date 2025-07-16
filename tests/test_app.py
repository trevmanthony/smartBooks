"""Tests for app module."""

# pylint: disable=wrong-import-position, import-outside-toplevel

from pathlib import Path
import sqlite3
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.concurrency import run_in_threadpool
from fastapi.testclient import TestClient
from bs4 import BeautifulSoup
from app import app, DB_PATH

client = TestClient(app)


def test_get_root():
    """Home page should render successfully and contain the heading."""
    response = client.get("/")
    assert response.status_code == 200
    soup = BeautifulSoup(response.text, "html.parser")
    h1 = soup.find("h1", class_="display-4")
    assert h1 is not None
    assert h1.text.strip() == "smartBooks"


def test_upload_valid_file(tmp_path):
    """Uploading a valid PDF should succeed."""
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(b"%PDF-1.4")
    with pdf_file.open("rb") as f:
        files = {"files": ("test.pdf", f, "application/pdf")}
        response = client.post("/upload", files=files)
    assert response.status_code == 200
    assert response.json() == {"filenames": ["test.pdf"]}
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT filename, content FROM files WHERE filename=?", ("test.pdf",)
        )
        row = cur.fetchone()
    assert row == ("test.pdf", b"%PDF-1.4")


def test_upload_invalid_file(tmp_path):
    """Uploading a non PDF/CSV should fail."""
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("dummy")
    with txt_file.open("rb") as f:
        files = {"files": ("test.txt", f, "text/plain")}
        response = client.post("/upload", files=files)
    assert response.status_code == 400


def test_upload_invalid_mime_type(tmp_path):
    """Uploading with valid extension but wrong MIME type should fail."""
    pdf_file = tmp_path / "fake.pdf"
    pdf_file.write_bytes(b"%PDF-1.4")
    with pdf_file.open("rb") as f:
        files = {"files": ("fake.pdf", f, "text/plain")}
        response = client.post("/upload", files=files)
    assert response.status_code == 400


def test_upload_too_large(tmp_path):
    """Files larger than the 16 MB limit should be rejected."""
    big_file = tmp_path / "big.pdf"
    big_file.write_bytes(b"0" * (16 * 1024 * 1024 + 1))
    with big_file.open("rb") as f:
        files = {"files": ("big.pdf", f, "application/pdf")}
        response = client.post("/upload", files=files)
    assert response.status_code == 400


def count_files():
    """Return number of stored file records."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT COUNT(*) FROM files")
        return cur.fetchone()[0]


def test_purge_endpoint(tmp_path):
    """Uploaded files should be removed by the purge endpoint."""
    pdf = tmp_path / "purge.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    with pdf.open("rb") as f:
        response = client.post(
            "/upload", files={"files": ("purge.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200
    assert count_files() > 0
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT filename, content FROM files WHERE filename=?", ("purge.pdf",)
        )
        row = cur.fetchone()
    assert row == ("purge.pdf", b"%PDF-1.4")

    response = client.post("/purge")
    assert response.status_code == 200
    assert response.json() == {"status": "purged"}
    assert count_files() == 0


def test_env_db_path(tmp_path, monkeypatch):
    """Setting DB_PATH should create database at the custom location."""
    custom_path = tmp_path / "custom.db"
    monkeypatch.setenv("DB_PATH", str(custom_path))
    import importlib
    import app as app_module

    importlib.reload(app_module)
    client_env = TestClient(app_module.app)

    response = client_env.get("/")
    assert response.status_code == 200
    assert custom_path.exists()

    monkeypatch.delenv("DB_PATH", raising=False)
    importlib.reload(app_module)

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT filename FROM files WHERE filename=?", ("purge.pdf",)
        )
        assert cur.fetchone() is None


def test_upload_uses_threadpool(tmp_path, monkeypatch):
    """upload_files should call run_in_threadpool for DB writes."""
    pdf = tmp_path / "thread.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    with pdf.open("rb") as f:
        files = {"files": ("thread.pdf", f, "application/pdf")}
        with monkeypatch.context() as m:
            called = False

            async def wrapper(func, *args, **kwargs):
                nonlocal called
                called = True
                return await run_in_threadpool(func, *args, **kwargs)

            m.setattr("app.run_in_threadpool", wrapper)
            response = client.post("/upload", files=files)
    assert response.status_code == 200
    assert called


def test_purge_uses_threadpool(monkeypatch):
    """purge_database should call run_in_threadpool."""
    with monkeypatch.context() as m:
        called = False

        async def wrapper(func, *args, **kwargs):
            nonlocal called
            called = True
            return await run_in_threadpool(func, *args, **kwargs)

        m.setattr("app.run_in_threadpool", wrapper)
        response = client.post("/purge")
    assert response.status_code == 200
    assert called
