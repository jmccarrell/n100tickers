import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2013_boy = 100  # num tickers at the start of 2013
num_tickers_2013_eoy = 100  # number of tickers at the end of 2013


def test_year_boundary_2013_2014() -> None:
    _test_at_year_boundary(2014)


def test_tickers_2013() -> None:
    assert len(tickers_as_of(2013, 1, 1)) == num_tickers_2013_boy
    assert len(tickers_as_of(2013, 12, 31)) == num_tickers_2013_eoy

    _test_one_swap(datetime.date.fromisoformat("2013-01-15"), "LMCA", "STRZA", num_tickers_2013_boy)
    _test_one_swap(datetime.date.fromisoformat("2013-03-18"), "STRZA", "KRFT", num_tickers_2013_boy)
    _test_one_swap(datetime.date.fromisoformat("2013-06-05"), "VMED", "LMCA", num_tickers_2013_boy)
    _test_one_swap(datetime.date.fromisoformat("2013-06-06"), "PRGO", "NFLX", num_tickers_2013_boy)
    # News Corporation became Twenty-First Century Fox
    _test_one_swap(datetime.date.fromisoformat("2013-07-01"), "NWSA", "FOXA", num_tickers_2013_boy)
    _test_one_swap(datetime.date.fromisoformat("2013-07-15"), "ORCL", "TSLA", num_tickers_2013_boy)
    _test_one_swap(datetime.date.fromisoformat("2013-07-25"), "BMC", "CHTR", num_tickers_2013_boy)
    _test_one_swap(datetime.date.fromisoformat("2013-08-22"), "LIFE", "GMCR", num_tickers_2013_boy)
    _test_one_swap(datetime.date.fromisoformat("2013-10-29"), "DELL", "VIP", num_tickers_2013_boy)
    _test_one_swap(datetime.date.fromisoformat("2013-11-18"), "GOLD", "MAR", num_tickers_2013_boy)

    before = tickers_as_of(2013, 12, 22)
    on = tickers_as_of(2013, 12, 23)
    removals = frozenset(("FOSL", "MCHP", "NUAN", "SHLD", "XRAY"))
    assert removals.issubset(before)
    assert on.isdisjoint(removals)
    additions = frozenset(("DISH", "ILMN", "NXPI", "TRIP", "TSCO"))
    assert additions.isdisjoint(before)
    assert additions.issubset(on)
    assert len(on) == len(before) - 5 + 5
