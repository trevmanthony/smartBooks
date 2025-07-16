# ADR: Use Celery with Redis for Background Tasks

## Context
Large file uploads can slow down HTTP responses if processed synchronously. We need an asynchronous
worker to handle storing files outside the FastAPI request cycle.

## Decision
Integrate [Celery](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html)
with a Redis broker. The `/upload` endpoint will queue a `store_file` task that writes the bytes to
SQLite. Tests run Celery in eager mode to avoid requiring a broker during CI.

## Links
- <https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html>
- <https://testdriven.io/blog/fastapi-celery/>
