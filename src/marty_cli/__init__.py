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
    name: str | None = None,
    all: bool = typer.Option(False, "--all", "-a", help="Add all bundled workflows"),
    path: Path = typer.Option(None, "--path", help="Target directory"),
) -> None:
    """Add a workflow to your project."""
    target_path = (path or Path(os.getcwd())) / ".github" / "workflows"
    manager = WorkflowManager(target_path)

    if all:
        bundled = manager.get_bundled_workflows()
        installed = manager.get_installed_workflows()
        for wf in bundled:
            if wf not in installed:
                if manager.add_workflow(wf):
                    typer.echo(f"Added workflow: {wf}")
                else:
                    typer.echo(f"Error: Failed to add {wf}")
        typer.echo("Done. Added all workflows.")
    elif name:
        if manager.add_workflow(name):
            typer.echo(f"Added workflow: {name}")
        else:
            typer.echo(f"Error: Workflow '{name}' not found in bundled workflows")
            raise typer.Exit(code=1)
    else:
        typer.echo("Error: Specify a workflow name or use --all")
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

    if bundled:
        typer.echo("Available:")
        for wf in bundled:
            status = "(installed)" if wf in installed else "(not installed)"
            typer.echo(f"  - {wf} {status}")
    else:
        typer.echo("No bundled workflows available.")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
