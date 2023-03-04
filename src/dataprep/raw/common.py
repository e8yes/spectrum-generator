import pickle
from os.path import basename
from os.path import join
from os import listdir
from snscrape.modules.twitter import Tweet
from typing import List
from typing import Tuple


def LoadRawTimeline(raw_timeline_file: str) -> Tuple[str, List[Tweet]]:
    """Loads the timeline of a Twitter user from his raw timeline file.

    Args:
        raw_timeline_file (str): Path to the raw timeline file.

    Returns:
        Tuple[str, List[Tweet]]: A tuple containing
            (user name, list of tweets).
    """
    with open(file=raw_timeline_file, mode="rb") as f:
        return basename(raw_timeline_file), pickle.load(file=f)


def RawTimelineFiles(raw_timeline_dir: str) -> List[str]:
    """Finds the path of the list of raw timeline files in the specified
    directory.

    Args:
        raw_timeline_dir (str): The directory to be searched.

    Returns:
        List[str]: A list of raw timeline files.
    """
    raw_timeline_file_names = listdir(path=raw_timeline_dir)
    return [join(raw_timeline_dir, file_name)
            for file_name in raw_timeline_file_names]
