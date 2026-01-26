import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2026 = 101


def test_year_boundary_2025_2026() -> None:
    assert len(tickers_as_of(2026, 1, 1)) == num_tickers_2026
    _test_at_year_boundary(2026)


def test_jan_2026_vsnt_spinoff_and_removal() -> None:
    # VSNT added on Jan 5 (spin-off from Comcast)
    tickers_before_add = tickers_as_of(2026, 1, 4)
    tickers_after_add = tickers_as_of(2026, 1, 5)
    assert len(tickers_before_add) == num_tickers_2026
    assert len(tickers_after_add) == num_tickers_2026 + 1
    assert "VSNT" in tickers_after_add

    # VSNT removed on Jan 9 (failed weight requirements)
    tickers_before_rem = tickers_as_of(2026, 1, 8)
    tickers_after_rem = tickers_as_of(2026, 1, 9)
    assert len(tickers_before_rem) == num_tickers_2026 + 1
    assert len(tickers_after_rem) == num_tickers_2026
    assert "VSNT" not in tickers_after_rem


def test_jan_2026_wmt_azn_swap() -> None:
    # On Jan 20, Walmart (WMT) replaced AstraZeneca (AZN)
    _test_one_swap(datetime.date.fromisoformat("2026-01-20"), "AZN", "WMT", num_tickers_2026)
