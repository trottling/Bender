import ctypes
import platform
import sys
import webbrowser

import httpx
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox
from loguru import logger

from ui.animations import image_change_anim, show_err_message, text_change_anim


class CheckTask(QThread):
    finished = pyqtSignal(int, list)
    def __init__(self, func, text, idx, total, parent=None):
        super().__init__(parent)
        self.func = func
        self.text = text
        self.idx = idx
        self.total = total
    def run(self):
        result = self.func()
        self.finished.emit(self.idx, result)


def run_start_tasks(self):
    self.start_tasks_running = True
    self.vulners_key = self.ui.api_key.text().strip()
    checks = [
        ("Checking for updates...", lambda: check_update(self)),
        ("Getting system info...", lambda: get_system_info(self)),
        ("Checking admin rights...", lambda: check_is_user_admin(self)),
        ("Checking network...", lambda: get_network(self)),
        ("Checking Vulners API...", lambda: check_vulners(self)),
        ("Checking Vulners key...", lambda: check_vulners_key(self)),
        ("Checking LoLDrivers DB...", lambda: check_loldrivers(self)),
    ]
    total = len(checks)
    self._start_threads = []
    self._start_tasks_finished = 0

    def on_check_finished(check_idx, result):
        self._start_tasks_finished += 1
        check_text, _ = checks[check_idx - 1]
        if result is not None:
            if not isinstance(result, list):
                result = [result]
            for action in result:
                try:
                    if isinstance(action, list) and len(action) > 0 and callable(action[0]):
                        action[0](*[arg for arg in action[1:]])
                    else:
                        logger.error(f"run_start_tasks: action is not a valid callable list: {action}")
                except Exception as e:
                    logger.error(f"run_start_tasks: {e}")
        if self._start_tasks_finished == total:
            self.start_tasks_running = False

    for idx, (check_text, func) in enumerate(checks, 1):
        thread = CheckTask(func, check_text, idx, total)
        thread.finished.connect(on_check_finished)
        self._start_threads.append(thread)
        thread.start()


def check_update(self):
    result = [[self.ui.image_version.clear]]
    try:
        self.resp = httpx.get("https://api.github.com/repos/trottling/Bender/releases/latest", timeout=10)
    except Exception as e:
        logger.error(f"CheckUpdate : request error : {e}")
        result.append([image_change_anim, self, self.ui.image_version, r"assets\images\fail.png"])
        return result

    if self.resp.status_code != 200:
        logger.error(f"CheckUpdate : Status code : {self.resp.status_code}")
        result.append([image_change_anim, self, self.ui.image_version, r"assets\images\fail.png"])
        return result

    try:
        data = self.resp.json()
        if data["tag_name"] != self.app_version:
            result.append([image_change_anim, self, self.ui.image_version, r"assets\images\warn.png"])
            if not self.update_msg_show:
                result.append([ask_update, self, f"{data["tag_name"]}\n\n{data["body"]}\n\nOpen new version download page?"])
                self.update_msg_show = True
        else:
            result.append([image_change_anim, self, self.ui.image_version, r"assets\images\apply.png"])

        return result

    except Exception as e:
        logger.error(f"CheckUpdate : parse error : {e}")
        result.append([image_change_anim, self, self.ui.image_version, r"assets\images\fail.png"])
        return result


def ask_update(self, text):
    if QMessageBox.question(self, "Update available", text) == QMessageBox.StandardButton.Yes:
        webbrowser.open("https://github.com/trottling/Bender/releases/latest")


def get_system_info(self):
    # OS name, OS release, OS version, OS support
    try:
        result = [[text_change_anim, self, self.ui.label_os_name_2, f"{platform.system()} {platform.release()}"],
                  [text_change_anim, self, self.ui.label_os_ver_2, platform.version()],
                  [self.ui.image_os_name.clear],
                  [self.ui.image_os_ver.clear]]

        self.validate_platform_release = platform.release()
        self.validate_platform_name = platform.system()
        self.win_icon_start = ""

        match self.validate_platform_release:
            case '11':
                self.win_icon_start = r"assets\images\win-11-small.png"
                self.os_sup_status = "Support"
                result.append([image_change_anim, self, self.ui.image_os_status, r"assets\images\apply.png"])

            case '10':
                self.win_icon_start = r"assets\images\win-10-small.png"
                self.os_sup_status = "Support"
                result.append([image_change_anim, self, self.ui.image_os_status, r"assets\images\apply.png"])

            case '8' | '8.1':
                self.win_icon_start = r"assets\images\win-8-small.png"
                self.os_sup_status = "Unknown"
                result.append([image_change_anim, self, self.ui.image_os_status, r"assets\images\warn.png"])

            case _:
                self.win_icon_start = r"assets\images\help.png"
                self.os_sup_status = "Unknown"
                result.append([image_change_anim, self, self.ui.image_os_status, r"assets\images\warn.png"])

        self.validate_os_sup_status = True
        if platform.system() != "Windows":
            self.validate_os_sup_status = False

        if sys.platform != "win32" or not platform.release().isdigit() or int(platform.release()) < 8:
            self.validate_os_sup_status = False

        result.append([image_change_anim, self, self.ui.image_os_name, self.win_icon_start])
        result.append([image_change_anim, self, self.ui.image_os_ver, r"assets\images\cpu.png"])
        result.append([text_change_anim, self, self.ui.label_os_status_2, self.os_sup_status])

        return result
    except Exception as e:
        logger.error(f"GetSystemInfo : {e}")
        return None


