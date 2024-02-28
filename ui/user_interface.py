from configparser import ConfigParser

from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow

from ui.animations import App_Open_Anim
from ui.buttons import Connect_Buttons
from ui.hide_elements import Hide_Elements
from ui.images import Load_Images_And_Icons
from ui.prepare_window import Prepare_Window
from ui.styles import Load_Styles
from ui.tools import CheckUserOs, Load_Settings, CheckUpdate


class User_UI(QMainWindow):
    def __init__(self, app_version, logger, appdir) -> None:
        super().__init__()
        self.app_version = app_version
        self.logger = logger
        self.appdir = appdir
        self.ui = None
        self.app_theme = None
        self.check_thread = None
        self.offset = None
        self.config_path = self.appdir + "\\" + "config.ini"
        self.config = ConfigParser()
        self.isVulnersKeyValid = False
        self.isSliderTimerStart = False
        self.result_list_model = None
        Start_App(self)
        CheckUserOs(self)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)


def Start_App(self) -> None:
    # Anywhere shit
    Prepare_Window(self)

    # Load settings
    Load_Settings(self)

    # Hide elements
    Hide_Elements(self)

    # Connect buttons
    Connect_Buttons(self)

    # Load images and Icons
    Load_Images_And_Icons(self)

    # Load styles
    Load_Styles(self)

    # Show UI
    App_Open_Anim(self)

    # Check new versions
    CheckUpdate(self)
