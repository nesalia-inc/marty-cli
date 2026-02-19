"""Tests for marty-cli."""

from typer.testing import CliRunner

from marty_cli import app

runner = CliRunner()


def test_hello():
    """Test hello command."""
    result = runner.invoke(app, ["hello", "World"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.stdout
