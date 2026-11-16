import datetime

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2006 = 100


def test_year_boundary_2006_2007() -> None:
    _test_at_year_boundary(2007)


def test_tickers_2006() -> None:
    # The year's first change falls after Jan 1, so tickers_on_Jan_1 must be 2005's closing set.
    _test_one_swap(datetime.date.fromisoformat("2006-01-04"), "MERQ", "JOYG", num_tickers_2006)
    # A ticker change: Ericsson's ADRs moved from ERICY to ERIC.
    _test_one_swap(datetime.date.fromisoformat("2006-08-24"), "ERICY", "ERIC", num_tickers_2006)
