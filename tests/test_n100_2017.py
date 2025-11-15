import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2017 = 104


def test_tickers_2017() -> None:
    # 2/7/2017 JBHT replaced NXPI
    _test_one_swap(datetime.date.fromisoformat("2017-02-07"), "NXPI", "JBHT", num_tickers_2017)

    # 3/20/2017 IDXX replaced SBAC
    _test_one_swap(datetime.date.fromisoformat("2017-03-20"), "SBAC", "IDXX", num_tickers_2017)

    # 4/24/2017 WYNN replaced TRIP
    _test_one_swap(datetime.date.fromisoformat("2017-04-24"), "TRIP", "WYNN", num_tickers_2017)

    # 6/19/2017 MELI replaced YHOO
    _test_one_swap(datetime.date.fromisoformat("2017-06-19"), "YHOO", "MELI", num_tickers_2017)

    # 10/23/2017 ALGN replaced MAT
    _test_one_swap(datetime.date.fromisoformat("2017-10-23"), "MAT", "ALGN", num_tickers_2017)

    # annual changes for 2017; effective Dec 18, 2017
    #  https://www.nasdaq.com/about/press-center/annual-changes-nasdaq-100-index-2
    dec_18_removals = frozenset(("AKAM", "DISCA", "DISCK", "NCLH", "TSCO", "VIAB"))
    dec_18_additions = frozenset(("ASML", "CDNS", "SNPS", "TTWO", "WDAY"))

    tickers_dec_17 = tickers_as_of(2017, 12, 17)
    assert len(tickers_dec_17) == num_tickers_2017
    assert dec_18_removals.issubset(tickers_dec_17)
    assert tickers_dec_17.isdisjoint(dec_18_additions)

    tickers_dec_18 = tickers_as_of(2017, 12, 18)
    # this was a remove 6 and add 5 change due to two classes of Discovery Communications: DISCA and DISCK
    assert len(tickers_dec_18) == num_tickers_2017 - 1

    assert dec_18_additions.issubset(tickers_dec_18)
    assert tickers_dec_18.isdisjoint(dec_18_removals)


def test_year_boundary_2016_2017() -> None:
    _test_at_year_boundary(2017)
