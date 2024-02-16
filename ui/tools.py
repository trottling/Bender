import darkdetect
import ctypes
import platform


def GetWindowsTheme(self) -> str:
    if darkdetect.isDark():
        self.logger.debug("GetWindowsTheme : Dark mode is enabled")
        return "Dark"
    else:
        self.logger.debug("GetWindowsTheme : Dark mode is disabled")
        return "Light"


def CheckUserOs(self):
    if platform.system() != "Windows":
        self.logger.debug("Unsupported operating system")
        self.stackedWidget.setCurrentIndex(4)
        self.logger.debug("CheckUserOs : self.stackedWidget.setCurrentIndex(0)")
        self.ui.page_errors.append(f"Unsupported operating system : {platform.system()}\n")
    if not IsUserAdmin(self):
        self.logger.debug("CheckUserOs : self.stackedWidget.setCurrentIndex(0)")
        self.ui.page_errors.append(f"App run without Admin privileges\n")


def IsUserAdmin(self):
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        self.stackedWidget.setCurrentIndex(4)
        self.ui.page_errors.append(f"App run Admin check failed, assuming not an admin : {e}\n")
        self.logger.debug(f"IsUserAdmin() : Admin check failed, assuming not an admin : {e}")
        return False
