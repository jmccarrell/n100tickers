import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2009_boy = 100  # num tickers at the start of 2009
num_tickers_2009_eoy = 100  # number of tickers at the end of 2009


def test_year_boundary_2009_2010() -> None:
    _test_at_year_boundary(2010)


def test_tickers_2009() -> None:
    assert len(tickers_as_of(2009, 1, 1)) == num_tickers_2009_boy
    assert len(tickers_as_of(2009, 12, 31)) == num_tickers_2009_eoy

    _test_one_swap(datetime.date.fromisoformat("2009-01-20"), "FMCN", "NWSA", num_tickers_2009_boy)
    _test_one_swap(datetime.date.fromisoformat("2009-07-17"), "JAVA", "CERN", num_tickers_2009_boy)
    _test_one_swap(datetime.date.fromisoformat("2009-10-29"), "JNPR", "PCLN", num_tickers_2009_boy)

    before = tickers_as_of(2009, 12, 20)
    on = tickers_as_of(2009, 12, 21)
    removals = frozenset(("AKAM", "HANS", "IACI", "LBTYA", "PPDI", "RYAAY", "STLD"))
    assert removals.issubset(before)
    assert on.isdisjoint(removals)
    additions = frozenset(("BMC", "MAT", "MYL", "QGEN", "SNDK", "VMED", "VOD"))
    assert additions.isdisjoint(before)
    assert additions.issubset(on)
    assert len(on) == len(before) - 7 + 7
