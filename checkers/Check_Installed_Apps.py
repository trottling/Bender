from windows_tools.installed_software import get_installed_software
from ui.tools import Report_Error


def RunCIA(self):
    raw_soft_list = []
    soft_list = []
    self.logger.debug("RunCIA : Started")
    self.ui.stackedWidget.setCurrentIndex(1)
    self.ui.work_log.appendPlainText("Check installed apps started..." + "\n")

    try:
        raw_soft_list = get_installed_software()
    except Exception as e:
        Report_Error(self, e)

    self.logger.debug(f"RunCIA : Raw Soft list : {raw_soft_list}")

    for software in raw_soft_list:
        if software['name'] != "" and software['version'] != "" and software['publisher'] != "":
            soft_list.append(software)

    self.logger.debug(f"RunCIA : Soft list : {soft_list}")

    self.ui.progressBar.setValue(10)

    self.ui.work_log.appendPlainText(f"Found {len(soft_list)} softwares\n")
