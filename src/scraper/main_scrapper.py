import argparse
import logging

from src.scraper.scrape_users import LoadTwitterUserIds
from src.scraper.scrape_users import ScrapeUsers
from src.scraper.scrape_users import ScrapedUserIds


def _ScrapeTimelines(user_csv: str, output_path: str) -> None:
    users = LoadTwitterUserIds(csv_file=user_csv)
    scraped = ScrapedUserIds(output_dir=output_path)

    to_be_scraped = list(set(users).difference(set(scraped)))

    logging.info(
        msg="_ScrapeTimelines: About to scrape the timeline of the following "
            "users: {users}".format(users=to_be_scraped))

    ScrapeUsers(user_ids=to_be_scraped, output_dir=output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrapes the timeline of Twitter users listed in the "
                    "specified CSV spreadsheet.")

    parser.add_argument(
        "--user_csv",
        type=str,
        help="Path to the CSV file that has a column called \"Link\" where it "
             "contains a list of links to the homepages of Twitter users.")
    parser.add_argument(
        "--output_path",
        type=str,
        help="Path under which the scraped timelines are stored.")

    args = parser.parse_args()

    if args.user_csv is None:
        print("user_csv is required.")
        exit(-1)
    if args.output_path is None:
        print("output_path is required.")
        exit(-1)

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    _ScrapeTimelines(user_csv=args.user_csv, output_path=args.output_path)
