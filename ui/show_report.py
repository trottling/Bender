import re

from PyQt6 import QtGui

from other.tcp_port_dict import port_dict
from ui.animations import StackedWidgetChangePage, UpdateWorkPageStat
from ui.tools import Report_Error, GetRelPath


def ReportApps(self, report):
    try:
        self.logger.debug(f"ReportApps : {len(report["cve_list"])} CVEs in list")
        # Setup list
        self.vunl_app_list_model = QtGui.QStandardItemModel()
        self.ui.Software_listView_vuln.setModel(self.vunl_app_list_model)

        if len(report["cve_list"]) == 0:
            list_item = QtGui.QStandardItem()
            list_item.setText("No vulnerable apps found")
            self.vunl_app_list_model.appendRow(list_item)
            return

        for item in report["cve_list"]:
            list_item = QtGui.QStandardItem()
            list_item.setText(f"{item['cve']}\t{str(item['score'])}\t{item['package'].capitalize()}\t{item['version']}")

            try:
                self.dot = ""
                self.score = "No score"
                self.score_raw = item['score']

                if self.score_raw in ("", "-", None):
                    self.dot = "dot-out.png"
                else:
                    self.score = float(self.score_raw)
                    if self.score == 0.0:
                        self.dot = "dot-out.png"
                    elif 0.0 < self.score < 4.0:
                        self.dot = "dot-yellow.png"
                    elif 4.0 < self.score < 7.0:
                        self.dot = "dot-orange.png"
                    elif 7.0 < self.score < 9.0:
                        self.dot = "dot-red.png"
                    elif self.score > 9.0:
                        self.dot = "dot-dark-red.png"
                    else:
                        self.dot = "dot-grey.png"
                self.logger.debug(f"ReportApps : Score {self.score_raw} --> {self.score if self.score else ""} --> {self.dot}")
                list_item.setIcon(QtGui.QIcon(GetRelPath(self, f"assets\\images\\{self.dot}")))
            except Exception as e:
                self.logger.error(f"ReportApps : Error setting dot : {e}")

            self.vunl_app_list_model.appendRow(list_item)

        self.ui.Software_listView_vuln.doubleClicked.connect(lambda index: ReportAppsFull(self, index, report))
        self.logger.debug("ReportApps : List maked")
        UpdateWorkPageStat(self, "good")
    except Exception as e:
        Report_Error(self, f"ReportApps : {e}")


def ReportAppsFull(self, index, report):
    try:
        item_index = index.row()
        self.logger.debug(f"ReportAppsFull : item index {str(item_index).strip()} ")
        cve_info = report["cve_list"][item_index]

        self.ui.label_cve_head.setText(f"{cve_info["cve"]} - {cve_info["package"].capitalize()} - {cve_info["version"]}")

        self.ui.label_published.setText(f"Published: {cve_info["datePublished"]}" if "datePublished" in cve_info and cve_info["datePublished"].strip != "" else "Published: No date")
        self.ui.cve_desc_plainTextEdit.setPlainText(cve_info["desc"].capitalize())

        self.ui.label_shortname.setText(f"Shortname: {cve_info["shortName"].capitalize()}")

        self.ui.plainTextEdit_references.clear()
        for ref in cve_info["references"]:
            self.ui.plainTextEdit_references.appendHtml(f"<a href='{ref['url']}'>{ref['url']}</a>")

        self.ui.plainTextEdit_cvss_3.clear()
        if "cvssV3_1" in cve_info["cvss_metrics"]:
            for item in cve_info["cvss_metrics"]["cvssV3_1"]:
                self.ui.plainTextEdit_cvss_3.appendPlainText(
                    f"{Split_Words(self, item)}: {cve_info["cvss_metrics"]["cvssV3_1"][item]}")
        else:
            self.ui.plainTextEdit_cvss_3.setPlainText("No info")

        StackedWidgetChangePage(self, 5)
    except Exception as e:
        Report_Error(self, f"ReportAppsFull : {e}")


def ReportDrivers(self, report):
    try:
        self.logger.debug(f"ReportDrivers : {len(report["driver_list"])} drivers in list")

        # Setup list
        self.vunl_app_list_model = QtGui.QStandardItemModel()
        self.ui.Drivers_listView_vuln.setModel(self.vunl_app_list_model)

        if len(report["driver_list"]) == 0:
            list_item = QtGui.QStandardItem()
            list_item.setText("No vulnerable drivers found")
            self.vunl_app_list_model.appendRow(list_item)
            return

        for item in report["driver_list"]:
            list_item = QtGui.QStandardItem()
            list_item.setText(f"  {item['shortName']}\t{str(item['version'])}\t{item["desc"]}")
            print(f"  {item['shortName']}\t{str(item['version'])}\t{item["desc"]}")
            self.vunl_app_list_model.appendRow(list_item)

        self.ui.Drivers_listView_vuln.doubleClicked.connect(lambda index: ReportDriversFull(self, index, report))
        self.logger.debug("ReportDrivers : List maked")
    except Exception as e:
        Report_Error(self, f"ReportDrivers : {e}")


