"functions to help compute over the nasdaq 100"
import datetime
from functools import lru_cache
import importlib.resources
import yaml
from typing import Iterable


def n100_tickers_sorted_for_date(year: int = 2020, month: int = 1, day: int = 1) -> Iterable[str]:
    """return the nasdaq 100 ticker symbols in sorted order as of the date passed in."""

    tickers = list(n100_tickers_set_for_date(year=year, month=month, day=day))
    return (t for t in sorted(tickers))


@lru_cache
def _load_tickers_from_yaml(year: int = 2020) -> dict:
    """load from the file system, parse, and return the structure defining the set operations to compute the
    constituents of the nasdaq 100 index for any date in the given year

    """
    module_name = "n100_tickers"
    resource_name = f"n100-ticker-changes-{year}.yml"
    if not importlib.resources.is_resource(module_name, resource_name):
        raise NotImplementedError(
            f"no nasdaq 100 tickers defined for {year}; cant find resource {resource_name}"
        )

    n100_tickers_yaml = importlib.resources.read_text(module_name, resource_name)
    return yaml.safe_load(n100_tickers_yaml)


def n100_tickers_set_for_date(year: int = 2020, month: int = 1, day: int = 1) -> frozenset:
    """given a calendar date, return the set of nasdaq 100 tickers in the index on that date"""

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
