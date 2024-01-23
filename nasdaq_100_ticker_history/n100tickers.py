"""Return the member companies of the NASDAQ 100 index as it has changed over time."""

import datetime
from functools import lru_cache
import importlib.resources
from strictyaml import load, Map, MapPattern, Optional, Str, Int, UniqueSeq

changes_schema = Map({Optional("union"): UniqueSeq(Str()),
                      Optional("difference"): UniqueSeq(Str())})

date_schema = MapPattern(Str(),
                         changes_schema)

ticker_schema = Map({"year": Int(),
                     "tickers_on_Jan_1": UniqueSeq(Str()),
                     Optional("changes"): date_schema,
                     })


@lru_cache
def _load_tickers_from_yaml(year: int = 2020) -> dict:
    """
    Load and return the dictionary defining nasdaq constituents for the given year.
    """

    module_name = "nasdaq_100_ticker_history"
    resource_name = f"n100-ticker-changes-{year}.yaml"
    resource = importlib.resources.files(module_name).joinpath(resource_name)

    if not resource.exists():
        raise NotImplementedError(
            f"no nasdaq 100 tickers defined for {year}; "
            "cant find resource {resource_name} in package {module_name}"
        )

    n100_tickers_yaml = resource.read_text(encoding="utf-8")
    return load(n100_tickers_yaml, ticker_schema).data


def tickers_as_of(year: int = 2020, month: int = 1, day: int = 1) -> frozenset:
    """
    Return a frozenset of NASDAQ 100 tickers in the index as of a date.

    :param year: the year of the date for the query
    :param month: month
    :param day: day
    :return: a frozenset of ``str`` of symbol names in the index as of year, month, day.
    :rtype: frozenset

    >>> 'TSLA' in tickers_as_of(2020, 9, 1)
    True
    >>> len(tickers_as_of(2020, 9, 1)) == 103
    True
    """

    tickers = _load_tickers_from_yaml(year=year)
    result = set(tickers["tickers_on_Jan_1"])
    query_date = datetime.date(year=year, month=month, day=day)
    if "changes" in tickers:  # changes are optional
        dates = list(map(datetime.date.fromisoformat, sorted(list(tickers["changes"].keys()))))
        for d in dates:
            if d <= query_date:
                ops = tickers["changes"][d.isoformat()]
                for k in ops.keys():
                    rhs = set(ops[k])
                    match k:
                        case 'union':
                            rhs_code = "result.union(rhs)"
                        case 'difference':
                            rhs_code = "result.difference(rhs)"
                        case _:
                            raise NotImplementedError(
                                f"unknown set operation: {k} in changes {d}")
                    r = eval(rhs_code)
                    result = r
    return frozenset(result)
