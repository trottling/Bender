import sys

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
    if sys.platform != "win32" or not platform.release().isdigit() or int(platform.release()) < 7:
        Report_Error(self, f"Unsupported operating system : {platform.system()} {platform.release()}")

    if not IsUserAdmin(self):
        Report_Error(self, "App run without Admin privileges")


def IsUserAdmin(self):
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        Report_Error(self, f"Admin check failed, assuming not an Admin : {e}\n")
        return False


def Report_Error(self, error):
    self.ui.stackedWidget.setCurrentIndex(4)
    self.logger.debug("CheckUserOs : self.stackedWidget.setCurrentIndex(0)")
    self.ui.errors_log.appendPlainText(str(error) + "\n")
    self.logger.error(f"Report_Error : {str(error)}")
