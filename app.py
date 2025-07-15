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

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def init_db() -> None:
    """Create the files table if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT)"
        )


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
    """Accept PDF and CSV files and store their names."""
    for file in files:
        if not (
            file.filename.lower().endswith(".pdf")
            or file.filename.lower().endswith(".csv")
        ):
            raise HTTPException(status_code=400, detail="Invalid file type")
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            "INSERT INTO files(filename) VALUES (?)",
            [(file.filename,) for file in files],
        )
    return {"filenames": [file.filename for file in files]}


@app.post("/purge")
async def purge_database():
    """Remove all uploaded file records."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM files")
    return {"status": "purged"}
