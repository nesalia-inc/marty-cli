"""marty-cli - CLI application."""

import typer

app = typer.Typer(help="marty-cli - A CLI application")

workflow_app = typer.Typer(help="Manage GitHub workflows")
app.add_typer(workflow_app, name="workflow")


@workflow_app.command("add")
def workflow_add(name: str) -> None:
    """Add a workflow to your project."""
    print(f"Adding workflow: {name}")


@workflow_app.command("update")
def workflow_update(name: str) -> None:
    """Update an existing workflow."""
    print(f"Updating workflow: {name}")


@workflow_app.command("delete")
def workflow_delete(name: str) -> None:
    """Delete a workflow from your project."""
    print(f"Deleting workflow: {name}")


@workflow_app.command("list")
def workflow_list() -> None:
    """List available and installed workflows."""
    print("Listing workflows...")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
