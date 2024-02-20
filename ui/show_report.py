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

    print(self.report)
    for item in self.report["cve_list"]:
        self.result_list_model.appendRow(
            QtGui.QStandardItem(f"{item["cve"]}\t{item["package"]}\t{item["version"]}\t{item["version"]}"))
