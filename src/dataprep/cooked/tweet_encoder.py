from pandas import DataFrame
from sentence_transformers import SentenceTransformer
from torch import Tensor
from torch import no_grad


def _Encode(sentence: str, model: SentenceTransformer) -> Tensor:
    with no_grad():
        return model.                                   \
            encode(sentence, convert_to_tensor=True).   \
            detach().                                   \
            numpy()


def EncodeContent(user_repr_tweets: DataFrame) -> None:
    """_summary_

    Args:
        user_repr_tweets (DataFrame): _description_
    """
    model = SentenceTransformer('distilroberta-base-paraphrase-v1')

    user_repr_tweets["embedding"] = user_repr_tweets["content"].map(
        lambda sentence: _Encode(sentence=sentence, model=model))
