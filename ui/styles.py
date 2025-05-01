import os.path
from os import listdir
from os.path import isfile, join

from ui.tools import get_windows_theme, get_rel_path


def load_styles(self):
    self.splash.change_pbar(95, "Loading styles")
    current_theme = self.ui.qss_comboBox.currentText()
    if current_theme == "" or current_theme is None:
        current_theme = get_windows_theme()
    if current_theme == "Light":
        qss_path = get_rel_path(self, "assets/qss/MaterialLight.qss")
        self.ui.setStyleSheet(open(qss_path, mode="r").read())
        self.logger.info("load_styles: Light theme applied")
    elif current_theme == "Dark":
        qss_path = get_rel_path(self, "assets/qss/MaterialDark.qss")
        self.ui.setStyleSheet(open(qss_path, mode="r").read())
        self.logger.info("load_styles: Dark theme applied")
