from nasdaq_100_ticker_history import tickers_as_of


def test_basics() -> None:
    assert "AMZN" in tickers_as_of(2020, 6, 1)
    assert len(tickers_as_of(2020, 6, 1)) >= 100