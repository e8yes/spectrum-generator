from pandas import DataFrame
from typing import Dict

from src.dataprep.cooked.constants import TWEET_MINIMUM_LENGTH_THRESHOLD
from src.dataprep.cooked.user_lookup import UserNameToId
from src.dataprep.cooked.text_tokenizer import CleanText
from src.dataprep.cooked.text_tokenizer import TokenizeText


def BuildUserTweetTable(raw_timelines: DataFrame,
                        user_lookup: Dict[str, int],
                        year_lookup: Dict[int, int]) -> DataFrame:
    """_summary_

    Args:
        raw_timelines (DataFrame): _description_
        user_lookup (Dict[str, int]): _description_
        year_lookup (Dict[int, int]): _description_

    Returns:
        DataFrame: _description_
    """
    tweet_ids = raw_timelines["id"]

    user_ids = raw_timelines["user_name"].apply(
        lambda user_name: UserNameToId(
            user_name=user_name, user_lookup=user_lookup))
    creation_year_ids = raw_timelines["creation_date"].apply(
        lambda date: year_lookup[date.year])

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
        "creation_year_id": creation_year_ids.astype(int),
        "context_content": context_contents,
        "external_content_summary": external_content_summaries,
        "content": contents,
    })

    return user_tweets


def DropShortTweets(user_tweets: DataFrame) -> None:
    """_summary_

    Args:
        user_tweets (DataFrame): _description_
    """
    context_content_len =                                   \
        user_tweets["context_content"].map(len)
    external_content_summary_len =                          \
        user_tweets["external_content_summary"].map(len)
    content_len =                                           \
        user_tweets["content"].map(len)

    tweet_len =                                             \
        context_content_len +                               \
        external_content_summary_len +                      \
        content_len

    user_tweets.drop(
        user_tweets[tweet_len < TWEET_MINIMUM_LENGTH_THRESHOLD].index,
        inplace=True)
