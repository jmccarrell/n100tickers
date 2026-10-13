import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

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

    # Liberty Media's recapitalization added BATRA, BATRK, LSXMA and LSXMK at zero
    # weight on Apr 18, with no replacements.  LSXMA and LSXMK left again before
    # the open on Apr 19.
    #  https://www.nasdaqtrader.com/TraderNews.aspx?id=fpnews2016-25
    apr_17_tickers = tickers_as_of(2016, 4, 17)
    assert len(apr_17_tickers) == 105
    apr_18_tickers = tickers_as_of(2016, 4, 18)
    assert len(apr_18_tickers) == 109
    apr_19_tickers = tickers_as_of(2016, 4, 19)
    assert len(apr_19_tickers) == 107

    apr_18_additions = frozenset(("BATRA", "BATRK", "LSXMA", "LSXMK"))
    assert apr_18_additions.isdisjoint(apr_17_tickers)
    assert apr_18_additions.issubset(apr_18_tickers)

    apr_19_removals = frozenset(("LSXMA", "LSXMK"))
    assert apr_19_tickers.isdisjoint(apr_19_removals)
    assert frozenset(("BATRA", "BATRK")).issubset(apr_19_tickers)

    # A 4-for-1 change announced Jun 10, effective before market open Jun 20.
    # https://ir.nasdaq.com/news-releases/news-release-details/dentsply-sirona-inc-join-nasdaq-100-index-beginning-june-20-2016
    jun_19_tickers = tickers_as_of(2016, 6, 19)
    assert len(jun_19_tickers) == 107
    jun_20_tickers = tickers_as_of(2016, 6, 20)
    assert len(jun_20_tickers) == 104

    jun_20_removals = frozenset(("LMCA", "LMCK", "BATRA", "BATRK"))
    assert jun_20_removals.issubset(jun_19_tickers)
    assert jun_20_tickers.isdisjoint(jun_20_removals)

    jun_20_additions = frozenset(("XRAY",))
    assert jun_20_additions.isdisjoint(jun_19_tickers)
    assert jun_20_additions.issubset(jun_20_tickers)

    # https://en.wikipedia.org/wiki/Nasdaq-100#cite_note-39
    _test_one_swap(datetime.date.fromisoformat("2016-07-18"), "ENDP", "MCHP", num_tickers_2016_eoy)

    # https://en.wikipedia.org/wiki/Nasdaq-100#cite_note-40
    _test_one_swap(datetime.date.fromisoformat("2016-10-19"), "LLTC", "SHPG", num_tickers_2016_eoy)
