# ADR: Maintain append-only audit log

## Context
The audit log at `logs/actions.jsonl` tracks changes to the codebase. During merges duplicate entries can appear, which makes chronological processing harder.

## Decision
We use a Python utility `scripts/cleanup_actions_log.py` to deduplicate entries and sort them by ISO 8601 timestamp. This keeps the log append-only and deterministic for parsing tools.

## Links
- https://jsonlines.org/
- https://docs.python.org/3/library/logging.html
