# ADR: Maintain append-only audit log

## Context
The audit log at `logs/actions.jsonl` tracks changes to the codebase using the JSON Lines format. During merges duplicate entries can appear, which makes chronological processing harder and can break streaming parsers that expect strictly ordered records.

## Decision
We use a Python utility `scripts/cleanup_actions_log.py` to deduplicate entries and sort them by ISO&nbsp;8601 timestamp. This keeps the log append-only and deterministic for parsing tools while adhering to the JSON Lines specification and Python logging best practices.

## Links
- https://jsonlines.org/
- https://docs.python.org/3/library/logging.html
