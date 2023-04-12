# This Python file uses the following encoding: utf-8

from datetime import datetime
from numpy import ndarray
from numpy import dot
from numpy.linalg import norm
from pandas import DataFrame
from pandas import read_pickle
from typing import Dict
from typing import List

MAX_TWEET_COUNT = 10


class RepresentativeEntry:
    """_summary_
    """

    def __init__(self,
                 id: str,
                 context: str,
                 content: str,
                 creation_date: datetime,
                 popularity: float,
                 tags: Dict[str, float],
                 embedding: ndarray) -> None:
        """_summary_

        Args:
            id (str): _description_
            context (str): _description_
            content (str): _description_
            creation_date (datetime): _description_
            popularity (float): _description_
            tags (Dict[str, float]): _description_
            embedding (ndarray): _description_
        """
        self.id = id
        self.context = context
        self.content = content
        self.creation_date = creation_date
        self.popularity = popularity
        self.tags = tags
        self.embedding = embedding

    def __repr__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return f"id={self.id}, "                    \
            f"context={self.context}, "             \
            f"content={self.content}, "             \
            f"creation_date={self.creation_date}, " \
            f"popularity={self.popularity}, "       \
            f"tags={self.tags}"


def _MostSimilar(entry: RepresentativeEntry,
                 repo: List[RepresentativeEntry]) -> RepresentativeEntry:
    max_sim = float("-inf")
    result = None

    for candid in repo:
        a = entry.embedding
        b = candid.embedding

        sim = dot(a, b)/(norm(a)*norm(b))
        if sim > max_sim:
            max_sim = sim
            result = candid

    return result


class RepresentativeData:
    """_summary_
    """

    def __init__(self, rep_data_path: str) -> None:
        """_summary_

        Args:
            rep_data_path (str): _description_
        """
        self.df: DataFrame = read_pickle(filepath_or_buffer=rep_data_path)

    def GetMostPopularEntries(
            self,
            user_name: str,
            top_n=MAX_TWEET_COUNT) -> List[RepresentativeEntry]:
        """_summary_

        Args:
            user_name (str): _description_
            top_n (_type_, optional):
                _description_. Defaults to MAX_TWEET_COUNT.

        Returns:
            List[RepresentativeEntry]: _description_
        """
        rep_tweets = self.df[self.df["user_name"] == user_name]
        rep_tweets = rep_tweets.sort_values(by="popularity", ascending=False)

        result = list()
        for _, row in rep_tweets.iterrows():
            if top_n is not None and len(result) == top_n:
                break

            entry = RepresentativeEntry(id=row["id"],
                                        context=row["context_content"],
                                        content=row["content"],
                                        creation_date=row["creation_date"],
                                        popularity=row["popularity"],
                                        tags=row["tags"],
                                        embedding=row["embedding"])
            result.append(entry)

        return result

    def GetMostMatchingEntries(
            self,
            user_name: str,
            context: List[RepresentativeEntry]) -> List[RepresentativeEntry]:
        """_summary_

        Args:
            user_name (str): _description_
            context (List[RepresentativeEntry]): _description_

        Returns:
            List[RepresentativeEntry]: _description_
        """
        repo = self.GetMostPopularEntries(user_name=user_name, top_n=None)

        result = list()
        for entry in context:
            result.append(_MostSimilar(entry=entry, repo=repo))

        return result
