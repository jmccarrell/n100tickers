# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project provides date-centric access to NASDAQ 100 index membership over time. The primary API is `tickers_as_of(year, month, day)` which returns a frozenset of ticker symbols that were in the index on the specified date. Coverage spans from February 1, 2007 through at least October 11, 2026.  Ticker symbols are point-in-time: a rename is recorded as a change event on its effective date, so a query returns the symbol that traded that day.

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

**Open the PR as the agent bot, not as `jmccarrell`.** A PR authored by the repo
owner cannot be approved by him, so a PR opened under Jeff's own login has to be
closed and reopened:

```sh
GH_TOKEN=$(lab-gh-token) gh pr create ...
```

Bare `gh pr create` uses Jeff's keyring login. `lab-gh-token` is on `~/mcc-lab-bin`
and mints a token for the `mcc-lab-agent` GitHub App, which is installed on this
repo. Only the PR author is constrained — issue and PR comments are fine under
either identity.

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
- `README.md` is the front page; its examples run as doctests under `just test`
- `docs/` holds the ADRs, the agent conventions, and the archived pre-Release-Please changelog

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

Releases are driven by [knope](https://knope.tech).  Nothing is released by
hand: every commit that reaches `main` is read as a Conventional Commit, and
knope keeps an open release PR that carries the next version bump and the
changelog entry.  Merging that PR is the release.

### Conventional Commits

The squash-merge title of every PR must be a Conventional Commit, because that
title is the only commit knope sees:

- `feat: ...` bumps the minor version — use this for index membership changes,
  which are the user-visible change this package exists to ship
- `fix: ...` bumps the patch version.  A dependency change that reaches
  consumers, such as a new range in `pyproject.toml`, is titled `fix(deps): ...`
  so that it is released
- `feat!: ...` or a `BREAKING CHANGE:` footer bumps the major version, which here
  is the year — do not use it for ordinary work
- `docs:`, `deps:`, `ci:`, `refactor:`, `test:`, `chore:` release nothing and
  make no changelog entry (ADR 0003)

A commit whose subject is not a Conventional Commit at all is invisible and
moves nothing.  The PR Title workflow fails a PR whose title is not one of the
types above, then an optional lowercase scope, an optional `!`, `: ` and a
summary.

### Cutting a release

1. Merge work to `main` with Conventional Commit titles
2. knope opens or updates the release PR ("chore: release 2026.13.0") from the
   `release` branch
3. Review it — it edits `pyproject.toml`, `CHANGELOG.md`, and this package's own
   entry in `uv.lock`.  knope has no built-in `uv.lock` support
   (knope-dev/knope#1995), so that last one is a regex `versioned_files` entry
   in `knope.toml`
4. Merge it.  The tag `v2026.13.0`, the GitHub Release, and the attached
   `uv build` artifacts follow automatically

### The year rollover

knope treats the year as the semver major, so it will never roll `2026.x` to
`2027.0.0` on its own — a `feat:` in January 2027 would produce `2026.13.0`.
Force the first release of a new year by running the Release workflow by hand
with `override_version: 2027.0.0`.  knope ignores `Release-As:` in commit
bodies.

### The release token

The `prepare` job authenticates as the `mcc-lab-agent` GitHub App: it mints a
one-hour installation token from `vars.MCC_LAB_AGENT_APP_ID` and
`secrets.MCC_LAB_AGENT_PRIVATE_KEY`, and uses it both to push the `release`
branch and as knope's `GITHUB_TOKEN` to open the PR.  The App needs Contents and
Pull requests set to read and write on this repository.  Neither alternative
works:

- The built-in `GITHUB_TOKEN`: GitHub does not run workflows from events that
  token creates, so the release PR would never run Validate and would never
  satisfy the required `build` check.
- A personal access token: its owner becomes the release PR's author, and GitHub
  does not let an author approve their own PR.

### The workflow

`.github/workflows/release.yml` runs on every push to `main`, and by hand:

1. `verify` runs the test suite.  knope publishes a release in the same step
   that creates it, so this job is the last gate that can stop a bad release
2. `release` skips unless the version in `pyproject.toml` has no tag yet.
   Otherwise it runs `uv build`, checks the wheel and sdist exist, runs
   `knope release`, and checks the published release carries the files.  If an
   earlier run left a draft with no tag, it finishes that draft by hand
   (`gh release upload --clobber`, then `gh release edit --draft=false`), since
   `knope release` refuses a release that already exists
3. `prepare` runs `knope prepare-release` to open or update the release PR.
   `releases::no_release` — nothing since the last tag bumps the version —
   counts as success; it happens after every release merge

This repository has immutable releases enabled, so a published release rejects
new assets with HTTP 422.  knope creates the release as a draft, attaches
`dist/*`, and only then publishes it.

A GitHub-forge release has no local tag: GitHub creates the tag when the release
is published, and `prepare` runs after `release` with a fresh checkout, so the
next release PR starts from the release just cut.

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
