# ADR: Adopt SQLModel with SQLAlchemy Async Extension

## Context
The project currently uses SQLite through the standard `sqlite3` library and `run_in_threadpool` to avoid blocking the event loop. The TODO list asked to evaluate asynchronous database options. We considered using SQLModel with SQLAlchemy's async extension, SQLAlchemy ORM directly with `AsyncSession`, and raw SQL drivers like `aiosqlite`.

## Decision
We will migrate the data layer to SQLModel using SQLAlchemy's `AsyncSession` support. This keeps the Pydantic-style models that SQLModel provides while leveraging fully asynchronous database operations available in SQLAlchemy 2.0.
A follow-up task will implement the migration and update all endpoints and tests.

## Links
- https://github.com/tiangolo/sqlmodel/pull/1347
- https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- https://fastapi.tiangolo.com/advanced/async-sql-databases/
