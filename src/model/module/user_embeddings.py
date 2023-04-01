import numpy as np
from torch import Tensor
from torch.nn import Module
from torch.nn import Embedding


class UserEmbeddings(Module):
    """_summary_

    Args:
        Module (_type_): _description_
    """

    def __init__(self,
                 user_count: int,
                 user_profile_size: int) -> None:
        """_summary_

        Args:
            user_count (int): _description_
            user_profile_size (int): _description_
        """
        super().__init__()

        self.user_embeddings = Embedding(
            num_embeddings=user_count,
            embedding_dim=user_profile_size)

    def forward(self, user_ids: Tensor) -> Tensor:
        """_summary_

        Args:
            user_ids (Tensor): _description_

        Returns:
            Tensor: _description_
        """
        return self.user_embeddings(user_ids)

    def Save(self, file_path: str) -> None:
        """_summary_

        Args:
            file_path (str): _description_
        """
        profiles = self.user_embeddings.    \
            weight.                         \
            detach().                       \
            numpy()
        np.savetxt(fname=file_path, X=profiles)
