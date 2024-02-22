import json

from PyQt6 import QtGui

from ui.animations import StackedWidgetChangePage, ElemShowAnim
from ui.tools import Report_Error


def Show_Report(self, rep):
    try:
        self.logger.debug("Show_Report : loading report")
        self.report = json.loads(rep)
    except Exception as e:
        Report_Error(self, "Failed to convert Vulners report to JSON format : " + str(e))

    self.ui.next_work_button.show()
    self.logger.debug("Show_Report : next_work_button : show")

    self.logger.debug(f"Show_Report : {len(self.report["cve_list"])} CVEs in list")
    if len(self.report["cve_list"]) == 0:
        ElemShowAnim(self, self.ui.label_no_cve)
        return

    try:
        # Calculate alignment
        str_max = 126
        cve_max = max(len(item["cve"]) for item in self.report["cve_list"]) + 8
        score_max = max(len(str(item['score'])) for item in self.report["cve_list"]) + 8
        package_max = max(len(item["package"]) for item in self.report["cve_list"]) + 8
        version_max = max(len(item["version"]) for item in self.report["cve_list"]) + 8
        self.logger.debug(
            f"Show_Report : cve_max {cve_max} : score_max {score_max} : package_max {package_max} : version_max {version_max}")

        # Header alignment
        header = f"     {'CVE'.ljust(cve_max)}{'Score'.ljust(score_max)}{'App'.ljust(package_max)}{'Version'.ljust(version_max)}Desc"
        self.ui.label_result_info.setText(header)

        # Setup list
        self.result_list_model = QtGui.QStandardItemModel()
        self.ui.result_listView.setModel(self.result_list_model)

        # Items alignment
        for item in self.report["cve_list"]:
            string = f"  {item['cve'].ljust(cve_max)}{str(item['score']).ljust(score_max)}{item['package'].capitalize().ljust(package_max)}{item['version'].ljust(version_max)}"

            if len(string + item["desc"]) > str_max:
                desc = f"{item['desc'][:120 - len(string)]}..."
            else:
                desc = item["desc"]

            list_item = QtGui.QStandardItem()
            list_item.setText(string + desc)
            list_item.setIcon(QtGui.QIcon(r"assets\images\risk.png"))

            self.result_list_model.appendRow(list_item)

        self.ui.result_listView.doubleClicked.connect(lambda index: ShowCVEInfo(self, index))
        self.logger.debug("Show_Report : List maked")
    except Exception as e:
        Report_Error(self, e)


def ShowCVEInfo(self, index):
    try:
        item_index = index.row()
        self.logger.debug(f"ShowCVEInfo : item index {str(item_index).strip()} ")
        cve_info = self.report["cve_list"][item_index]

        self.ui.label_cve_head.setText(
            f"{cve_info["cve"]} - {cve_info["package"].capitalize()} - {cve_info["version"]}")

        self.ui.label_published.setText(
            f"Published: {cve_info["datePublished"]}" if "datePublished" in cve_info and cve_info[
                "datePublished"].strip is not "" else "Published: No date")
        self.ui.cve_desc_plainTextEdit.setPlainText(cve_info["desc"].capitalize())

        self.ui.label_shortname.setText(f"Shortname: {cve_info["shortName"].capitalize()}")

        for ref in cve_info["references"]:
            self.ui.plainTextEdit_references.appendHtml(f"<a href='{ref['url']}'>{ref['url']}</a>")

        if "cvssV3_1" in cve_info["cvss_metrics"]:
            for item in cve_info["cvss_metrics"]["cvssV3_1"]:
                self.ui.plainTextEdit_cvss_3.appendPlainText(f"{item}: {cve_info["cvss_metrics"]["cvssV3_1"][item]}")
        else:
            self.ui.plainTextEdit_cvss_3.appendPlainText("No info")

        StackedWidgetChangePage(self, 5)
    except Exception as e:
        Report_Error(self, e)
