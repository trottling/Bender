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

    # Calculate alignment
    desc = ""
    str_max = 126
    cve_max = max(len(item["cve"]) for item in self.report["cve_list"])
    score_max = max(len(str(item['score'])) for item in self.report["cve_list"])
    package_max = max(len(item["package"]) for item in self.report["cve_list"])
    version_max = max(len(item["version"]) for item in self.report["cve_list"])

    # Header alignment
    header = f"{'CVE':<{cve_max}}\t{'Score':<{score_max}}\t{'App':<{package_max}}\t{'Version':<{version_max}}\tDesc"
    self.ui.label_result_info.setText(header)

    # Items alignment
    for item in self.report["cve_list"]:
        string = f"{item['cve']:<{cve_max}}\t{str(item['score']):<{score_max}}\t{item['package']:<{package_max}}\t{item['version']:<{version_max}}"

        if len(string + item["desc"]) > str_max:
            desc = f"{item['desc'][:120 - len(string)]}..."
        else:
            desc = item["desc"]

        self.result_list_model.appendRow(QtGui.QStandardItem(f"{string}\t{desc}"))

    self.logger.debug("Show_Report : List maked")
