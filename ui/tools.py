import json
import os
import sys
import webbrowser

import darkdetect
import ctypes
import platform

import threading

import httpx
from PyQt6.QtWidgets import QDialog, QPushButton, QMessageBox


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
    self.ui.errors_log.appendPlainText(str(error) + "\n")
    self.logger.error(f"Report_Error : {str(error)}")


def Save_Settings(self):
    CheckConfigFile(self)
    try:

        self.config.set('main', "app_theme", self.ui.qss_comboBox.currentText())
        self.config.set('main', "cve_db", self.ui.db_comboBox.currentText())
        self.config.set('main', "vulners_api_key", self.ui.api_key.text().strip())
        self.config.set('main', "net_workers", str(self.ui.horizontalSlider_network_threads.value()))
        self.config.set('main', "data_workers", str(self.ui.horizontalSlider_data_threads.value()))

        with open(self.config_path, 'w') as f:
            self.config.write(f)
            self.logger.debug("Save_Settings : Settings saved")
    except Exception as e:
        self.logger.error(f"Save_Settings : {e}")


def Load_Settings(self):
    if CheckConfigFile(self):
        try:
            self.config.read(self.config_path)

            self.logger.debug(f"Load_Settings : app_theme : {self.config.get('main', "app_theme")}")
            self.app_theme = self.config.get('main', "app_theme")

            self.logger.debug(f"Load_Settings : cve_db : {self.config.get('main', "cve_db")}")
            if self.config.get("main", "cve_db") not in (None, ""):
                self.ui.db_comboBox.setCurrentText(self.config.get("main", "cve_db"))

            self.logger.debug(f"Load_Settings : net_workers : {self.config.get('main', "net_workers")}")
            if self.config.get("main", "net_workers") not in (None, ""):
                self.ui.horizontalSlider_network_threads.setValue(int(self.config.get("main", "net_workers")))
                self.ui.label_network_threads_value.setText(self.config.get("main", "net_workers"))

            self.logger.debug(f"Load_Settings : data_workers : {self.config.get('main', "data_workers")}")
            if self.config.get("main", "data_workers") not in (None, ""):
                self.ui.horizontalSlider_data_threads.setValue(int(self.config.get("main", "data_workers")))
                self.ui.label_data_threads_value.setText(self.config.get("main", "data_workers"))

            if self.config.get("main", "vulners_api_key") not in (None, ""):
                self.logger.debug(f"Load_Settings : vulners_api_key : * IS NOT EMPTY *")
                self.ui.api_key.setText(str(self.config.get('main', "vulners_api_key")))
                if Check_Vulners_Key_Request(self):
                    self.ui.vulners_check_result.setStyleSheet(
                        r".QFrame {image: url('" + str(GetRelPath(self, 'assets//images//apply.png')) + "')}")
            self.logger.debug("Load_Settings : Settings loaded")

        except Exception as e:
            self.logger.error(f"Load_Settings : {e}")
    else:
        open(self.config_path, "w").close()
        self.logger.debug("Load_Settings : config empty")


def CheckConfigFile(self):
    if not os.path.isfile(self.config_path) or open(self.config_path, "r").read() == "" or open(self.config_path,
                                                                                                "r").read() is None:
        open(self.config_path, "w").close()
        self.logger.debug(f"CheckConfigFile : {self.config_path} : config created")
        self.config.read(self.config_path)
        if not self.config.has_section('main'):
            self.config.add_section('main')
        self.logger.debug(f"CheckConfigFile : main : add section")
        return False
    else:
        self.logger.debug(f"CheckConfigFile :  {self.config_path} : config exist")
        return True


def Check_Vulners_Key_Request(self):
    try:
        resp = httpx.post(url=f"https://vulners.com/api/v3/apiKey/valid/?keyID={self.ui.api_key.text().strip()}")
        if resp.status_code != 200:
            self.logger.debug(f"Check_Vulners_Key_Req : resp.status_code {resp.status_code}")
            return False
        if resp.json()['data']['valid']:
            self.logger.debug(f"Check_Vulners_Key_Req : key valid")
            self.isVulnersKeyValid = True
            return True
        else:
            self.logger.debug(f"Check_Vulners_Key_Req : key invalid : {resp.json()}")
            self.isVulnersKeyValid = False
            return False
    except Exception as e:
        self.logger.error(f"Check_Vulners_Key_Req : {e}")
        return False


def GetRelPath(self, data_path, slash_replace=True):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        data_path = f"..\\{data_path}"
        base_path = os.path.dirname(os.path.abspath(__file__))

    result = os.path.join(base_path, data_path)

    if slash_replace:
        result = result.replace("\\", "/")

    self.logger.debug(f"GetRelPath : {result}")

    return result


def ClearResult(self):
    if self.result_list_model is not None:
        self.result_list_model.removeRows(0, self.result_list_model.rowCount())

    self.ui.work_log.setPlainText("")
    self.ui.progressBar.setValue(0)
    self.ui.plainTextEdit_vuln.clear()
    self.ui.plainTextEdit_references.clear()
    self.ui.plainTextEdit_cvss_3.clear()
    self.ui.next_work_button.hide()
    self.ui.label_no_cve.hide()

    self.logger.debug(f"ClearResult : Cleared")


def CheckUpdate(self):
    thread = UPD_Thread(self.logger, self.app_version)
    thread.start()
    self.logger.debug(f"CheckUpdate : thread start")
    thread.join()
    self.logger.debug(f"CheckUpdate : thread finish")

    if thread.isErr:
        return

    res = thread.upd_res

    button = QMessageBox.question(self, "Update aviable",
                                  f"{res["version"]}\n\n{res["changelog"]}\n\nOpen new version download page?")
    if button == QMessageBox.StandardButton.Yes:
        webbrowser.open("https://github.com/trottling/Bender/releases/latest")


class UPD_Thread(threading.Thread):
    def __init__(self, logger, app_version) -> None:
        super().__init__()
        self.logger = logger
        self.app_version = app_version
        self.isErr = False
        self.upd_res = {}

    def run(self):
        resp = None
        try:
            resp = httpx.get("https://api.github.com/repos/trottling/Bender/releases/latest", timeout=10)
        except Exception as e:
            self.logger.error(f"GitUpdateReq : request error : {e}")
            self.isErr = True
            return

        if resp.status_code != 200:
            self.logger.error(f"GitUpdateReq : Status code : {resp.status_code}")
            self.isErr = True
            return

        try:
            data = resp.json()
            result = {
                "version": "",
                "changelog": "",
            }
            if data["tag_name"] != self.app_version:
                result["version"] = data["tag_name"]
                result["changelog"] = data["body"]
                self.upd_res = result
                return
            else:
                self.isErr = True

        except Exception as e:
            self.logger.error(f"GitUpdateReq : parse error : {e}")
            self.isErr = True
