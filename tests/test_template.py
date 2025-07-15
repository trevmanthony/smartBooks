"""Regression tests for HTML template integrity."""

from pathlib import Path
from bs4 import BeautifulSoup


def test_index_html_structure():
    """index.html should end with closing tags and contain the success message."""
    html_path = Path(__file__).resolve().parents[1] / "templates" / "index.html"
    html_content = html_path.read_text()
    soup = BeautifulSoup(html_content, "html.parser")

    assert soup.html is not None
    assert soup.body is not None
    assert html_content.rstrip().endswith("</html>")
    assert "Files uploaded successfully!" in html_content
