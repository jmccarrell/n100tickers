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


def test_apr_2026_sndk_team_swap() -> None:
    # On Apr 20, Sandisk (SNDK) replaced Atlassian (TEAM)
    _test_one_swap(datetime.date.fromisoformat("2026-04-20"), "TEAM", "SNDK", num_tickers_2026)


def test_may_2026_lite_csgp_swap() -> None:
    # On May 18, Lumentum (LITE) replaced CoStar Group (CSGP)
    _test_one_swap(datetime.date.fromisoformat("2026-05-18"), "CSGP", "LITE", num_tickers_2026)


def test_jun_2026_quarterly_reconstitution() -> None:
    # On Jun 22, 2026, quarterly reconstitution:
    # Removed: CHTR, CTSH, INSM, VRSK, ZS
    # Added: ALAB, CRWV, NBIS, RKLB, TER
    # Source: https://ir.nasdaq.com/news-releases/news-release-details/nasdaq-100-indexr-june-2026-quarterly-changes
    tickers_before = tickers_as_of(2026, 6, 21)
    tickers_after = tickers_as_of(2026, 6, 22)

    # Total should remain 101 (5 removed, 5 added)
    assert len(tickers_before) == num_tickers_2026
    assert len(tickers_after) == num_tickers_2026

    # Verify removals
    removed = {"CHTR", "CTSH", "INSM", "VRSK", "ZS"}
    for ticker in removed:
        assert ticker in tickers_before
        assert ticker not in tickers_after

    # Verify additions
    added = {"ALAB", "CRWV", "NBIS", "RKLB", "TER"}
    for ticker in added:
        assert ticker not in tickers_before
        assert ticker in tickers_after


def test_jun_2026_hona_spinoff() -> None:
    # On Jun 29, Honeywell Aerospace (HONA) spun off from Honeywell International,
    # which renamed itself Honeywell Technologies and kept HON.  Both are members,
    # and nothing was removed, so the index grew to 102.
    tickers_before = tickers_as_of(2026, 6, 28)
    tickers_after = tickers_as_of(2026, 6, 29)
    assert len(tickers_before) == num_tickers_2026
    assert len(tickers_after) == num_tickers_2026 + 1
    assert "HONA" not in tickers_before
    assert "HONA" in tickers_after
    assert "HON" in tickers_after


def test_jul_2026_spcx_addition() -> None:
    # SpaceX (SPCX) joined before market open on Jul 7 under the fast-track rule for
    # newly public megacaps.  Nothing was removed, so the index grew to 103.
    # Source: https://ir.nasdaq.com/news-releases/news-release-details/space-exploration-technologies-corporation-join-nasdaq-100
    tickers_before = tickers_as_of(2026, 7, 6)
    tickers_after = tickers_as_of(2026, 7, 7)
    assert len(tickers_before) == num_tickers_2026 + 1
    assert len(tickers_after) == num_tickers_2026 + 2
    assert "SPCX" not in tickers_before
    assert "SPCX" in tickers_after


def test_aug_2026_ea_removal() -> None:
    # Electronic Arts (EA) left the index on Aug 4 with no replacement, taking it
    # from 103 to 102.
    tickers_before = tickers_as_of(2026, 8, 3)
    tickers_after = tickers_as_of(2026, 8, 4)
    assert len(tickers_before) == num_tickers_2026 + 2
    assert len(tickers_after) == num_tickers_2026 + 1
    assert "EA" in tickers_before
    assert "EA" not in tickers_after
