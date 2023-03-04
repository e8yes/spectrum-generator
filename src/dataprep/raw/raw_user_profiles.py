from pandas import DataFrame

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
            "user_name": self.user_names,
            "display_name": self.display_names,
            "description": self.descriptions,
            "description_links": self.description_links,
            "verification_status": self.verification_statuses,
            "creation_date": self.creation_dates,
            "followers_count": self.followers_counts,
            "friends_count": self.friends_counts,
            "statuses_count": self.statuses_counts,
            "favourites_count": self.favourites_counts,
            "listed_count": self.listed_counts,
            "media_count": self.media_counts,
            "location": self.locations,
            "protection_status": self.protection_statuses,
            "link": self.links,
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

    return cols.CreateTable()


df = CreateUsersProfileTable(raw_timeline_dir="data/tweets")
print(df.columns)
