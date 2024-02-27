import json
import re

from PyQt6 import QtGui

from ui.animations import StackedWidgetChangePage, ElemShowAnim
from ui.tools import Report_Error, GetRelPath


def Show_Report_CIA(self, rep):
    try:
        self.logger.debug("Show_Report_CIA : loading report")
        self.report = json.loads(rep)
    except Exception as e:
        Report_Error(self, "Failed to convert report to JSON format : " + str(e))

    self.ui.next_work_button.show()
    self.logger.debug("Show_Report_CIA : next_work_button : show")

    self.logger.debug(f"Show_Report_CIA : {len(self.report["cve_list"])} CVEs in list")
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
            f"Show_Report_CIA : cve_max {cve_max} : score_max {score_max} : package_max {package_max} : version_max {version_max}")

        # Header alignment
        header = f"     {'CVE'.ljust(cve_max)}{'Score'.ljust(score_max)}{'App'.ljust(package_max)}{'Version'.ljust(version_max)}Desc"
        self.ui.label_result_info.setText(header)

        # Setup list
        self.result_list_model = QtGui.QStandardItemModel()
        self.ui.result_listView.setModel(self.result_list_model)

        # Items alignment
        for item in self.report["cve_list"]:
            string = f"{item['cve'].ljust(cve_max)}{str(item['score']).ljust(score_max)}{item['package'].capitalize().ljust(package_max)}{item['version'].ljust(version_max)}"

            if len(string + item["desc"]) > str_max:
                desc = f"{item['desc'][:120 - len(string)]}..."
            else:
                desc = item["desc"]

            list_item = QtGui.QStandardItem()
            list_item.setText(string + desc)

            dot = ""
            score = item['score']

            if score in ("", "-", None):
                dot = "dot-grey.png"
            else:
                score = float(score)
                if score == 0.0:
                    dot = "dot-grey.png"
                elif 0.0 < score < 4.0:
                    dot = "dot-yellow.png"
                elif 4.0 < score < 7.0:
                    dot = "dot-orange.png"
                elif 7.0 < score < 9.0:
                    dot = "dot-red.png"
                elif score > 9.0:
                    dot = "dot-dark-red.png"
                else:
                    dot = "dot-grey.png"

            list_item.setIcon(QtGui.QIcon(GetRelPath(self, f"assets\images\{dot}")))

            self.result_list_model.appendRow(list_item)

        self.ui.result_listView.doubleClicked.connect(lambda index: ShowCVEInfo_CIA(self, index))
        self.logger.debug("Show_Report_CIA : List maked")
    except Exception as e:
        Report_Error(self, f"Show_Report_CIA : {e}")


def ShowCVEInfo_CIA(self, index):
    try:
        item_index = index.row()
        self.logger.debug(f"ShowCVEInfo_CIA : item index {str(item_index).strip()} ")
        cve_info = self.report["cve_list"][item_index]

        self.ui.label_cve_head.setText(
            f"{cve_info["cve"]} - {cve_info["package"].capitalize()} - {cve_info["version"]}")

        self.ui.label_published.setText(
            f"Published: {cve_info["datePublished"]}" if "datePublished" in cve_info and cve_info[
                "datePublished"].strip != "" else "Published: No date")
        self.ui.cve_desc_plainTextEdit.setPlainText(cve_info["desc"].capitalize())

        self.ui.label_shortname.setText(f"Shortname: {cve_info["shortName"].capitalize()}")

        for ref in cve_info["references"]:
            self.ui.plainTextEdit_references.appendHtml(f"<a href='{ref['url']}'>{ref['url']}</a>")

        if "cvssV3_1" in cve_info["cvss_metrics"]:
            for item in cve_info["cvss_metrics"]["cvssV3_1"]:
                self.ui.plainTextEdit_cvss_3.appendPlainText(
                    f"{Split_by_Uppercase(self, item)}: {cve_info["cvss_metrics"]["cvssV3_1"][item]}")
        else:
            self.ui.plainTextEdit_cvss_3.setPlainText("No info")

        StackedWidgetChangePage(self, 5)
    except Exception as e:
        Report_Error(self, f"ShowCVEInfo_CIA : {e}")


