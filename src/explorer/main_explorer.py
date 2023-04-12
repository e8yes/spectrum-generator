import argparse
import sys
from PySide6.QtWidgets import QApplication

from src.explorer.data_profile import ProfileData
from src.explorer.data_representative import \
    RepresentativeData
from src.explorer.view_explorer import MainExplorerView


def _Launch(profile_data_path: str, rep_data_path: str) -> None:
    app = QApplication(sys.argv)

    profile_data = ProfileData(profile_data_path=profile_data_path)
    representative_data = RepresentativeData(rep_data_path=rep_data_path)

    explorer = MainExplorerView(
        profile_data=profile_data,
        representative_data=representative_data)
    explorer.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Launches the user profile explorer GUI program.")

    parser.add_argument(
        "--profile_data_path",
        type=str,
        help="Path to the user features and profile data frame file.")
    parser.add_argument(
        "--rep_data_path",
        type=str,
        help="Path to the representative user tweets data frame file.")

    args = parser.parse_args()

    if args.profile_data_path is None:
        print("profile_data_path is required.")
        exit(-1)
    if args.rep_data_path is None:
        print("rep_data_path is required.")
        exit(-1)

    _Launch(profile_data_path=args.profile_data_path,
            rep_data_path=args.rep_data_path)
