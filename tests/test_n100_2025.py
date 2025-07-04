import datetime
from nasdaq_100_ticker_history import tickers_as_of
from .helpers import _test_one_swap, _test_at_year_boundary

num_tickers_2025 = 101


def test_year_boundary_2024_2025() -> None:
    assert len(tickers_as_of(2025, 1, 1)) == num_tickers_2025
    _test_at_year_boundary(2025)


def test_may_2025_shop_mdb_swap() -> None:
    # On May 19, Shopify (SHOP) replaced MongoDB (MDB) in the index
    _test_one_swap(
        datetime.date.fromisoformat("2025-05-19"), "MDB", "SHOP", num_tickers_2025
    )
