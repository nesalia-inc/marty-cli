"""Tests for workflow_manager."""

import pytest

from marty_cli.workflow_manager import WorkflowManager


class TestWorkflowManager:
    """Tests for WorkflowManager class."""

    @pytest.fixture
    def target_path(self, tmp_path):
        """Return the .github/workflows path inside tmp_path."""
        return tmp_path / ".github" / "workflows"

    def test_get_bundled_workflows(self):
        """Test getting bundled workflows."""
        manager = WorkflowManager()
        bundled = manager.get_bundled_workflows()
        assert isinstance(bundled, list)
        assert "issue-discussion" in bundled

    def test_get_installed_workflows_empty(self, target_path):
        """Test getting installed workflows when directory doesn't exist."""
        manager = WorkflowManager(target_path)
        installed = manager.get_installed_workflows()
        assert installed == []

    def test_get_installed_workflows_with_files(self, target_path):
        """Test getting installed workflows when directory exists."""
        target_path.mkdir(parents=True)
        (target_path / "test.yml").touch()
        (target_path / "another.yml").touch()

        manager = WorkflowManager(target_path)
        installed = manager.get_installed_workflows()

        assert "test" in installed
        assert "another" in installed

    def test_add_workflow_success(self, target_path):
        """Test adding a workflow successfully."""
        target_path.mkdir(parents=True)

        manager = WorkflowManager(target_path)
        result = manager.add_workflow("issue-discussion")

        assert result is True
        assert (target_path / "issue-discussion.yml").exists()

    def test_add_workflow_not_found(self, target_path):
        """Test adding a workflow that doesn't exist in bundled."""
        target_path.mkdir(parents=True)

        manager = WorkflowManager(target_path)
        result = manager.add_workflow("nonexistent")

        assert result is False

    def test_update_workflow_success(self, target_path):
        """Test updating an installed workflow."""
        target_path.mkdir(parents=True)
        (target_path / "issue-discussion.yml").write_text("old content")

        manager = WorkflowManager(target_path)
        result = manager.update_workflow("issue-discussion")

        assert result is True

    def test_update_workflow_not_installed(self, target_path):
        """Test updating a workflow that isn't installed."""
        target_path.mkdir(parents=True)

        manager = WorkflowManager(target_path)
        result = manager.update_workflow("issue-discussion")

        assert result is False

    def test_update_workflow_not_bundled(self, target_path):
        """Test updating a workflow that isn't in bundled."""
        target_path.mkdir(parents=True)
        (target_path / "custom.yml").touch()

        manager = WorkflowManager(target_path)
        result = manager.update_workflow("custom")

        assert result is False

    def test_delete_workflow_success(self, target_path):
        """Test deleting an installed workflow."""
        target_path.mkdir(parents=True)
        (target_path / "issue-discussion.yml").touch()

        manager = WorkflowManager(target_path)
        result = manager.delete_workflow("issue-discussion")

        assert result is True
        assert not (target_path / "issue-discussion.yml").exists()

    def test_delete_workflow_not_installed(self, target_path):
        """Test deleting a workflow that isn't installed."""
        target_path.mkdir(parents=True)

        manager = WorkflowManager(target_path)
        result = manager.delete_workflow("issue-discussion")

        assert result is False

    def test_add_workflow_creates_directory(self, target_path):
        """Test that add_workflow creates the directory if it doesn't exist."""
        manager = WorkflowManager(target_path)
        result = manager.add_workflow("issue-discussion")

        assert result is True
        assert (target_path / "issue-discussion.yml").exists()
