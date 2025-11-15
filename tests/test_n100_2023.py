import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

num_tickers_2023 = 101


def test_year_boundary_2022_2023() -> None:
    _test_at_year_boundary(2023)


def test_dec_2023_changes() -> None:
    assert len(tickers_as_of(2023, 1, 1)) == num_tickers_2023
    assert len(tickers_as_of(2023, 10, 1)) == num_tickers_2023

    # On Dec 14, SeaGen (SGEN) was dropped after its merger with Pfizer, it was replaced by Take-Two
    # Interactive (TTWO).
    _test_one_swap(datetime.date.fromisoformat("2023-12-14"), "SGEN", "TTWO", num_tickers_2023)

    # On Dec 18, the annual re-ranking was applied:
    # Align Technology Inc (ALGN), eBay (EBAY), Enphase Energy (ENPH), JD.com (JD), Lucid Group (LCID) and
    # Zoom Video Communications (ZOOM) were dropped.
    assert len(tickers_as_of(2023, 12, 15)) == num_tickers_2023
    tickers_removed_2023_12_18 = frozenset(("ALGN", "EBAY", "ENPH", "JD", "LCID", "ZM"))
    assert tickers_removed_2023_12_18.issubset(tickers_as_of(2023, 12, 15))
    assert tickers_removed_2023_12_18.isdisjoint(tickers_as_of(2023, 12, 18))

    # CDW, Coca-Cola Europacific Partners (CCEP), DoorDash (DASH), MongoDB Inc (MDB), Roper Technologies
    # (ROP) and Splunk (SPLK) were added.
    tickers_added_2023_12_18 = frozenset(("CDW", "CCEP", "DASH", "MDB", "ROP", "SPLK"))
    assert tickers_added_2023_12_18.isdisjoint(tickers_as_of(2023, 12, 15))
    assert tickers_added_2023_12_18.issubset(tickers_as_of(2023, 12, 18))
    assert len(tickers_as_of(2023, 12, 18)) == num_tickers_2023


def test_jun_jul_2023_changes() -> None:
    # On June 7, GE HealthCare Technologies replaced Fiserv.
    # On June 20, Onsemi replaced Rivian.
    # On July 17, The Trade Desk replaced Activision Blizzard.
    assert len(tickers_as_of(2023, 1, 1)) == num_tickers_2023

    _test_one_swap(datetime.date.fromisoformat("2023-06-07"), "FISV", "GEHC", num_tickers_2023)
    _test_one_swap(datetime.date.fromisoformat("2023-06-20"), "RIVN", "ON", num_tickers_2023)
    _test_one_swap(datetime.date.fromisoformat("2023-07-17"), "ATVI", "TTD", num_tickers_2023)
