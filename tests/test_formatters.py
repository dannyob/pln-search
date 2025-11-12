"""Tests for output formatters."""

import sys
from io import StringIO
from pln_search.formatters import OutputFormatter
from pln_search.models import Member, Team, Project


def test_formatter_auto_detection_tty(monkeypatch):
    """Test auto format detection for TTY."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    formatter = OutputFormatter(format_type="auto")
    assert formatter.format_type == "rich"


def test_formatter_auto_detection_pipe(monkeypatch):
    """Test auto format detection for pipe."""
    monkeypatch.setattr(sys.stdout, "isatty", lambda: False)

    formatter = OutputFormatter(format_type="auto")
    assert formatter.format_type == "plain"


def test_formatter_explicit_json():
    """Test explicit JSON format."""
    formatter = OutputFormatter(format_type="json")
    assert formatter.format_type == "json"


def test_format_members_json():
    """Test JSON formatting for members."""
    from unittest.mock import patch

    members = [
        Member(
            uid="m1",
            name="John Doe",
            email="john@example.com",
            bio="Engineer",
            location="SF",
            skills=["Python"],
            github_handler="john",
        )
    ]

    formatter = OutputFormatter(format_type="json")

    with patch("builtins.print") as mock_print:
        formatter.format_members(members)
        output = mock_print.call_args[0][0]
        assert "John Doe" in output
        assert "m1" in output


def test_format_members_plain():
    """Test plain text formatting for members."""
    from unittest.mock import patch

    members = [
        Member(
            uid="m1",
            name="Jane Doe",
            email=None,
            bio=None,
            location="NYC",
            skills=["Rust", "Go"],
            github_handler=None,
        )
    ]

    formatter = OutputFormatter(format_type="plain")

    with patch("builtins.print") as mock_print:
        formatter.format_members(members)
        # Check print was called with member info
        calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join(calls)
        assert "Jane Doe" in output
        assert "NYC" in output
