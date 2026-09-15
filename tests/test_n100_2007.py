import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2007_boy = 100  # num tickers at the start of 2007
num_tickers_2007_eoy = 100  # number of tickers at the end of 2007


def test_year_boundary_2007_2008() -> None:
    _test_at_year_boundary(2008)


def test_membership_at_start_of_coverage() -> None:
    """Anchor the backward extension: the whole index on Feb 14, 2007, as the
    Nasdaq-100 article listed it that day. Every other set in the years this
    package covers is derived by walking changes away from this one."""

    feb_14_tickers = frozenset(
        """
        AAPL ADBE ADSK AEOS AKAM ALTR AMAT AMGN AMLN AMZN APOL ATVI BBBY BEAS BIIB BMET BRCM CDNS CDWC
        CELG CHKP CHRW CKFR CMCSA COST CSCO CTAS CTSH CTXS DELL DISCA DISH EBAY ERIC ERTS ESRX EXPD EXPE
        FAST FISV FLEX GENZ GILD GOOG GRMN IACI INFY INTC INTU ISRG JNPR JOYG KLAC LAMR LBTYA LINTA LLTC
        LOGI LRCX LVLT MCHP MEDI MICC MNST MRVL MSFT MXIM NIHD NTAP NTLI NVDA ORCL PAYX PCAR PDCO PETM
        PTEN QCOM RIMM ROST RYAAY SBUX SEPR SHLD SIAL SIRI SNDK SPLS SUNW SYMC TEVA TLAB VRSN VRTX WFMI
        WYNN XLNX XMSR XRAY YHOO
        """.split()
    )
    assert len(feb_14_tickers) == 100
    assert tickers_as_of(2007, 2, 14) == feb_14_tickers


def test_tickers_2007() -> None:
    assert len(tickers_as_of(2007, 1, 1)) == num_tickers_2007_boy
    assert len(tickers_as_of(2007, 12, 31)) == num_tickers_2007_eoy

    _test_one_swap(datetime.date.fromisoformat("2007-02-01"), "CMVT", "LOGI", num_tickers_2007_boy)
    _test_one_swap(datetime.date.fromisoformat("2007-02-14"), "APCC", "RYAAY", num_tickers_2007_boy)
    _test_one_swap(datetime.date.fromisoformat("2007-03-08"), "AEOS", "UAUA", num_tickers_2007_boy)
    _test_one_swap(datetime.date.fromisoformat("2007-06-01"), "MEDI", "CEPH", num_tickers_2007_boy)
    _test_one_swap(datetime.date.fromisoformat("2007-07-12"), "BMET", "FWLT", num_tickers_2007_boy)

    # both pairs are ticker changes: NTL became Virgin Media, Sun Microsystems became JAVA
    before = tickers_as_of(2007, 8, 26)
    on = tickers_as_of(2007, 8, 27)
    removals = frozenset(("NTLI", "SUNW"))
    assert removals.issubset(before)
    assert on.isdisjoint(removals)
    additions = frozenset(("JAVA", "VMED"))
    assert additions.isdisjoint(before)
    assert additions.issubset(on)
    assert len(on) == len(before) - 2 + 2

    # Maxim was suspended from Nasdaq over delinquent filings; it rejoins in Dec 2008.
    _test_one_swap(datetime.date.fromisoformat("2007-10-02"), "MXIM", "HSIC", num_tickers_2007_boy)
    _test_one_swap(datetime.date.fromisoformat("2007-10-08"), "CDWC", "LEAP", num_tickers_2007_boy)
    _test_one_swap(datetime.date.fromisoformat("2007-12-04"), "CKFR", "BIDU", num_tickers_2007_boy)

    before = tickers_as_of(2007, 12, 23)
    on = tickers_as_of(2007, 12, 24)
    removals = frozenset(("ERIC", "PTEN", "ROST", "SEPR", "XMSR"))
    assert removals.issubset(before)
    assert on.isdisjoint(removals)
    additions = frozenset(("FMCN", "HANS", "HOLX", "SRCL", "STLD"))
    assert additions.isdisjoint(before)
    assert additions.issubset(on)
    assert len(on) == len(before) - 5 + 5
