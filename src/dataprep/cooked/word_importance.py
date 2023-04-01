import numpy as np
from pandas import DataFrame
from pandas import Series
from typing import Dict


def _ToWordAndId(user_tweet_df: DataFrame,
                 text_col_name: str) -> DataFrame:

    id_col = list()
    word_col = list()

    for _, row in user_tweet_df.iterrows():
        for word in set(row[text_col_name]):
            id_col.append(row["tweet_id"])
            word_col.append(word)

    return DataFrame(data={
        "word": word_col,
        "tweet_id": id_col
    })


def _ComputeWordIdf(user_tweet_df: DataFrame,
                    text_col_name: str):
    doc_count = user_tweet_df.shape[0]

    word_and_id = _ToWordAndId(user_tweet_df=user_tweet_df,
                               text_col_name=text_col_name)
    word_and_doc_freq = word_and_id.        \
        groupby("word").                    \
        count().                            \
        rename(columns={"tweet_id": "df"}). \
        reset_index()

    word_and_doc_freq["idf"] = np.log(
        doc_count / word_and_doc_freq["df"])

    word_and_doc_freq.sort_values(
        by="idf", ascending=False, inplace=True)

    return word_and_doc_freq


def _ToIdfLookup(word_and_doc_freq: DataFrame) -> Dict[str, float]:
    idf_lookup = dict()

    for _, row in word_and_doc_freq.iterrows():
        idf_lookup[row["word"]] = row["idf"]

    return idf_lookup


def _ComputeSentenceImportance(user_tweet_df: DataFrame,
                               text_col_name: str,
                               idf_lookup: Dict[str, float]) -> Series:
    col = list()

    for _, row in user_tweet_df.iterrows():
        sentence_importance = list()

        for word in set(row[text_col_name]):
            if word in idf_lookup:
                sentence_importance.append(idf_lookup[word])
            else:
                sentence_importance.append(0.0)

        s = sum(sentence_importance)
        for i in range(len(sentence_importance)):
            sentence_importance[i] /= s

        col.append(sentence_importance)

    return col


def AssignWordImportance(user_tweet_df: DataFrame) -> DataFrame:
    """_summary_

    Args:
        user_tweet_df (DataFrame): _description_
    """
    text_col_name = "content"

    word_and_doc_freq = _ComputeWordIdf(user_tweet_df=user_tweet_df,
                                        text_col_name=text_col_name)
    idf_lookup = _ToIdfLookup(word_and_doc_freq=word_and_doc_freq)

    user_tweet_df[text_col_name + "_importance"] = \
        _ComputeSentenceImportance(user_tweet_df=user_tweet_df,
                                   text_col_name=text_col_name,
                                   idf_lookup=idf_lookup)

    return word_and_doc_freq
