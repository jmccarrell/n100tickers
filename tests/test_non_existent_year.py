import pytest
from nasdaq_100_ticker_history import tickers_as_of

def test_non_existent_year_raises(year: int = 2060) -> None:
    """
    Ensure we report a useful exception when asked for data we cannot provide.
    """
    with pytest.raises(NotImplementedError, match=f"no nasdaq 100 tickers defined for {year}"):
        tickers_as_of(year, 1, 1)
