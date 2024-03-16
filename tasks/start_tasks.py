import concurrent.futures as cf
import ctypes
import platform
import sys
import webbrowser

import httpx
from PyQt6 import QtTest
from PyQt6.QtWidgets import QMessageBox

from ui.animations import ImageChangeAnim, TextChangeAnim, ShowErrMessage
from ui.tools import GetRelPath


def Run_Start_Tasks(self):
    #
    # Run task in other Thread -->
    # Task return list like [[func1, arg1], [func2, arg2]] -->
    # Run funcs with args from list in UI thread
    #

    self.start_tasks_running = True

    # This call will be in UI thread
    self.vulners_key = self.ui.api_key.text().strip()

    self.done_start_tasks_list = []
    self.start_tasks_list = [CheckUpdate, GetSystemInfo, CheckIsUserAdmin, GetNetwork,
                             CheckVulners, CheckVulnersKey, CheckLoldrivers]

    with cf.ThreadPoolExecutor(max_workers=len(self.start_tasks_list)) as self.st_pool:

        [self.done_start_tasks_list.append(self.st_pool.submit(task, self)) for task in self.start_tasks_list]

        # Even though it's a crutch, it fucking really works and takes away the ui freezes
        while all([i.done() is not True for i in self.done_start_tasks_list]):
            QtTest.QTest.qWait(200)

        #
        # First element in list is func, other is args
        # Sleep for more pretty anim
        #

        QtTest.QTest.qWait(500)
        for task in self.done_start_tasks_list:
            if task.result() is not None:
                for func in task.result():
                    try:
                        QtTest.QTest.qWait(25)
                        func[0](*[arg for arg in func[1:] if len(func) > 1])
                    except Exception as e:
                        self.logger.error(f"Run_Start_Tasks : {e}")

    QtTest.QTest.qWait(250)
    self.start_tasks_running = False


def CheckUpdate(self):
    result = [[self.ui.image_version.clear]]
    try:
        self.resp = httpx.get("https://api.github.com/repos/trottling/Bender/releases/latest", timeout=10)
    except Exception as e:
        self.logger.error(f"CheckUpdate : request error : {e}")
        result.append([ImageChangeAnim, self, self.ui.image_version, r"assets\images\fail.png"])
        return result

    if self.resp.status_code != 200:
        self.logger.error(f"CheckUpdate : Status code : {self.resp.status_code}")
        result.append([ImageChangeAnim, self, self.ui.image_version, r"assets\images\fail.png"])
        return result

    try:
        data = self.resp.json()
        if data["tag_name"] != self.app_version:
            result.append([ImageChangeAnim, self, self.ui.image_version, r"assets\images\warn.png"])
            if not self.update_msg_show:
                result.append([AskUpdate, self, f"{data["tag_name"]}\n\n{data["body"]}\n\nOpen new version download page?"])
                self.update_msg_show = True
        else:
            result.append([ImageChangeAnim, self, self.ui.image_version, r"assets\images\apply.png"])

        return result

    except Exception as e:
        self.logger.error(f"CheckUpdate : parse error : {e}")
        result.append([ImageChangeAnim, self, self.ui.image_version, r"assets\images\fail.png"])
        return result


def AskUpdate(self, text):
    msg = QMessageBox(self)
    msg.setWindowTitle("Update aviable")
    msg.setText(text)
    msg.setIcon(GetRelPath(self, "assets/icons/bender.ico"))
    button = msg.question(self)
    if button == QMessageBox.StandardButton.Yes:
        webbrowser.open("https://github.com/trottling/Bender/releases/latest")


def GetSystemInfo(self):
    # OS name, OS release, OS version, OS support
    try:
        result = [[TextChangeAnim, self, self.ui.label_os_name_2, f"{platform.system()} {platform.release()}"],
                  [TextChangeAnim, self, self.ui.label_os_ver_2, platform.version()],
                  [self.ui.image_os_name.clear],
                  [self.ui.image_os_ver.clear]]

        self.validate_platform_release = platform.release()
        self.validate_platform_name = platform.system()
        self.win_icon_start = ""

        match self.validate_platform_release:
            case '11':
                self.win_icon_start = r"assets\images\win-11-small.png"
                self.os_sup_status = "Support"
                result.append([ImageChangeAnim, self, self.ui.image_os_status, r"assets\images\apply.png"])

            case '10':
                self.win_icon_start = r"assets\images\win-10-small.png"
                self.os_sup_status = "Support"
                result.append([ImageChangeAnim, self, self.ui.image_os_status, r"assets\images\apply.png"])

            case '8' | '8.1':
                self.win_icon_start = r"assets\images\win-8-small.png"
                self.os_sup_status = "Unknown"
                result.append([ImageChangeAnim, self, self.ui.image_os_status, r"assets\images\warn.png"])

            case _:
                self.win_icon_start = r"assets\images\help.png"
                self.os_sup_status = "Unknown"
                result.append([ImageChangeAnim, self, self.ui.image_os_status, r"assets\images\warn.png"])

        self.validate_os_sup_status = True
        if platform.system() != "Windows":
            self.validate_os_sup_status = False

        if sys.platform != "win32" or not platform.release().isdigit() or int(platform.release()) < 8:
            self.validate_os_sup_status = False

        result.append([ImageChangeAnim, self, self.ui.image_os_name, self.win_icon_start])
        result.append([ImageChangeAnim, self, self.ui.image_os_ver, r"assets\images\cpu.png"])
        result.append([TextChangeAnim, self, self.ui.label_os_status_2, self.os_sup_status])

        return result
    except Exception as e:
        self.logger.error(f"GetSystemInfo : {e}")


