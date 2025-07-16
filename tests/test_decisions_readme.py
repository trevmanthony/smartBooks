"""Tests for decisions README updates."""

from pathlib import Path


def test_docker_pylint_error_marked_superseded():
    """The README should note that docker_pylint_error_adr is superseded."""
    readme = Path(__file__).resolve().parents[1] / "decisions" / "README.md"
    content = readme.read_text()
    expected = (
        "[docker_pylint_error_adr.md](docker_pylint_error_adr.md)"
        " — *superseded by* [include_tests_in_docker_adr.md](include_tests_in_docker_adr.md)"
    )
    assert expected in content


def test_docker_pylint_adr_contains_note():
    """ADR file itself should contain superseded status note."""
    adr_path = (
        Path(__file__).resolve().parents[1] / "decisions" / "docker_pylint_error_adr.md"
    )
    content = adr_path.read_text()
    assert "superseded" in content
    assert "include_tests_in_docker_adr.md" in content


def test_structured_logging_adr_indexed():
    """README should list the structured logging ADR."""
    readme = Path(__file__).resolve().parents[1] / "decisions" / "README.md"
    content = readme.read_text()
    assert "structured_logging_structlog_adr.md" in content


def test_structured_logging_adr_mentions_structlog():
    """ADR file should mention structlog."""
    adr_path = (
        Path(__file__).resolve().parents[1]
        / "decisions"
        / "structured_logging_structlog_adr.md"
    )
    content = adr_path.read_text().lower()
    assert "structlog" in content
