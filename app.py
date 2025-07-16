"""Web application for smartBooks."""

import os
from typing import List

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Request,
    HTTPException,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import delete
from database import AsyncSessionLocal, File as DBFile, Extraction
import database
from worker import process_file_task
from config import settings

app = FastAPI()

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

os.makedirs(settings.db_path.parent, exist_ok=True)


@app.on_event("startup")
async def on_startup() -> None:
    """Initialize the database on startup."""
    await database.init_db_async()


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
        records.append(DBFile(filename=file.filename, content=content))

    async with AsyncSessionLocal() as session:
        session.add_all(records)
        await session.commit()
    return {"filenames": [file.filename for file in files]}


@app.post("/purge")
async def purge_database():
    """Remove all uploaded file records."""

    async with AsyncSessionLocal() as session:
        await session.exec(delete(Extraction))
        await session.exec(delete(DBFile))
        await session.commit()
    return {"status": "purged"}


@app.post("/process/{file_id}")
async def process_file(file_id: int):
    """Run the OCR and LLM pipeline for a stored file."""

    async with AsyncSessionLocal() as session:
        file = await session.get(DBFile, file_id)
        if file is None:
            raise HTTPException(status_code=404, detail="File not found")

    process_file_task.delay(file_id)
    return {"status": "queued"}
