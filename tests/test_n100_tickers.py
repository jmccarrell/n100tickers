import datetime

from nasdaq_100_ticker_history import tickers_as_of


def test_basics() -> None:
    assert 'AMZN' in tickers_as_of(2020, 6, 1)
    assert len(tickers_as_of(2020, 6, 1)) >= 100


def _test_one_swap(as_of_date: datetime.date,
                   removed_ticker: str,
                   added_ticker: str,
                   expected_number_of_tickers: int) -> None:
    tickers_on_change_date = tickers_as_of(as_of_date.year,
                                           as_of_date.month,
                                           as_of_date.day)
    assert len(tickers_on_change_date) == expected_number_of_tickers
    before_change_date = as_of_date - datetime.timedelta(days=1)
    tickers_before_change_date = tickers_as_of(before_change_date.year,
                                               before_change_date.month,
                                               before_change_date.day)
    assert len(tickers_before_change_date) == expected_number_of_tickers

    assert removed_ticker in tickers_before_change_date
    assert added_ticker not in tickers_before_change_date
    assert removed_ticker not in tickers_on_change_date
    assert added_ticker in tickers_on_change_date


def _test_at_year_boundary(year: int, expected_number_of_tickers: int) -> None:
    """prove the tickers at the beginning of the year match the set at the end of the
    previous year.
    """
    begin_of_current_year = datetime.date.fromisoformat(f"{year}-01-01")
    end_of_previous_year = begin_of_current_year - datetime.timedelta(days=1)

    current_tickers = tickers_as_of(begin_of_current_year.year,
                                    begin_of_current_year.month,
                                    begin_of_current_year.day)
    previous_tickers = tickers_as_of(end_of_previous_year.year,
                                     end_of_previous_year.month,
                                     end_of_previous_year.day)
    assert previous_tickers == current_tickers


def test_tickers_2020() -> None:
    num_tickers_2020: int = 103

    _test_at_year_boundary(2020, num_tickers_2020)

    # On April 20, Dexcom replaced American Airlines Group in the index
    _test_one_swap(datetime.date.fromisoformat('2020-04-20'), 'AAL', 'DXCM', num_tickers_2020)

    # On April 30, Zoom Video Communications replaced Willis Towers Watson
    _test_one_swap(datetime.date.fromisoformat('2020-04-30'), 'WLTW', 'ZM', num_tickers_2020)

    # On June 22, DocuSign, Inc. (DOCU) will replace United Airlines Holdings, Inc. (Nasdaq: UAL)
    _test_one_swap(datetime.date.fromisoformat('2020-06-22'), 'UAL', 'DOCU', num_tickers_2020)

    # On Jul 20, Moderna MRNA replaces CoStar Group CGSP
    # https://www.globenewswire.com/news-release/2020/07/13/2061339/0/en/Moderna-Inc-to-Join-the-NASDAQ-100-Index-Beginning-July-20-2020.html
    _test_one_swap(datetime.date.fromisoformat('2020-07-20'), 'CSGP', 'MRNA', num_tickers_2020)

    # On 24 Aug 2020, Pinduoduo, Inc. PDD replaced NetApp, Inc. NTAP in the NASDAQ-100 Index.
    # https://www.globenewswire.com/news-release/2020/08/15/2078875/0/en/Pinduoduo-Inc-to-Join-the-NASDAQ-100-Index-Beginning-August-24-2020.html
    _test_one_swap(datetime.date.fromisoformat('2020-08-24'), 'NTAP', 'PDD', 103)

    # Western Digital Corp (WDC) is replaced by Keurig Dr Pepper Inc. (KDP) as of Oct 19, 2020.
    # https://www.globenewswire.com/news-release/2020/10/10/2106521/0/en/Keurig-Dr-Pepper-Inc-to-Join-the-NASDAQ-100-Index-Beginning-October-19-2020.html
    _test_one_swap(datetime.date.fromisoformat('2020-10-19'), 'WDC', 'KDP', 103)


def test_tickers_2019() -> None:
    num_tickers_2019: int = 103

    _test_at_year_boundary(2019, num_tickers_2019)

    # 6 tickers added and removed on 12/23/2019
    # https://finance.yahoo.com/news/annual-changes-nasdaq-100-index-010510822.html
    tickers_2019_dec_23 = tickers_as_of(2019, 12, 23)
    assert len(tickers_2019_dec_23) == num_tickers_2019
    dec_23_removals = frozenset(('HAS', 'HSIC', 'JBHT', 'MYL', 'NLOK', 'WYNN'))
    assert tickers_2019_dec_23.isdisjoint(dec_23_removals)
    dec_23_additions = frozenset(('ANSS', 'CDW', 'CPRT', 'CSGP', 'SGEN', 'SPLK'))
    assert dec_23_additions.issubset(tickers_2019_dec_23)

    tickers_2019_dec_20 = tickers_as_of(2019, 12, 20)
    assert len(tickers_2019_dec_20) == num_tickers_2019
    assert dec_23_removals.issubset(tickers_2019_dec_20)
    assert tickers_2019_dec_20.isdisjoint(dec_23_additions)

    # 1 swap Nov 19
    # https://www.nasdaq.com/press-release/exelon-corporation-to-join-the-nasdaq-100-index-beginning-november-21-2019-2019-11-18
    _test_one_swap(datetime.date.fromisoformat('2019-11-19'), 'CELG', 'EXC', num_tickers_2019)

    # there was a record of 21st Century Fox changing to Fox Corp.  But as near as I can tell, the ticker
    # symbols were the same.


