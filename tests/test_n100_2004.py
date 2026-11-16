import datetime

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2004 = 100


def test_year_boundary_2004_2005() -> None:
    _test_at_year_boundary(2005)


def test_tickers_2004() -> None:
    _test_one_swap(datetime.date.fromisoformat("2004-08-19"), "SPOT", "KMRT", num_tickers_2004)
