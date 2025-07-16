"""Browser-based tests for index.html JavaScript."""

# pylint: disable=redefined-outer-name, import-error

from __future__ import annotations
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

sys.path.append(str(Path(__file__).resolve().parents[1]))
from config import settings  # pylint: disable=wrong-import-position

PORT = 8001
SERVER_CMD = ["uvicorn", "app:app", "--port", str(PORT)]


@pytest.fixture(scope="module", autouse=True)
def server():
    """Start the FastAPI server for browser tests."""
    with subprocess.Popen(SERVER_CMD) as proc:
        time.sleep(2)
        yield
        proc.terminate()
        proc.wait()


@pytest.fixture()
def driver(server):  # pylint: disable=unused-argument
    """Provide a headless Chrome WebDriver."""
    options = Options()
    for arg in ["--headless", "--no-sandbox", "--disable-dev-shm-usage"]:
        options.add_argument(arg)
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(3)
    yield drv
    drv.quit()


def count_files() -> int:
    """Return current count of uploaded files."""
    with sqlite3.connect(settings.db_path) as conn:
        cur = conn.execute("SELECT COUNT(*) FROM files")
        return cur.fetchone()[0]


def test_upload_via_browser(driver, tmp_path):
    """Uploading a file through the UI should create a DB record."""
    pdf = tmp_path / "browser.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    driver.get(f"http://localhost:{PORT}/")
    # Open the upload modal first
    driver.find_element(By.CSS_SELECTOR, "[data-bs-target='#uploadModal']").click()
    WebDriverWait(driver, 5).until(
        lambda d: d.find_element(By.ID, "uploadModal").is_displayed()
    )
    driver.find_element(By.ID, "file").send_keys(str(pdf))
    driver.find_element(By.ID, "upload-btn").click()
    WebDriverWait(driver, 5).until(
        lambda d: "Files uploaded successfully!" in d.page_source
    )
    WebDriverWait(driver, 5).until(lambda d: count_files() > 0)
    assert count_files() > 0


def test_purge_via_browser(driver):
    """Clicking Purge DB should remove records."""
    with sqlite3.connect(settings.db_path) as conn:
        conn.execute("INSERT INTO files(filename) VALUES ('dummy.pdf')")
    assert count_files() > 0
    driver.get(f"http://localhost:{PORT}/")
    driver.find_element(By.CSS_SELECTOR, "button[onclick='purgeDatabase()']").click()
    alert = driver.switch_to.alert
    alert.accept()
    WebDriverWait(driver, 5).until(lambda d: "Database purged." in d.page_source)
    WebDriverWait(driver, 5).until(lambda d: count_files() == 0)
    assert count_files() == 0
