from transformers import BertForMaskedLM
from torch.nn import CrossEntropyLoss
from torch.nn import Module
from torch import Tensor
from torch import zeros
from torch import long

from src.model.example.constants import LANGUAGE_MODEL_TYPE
from src.model.example.constants import LANGUAGE_MODEL_VOCAB_SIZE
from src.model.example.constants import LANGUAGE_MODEL_UNMASK_TOKEN_ID
from src.model.module.model_provider import ModelProviderInterface


class BaselineMaskedLanguageModel(Module):
    """_summary_
    """

    def __init__(self) -> None:
        """_summary_
        """
        super().__init__()
        self.bert = BertForMaskedLM.from_pretrained(LANGUAGE_MODEL_TYPE)

    def forward(self,
                tokens: Tensor,
                attention_masks: Tensor) -> Tensor:
        output = self.bert(
            input_ids=tokens,
            token_type_ids=zeros(size=tokens.size(), dtype=long),
            attention_mask=attention_masks)
        return output.logits


class BaselineModelProvider(ModelProviderInterface):
    """_summary_

    Args:
        ModelProviderInterface (_type_): _description_
    """

    def __init__(self) -> None:
        super().__init__()

        self.loss_fn = CrossEntropyLoss(
            ignore_index=LANGUAGE_MODEL_UNMASK_TOKEN_ID,
            reduction="mean")

    def Name(self) -> str:
        return "baseline_model"

    def LoadOrCreate(self, model_path: str):
        if model_path is not None:
            self.Load(model_path=model_path)
            return

        self.model = BaselineMaskedLanguageModel()

    def Loss(self,
             user_ids: Tensor,
             creation_year_ids: Tensor,
             tokens: Tensor,
             attention_masks: Tensor,
             labels: Tensor) -> Tensor:
        seq_logits = self.model(tokens=tokens,
                                attention_masks=attention_masks)

        unrolled_seq_logits = seq_logits.\
            view(size=(-1, LANGUAGE_MODEL_VOCAB_SIZE))
        unrolled_label_tokens = labels.view(size=(-1,))

        return self.loss_fn(unrolled_seq_logits, unrolled_label_tokens)

    def ExportExtractedInsights(self, output_path: str, tag: str) -> None:
        # Nothing to export.
        return
