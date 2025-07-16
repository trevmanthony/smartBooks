# ADR: Offload SQLite operations with run_in_threadpool

## Context
FastAPI endpoints in `app.py` perform SQLite writes and deletes using the
standard `sqlite3` library. These blocking calls can stall the event loop when
executed directly inside `async` path operations.

## Decision
Use FastAPI's `run_in_threadpool` utility to execute all SQLite write and delete
operations in a background thread. This keeps the event loop responsive while
avoiding a switch to a dedicated async database library.

## Links
- https://fastapi.tiangolo.com/async/
- https://github.com/encode/starlette/blob/master/docs/threadpool.md
