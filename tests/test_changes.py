"""Tests for the bidirectional membership-changes API (ADR-0001)."""

import datetime

import pytest

from nasdaq_100_ticker_history import (
    BASELINE_DATE,
    BASELINE_MEMBERSHIP,
    MembershipChange,
    changes_before,
    changes_since,
    tickers_as_of,
)
from nasdaq_100_ticker_history.changes import _covered_years


def test_baseline_date_is_2020_01_01() -> None:
    assert BASELINE_DATE == datetime.date(2020, 1, 1)


def test_baseline_invariant() -> None:
    """``BASELINE_MEMBERSHIP`` must match the YAML-derived membership on
    ``BASELINE_DATE``. Drift here means the constant is stale."""

    derived = tickers_as_of(BASELINE_DATE.year, BASELINE_DATE.month, BASELINE_DATE.day)
    assert BASELINE_MEMBERSHIP == derived


def test_covered_years_are_contiguous() -> None:
    years = _covered_years()
    assert years, "_covered_years must not be empty"
    assert tuple(years) == tuple(range(years[0], years[-1] + 1))


def test_changes_since_is_chronological_and_post_baseline() -> None:
    events = list(changes_since())
    dates = [e.effective_date for e in events]
    assert dates == sorted(dates), "changes_since must yield in chronological order"
    for d in dates:
        assert d > BASELINE_DATE


def test_changes_before_is_reverse_chronological_and_pre_baseline() -> None:
    events = list(changes_before())
    dates = [e.effective_date for e in events]
    assert dates == sorted(dates, reverse=True), "changes_before must yield in reverse chronological order"
    for d in dates:
        assert d <= BASELINE_DATE


def test_changes_since_reproduces_tickers_as_of_at_each_change() -> None:
    """Folding ``changes_since`` onto ``BASELINE_MEMBERSHIP`` reproduces
    ``tickers_as_of(d)`` at every post-baseline change point."""

    state = BASELINE_MEMBERSHIP
    saw_at_least_one = False
    for chg in changes_since():
        state = state.union(chg.additions).difference(chg.removals)
        expected = tickers_as_of(chg.effective_date.year, chg.effective_date.month, chg.effective_date.day)
        assert state == expected, (
            f"after change on {chg.effective_date}, state mismatch: "
            f"missing {sorted(expected - state)}, extra {sorted(state - expected)}"
        )
        saw_at_least_one = True
    assert saw_at_least_one, "expected at least one post-baseline change"


def test_changes_before_reproduces_tickers_as_of_predecessor() -> None:
    """After applying an inverse event for date ``d`` going backward, the
    state matches ``tickers_as_of(d - 1 day)``."""

    state = BASELINE_MEMBERSHIP
    saw_at_least_one = False
    for chg in changes_before():
        state = state.union(chg.additions).difference(chg.removals)
        prev = chg.effective_date - datetime.timedelta(days=1)
        expected = tickers_as_of(prev.year, prev.month, prev.day)
        assert state == expected, (
            f"after stepping back through {chg.effective_date}, state should match "
            f"tickers_as_of({prev}); missing {sorted(expected - state)}, "
            f"extra {sorted(state - expected)}"
        )
        saw_at_least_one = True
    assert saw_at_least_one, "expected at least one pre-baseline change"


def test_membership_change_is_frozen() -> None:
    chg = MembershipChange(
        effective_date=datetime.date(2020, 1, 1),
        additions=frozenset({"AAA"}),
        removals=frozenset({"BBB"}),
    )
    with pytest.raises(Exception):
        chg.effective_date = datetime.date(2021, 1, 1)  # type: ignore[misc]


def test_no_zero_change_events_emitted_since() -> None:
    for chg in changes_since():
        assert chg.additions or chg.removals, f"empty change at {chg.effective_date}"


def test_no_zero_change_events_emitted_before() -> None:
    for chg in changes_before():
        assert chg.additions or chg.removals, f"empty change at {chg.effective_date}"
