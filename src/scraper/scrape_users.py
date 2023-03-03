import pandas as pd
import re
from os import listdir
from typing import List

from src.scraper.scrape_user_timeline import ScrapeUserTimeline


_USER_ID_RE = re.compile(pattern=".*twitter.com/(.+)")


def _ToTwitterUserId(link: str) -> str:
    """Extracts a user's twitter ID from the homepage link.

    Args:
        link (str): The user's twitter homepage link. e.g.
            https://twitter.com/SenatorBaldwin

    Returns:
        str: The user's twitter ID.
    """
    return _USER_ID_RE.match(string=link).group(1)


def ScrapedUserIds(output_dir: str) -> List[str]:
    """Returns a list of Twitter IDs that have already been scraped. A Twitter
    ID has been scraped if there is a file corresponding to the account in the
    specified output_dir.

    Args:
        output_dir (str): The directory to be analyzed.

    Returns:
        List[str]: A list of Twitter IDs that have already been scraped.
    """
    return listdir(path=output_dir)


def LoadTwitterUserIds(csv_file: str) -> List[str]:
    """Loads the list of Twitter user IDs from a CSV file. The CSV file has a
    column called "Link" where it contains a list of links to the homepages of
    Twitter users.

    Args:
        csv_file (str): File path to the CSV file.

    Returns:
        List[str]: A list of unique Twitter user IDs.
    """
    df = pd.read_csv(filepath_or_buffer=csv_file)
    user_ids = df["Link"].apply(_ToTwitterUserId).unique()
    return list(user_ids)


def ScrapeUsers(user_ids: List[str], output_dir: str) -> None:
    """Scrapes the twitter timeline of the specified users and persists them
    as pickle files. The filename of each pickle file is the user_id.

    Args:
        user_ids (List[str]): The list of Twitter user ids whose timeline is
            to be scraped.
        output_dir (str):  Directory under which the scraped timeline files are
            going to be stored.
    """
    for user_id in user_ids:
        ScrapeUserTimeline(user_id=user_id, output_dir=output_dir)
