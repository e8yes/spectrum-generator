from math import ceil
from math import pow
from torch import Tensor
from torch.nn import CrossEntropyLoss
from torch.nn import Module
from typing import Tuple

from src.model.example.constants import LANGUAGE_MODEL_UNMASK_TOKEN_ID
from src.model.example.constants import LANGUAGE_MODEL_VOCAB_SIZE
from src.model.module.user_embeddings import UserEmbeddings
from src.model.module.personalized_masked_token_classifier import \
    PersonalizedMaskedTokenClassifier
from src.model.module.model_provider import ModelProviderInterface


class PersonalizedMaskedLanguageModel(Module):
    def __init__(self,
                 user_count: int) -> None:
        super().__init__()

        user_profile_size = int(ceil(pow(user_count, 0.25)))

        self.user_embed = UserEmbeddings(
            user_count=user_count, user_profile_size=user_profile_size)
        self.classifer = PersonalizedMaskedTokenClassifier(
            user_profile_size=user_profile_size)

    def forward(self,
                user_ids: Tensor,
                tokens: Tensor,
                attention_masks: Tensor) -> Tuple[Tensor, Tensor]:
        """_summary_

        Args:
            user_ids (Tensor): _description_
            tokens (Tensor): _description_
            attention_masks (Tensor): _description_

        Returns:
            Tensor: _description_
        """
        user_profiles = self.user_embed(user_ids=user_ids)
        masked_tokens_preds, masked_tokens_logits = self.classifer(
            user_profiles=user_profiles,
            tokens=tokens,
            attention_masks=attention_masks)
        return masked_tokens_preds, masked_tokens_logits


loss_fn = CrossEntropyLoss(ignore_index=LANGUAGE_MODEL_UNMASK_TOKEN_ID,
                           reduction="mean")


def Loss(preds_and_logits: Tuple[Tensor, Tensor],
         label_tokens: Tensor) -> Tensor:
    """_summary_

    Args:
        masked_tokens_preds (Tensor): _description_
        label_tokens (Tensor): _description_

    Returns:
        Tensor: _description_
    """
    _, seq_logits = preds_and_logits

    unrolled_seq_logits = seq_logits.\
        view(size=(-1, LANGUAGE_MODEL_VOCAB_SIZE))
    unrolled_label_tokens = label_tokens.view(size=(-1,))

    return loss_fn(unrolled_seq_logits, unrolled_label_tokens)


class PersonalizedModelProvider(ModelProviderInterface):
    """_summary_

    Args:
        ModelProviderInterface (_type_): _description_
    """

    def __init__(self, user_count: int) -> None:
        """_summary_

        Args:
            user_count (int): _description_
        """
        super().__init__()

        self.user_count = user_count

    def Name(self) -> str:
        return "personalized_model"

    def LoadOrCreate(self, model_path: str) -> Module:
        if model_path is not None:
            self.Load(model_path=model_path)
            return

        self.model = PersonalizedMaskedLanguageModel(
            user_count=self.user_count)

    def Loss(self,
             user_ids: Tensor,
             years: Tensor,
             tokens: Tensor,
             attention_masks: Tensor,
             labels: Tensor) -> Tensor:
        preds_and_logits = self.model(
            user_ids=user_ids,
            tokens=tokens,
            attention_masks=attention_masks)

        return Loss(preds_and_logits=preds_and_logits,
                    label_tokens=labels)
