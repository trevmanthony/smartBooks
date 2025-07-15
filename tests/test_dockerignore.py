"""Tests for the .dockerignore file."""

from pathlib import Path


def test_dockerignore_contains_expected_patterns():
    """Verify .dockerignore includes key directories."""
    dockerignore_path = Path(__file__).resolve().parents[1] / ".dockerignore"
    assert dockerignore_path.exists()
    content = dockerignore_path.read_text().splitlines()
    expected = {".git", "__pycache__/", ".pytest_cache/", "tests/", "venv/", ".venv/"}
    for pattern in expected:
        assert pattern in content
