from typing import List
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QTextBrowser

from src.explorer.profile_explorer.data_profile import ProfileData
from src.explorer.profile_explorer.data_representative import \
    RepresentativeData
from src.explorer.profile_explorer.data_representative import \
    RepresentativeEntry


def _GenerateOutputText(
        user_name: str, entries: List[RepresentativeEntry]) -> str:
    result = f"@{user_name}\n\n"

    for i in range(len(entries)):
        result += f"TWEET_{i + 1}.popularity={entries[i].popularity}\n"
        if entries[i].context is not None and len(entries[i].context) > 0:
            result += f"\t{entries[i].context}\n"
            result += "\t--------------CONTEXT END--------------\n"

        result += f"\t{entries[i].content}\n\n"
        result += f"{entries[i].tags}\n"
        result += "----------------------------------------------------------"\
                  "--------------------------------------------------------\n"

    return result


class UserComparisonView:
    def __init__(self,
                 distance_output_text: QLineEdit,
                 source_output_text: QTextBrowser,
                 target_output_text: QTextBrowser,
                 profile_data: ProfileData,
                 rep_data: RepresentativeData) -> None:
        """_summary_

        Args:
            distance_output_text (QLineEdit): _description_
            source_output_text (QTextBrowser): _description_
            target_output_text (QTextBrowser): _description_
            profile_data (ProfileData): _description_
            rep_data (RepresentativeData): _description_
        """
        self.distance_output_text = distance_output_text
        self.source_output_text = source_output_text
        self.target_output_text = target_output_text
        self.profile_data = profile_data
        self.rep_data = rep_data

        self.source_user_name = None
        self.target_user_name = None

    def _UpdateProfileDistance(self):
        if self.source_user_name is None or self.target_user_name is None:
            self.distance_output_text.setText("nan")
            return

        distance = self.profile_data.ComputeDistanceBetween(
            user_name1=self.source_user_name, user_name2=self.target_user_name)
        self.distance_output_text.setText(str(distance))

    def _UpdateOutputText(self):
        source_user_tweets = list()
        if self.source_user_name is not None:
            source_user_tweets = self.rep_data.GetMostPopularEntries(
                user_name=self.source_user_name)
            source_text = _GenerateOutputText(
                self.source_user_name, entries=source_user_tweets)
            self.source_output_text.setText(source_text)

        if self.target_user_name is not None:
            target_user_tweets = self.rep_data.GetMostMatchingEntries(
                user_name=self.target_user_name,
                context=source_user_tweets)
            target_text = _GenerateOutputText(
                user_name=self.target_user_name,
                entries=target_user_tweets)
            self.target_output_text.setText(target_text)

    def SetSourceUser(self, user_name: str):
        self.source_user_name = user_name
        self._UpdateProfileDistance()
        self._UpdateOutputText()

    def SetTargetUser(self, user_name: str):
        self.target_user_name = user_name
        self._UpdateProfileDistance()
        self._UpdateOutputText()
