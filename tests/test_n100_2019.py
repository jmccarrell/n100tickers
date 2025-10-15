import datetime
from nasdaq_100_ticker_history import tickers_as_of
from .helpers import _test_one_swap, _test_at_year_boundary

num_tickers_2019 = 103


def test_tickers_2019() -> None:
    _test_at_year_boundary(2019)

    # https://www.nasdaq.com/press-release/exelon-corporation-to-join-the-nasdaq-100-index-beginning-november-21-2019-2019-11-18
    _test_one_swap(datetime.date.fromisoformat("2019-11-19"), "CELG", "EXC", num_tickers_2019)

    # Ctrip.com International, Ltd. (CTRP) will change its name, trading symbol,
    # and CUSIP to Trip.com Group Limited (TCOM), CUSIP 89677Q107
    # https://www.miaxglobal.com/sites/default/files/alert-files/CTRP_Symbol_Name___45919.pdf
    _test_one_swap(datetime.date.fromisoformat("2019-11-05"), "CTRP", "TCOM", num_tickers_2019)

    # 6 tickers added and removed on 12/23/2019
    # https://finance.yahoo.com/news/annual-changes-nasdaq-100-index-010510822.html
    tickers_2019_dec_23 = tickers_as_of(2019, 12, 23)
    assert len(tickers_2019_dec_23) == num_tickers_2019
    dec_23_removals = frozenset(("HAS", "HSIC", "JBHT", "MYL", "NLOK", "WYNN"))
    assert tickers_2019_dec_23.isdisjoint(dec_23_removals)
    dec_23_additions = frozenset(("ANSS", "CDW", "CPRT", "CSGP", "SGEN", "SPLK"))
    assert dec_23_additions.issubset(tickers_2019_dec_23)

    tickers_2019_dec_20 = tickers_as_of(2019, 12, 20)
    assert len(tickers_2019_dec_20) == num_tickers_2019
    assert dec_23_removals.issubset(tickers_2019_dec_20)
    assert tickers_2019_dec_20.isdisjoint(dec_23_additions)

    # there was a record of 21st Century Fox changing to Fox Corp.  But as near as I can tell, the ticker
    # symbols were the same.
