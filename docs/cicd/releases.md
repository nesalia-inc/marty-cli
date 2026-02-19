# Releases

This document describes how to release a new version of marty-cli to PyPI.

## Overview

Releases are automated using GitHub Actions. When you publish a release on GitHub, the workflow automatically builds and publishes the package to PyPI.

## Prerequisites

### PyPI Trusted Publisher

1. Go to [PyPI](https://pypi.org)
2. Navigate to your project → Publishing
3. Add a new publisher:
   - **Owner**: Your GitHub username or organization
   - **Repository name**: `marty-cli`
   - **Workflow filename**: `release.yml`
   - **Environment name**: `production`

No API tokens or secrets are required!

## Release Process

### 1. Update the version

```bash
# Update to a specific version
uv version 1.0.0

# Or bump the version
uv version --bump minor
uv version --bump patch
uv version --bump major
```

This automatically updates the version in `pyproject.toml`.

### 2. Commit and tag

```bash
git add pyproject.toml
git commit -m "Bump version to 1.0.0"
git tag v1.0.0
git push origin main --tags
```

### 3. Create a release

Go to [GitHub Releases](https://github.com/nesalia-inc/marty-cli/releases) and create a new release:

- **Tag**: Select the tag you just pushed (e.g., `v1.0.0`)
- **Release title**: Version number (e.g., `v1.0.0`)
- **Description**: Add release notes (optional)

Click **Publish release**.

### 4. Wait for the workflow

The release workflow will:
1. Build the package with `uv build --no-sources`
2. Publish to PyPI with `uv publish`

Check the **Actions** tab on GitHub to monitor progress.

## Testing with TestPyPI

Before publishing to the main PyPI, you can test with TestPyPI:

1. Add TestPyPI as a trusted publisher on TestPyPI
2. Modify the workflow to use TestPyPI:
   ```bash
   uv publish --index testpypi
   ```

## Manual Release (if needed)

```bash
# Build the package
uv build --no-sources

# Publish to PyPI
uv publish

# Or publish to TestPyPI
uv publish --index testpypi
```
