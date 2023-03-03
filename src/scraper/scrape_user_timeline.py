import logging
import pickle
import re
from os import path
from snscrape.modules.twitter import TwitterSearchScraper


_USER_ID_RE = re.compile(pattern=".*://twitter.com/(.+)")


def UserTwitterId(link: str) -> str:
    """Extracts a user's twitter ID from the homepage link.

    Args:
        link (str): The user's twitter homepage link. e.g.
            https://twitter.com/SenatorBaldwin

    Returns:
        str: The user's twitter ID.
    """
    match = _USER_ID_RE.match(string=link)
    return match.group(1)


def ScrapeUserTimeline(user_id: str, output_dir: str) -> None:
    """Scrapes the twitter timeline of the specified user and persists each
    tweet as a pickle file. The format of the file goes as follow:
        {user_id}.{date}

    Args:
        user_id (str): Twitter ID of the user whose timeline is to be scraped.
        output_dir (str): Directory under which the scraped tweet files are
            going to be stored.
    """
    timeline_query = "from:{user_id}".format(user_id=user_id)
    cursor = TwitterSearchScraper(timeline_query).get_items()

    for i, tweet in enumerate(cursor):
        if tweet is None:
            logging.warn(
                msg="ScrapeUserTimeline: {user_id}.{tweet_index} "
                    "is null".format(user_id=user_id, tweet_index=i))
            continue

        file_name = "{user_id}.{date}".format(
            user_id=user_id, date=tweet.date)
        output_file_path = path.join(output_dir, file_name)

        with open(output_file_path, mode="wb") as output_file:
            pickle.dump(obj=tweet, file=output_file)

        logging.info(
            msg="ScrapeUserTimeline: Saved {user_id}.{tweet_index} to "
                "{output_file_path}".format(
                    user_id=user_id, tweet_index=i,
                    output_file_path=output_file_path))
