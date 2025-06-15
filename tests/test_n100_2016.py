import datetime
from nasdaq_100_ticker_history import tickers_as_of
from .helpers import _test_one_swap, _test_at_year_boundary

num_tickers_2016_boy = 105  # num tickers at the start of 2016
num_tickers_2016_eoy = 104  # number of tickers at the end of 2016


def test_year_boundary_2016_2017() -> None:
    _test_at_year_boundary(2017)


def test_2016_annual_changes() -> None:
    # annual changes for 2016; effective Dec 19, 2016 announced Dec 9
    #  https://en.wikipedia.org/wiki/Nasdaq-100#Changes_in_2016
    dec_18_tickers = tickers_as_of(2016, 12, 18)
    dec_19_tickers = tickers_as_of(2016, 12, 19)
    assert len(dec_18_tickers) == len(dec_19_tickers)

    dec_19_removals = frozenset(("BBBY", "NTAP", "SRCL", "WFM"))
    assert dec_19_removals.issubset(dec_18_tickers)
    assert dec_19_tickers.isdisjoint(dec_19_removals)

    dec_19_additions = frozenset(("CTAS", "HAS", "HOLX", "KLAC"))
    assert dec_19_additions.isdisjoint(dec_18_tickers)
    assert dec_19_additions.issubset(dec_19_tickers)


def test_tickers_2016() -> None:
    assert len(tickers_as_of(2016, 1, 1)) == num_tickers_2016_boy
    assert len(tickers_as_of(2016, 12, 31)) == num_tickers_2016_eoy

    # https://ir.nasdaq.com/news-releases/news-release-details/csx-corporation-join-nasdaq-100-index-beginning-february-22-2016
    _test_one_swap(datetime.date.fromisoformat("2016-02-22"), "KLAC", "CSX", num_tickers_2016_boy)

    #  https://www.nasdaq.com/about/press-center/netease-inc-join-nasdaq-100-index-beginning-march-16-2016
    _test_one_swap(datetime.date.fromisoformat("2016-03-16"), "SNDK", "NTES", num_tickers_2016_boy)

    # adds BATRA, BATRK as of Apr 18; no replacements
    #  https://en.wikipedia.org/wiki/Nasdaq-100#cite_note-37
    apr_17_tickers = tickers_as_of(2016, 4, 17)
    assert len(apr_17_tickers) == 105
    apr_18_tickers = tickers_as_of(2016, 4, 18)
    assert len(apr_18_tickers) == 107

    apr_18_additions = frozenset(("BATRA", "BATRK"))
    assert apr_18_additions.isdisjoint(apr_17_tickers)
    assert apr_18_additions.issubset(apr_18_tickers)

    # https://en.wikipedia.org/wiki/Nasdaq-100#cite_note-38
    #  this is a 4 for one change as of June 10
    jun_09_tickers = tickers_as_of(2016, 6, 9)
    assert len(jun_09_tickers) == 107
    jun_10_tickers = tickers_as_of(2016, 6, 10)
    assert len(jun_10_tickers) == 104

    jun_10_removals = frozenset(("LMCA", "LMCK", "BATRA", "BATRK"))
    assert jun_10_removals.issubset(jun_09_tickers)
    assert jun_10_tickers.isdisjoint(jun_10_removals)

    jun_10_additions = frozenset(("XRAY",))
    assert jun_10_additions.isdisjoint(jun_09_tickers)
    assert jun_10_additions.issubset(jun_10_tickers)

    # https://en.wikipedia.org/wiki/Nasdaq-100#cite_note-39
    _test_one_swap(datetime.date.fromisoformat("2016-07-18"), "ENDP", "MCHP", num_tickers_2016_eoy)

    # https://en.wikipedia.org/wiki/Nasdaq-100#cite_note-40
    _test_one_swap(datetime.date.fromisoformat("2016-10-19"), "LLTC", "SHPG", num_tickers_2016_eoy)
