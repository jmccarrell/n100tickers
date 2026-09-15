import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2011_boy = 100  # num tickers at the start of 2011
num_tickers_2011_eoy = 100  # number of tickers at the end of 2011


def test_year_boundary_2011_2012() -> None:
    _test_at_year_boundary(2012)


def test_tickers_2011() -> None:
    assert len(tickers_as_of(2011, 1, 1)) == num_tickers_2011_boy
    assert len(tickers_as_of(2011, 12, 31)) == num_tickers_2011_eoy

    _test_one_swap(datetime.date.fromisoformat("2011-04-04"), "GENZ", "ALXN", num_tickers_2011_boy)
    # ticker change
    _test_one_swap(datetime.date.fromisoformat("2011-05-06"), "WFMI", "WFM", num_tickers_2011_boy)
    _test_one_swap(datetime.date.fromisoformat("2011-05-27"), "MICC", "GMCR", num_tickers_2011_boy)
    _test_one_swap(datetime.date.fromisoformat("2011-07-15"), "CEPH", "SIRI", num_tickers_2011_boy)
    _test_one_swap(datetime.date.fromisoformat("2011-12-06"), "JOYG", "PRGO", num_tickers_2011_boy)

    before = tickers_as_of(2011, 12, 18)
    on = tickers_as_of(2011, 12, 19)
    removals = frozenset(("FLIR", "ILMN", "NIHD", "QGEN", "URBN"))
    assert removals.issubset(before)
    assert on.isdisjoint(removals)
    additions = frozenset(("AVGO", "FOSL", "GOLD", "HANS", "NUAN"))
    assert additions.isdisjoint(before)
    assert additions.issubset(on)
    assert len(on) == len(before) - 5 + 5

    # ticker change
    _test_one_swap(datetime.date.fromisoformat("2011-12-20"), "ERTS", "EA", num_tickers_2011_boy)
