import sys

from PyQt6 import uic, QtGui
from PyQt6.QtCore import Qt
from screeninfo import get_monitors

from ui.tools import GetRelPath


def Prepare_Window(self):
    ui_path = GetRelPath(self, "assets/app.ui")
    self.logger.debug(f"Prepare_Window : Loading UI : {ui_path}")

    # Load UI file

    self.ui = uic.loadUi(ui_path, self)
    self.logger.debug(f"Prepare_Window : UI loaded")

    # Icon
    self.ui.setWindowIcon(QtGui.QIcon(GetRelPath(self, "assets//icons//bender.ico.ui")))
    self.logger.debug(f"Prepare_Window : Icon seted")

    # Title
    self.ui.setWindowTitle("Windows Vulnerability Scanner")
    self.logger.debug(f"Prepare_Window : Title seted")

    # Set version
    self.ui.app_ver.setText(
        f"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\">ver {self.app_version}</span></p"
        f"></body></html>")
    self.ui.python_version.setText(
        f"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\">Python {sys.version}</span></p"
        f"></body></html>")
    self.logger.debug(f"Prepare_Window : Versions seted")

    # Window settings
    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    # Set geometry 3/4 primary screen size and move to screen center
    try:
        for monitor in get_monitors():
            if monitor.is_primary:
                self.screen_width = monitor.width
                self.screen_height = monitor.height
                self.screen_width_cut = int(round(self.screen_width * 0.75))
                self.screen_height_cut = int(round(self.screen_height * 0.75))
                self.ui.resize(self.screen_width_cut, self.screen_height_cut)
                self.ui.move(int((self.screen_width - self.ui.size().width()) / 2),
                             int((self.screen_height - self.ui.size().height()) / 2))
                self.logger.debug(
                    f"Prepare_Window : Resize to {self.screen_width_cut} x {self.screen_height_cut} : Original {self.screen_width} x {self.screen_height}")
                break
    except Exception as e:
        self.logger.error(f"Prepare_Window : Cannot Set window size : {e}")

    # Make grips invisible
    [self.cornerGrips[i].setStyleSheet(r"background-color: transparent;") for i in range(4)]
    self.logger.debug(f"Prepare_Window : grips invisible")

    self.logger.debug(f"Prepare_Window : Window Prepared")
