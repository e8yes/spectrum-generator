import logging
from pandas import DataFrame
from pandas import Series
from pandas import DatetimeTZDtype

from src.dataprep.raw.common import LoadRawTimeline
from src.dataprep.raw.common import RawTimelineFiles


class _UserProfileColumns:
    def __init__(self) -> None:
        self.user_names = list()
        self.display_names = list()
        self.descriptions = list()
        self.description_links = list()
        self.verification_statuses = list()
        self.creation_dates = list()
        self.followers_counts = list()
        self.friends_counts = list()
        self.statuses_counts = list()
        self.favourites_counts = list()
        self.listed_counts = list()
        self.media_counts = list()
        self.locations = list()
        self.protection_statuses = list()
        self.links = list()

    def CreateTable(self) -> DataFrame:
        return DataFrame(data={
            "user_name": Series(data=self.user_names, dtype=str),
            "display_name": Series(data=self.display_names, dtype=str),
            "description": Series(data=self.descriptions, dtype=str),
            "description_links": Series(
                data=self.description_links, dtype=object),
            "verification_status": Series(
                data=self.verification_statuses, dtype=bool),
            "creation_date": Series(
                data=self.creation_dates, dtype=DatetimeTZDtype),
            "followers_count": Series(
                data=self.followers_counts, dtype=int),
            "friends_count": Series(
                data=self.friends_counts, dtype=int),
            "statuses_count": Series(
                data=self.statuses_counts, dtype=int),
            "favourites_count": Series(
                data=self.favourites_counts, dtype=int),
            "listed_count": Series(data=self.listed_counts, dtype=int),
            "media_count": Series(data=self.media_counts, dtype=int),
            "location": Series(data=self.locations, dtype=str),
            "protection_status": Series(
                data=self.protection_statuses, dtype=bool),
            "link": Series(data=self.links, dtype=str),
        })


def _AddRow(raw_timeline_file: str, cols: _UserProfileColumns) -> None:
    user_id, tweets = LoadRawTimeline(raw_timeline_file=raw_timeline_file)

    if len(tweets) == 0:
        return

    user_profile = tweets[0].user

    cols.user_names.append(user_id)
    cols.display_names.append(user_profile.displayname)
    cols.descriptions.append(user_profile.renderedDescription)
    cols.description_links.append(
        [link.url for link in user_profile.descriptionLinks]
        if user_profile.descriptionLinks is not None else [])
    cols.verification_statuses.append(user_profile.verified)
    cols.creation_dates.append(user_profile.created)
    cols.followers_counts.append(user_profile.followersCount)
    cols.friends_counts.append(user_profile.friendsCount)
    cols.statuses_counts.append(user_profile.statusesCount)
    cols.favourites_counts.append(user_profile.favouritesCount)
    cols.listed_counts.append(user_profile.listedCount)
    cols.media_counts.append(user_profile.mediaCount)
    cols.locations.append(user_profile.location)
    cols.protection_statuses.append(user_profile.protected)
    cols.links.append(user_profile.link.url
                      if user_profile.link is not None else None)


def CreateUsersProfileTable(raw_timeline_dir: str) -> DataFrame:
    """Creates a table containing basic information about each Twitter user,
    extracted from raw timeline files.

    Args:
        raw_timeline_dir (str): Directory which contains each Twitter user's
            raw timeline file.

    Returns:
        DataFrame: A table containing basic information about each Twitter
            user. The table schema is as follow:
                user_name: str
                display_name: str
                description: str
                description_links: List[str]
                verification_status: bool
                creation_date: datetime
                followers_count: int
                friends_count: int
                statuses_count: int
                favourites_count: int
                listed_count: int
                media_count: int
                location: str
                protection_status: bool
                link: str
    """
    cols = _UserProfileColumns()

    for raw_timeline_file in RawTimelineFiles(
            raw_timeline_dir=raw_timeline_dir):
        _AddRow(raw_timeline_file=raw_timeline_file, cols=cols)

        logging.info(
            "CreateUsersProfileTable: Processed user profile {0}".format(
                raw_timeline_file))

    return cols.CreateTable()
