import datetime
from nasdaq_100_ticker_history import tickers_as_of
from .helpers import _test_one_swap, _test_at_year_boundary


def test_tickers_2020() -> None:
    num_tickers_2020: int = 103

    _test_at_year_boundary(2020)

    # On April 20, Dexcom replaced American Airlines Group in the index
    _test_one_swap(datetime.date.fromisoformat("2020-04-20"), "AAL", "DXCM", num_tickers_2020)

    # On April 30, Zoom Video Communications replaced Willis Towers Watson
    _test_one_swap(datetime.date.fromisoformat("2020-04-30"), "WLTW", "ZM", num_tickers_2020)

    # On June 22, DocuSign, Inc. (DOCU) will replace United Airlines Holdings, Inc. (Nasdaq: UAL)
    _test_one_swap(datetime.date.fromisoformat("2020-06-22"), "UAL", "DOCU", num_tickers_2020)

    # On Jul 20, Moderna MRNA replaces CoStar Group CGSP
    # https://www.globenewswire.com/news-release/2020/07/13/2061339/0/en/Moderna-Inc-to-Join-the-NASDAQ-100-Index-Beginning-July-20-2020.html
    _test_one_swap(datetime.date.fromisoformat("2020-07-20"), "CSGP", "MRNA", num_tickers_2020)

    # On 24 Aug 2020, Pinduoduo, Inc. PDD replaced NetApp, Inc. NTAP in the NASDAQ-100 Index.
    # https://www.globenewswire.com/news-release/2020/08/15/2078875/0/en/Pinduoduo-Inc-to-Join-the-NASDAQ-100-Index-Beginning-August-24-2020.html
    _test_one_swap(datetime.date.fromisoformat("2020-08-24"), "NTAP", "PDD", 103)

    # Western Digital Corp (WDC) is replaced by Keurig Dr Pepper Inc. (KDP) as of Oct 19, 2020.
    # https://www.globenewswire.com/news-release/2020/10/10/2106521/0/en/Keurig-Dr-Pepper-Inc-to-Join-the-NASDAQ-100-Index-Beginning-October-19-2020.html
    _test_one_swap(datetime.date.fromisoformat("2020-10-19"), "WDC", "KDP", 103)


def test_2020_annual_changes() -> None:
    # Annual 2020 changes
    # https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-index-2020-12-11
    #
    # 6 companies added; 6 removed.  However, Liberty Global PLC has 2 symbols: (Nasdaq: LBTYA/LBTYK)
    # So total tickers change from 103 to 102.
    # Effective date: 2020-12-21
    assert len(tickers_as_of(2020, 12, 18)) == 103
    tickers_removed_12_21 = frozenset(("BMRN", "CTXS", "EXPE", "LBTYA", "LBTYK", "TTWO", "ULTA"))
    assert tickers_removed_12_21.issubset(tickers_as_of(2020, 12, 18))
    tickers_added_12_21 = frozenset(("AEP", "MRVL", "MTCH", "OKTA", "PTON", "TEAM"))
    assert tickers_added_12_21.isdisjoint(tickers_as_of(2020, 12, 18))

    assert len(tickers_as_of(2020, 12, 21)) == 102
    assert tickers_removed_12_21.isdisjoint(tickers_as_of(2020, 12, 21))
    assert tickers_added_12_21.issubset(tickers_as_of(2020, 12, 21))