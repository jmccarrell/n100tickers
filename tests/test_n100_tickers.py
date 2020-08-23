from n100_tickers import __version__, n100_tickers_set_for_date


def test_version():
    assert __version__ == '0.1.0'


def test_tickers_2020() -> None:
    tickers_2020_jan_1 = n100_tickers_set_for_date(2020, 1, 1)
    assert len(tickers_2020_jan_1) == 103

    #  On April 20, Dexcom replaced American Airlines Group in the index
    tickers_2020_apr_19 = n100_tickers_set_for_date(2020, 4, 19)
    assert len(tickers_2020_apr_19) == 103
    assert 'AAL' in tickers_2020_apr_19
    assert 'DXCM' not in tickers_2020_apr_19

    tickers_2020_apr_20 = n100_tickers_set_for_date(2020, 4, 20)
    assert len(tickers_2020_apr_20) == 103
    assert 'AAL' not in tickers_2020_apr_20
    assert 'DXCM' in tickers_2020_apr_20

    #  On April 30, Zoom Video Communications replaced Willis Towers Watson
    assert 'WLTW' in tickers_2020_apr_20
    assert 'ZM' not in tickers_2020_apr_20

    tickers_2020_apr_30 = n100_tickers_set_for_date(2020, 4, 30)
    assert len(tickers_2020_apr_30) == 103
    assert 'WLTW' not in tickers_2020_apr_30
    assert 'ZM' in tickers_2020_apr_30

    #  On June 22, DocuSign, Inc. (DOCU) will replace United Airlines Holdings, Inc. (Nasdaq: UAL)
    assert 'UAL' in tickers_2020_apr_30
    assert 'DOCU' not in tickers_2020_apr_30

    tickers_2020_jun_22 = n100_tickers_set_for_date(2020, 6, 22)
    assert len(tickers_2020_jun_22) == 103
    assert 'UAL' not in tickers_2020_jun_22
    assert 'DOCU' in tickers_2020_jun_22

    # On Jul 20, Moderna MRNA replaces CoStar Group CGSP
    #  https://www.globenewswire.com/news-release/2020/07/13/2061339/0/en/Moderna-Inc-to-Join-the-NASDAQ-100-Index-Beginning-July-20-2020.html
    assert 'MRNA' not in tickers_2020_jun_22
    assert 'CSGP' in tickers_2020_jun_22

    tickers_2020_jul_20 = n100_tickers_set_for_date(2020, 7, 20)
    assert len(tickers_2020_jul_20) == 103
    assert 'CSGP' not in tickers_2020_jul_20
    assert 'MRNA' in tickers_2020_jul_20

    # ensure we are consistent at year end / year beginning
    tickers_2019_dec_31 = n100_tickers_set_for_date(2019, 12, 31)
    assert tickers_2020_jan_1 == tickers_2019_dec_31


def test_tickers_2019() -> None:
    # 6 tickers added and removed on 12/23/2019
    #  https://finance.yahoo.com/news/annual-changes-nasdaq-100-index-010510822.html
    tickers_2019_dec_23 = n100_tickers_set_for_date(2019, 12, 23)
    assert len(tickers_2019_dec_23) == 103
    dec_23_removals = frozenset(('HAS', 'HSIC', 'JBHT', 'MYL', 'NLOK', 'WYNN'))
    assert tickers_2019_dec_23.isdisjoint(dec_23_removals)
    dec_23_additions = frozenset(('ANSS', 'CDW', 'CPRT', 'CSGP', 'SGEN', 'SPLK'))
    assert dec_23_additions.issubset(tickers_2019_dec_23)

    tickers_2019_dec_20 = n100_tickers_set_for_date(2019, 12, 20)
    assert len(tickers_2019_dec_20) == 103
    assert dec_23_removals.issubset(tickers_2019_dec_20)
    assert tickers_2019_dec_20.isdisjoint(dec_23_additions)

    # 1 swap Nov 19
    #  https://www.nasdaq.com/press-release/exelon-corporation-to-join-the-nasdaq-100-index-beginning-november-21-2019-2019-11-18
    tickers_2019_nov_19 = n100_tickers_set_for_date(2019, 11, 19)
    assert len(tickers_2019_nov_19) == 103
    assert 'CELG' not in tickers_2019_nov_19
    assert 'EXC' in tickers_2019_nov_19
    tickers_2019_nov_18 = n100_tickers_set_for_date(2019, 11, 18)
    assert len(tickers_2019_nov_18) == 103
    assert 'CELG' in tickers_2019_nov_18
    assert 'EXC' not in tickers_2019_nov_18

    # there was a record of 21st Century Fox changing to Fox Corp.  But as near as I can tell, the ticker symbols were the same.


