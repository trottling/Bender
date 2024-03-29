import os
import sys

import darkdetect
import httpx


def GetWindowsTheme(self) -> str:
    if darkdetect.isDark():
        self.logger.debug("GetWindowsTheme : Dark mode is enabled")
        return "Dark"
    else:
        self.logger.debug("GetWindowsTheme : Dark mode is disabled")
        return "Light"


def Report_Error(self, error):
    self.ui.stackedWidget.setCurrentIndex(4)
    self.ui.errors_log.appendPlainText(str(error) + "\n")
    self.logger.error(f"Report_Error : {str(error)}")


def Check_Vulners_Key_Request(self):
    try:
        resp = httpx.post(url=f"https://vulners.com/api/v3/apiKey/valid/?keyID={self.ui.api_key.text().strip()}")
        if resp.status_code != 200:
            self.logger.debug(f"Check_Vulners_Key_Req : resp.status_code {resp.status_code}")
            return False
        if resp.json()['data']['valid']:
            self.logger.debug(f"Check_Vulners_Key_Req : key valid")
            return True
        else:
            self.logger.debug(f"Check_Vulners_Key_Req : key invalid : {resp.json()}")
            return False
    except Exception as e:
        self.logger.error(f"Check_Vulners_Key_Req : {e}")
        return False


def GetRelPath(self, data_path, slash_replace=True):
    if getattr(sys, 'frozen', False):

        try:
            base_path = sys._MEIPASS
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"GetRelPath : {e}")
            return ""

    else:
        data_path = f"..\\{data_path}"
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Instead of several calls to get the relative path of one element,
    # a single call will be made and the result
    # will be saved in dict for later use
    #
    # Only for User_UI class

    if hasattr(self, 'rel_path_dict') and data_path in self.rel_path_dict:
        result = self.rel_path_dict[data_path]
        self.logger.debug(f"GetRelPath : ext : {result}")
        return result

    result = os.path.join(base_path, data_path)

    if slash_replace:
        result = result.replace("\\", "/")

    if hasattr(self, 'rel_path_dict'):
        self.rel_path_dict[data_path] = result

    if hasattr(self, 'logger'):
        self.logger.debug(f"GetRelPath : new : {result}")

    return str(result)
