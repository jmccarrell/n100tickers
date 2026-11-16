import datetime

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2005 = 100


def test_year_boundary_2005_2006() -> None:
    _test_at_year_boundary(2006)


def test_tickers_2005() -> None:
    # A successor, not an index change: Kmart Holding became Sears Holdings.
    _test_one_swap(datetime.date.fromisoformat("2005-03-28"), "KMRT", "SHLD", num_tickers_2005)
