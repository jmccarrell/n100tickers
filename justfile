set dotenv-load

ARGS_TEST := env("_UV_RUN_ARGS_TEST", "")


@_:
    just --list


# Run tests
[group('qa')]
test *args:
    uv run {{ ARGS_TEST }} -m pytest {{ args }}

_cov *args:
    uv run -m coverage {{ args }}

# Run tests and measure coverage
[group('qa')]
@cov:
    just _cov erase
    just _cov run -m pytest tests
    just _cov combine
    just _cov report
    just _cov html

# Run linters
[group('qa')]
lint:
    uvx ruff check
    uvx ruff format --check

# Fix ruff issues + format
[group('qa')]
fmt:
    uvx ruff check --fix
    uvx ruff format

# Check types
[group('qa')]
typing:
    uvx ty check --python .venv src

# Perform all checks
[group('qa')]
check-all: lint cov typing


# Update dependencies
[group('lifecycle')]
update:
    uv sync --upgrade

# Ensure project virtualenv is up to date
[group('lifecycle')]
install:
    uv sync

# Remove temporary files
[group('lifecycle')]
clean:
    rm -rf .venv .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
    rm -rf docs/_build
    find . -type d -name "__pycache__" -exec rm -r {} +
    find . -type d -name ".pytest_cache" -exec rm -r {} +

# Recreate project virtualenv from nothing
[group('lifecycle')]
fresh: clean install

# Dispatch the Release workflow against main: just release 2026.2.1
[group('lifecycle')]
release VERSION:
    #!/usr/bin/env bash
    set -euo pipefail
    if ! echo "{{ VERSION }}" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
        echo "error: VERSION must be CalVer (e.g. 2026.2.0), got '{{ VERSION }}'"
        exit 1
    fi
    gh workflow run release.yml --ref main -f version={{ VERSION }}
    echo "dispatched; follow it with: gh run watch \$(gh run list -w Release -L1 --json databaseId --jq '.[0].databaseId')"
