import torch
from torch.nn import Module
from torch.nn import Linear
from torch.nn import ReLU
from torch.nn import Softmax
# from torch.nn.functional import one_hot
from torch import Tensor
from torch import zeros
from torch import long
from transformers import BertModel
from typing import Tuple

from src.model.example.constants import LANGUAGE_MODEL_TYPE
from src.model.example.constants import LANGUAGE_MODEL_FEATURE_SIZE
from src.model.example.constants import LANGUAGE_MODEL_VOCAB_SIZE


class PersonalizedMaskedTokenClassifier(Module):
    """_summary_
    """

    def __init__(self,
                 user_profile_size: int) -> None:
        """_summary_

        Args:
            user_profile_size (int): _description_
            year_count (int): _description_
        """
        super().__init__()

        self.bert = BertModel.from_pretrained(LANGUAGE_MODEL_TYPE)

        self.user_profile_size = user_profile_size
        # self.year_count = year_count
        year_count = 0

        all_feature_size =                      \
            user_profile_size +                 \
            year_count +                        \
            LANGUAGE_MODEL_FEATURE_SIZE

        self.seq_linear1 = Linear(
            in_features=all_feature_size,
            out_features=all_feature_size)
        self.seq_relu1 = ReLU()

        self.seq_linear2 = Linear(
            in_features=all_feature_size,
            out_features=all_feature_size)
        self.seq_relu2 = ReLU()

        self.seq_linear3 = Linear(
            in_features=all_feature_size,
            out_features=LANGUAGE_MODEL_VOCAB_SIZE)
        self.seq_softmax = Softmax(dim=1)

    def forward(self,
                user_profiles: Tensor,
                # years: Tensor,
                tokens: Tensor,
                attention_masks: Tensor) -> Tuple[Tensor, Tensor]:
        """_summary_

        Args:
            user_profiles (Tensor): _description_
            years (Tensor): _description_
            tokens (Tensor): _description_
            attention_masks (Tensor): _description_

        Returns:
            Tuple[Tensor, Tensor]: _description_
        """
        # Computes textual features.
        text_features = self.bert(
            input_ids=tokens,
            token_type_ids=zeros(size=tokens.size(), dtype=long),
            attention_mask=attention_masks)

        batch_size = text_features.last_hidden_state.size()[0]
        sequence_len = text_features.last_hidden_state.size()[1]

        # Copies the user profile vector sequence_len times.
        user_profiles_expanded = user_profiles.                         \
            view(size=(batch_size, 1, self.user_profile_size)).         \
            repeat(repeats=(1, sequence_len, 1))

        # Copies the year vector sequence_len times.
        # years_expanded = one_hot(years, num_classes=self.year_count).   \
        #     view(size=(batch_size, 1, self.year_count)).                \
        #     repeat(repeats=(1, sequence_len, 1))

        # Concatenates user profiles, year and textual features into one
        # vector.
        all_features = torch.concatenate(
            (user_profiles_expanded,
             # years_expanded,
             text_features.last_hidden_state),
            dim=2)

        # Transforms and makes masked word predictions at every location in
        # the sequence.
        z1 = self.seq_linear1(all_features)
        h1 = self.seq_relu1(z1)

        z2 = self.seq_linear2(h1)
        h2 = self.seq_relu2(all_features + z2)

        seq_logits = self.seq_linear3(h2)
        mask_preds = self.seq_softmax(seq_logits)

        return mask_preds, seq_logits
