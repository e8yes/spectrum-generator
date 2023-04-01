import argparse
import json
from os import path

from src.dataprep.cooked.user_lookup import LoadRawUserProfiles
from src.dataprep.cooked.user_lookup import BuildUserLookup
from src.dataprep.cooked.tweets import LoadRawTimelines
from src.dataprep.cooked.tweets import BuildUserTweetTable
from src.dataprep.cooked.word_importance import AssignWordImportance


def _Cook(raw_user_profile_file: str,
          raw_timeline_file: str,
          output_path: str):
    user_profiles = LoadRawUserProfiles(file_path=raw_user_profile_file)
    user_lookup = BuildUserLookup(raw_user_profile=user_profiles)
    with open(file=path.join(output_path, "user_lookup.json"),
              mode="w") as f:
        json.dump(user_lookup, f)

    raw_timelines = LoadRawTimelines(file_path=raw_timeline_file)
    user_tweets = BuildUserTweetTable(raw_timelines=raw_timelines,
                                      user_lookup=user_lookup)
    del raw_timelines
    user_tweets.to_csv(path.join(output_path, "user_tweets.csv"))

    word_doc_freq = AssignWordImportance(user_tweet_df=user_tweets)
    user_tweets.to_csv(
        path.join(output_path, "user_tweets_final.csv"))
    word_doc_freq.to_csv(
        path.join(output_path, "user_tweet_word_doc_freq.csv"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Processes raw dataframes into cooked feature tables.")

    parser.add_argument(
        "--raw_user_profile_file",
        type=str,
        help="Path to the raw user profile dataframe file.")
    parser.add_argument(
        "--raw_timeline_file",
        type=str,
        help="Path to the raw timeline dataframe file.")
    parser.add_argument(
        "--output_path",
        type=str,
        help="Path under which the built tables are stored.")

    args = parser.parse_args()

    if args.raw_user_profile_file is None:
        print("raw_user_profile_file is required.")
        exit(-1)
    if args.raw_timeline_file is None:
        print("raw_timeline_file is required.")
        exit(-1)
    if args.output_path is None:
        print("output_path is required.")
        exit(-1)

    _Cook(raw_user_profile_file=args.raw_user_profile_file,
          raw_timeline_file=args.raw_timeline_file,
          output_path=args.output_path)
