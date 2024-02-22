import os
import sys

import darkdetect
import ctypes
import platform

import httpx


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

            if self.config.get("main", "vulners_api_key") not in (None, ""):
                self.logger.debug(f"Load_Settings : vulners_api_key : * IS NOT EMPTY *")
                self.ui.api_key.setText(str(self.config.get('main', "vulners_api_key")))
                if Check_Vulners_Key_Request(self):
                    self.ui.vulners_check_result.setStyleSheet(
                        r".QFrame {image: url('assets//images//apply.png')}")
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
