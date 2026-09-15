import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2012_boy = 100  # num tickers at the start of 2012
num_tickers_2012_eoy = 100  # number of tickers at the end of 2012


def test_year_boundary_2012_2013() -> None:
    _test_at_year_boundary(2013)


def test_tickers_2012() -> None:
    assert len(tickers_as_of(2012, 1, 1)) == num_tickers_2012_boy
    assert len(tickers_as_of(2012, 12, 31)) == num_tickers_2012_eoy

    # Hansen Natural became Monster Beverage
    _test_one_swap(datetime.date.fromisoformat("2012-01-09"), "HANS", "MNST", num_tickers_2012_boy)
    _test_one_swap(datetime.date.fromisoformat("2012-04-23"), "FSLR", "TXN", num_tickers_2012_boy)
    _test_one_swap(datetime.date.fromisoformat("2012-05-30"), "TEVA", "VIAB", num_tickers_2012_boy)
    _test_one_swap(datetime.date.fromisoformat("2012-07-23"), "CTRP", "KFT", num_tickers_2012_boy)
    # Kraft Foods Inc. became Mondelez International
    _test_one_swap(datetime.date.fromisoformat("2012-10-02"), "KFT", "MDLZ", num_tickers_2012_boy)
    _test_one_swap(datetime.date.fromisoformat("2012-12-12"), "INFY", "FB", num_tickers_2012_boy)

    before = tickers_as_of(2012, 12, 23)
    on = tickers_as_of(2012, 12, 24)
    removals = frozenset(("APOL", "EA", "FLEX", "GMCR", "LRCX", "MRVL", "NFLX", "RIMM", "VRSN", "WCRX"))
    assert removals.issubset(before)
    assert on.isdisjoint(removals)
    additions = frozenset(("ADI", "CTRX", "DISCA", "EQIX", "LBTYA", "LMCA", "REGN", "SBAC", "VRSK", "WDC"))
    assert additions.isdisjoint(before)
    assert additions.issubset(on)
    assert len(on) == len(before) - 10 + 10
