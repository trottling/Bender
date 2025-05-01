import os.path
from os import listdir
from os.path import isfile, join

from ui.tools import get_windows_theme, get_rel_path


def load_styles(self):
    self.splash.change_pbar(95, "Loading styles")
    self.user_themes_path = f"{self.appdir}\\saved_qss\\"
    self.default_theme = get_windows_theme(self)
    self.theme_to_load = None
    self.ui.qss_comboBox.clear()
    self.ui.qss_comboBox.addItem("Default (Light)")
    self.ui.qss_comboBox.addItem("Default (Dark)")
    for theme in [f for f in listdir(self.user_themes_path) if isfile(join(self.user_themes_path, f))]:
        self.ui.qss_comboBox.addItem(theme)
        self.logger.debug(f"load_styles : qss_comboBox : added {theme}")
        self.logger.debug(f"load_styles : {self.appdir}\\saved_qss\\{theme} : User saved styles loaded")
    if self.app_theme in (None, "", "Default (Dark)", "Default (Light)"):
        match self.app_theme:
            case "Default (Light)":
                self.theme_to_load = "Light"
                self.ui.qss_comboBox.setCurrentText("Default (Light)")
            case "Default (Dark)":
                self.theme_to_load = "Dark"
                self.ui.qss_comboBox.setCurrentText("Default (Dark)")
            case "" | None:
                self.theme_to_load = self.default_theme
        self.logger.debug(f"load_styles : Loading default theme : {self.app_theme} --> {self.theme_to_load}")
        self.ui.setStyleSheet(open(file=get_rel_path(self, f"assets\\qss\\Material{self.theme_to_load}.qss"), mode="r").read())
        self.logger.debug(f"load_styles : assets\\qss\\Material{self.theme_to_load} : Default Styles loaded")
    else:
        if os.path.isfile(f"{self.appdir}\\saved_qss\\{self.app_theme}"):
            self.logger.debug(f"load_styles : Loading User theme : {self.app_theme}")
            try:
                self.ui.setStyleSheet(open(file=get_rel_path(self, f"{self.appdir}\\saved_qss\\{self.app_theme}"), mode="r").read())
                self.ui.qss_comboBox.setCurrentText(self.app_theme)
                self.logger.debug(f"load_styles : {self.app_theme} : User theme loaded")
            except Exception as e:
                self.logger.error(f"load_styles : {self.app_theme} : {e}")
        else:
            self.logger.error(f"load_styles : User theme not found: {self.app_theme}")
            if self.default_theme == "Light":
                self.ui.qss_comboBox.setCurrentText("Default (Light)")
            else:
                self.ui.qss_comboBox.setCurrentText("Default (Dark)")
            self.ui.setStyleSheet(open(file=get_rel_path(self, f"assets\\qss\\Material{self.theme_to_load}.qss"), mode="r").read())
            self.logger.debug(f"load_styles : assets\\qss\\Material{self.theme_to_load} : Default Styles loaded")
