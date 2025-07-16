# ADR: Implement Celery worker microservice

## Context
We decided to move long running OCR and LLM processing out of FastAPI
background tasks. Celery provides retry logic and distributed workers.
This ADR records the resources consulted when wiring Celery into the
existing application.

## Decision
Create `worker.py` defining a Celery app and `process_file_task`. The
`/process/{id}` endpoint now calls `process_file_task.delay()` instead of
FastAPI `BackgroundTasks`. A `USE_REAL_PIPELINE` environment variable
switches between stub and real pipeline implementations.

## Links
- https://docs.celeryq.dev/en/stable/getting-started/introduction.html
- https://docs.celeryq.dev/en/stable/userguide/tasks.html
- https://testdriven.io/blog/fastapi-celery/
