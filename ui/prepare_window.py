import sys

from PyQt6 import uic, QtGui
from PyQt6.QtCore import Qt

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

    self.logger.debug(f"Prepare_Window : Window Prepared")
