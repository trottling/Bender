import os
import sys
import darkdetect
import httpx
from loguru import logger
#
# !!! Required by QT Designer WebView widget !!!
# from PyQt6 import QtWebEngineWidgets
#
# noinspection PyUnresolvedReferences
from PyQt6 import QtWebEngineWidgets
from PyQt6 import uic, QtGui
from PyQt6.QtCore import Qt, QUrl
from screeninfo import get_monitors

from bender.ui.animations import update_work_page_stat
from bender.ui.tools import get_rel_path


def prepare_window(self):
    # Set environment flag for QTWEBENGINE
    if darkdetect.isDark():
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--blink-settings=darkMode=4,darkModeImagePolicy=2"
    logger.debug("prepare_window: env flag set")
    ui_path = get_rel_path(self, "assets/ui/app.ui")

    # Load ui file
    logger.debug(f"prepare_window: Loading ui: {ui_path}")
    logger.debug("prepare_window: NOTE: If ui not loaded in long time, check 'from PyQt6 import QtWebEngineWidgets' import")
    self.ui = uic.loadUi(ui_path, self)
    logger.debug("prepare_window: ui loaded")

    # Set window icon
    self.ui.setWindowIcon(QtGui.QIcon(get_rel_path(self, "assets//icons//bender.ico")))
    logger.debug("prepare_window: Icon set")

    # Set window title
    self.ui.setWindowTitle("Windows Vulnerability Scanner")
    logger.debug("prepare_window: Title set")

    # Set version
    self.ui.app_ver.setText(f'<html><head/><body><p align="right"><a href="https://github.com/trottling/Bender/releases/tag/{self.app_version}"><span style=" text-decoration: underline; color:#a9b7c6;">ver {self.app_version}</span></a></p></body></html>')
    self.ui.python_version.setText(f"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt;\">Python {sys.version}</span></p></body></html>")
    logger.debug("prepare_window: Versions set")

    # Set window flags
    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    # Set geometry to 3/4 of primary screen size and center
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
        logger.debug(f"prepare_window: Resized to {self.screen_width_cut} x {self.screen_height_cut} (Original {self.screen_width} x {self.screen_height})")
    except Exception as e:
        logger.error(f"prepare_window: Cannot set window size: {e}")

    # Make grips invisible
    [self.corner_grips[i].setStyleSheet(r"background-color: transparent;") for i in range(4)]
    logger.debug("prepare_window: Grips set to transparent")

    # Create start check elements lists
    self.start_processing_elems = [self.ui.image_os_name, self.ui.image_os_ver, self.ui.image_os_status,
                                   self.ui.image_as_admin, self.ui.image_net_status, self.ui.image_vulners_api,
                                   self.ui.image_vulners_key_check, self.ui.image_loldrivers, self.ui.image_version]

    self.start_processing_labels = [self.ui.label_os_name_2, self.ui.label_os_ver_2, self.ui.label_os_status_2,
                                    self.ui.label_admin_result, self.ui.label_net_status_2, self.ui.label_vulners_api_2,
                                    self.ui.label_vulners_key_3, self.ui.label_loldrivers_2]

    try:
        ip = httpx.get(url="https://api.ipify.org", timeout=5).content.decode('utf8')
        self.ui.WebWidget.load(QUrl(f"https://www.shodan.io/host/{ip}"))
        self.ui.WebWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        logger.debug("prepare_window: Shodan report loaded")
        update_work_page_stat(self, "good")
    except Exception as e:
        logger.error(f"prepare_window: Failed to load Shodan report: {e}")
        update_work_page_stat(self, "bad")

    logger.debug("prepare_window: Window prepared")
