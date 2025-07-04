import datetime
from nasdaq_100_ticker_history import tickers_as_of
from .helpers import _test_one_swap, _test_at_year_boundary

num_tickers_2024 = 101


def test_year_boundary_2023_2024() -> None:
    _test_at_year_boundary(2024)


def test_dec_2024_changes() -> None:
    """test the expected annual changes at end of 2024."""

    # On December 13, as part of the annual reconstitution of the index, Nasdaq
    # announced that three new companies would join the index prior to the
    # market open on December 23, 2024. They are Palantir Technologies,
    # MicroStrategy and Axon Enterprise. They will replace Illumina, Moderna,
    # and Supermicro.
    before_date = tuple((2024, 12, 20))
    effective_date = tuple((2024, 12, 23))

    assert len(tickers_as_of(*before_date)) == num_tickers_2024
    tickers_removed = frozenset(("ILMN", "MRNA", "SMCI"))
    assert tickers_removed.issubset(tickers_as_of(*before_date))
    assert tickers_removed.isdisjoint(tickers_as_of(*effective_date))

    tickers_added = frozenset(("AXON", "MSTR", "PLTR"))
    assert tickers_added.isdisjoint(tickers_as_of(*before_date))
    assert tickers_added.issubset(tickers_as_of(*effective_date))
    assert len(tickers_as_of(*effective_date)) == num_tickers_2024


def test_2024_wba_smci_swap() -> None:
    # On July 22, Supermicro replaced Walgreens Boots Alliance as WBA no longer met minimum weighting standards.
    _test_one_swap(datetime.date.fromisoformat("2024-07-22"), "WBA", "SMCI", num_tickers_2024)


def test_2024_arm_siri_swap() -> None:
    # On June 24, ARM Holdings (ARM) replaced SiriusXM Radio as SiriusXM failed to meet minimum standards
    _test_one_swap(datetime.date.fromisoformat("2024-06-24"), "SIRI", "ARM", num_tickers_2024)


def test_2024_linde_splunk_swap() -> None:
    # On March 18, Linde plc replaced Splunk after Cisco Systems completed Splunk acquisition.
    # https://en.wikipedia.org/wiki/Nasdaq-100#cite_ref-80
    _test_one_swap(datetime.date.fromisoformat("2024-03-18"), "SPLK", "LIN", num_tickers_2024)
