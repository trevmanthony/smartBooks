# ADR: Use Celery worker microservice for Document AI pipeline

## Context
Running OCR via Google Document AI and the o4-mini LLM can take several seconds. FastAPI `BackgroundTasks` work for short operations but lack retry logic and distributed execution. We want a more reliable way to process documents without blocking the API server.

## Decision
Move the Document AI and o4-mini processing into a dedicated Celery worker. The main FastAPI app will enqueue jobs on a message broker (e.g., Redis) and return immediately. Celery workers will fetch tasks and run the pipeline asynchronously.

## Links
- https://docs.celeryq.dev/en/stable/getting-started/introduction.html
- https://testdriven.io/blog/fastapi-celery/
