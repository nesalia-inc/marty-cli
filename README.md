# marty-cli

CLI tool to manage Marty actions workflows. Add bundled workflows with one command.

## Requirements

- Python 3.12+
- uv (recommended) or pip

## Installation

```bash
# Install marty-cli
pip install marty-cli

# Or using uv
uv pip install marty-cli
```

## Usage

```bash
# List available workflows
marty-cli workflow list

# Add a workflow
marty-cli workflow add issue-discussion

# Add all bundled workflows
marty-cli workflow add --all

# Update a workflow
marty-cli workflow update issue-discussion

# Update all installed workflows
marty-cli workflow update --all

# Delete a workflow
marty-cli workflow delete issue-discussion

# Use custom path
marty-cli workflow add issue-discussion --path /my/project
```

## Available Workflows

- `issue-discussion` - Marty AI responds to GitHub issues when mentioned
- `issue-implementation` - Marty implements features when asked ("implement")
- `issue-triage` - Auto triage new issues
- `pr-discussion` - Marty discusses in PRs when mentioned
- `pr-fix` - Marty fixes PR issues when asked ("fix")
- `pr-review` - Auto review PRs

## Development

```bash
# Clone and install
git clone https://github.com/nesalia-inc/marty-cli.git
cd marty-cli

# Install dependencies
uv sync --extra dev

# Run linter
ruff check .

# Run type checker
mypy src

# Run tests
pytest
```

## License

MIT
