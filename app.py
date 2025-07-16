"""Web application for smartBooks."""

import os
import sqlite3
from typing import List

from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.concurrency import run_in_threadpool
from config import settings

app = FastAPI()

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


def init_db() -> None:
    """Create the files table if it doesn't exist and ensure `content` column."""
    os.makedirs(settings.db_path.parent, exist_ok=True)
    with sqlite3.connect(settings.db_path) as conn:
        conn.execute(
            (
                "CREATE TABLE IF NOT EXISTS files ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "filename TEXT, content BLOB)"
            )
        )
        cols = [row[1] for row in conn.execute("PRAGMA table_info(files)")]
        if "content" not in cols:
            conn.execute("ALTER TABLE files ADD COLUMN content BLOB")


init_db()


DEFAULT_CONTEXT = {
    "view_type": "index",
    "transaction_type": "inflow",
    "total_amount": 0.0,
    "has_unclassified": False,
    "leaderboard": [],
}


def render(
    template_name: str, request: Request, context: dict | None = None
) -> HTMLResponse:
    """Return a TemplateResponse with default context."""
    final_context = {"request": request, **DEFAULT_CONTEXT}
    if context:
        final_context.update(context)
    return templates.TemplateResponse(template_name, final_context)


@app.get("/", response_class=HTMLResponse, name="index")
async def read_root(request: Request):
    """Render the home page."""
    return render("index.html", request)


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Accept PDF and CSV files and store their contents."""
    allowed_types = {"application/pdf", "text/csv"}
    records = []
    for file in files:
        if not (
            file.filename.lower().endswith(".pdf")
            or file.filename.lower().endswith(".csv")
        ):
            raise HTTPException(status_code=400, detail="Invalid file type")
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid MIME type")
        content = await file.read()
        if len(content) > settings.max_file_size:
            raise HTTPException(status_code=400, detail="File too large")
        records.append((file.filename, sqlite3.Binary(content)))

    def insert_records() -> None:
        with sqlite3.connect(settings.db_path) as conn:
            conn.executemany(
                "INSERT INTO files(filename, content) VALUES (?, ?)",
                records,
            )

    await run_in_threadpool(insert_records)
    return {"filenames": [file.filename for file in files]}


@app.post("/purge")
async def purge_database():
    """Remove all uploaded file records."""

    def purge() -> None:
        with sqlite3.connect(settings.db_path) as conn:
            conn.execute("DELETE FROM files")

    await run_in_threadpool(purge)
    return {"status": "purged"}
