from pandas import DataFrame
from json import dump
from json import load
from os import path
from typing import Dict
from typing import Tuple


def BuildUserLookup(
        raw_user_profile: DataFrame) -> Tuple[Dict[str, int], Dict[int, str]]:
    """_summary_

    Args:
        raw_user_profile (DataFrame): _description_

    Returns:
        Dict[str, int]: _description_
    """
    user_names = raw_user_profile["user_name"].to_list()
    user_names = sorted(user_names)

    lookup = dict()
    user_id = 0
    for user_name in user_names:
        lookup[user_name] = user_id
        user_id += 1

    inv_lookup = {v: k for k, v in lookup.items()}

    return lookup, inv_lookup


def UserNameToId(user_name: str, user_lookup: Dict[str, int]) -> int:
    """_summary_

    Args:
        user_name (str): _description_
        user_lookup (Dict[str, int]): _description_

    Returns:
        int: _description_
    """
    if user_name not in user_lookup:
        return None

    return user_lookup[user_name]


def LoadUserLookup(input_path: str) -> Dict[int, str]:
    """_summary_

    Args:
        input_path (str): _description_

    Returns:
        Dict[str, int]: _description_
    """
    lookup_file = path.join(input_path, "user_lookup.json")

    with open(file=lookup_file, mode="r") as f:
        return load(fp=f)


def SaveUserLookup(lookup: Dict[int, str], output_path: str) -> None:
    """_summary_

    Args:
        lookup (Dict[str, int]): _description_
        output_path (str): _description_
    """
    lookup_file = path.join(output_path, "user_lookup.json")

    with open(file=lookup_file, mode="w") as f:
        dump(obj=lookup, fp=f)
