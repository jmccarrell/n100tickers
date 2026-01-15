import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2026 = 102


def test_year_boundary_2025_2026() -> None:
    assert len(tickers_as_of(2026, 1, 1)) == num_tickers_2026
    _test_at_year_boundary(2026)