def Show_Report_CCD(self, rep):
    try:
        self.logger.debug("Show_Report_CCD : loading report")
        self.report = json.loads(rep)
    except Exception as e:
        Report_Error(self, "Failed to convert report to JSON format : " + str(e))

    self.ui.next_work_button.show()
    self.logger.debug("Show_Report_CCD : next_work_button : show")

    self.logger.debug(f"Show_Report_CCD : {len(self.report["driver_list"])} drivers in list")
    if len(self.report["driver_list"]) == 0:
        ElemShowAnim(self, self.ui.label_no_cve)
        return

    try:
        # Calculate alignment
        str_max = 126
        shortName_max = max(len(item["shortName"]) for item in self.report["driver_list"]) + 8
        version_max = max(len(item["version"]) for item in self.report["driver_list"]) + 8
        self.logger.debug(
            f"Show_Report_CCD : cve_max {shortName_max} : version_max {version_max}")

        # Header alignment
        header = f"     {'Name'.ljust(shortName_max)}{'Version'.ljust(version_max)}Desc"
        self.ui.label_result_info.setText(header)

        # Setup list
        self.result_list_model = QtGui.QStandardItemModel()
        self.ui.result_listView.setModel(self.result_list_model)

        # Items alignment
        for item in self.report["driver_list"]:
            string = f"  {item['shortName'].ljust(shortName_max)}{str(item['version']).ljust(version_max)}"

            if len(string + item["desc"]) > str_max:
                desc = f"{item['desc'][:120 - len(string)]}..."
            else:
                desc = item["desc"]

            list_item = QtGui.QStandardItem()
            list_item.setText(string + desc)
            list_item.setIcon(QtGui.QIcon(r"assets\images\risk.png"))

            self.result_list_model.appendRow(list_item)

        self.ui.result_listView.doubleClicked.connect(lambda index: ShowCVEInfo_CCD(self, index))
        self.logger.debug("Show_Report_CCD : List maked")
    except Exception as e:
        Report_Error(self, f"Show_Report_CCD : {e}")


def ShowCVEInfo_CCD(self, index):
    try:
        item_index = index.row()
        self.logger.debug(f"ShowCVEInfo_CIA : item index {str(item_index).strip()} ")
        driver_info = self.report["driver_list"][item_index]
        self.ui.label_vuln_head.setText(f"{driver_info["shortName"]} - {driver_info["version"]}")

        self.ui.plainTextEdit_vuln.setPlainText(FormatDict(self, driver_info))

        StackedWidgetChangePage(self, 7)
    except Exception as e:
        Report_Error(self, f"ShowCVEInfo_CCD : {e}")


def FormatDict(self, data, indent=0):
    formatted_data = ""
    for key, value in data.items():
        formatted_key = Split_by_Uppercase(self, key if isinstance(key, str) else str(key), split_dot=True)
        if isinstance(value, dict):
            formatted_value = FormatDict(self, value, indent + 4)
        elif isinstance(value, list):
            list_lenght = len(value)
            if list_lenght == 0 or all(v is None or "" for v in value):
                continue
            elif list_lenght == 1:
                formatted_value = f"{value[0] if isinstance(value[0], str) else str(value[0])}"
            else:
                formatted_value = f"\n{" " * (indent + 8)}· " + f"\n{" " * (indent + 8)}· ".join(
                    [f"{item}" if isinstance(item, str) else str(item) for item in value]) + "\n"
        else:
            formatted_value = f"{value}" if isinstance(value, str) else str(value)
        formatted_data += " " * indent + formatted_key + " : " + formatted_value + "\n"
    self.logger.debug(f"FormatDict : Formated")
    return formatted_data


def Split_by_Uppercase(self, word, split_dot=False):
    result = re.sub(r"([a-z])([A-Z])", r"\1 \2", word).strip().capitalize()
    if split_dot:
        result = result.replace(".", " ")
    self.logger.debug(f"Split_by_uppercase : {word} --> {result}")
    return result
