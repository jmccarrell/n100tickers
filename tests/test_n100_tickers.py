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


# def test_year_boundary_2021_2022() -> None:
#     _test_at_year_boundary(2022, 102)


# def test_2021_annual_changes() -> None:
#     num_tickers_2021_end_of_year = 102
#     # Annual 2021 changes
#     # https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-indexr-2021-12-10-0
#     #
#     # On December 10, 2021 Nasdaq announced that six new companies would join the index prior to the market open on December 20, 2021.
#     # They are Airbnb (ABNB), Datadog (DDOG), Fortinet (FTNT), Lucid Group (LCID), Palo Alto Networks (PANW), and Zscaler (ZS).
#     # They will replace CDW (CDW), Cerner (CERN), Check Point (CHKP), Fox Corporation (FOXA/FOX), Incyte (INCY), and Trip.com (TCOM).
#     # https://greenstocknews.com/news/nasdaq/lcid/annual-changes-to-the-nasdaq-100-index
#     assert len(tickers_as_of(2021, 12, 17)) == num_tickers_2021_end_of_year


def test_tickers_2021() -> None:
    num_tickers_2021 = 102

    # On July 21, Honeywell replaces Alexion
    _test_one_swap(datetime.date.fromisoformat('2021-07-21'), 'ALXN', 'HON', num_tickers_2021)

    # On Aug 26, Crowdstrike replaced Maxim Integrated Products, who is being acquired by Analog Devices.
    _test_one_swap(datetime.date.fromisoformat('2021-08-26'), 'MXIM', 'CRWD', num_tickers_2021)


def test_year_boundary_2020_2021() -> None:
    _test_at_year_boundary(2021, 102)


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


def test_2020_annual_changes() -> None:
    # Annual 2020 changes
    # https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-index-2020-12-11
    #
    # 6 companies added; 6 removed.  However, Liberty Global PLC has 2 symbols: (Nasdaq: LBTYA/LBTYK)
    # So total tickers change from 103 to 102.
    # Effective date: 2020-12-21
    assert len(tickers_as_of(2020, 12, 18)) == 103
    tickers_removed_12_21 = frozenset(('BMRN', 'CTXS', 'EXPE', 'LBTYA', 'LBTYK', 'TTWO', 'ULTA'))
    assert tickers_removed_12_21.issubset(tickers_as_of(2020, 12, 18))
    tickers_added_12_21 = frozenset(('AEP', 'MRVL', 'MTCH', 'OKTA', 'PTON', 'TEAM'))
    assert tickers_added_12_21.isdisjoint(tickers_as_of(2020, 12, 18))

    assert len(tickers_as_of(2020, 12, 21)) == 102
    assert tickers_removed_12_21.isdisjoint(tickers_as_of(2020, 12, 21))
    assert tickers_added_12_21.issubset(tickers_as_of(2020, 12, 21))


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


def test_year_boundary_2016_2017() -> None:
    _test_at_year_boundary(2017, 104)


def test_2016_annual_changes() -> None:
    # annual changes for 2016; effective Dec 19, 2016 announced Dec 9
    #  https://en.wikipedia.org/wiki/Nasdaq-100#Changes_in_2016
    dec_18_tickers = tickers_as_of(2016, 12, 18)
    dec_19_tickers = tickers_as_of(2016, 12, 19)
    assert len(dec_18_tickers) == len(dec_19_tickers)

    dec_19_removals = frozenset(('BBBY', 'NTAP', 'SRCL', 'WFM'))
    assert dec_19_removals.issubset(dec_18_tickers)
    assert dec_19_tickers.isdisjoint(dec_19_removals)

    dec_19_additions = frozenset(('CTAS', 'HAS', 'HOLX', 'KLAC'))
    assert dec_19_additions.isdisjoint(dec_18_tickers)
    assert dec_19_additions.issubset(dec_19_tickers)


def test_tickers_2016() -> None:
    num_tickers_2016_boy = 105   # num tickers at the start of 2016
    num_tickers_2016_eoy = 104   # number of tickers at the end of 2016

    assert len(tickers_as_of(2016, 1, 1)) == num_tickers_2016_boy
    assert len(tickers_as_of(2016, 12, 31)) == num_tickers_2016_eoy

    # https://ir.nasdaq.com/news-releases/news-release-details/csx-corporation-join-nasdaq-100-index-beginning-february-22-2016
    _test_one_swap(datetime.date.fromisoformat('2016-02-22'), 'KLAC', 'CSX', num_tickers_2016_boy)

    #  https://www.nasdaq.com/about/press-center/netease-inc-join-nasdaq-100-index-beginning-march-16-2016
    _test_one_swap(datetime.date.fromisoformat('2016-03-16'), 'SNDK', 'NTES', num_tickers_2016_boy)

    # adds BATRA, BATRK as of Apr 18; no replacements
    #  https://en.wikipedia.org/wiki/Nasdaq-100#cite_note-37
    apr_17_tickers = tickers_as_of(2016, 4, 17)
    assert len(apr_17_tickers) == 105
    apr_18_tickers = tickers_as_of(2016, 4, 18)
    assert len(apr_18_tickers) == 107

    apr_18_additions = frozenset(('BATRA', 'BATRK'))
    assert apr_18_additions.isdisjoint(apr_17_tickers)
    assert apr_18_additions.issubset(apr_18_tickers)

    # https://en.wikipedia.org/wiki/Nasdaq-100#cite_note-38
    #  this is a 4 for one change as of June 10
    jun_09_tickers = tickers_as_of(2016, 6, 9)
    assert len(jun_09_tickers) == 107
    jun_10_tickers = tickers_as_of(2016, 6, 10)
    assert len(jun_10_tickers) == 104

    jun_10_removals = frozenset(('LMCA', 'LMCK', 'BATRA', 'BATRK'))
    assert jun_10_removals.issubset(jun_09_tickers)
    assert jun_10_tickers.isdisjoint(jun_10_removals)

    jun_10_additions = frozenset(('XRAY',))
    assert jun_10_additions.isdisjoint(jun_09_tickers)
    assert jun_10_additions.issubset(jun_10_tickers)

    # https://en.wikipedia.org/wiki/Nasdaq-100#cite_note-39
    _test_one_swap(datetime.date.fromisoformat('2016-07-18'), 'ENDP', 'MCHP', num_tickers_2016_eoy)

    # https://en.wikipedia.org/wiki/Nasdaq-100#cite_note-40
    _test_one_swap(datetime.date.fromisoformat('2016-10-19'), 'LLTC', 'SHPG', num_tickers_2016_eoy)
