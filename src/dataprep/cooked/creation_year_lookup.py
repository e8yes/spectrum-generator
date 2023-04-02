from json import dump
from json import load
from os import path
from pandas import DataFrame
from typing import Dict
from typing import List
from typing import Tuple


def _ToDict(years: List[int]) -> Dict[int, int]:
    result = dict()

    for i in range(len(years)):
        result[years[i]] = i

    return result


def _InvertDict(lookup: Dict[int, int]) -> Dict[int, int]:
    return {v: k for k, v in lookup.items()}


def BuildCreationYearLookup(raw_timelines: DataFrame) -> Tuple[Dict[int, int],
                                                               Dict[int, int]]:
    """_summary_

    Args:
        raw_timelines (DataFrame): _description_

    Returns:
        Tuple[Dict[int, int], Dict[int, int]]: _description_
    """
    creation_years = raw_timelines["creation_date"].\
        map(lambda date: date.year)
    year_set = creation_years.unique()
    year_set = sorted(year_set.tolist())

    lookup = _ToDict(years=year_set)
    inv_lookup = _InvertDict(lookup=lookup)

    return lookup, inv_lookup


def LoadYearIdLookup(input_path: str) -> Dict[int, int]:
    """_summary_

    Args:
        input_path (str): _description_
    """
    lookup_file = path.join(input_path, "year_lookup.json")

    with open(file=lookup_file, mode="r") as f:
        return load(fp=f)


def SaveYearIdLookup(lookup: Dict[int, int], output_path: str) -> None:
    """_summary_

    Args:
        lookup (Dict[int, int]): _description_
        output_path (str): _description_
    """
    lookup_file = path.join(output_path, "year_lookup.json")

    with open(file=lookup_file, mode="w") as f:
        return dump(obj=lookup, fp=f)
