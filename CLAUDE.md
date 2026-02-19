# Marty CLI Development Guide

This document explains the development and release workflow for marty-cli.

## Versioning

We use [Semantic Versioning (SemVer)](https://semver.org/):

- **MAJOR** (1.0.0) - Breaking changes
- **MINOR** (0.1.0) - New features (backward compatible)
- **PATCH** (0.0.1) - Bug fixes

## Release Workflow

### Prerequisites

1. **PyPI Token** - Stored as GitHub secret (`PYPI_TOKEN`)
2. **Trusted Publisher** - Configured on PyPI (optional, token works fine)

### Release Process

```bash
# 1. Bump version (choose one)
uv version 0.1.9          # Specific version
uv version --bump minor  # 0.1.8 → 0.2.0
uv version --bump patch  # 0.1.8 → 0.1.9

# 2. Commit and push
git add pyproject.toml
git commit -m "Bump version to X.Y.Z"
git push

# 3. Create GitHub release (triggers PyPI publish)
gh release create vX.Y.Z --title "vX.Y.Z" --notes "Release notes"
```

### What Happens

1. `git push` triggers CI workflows (Ruff, Mypy, Pytest)
2. Creating a GitHub release triggers the Release workflow
3. Release workflow:
   - Builds the package: `uv build --no-sources`
   - Publishes to PyPI: `uv publish --token ${{ secrets.PYPI_TOKEN }}`

### CI/CD Workflows

| Workflow | Trigger | Description |
|----------|---------|-------------|
| `ruff.yml` | push/PR | Linting |
| `mypy.yml` | push/PR | Type checking |
| `pytest.yml` | push/PR | Run tests |
| `release.yml` | GitHub release | Publish to PyPI |

## Adding New Features

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Implement the feature
3. Add tests if needed
4. Commit and push
5. Create a PR
6. Merge to main
7. Bump version and create release

## Adding Bundled Workflows

To add a new bundled workflow:

1. Create the YAML file in `src/marty_cli/workflows/`
2. Update documentation in `docs/features/workflows.md`
3. Bump version and release