def test_tickers_2018() -> None:
    # 6 tickers added and removed on 12/24/2018
    #  https://www.nasdaq.com/about/press-center/annual-changes-nasdaq-100-index-0
    tickers_2018_dec_23 = n100_tickers_set_for_date(2018, 12, 23)
    assert len(tickers_2018_dec_23) == 103

    tickers_2018_dec_24 = n100_tickers_set_for_date(2018, 12, 24)
    assert len(tickers_2018_dec_24) == 103

    dec_24_removals = frozenset(('ESRX', 'HOLX', 'QRTEA', 'SHPG', 'STX', 'VOD'))
    assert dec_24_removals.issubset(tickers_2018_dec_23)
    assert tickers_2018_dec_24.isdisjoint(dec_24_removals)
    dec_24_additions = frozenset(('AMD', 'LULU', 'NTAP', 'UAL', 'VRSN', 'WLTW'))
    assert dec_24_additions.issubset(tickers_2018_dec_24)

    # 11/19/2018 XEL replaces XRAY
    #  https://www.nasdaq.com/about/press-center/xcel-energy-inc-join-nasdaq-100-index-beginning-november-19-2018
    tickers_2018_nov_18 = n100_tickers_set_for_date(2018, 11, 18)
    assert len(tickers_2018_nov_18) == 103
    tickers_2018_nov_19 = n100_tickers_set_for_date(2018, 11, 19)
    assert len(tickers_2018_nov_19) == 103

    nov_19_removals = frozenset(('XRAY',))
    assert nov_19_removals.issubset(tickers_2018_nov_18)
    assert nov_19_removals.isdisjoint(tickers_2018_nov_19)
    nov_19_additions = frozenset(('XEL',))
    nov_19_additions.issubset(tickers_2018_nov_19)
    nov_19_additions.isdisjoint(tickers_2018_nov_18)

    # 11/5/2018 NXPI replaces CA
    #  (link broken): https://business.nasdaq.com/mediacenter/pressreleases/1831989/nxp-semiconductors-nv-to-join-the-nasdaq-100-index-beginning-november-5-2018
    tickers_2018_nov_4 = n100_tickers_set_for_date(2018, 11, 4)
    assert len(tickers_2018_nov_4) == 103

    nov_5_removals = frozenset(('CA',))
    assert nov_5_removals.issubset(tickers_2018_nov_4)
    assert nov_5_removals.isdisjoint(tickers_2018_nov_18)
    nov_5_additions = frozenset(('NXPI',))
    assert nov_5_additions.issubset(tickers_2018_nov_18)
    assert nov_5_additions.isdisjoint(tickers_2018_nov_4)

    # 7/23/2018 PEP replaces DISH
    tickers_2018_jul_22 = n100_tickers_set_for_date(2018, 7, 22)
    assert len(tickers_2018_jul_22) == 103

    jul_23_removals = frozenset(('DISH',))
    assert jul_23_removals.issubset(tickers_2018_jul_22)
    assert jul_23_removals.isdisjoint(tickers_2018_nov_4)
    jul_23_additions = frozenset(('PEP',))
    assert jul_23_additions.issubset(tickers_2018_nov_4)
    assert jul_23_additions.isdisjoint(tickers_2018_jul_22)
