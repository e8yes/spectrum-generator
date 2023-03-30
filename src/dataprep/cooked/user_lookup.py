from pandas import DataFrame
from pandas import read_pickle
from typing import Dict


def LoadRawUserProfiles(file_path: str) -> DataFrame:
    """_summary_

    Args:
        file_path (str): _description_

    Returns:
        DataFrame: _description_
    """
    return read_pickle(file_path)


def BuildUserLookup(raw_user_profile: DataFrame) -> Dict[str, int]:
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

    return lookup
