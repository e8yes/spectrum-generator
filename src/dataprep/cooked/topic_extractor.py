from keybert import KeyBERT
from nltk import word_tokenize
from pandas import DataFrame
from torch import no_grad
from typing import Dict


# Define input sentence
sentence = "The quick brown fox jumps over the lazy dog."


def _ExtractTags(sentence: str, model: KeyBERT) -> Dict[str, float]:
    keywords = list()
    with no_grad():
        keywords = model.extract_keywords(
            sentence,
            keyphrase_ngram_range=(1, 2),
            stop_words=None,
            top_n=5)

    result = dict()
    total_score = 0

    for phrase, score in keywords:
        for word in word_tokenize(phrase):
            if word not in result:
                result[word] = score
            else:
                result[word] += score

            total_score += score

    for tag in result:
        result[tag] /= total_score

    return result


def AnnotateTopics(user_repr_tweets: DataFrame) -> None:
    """_summary_

    Args:
        user_repr_tweets (DataFrame): _description_
    """
    model = KeyBERT()
    user_repr_tweets["tags"] = user_repr_tweets["content"].map(
        lambda sentence: _ExtractTags(sentence=sentence, model=model))