def ReportDriversFull(self, index, report):
    try:
        item_index = index.row()
        self.logger.debug(f"ShowCVEInfo_CIA : item index {str(item_index).strip()} ")
        driver_info = report["driver_list"][item_index]
        self.ui.label_vuln_head.setText(f"{driver_info["shortName"]} - {driver_info["version"]}")

        self.ui.plainTextEdit_vuln.setPlainText(FormatDict(self, driver_info))

        StackedWidgetChangePage(self, 7)
    except Exception as e:
        Report_Error(self, f"ShowCVEInfo_CCD : {e}")


def FormatDict(self, data, indent=0):
    formatted_data = ""
    for key, value in data.items():
        formatted_key = Split_Words(self, key if isinstance(key, str) else str(key), split_dot=True)
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


def Split_Words(self, word, split_dot=False):
    result = re.sub(r"([a-z])([A-Z])", r"\1 \2", word).strip().capitalize()
    if split_dot:
        result = result.replace(".", " ")
    self.logger.debug(f"Split_Words : {word} --> {result}")
    return result


def ReportKB(self, report):
    try:
        self.logger.debug(f"ReportKB : {len(report["cve_list"])} CVEs in list")

        # Setup list
        self.vunl_app_list_model = QtGui.QStandardItemModel()
        self.ui.vuln_kb_list.setModel(self.vunl_app_list_model)

        if len(report["cve_list"]) == 0:
            list_item = QtGui.QStandardItem()
            list_item.setText("No vulnerable Windows KB found")
            self.vunl_app_list_model.appendRow(list_item)
            return

        for item in report["cve_list"]:
            list_item = QtGui.QStandardItem()
            list_item.setText(f"{item['cve']}\t{str(item['score'])}")

            try:
                self.dot = ""
                self.score = "No score"
                self.score_raw = item['score']

                if self.score_raw in ("", "-", None):
                    self.dot = "dot-out.png"
                else:
                    self.score = float(self.score_raw)
                    if self.score == 0.0:
                        self.dot = "dot-out.png"
                    elif 0.0 < self.score < 4.0:
                        self.dot = "dot-yellow.png"
                    elif 4.0 < self.score < 7.0:
                        self.dot = "dot-orange.png"
                    elif 7.0 < self.score < 9.0:
                        self.dot = "dot-red.png"
                    elif self.score > 9.0:
                        self.dot = "dot-dark-red.png"
                    else:
                        self.dot = "dot-grey.png"
                self.logger.debug(f"ReportKB : Score {self.score_raw} --> {self.score if self.score else ""} --> {self.dot}")
                list_item.setIcon(QtGui.QIcon(GetRelPath(self, f"assets\\images\\{self.dot}")))
            except Exception as e:
                self.logger.error(f"ReportKB : Error setting dot : {e}")

            self.vunl_app_list_model.appendRow(list_item)

        self.ui.vuln_kb_list.doubleClicked.connect(lambda index: ReportKBFull(self, index, report))
        self.logger.debug("ReportKB : List maked")
        UpdateWorkPageStat(self, "good")
    except Exception as e:
        Report_Error(self, f"ReportKB : {e}")


def ReportKBFull(self, index, report):
    try:
        item_index = index.row()
        self.logger.debug(f"ReportKBFull : item index {str(item_index).strip()} ")
        cve_info = report["cve_list"][item_index]

        self.ui.label_cve_head.setText(cve_info["cve"])

        self.ui.label_published.setText(f"Published: {cve_info["datePublished"]}" if "datePublished" in cve_info and cve_info["datePublished"].strip != "" else "Published: No date")
        self.ui.cve_desc_plainTextEdit.setPlainText(cve_info["desc"].capitalize())
        self.ui.label_shortname.setText(f"Shortname: {cve_info["shortName"].capitalize()}")

        self.ui.plainTextEdit_references.clear()
        for ref in cve_info["references"]:
            self.ui.plainTextEdit_references.appendHtml(f"<a href='{ref['url']}'>{ref['url']}</a>")

        self.ui.plainTextEdit_cvss_3.clear()
        if "cvssV3_1" in cve_info["cvss_metrics"]:
            for item in cve_info["cvss_metrics"]["cvssV3_1"]:
                self.ui.plainTextEdit_cvss_3.appendPlainText(f"{Split_Words(self, item)}: {cve_info["cvss_metrics"]["cvssV3_1"][item]}")
        else:
            self.ui.plainTextEdit_cvss_3.setPlainText("No info")

        StackedWidgetChangePage(self, 5)
    except Exception as e:
        Report_Error(self, f"ReportKBFull : {e}")