def check_is_user_admin(self):
    result = []
    try:
        self.validate_user_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        logger.error(f"IsUserAdmin() : Admin check failed, assuming not an admin. : {e}")
        self.validate_user_admin = True

    result.append([self.ui.image_as_admin.clear])

    if self.validate_user_admin:
        result.append([image_change_anim, self, self.ui.image_as_admin, r"assets\images\admin.png"])
        result.append([text_change_anim, self, self.ui.label_admin_result, "True"])
    else:
        result.append([image_change_anim, self, self.ui.image_as_admin, r"assets\images\fail.png"])
        result.append([text_change_anim, self, self.ui.label_admin_result, "False"])

    return result


def get_network(self):
    result = []
    try:
        _ = httpx.get("https://www.google.com/", timeout=10)
        self.validate_net_status = True
    except Exception as e:
        logger.error(f"GetNetwork : {e}")
        self.validate_net_status = False

    result.append([self.ui.image_net_status.clear])

    if self.validate_net_status:
        result.append([image_change_anim, self, self.ui.image_net_status, r"assets\images\network.png"])
        result.append([text_change_anim, self, self.ui.label_net_status_2, "Connected"])
    else:
        result.append([image_change_anim, self, self.ui.image_net_status, r"assets\images\fail.png"])
        result.append([text_change_anim, self, self.ui.label_net_status_2, "Disconnected"])

    return result


def check_vulners(self):
    result = []
    try:
        _ = httpx.get("https://vulners.com/", timeout=10)
        self.validate_vulners_status = True
    except Exception as e:
        logger.error(f"CheckVulners : {e}")
        self.validate_vulners_status = False

    result.append([self.ui.image_vulners_api.clear])

    if self.validate_vulners_status:
        result.append([image_change_anim, self, self.ui.image_vulners_api, r"assets\images\server.png"])
        result.append([text_change_anim, self, self.ui.label_vulners_api_2, "Available"])
    else:
        result.append([image_change_anim, self, self.ui.image_vulners_api, r"assets\images\fail.png"])
        result.append([text_change_anim, self, self.ui.label_vulners_api_2, "Unavailable"])

    return result


def check_vulners_key(self):
    result = [[self.ui.image_vulners_key_check.clear]]

    if self.vulners_key in ("", None):
        result.append([image_change_anim, self, self.ui.image_vulners_key_check, r"assets\images\fail.png"])
        result.append([text_change_anim, self, self.ui.label_vulners_key_3, "Key empty"])
        result.append([show_err_message, self, "Enter your Vulners.com key in setting and validate it. <a href='https://github.com/trottling/Bender/blob/main/VULNERS-API-KEY-HELP.md'>Click for help</a>"])
        return result

    # Skip key check if key already validates in setting in one session time
    if not self.validate_vulners_key:
        try:
            resp = httpx.post(url=f"https://vulners.com/api/v3/apiKey/valid/?keyID={self.vulners_key}")
            if resp.status_code != 200:
                logger.debug(f"CheckVulnersKey : resp.status_code {resp.status_code}")
                self.validate_vulners_key = False
                result.append([text_change_anim, self, self.ui.label_vulners_key_3, "Error"])
                result.append([image_change_anim, self, self.ui.image_vulners_key_check, r"assets\images\fail.png"])

            if resp.json()['data']['valid']:
                logger.debug(f"CheckVulnersKey : key valid")
                self.validate_vulners_key = True
                result.append([text_change_anim, self, self.ui.label_vulners_key_3, "Valid"])
                result.append([image_change_anim, self, self.ui.image_vulners_key_check, r"assets\images\key.png"])
                result.append([image_change_anim, self, self.ui.vulners_check_result, r"assets\images\apply.png"])

            else:
                logger.debug(f"CheckVulnersKey : key invalid : {resp.json()}")
                self.validate_vulners_key = False
                result.append([text_change_anim, self, self.ui.label_vulners_key_3, "Invalid"])
                result.append([image_change_anim, self, self.ui.image_vulners_key_check, r"assets\images\fail.png"])
                result.append([image_change_anim, self, self.ui.vulners_check_result, r"assets\images\fail.png"])

        except Exception as e:
            logger.error(f"CheckVulnersKey : {e}")
            self.validate_vulners_key = False
            result.append([text_change_anim, self, self.ui.label_vulners_key_3, "Error"])
            result.append([image_change_anim, self, self.ui.image_vulners_key_check, r"assets\images\fail.png"])

    else:
        logger.debug(f"CheckVulnersKey : key valid : checked in settings")
        self.validate_vulners_key = True
        result.append([text_change_anim, self, self.ui.label_vulners_key_3, "Key valid"])
        result.append([image_change_anim, self, self.ui.image_vulners_key_check, r"assets\images\key.png"])

    return result


def check_loldrivers(self):
    result = []
    try:
        _ = httpx.get("https://www.loldrivers.io/api/", timeout=10)
        self.validate_loldrivers_status = True
    except Exception as e:
        logger.error(f"CheckLoldrivers : {e}")
        self.validate_loldrivers_status = False

    result.append([self.ui.image_loldrivers.clear])

    if self.validate_loldrivers_status:
        result.append([image_change_anim, self, self.ui.image_loldrivers, r"assets\images\db.png"])
        result.append([text_change_anim, self, self.ui.label_loldrivers_2, "Available"])
    else:
        result.append([image_change_anim, self, self.ui.image_loldrivers, r"assets\images\fail.png"])
        result.append([text_change_anim, self, self.ui.label_loldrivers_2, "Unavailable"])

    return result

