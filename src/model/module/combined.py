from math import ceil
from math import pow
from torch import Tensor
from torch.nn import CrossEntropyLoss
from torch.nn import Module

from src.model.example.constants import LANGUAGE_MODEL_UNMASK_TOKEN_ID
from src.model.module.user_embeddings import UserEmbeddings
from src.model.module.personalized_masked_lm import \
    PersonalizedMaskedLanguageModel


class UserProfileExtractionModel(Module):
    def __init__(self,
                 user_count: int) -> None:
        super().__init__()

        user_profile_size = int(ceil(pow(user_count, 0.25)))

        self.user_embed = UserEmbeddings(
            user_count=user_count, user_profile_size=user_profile_size)
        self.pmlm = PersonalizedMaskedLanguageModel(
            user_profile_size=user_profile_size)

    def forward(self,
                user_ids: Tensor,
                tokens: Tensor,
                attention_masks: Tensor) -> Tensor:
        """_summary_

        Args:
            user_ids (Tensor): _description_
            tokens (Tensor): _description_
            attention_masks (Tensor): _description_

        Returns:
            Tensor: _description_
        """
        user_profiles = self.user_embed(user_ids=user_ids)
        masked_tokens_preds = self.pmlm(user_profiles=user_profiles,
                                        tokens=tokens,
                                        attention_masks=attention_masks)
        return masked_tokens_preds


loss_fn = CrossEntropyLoss(ignore_index=LANGUAGE_MODEL_UNMASK_TOKEN_ID)


def Loss(masked_tokens_preds: Tensor, label_tokens: Tensor) -> Tensor:
    """_summary_

    Args:
        masked_tokens_preds (Tensor): _description_
        label_tokens (Tensor): _description_

    Returns:
        Tensor: _description_
    """
    batch_size = masked_tokens_preds.size()[0]
    seq_len = masked_tokens_preds.size()[1]
    vocab_size = masked_tokens_preds.size()[2]

    unrolled_seq_preds = masked_tokens_preds.reshape(
        (batch_size * seq_len, vocab_size))
    unrolled_label_tokens = label_tokens.reshape((batch_size*seq_len,))

    return loss_fn(unrolled_seq_preds, unrolled_label_tokens)
