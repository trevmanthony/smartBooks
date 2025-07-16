"""Tests for cleanup_actions_log utility."""

import json

import scripts.cleanup_actions_log as cleanup


def test_cleanup_removes_duplicates_and_sorts(tmp_path):
    """Deduplicates and sorts log entries."""
    sample = tmp_path / "actions.jsonl"
    lines = [
        {"timestamp": "2025-07-15T21:06:40Z", "action": "A", "ticket_id": "t"},
        {"timestamp": "2025-07-15T20:00:00Z", "action": "B", "ticket_id": "t"},
        {"timestamp": "2025-07-15T21:06:40Z", "action": "A", "ticket_id": "t"},
    ]
    with sample.open("w", encoding="utf-8") as handle:
        for entry in lines:
            handle.write(json.dumps(entry) + "\n")

    cleanup.cleanup(sample)

    entries = [json.loads(l) for l in sample.read_text().splitlines()]
    assert entries == [
        {"timestamp": "2025-07-15T20:00:00Z", "action": "B", "ticket_id": "t"},
        {"timestamp": "2025-07-15T21:06:40Z", "action": "A", "ticket_id": "t"},
    ]
