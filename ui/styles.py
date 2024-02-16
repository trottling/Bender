from ui.tools import GetWindowsTheme


def Load_Styles(self):
    theme = GetWindowsTheme(self)

    if theme == "Light":
        self.ui.qss_comboBox.setCurrentText("Default (Light)")
    else:
        self.ui.qss_comboBox.setCurrentText("Default (Dark)")

    self.ui.setStyleSheet(open(file=f"assets\\qss\\Material{theme}.qss", mode="r").read())
    self.logger.debug(f"Load_Styles : assets\\qss\\Material{theme} : Styles loaded")