def test_tickers_2018() -> None:
    num_tickers_2018: int = 103

    _test_at_year_boundary(2018, num_tickers_2018)

    # 6 tickers added and removed on 12/24/2018
    # https://www.nasdaq.com/about/press-center/annual-changes-nasdaq-100-index-0
    tickers_2018_dec_23 = tickers_as_of(2018, 12, 23)
    assert len(tickers_2018_dec_23) == num_tickers_2018

    tickers_2018_dec_24 = tickers_as_of(2018, 12, 24)
    assert len(tickers_2018_dec_24) == num_tickers_2018

    dec_24_removals = frozenset(('ESRX', 'HOLX', 'QRTEA', 'SHPG', 'STX', 'VOD'))
    assert dec_24_removals.issubset(tickers_2018_dec_23)
    assert tickers_2018_dec_24.isdisjoint(dec_24_removals)
    dec_24_additions = frozenset(('AMD', 'LULU', 'NTAP', 'UAL', 'VRSN', 'WLTW'))
    assert dec_24_additions.issubset(tickers_2018_dec_24)

    # 11/19/2018 XEL replaces XRAY
    # https://www.nasdaq.com/about/press-center/xcel-energy-inc-join-nasdaq-100-index-beginning-november-19-2018
    _test_one_swap(datetime.date.fromisoformat('2018-11-19'), 'XRAY', 'XEL', num_tickers_2018)

    # 11/5/2018 NXPI replaces CA
    # (link broken):
    # https://business.nasdaq.com/mediacenter/pressreleases/1831989/nxp-semiconductors-nv-to-join-the-nasdaq-100-index-beginning-november-5-2018
    _test_one_swap(datetime.date.fromisoformat('2018-11-05'), 'CA', 'NXPI', num_tickers_2018)

    # 7/23/2018 PEP replaces DISH
    _test_one_swap(datetime.date.fromisoformat('2018-07-23'), 'DISH', 'PEP', num_tickers_2018)


def test_tickers_2017() -> None:
    num_tickers_2017: int = 104

    # 2/7/2017 JBHT replaced NXPI
    _test_one_swap(datetime.date.fromisoformat('2017-02-07'), 'NXPI', 'JBHT', num_tickers_2017)

    # 3/20/2017 IDXX replaced SBAC
    _test_one_swap(datetime.date.fromisoformat('2017-03-20'), 'SBAC', 'IDXX', num_tickers_2017)

    # 4/24/2017 WYNN replaced TRIP
    _test_one_swap(datetime.date.fromisoformat('2017-04-24'), 'TRIP', 'WYNN', num_tickers_2017)

    # 6/19/2017 MELI replaced YHOO
    _test_one_swap(datetime.date.fromisoformat('2017-06-19'), 'YHOO', 'MELI', num_tickers_2017)

    # 10/23/2017 ALGN replaced MAT
    _test_one_swap(datetime.date.fromisoformat('2017-10-23'), 'MAT', 'ALGN', num_tickers_2017)

    # annual changes for 2017; effective Dec 18, 2017
    #  https://www.nasdaq.com/about/press-center/annual-changes-nasdaq-100-index-2
    dec_18_removals = frozenset(('AKAM', 'DISCA', 'DISCK', 'NCLH', 'TSCO', 'VIAB'))
    dec_18_additions = frozenset(('ASML', 'CDNS', 'SNPS', 'TTWO', 'WDAY'))

    tickers_dec_17 = tickers_as_of(2017, 12, 17)
    assert len(tickers_dec_17) == num_tickers_2017
    assert dec_18_removals.issubset(tickers_dec_17)
    assert tickers_dec_17.isdisjoint(dec_18_additions)

    tickers_dec_18 = tickers_as_of(2017, 12, 18)
    # this was a remove 6 and add 5 change due to two classes of Discovery Communications: DISCA and DISCK
    assert len(tickers_dec_18) == num_tickers_2017 - 1

    assert dec_18_additions.issubset(tickers_dec_18)
    assert tickers_dec_18.isdisjoint(dec_18_removals)
