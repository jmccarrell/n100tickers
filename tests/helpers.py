import datetime

from nasdaq_100_ticker_history import tickers_as_of


def _test_one_swap(
    as_of_date: datetime.date, removed_ticker: str, added_ticker: str, expected_number_of_tickers: int
) -> None:
    tickers_on_change_date = tickers_as_of(as_of_date.year, as_of_date.month, as_of_date.day)
    assert len(tickers_on_change_date) == expected_number_of_tickers
    before_change_date = as_of_date - datetime.timedelta(days=1)
    tickers_before_change_date = tickers_as_of(
        before_change_date.year, before_change_date.month, before_change_date.day
    )
    assert len(tickers_before_change_date) == expected_number_of_tickers

    assert removed_ticker in tickers_before_change_date
    assert added_ticker not in tickers_before_change_date
    assert removed_ticker not in tickers_on_change_date
    assert added_ticker in tickers_on_change_date


def _test_at_year_boundary(year: int) -> None:
    """prove the tickers at the beginning of the year match the set at the end of the
    previous year.
    """
    begin_of_current_year = datetime.date.fromisoformat(f"{year}-01-01")
    end_of_previous_year = begin_of_current_year - datetime.timedelta(days=1)

    current_tickers = tickers_as_of(
        begin_of_current_year.year, begin_of_current_year.month, begin_of_current_year.day
    )
    previous_tickers = tickers_as_of(
        end_of_previous_year.year, end_of_previous_year.month, end_of_previous_year.day
    )
    assert previous_tickers == current_tickers
