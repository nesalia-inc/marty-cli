"""Workflow manager for handling bundled and installed workflows."""

import shutil
from pathlib import Path


class WorkflowManager:
    """Manages bundled and installed GitHub workflows."""

    def __init__(self, target_path: Path | None = None) -> None:
        """Initialize the workflow manager.

        Args:
            target_path: Path to the target .github/workflows directory.
                        Defaults to current directory.
        """
        self.target_path = target_path or Path.cwd() / ".github" / "workflows"
        self.bundled_path = Path(__file__).parent / "workflows"

    def get_bundled_workflows(self) -> list[str]:
        """Get list of available bundled workflows.

        Returns:
            List of workflow names (without .yml extension).
        """
        if not self.bundled_path.exists():
            return []
        return [f.stem for f in self.bundled_path.glob("*.yml")]

    def get_installed_workflows(self) -> list[str]:
        """Get list of installed workflows.

        Returns:
            List of workflow names (without .yml extension).
        """
        if not self.target_path.exists():
            return []
        return [f.stem for f in self.target_path.glob("*.yml")]

    def add_workflow(self, name: str) -> bool:
        """Add a bundled workflow to the project.

        Args:
            name: Name of the workflow to add.

        Returns:
            True if successful, False otherwise.
        """
        bundled_workflows = self.get_bundled_workflows()
        if name not in bundled_workflows:
            return False

        source = self.bundled_path / f"{name}.yml"
        self.target_path.mkdir(parents=True, exist_ok=True)
        dest = self.target_path / f"{name}.yml"
        shutil.copy2(source, dest)
        return True

    def update_workflow(self, name: str) -> bool:
        """Update an installed workflow from the bundled version.

        Args:
            name: Name of the workflow to update.

        Returns:
            True if successful, False otherwise.
        """
        installed_workflows = self.get_installed_workflows()
        bundled_workflows = self.get_bundled_workflows()

        if name not in installed_workflows:
            return False
        if name not in bundled_workflows:
            return False

        source = self.bundled_path / f"{name}.yml"
        dest = self.target_path / f"{name}.yml"
        shutil.copy2(source, dest)
        return True

    def delete_workflow(self, name: str) -> bool:
        """Delete an installed workflow.

        Args:
            name: Name of the workflow to delete.

        Returns:
            True if successful, False otherwise.
        """
        installed_workflows = self.get_installed_workflows()
        if name not in installed_workflows:
            return False

        workflow_file = self.target_path / f"{name}.yml"
        workflow_file.unlink()
        return True
