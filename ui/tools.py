from loguru import logger
import os
import sys

import darkdetect
import httpx


def GetWindowsTheme(self) -> str:
    if darkdetect.isDark():
        logger.debug("GetWindowsTheme: Dark mode is enabled")
        return "Dark"
    else:
        logger.debug("GetWindowsTheme: Dark mode is disabled")
        return "Light"


def Report_Error(self, error):
    self.ui.stackedWidget.setCurrentIndex(4)
    self.ui.errors_log.appendPlainText(str(error) + "\n")
    logger.error(f"Report_Error: {str(error)}")


def Check_Vulners_Key_Request(self):
    try:
        resp = httpx.post(url=f"https://vulners.com/api/v3/apiKey/valid/?keyID={self.ui.api_key.text().strip()}")
        if resp.status_code != 200:
            logger.debug(f"Check_Vulners_Key_Request: resp.status_code {resp.status_code}")
            return False
        if resp.json()['data']['valid']:
            logger.debug("Check_Vulners_Key_Request: key valid")
            return True
        else:
            logger.debug(f"Check_Vulners_Key_Request: key invalid: {resp.json()}")
            return False
    except Exception as e:
        logger.error(f"Check_Vulners_Key_Request: {e}")
        return False


def GetRelPath(self, data_path, slash_replace=True):
    if getattr(sys, 'frozen', False):
        try:
            base_path = sys._MEIPASS
        except Exception as e:
            logger.error(f"GetRelPath: {e}")
            return ""
    else:
        data_path = f"..\\{data_path}"
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Use a dict to cache relative paths for User_UI class
    if hasattr(self, 'rel_path_dict') and data_path in self.rel_path_dict:
        result = self.rel_path_dict[data_path]
        logger.debug(f"GetRelPath: cached: {result}")
        return result

    result = os.path.join(base_path, data_path)

    if slash_replace:
        result = result.replace("\\", "/")

    if hasattr(self, 'rel_path_dict'):
        self.rel_path_dict[data_path] = result

    logger.debug(f"GetRelPath: new: {result}")

    return str(result)
