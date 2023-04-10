import argparse
from pandas import read_pickle
from os import path

from src.dataprep.cooked.representatives import \
    BuildUserRepresentativeTweetTable
from src.dataprep.cooked.topic_extractor import AnnotateTopics
from src.dataprep.cooked.tweet_encoder import EncodeContent


def _Extract(raw_timeline_file: str, output_path: str) -> None:
    raw_timelines = read_pickle(raw_timeline_file)
    user_repr_tweets = BuildUserRepresentativeTweetTable(
        raw_timelines=raw_timelines)
    del raw_timelines

    AnnotateTopics(user_repr_tweets=user_repr_tweets)
    EncodeContent(user_repr_tweets=user_repr_tweets)

    user_repr_tweets.to_pickle(
        path.join(output_path, "user_representative_tweets"))
    user_repr_tweets.to_csv(
        path.join(output_path, "user_representative_tweets.csv"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extracts representative data for each user from the raw "
                    "timelines.")

    parser.add_argument(
        "--raw_timeline_file",
        type=str,
        help="Path to the raw timeline dataframe file.")
    parser.add_argument(
        "--output_path",
        type=str,
        help="Path under which the built tables are stored.")

    args = parser.parse_args()

    if args.raw_timeline_file is None:
        print("raw_timeline_file is required.")
        exit(-1)
    if args.output_path is None:
        print("output_path is required.")
        exit(-1)

    _Extract(raw_timeline_file=args.raw_timeline_file,
             output_path=args.output_path)
