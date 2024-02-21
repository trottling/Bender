from PyQt6 import QtGui
import json

from ui.tools import Report_Error


def Show_Report(self, rep):
    try:
        self.logger.debug("Show_Report : converting to JSON")
        self.report = json.loads(rep)
    except Exception as e:
        Report_Error(self, "Failed to convert Vulners report to JSON format : " + str(e))

    self.ui.next_work_button.show()
    self.logger.debug("Show_Report : next_work_button : show")

    # Setup list
    self.result_list_model = QtGui.QStandardItemModel()
    self.ui.result_listView.setModel(self.result_list_model)

    # Calculate aligment

    ds = ""
    str_max = 126
    cve_max = max(len(item["cve"]) for item in self.report["cve_list"])
    score_max = max(len(str(item['score'])) for item in self.report["cve_list"])
    package_max = max(len(item["package"]) for item in self.report["cve_list"])
    version_max = max(len(item["version"]) for item in self.report["cve_list"])
    self.ui.label_result_info.setText(
        f"{"CVE".ljust(cve_max)}\t{"Score".ljust(score_max)}\t{"App".ljust(package_max)}\t{"Version".ljust(version_max)}\tDesc")

    for item in self.report["cve_list"]:

        st = f"{item['cve'].ljust(cve_max)}\t{str(item['score']).ljust(score_max)}\t{item['package'].ljust(package_max)}\t{item['version'].ljust(version_max)}"

        if len(st + item["desc"]) > str_max:
            ds = f"{item["desc"][:120 - len(st)]}..."
        else:
            ds = item["desc"]

        self.result_list_model.appendRow(QtGui.QStandardItem(f"{st}\t{ds}"))

    self.logger.debug("Show_Report : List maked")
