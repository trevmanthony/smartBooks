"""Celery tasks for background file processing."""

import os
import sqlite3
from celery import Celery

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "data", "database.db")
DB_PATH = os.getenv("DB_PATH", DEFAULT_DB_PATH)

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery_app = Celery("smartbooks", broker=CELERY_BROKER_URL)

if os.getenv("CELERY_TASK_ALWAYS_EAGER"):
    celery_app.conf.task_always_eager = True


def init_db() -> None:
    """Create the files table if needed."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            (
                "CREATE TABLE IF NOT EXISTS files ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "filename TEXT, content BLOB)"
            )
        )


init_db()


@celery_app.task
def store_file(filename: str, content: bytes) -> None:
    """Persist an uploaded file to the SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO files(filename, content) VALUES (?, ?)",
            (filename, sqlite3.Binary(content)),
        )
