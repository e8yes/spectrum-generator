from pandas import DataFrame
from pandas import read_pickle
from typing import Dict

from src.dataprep.cooked.constants import TWEET_MINIMUM_LENGTH_THRESHOLD
from src.dataprep.cooked.user_lookup import UserNameToId
from src.dataprep.cooked.text_tokenizer import CleanText
from src.dataprep.cooked.text_tokenizer import TokenizeText


def LoadRawTimelines(file_path: str) -> DataFrame:
    """_summary_

    Args:
        file_path (str): _description_

    Returns:
        _type_: _description_
    """
    return read_pickle(file_path)


def BuildUserTweetTable(raw_timelines: DataFrame,
                        user_lookup: Dict[str, int]) -> DataFrame:
    """_summary_

    Args:
        raw_timelines (DataFrame): _description_
        user_lookup (Dict[str, int]): _description_

    Returns:
        DataFrame: _description_
    """
    tweet_ids = raw_timelines["id"]

    user_ids = raw_timelines["user_name"].apply(
        lambda user_name: UserNameToId(
            user_name=user_name, user_lookup=user_lookup))

    contents = raw_timelines["content"].                    \
        apply(CleanText).                                   \
        apply(TokenizeText)
    context_contents = raw_timelines["context_content"].    \
        apply(CleanText).                                   \
        apply(TokenizeText)
    external_content_summaries =                            \
        raw_timelines["external_content_summary"].          \
        apply(CleanText).                                   \
        apply(TokenizeText)

    user_tweets = DataFrame(data={
        "tweet_id": tweet_ids.astype(int),
        "user_id": user_ids.astype(int),
        "context_content": context_contents,
        "external_content_summary": external_content_summaries,
        "content": contents,
    })

    short_tweets = user_tweets["content"].                  \
        map(len) < TWEET_MINIMUM_LENGTH_THRESHOLD
    user_tweets.drop(user_tweets[short_tweets].index,
                     inplace=True)

    return user_tweets
