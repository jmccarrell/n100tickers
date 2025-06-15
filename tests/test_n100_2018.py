import datetime
from nasdaq_100_ticker_history import tickers_as_of
from .helpers import _test_one_swap, _test_at_year_boundary


def test_tickers_2018() -> None:
    num_tickers_2018: int = 103

    _test_at_year_boundary(2018)

    # 6 tickers added and removed on 12/24/2018
    # https://www.nasdaq.com/about/press-center/annual-changes-nasdaq-100-index-0
    tickers_2018_dec_23 = tickers_as_of(2018, 12, 23)
    assert len(tickers_2018_dec_23) == num_tickers_2018

    tickers_2018_dec_24 = tickers_as_of(2018, 12, 24)
    assert len(tickers_2018_dec_24) == num_tickers_2018

    dec_24_removals = frozenset(("ESRX", "HOLX", "QRTEA", "SHPG", "STX", "VOD"))
    assert dec_24_removals.issubset(tickers_2018_dec_23)
    assert tickers_2018_dec_24.isdisjoint(dec_24_removals)
    dec_24_additions = frozenset(("AMD", "LULU", "NTAP", "UAL", "VRSN", "WLTW"))
    assert dec_24_additions.issubset(tickers_2018_dec_24)

    # 11/19/2018 XEL replaces XRAY
    # https://www.nasdaq.com/about/press-center/xcel-energy-inc-join-nasdaq-100-index-beginning-november-19-2018
    _test_one_swap(datetime.date.fromisoformat("2018-11-19"), "XRAY", "XEL", num_tickers_2018)

    # 11/5/2018 NXPI replaces CA
    # (link broken):
    # https://business.nasdaq.com/mediacenter/pressreleases/1831989/nxp-semiconductors-nv-to-join-the-nasdaq-100-index-beginning-november-5-2018
    _test_one_swap(datetime.date.fromisoformat("2018-11-05"), "CA", "NXPI", num_tickers_2018)

    # 7/23/2018 PEP replaces DISH
    _test_one_swap(datetime.date.fromisoformat("2018-07-23"), "DISH", "PEP", num_tickers_2018)