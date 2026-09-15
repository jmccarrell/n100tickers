import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2010_boy = 100  # num tickers at the start of 2010
num_tickers_2010_eoy = 100  # number of tickers at the end of 2010


def test_year_boundary_2010_2011() -> None:
    _test_at_year_boundary(2011)


def test_tickers_2010() -> None:
    assert len(tickers_as_of(2010, 1, 1)) == num_tickers_2010_boy
    assert len(tickers_as_of(2010, 12, 31)) == num_tickers_2010_eoy

    before = tickers_as_of(2010, 12, 19)
    on = tickers_as_of(2010, 12, 20)
    removals = frozenset(("CTAS", "DISH", "FWLT", "HOLX", "JBHT", "LOGI", "PDCO"))
    assert removals.issubset(before)
    assert on.isdisjoint(removals)
    additions = frozenset(("AKAM", "CTRP", "DLTR", "FFIV", "MU", "NFLX", "WFMI"))
    assert additions.isdisjoint(before)
    assert additions.issubset(on)
    assert len(on) == len(before) - 7 + 7
