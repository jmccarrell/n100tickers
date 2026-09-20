# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project provides date-centric access to NASDAQ 100 index membership over time. The primary API is `tickers_as_of(year, month, day)` which returns a frozenset of ticker symbols that were in the index on the specified date. Coverage spans from February 1, 2007 through at least September 15, 2026.  Ticker symbols are point-in-time: a rename is recorded as a change event on its effective date, so a query returns the symbol that traded that day.

## Worktree Workflow

This project is a **plain clone** with sibling worktrees under
`n100tickers.worktrees/`. Worktree operations go through
[worktrunk](https://worktrunk.dev) (`wt`); see `~/.claude/CLAUDE.md` for the
full convention.

- `wt switch --create <slug>` — create branch + worktree, based on the default branch
- `wt switch <slug>` — move to an existing worktree
- `wt list` — all worktrees, with dirty/ahead/behind status
- `wt remove <slug>` — remove the worktree; delete the branch if merged

If `wt` is not on PATH, fall back to the raw equivalents — `git worktree add
../n100tickers.worktrees/<slug> -b <slug>`, `git worktree remove <path>`,
`git worktree list`.

**Verify gate before opening a PR:** `just check-all` (lint + cov + typing).

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

Version follows CalVer format: `YYYY.minor.patch`.

Releases are driven by [Release Please](https://github.com/googleapis/release-please).
Nothing is released by hand: every commit that reaches `main` is read as a
Conventional Commit, and Release Please keeps an open release PR that carries the
next version bump and the changelog entry.  Merging that PR is the release.

### Conventional Commits

The squash-merge title of every PR must be a Conventional Commit, because that
title is the only commit Release Please sees:

- `feat: ...` bumps the minor version — use this for index membership changes,
  which are the user-visible change this package exists to ship
- `fix: ...` bumps the patch version
- `feat!: ...` or a `BREAKING CHANGE:` footer bumps the major version, which here
  is the year — do not use it for ordinary work
- `docs:`, `deps:`, `ci:`, `refactor:`, `test:`, `chore:` bump nothing

A commit whose type bumps nothing produces no release PR on its own.  Only
`feat`, `fix`, and breaking changes move the version.

### Cutting a release

1. Merge work to `main` with Conventional Commit titles
2. Release Please opens or updates the release PR ("chore: release 2026.11.0")
3. Review it — it edits `pyproject.toml`, `CHANGELOG.md`, and
   `.release-please-manifest.json`
4. Merge it.  The tag `v2026.11.0`, the GitHub Release, and the attached
   `uv build` artifacts follow automatically

### The year rollover

Release Please treats the year as the semver major, so it will never roll
`2026.x` to `2027.0.0` on its own — a `feat:` in January 2027 would produce
`2026.12.0`.  Force the first release of a new year by putting
`Release-As: 2027.0.0` in the commit body, or by setting `release-as` in
`release-please-config.json` for that one release.

### The workflow

`.github/workflows/release-please.yml` runs on every push to `main`:

1. `verify` runs the test suite.  Release Please tags at merge time, so this job
   is the last gate that can stop a bad release
2. `release-please` opens/updates the release PR, or — when the merged commit was
   the release PR — creates the tag and the GitHub Release
3. `publish` runs only on an actual release: it checks out the new tag, runs
   `uv build`, and uploads `dist/*` to the release

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
