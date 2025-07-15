# ADR: Implement Purge Endpoint

## Context
The UI contained a "Purge DB" button without server-side support. To make it functional we need a backend endpoint that clears stored upload records.

## Decision
Introduce an SQLite database using Python's built-in `sqlite3` module to persist uploaded file names. Add a POST `/purge` endpoint in FastAPI that deletes all rows from the `files` table. The `purgeDatabase()` JavaScript function now calls this endpoint and displays a notification on success or failure.

## Links
- https://docs.python.org/3/library/sqlite3.html
- https://www.sqlite.org/lang_delete.html
- https://fastapi.tiangolo.com/advanced/async-sql-databases/
