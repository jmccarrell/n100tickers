import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2014_boy = 100  # num tickers at the start of 2014
num_tickers_2014_eoy = 105  # number of tickers at the end of 2014


def test_year_boundary_2014_2015() -> None:
    _test_at_year_boundary(2015)


def test_tickers_2014() -> None:
    assert len(tickers_as_of(2014, 1, 1)) == num_tickers_2014_boy
    assert len(tickers_as_of(2014, 12, 31)) == num_tickers_2014_eoy

    # Google's Class C distribution: the Class A line became GOOGL, the new Class C took GOOG
    before = tickers_as_of(2014, 4, 2)
    on = tickers_as_of(2014, 4, 3)
    additions = frozenset(("GOOGL",))
    assert additions.isdisjoint(before)
    assert additions.issubset(on)
    assert len(on) == len(before) + 1

    # Liberty Media Series C began regular-way trading
    before = tickers_as_of(2014, 7, 23)
    on = tickers_as_of(2014, 7, 24)
    additions = frozenset(("LMCK",))
    assert additions.isdisjoint(before)
    assert additions.issubset(on)
    assert len(on) == len(before) + 1

    # Discovery Communications Series C began regular-way trading
    before = tickers_as_of(2014, 8, 6)
    on = tickers_as_of(2014, 8, 7)
    additions = frozenset(("DISCK",))
    assert additions.isdisjoint(before)
    assert additions.issubset(on)
    assert len(on) == len(before) + 1

    # Liberty Interactive's Interactive Group became the QVC Group tracking stock
    _test_one_swap(datetime.date.fromisoformat("2014-10-07"), "LINTA", "QVCA", 103)

    before = tickers_as_of(2014, 12, 21)
    on = tickers_as_of(2014, 12, 22)
    removals = frozenset(("EXPE", "FFIV", "MXIM"))
    assert removals.issubset(before)
    assert on.isdisjoint(removals)
    additions = frozenset(("AAL", "EA", "FOX", "LBTYK", "LRCX"))
    assert additions.isdisjoint(before)
    assert additions.issubset(on)
    assert len(on) == len(before) - 3 + 5
