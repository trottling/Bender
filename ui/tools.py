from loguru import logger
import os
import sys

import darkdetect
import httpx


def get_windows_theme(self) -> str:
    if darkdetect.isDark():
        logger.debug("get_windows_theme: Dark mode is enabled")
        return "Dark"
    else:
        logger.debug("get_windows_theme: Dark mode is disabled")
        return "Light"


def report_error(self, error):
    self.ui.stackedWidget.setCurrentIndex(4)
    self.ui.errors_log.appendPlainText(str(error) + "\n")
    logger.error(f"report_error: {str(error)}")


def check_vulners_key_request(self):
    try:
        resp = httpx.post(url=f"https://vulners.com/api/v3/apiKey/valid/?keyID={self.ui.api_key.text().strip()}")
        if resp.status_code != 200:
            logger.debug(f"check_vulners_key_request: resp.status_code {resp.status_code}")
            return False
        if resp.json()['data']['valid']:
            logger.debug("check_vulners_key_request: key valid")
            return True
        else:
            logger.debug(f"check_vulners_key_request: key invalid: {resp.json()}")
            return False
    except Exception as e:
        logger.error(f"check_vulners_key_request: {e}")
        return False


def get_rel_path(self, data_path, slash_replace=True):
    if getattr(sys, 'frozen', False):
        try:
            base_path = sys._MEIPASS
        except Exception as e:
            logger.error(f"get_rel_path: {e}")
            return ""
    else:
        data_path = f"..\\{data_path}"
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Use a dict to cache relative paths for UserUI class
    if hasattr(self, 'rel_path_dict') and data_path in self.rel_path_dict:
        result = self.rel_path_dict[data_path]
        logger.debug(f"get_rel_path: cached: {result}")
        return result

    result = os.path.join(base_path, data_path)

    if slash_replace:
        result = result.replace("\\", "/")

    if hasattr(self, 'rel_path_dict'):
        self.rel_path_dict[data_path] = result

    logger.debug(f"get_rel_path: new: {result}")

    return str(result)