def CheckIsUserAdmin(self):
    result = []
    try:
        self.validate_user_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        self.logger.error(f"IsUserAdmin() : Admin check failed, assuming not an admin. : {e}")
        self.validate_user_admin = True

    result.append([self.ui.image_as_admin.clear])

    if self.validate_user_admin:
        result.append([ImageChangeAnim, self, self.ui.image_as_admin, r"assets\images\admin.png"])
        result.append([TextChangeAnim, self, self.ui.label_admin_result, "True"])
    else:
        result.append([ImageChangeAnim, self, self.ui.image_as_admin, r"assets\images\fail.png"])
        result.append([TextChangeAnim, self, self.ui.label_admin_result, "False"])

    return result


def GetNetwork(self):
    result = []
    try:
        _ = httpx.get("https://www.google.com/", timeout=10)
        self.validate_net_status = True
    except Exception as e:
        self.logger.error(f"GetNetwork : {e}")
        self.validate_net_status = False

    result.append([self.ui.image_net_status.clear])

    if self.validate_net_status:
        result.append([ImageChangeAnim, self, self.ui.image_net_status, r"assets\images\network.png"])
        result.append([TextChangeAnim, self, self.ui.label_net_status_2, "Connected"])
    else:
        result.append([ImageChangeAnim, self, self.ui.image_net_status, r"assets\images\fail.png"])
        result.append([TextChangeAnim, self, self.ui.label_net_status_2, "Disconnected"])

    return result


def CheckVulners(self):
    result = []
    try:
        _ = httpx.get("https://vulners.com/", timeout=10)
        self.validate_vulners_status = True
    except Exception as e:
        self.logger.error(f"CheckVulners : {e}")
        self.validate_vulners_status = False

    result.append([self.ui.image_vulners_api.clear])

    if self.validate_vulners_status:
        result.append([ImageChangeAnim, self, self.ui.image_vulners_api, r"assets\images\server.png"])
        result.append([TextChangeAnim, self, self.ui.label_vulners_api_2, "Aviable"])
    else:
        result.append([ImageChangeAnim, self, self.ui.image_vulners_api, r"assets\images\fail.png"])
        result.append([TextChangeAnim, self, self.ui.label_vulners_api_2, "Unavailable"])

    return result


def CheckVulnersKey(self):
    result = [[self.ui.image_vulners_key_check.clear]]

    if self.vulners_key in ("", None):
        result.append([ImageChangeAnim, self, self.ui.image_vulners_key_check, r"assets\images\fail.png"])
        result.append([TextChangeAnim, self, self.ui.label_vulners_key_3, "Key empty"])
        result.append([ShowErrMessage, self, "Enter your Vulners.com key in setting and validate it. <a href='https://github.com/trottling/Bender/blob/main/VULNERS-API-KEY-HELP.md'>Click for help</a>"])
        return result

    # Skip key check if key already validate in setting in one session time
    if not self.validate_vulners_key:
        try:
            resp = httpx.post(url=f"https://vulners.com/api/v3/apiKey/valid/?keyID={self.vulners_key}")
            if resp.status_code != 200:
                self.logger.debug(f"CheckVulnersKey : resp.status_code {resp.status_code}")
                self.validate_vulners_key = False
                result.append([TextChangeAnim, self, self.ui.label_vulners_key_3, "Error"])
                result.append([ImageChangeAnim, self, self.ui.image_vulners_key_check, r"assets\images\fail.png"])

            if resp.json()['data']['valid']:
                self.logger.debug(f"CheckVulnersKey : key valid")
                self.validate_vulners_key = True
                result.append([TextChangeAnim, self, self.ui.label_vulners_key_3, "Valid"])
                result.append([ImageChangeAnim, self, self.ui.image_vulners_key_check, r"assets\images\key.png"])
                result.append([ImageChangeAnim, self, self.ui.vulners_check_result, r"assets\images\apply.png"])

            else:
                self.logger.debug(f"CheckVulnersKey : key invalid : {resp.json()}")
                self.validate_vulners_key = False
                result.append([TextChangeAnim, self, self.ui.label_vulners_key_3, "Invalid"])
                result.append([ImageChangeAnim, self, self.ui.image_vulners_key_check, r"assets\images\fail.png"])
                result.append([ImageChangeAnim, self, self.ui.vulners_check_result, r"assets\images\fail.png"])

        except Exception as e:
            self.logger.error(f"CheckVulnersKey : {e}")
            self.validate_vulners_key = False
            result.append([TextChangeAnim, self, self.ui.label_vulners_key_3, "Error"])
            result.append([ImageChangeAnim, self, self.ui.image_vulners_key_check, r"assets\images\fail.png"])

    else:
        self.logger.debug(f"CheckVulnersKey : key valid : checked in settings")
        self.validate_vulners_key = True
        result.append([TextChangeAnim, self, self.ui.label_vulners_key_3, "Key valid"])
        result.append([ImageChangeAnim, self, self.ui.image_vulners_key_check, r"assets\images\key.png"])

    return result


def CheckLoldrivers(self):
    result = []
    try:
        _ = httpx.get("https://www.loldrivers.io/api/", timeout=10)
        self.validate_loldrivers_status = True
    except Exception as e:
        self.logger.error(f"CheckLoldrivers : {e}")
        self.validate_loldrivers_status = False

    result.append([self.ui.image_loldrivers.clear])

    if self.validate_loldrivers_status:
        result.append([ImageChangeAnim, self, self.ui.image_loldrivers, r"assets\images\db.png"])
        result.append([TextChangeAnim, self, self.ui.label_loldrivers_2, "Aviable"])
    else:
        result.append([ImageChangeAnim, self, self.ui.image_loldrivers, r"assets\images\fail.png"])
        result.append([TextChangeAnim, self, self.ui.label_loldrivers_2, "Unavailable"])

    return result
