"""Return the member companies of the NASDAQ 100 index as it has changed over time."""

import datetime
import importlib.resources
from functools import lru_cache
from importlib.resources.abc import Traversable
from typing import cast

from strictyaml import Int, Map, MapPattern, Optional, Str, UniqueSeq, load

changes_schema = Map({Optional("union"): UniqueSeq(Str()), Optional("difference"): UniqueSeq(Str())})

date_schema = MapPattern(
    Str(),  # date of change encoded as YYYY-MM-DD
    changes_schema,
)

ticker_schema = Map(
    {
        "year": Int(),
        "tickers_on_Jan_1": UniqueSeq(Str()),
        Optional("changes"): date_schema,
    }
)


@lru_cache
def _load_tickers_from_yaml(year: int = 2020) -> dict:
    """
    Load and return the dictionary defining nasdaq constituents for the given year.
    """

    module_name = "nasdaq_100_ticker_history"
    resource_name = f"n100-ticker-changes-{year}.yaml"
    resource: Traversable = importlib.resources.files(module_name).joinpath(resource_name)

    if not resource.is_file():
        raise NotImplementedError(
            f"no nasdaq 100 tickers defined for {year}; "
            f"cant find resource {resource_name} in package {module_name}"
        )

    n100_tickers_yaml = resource.read_text(encoding="utf-8")
    return cast(dict, load(n100_tickers_yaml, ticker_schema).data)


def tickers_as_of(year: int = 2020, month: int = 1, day: int = 1) -> frozenset:
    """
    Return a frozenset of NASDAQ 100 tickers in the index as of a date.

    :param year: the year of the date for the query
    :param month: month
    :param day: day
    :return: a frozenset of ``str`` of symbol names in the index as of year, month, day.
    :rtype: frozenset

    >>> "TSLA" in tickers_as_of(2020, 9, 1)
    True
    >>> len(tickers_as_of(2020, 9, 1)) == 103
    True
    """

    tickers_year = _load_tickers_from_yaml(year=year)
    result = set(tickers_year["tickers_on_Jan_1"])
    if "changes" in tickers_year:  # pragma: no branch.  Needed as every year has changes.
        # changes happen sometime later in the year.
        query_date = datetime.date(year=year, month=month, day=day)
        for d in list(map(datetime.date.fromisoformat, sorted(list(tickers_year["changes"].keys())))):
            if d <= query_date:
                ops = tickers_year["changes"][d.isoformat()]
                for operation, operands in ops.items():
                    tickers = set(operands)
                    if operation == "union":
                        result = result.union(tickers)
                    elif operation == "difference":
                        result = result.difference(tickers)
                    else:  # pragma: no cover
                        raise NotImplementedError(f"unknown set operation: {operation} in changes {d}")
    return frozenset(result)
