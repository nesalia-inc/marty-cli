"""Tests for CLI commands."""

import pytest
from typer.testing import CliRunner
from unittest.mock import patch

from marty_cli import app, main


@pytest.fixture
def runner():
    """Return CliRunner instance."""
    return CliRunner()


@pytest.fixture
def project_path(tmp_path):
    """Return a project directory path."""
    return tmp_path


class TestWorkflowList:
    """Tests for workflow list command."""

    def test_list_empty(self, runner, project_path):
        """Test list with no installed workflows."""
        result = runner.invoke(app, ["workflow", "list", "--path", str(project_path)])
        assert result.exit_code == 0
        assert "Available:" in result.stdout
        assert "issue-discussion" in result.stdout

    def test_list_with_installed(self, runner, project_path):
        """Test list with installed workflows."""
        workflows_dir = project_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        (workflows_dir / "issue-discussion.yml").touch()

        result = runner.invoke(app, ["workflow", "list", "--path", str(project_path)])
        assert result.exit_code == 0
        assert "(installed)" in result.stdout

    def test_list_no_bundled(self, runner, project_path):
        """Test list when no bundled workflows available."""
        with patch("marty_cli.WorkflowManager.get_bundled_workflows", return_value=[]):
            result = runner.invoke(app, ["workflow", "list", "--path", str(project_path)])
            assert result.exit_code == 0
            assert "No bundled workflows available." in result.stdout


class TestWorkflowAdd:
    """Tests for workflow add command."""

    def test_add_success(self, runner, project_path):
        """Test adding a workflow successfully."""
        result = runner.invoke(app, ["workflow", "add", "--name", "issue-discussion", "--path", str(project_path)])
        assert result.exit_code == 0
        assert "Added workflow: issue-discussion" in result.stdout
        assert (project_path / ".github" / "workflows" / "issue-discussion.yml").exists()

    def test_add_not_found(self, runner, project_path):
        """Test adding a workflow that doesn't exist."""
        result = runner.invoke(app, ["workflow", "add", "--name", "nonexistent", "--path", str(project_path)])
        assert result.exit_code == 1
        assert "not found in bundled" in result.stdout

    def test_add_all(self, runner, project_path):
        """Test adding all workflows."""
        result = runner.invoke(app, ["workflow", "add", "--all", "--path", str(project_path)])
        assert result.exit_code == 0
        assert "Done" in result.stdout

    def test_add_no_args(self, runner, project_path):
        """Test add with no arguments."""
        result = runner.invoke(app, ["workflow", "add", "--path", str(project_path)])
        assert result.exit_code == 1


class TestWorkflowUpdate:
    """Tests for workflow update command."""

    def test_update_success(self, runner, project_path):
        """Test updating a workflow successfully."""
        workflows_dir = project_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        (workflows_dir / "issue-discussion.yml").write_text("old")

        result = runner.invoke(app, ["workflow", "update", "--name", "issue-discussion", "--path", str(project_path)])
        assert result.exit_code == 0
        assert "Updated workflow" in result.stdout

    def test_update_not_installed(self, runner, project_path):
        """Test updating a workflow that isn't installed."""
        result = runner.invoke(app, ["workflow", "update", "--name", "issue-discussion", "--path", str(project_path)])
        assert result.exit_code == 1

    def test_update_all(self, runner, project_path):
        """Test updating all workflows."""
        workflows_dir = project_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        (workflows_dir / "issue-discussion.yml").write_text("old")

        result = runner.invoke(app, ["workflow", "update", "--all", "--path", str(project_path)])
        assert result.exit_code == 0

    def test_update_no_args(self, runner, project_path):
        """Test update with no arguments."""
        result = runner.invoke(app, ["workflow", "update", "--path", str(project_path)])
        assert result.exit_code == 1

    def test_update_all_nothing_to_update(self, runner, project_path):
        """Test update --all when no workflows to update."""
        result = runner.invoke(app, ["workflow", "update", "--all", "--path", str(project_path)])
        assert result.exit_code == 0
        assert "No workflows to update." in result.stdout


class TestWorkflowDelete:
    """Tests for workflow delete command."""

    def test_delete_success(self, runner, project_path):
        """Test deleting a workflow successfully."""
        workflows_dir = project_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        (workflows_dir / "issue-discussion.yml").touch()

        result = runner.invoke(app, ["workflow", "delete", "issue-discussion", "--path", str(project_path)])
        assert result.exit_code == 0
        assert "Deleted workflow" in result.stdout
        assert not (workflows_dir / "issue-discussion.yml").exists()

    def test_delete_not_installed(self, runner, project_path):
        """Test deleting a workflow that isn't installed."""
        result = runner.invoke(app, ["workflow", "delete", "issue-discussion", "--path", str(project_path)])
        assert result.exit_code == 1
        assert "not installed" in result.stdout


class TestMain:
    """Tests for main entry point."""

    def test_main_import(self):
        """Test that main can be imported."""
        assert callable(main)

    def test_main_via_cli_runner(self, runner, project_path):
        """Test main via CliRunner (covers if __name__ == '__main__')."""
        # This tests the main entry point
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "marty-cli" in result.stdout
