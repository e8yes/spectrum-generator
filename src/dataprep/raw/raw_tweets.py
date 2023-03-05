import logging
from pandas import DataFrame
from pandas import Series
from pandas import DatetimeTZDtype
from src.dataprep.raw.common import LoadRawTimeline
from src.dataprep.raw.common import RawTimelineFiles
from snscrape.modules.twitter import Tweet
from snscrape.modules.twitter import User
from snscrape.modules.twitter import TextLink
from snscrape.modules.twitter import Medium
from snscrape.modules.twitter import Photo
from snscrape.modules.twitter import Video
from snscrape.modules.twitter import Gif
from snscrape.modules.twitter import Vibe
from typing import List
from typing import Optional


CONTEXT_TYPE_RETWEET = "RETWEET"
CONTEXT_TYPE_QUOTE = "QUOTE"

MEDIUM_TYPE_PHOTO = "PHOTO"
MEDIUM_TYPE_VIDEO = "VIDEO"
MEDIUM_TYPE_GIF = "GIF"


class _TweetColumns:
    def __init__(self) -> None:
        self.ids = list()
        self.urls = list()
        self.user_names = list()
        self.contents = list()
        self.creation_dates = list()
        self.reply_counts = list()
        self.retweet_counts = list()
        self.like_counts = list()
        self.quote_counts = list()
        self.view_counts = list()
        self.conversation_ids = list()
        self.languages = list()
        self.sources = list()
        self.source_urls = list()
        self.source_labels = list()
        self.links = list()
        self.media_types = list()
        self.reply_tweet_ids = list()
        self.reply_user_names = list()
        self.hashtags = list()
        self.cashtags = list()
        self.vibe_texts = list()

        self.context_ids = list()
        self.context_urls = list()
        self.context_user_names = list()
        self.context_user_descriptions = list()
        self.context_contents = list()
        self.context_creation_dates = list()
        self.context_reply_counts = list()
        self.context_retweet_counts = list()
        self.context_like_counts = list()
        self.context_quote_counts = list()
        self.context_view_counts = list()
        self.context_conversation_ids = list()
        self.context_languages = list()
        self.context_sources = list()
        self.context_source_urls = list()
        self.context_source_labels = list()
        self.context_links = list()
        self.context_media_types = list()
        self.context_reply_tweet_ids = list()
        self.context_reply_user_names = list()
        self.context_hashtags = list()
        self.context_cashtags = list()
        self.context_vibe_texts = list()
        self.context_types = list()

    def CreateTable(self) -> DataFrame:
        return DataFrame(data={
            "id": Series(data=self.ids, dtype=int),
            "url": Series(data=self.urls, dtype=str),
            "user_name": Series(data=self.user_names, dtype=str),
            "content": Series(data=self.contents, dtype=str),
            "creation_date": Series(
                data=self.creation_dates, dtype=DatetimeTZDtype),
            "reply_count": Series(data=self.reply_counts, dtype=int),
            "retweet_count": Series(data=self.retweet_counts, dtype=int),
            "like_count": Series(data=self.like_counts, dtype=int),
            "quote_count": Series(data=self.quote_counts, dtype=int),
            "view_count": Series(data=self.view_counts, dtype=object),
            "conversation_id": Series(data=self.conversation_ids, dtype=int),
            "language": Series(data=self.languages, dtype=str),
            "source": Series(data=self.sources, dtype=str),
            "source_url": Series(data=self.source_urls, dtype=str),
            "source_label": Series(data=self.source_labels, dtype=str),
            "links": Series(data=self.links, dtype=object),
            "media_types": Series(data=self.media_types, dtype=object),
            "reply_tweet_id": Series(data=self.reply_tweet_ids, dtype=object),
            "reply_user_name": Series(data=self.reply_user_names, dtype=str),
            "hashtags": Series(data=self.hashtags, dtype=object),
            "cashtags": Series(data=self.cashtags, dtype=object),
            "vibe_text": Series(data=self.vibe_texts, dtype=str),

            "context_id": Series(data=self.context_ids, dtype=object),
            "context_url": Series(data=self.context_urls, dtype=str),
            "context_user_name": Series(
                data=self.context_user_names, dtype=str),
            "context_content": Series(data=self.context_contents, dtype=str),
            "context_creation_date": Series(
                data=self.context_creation_dates, dtype=DatetimeTZDtype),
            "context_reply_count": Series(
                data=self.context_reply_counts, dtype=object),
            "context_retweet_count": Series(
                data=self.context_retweet_counts, dtype=object),
            "context_like_count": Series(
                data=self.context_like_counts, dtype=object),
            "context_quote_count": Series(
                data=self.context_quote_counts, dtype=object),
            "context_view_count": Series(
                data=self.context_view_counts, dtype=object),
            "context_conversation_id": Series(
                data=self.context_conversation_ids, dtype=object),
            "context_language": Series(data=self.context_languages, dtype=str),
            "context_source": Series(data=self.context_sources, dtype=str),
            "context_source_url": Series(
                data=self.context_source_urls, dtype=str),
            "context_source_label": Series(
                data=self.context_source_labels, dtype=str),
            "context_links": Series(data=self.context_links, dtype=object),
            "context_media_types": Series(
                data=self.context_media_types, dtype=object),
            "context_reply_tweet_id": Series(
                data=self.context_reply_tweet_ids, dtype=object),
            "context_reply_user_name": Series(
                data=self.context_reply_user_names, dtype=str),
            "context_hashtags": Series(
                data=self.context_hashtags, dtype=object),
            "context_cashtags": Series(
                data=self.context_cashtags, dtype=object),
            "context_vibe_text": Series(
                data=self.context_vibe_texts, dtype=str),
            "context_types": Series(data=self.context_types, dtype=str),
        })


