import argparse
from os import path
from pandas import DataFrame
from pandas import read_pickle
from typing import Dict

from src.dataprep.cooked.user_lookup import BuildUserLookup
from src.dataprep.cooked.user_lookup import SaveUserLookup
from src.dataprep.cooked.creation_year_lookup import BuildCreationYearLookup
from src.dataprep.cooked.creation_year_lookup import SaveYearIdLookup
from src.dataprep.cooked.tweets import BuildUserTweetTable
from src.dataprep.cooked.tweets import DropShortTweets
from src.dataprep.cooked.word_importance import AssignWordImportance


def _CookUserLookup(raw_user_profile_file: str,
                    output_path: str) -> Dict[str, int]:
    print("Running _CookUserLookup()...")

    user_profiles = read_pickle(raw_user_profile_file)

    user_lookup = BuildUserLookup(raw_user_profile=user_profiles)
    SaveUserLookup(lookup=user_lookup, output_path=output_path)

    return user_lookup


def _CookCreationYearLookup(raw_timeline_file: str,
                            output_path: str) -> Dict[int, int]:
    print("Running _CookCreationYearLookup()...")

    raw_timelines = read_pickle(raw_timeline_file)

    year_lookup, year_id_lookup = BuildCreationYearLookup(
        raw_timelines=raw_timelines)
    SaveYearIdLookup(lookup=year_id_lookup, output_path=output_path)

    return year_lookup


def _CookInitialUserTweets(raw_timeline_file: str,
                           user_lookup: Dict[str, int],
                           year_lookup: Dict[int, int],
                           output_path: str) -> DataFrame:
    print("Running _CookInitialUserTweets()...")

    raw_timelines = read_pickle(raw_timeline_file)

    user_tweets = BuildUserTweetTable(
        raw_timelines=raw_timelines,
        user_lookup=user_lookup,
        year_lookup=year_lookup)
    user_tweets.to_pickle(
        path.join(output_path, "user_tweets_initial"))

    return user_tweets


def _CookFinalUserTweets(output_path: str) -> None:
    print("Running _CookFinalUserTweets()...")

    user_tweets = read_pickle(
        path.join(output_path, "user_tweets_initial"))

    DropShortTweets(user_tweets=user_tweets)

    word_doc_freq = AssignWordImportance(user_tweet_df=user_tweets)
    user_tweets.to_pickle(
        path.join(output_path, "user_tweets"))
    word_doc_freq.to_csv(
        path.join(output_path, "user_tweet_word_doc_freq.csv"))


def _Cook(raw_user_profile_file: str,
          raw_timeline_file: str,
          output_path: str):
    user_lookup = _CookUserLookup(
        raw_user_profile_file=raw_user_profile_file, output_path=output_path)
    year_lookup = _CookCreationYearLookup(
        raw_timeline_file=raw_timeline_file, output_path=output_path)
    _CookInitialUserTweets(
        raw_timeline_file=raw_timeline_file,
        user_lookup=user_lookup,
        year_lookup=year_lookup,
        output_path=output_path)
    _CookFinalUserTweets(output_path=output_path)

    print("_Cook() is complete.")


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
