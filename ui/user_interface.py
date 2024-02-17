from PyQt6.QtWidgets import QMainWindow

from ui.buttons import Connect_Buttons
from ui.prepare_window import Prepare_Window
from ui.images import Load_Images_And_Icons
from ui.styles import Load_Styles
from ui.tools import CheckUserOs


class User_UI(QMainWindow):
    def __init__(self, app_version, logger, appdir) -> None:
        super().__init__()
        self.app_version = app_version
        self.logger = logger
        self.appdir = appdir
        self.ui = None
        Start_App(self)
        CheckUserOs(self)


def Start_App(self) -> None:
    # Anywhere shit
    Prepare_Window(self)

    # Connect buttons
    Connect_Buttons(self)

    # Load images and Icons
    Load_Images_And_Icons(self)

    # Load styles
    Load_Styles(self)

    # Show UI
    self.stackedWidget.setCurrentIndex(0)
    self.ui.show()
    self.logger.debug(f"Load_UI : UI showed")