def _ExtractLinks(links: Optional[List[TextLink]]) -> List[str]:
    if links is None:
        return list()

    return [link.url for link in links]


def _ExtractMediaTypes(media: Optional[List[Medium]]) -> List[str]:
    if media is None:
        return list()

    media_types = list()

    for medium in media:
        if isinstance(medium, Photo):
            media_types.append(MEDIUM_TYPE_PHOTO)
        elif isinstance(medium, Video):
            media_types.append(MEDIUM_TYPE_VIDEO)
        elif isinstance(medium, Gif):
            media_types.append(MEDIUM_TYPE_GIF)
        else:
            logging.error(
                "_ExtractMediaTypes: Unknown medium type {0}".format(
                    type(medium)))

    return media_types


def _ExtractTags(tags: Optional[List[str]]) -> List[str]:
    if tags is None:
        return list()
    return tags


def _ExtractVibeText(vibe: Optional[Vibe]) -> str:
    if vibe is None:
        return None
    return vibe.text


def _ExtractRepliedUserName(user: Optional[User]) -> str:
    if user is None:
        return None
    return user.username


def _AddRow(user_name: str, tweet: Tweet, cols: _TweetColumns) -> None:
    cols.ids.append(tweet.id)
    cols.urls.append(tweet.url)
    cols.user_names.append(user_name)
    cols.contents.append(tweet.renderedContent)
    cols.creation_dates.append(tweet.date)
    cols.reply_counts.append(tweet.replyCount)
    cols.retweet_counts.append(tweet.retweetCount)
    cols.like_counts.append(tweet.likeCount)
    cols.quote_counts.append(tweet.quoteCount)
    cols.view_counts.append(tweet.viewCount)
    cols.conversation_ids.append(tweet.conversationId)
    cols.languages.append(tweet.lang)
    cols.sources.append(tweet.source)
    cols.source_urls.append(tweet.sourceUrl)
    cols.source_labels.append(tweet.sourceLabel)
    cols.links.append(_ExtractLinks(links=tweet.links))
    cols.media_types.append(_ExtractMediaTypes(media=tweet.media))
    cols.reply_tweet_ids.append(tweet.inReplyToTweetId)
    cols.reply_user_names.append(
        _ExtractRepliedUserName(user=tweet.inReplyToUser))
    cols.hashtags.append(_ExtractTags(tags=tweet.hashtags))
    cols.cashtags.append(_ExtractTags(tags=tweet.cashtags))
    cols.vibe_texts.append(_ExtractVibeText(vibe=tweet.vibe))

    context_tweet: Tweet = None
    context_type: str = None
    if tweet.retweetedTweet is not None:
        context_tweet = tweet.retweetedTweet
        context_type = CONTEXT_TYPE_RETWEET

        assert tweet.quotedTweet is None
    elif tweet.quotedTweet is not None:
        context_tweet = tweet.quotedTweet
        context_type = CONTEXT_TYPE_QUOTE

        assert tweet.retweetedTweet is None

    if context_tweet is not None:
        cols.context_ids.append(context_tweet.id)
        cols.context_urls.append(context_tweet.url)
        cols.context_user_names.append(context_tweet.user.username)
        cols.context_contents.append(context_tweet.renderedContent)
        cols.context_creation_dates.append(context_tweet.date)
        cols.context_reply_counts.append(context_tweet.replyCount)
        cols.context_retweet_counts.append(context_tweet.retweetCount)
        cols.context_like_counts.append(context_tweet.likeCount)
        cols.context_quote_counts.append(context_tweet.quoteCount)
        cols.context_view_counts.append(context_tweet.viewCount)
        cols.context_conversation_ids.append(context_tweet.conversationId)
        cols.context_languages.append(context_tweet.lang)
        cols.context_sources.append(context_tweet.source)
        cols.context_source_urls.append(context_tweet.sourceUrl)
        cols.context_source_labels.append(context_tweet.sourceLabel)
        cols.context_links.append(_ExtractLinks(links=context_tweet.links))
        cols.context_media_types.append(
            _ExtractMediaTypes(media=context_tweet.media))
        cols.context_reply_tweet_ids.append(context_tweet.inReplyToTweetId)
        cols.context_reply_user_names.append(
            _ExtractRepliedUserName(user=context_tweet.inReplyToUser))
        cols.context_hashtags.append(_ExtractTags(tags=context_tweet.hashtags))
        cols.context_cashtags.append(_ExtractTags(tags=context_tweet.cashtags))
        cols.context_vibe_texts.append(
            _ExtractVibeText(vibe=context_tweet.vibe))
        cols.context_types.append(context_type)
    else:
        cols.context_ids.append(None)
        cols.context_urls.append(None)
        cols.context_user_names.append(None)
        cols.context_contents.append(None)
        cols.context_creation_dates.append(None)
        cols.context_reply_counts.append(None)
        cols.context_retweet_counts.append(None)
        cols.context_like_counts.append(None)
        cols.context_quote_counts.append(None)
        cols.context_view_counts.append(None)
        cols.context_conversation_ids.append(None)
        cols.context_languages.append(None)
        cols.context_sources.append(None)
        cols.context_source_urls.append(None)
        cols.context_source_labels.append(None)
        cols.context_links.append(None)
        cols.context_media_types.append(None)
        cols.context_reply_tweet_ids.append(None)
        cols.context_reply_user_names.append(None)
        cols.context_hashtags.append(None)
        cols.context_cashtags.append(None)
        cols.context_vibe_texts.append(None)
        cols.context_types.append(None)


