from pandas import DataFrame
from pandas import merge

from src.dataprep.cooked.text_tokenizer import CleanText

N_TOP = 50


def _PopularTweets(raw_timelines: DataFrame) -> DataFrame:
    id_col = raw_timelines["id"]
    user_name_col = raw_timelines["user_name"]
    popularity_col = raw_timelines["like_count"] +  \
        2.5*raw_timelines["retweet_count"] +        \
        20*raw_timelines["quote_count"]

    df = DataFrame(data={
        "id": id_col,
        "user_name": user_name_col,
        "popularity": popularity_col,
    })
    df.set_index(keys="id", inplace=True)

    popular_tweets = df.                        \
        groupby(by="user_name")["popularity"].  \
        nlargest(N_TOP).                        \
        reset_index().                          \
        drop(labels="user_name", axis=1)

    return popular_tweets


def BuildUserRepresentativeTweetTable(raw_timelines: DataFrame) -> DataFrame:
    """_summary_

    Args:
        raw_timelines (DataFrame): _description_

    Returns:
        DataFrame: _description_
    """
    popular_tweets = _PopularTweets(raw_timelines=raw_timelines)
    popular_timelines = merge(left=popular_tweets,
                              right=raw_timelines,
                              how="inner",
                              on="id")

    content_col = popular_timelines["content"].map(CleanText)
    context_content_col = popular_timelines["context_content"].map(CleanText)
    external_content_summary_col = \
        popular_timelines["external_content_summary"].apply(CleanText)

    return DataFrame(data={
        "id": popular_timelines["id"],
        "user_name": popular_timelines["user_name"],
        "creation_date": popular_timelines["creation_date"],
        "popularity": popular_timelines["popularity"],
        "hashtags": popular_timelines["hashtags"],
        "content": content_col,
        "context_content": context_content_col,
        "external_content_summary": external_content_summary_col,
    })
