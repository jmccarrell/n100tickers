import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2003 = 100


def test_year_boundary_2003_2004() -> None:
    _test_at_year_boundary(2004)


def test_tickers_2003() -> None:
    # Biogen Idec: IDEC's symbol changed to BIIB, Biogen left, and SanDisk took its place.
    before = tickers_as_of(2003, 11, 12)
    on = tickers_as_of(2003, 11, 13)
    assert {"BGEN", "IDPH"} <= before and not {"BIIB", "SNDK"} & before
    assert {"BIIB", "SNDK"} <= on and not {"BGEN", "IDPH"} & on
    _test_one_swap(datetime.date.fromisoformat("2003-05-01"), "TMPW", "MNST", num_tickers_2003)
