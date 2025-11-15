import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2015_boy = 105  # num tickers at the start of 2015
num_tickers_2015_eoy = 105  # number of tickers at the end of 2015


def test_year_boundary_2015_2016() -> None:
    _test_at_year_boundary(2016)


def test_2015_annual_changes() -> None:
    # annual changes for 2015; effective Dec 21, 2015
    #  https://en.wikipedia.org/wiki/Nasdaq-100#Changes_in_2015
    dec_20_tickers = tickers_as_of(2015, 12, 20)
    dec_21_tickers = tickers_as_of(2015, 12, 21)
    assert len(dec_20_tickers) == 107
    assert len(dec_21_tickers) == num_tickers_2015_eoy

    dec_21_removals = frozenset(("CHRW", "EXPD", "GMCR", "GRMN", "SPLS", "WYNN", "VIP", "LILA", "LILAK"))
    assert dec_21_removals.issubset(dec_20_tickers)
    assert dec_21_tickers.isdisjoint(dec_21_removals)

    dec_21_additions = frozenset(("CTRP", "ENDP", "EXPE", "MXIM", "NCLH", "TMUS", "ULTA"))
    assert dec_21_additions.isdisjoint(dec_20_tickers)
    assert dec_21_additions.issubset(dec_21_tickers)


def test_tickers_2015() -> None:
    assert len(tickers_as_of(2015, 1, 1)) == num_tickers_2015_boy
    assert len(tickers_as_of(2015, 12, 31)) == num_tickers_2015_eoy

    _test_one_swap(datetime.date.fromisoformat("2015-03-23"), "EQIX", "WBA", num_tickers_2015_boy)

    # Jul 2: -KRFT, +KHC, +LILA, +LILAK
    jul_1_tickers = tickers_as_of(2015, 7, 1)
    assert len(jul_1_tickers) == num_tickers_2015_boy
    jul_2_tickers = tickers_as_of(2015, 7, 2)
    assert len(jul_2_tickers) == 107
    assert "KRFT" in jul_1_tickers
    assert "KRFT" not in jul_2_tickers
    assert "KHC" not in jul_1_tickers
    assert "LILA" not in jul_1_tickers
    assert "LILAK" not in jul_1_tickers
    assert "KHC" in jul_2_tickers
    assert "LILA" in jul_2_tickers
    assert "LILAK" in jul_2_tickers

    _test_one_swap(datetime.date.fromisoformat("2015-07-27"), "DTV", "BMRN", 107)
    _test_one_swap(datetime.date.fromisoformat("2015-07-29"), "CTRX", "JD", 107)
    _test_one_swap(datetime.date.fromisoformat("2015-08-03"), "SIAL", "SWKS", 107)
    _test_one_swap(datetime.date.fromisoformat("2015-10-07"), "ALTR", "INCY", 107)
    _test_one_swap(datetime.date.fromisoformat("2015-11-11"), "BRCM", "PYPL", 107)
