# Workflows Management

Manage GitHub Actions workflows in your `.github/workflows/` directory.

## Overview

Workflows are **bundled with the package**. When you install `marty-cli`, you get a set of pre-defined workflows. To get new or updated workflows, simply update the package.

```bash
# Install
pip install marty-cli

# Get new workflows
pip install -U marty-cli
```

## Commands

### Add

Add a bundled workflow to your project.

```bash
marty-cli workflow add <name>
```

**Arguments:**
- `name` - Name of the bundled workflow to add

**Examples:**
```bash
# Add the pr-review workflow
marty-cli workflow add pr-review

# Add the ci workflow
marty-cli workflow add ci
```

### Update

Update a workflow to the latest version from the package.

```bash
marty-cli workflow update <name>
```

**Arguments:**
- `name` - Name of the workflow to update

**Examples:**
```bash
marty-cli workflow update pr-review
```

### Delete

Remove a workflow from your project.

```bash
marty-cli workflow delete <name>
```

**Arguments:**
- `name` - Name of the workflow to delete

**Examples:**
```bash
marty-cli workflow delete pr-review
```

### List

List available bundled workflows and installed workflows.

```bash
marty-cli workflow list
```

**Output:**
- **Available**: Bundled workflows from the package (can be added)
- **Installed**: Workflows already in `.github/workflows/`

## Bundled Workflows

The package includes the following workflows:

| Name | Description |
|------|-------------|
| `pr-review` | Pull request review workflow |
| `ci` | Continuous integration workflow |

## Options

These options are available for all workflow commands:

| Option | Description |
|--------|-------------|
| `--help` | Show help message |
| `--path` | Custom path to `.github/workflows/` (defaults to current directory) |

## Notes

- Workflow files are copied to `.github/workflows/<name>.yml`
- Use `--force` flag with `add` to overwrite existing workflows without confirmation
