from PySide6.QtWidgets import QComboBox

from src.explorer.data_profile import ProfileData
from src.explorer.view_profile import ProfileView


class FeatureView:
    """_summary_
    """

    def __init__(self,
                 feature_selector: QComboBox,
                 profile_view: ProfileView,
                 profile_data: ProfileData) -> None:
        """_summary_

        Args:
            feature_selector (QComboBox): _description_
            profile_data (ProfileData): _description_
        """
        self.feature_selector = feature_selector
        self.profile_view = profile_view
        self.profile_data = profile_data

        for feature in profile_data.GetAvailableFeatures():
            feature_selector.addItem(feature)

        self.profile_view.Plot(profile_data=profile_data,
                               feature=feature_selector.currentText())

        feature_selector.currentIndexChanged.connect(
            self._OnFeatureSelectorChanged)

    def _OnFeatureSelectorChanged(self, _: int) -> None:
        self.profile_view.Plot(profile_data=self.profile_data,
                               feature=self.feature_selector.currentText())
