import os
import sys

import darkdetect
import httpx
#
# !!! Required by QT Designer WebView widget !!!
# from PyQt6 import QtWebEngineWidgets
#
# noinspection PyUnresolvedReferences
from PyQt6 import QtWebEngineWidgets
from PyQt6 import uic, QtGui
from PyQt6.QtCore import Qt, QUrl
from screeninfo import get_monitors

from ui.animations import UpdateWorkPageStat
from ui.tools import GetRelPath


def Prepare_Window(self):
    # Set env flag for QTWEBENGINE
    if darkdetect.isDark():
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--blink-settings=darkMode=4,darkModeImagePolicy=2"
    self.logger.debug(f"Prepare_Window : env flag seted")
    ui_path = GetRelPath(self, "assets/app.ui")

    self.splash.ChangePbar(10, "Loading UI")

    # Load UI file
    self.logger.debug(f"Prepare_Window : Loading UI : {ui_path}")
    self.logger.debug(f"Prepare_Window : NOTE : If ui not loaded in long time, check 'from PyQt6 import QtWebEngineWidgets' import")
    self.ui = uic.loadUi(ui_path, self)
    self.logger.debug(f"Prepare_Window : UI loaded")

    self.splash.ChangePbar(20, "Installing icons")

    # Icon
    self.ui.setWindowIcon(QtGui.QIcon(GetRelPath(self, "assets//icons//bender.ico.ui")))
    self.logger.debug(f"Prepare_Window : Icon seted")

    self.splash.ChangePbar(30, "Setting descriptions")

    # Title
    self.ui.setWindowTitle("Windows Vulnerability Scanner")
    self.logger.debug(f"Prepare_Window : Title seted")

    # Set version
    self.ui.app_ver.setText(f'<html><head/><body><p align="right"><a href="https://github.com/trottling/Bender/releases/latest"><span style=" text-decoration: underline; color:#a9b7c6;">ver {self.app_version}</span></a></p></body></html>')
    self.ui.python_version.setText(f"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\">Python {sys.version}</span></p></body></html>")
    self.logger.debug(f"Prepare_Window : Versions seted")

    self.splash.ChangePbar(40, "Preparing the window")

    # Window settings
    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    # Set geometry 3/4 primary screen size and move to primary screen center
    try:

        monitors_list = [monitor for monitor in get_monitors()]
        primary_monitor = [monitor for monitor in monitors_list if monitor.is_primary]
        monitor = primary_monitor[0] if len(primary_monitor) >= 1 else monitors_list[0]

        self.screen_width = monitor.width
        self.screen_height = monitor.height
        w_cut = int(round(self.screen_width * 0.75))
        h_cut = int(round(self.screen_height * 0.75))
        self.screen_width_cut = w_cut if w_cut > 1200 else 1200
        self.screen_height_cut = h_cut if h_cut > 650 else 650
        self.ui.resize(self.screen_width_cut, self.screen_height_cut)
        self.ui.move(int((self.screen_width - self.ui.size().width()) / 2), int((self.screen_height - self.ui.size().height()) / 2))
        self.logger.debug(f"Prepare_Window : Resized to {self.screen_width_cut} x {self.screen_height_cut} : Original {self.screen_width} x {self.screen_height}")

    except Exception as e:
        self.logger.error(f"Prepare_Window : Cannot Set window size : {e}")

    # Make grips invisible
    [self.cornerGrips[i].setStyleSheet(r"background-color: transparent;") for i in range(4)]
    self.logger.debug(f"Prepare_Window : grips invisible")

    # Create start check elems lists
    self.start_processing_elems = [self.ui.image_os_name, self.ui.image_os_ver, self.ui.image_os_status,
                                   self.ui.image_as_admin, self.ui.image_net_status, self.ui.image_vulners_api,
                                   self.ui.image_vulners_key_check, self.ui.image_loldrivers, self.ui.image_version]

    self.start_processing_labels = [self.ui.label_os_name_2, self.ui.label_os_ver_2, self.ui.label_os_status_2,
                                    self.ui.label_admin_result, self.ui.label_net_status_2, self.ui.label_vulners_api_2,
                                    self.ui.label_vulners_key_3, self.ui.label_loldrivers_2]

    self.splash.ChangePbar(50, "Loading Shodan info")

    try:
        ip = httpx.get(url="https://api.ipify.org", timeout=5).content.decode('utf8')
        self.ui.WebWidget.load(QUrl(f"https://www.shodan.io/host/{ip}"))
        self.logger.debug("LoadShodanReport : loaded")
        UpdateWorkPageStat(self, "good")
    except Exception as e:
        self.logger.error(f"LoadShodanReport : {e}")
        UpdateWorkPageStat(self, "bad")

    self.logger.debug(f"Prepare_Window : Window Prepared")
