"""Web application for smartBooks."""

import os
import sqlite3
from typing import List

from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "data", "database.db")
DB_PATH = os.getenv("DB_PATH", DEFAULT_DB_PATH)


def init_db() -> None:
    """Create the files table if it doesn't exist and ensure `content` column."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
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
    records = []
    for file in files:
        if not (
            file.filename.lower().endswith(".pdf")
            or file.filename.lower().endswith(".csv")
        ):
            raise HTTPException(status_code=400, detail="Invalid file type")
        content = await file.read()
        records.append((file.filename, sqlite3.Binary(content)))
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            "INSERT INTO files(filename, content) VALUES (?, ?)",
            records,
        )
    return {"filenames": [file.filename for file in files]}


@app.post("/purge")
async def purge_database():
    """Remove all uploaded file records."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM files")
    return {"status": "purged"}
