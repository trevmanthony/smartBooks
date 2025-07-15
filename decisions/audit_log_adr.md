# ADR: Use JSON Lines for audit log

## Context
We maintain an audit log at `logs/actions.jsonl` to record code and data changes. JSON Lines provides a simple, newline-delimited format that is easy to append and parse.

## Decision
Store each log entry as a single JSON object per line with fields `timestamp`, `action`, and `ticket_id`. Entries are kept in ascending timestamp order with no blank lines to ensure deterministic processing.

## Links
- https://jsonlines.org/
- https://docs.python.org/3/library/logging.html
