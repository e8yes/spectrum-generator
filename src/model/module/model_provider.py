from os import path
from torch import Tensor
from torch import load
from torch import save
from torch.nn import Module
from torch.nn import Parameter
from typing import List
from typing import Tuple


class ModelProviderInterface:
    """_summary_
    """

    def __init__(self) -> None:
        self.model = Module()

    def Name(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        raise NotImplementedError()

    def LoadOrCreate(self, model_path: str) -> None:
        """_summary_

        Args:
            model_path (str): _description_

        Returns:
            Module: _description_
        """
        raise NotImplementedError()

    def Loss(self,
             user_ids: Tensor,
             creation_year_ids: Tensor,
             tokens: Tensor,
             attention_masks: Tensor,
             labels: Tensor) -> Tensor:
        """_summary_

        Args:
            user_ids (Tensor): _description_
            creation_year_ids (Tensor): _description_
            tokens (Tensor): _description_
            attention_masks (Tensor): _description_
            labels (Tensor): _description_

        Returns:
            Tensor: _description_
        """
        raise NotImplementedError()

    def ExportExtractedInsights(self, output_path: str, tag: str) -> None:
        """_summary_

        Args:
            output_path (str): _description_
            tag (str): _description_

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError()

    def SetMode(self, mode: str) -> None:
        """_summary_

        Args:
            mode (str): _description_
        """
        if mode == "train":
            self.model.train()
        elif mode == "eval":
            self.model.eval()
        else:
            assert False

    def TrainableParameters(self) -> Tuple[List[Parameter], int]:
        """_summary_

        Returns:
            Tuple[List[Parameter], int]: _description_
        """
        params = [p for p in self.model.parameters() if p.requires_grad]
        param_count = sum(p.numel() for p in params)

        return params, param_count

    def Load(self, model_path: str) -> None:
        """_summary_

        Args:
            model_path (str): _description_
        """
        assert model_path is not None

        model_input_path = path.join(model_path,
                                     f"{self.Name()}.pt")
        self.model = load(model_input_path)

    def Save(self, model_path: str, tag: str) -> None:
        """_summary_

        Args:
            model_path (str): _description_
            tag (str): _description_
        """
        assert model_path is not None
        assert tag is not None

        model_output_path = path.join(
            model_path,
            f"{self.Name()}_{tag}.pt")
        save(self.model, model_output_path)
