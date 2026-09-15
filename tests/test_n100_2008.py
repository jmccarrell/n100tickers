import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2008_boy = 100  # num tickers at the start of 2008
num_tickers_2008_eoy = 100  # number of tickers at the end of 2008


def test_year_boundary_2008_2009() -> None:
    _test_at_year_boundary(2009)


def test_tickers_2008() -> None:
    assert len(tickers_as_of(2008, 1, 1)) == num_tickers_2008_boy
    assert len(tickers_as_of(2008, 12, 31)) == num_tickers_2008_eoy

    _test_one_swap(datetime.date.fromisoformat("2008-04-30"), "BEAS", "DTV", num_tickers_2008_boy)
    _test_one_swap(datetime.date.fromisoformat("2008-05-19"), "TLAB", "CA", num_tickers_2008_boy)
    _test_one_swap(datetime.date.fromisoformat("2008-07-21"), "UAUA", "FLIR", num_tickers_2008_boy)
    _test_one_swap(datetime.date.fromisoformat("2008-11-10"), "MNST", "STX", num_tickers_2008_boy)

    before = tickers_as_of(2008, 12, 21)
    on = tickers_as_of(2008, 12, 22)
    removals = frozenset(
        ("AMLN", "CDNS", "DISCA", "LAMR", "LEAP", "LVLT", "PETM", "SIRI", "SNDK", "VMED", "WFMI")
    )
    assert removals.issubset(before)
    assert on.isdisjoint(removals)
    additions = frozenset(
        ("ADP", "FSLR", "ILMN", "JBHT", "LIFE", "MXIM", "ORLY", "PPDI", "ROST", "URBN", "WCRX")
    )
    assert additions.isdisjoint(before)
    assert additions.issubset(on)
    assert len(on) == len(before) - 11 + 11
