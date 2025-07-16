# ADR: July 2025 Codebase Review

## Context
A review of the repository was performed to summarize the current structure and identify potential areas for improvement.

## Decision
The project uses FastAPI with Jinja2 templates and stores uploaded PDFs and CSVs in a SQLite database. CI builds a Docker image and runs Black, Pylint, and Pytest, including Selenium tests. Overall the codebase is organized with clear ADRs and test coverage.

Potential improvements include:
- Introduce Pydantic's `BaseSettings` to manage configuration via environment variables with validation.
- Evaluate using an async-friendly database layer such as SQLModel or SQLAlchemy for future scalability.

## Links
- https://docs.pydantic.dev/latest/usage/pydantic_settings/
- https://sqlite.org/whentouse.html
