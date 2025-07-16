#!/usr/bin/env python3
"""Utility to deduplicate and sort the audit log."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_entries(path: Path) -> list[dict[str, str]]:
    """Load JSON entries from the given path."""
    entries: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            entries.append(json.loads(line))
    return entries


def dedupe_sort(entries: list[dict[str, str]]) -> list[dict[str, str]]:
    """Return entries deduplicated and sorted by timestamp."""
    unique = {}
    for entry in entries:
        key = (entry["timestamp"], entry["action"], entry["ticket_id"])
        unique[key] = entry
    return sorted(unique.values(), key=lambda e: e["timestamp"])  # type: ignore[index]


def save_entries(entries: list[dict[str, str]], path: Path) -> None:
    """Write entries back to JSON Lines file."""
    with path.open("w", encoding="utf-8") as handle:
        for entry in entries:
            line = json.dumps(
                {
                    "timestamp": entry["timestamp"],
                    "action": entry["action"],
                    "ticket_id": entry["ticket_id"],
                }
            )
            handle.write(f"{line}\n")


def cleanup(path: Path) -> None:
    """Load, dedupe, sort, and save log entries."""
    entries = load_entries(path)
    entries = dedupe_sort(entries)
    save_entries(entries, path)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        type=Path,
        default=Path("logs/actions.jsonl"),
        nargs="?",
        help="Path to log file",
    )
    args = parser.parse_args()
    cleanup(args.path)


if __name__ == "__main__":
    main()
