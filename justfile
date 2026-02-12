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
    find . -type d -name "__pycache__" -exec rm -r {} +

# Recreate project virtualenv from nothing
[group('lifecycle')]
fresh: clean install

# Cut a release: just release 2026.2.1
[group('lifecycle')]
release VERSION:
    #!/usr/bin/env bash
    set -euo pipefail
    if ! echo "{{ VERSION }}" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
        echo "error: VERSION must be CalVer (e.g. 2026.2.0), got '{{ VERSION }}'"
        exit 1
    fi
    if [ -n "$(git status --porcelain)" ]; then
        echo "error: uncommitted changes — commit or stash first"
        exit 1
    fi
    sed -i.bak 's/^version = ".*"/version = "{{ VERSION }}"/' pyproject.toml && rm pyproject.toml.bak
    git add pyproject.toml
    git commit -m "release v{{ VERSION }}"
    git tag -a "v{{ VERSION }}" -m "v{{ VERSION }}"
    git push
    git push origin "v{{ VERSION }}"
