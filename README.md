<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="public/marty.png">
    <source media="(prefers-color-scheme: light)" srcset="public/marty.png">
    <img src="public/marty.png" alt="marty-cli" width="150" height="150" style="border-radius: 50%;">
  </picture>
</p>

<h1 align="center">marty-cli</h1>

<p align="center">
  <a href="https://pypi.org/project/marty-cli/">
    <img src="https://img.shields.io/pypi/v/marty-cli" alt="PyPI Version">
  </a>
  <a href="https://pypi.org/project/marty-cli/">
    <img src="https://img.shields.io/pypi/pyversions/marty-cli?logo=python" alt="Python">
  </a>
  <a href="https://github.com/nesalia-inc/marty-cli/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/nesalia-inc/marty-cli/ruff?label=tests" alt="Tests">
  </a>
  <a href="https://github.com/nesalia-inc/marty-cli/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/nesalia-inc/marty-cli" alt="License">
  </a>
</p>

> CLI tool to manage Marty actions workflows. Add bundled workflows with one command.

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

## Getting Started

```bash
# Quick start - add all workflows
marty-cli workflow add --all

# Or add specific workflows
marty-cli workflow add issue-discussion
marty-cli workflow add pr-review
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

- **Nesalia Inc.**

## Security

If you discover any security vulnerabilities, please send an e-mail to security@nesalia.com.

## License

MIT License - see the [LICENSE](LICENSE) file for details.
