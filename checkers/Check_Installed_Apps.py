from vulners import vscanner
from windows_tools.installed_software import get_installed_software
import vulners
import json
from checkers.rep import rep


def RunCIA(self):
    self.raw_soft_list = []
    self.soft_list = []
    self.soft_list_vulners = []
    self.report = None

    self.logger.debug("RunCIA : Started")
    self.log_signal.emit("Check installed apps started..." + "\n")

    try:
        self.raw_soft_list = get_installed_software()
    except Exception as e:
        self.err_signal.emit("Error getting installed apps : " + str(e))
        return

    self.logger.debug(f"RunCIA : Raw Soft list : {len(self.raw_soft_list)} softwares")

    for software in self.raw_soft_list:
        if software['name'] != "" and software['version'] != "":
            self.soft_list.append(software)

    if len(self.soft_list) == 0:
        self.err_signal.emit("ERROR : Could not find any software to check")

    self.logger.debug(f"RunCIA : Soft list : {len(self.soft_list)} softwares")
    self.log_signal.emit(f"Found {len(self.raw_soft_list)} softwares, {len(self.soft_list)} aviable to check\n")

    match self.db:
        case "vulners.com (Recommended)": Check_By_Vulners(self)


def Check_By_Vulners(self):
    if len(self.soft_list) > 500:
        self.soft_list = self.soft_list[:500]
        self.log_signal.emit(f"Software list is too bigger : {len(self.soft_list)} : Cut lenght to 500\n")

    self.log_signal.emit(f"Transforming softwares list to vulners format\n")
    for software in self.soft_list:
        if self.db == "vulners.com (Recommended)":
            self.soft_list_vulners.append(dict({"software": software['name'], "version": software['version']}))
    """
    self.log_signal.emit(f"Connecting to vulners API\n")
    try:
        self.vulners_api = vulners.VulnersApi(api_key=self.api_key)
    except Exception as e:
        self.err_signal.emit("Failed to connect Vulners Api : " + str(e))
        return

    self.log_signal.emit(f"Sending softwares list to vulners\n")
    try:
        self.report = self.vulners_api.software_audit(os="", version="", packages=self.soft_list_vulners)
    except Exception as e:
        self.err_signal.emit("Failed to get Vulners report : " + str(e))
        return
        """
    self.report = rep
    try:
        self.log_signal.emit(
            f"Done : {len(self.report.get("exploit"))} Exploits : {len(self.report.get("software"))} Software vulnerabiliries\n")
    except Exception as e:
        self.err_signal.emit("Failed read Vulners report : " + str(e))
    self.log_signal.emit("Click Next button to see scan results")
    self.result_signal.emit(self.report)
