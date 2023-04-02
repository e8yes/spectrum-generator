from torch import Tensor
from torch import LongTensor
from torch import full
from torch import hstack
from torch import long
from transformers import BertTokenizer
from typing import List
from typing import Set
from math import ceil
import numpy as np

from src.model.example.constants import LANGUAGE_MODEL_TYPE
# from src.model.example.constants import LANGUAGE_MODEL_CLS_TOKEN_ID
from src.model.example.constants import LANGUAGE_MODEL_SEP_TOKEN_ID
from src.model.example.constants import LANGUAGE_MODEL_MASK_TOKEN_ID


def SampleSentenceMask(sentence: List[str],
                       word_importance: List[float],
                       mask_ratio: float = 0.15) -> Set[int]:
    """_summary_

    Args:
        sentence (List[str]): _description_
        word_importance (List[float]): _description_
        mask_ratio (float, optional): _description_. Defaults to 0.15.

    Returns:
        List[int]: _description_
    """
    word_count = len(sentence)
    mask_count = min(word_count, ceil(word_count * mask_ratio))
    positions = np.arange(start=0, stop=word_count)
    masked_positions = np.random.choice(
        a=positions, size=mask_count, p=word_importance)

    result = set()
    for position in masked_positions:
        if sentence[position].startswith("~"):
            continue

        result.add(position)

    return result


def EncodeMaskedInput(text: List[str],
                      masked_positions: Set[int],
                      tokenizer: BertTokenizer) -> Tensor:
    label_codes = list()
    masked_codes = list()

    for i in range(len(text)):
        label_code = tokenizer(text=text[i],
                               add_special_tokens=False,
                               return_token_type_ids=False,
                               return_attention_mask=False,
                               return_tensors="pt")["input_ids"].long()

        masked_code: Tensor = None
        if i in masked_positions:
            masked_code = full(
                size=label_code.size(),
                fill_value=LANGUAGE_MODEL_MASK_TOKEN_ID,
                dtype=long)
        else:
            masked_code = label_code

        label_codes.append(label_code)
        masked_codes.append(masked_code)

    return (
        hstack(tensors=label_codes),
        hstack(tensors=masked_codes)
    )


class Example:
    """_summary_
    """

    def __init__(self,
                 user_id: Tensor,
                 creation_year_id: Tensor,
                 masked_token_ids: Tensor,
                 label_token_ids: Tensor) -> None:
        """_summary_

        Args:
            user_id (Tensor): _description_
            creation_year_id (Tensor): _description_
            masked_token_ids (Tensor): _description_
            label_token_ids (Tensor): _description_
        """
        self.user_id = user_id
        self.creation_year_id = creation_year_id
        self.masked_token_ids = masked_token_ids
        self.label_token_ids = label_token_ids


class ExampleBuilder:
    """_summary_
    """

    def __init__(self) -> None:
        """_summary_
        """
        self.tokenizer = BertTokenizer.from_pretrained(LANGUAGE_MODEL_TYPE)

    def Build(self,
              user_id: int,
              creation_year_id: int,
              context_content: List[str],
              external_content_summary: List[str],
              content: List[str],
              content_importance: List[float]) -> Example:
        """_summary_

        Args:
            user_id (int): _description_
            context_content (List[str]): _description_
            external_content_summary (List[str]): _description_
            content (List[str]): _description_
            content_importance (List[float]): _description_

        Returns:
            Example: _description_
        """
        sep = LongTensor([[LANGUAGE_MODEL_SEP_TOKEN_ID]])

        training_features = list()
        training_label = list()

        if len(context_content) > 0:
            context_code = self.tokenizer(
                " ".join(context_content),
                add_special_tokens=False,
                return_token_type_ids=False,
                return_attention_mask=False,
                return_tensors="pt")["input_ids"].long()

            training_features.append(context_code)
            training_features.append(sep)
            training_label.append(context_code)
            training_label.append(sep)

        if len(external_content_summary) > 0:
            external_content_summary_code = self.tokenizer(
                " ".join(external_content_summary),
                add_special_tokens=False,
                return_token_type_ids=False,
                return_attention_mask=False,
                return_tensors="pt")["input_ids"].long()

            training_features.append(external_content_summary_code)
            training_features.append(sep)
            training_label.append(external_content_summary_code)
            training_label.append(sep)

        masked_positions = SampleSentenceMask(
            sentence=content, word_importance=content_importance)
        label_content_code, masked_content_code = EncodeMaskedInput(
            text=content,
            masked_positions=masked_positions,
            tokenizer=self.tokenizer)

        training_features.append(masked_content_code)
        training_features.append(sep)
        training_label.append(label_content_code)
        training_label.append(sep)

        masked_token_ids = hstack(training_features)
        label_token_ids = hstack(training_label)

        return Example(user_id=LongTensor([user_id]),
                       creation_year_id=LongTensor([creation_year_id]),
                       masked_token_ids=masked_token_ids,
                       label_token_ids=label_token_ids)
