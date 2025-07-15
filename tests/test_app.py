"""Tests for app module."""

# pylint: disable=wrong-import-position

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from bs4 import BeautifulSoup
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


def test_upload_invalid_file(tmp_path):
    """Uploading a non PDF/CSV should fail."""
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("dummy")
    with txt_file.open("rb") as f:
        files = {"files": ("test.txt", f, "text/plain")}
        response = client.post("/upload", files=files)
    assert response.status_code == 400
