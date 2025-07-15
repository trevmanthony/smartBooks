# ADR: FastAPI Jinja2 Templates and File Uploads

## Context
We need to serve HTML using Jinja2 templates and handle PDF and CSV uploads.

## Decision
Use FastAPI's built-in `Jinja2Templates` utility to render templates located in a `templates/` directory. Handle file uploads with `UploadFile` objects and validate extensions.

## Links
- [FastAPI Templates Documentation](https://fastapi.tiangolo.com/advanced/templates/)
- [FastAPI File Uploads](https://fastapi.tiangolo.com/tutorial/request-files/)
