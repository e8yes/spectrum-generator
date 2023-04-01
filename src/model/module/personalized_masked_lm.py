import torch
from torch.nn import Module
from torch.nn import Linear
from torch.nn import ReLU
from torch.nn import Softmax
from torch import Tensor
from transformers import BertModel
from transformers import BertTokenizer

_LM_FEATURE_SIZE = 768
_LM_MODEL = "bert-base-uncased"


class PersonalizedMaskedLanguageModel(Module):
    """_summary_
    """

    def __init__(self, user_profile_size: int) -> None:
        """_summary_

        Args:
            user_profile_size (int): _description_
        """
        super().__init__()

        self.bert = BertModel.from_pretrained(_LM_MODEL)
        self.tokenizer = BertTokenizer.from_pretrained(_LM_MODEL)

        self.user_profile_size = user_profile_size

        self.seq_linear1 = Linear(
            in_features=user_profile_size + _LM_FEATURE_SIZE,
            out_features=user_profile_size + _LM_FEATURE_SIZE)
        self.seq_relu = ReLU()
        self.seq_linear2 = Linear(
            in_features=user_profile_size + _LM_FEATURE_SIZE,
            out_features=self.tokenizer.vocab_size)
        self.seq_softmax = Softmax(dim=1)

        # Freezes the language model.
        for parameter in self.bert.parameters():
            parameter.requires_grad = False

    def forward(self,
                user_profiles: Tensor,
                tokens: Tensor,
                token_types: Tensor,
                attention_mask: Tensor) -> Tensor:
        """_summary_

        Args:
            user_profiles (Tensor): _description_
            tokens (Tensor): _description_
            token_types (Tensor): _description_
            attention_mask (Tensor): _description_

        Returns:
            Tensor: _description_
        """
        # Computes textual features.
        text_features = self.bert(
            input_ids=tokens,
            token_type_ids=token_types,
            attention_mask=attention_mask)

        # Concatenates user profiles with textual features.
        batch_size = text_features.last_hidden_state.size()[0]
        sequence_len = text_features.last_hidden_state.size()[1]

        user_profiles_expanded = torch.reshape(
            input=user_profiles,
            shape=(batch_size, 1, self.user_profile_size)).\
            repeat(repeats=(1, sequence_len, 1))

        all_features = torch.concatenate(
            (user_profiles_expanded,
             text_features.last_hidden_state),
            dim=2)

        # Transforms and makes masked word predictions at every location in
        # the sequence.
        z1 = self.seq_linear1(all_features)
        h1 = self.seq_relu(z1)
        seq_logits = self.seq_linear2(h1)
        mask_preds = self.seq_softmax(seq_logits)

        return mask_preds
