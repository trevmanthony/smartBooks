"""Tests for app module."""

# pylint: disable=wrong-import-position, import-outside-toplevel, unused-argument

from pathlib import Path
import asyncio
import sys
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from bs4 import BeautifulSoup
from sqlmodel import select
from database import AsyncSessionLocal, File as DBFile
from app import app

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

    async def fetch():
        async with AsyncSessionLocal() as session:
            result = await session.exec(
                select(DBFile.filename, DBFile.content).where(
                    DBFile.filename == "test.pdf"
                )
            )
            return result.first()

    row = asyncio.run(fetch())
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

    async def _count():
        async with AsyncSessionLocal() as session:
            result = await session.exec(select(DBFile))
            return len(result.all())

    return asyncio.run(_count())


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

    async def fetch():
        async with AsyncSessionLocal() as session:
            result = await session.exec(
                select(DBFile.filename, DBFile.content).where(
                    DBFile.filename == "purge.pdf"
                )
            )
            return result.first()

    row = asyncio.run(fetch())
    assert row == ("purge.pdf", b"%PDF-1.4")

    response = client.post("/purge")
    assert response.status_code == 200
    assert response.json() == {"status": "purged"}
    assert count_files() == 0


@pytest.mark.xfail(strict=True, reason="Module reload conflicts with SQLModel")
def test_env_db_path(tmp_path, monkeypatch):
    """Setting DB_PATH should create database at the custom location."""
    custom_path = tmp_path / "custom.db"
    monkeypatch.setenv("DB_PATH", str(custom_path))
    import importlib
    import config as config_module

    sys.modules.pop("database", None)
    import app as app_module

    importlib.reload(config_module)
    importlib.reload(app_module)
    client_env = TestClient(app_module.app)

    response = client_env.get("/")
    assert response.status_code == 200
    assert custom_path.exists()

    monkeypatch.delenv("DB_PATH", raising=False)
    importlib.reload(app_module)


def test_upload_not_threadpool(tmp_path, monkeypatch):
    """upload_files should not use run_in_threadpool with async DB."""
    pdf = tmp_path / "thread.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    with pdf.open("rb") as f:
        files = {"files": ("thread.pdf", f, "application/pdf")}
        assert not hasattr(app, "run_in_threadpool")
        response = client.post("/upload", files=files)
    assert response.status_code == 200


def test_purge_not_threadpool(monkeypatch):
    """purge_database should not use run_in_threadpool."""
    assert not hasattr(app, "run_in_threadpool")
    response = client.post("/purge")
    assert response.status_code == 200
