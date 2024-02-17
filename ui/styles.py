from ui.tools import GetWindowsTheme
from os import listdir
from os.path import isfile, join


def Load_Styles(self):
    theme = GetWindowsTheme(self)
    user_themes_path = f"{self.appdir}\\saved_qss\\"

    if theme == "Light":
        self.ui.qss_comboBox.setCurrentText("Default (Light)")
    else:
        self.ui.qss_comboBox.setCurrentText("Default (Dark)")

    self.ui.setStyleSheet(open(file=f"assets\\qss\\Material{theme}.qss", mode="r").read())
    self.logger.debug(f"Load_Styles : assets\\qss\\Material{theme} : Default Styles loaded")

    for theme in [f for f in listdir(user_themes_path) if isfile(join(user_themes_path, f))]:
        self.ui.qss_comboBox.addItem(theme)
        self.logger.debug(f"Load_Styles : qss_comboBox : loaded {theme}")

    self.logger.debug(f"Load_Styles : assets\\qss\\Material{theme} : User Styles loaded")
