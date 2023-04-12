from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QRadioButton

from src.explorer.data_profile import ProfileData
from src.explorer.view_compare_user import UserComparisonView


class SearchUserView:
    """_summary_
    """

    def __init__(self,
                 select_source_radio: QRadioButton,
                 select_target_radio: QRadioButton,
                 search_input: QLineEdit,
                 search_button: QPushButton,
                 user_comparison_view: UserComparisonView,
                 profile_data: ProfileData) -> None:
        self.search_input = search_input
        self.user_comparison_view = user_comparison_view
        self.profile_data = profile_data

        select_source_radio.clicked.connect(self._OnSetSourceMode)
        select_target_radio.clicked.connect(self._OnSetTargetMode)
        self.mode = "source" if select_source_radio.isChecked() else "target"

        search_button.clicked.connect(self._OnClickSearchUser)

    def SetSearchedUser(self, user_name: str) -> bool:
        """_summary_

        Args:
            user_name (str): _description_

        Returns:
            bool: _description_
        """
        u = self.profile_data.SearchDatapoint(user_name=user_name)
        if u is None:
            return False

        if self.mode == "source":
            self.user_comparison_view.SetSourceUser(user_name=user_name)
        else:
            self.user_comparison_view.SetTargetUser(user_name=user_name)

        return True

    def _OnSetSourceMode(self):
        self.mode = "source"

    def _OnSetTargetMode(self):
        self.mode = "target"

    def _OnClickSearchUser(self):
        user_name = self.search_input.text()[1:]

        exists = self.SetSearchedUser(user_name=user_name)
        if not exists:
            popup = QMessageBox()
            popup.setIcon(QMessageBox.Icon.Critical)
            popup.setText(
                f"The user '{user_name}' can't be found from the profile.")
            popup.setWindowTitle("User Not Found")
            popup.setStandardButtons(QMessageBox.Ok)

            popup.exec()
