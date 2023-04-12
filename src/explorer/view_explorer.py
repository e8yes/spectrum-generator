# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QWidget

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py
from src.explorer.ui_form import Ui_Widget

from src.explorer.data_profile import ProfileData
from src.explorer.data_representative import RepresentativeData
from src.explorer.view_compare_user import UserComparisonView
from src.explorer.view_search_user import SearchUserView
from src.explorer.view_feature import FeatureView
from src.explorer.view_profile import ProfileView


class MainExplorerView(QWidget):
    """_summary_

    Args:
        QWidget (_type_): _description_
    """

    def __init__(self,
                 profile_data: ProfileData,
                 representative_data: RepresentativeData,
                 parent: QWidget = None):
        """_summary_

        Args:
            profile_data (ProfileData): _description_
            representative_data (RepresentativeData): _description_
            parent (QWidget, optional): _description_. Defaults to None.
        """
        super().__init__(parent)

        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.user_comparison_view = UserComparisonView(
            distance_output_text=self.ui.profile_distance_output,
            source_output_text=self.ui.source_user_tweet_output,
            target_output_text=self.ui.target_user_tweet_output,
            profile_data=profile_data,
            rep_data=representative_data)

        self.search_user_view = SearchUserView(
            select_source_radio=self.ui.source_mode_radio,
            select_target_radio=self.ui.target_mode_radio,
            search_input=self.ui.user_name_input,
            user_comparison_view=self.user_comparison_view,
            search_button=self.ui.search_user_button,
            profile_data=profile_data)

        self.profile_view = ProfileView(
            scatter_chart_frame=self.ui.scatter_chart,
            search_user_view=self.search_user_view)

        self.feature_view = FeatureView(
            feature_selector=self.ui.feature_combo_box,
            profile_view=self.profile_view,
            profile_data=profile_data)
