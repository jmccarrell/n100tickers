import datetime

from nasdaq_100_ticker_history import tickers_as_of

from .helpers import _test_at_year_boundary, _test_one_swap

# Annual changes 2022:
# On December 19, the annual re-ranking of the index took place prior to market open.
# The six stocks joining the index were CoStar Group, Rivian Automotive, Warner Bros. Discovery,
# GlobalFoundries, Baker Hughes, and Diamondback Energy.
# They replaced Baidu, DocuSign, Match Group, NetEase, Skyworks Solutions, Splunk, and Verisign.
# Dropping seven components allowed the Nasdaq-100 index to once again have 100 companies.

# there are 100 companies, but 101 tickers because of GOOG and GOOGL
initial_num_tickers_2022 = 101
mid_year_num_tickers_2022 = 102
final_num_tickers_2022 = 101


def test_year_boundary_2021_2022() -> None:
    _test_at_year_boundary(2022)


def test_2022_annual_changes() -> None:
    # on Dec 19, 7 were dropped, 6 were added
    assert len(tickers_as_of(2022, 12, 15)) == mid_year_num_tickers_2022
    tickers_removed_2022_12_19 = frozenset(("BIDU", "DOCU", "MTCH", "NTES", "SPLK", "SWKS", "VRSN"))
    assert tickers_removed_2022_12_19.issubset(tickers_as_of(2022, 12, 15))
    tickers_added_2022_12_19 = frozenset(("BKR", "CSGP", "FANG", "GFS", "RIVN", "WBD"))
    assert tickers_added_2022_12_19.isdisjoint(tickers_as_of(2022, 12, 15))

    assert len(tickers_as_of(2022, 12, 19)) == final_num_tickers_2022
    assert tickers_removed_2022_12_19.isdisjoint(tickers_as_of(2022, 12, 19))
    assert tickers_added_2022_12_19.issubset(tickers_as_of(2022, 12, 19))


def test_tickers_2022() -> None:
    assert len(tickers_as_of(2022, 1, 1)) == initial_num_tickers_2022

    # On Jan 24, Old Dominion replaces Peloton
    _test_one_swap(datetime.date.fromisoformat("2022-01-24"), "PTON", "ODFL", initial_num_tickers_2022)

    # On Feb 2, Excelon EXC split off Constellation Energy CEG, which remained in the index
    tickers_added_2022_02_02 = frozenset(("CEG",))
    assert tickers_added_2022_02_02.isdisjoint(tickers_as_of(2022, 2, 1))
    assert tickers_added_2022_02_02.issubset(tickers_as_of(2022, 2, 2))
    assert len(tickers_as_of(2022, 2, 2)) == mid_year_num_tickers_2022

    # AMD completed its acquisition of Xilinx XLNX on or about 14 Feb.
    # So AstraZeneca AZN replaces XLNX as of 22 Feb 2022.
    _test_one_swap(datetime.date.fromisoformat("2022-02-22"), "XLNX", "AZN", mid_year_num_tickers_2022)

    # On Jun 9, FB became META
    _test_one_swap(datetime.date.fromisoformat("2022-06-09"), "FB", "META", mid_year_num_tickers_2022)

    # On Nov 21, OKTA is replaced by Enphase Energy ENPH
    _test_one_swap(datetime.date.fromisoformat("2022-11-21"), "OKTA", "ENPH", mid_year_num_tickers_2022)
