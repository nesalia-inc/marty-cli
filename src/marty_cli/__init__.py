"""marty-cli - CLI application."""

import os
from pathlib import Path

import typer

from marty_cli.workflow_manager import WorkflowManager

app = typer.Typer(help="marty-cli - A CLI application")

workflow_app = typer.Typer(help="Manage GitHub workflows")
app.add_typer(workflow_app, name="workflow")


@workflow_app.command("add")
def workflow_add(
    name: str,
    path: Path = typer.Option(None, "--path", help="Target directory"),
) -> None:
    """Add a workflow to your project."""
    target_path = (path or Path(os.getcwd())) / ".github" / "workflows"
    manager = WorkflowManager(target_path)

    if manager.add_workflow(name):
        typer.echo(f"Added workflow: {name}")
    else:
        typer.echo(f"Error: Workflow '{name}' not found in bundled workflows")
        raise typer.Exit(code=1)


@workflow_app.command("update")
def workflow_update(
    name: str,
    path: Path = typer.Option(None, "--path", help="Target directory"),
) -> None:
    """Update an existing workflow."""
    target_path = (path or Path(os.getcwd())) / ".github" / "workflows"
    manager = WorkflowManager(target_path)

    if manager.update_workflow(name):
        typer.echo(f"Updated workflow: {name}")
    else:
        typer.echo(f"Error: Workflow '{name}' is not installed or not found in bundled workflows")
        raise typer.Exit(code=1)


@workflow_app.command("delete")
def workflow_delete(
    name: str,
    path: Path = typer.Option(None, "--path", help="Target directory"),
) -> None:
    """Delete a workflow from your project."""
    target_path = (path or Path(os.getcwd())) / ".github" / "workflows"
    manager = WorkflowManager(target_path)

    if manager.delete_workflow(name):
        typer.echo(f"Deleted workflow: {name}")
    else:
        typer.echo(f"Error: Workflow '{name}' is not installed")
        raise typer.Exit(code=1)


@workflow_app.command("list")
def workflow_list(
    path: Path = typer.Option(None, "--path", help="Target directory"),
) -> None:
    """List available and installed workflows."""
    target_path = (path or Path(os.getcwd())) / ".github" / "workflows"
    manager = WorkflowManager(target_path)

    bundled = manager.get_bundled_workflows()
    installed = manager.get_installed_workflows()

    typer.echo("Available (bundled):")
    for wf in bundled:
        status = "installed" if wf in installed else "not installed"
        typer.echo(f"  - {wf} ({status})")

    typer.echo("\nInstalled:")
    if installed:
        for wf in installed:
            typer.echo(f"  - {wf}")
    else:
        typer.echo("  (none)")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
