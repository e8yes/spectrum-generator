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
                 epoch_number: int,
                 input_path: str,
                 temp_path: str,
                 batch_size: int) -> None:
        """_summary_

        Args:
            epoch_number (int): _description_
            input_path (str): _description_
            temp_path (str): _description_
            batch_size (int): _description_
        """
        self.epoch_number = epoch_number
        self.temp_path = temp_path
        self.batch_size = batch_size

        self.user_tweet_file_path = path.join(input_path, "user_tweets")
        self.user_tweet_df: DataFrame = None

    def __iter__(self):
        """_summary_

        Returns:
            BatchExamples: _description_
        """
        user_tweet_df: DataFrame = read_pickle(self.user_tweet_file_path)
        sampled_user_tweets = user_tweet_df.                    \
            groupby("user_id").                                 \
            sample(n=TWEET_COUNT_PER_USER_EPOCH, replace=True). \
            sample(frac=1)

        # Saves the samples into a file then releases the occupied memory.
        tmp_data_file = path.join(
            self.temp_path, f"tmp{self.epoch_number}")
        sampled_user_tweets.to_pickle(tmp_data_file)

        del sampled_user_tweets
        del user_tweet_df

        self.user_tweet_df = read_pickle(tmp_data_file)

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
