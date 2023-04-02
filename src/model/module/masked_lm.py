from transformers import BertForMaskedLM
from torch.nn import Module
from torch import Tensor
from torch import zeros
from torch import long

from src.model.example.constants import LANGUAGE_MODEL_TYPE
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
                attention_masks: Tensor,
                label_tokens: Tensor) -> Tensor:
        output = self.bert(
            input_ids=tokens,
            token_type_ids=zeros(size=tokens.size(), dtype=long),
            attention_mask=attention_masks,
            labels=label_tokens)
        return output.loss


class BaselineMaskedLanguageModelProvider(ModelProviderInterface):
    """_summary_

    Args:
        ModelProviderInterface (_type_): _description_
    """

    def __init__(self) -> None:
        super().__init__()

    def Name(self) -> str:
        return "baseline_model"

    def LoadOrCreate(self, model_path: str):
        if model_path is not None:
            self.Load(model_path=model_path)
            return

        self.model = BaselineMaskedLanguageModel()

    def Loss(self,
             user_ids: Tensor,
             years: Tensor,
             tokens: Tensor,
             attention_masks: Tensor,
             labels: Tensor) -> Tensor:
        return self.model(tokens=tokens,
                          attention_masks=attention_masks,
                          label_tokens=labels)
