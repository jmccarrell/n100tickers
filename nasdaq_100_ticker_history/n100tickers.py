"""Return the member companies of the NASDAQ 100 index as it has changed over time."""

import datetime
from functools import lru_cache
import importlib.resources
import yaml


@lru_cache
def _load_tickers_from_yaml(year: int = 2020) -> dict:
    """
    Load and return the data structure defining nasdaq constituents for the given year.
    """

    module_name = "nasdaq_100_ticker_history"
    resource_name = f"n100-ticker-changes-{year}.yml"
    if not importlib.resources.is_resource(module_name, resource_name):
        raise NotImplementedError(
            f"no nasdaq 100 tickers defined for {year}; cant find resource {resource_name}"
        )

    n100_tickers_yaml = importlib.resources.read_text(module_name, resource_name)
    return yaml.safe_load(n100_tickers_yaml)


def tickers_as_of(year: int = 2020, month: int = 1, day: int = 1) -> frozenset:
    """
    Return a frozenset of NASDAQ 100 tickers in the index as of a date.

    :param year: the year of the date for the query
    :param month: month
    :param day: day
    :return: a frozenset of ``str`` of symbol names in the index of of year, month, day.
    :rtype: frozenset

    >>> 'TSLA' in tickers_as_of(2020, 9, 1)
    True
    >>> len(tickers_as_of(2020, 9, 1)) == 103
    True
    """

    tickers = _load_tickers_from_yaml(year=year)
    dates = list(map(lambda d: datetime.date.fromisoformat(d), sorted(list(tickers["changes"].keys()))))
    query_date = datetime.date(year=year, month=month, day=day)
    result = tickers["tickers_on_Jan_1"]
    for d in dates:
        if d <= query_date:
            ops = tickers["changes"][d.isoformat()]
            assert len(ops["python_set_operators"]) == len(ops["rhs_operands"])
            for (op, rhs) in zip(ops["python_set_operators"], ops["rhs_operands"]):
                r = eval(f"result {op} {rhs}")
                result = r
    return frozenset(result)
