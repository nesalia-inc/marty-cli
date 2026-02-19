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

# Update an installed workflow
marty-cli workflow update issue-discussion

# Delete a workflow
marty-cli workflow delete issue-discussion
```

## Available Workflows

- `issue-discussion` - Marty AI responds to GitHub issues when mentioned

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
