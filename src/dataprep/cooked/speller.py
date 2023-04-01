from autocorrect import Speller
from pandas import DataFrame
from typing import Dict
from typing import List
from typing import Set


def _CollectWords(user_tweet_df: DataFrame,
                  text_cols: List[str]) -> Set[str]:
    words = set()

    for _, row in user_tweet_df.iterrows():
        for col_name in text_cols:
            for word in row[col_name]:
                words.add(word)

    return words


def _BuildCorrectionLookup(words: Set[str]) -> Dict[str, str]:
    speller = Speller()

    lookup = dict()
    for word in words:
        corrected_word = speller.autocorrect_sentence(word)
        if corrected_word != word:
            lookup[word] = corrected_word

    return lookup


def _CorrectSpelling(user_tweet_df: DataFrame,
                     col_names: List[str],
                     lookup: Dict[str, str]):
    for _, row in user_tweet_df.iterrows():
        for col_name in col_names:
            sentence = row[col_name]
            for i in range(len(sentence)):
                if sentence[i] in lookup:
                    sentence[i] = lookup[sentence[i]]


def CorrectTweetSpelling(user_tweet_df: DataFrame) -> Dict[str, str]:
    """_summary_

    Args:
        user_tweet_df (DataFrame): _description_

    Returns:
        Dict[str, str]: _description_
    """
    text_cols = ["context_content",
                 "external_content_summary",
                 "content"]

    words = _CollectWords(user_tweet_df=user_tweet_df,
                          text_cols=text_cols)
    lookup = _BuildCorrectionLookup(words=words)
    _CorrectSpelling(user_tweet_df=user_tweet_df,
                     col_names=text_cols,
                     lookup=lookup)

    return lookup
