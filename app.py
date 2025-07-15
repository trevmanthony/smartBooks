"""Web application for smartBooks."""

import os
from typing import List

from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


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
    """Accept PDF and CSV files and return their names."""
    for file in files:
        if not (
            file.filename.lower().endswith(".pdf")
            or file.filename.lower().endswith(".csv")
        ):
            raise HTTPException(status_code=400, detail="Invalid file type")
    return {"filenames": [file.filename for file in files]}
