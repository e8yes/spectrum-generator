# This Python file uses the following encoding: utf-8

from numpy import ndarray
from numpy import squeeze
from numpy import vstack
from numpy.linalg import norm
from pandas import DataFrame
from pandas import read_pickle
from sklearn.manifold import TSNE
from typing import List
from typing import Optional


class ProfileData:
    """_summary_
    """

    def __init__(self, profile_data_path: str) -> None:
        """_summary_

        Args:
            profile_data_path (str): _description_
        """
        self.df: DataFrame = read_pickle(filepath_or_buffer=profile_data_path)
        self.cached_vis_embed = None

    def GetAvailableFeatures(self) -> List[str]:
        """_summary_

        Returns:
            List[str]: _description_
        """
        result = list()

        for column in self.df.columns:
            if column in {"user_id", "user_name", "profile"}:
                continue

            result.append(column)

        return sorted(result)

    def GetFeatures(self, feature: str) -> ndarray:
        """_summary_

        Args:
            feature (str): _description_

        Returns:
            ndarray: _description_
        """
        col = vstack(self.df[feature].values)
        return squeeze(col)

    def ComputeVisualizationEmbeddings(self) -> ndarray:
        """_summary_

        Returns:
            ndarray: _description_
        """
        if self.cached_vis_embed is not None:
            return self.cached_vis_embed

        profiles = vstack(self.df["profile"].values)

        tsne = TSNE(n_components=2, random_state=42)
        self.cached_vis_embed = tsne.fit_transform(profiles)

        return self.cached_vis_embed

    def SearchDatapoint(self, user_name: str) -> Optional[int]:
        """_summary_

        Args:
            user_name (str): _description_

        Returns:
            Optional[int]: _description_
        """
        query_result = self.df[self.df["user_name"] == user_name].index
        if query_result.shape[0] == 0:
            return None

        return query_result[0]

    def ComputeDistanceBetween(self,
                               user_name1: str,
                               user_name2: str) -> float:
        """_summary_

        Args:
            user_name1 (str): _description_
            user_name2 (str): _description_

        Returns:
            float: _description_
        """
        user1_profile = self.df[self.df["user_name"]
                                == user_name1]["profile"].values[0]
        user2_profile = self.df[self.df["user_name"]
                                == user_name2]["profile"].values

        print(user1_profile.shape)

        return norm(user1_profile - user2_profile)
