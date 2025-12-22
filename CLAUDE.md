# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project provides date-centric access to NASDAQ 100 index membership over time. The primary API is `tickers_as_of(year, month, day)` which returns a frozenset of ticker symbols that were in the index on the specified date. Coverage spans from January 1, 2015 through at least November 15, 2025.

## Common Commands

This project uses `just` for task automation and `uv` for Python dependency management.

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

## Notes

- Python 3.11+ required
- Line length: 108 characters (configured in `ruff.toml`)
- Import sorting enabled via ruff (isort rules)
- Coverage settings: branch coverage enabled, shows missing lines, skips covered lines
