# ADR: Persist pipeline results in the database

## Context
The Celery worker currently returns OCR+LLM results directly without
saving them. Persisting results enables the UI to fetch the structured
JSON later and avoids recomputation.

## Decision
Create a new `extractions` table using SQLModel with an async
`AsyncSession`. The Celery task will store the JSON returned by the
pipeline in this table keyed by the uploaded file ID.

## Links
- https://sqlmodel.tiangolo.com/async/
- https://docs.celeryq.dev/en/stable/getting-started/next-steps.html#keeping-results
