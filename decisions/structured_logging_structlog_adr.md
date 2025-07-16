# ADR: Adopt structlog for JSON logging

## Context
We currently use Python's built-in logging for miscellaneous messages but lack a consistent structured format. Structured logs facilitate easier filtering and analysis in production. structlog is a well-maintained library focused on structured logging and integrates with the standard logging module.

## Decision
We will adopt the `structlog` library to produce JSON-formatted logs across the application. This allows adding contextual data to log events and outputs JSON for ingestion by log processors.

## Consequences
- Adds `structlog` as a project dependency.
- Requires initializing structlog early in application startup.
- Existing log statements should be migrated to use the new API.

## Links
- https://www.structlog.org/en/stable/why.html
- https://www.structlog.org/en/stable/getting-started.html