def _AddTimeline(raw_timeline_file: str, cols: _TweetColumns) -> None:
    user_name, tweets = LoadRawTimeline(raw_timeline_file=raw_timeline_file)

    if len(tweets) == 0:
        return

    for tweet in tweets:
        _AddRow(user_name=user_name, tweet=tweet, cols=cols)


def CreateRawTweetTable(raw_timeline_dir: str) -> DataFrame:
    """Creates a table containing all user tweets, extracted from raw timeline
    files.

    Args:
        raw_timeline_dir (str): Directory which contains each Twitter user's
            raw timeline file.

    Returns:
        DataFrame: A table containing all user tweets. The table schema is as
            follow:
                id: int
                url: str
                user_name: str
                content: str
                creation_date: datetime
                reply_count: int
                retweet_count: int
                like_count: int
                quote_count: int
                view_count: int
                conversation_id: int
                language: str
                source: str
                source_url: str
                source_label: str
                links: List[str]
                media_types: List[str]
                reply_tweet_id: int
                reply_user_name: str
                hashtags: List[str]
                cashtags: List[str]
                vibe_text: str
                context_id: int
                context_url: str
                context_user_name: str
                context_content: str
                context_creation_date: datetime
                context_reply_count: int
                context_retweet_count: int
                context_like_count: int
                context_quote_count: int
                context_view_count: int
                context_conversation_id: int
                context_language: str
                context_source: str
                context_source_url: str
                context_source_label: str
                context_links: List[str]
                context_media_types: List[str]
                context_reply_tweet_id: int
                context_reply_user_name: str
                context_hashtags: List[str]
                context_cashtags: List[str]
                context_vibe_text: str
    """
    cols = _TweetColumns()

    for raw_timeline_file in RawTimelineFiles(
            raw_timeline_dir=raw_timeline_dir):
        _AddTimeline(raw_timeline_file=raw_timeline_file, cols=cols)

        logging.info("CreateRawTweetTable: Processed user timeline {0}".format(
            raw_timeline_file))

    return cols.CreateTable()
