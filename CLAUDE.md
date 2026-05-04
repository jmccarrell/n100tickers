# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project provides date-centric access to NASDAQ 100 index membership over time. The primary API is `tickers_as_of(year, month, day)` which returns a frozenset of ticker symbols that were in the index on the specified date. Coverage spans from January 1, 2015 through at least November 15, 2025.

## Worktree Workflow

This project uses the **bare-root + worktrees** layout. The detailed flow
is documented in the `git-worktree-flow` skill (`~/.claude/skills/git-worktree-flow/SKILL.md`)
and its operational counterpart `~/.config/just/worktree.just`, wired into
this project's justfile as `mod wt`.

- **Verify gate before fixup or close:** `just check-all` (lint + cov + typing).
  The `wt::*` recipes do not call back into project recipes; run verification yourself.
- **Recipes available** (full list: `just wt`):
  - `just wt::new <feature>` — create sibling worktree on a new branch
  - `just wt::track <feature>` — track an existing remote branch on this machine
  - `just wt::status` — read-only drift report against origin
  - `just wt::fixup` — fixup staged changes against the first commit on this branch
  - `just wt::squash` / `just wt::close` — autosquash; `close` also drops `TASK.md`
  - `just wt::clean <feature>` — remove a merged worktree and delete its branch
- **Pre-push warning hook** — install per-machine with `just install-fixup-hook`.
  Canonical source: `hooks/pre-push` (tracked). Warns (does not block) when
  pushing a branch with unsquashed `fixup!` commits.

## Common Commands

This project uses `just` for task automation and `uv` for Python dependency management.

### Run python code
- use `uv run python` to execute python (never bare `python`/`python3`; package ops via `uv add`/`uv sync` — repo-wide rule, see top-level CLAUDE.md)

### Testing
- Run all tests: `just test`
- Run specific test: `just test tests/test_n100_2023.py`
- Run specific test function: `just test tests/test_n100_2023.py::test_year_boundary_2022_2023`
- Run tests with coverage: `just cov` (generates HTML report in `htmlcov/`)

### Code Quality
- Run linters (ruff check + format): `just lint`
- Check types: `just typing`
- Run all checks: `just check-all` (lint + cov + typing)

### Dependency Management
- Install/sync dependencies: `just install` or `uv sync`
- Update dependencies: `just update` or `uv sync --upgrade`
- Clean and reinstall: `just fresh`

### Documentation
- Sphinx docs are in `docs/`
- README is a symlink to `docs/index.rst`

## Architecture

### Core Module: `src/nasdaq_100_ticker_history/n100tickers.py`

The main function `tickers_as_of(year, month, day)` works by:
1. Loading ticker data from YAML files via `_load_tickers_from_yaml(year)` (cached with `@lru_cache`)
2. Starting with the `tickers_on_Jan_1` set for the specified year
3. Applying any index changes (union/difference operations) that occurred on or before the query date
4. Returning the result as a frozenset

### Data Model: YAML Change Files

Each year has a YAML file (`n100-ticker-changes-YYYY.yaml`) defining:
- `year`: integer year
- `tickers_on_Jan_1`: list of ticker symbols in the index on January 1st
- `changes`: optional map of ISO dates (YYYY-MM-DD) to change operations
  - `union`: tickers added to the index
  - `difference`: tickers removed from the index

Example:
```yaml
changes:
  '2025-05-19':
    difference:
      - MDB
    union:
      - SHOP
```

YAML files use StrictYAML with a defined schema (`ticker_schema`) for validation.

### Test Structure

Tests are organized by year (`test_n100_YYYY.py`). Each test file:
- Defines `num_tickers_YYYY` constant for the expected index size that year
- Tests year boundary continuity via `_test_at_year_boundary(year)` helper
- Tests individual ticker swaps via `_test_one_swap(date, removed, added, expected_count)` helper

Test helpers are defined in `tests/helpers.py`.

## Adding New Index Changes

When NASDAQ announces index changes:
1. Update the appropriate YAML file in `src/nasdaq_100_ticker_history/`
2. Add test cases in the corresponding `tests/test_n100_YYYY.py` file
3. Tests should verify the swap occurred on the correct date
4. Run `just check-all` before committing
5. Version follows CalVer format: `YYYY.minor.patch`

## Releasing

Version follows CalVer format: `YYYY.minor.patch`

### Cutting a release
1. Get the release version from the user
2. Update `pyproject.toml` with the new version
3. Update `index.rst` to the current date
4. Commit all changes
5. Run `just release VERSION` (e.g. `just release 2026.2.1`)

The `just release` recipe:
- Validates the version format
- Checks for uncommitted changes
- Updates the version in `pyproject.toml`, commits, and creates an annotated `vVERSION` tag
- Pushes the commit and tag to origin

### Automated GitHub Release
Pushing a `v*` tag triggers the `.github/workflows/release.yml` workflow, which:
1. Verifies the tag version matches `pyproject.toml`
2. Runs the test suite
3. Builds the distribution with `uv build`
4. Creates a GitHub Release with auto-generated notes and build artifacts

## Notes

- Python 3.11+ required
- Line length: 108 characters (configured in `ruff.toml`)
- Import sorting enabled via ruff (isort rules)
- Coverage settings: branch coverage enabled, shows missing lines, skips covered lines

## Agent skills

### Issue tracker

Issues live in GitHub Issues for `jmccarrell/n100tickers`, accessed via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical triage roles use their default label names (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
