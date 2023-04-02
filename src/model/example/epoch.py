import gc
from os import path
from pandas import DataFrame
from pandas import read_pickle
from typing import Tuple

from src.model.example.constants import TWEET_COUNT_PER_USER_EPOCH
from src.model.example.batch import BatchExampleBuilder
from src.model.example.batch import BatchExamples


class DataEpoch:
    """_summary_
    """

    def __init__(self,
                 input_path: str,
                 batch_size: int) -> None:
        """_summary_

        Args:
            input_path (str): _description_
            batch_size (int): _description_
        """
        self.user_tweet_file_path = path.join(input_path, "user_tweets")
        self.user_tweet_df: DataFrame = None
        self.batch_size = batch_size

    def __iter__(self):
        """_summary_

        Returns:
            BatchExamples: _description_
        """
        user_tweet_df: DataFrame = read_pickle(self.user_tweet_file_path)
        self.user_tweet_df = user_tweet_df.                     \
            groupby("user_id").                                 \
            sample(n=TWEET_COUNT_PER_USER_EPOCH, replace=True). \
            sample(frac=1)

        del user_tweet_df
        gc.collect()

        self.batch_start = 0
        self.batch_builder = BatchExampleBuilder()

        return self

    def __next__(self) -> Tuple[int, BatchExamples]:
        """_summary_

        Raises:
            StopIteration: _description_
        """
        if self.batch_start >= self.user_tweet_df.shape[0]:
            raise StopIteration

        cols = self.user_tweet_df[["user_id",
                                   "creation_year_id",
                                   "context_content",
                                   "external_content_summary",
                                   "content",
                                   "content_importance"]]
        batch_df = cols[self.batch_start: self.batch_start + self.batch_size]
        batch_examples = self.batch_builder.Build(batch=batch_df)

        self.batch_start += self.batch_size
        progress = int(self.batch_start/self.user_tweet_df.shape[0]*100)

        return progress, batch_examples
