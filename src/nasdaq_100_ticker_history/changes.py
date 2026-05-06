"""Membership-changes API for NASDAQ-100 history.

Bidirectional iterators anchored at a fixed BASELINE_DATE / BASELINE_MEMBERSHIP
pair, so that coverage expansion in either direction (forward as new changes
are recorded, backward as earlier history is uncovered) does not shift any
previously emitted event.

See ``docs/adr/0001-bidirectional-membership-changes-api.md`` for the design
rationale and rejected alternatives.
"""

import datetime
import importlib.resources
import re
from collections.abc import Iterator
from dataclasses import dataclass
from functools import lru_cache

from .n100tickers import _load_tickers_from_yaml

#: Fixed anchor date for the membership-changes iterators. Chosen to sit
#: roughly mid-coverage so both :func:`changes_since` and
#: :func:`changes_before` are non-empty from day one.
BASELINE_DATE: datetime.date = datetime.date(2020, 1, 1)

#: NASDAQ-100 membership on :data:`BASELINE_DATE`. Hardcoded so any drift
#: in the underlying YAML data is caught by
#: ``tests/test_changes.py::test_baseline_invariant``.
BASELINE_MEMBERSHIP: frozenset[str] = frozenset(
    {
        "AAL",
        "AAPL",
        "ADBE",
        "ADI",
        "ADP",
        "ADSK",
        "ALGN",
        "ALXN",
        "AMAT",
        "AMD",
        "AMGN",
        "AMZN",
        "ANSS",
        "ASML",
        "ATVI",
        "AVGO",
        "BIDU",
        "BIIB",
        "BKNG",
        "BMRN",
        "CDNS",
        "CDW",
        "CERN",
        "CHKP",
        "CHTR",
        "CMCSA",
        "COST",
        "CPRT",
        "CSCO",
        "CSGP",
        "CSX",
        "CTAS",
        "CTSH",
        "CTXS",
        "DLTR",
        "EA",
        "EBAY",
        "EXC",
        "EXPE",
        "FAST",
        "FB",
        "FISV",
        "FOX",
        "FOXA",
        "GILD",
        "GOOG",
        "GOOGL",
        "IDXX",
        "ILMN",
        "INCY",
        "INTC",
        "INTU",
        "ISRG",
        "JD",
        "KHC",
        "KLAC",
        "LBTYA",
        "LBTYK",
        "LRCX",
        "LULU",
        "MAR",
        "MCHP",
        "MDLZ",
        "MELI",
        "MNST",
        "MSFT",
        "MU",
        "MXIM",
        "NFLX",
        "NTAP",
        "NTES",
        "NVDA",
        "NXPI",
        "ORLY",
        "PAYX",
        "PCAR",
        "PEP",
        "PYPL",
        "QCOM",
        "REGN",
        "ROST",
        "SBUX",
        "SGEN",
        "SIRI",
        "SNPS",
        "SPLK",
        "SWKS",
        "TCOM",
        "TMUS",
        "TSLA",
        "TTWO",
        "TXN",
        "UAL",
        "ULTA",
        "VRSK",
        "VRSN",
        "VRTX",
        "WBA",
        "WDAY",
        "WDC",
        "WLTW",
        "XEL",
        "XLNX",
    }
)


@dataclass(frozen=True)
class MembershipChange:
    """A single membership-change event in the NASDAQ-100 history.

    :param effective_date: the date the change took effect.
    :param additions: tickers added by this event (interpretation depends on
        which iterator yielded it; see :func:`changes_since` and
        :func:`changes_before`).
    :param removals: tickers removed by this event.
    """

    effective_date: datetime.date
    additions: frozenset[str]
    removals: frozenset[str]


_YAML_FILENAME_RE = re.compile(r"^n100-ticker-changes-(\d{4})\.yaml$")


@lru_cache
def _covered_years() -> tuple[int, ...]:
    """Return the sorted tuple of years for which YAML data is present.

    Years are discovered dynamically from the package's resources so that
    adding or removing a ``n100-ticker-changes-YYYY.yaml`` file is the only
    edit needed when coverage expands. Raises :class:`RuntimeError` if the
    discovered set is non-contiguous.
    """

    package = importlib.resources.files("nasdaq_100_ticker_history")
    years: list[int] = []
    for entry in package.iterdir():
        m = _YAML_FILENAME_RE.match(entry.name)
        if m:
            years.append(int(m.group(1)))
    if not years:
        raise RuntimeError("no n100-ticker-changes-*.yaml resources found")
    years.sort()
    expected = tuple(range(years[0], years[-1] + 1))
    if tuple(years) != expected:
        raise RuntimeError(f"non-contiguous YAML coverage: {years}")
    return tuple(years)


def _changes_for_year(year: int) -> Iterator[tuple[datetime.date, frozenset[str], frozenset[str]]]:
    """Yield (effective_date, forward_additions, forward_removals) for one year."""

    yaml = _load_tickers_from_yaml(year=year)
    if "changes" not in yaml:
        return
    for date_str in sorted(yaml["changes"].keys()):
        d = datetime.date.fromisoformat(date_str)
        ops = yaml["changes"][date_str]
        additions = frozenset(ops.get("union", ()))
        removals = frozenset(ops.get("difference", ()))
        yield d, additions, removals


def changes_since() -> Iterator[MembershipChange]:
    """Yield membership changes with ``effective_date > BASELINE_DATE``.

    Events are yielded in chronological order with **forward-sense** semantics:
    ``additions`` are tickers added to the index on that date and ``removals``
    are tickers removed.

    Folding these onto :data:`BASELINE_MEMBERSHIP` from earliest to latest
    reproduces ``tickers_as_of(d)`` at every change point post-baseline.
    """

    for year in _covered_years():
        if year < BASELINE_DATE.year:
            continue
        for d, additions, removals in _changes_for_year(year):
            if d > BASELINE_DATE:
                yield MembershipChange(d, additions, removals)


def changes_before() -> Iterator[MembershipChange]:
    """Yield inverted membership changes with ``effective_date <= BASELINE_DATE``.

    Events are yielded in **reverse chronological** order with **inverse-sense**
    semantics: each event describes what to apply to your current set when
    stepping backward through ``effective_date``. Concretely, ``additions``
    here are tickers that were *removed* by the forward change (and so are
    re-added when walking backward), and ``removals`` here are tickers that
    were *added* by the forward change.

    Folding these onto :data:`BASELINE_MEMBERSHIP` in iterator order: after
    applying the event for date ``d`` your state matches
    ``tickers_as_of(d - 1 day)`` — the membership for the period immediately
    preceding ``d``.
    """

    pre: list[tuple[datetime.date, frozenset[str], frozenset[str]]] = []
    for year in _covered_years():
        if year > BASELINE_DATE.year:
            continue
        for d, additions, removals in _changes_for_year(year):
            if d <= BASELINE_DATE:
                pre.append((d, additions, removals))
    pre.sort(key=lambda x: x[0], reverse=True)
    for d, forward_additions, forward_removals in pre:
        yield MembershipChange(effective_date=d, additions=forward_removals, removals=forward_additions)
