import datetime
from nasdaq_100_ticker_history import tickers_as_of
from .helpers import _test_one_swap, _test_at_year_boundary

num_tickers_2021_end_of_year = 101
num_tickers_2021 = 102


def test_year_boundary_2020_2021() -> None:
    _test_at_year_boundary(2021)


def test_2021_annual_changes() -> None:
    # Annual 2021 changes
    # https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-indexr-2021-12-10-0
    #
    # On December 10, 2021 Nasdaq announced that six new companies would join the index
    #  prior to the market open on December 20, 2021.
    # They are Airbnb (ABNB), Datadog (DDOG), Fortinet (FTNT), Lucid Group (LCID),
    #   Palo Alto Networks (PANW), and Zscaler (ZS).
    # They will replace CDW (CDW), Cerner (CERN), Check Point (CHKP), Fox Corporation (FOXA/FOX),
    #  Incyte (INCY), and Trip.com (TCOM).
    # https://greenstocknews.com/news/nasdaq/lcid/annual-changes-to-the-nasdaq-100-index
    # This removes 7 tickers while adding 6, so total number of tickers goes to 101
    assert len(tickers_as_of(2021, 12, 17)) == num_tickers_2021
    tickers_removed_2021_12_20 = frozenset(("CDW", "CERN", "CHKP", "FOX", "FOXA", "INCY", "TCOM"))
    assert tickers_removed_2021_12_20.issubset(tickers_as_of(2021, 12, 17))
    tickers_added_2021_12_20 = frozenset(("ABNB", "DDOG", "FTNT", "LCID", "PANW", "ZS"))
    assert tickers_added_2021_12_20.isdisjoint(tickers_as_of(2021, 12, 17))

    assert len(tickers_as_of(2021, 12, 20)) == num_tickers_2021_end_of_year
    assert tickers_removed_2021_12_20.isdisjoint(tickers_as_of(2021, 12, 20))
    assert tickers_added_2021_12_20.issubset(tickers_as_of(2021, 12, 20))


def test_tickers_2021() -> None:
    # On July 21, Honeywell replaces Alexion
    _test_one_swap(datetime.date.fromisoformat("2021-07-21"), "ALXN", "HON", num_tickers_2021)

    # On Aug 26, Crowdstrike replaced Maxim Integrated Products, who is being acquired by Analog Devices.
    _test_one_swap(datetime.date.fromisoformat("2021-08-26"), "MXIM", "CRWD", num_tickers_2021)
