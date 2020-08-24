"""functions that return date-aware consituents of the NASDAQ 100 index."""

import datetime
from functools import lru_cache
import importlib.resources
import yaml
from typing import Iterable


def n100_tickers_sorted_for_date(year: int = 2020, month: int = 1, day: int = 1) -> Iterable[str]:
    """
    Return the nasdaq 100 ticker symbols in sorted order as of the date.

    :param year: the year of the date for the query
    :param month: month
    :param day: days

    :returns: an iterator that returns the ticker symbols in sorted order.


    >>> next(n100_tickers_sorted_for_date(2020, 6, 1))
    'AAPL'
    """

    tickers = list(n100_tickers_set_for_date(year=year, month=month, day=day))
    return (t for t in sorted(tickers))


@lru_cache
def _load_tickers_from_yaml(year: int = 2020) -> dict:
    """load from the file system, parse, and return the structure defining the set operations to compute the
    constituents of the nasdaq 100 index for any date in the given year

    """
    module_name = "n100tickers"
    resource_name = f"n100-ticker-changes-{year}.yml"
    if not importlib.resources.is_resource(module_name, resource_name):
        raise NotImplementedError(
            f"no nasdaq 100 tickers defined for {year}; cant find resource {resource_name}"
        )

    n100_tickers_yaml = importlib.resources.read_text(module_name, resource_name)
    return yaml.safe_load(n100_tickers_yaml)


def n100_tickers_set_for_date(year: int = 2020, month: int = 1, day: int = 1) -> frozenset:
    """
    Return a frozenset of NASDAQ 100 tickers in the index as of a date.

    :param year: the year of the date for the query
    :param month: month
    :param day: days
    :return: a set of ``str`` of symbol names in the index of of year, month, day.
    :rtype: frozenset

    >>> 'AMZN' in n100_tickers_set_for_date(2020, 6, 1)
    True
    >>> len(n100_tickers_set_for_date(2020, 6, 1)) >= 100
    True
    """

    tickers = _load_tickers_from_yaml(year=year)
    dates = list(map(lambda d: datetime.date.fromisoformat(d), sorted(list(tickers["changes"].keys()))))
    query_date = datetime.date(year=year, month=month, day=day)
    result = tickers["base_set"]
    for d in dates:
        if d <= query_date:
            ops = tickers["changes"][d.isoformat()]
            assert len(ops["python_set_operators"]) == len(ops["rhs_operands"])
            for (op, rhs) in zip(ops["python_set_operators"], ops["rhs_operands"]):
                r = eval(f"result {op} {rhs}")
                result = r
    return frozenset(result)
