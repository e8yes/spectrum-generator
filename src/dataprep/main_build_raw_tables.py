import argparse
import logging
from os import path

from src.dataprep.raw.raw_user_profiles import CreateUsersProfileTable
from src.dataprep.raw.raw_tweets import CreateRawTweetTable


def _BuildTable(raw_timeline_dir: str, output_path: str) -> None:
    user_profile_table = CreateUsersProfileTable(
        raw_timeline_dir=raw_timeline_dir)
    raw_tweet_table = CreateRawTweetTable(raw_timeline_dir=raw_timeline_dir)

    user_profile_table.to_pickle(
        path=path.join(output_path, "raw_user_profiles"))
    raw_tweet_table.to_pickle(
        path=path.join(output_path, "raw_tweets"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Builds raw user profile and tweet tables from raw "
                    "timeline files.")

    parser.add_argument(
        "--raw_timeline_dir",
        type=str,
        help="Path to the CSV file that has a column called \"Link\" where it "
             "contains a list of links to the homepages of Twitter users.")
    parser.add_argument(
        "--output_path",
        type=str,
        help="Path under which the built tables are stored.")

    args = parser.parse_args()

    if args.raw_timeline_dir is None:
        print("raw_timeline_dir is required.")
        exit(-1)
    if args.output_path is None:
        print("output_path is required.")
        exit(-1)

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    _BuildTable(raw_timeline_dir=args.raw_timeline_dir,
                output_path=args.output_path)