def FillLocalPorts(self, ports):
    try:
        self.local_ports_list_model = QtGui.QStandardItemModel()
        self.ui.open_local_ports_list.setModel(self.local_ports_list_model)

        if len(ports) == 0:
            list_item = QtGui.QStandardItem()
            list_item.setText("No Local ports found")
            self.local_ports_list_model.appendRow(list_item)
            return

        for item in ports:
            port = str(item[1])
            if port in port_dict:
                list_item = QtGui.QStandardItem()
                service = port_dict[port]["Service Name"] if port_dict[port]["Service Name"] != "" else "No Service Info"
                desc = port_dict[port]["Description"] if port_dict[port]["Description"] != "" else "No Description"
                list_item.setText(f"{port}\t{service}\t{desc}")
                self.local_ports_list_model.appendRow(list_item)
        UpdateWorkPageStat(self, "good")
    except Exception as e:
        self.logger.error(f"FillLocalPorts : {e}")
        UpdateWorkPageStat(self, "bad")


def FillExtPorts(self, ports):
    try:
        self.ext_ports_list_model = QtGui.QStandardItemModel()
        self.ui.open_Externall_ports_list.setModel(self.ext_ports_list_model)

        if len(ports) == 0:
            list_item = QtGui.QStandardItem()
            list_item.setText("No External ports found")
            self.ext_ports_list_model.appendRow(list_item)
            return

        for item in ports:
            port = str(item[1])
            if port in port_dict:
                list_item = QtGui.QStandardItem()
                service = port_dict[port]["Service Name"] if port_dict[port]["Service Name"] != "" else "No Service Info"
                desc = port_dict[port]["Description"] if port_dict[port]["Description"] != "" else "No Description"
                list_item.setText(f"{port}\t{service}\t{desc}")
                self.ext_ports_list_model.appendRow(list_item)
        UpdateWorkPageStat(self, "good")
    except Exception as e:
        self.logger.error(f"FillExtPorts : {e}")
        UpdateWorkPageStat(self, "bad")


def FillKBList(self, data_inst, data_miss):
    try:
        self.All_kb_list_model = QtGui.QStandardItemModel()
        self.ui.all_kb_list.setModel(self.All_kb_list_model)

        if len(data_miss) + len(data_inst) == 0:
            list_item = QtGui.QStandardItem()
            list_item.setText("No installed KB found")
            list_item.setIcon(QtGui.QIcon(GetRelPath(self, f"assets\\images\\dot-grey.png")))
            self.All_kb_list_model.appendRow(list_item)
            return

        for item in data_inst:
            list_item = QtGui.QStandardItem()
            kb = item[str('kb')] if item[str('kb')] not in ("", None) else "No KB ID"
            list_item.setText(f"{kb}\t{item["result"]}\t{item["title"]}")
            list_item.setIcon(QtGui.QIcon(GetRelPath(self, f"assets\\images\\dot-green.png")))
            self.All_kb_list_model.appendRow(list_item)

        for item in data_miss['kbMissed']:
            list_item = QtGui.QStandardItem()
            list_item.setText(item)
            list_item.setIcon(QtGui.QIcon(GetRelPath(self, f"assets\\images\\dot-red.png")))
            self.All_kb_list_model.appendRow(list_item)

        UpdateWorkPageStat(self, "good")
    except Exception as e:
        self.logger.error(f"FillKBList : {e}")
        UpdateWorkPageStat(self, "bad")


def FillAllAppsList(self, data):
    try:
        self.all_app_list_model = QtGui.QStandardItemModel()
        self.ui.Software_listView_all.setModel(self.all_app_list_model)

        if len(data) == 0:
            list_item = QtGui.QStandardItem()
            list_item.setText("No installed apps found")
            self.all_app_list_model.appendRow(list_item)
            return

        for item in data:
            list_item = QtGui.QStandardItem()
            list_item.setText(f"{str(item['name']).capitalize()}\t{str(item['version'])}")
            self.all_app_list_model.appendRow(list_item)

        UpdateWorkPageStat(self, "good")
    except Exception as e:
        self.logger.error(f"FillAllAppsList : {e}")
        UpdateWorkPageStat(self, "bad")


def FillDriversList(self, data):
    try:
        self.Drivers_list_model = QtGui.QStandardItemModel()
        self.ui.Drivers_listView_all.setModel(self.Drivers_list_model)

        if len(data) == 0:
            list_item = QtGui.QStandardItem()
            list_item.setText("No installed drivers found")
            self.Drivers_list_model.appendRow(list_item)
            return

        for item in data:
            list_item = QtGui.QStandardItem()
            list_item.setText(str(item))
            self.Drivers_list_model.appendRow(list_item)

        UpdateWorkPageStat(self, "good")
    except Exception as e:
        self.logger.error(f"FillDriversList : {e}")
        UpdateWorkPageStat(self, "bad")
