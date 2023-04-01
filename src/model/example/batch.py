from pandas import DataFrame
from torch import Tensor
from torch import full
from torch import hstack
from torch import vstack
from typing import List
from typing import Tuple

from src.model.example.constants import LANGUAGE_MODEL_MASK_TOKEN_ID
from src.model.example.constants import LANGUAGE_MODEL_UNMASK_TOKEN_ID
from src.model.example.constants import LANGUAGE_MODEL_PAD_TOKEN_ID
from src.model.example.example import Example
from src.model.example.example import ExampleBuilder


def _MaxSequenceLength(examples: List[Example]) -> int:
    max_len = 0

    for example in examples:
        seq_len = example.label_token_ids.size()[1]
        max_len = max(max_len, seq_len)

    return max_len


def _CollectExamples(
        examples: List[Example]) -> Tuple[List[Tensor],
                                          List[Tensor],
                                          List[Tensor]]:
    user_ids = list()
    masked_tokens = list()
    label_tokens = list()

    for example in examples:
        user_ids.append(example.user_id)
        masked_tokens.append(example.masked_token_ids)
        label_tokens.append(example.label_token_ids)

    return user_ids, masked_tokens, label_tokens


def _PaddedSequences(seqs: List[Tensor], max_len: int) -> Tensor:
    result_seqs = list()

    for seq in seqs:
        pad = full(size=((1, max_len - seq.size()[1])),
                   fill_value=LANGUAGE_MODEL_PAD_TOKEN_ID)
        padded = hstack(tensors=(seq, pad))
        result_seqs.append(padded)

    return vstack(result_seqs)


class BatchExamples:
    """_summary_
    """

    def __init__(self,
                 user_ids: Tensor,
                 masked_token_ids: Tensor,
                 attention_masks: Tensor,
                 label_token_ids: Tensor) -> None:
        """_summary_

        Args:
            user_ids (Tensor): _description_
            masked_token_ids (Tensor): _description_
            attention_masks (Tensor): _description_
            label_token_ids (Tensor): _description_
        """
        self.user_ids = user_ids
        self.masked_token_ids = masked_token_ids
        self.attention_masks = attention_masks
        self.label_token_ids = label_token_ids

    def __repr__(self) -> str:
        return f"user_ids={self.user_ids}\n\
masked_token_ids={self.masked_token_ids}\n\
attention_masks={self.attention_masks}\n\
label_token_ids={self.label_token_ids}"


class BatchExampleBuilder:
    def __init__(self) -> None:
        self.example_builder = ExampleBuilder()

    def Build(self, batch: DataFrame) -> BatchExamples:
        """_summary_

        Args:
            batch (DataFrame): _description_

        Returns:
            BatchExamples: _description_
        """
        examples = list()

        for i in range(batch.shape[0]):
            row = batch.iloc[i]

            example = self.example_builder.Build(
                user_id=row["user_id"],
                context_content=row["context_content"],
                external_content_summary=row["external_content_summary"],
                content=row["content"],
                content_importance=row["content_importance"])

            examples.append(example)

        user_ids, masked_tokens, label_tokens = _CollectExamples(
            examples=examples)

        user_ids = vstack(user_ids)

        max_len = _MaxSequenceLength(examples=examples)
        masked_tokens = _PaddedSequences(seqs=masked_tokens, max_len=max_len)
        attention_masks = (masked_tokens != LANGUAGE_MODEL_PAD_TOKEN_ID).long()

        label_tokens = _PaddedSequences(seqs=label_tokens, max_len=max_len)
        label_tokens[masked_tokens != LANGUAGE_MODEL_MASK_TOKEN_ID] = \
            LANGUAGE_MODEL_UNMASK_TOKEN_ID

        return BatchExamples(
            user_ids=user_ids,
            masked_token_ids=masked_tokens,
            attention_masks=attention_masks,
            label_token_ids=label_tokens)
