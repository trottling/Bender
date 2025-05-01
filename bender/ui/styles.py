from loguru import logger
from bender.ui.tools import get_rel_path, get_windows_theme


def load_styles(self):
    current_theme = self.ui.qss_comboBox.currentText()
    if current_theme == "" or current_theme is None:
        self.logger.warning("load_styles: Saved theme is empty")
        current_theme = get_windows_theme()
    if current_theme == "Light":
        qss_path = get_rel_path(self, "assets/qss/MaterialLight.qss")
        self.ui.setStyleSheet(open(qss_path, mode="r").read())
        logger.info("load_styles: Light theme applied")
    elif current_theme == "Dark":
        qss_path = get_rel_path(self, "assets/qss/MaterialDark.qss")
        self.ui.setStyleSheet(open(qss_path, mode="r").read())
        logger.info("load_styles: Dark theme applied")
