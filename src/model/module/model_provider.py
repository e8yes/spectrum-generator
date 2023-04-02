from torch.nn import Module
from torch import Tensor


class ModelProviderInterface:
    """_summary_
    """

    def __init__(self) -> None:
        pass

    def Name(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return None

    def LoadOrCreate(self, model_path: str) -> Module:
        """_summary_

        Args:
            model_path (str): _description_

        Returns:
            Module: _description_
        """
        return None

    def Loss(self,
             model: Module,
             user_ids: Tensor,
             years: Tensor,
             tokens: Tensor,
             attention_masks: Tensor,
             labels: Tensor) -> Tensor:
        """_summary_

        Args:
            model (Module): _description_
            user_ids (Tensor): _description_
            years (Tensor): _description_
            tokens (Tensor): _description_
            attention_masks (Tensor): _description_
            labels (Tensor): _description_

        Returns:
            Tensor: _description_
        """
        return None
