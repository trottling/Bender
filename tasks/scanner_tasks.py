import concurrent.futures as cf
import platform
import shutil
import socket
import subprocess

import cpuinfo
import httpx
import psutil
import vulners
import win32api
import wmi

from PyQt6 import QtTest, QtCore
from PyQt6.QtGui import QMovie
from PyQt6.uic.properties import QtGui
from getmac import get_mac_address
from windows_tools import windows_firewall, bitness, bitlocker
from windows_tools.installed_software import get_installed_software

from ui.animations import StackedWidgetChangePage, ElemShowAnim, TextChangeAnim, ImageChangeAnim
from ui.show_report import Show_Report_CIA
from ui.tools import GetRelPath


def Run_Scanner_Tasks(self):
    StackedWidgetChangePage(self, 1)

    #
    # Run ThreadPoolExecutor --> Put result in result page
    #

    # Funcs calls results
    self.scan_result = []

    # Custom waiting list
    self.done_scan_tasks_list = []

    # Funcs to call
    self.scan_tasks_list = [RunCIA, GetWinIcon, GetWinVersions, GetCpu, GetGpu, GetRam, GetRom,
                            GetFirewall, GetMac, GetLocalIP, GetExtIP, GetBitness, GetBitlocker,
                            GetVirtualization]

    # UI Input vars
    self.net_threads = self.ui.horizontalSlider_network_threads.value()
    self.data_workers = self.ui.horizontalSlider_data_threads.value()
    self.vulners_key = self.ui.api_key.text().strip()

    # Scan funcs vars
    self.apps_report = {}
    self.soft_list = []
    self.soft_list_vulners = []

    # Pbar values
    self.res_good = 0
    self.res_bad = 0

    # Set loading gif to progress label
    QtTest.QTest.qWait(500)
    gif = QMovie(GetRelPath(self, r"assets\gifs\loading.gif"))
    gif.setFormat(b"gif")
    gif.setScaledSize(QtCore.QSize(45, 45))
    self.ui.image_work_progress.setMovie(gif)
    gif.start()
    ElemShowAnim(self, self.ui.image_work_progress, dur=200)
    ElemShowAnim(self, self.ui.label_work_progress, dur=200)
    QtTest.QTest.qWait(500)

    # Start funcs
    with cf.ThreadPoolExecutor(max_workers=len(self.scan_tasks_list)) as self.sc_pool:

        [self.done_scan_tasks_list.append(self.sc_pool.submit(task, self)) for task in self.scan_tasks_list]

        while all([i.done() is not True for i in self.done_scan_tasks_list]):
            QtTest.QTest.qWait(200)
        self.sc_pool.shutdown(wait=True, cancel_futures=False)

    #
    # First element in list is func, other is args
    # Sleep for more pretty anim
    #

    for task in self.scan_result:
        if task is not None:
            try:
                task[0](*[arg for arg in task[1:] if len(task) > 1])
            except Exception as e:
                self.logger.error(f"Run_Scanner_Tasks : {e}")

    ElemShowAnim(self, self.ui.next_work_btn)
    TextChangeAnim(self, self.ui.label_work_progress, "Done")
    self.ui.image_work_progress.clear()
    ImageChangeAnim(self, self.ui.image_work_progress, r"assets\images\bender-medium.png")
    UpdateResultInfo(self)


def UpdateResultInfo(self):
    TextChangeAnim(self, self.ui.label_scan_successful_len, str(self.res_good))
    TextChangeAnim(self, self.ui.label_scan_error_len, str(self.res_bad))


def GetWinIcon(self):
    try:
        win_icon = ""
        match platform.release():
            case '11':
                win_icon = r"windows-11.png"
            case '10':
                win_icon = r"windows-10.png"
            case '8' | '8.1':
                win_icon = r"windows-8.png"

        self.scan_result.append([self.ui.label_System_image.setStyleSheet,
                                 str(".QLabel {image: url('" + GetRelPath(self,
                                                                          r"assets\\images\\" + win_icon) + "')}")])

        self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetWinIcon : {e}")
        self.res_bad += 1


def GetWinVersions(self):
    try:
        self.scan_result.append([self.ui.label_System_name.setText, f"{platform.system()} {platform.release()}"])
        self.scan_result.append([self.ui.label_System_ver.setText, platform.version()])
        self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetWinVersions : {e}")
        self.res_bad += 1


def GetCpu(self):
    try:
        self.scan_result.append([self.ui.label_Hardware_cpu.setText, cpuinfo.get_cpu_info()['brand_raw']])
        self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetCpu : {e}")
        self.res_bad += 1


def GetGpu(self):
    try:
        self.scan_result.append(
            [self.ui.label_Hardware_gpu.setText, str(wmi.WMI().Win32_VideoController()[0].wmi_property('Name').value)])
        self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetGpu : {e}")
        self.res_bad += 1


def GetRam(self):
    try:
        self.scan_result.append(
            [self.ui.label_Hardware_ram.setText, f"{round(psutil.virtual_memory().total / 1073741824)} Gb RAM"])
        self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetRam : {e}")
        self.res_bad += 1


def GetRom(self):
    try:
        space = 0.0
        for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
            total, _, _ = shutil.disk_usage(drive)
            space += total
        self.scan_result.append([self.ui.label_Hardware_rom.setText, f"{space // (2 ** 30)} Gb ROM"])
        self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetRom : {e}")
        self.res_bad += 1


def GetFirewall(self):
    try:
        if windows_firewall.is_firewall_active():
            fwlen = len(
                subprocess.run(["powershell", "Get-NetFirewallRule"], capture_output=True, text=True).stdout.split(
                    "\n\n"))
            self.scan_result.append(
                [self.ui.label_Network_rules.setText, f"{fwlen} Firewall rules" if fwlen > 0 else "Firewall Active"])
        else:
            self.scan_result.append([self.ui.label_Network_rules.setText, "Firewall Inactive"])
            self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetFirewall : {e}")
        self.res_bad += 1


def GetMac(self):
    try:
        self.scan_result.append([self.ui.label_network_mac.setText, f"{str(get_mac_address())} - Mac adress"])
        self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetMac : {e}")
        self.res_bad += 1


def GetLocalIP(self):
    try:
        self.scan_result.append(
            [self.ui.label_Network_local_ip.setText, f"{socket.gethostbyname(socket.gethostname())} - Local IP"])
        self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetLocalIP : {e}")
        self.res_bad += 1


def GetExtIP(self):
    try:
        self.scan_result.append(
            [self.ui.label_Network_ext_ip.setText,
             f"{httpx.get(url="https://api.ipify.org", timeout=5).content.decode('utf8')} - External IP"])
        self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetExtIP : {e}")
        self.res_bad += 1


def GetBitness(self):
    try:
        if bitness.is_64bit():
            self.scan_result.append([self.ui.frame_sys_bitness.setStyleSheet,
                                     ".QFrame {image: url('" + GetRelPath(self, 'assets//images//64-bit.png') + "')}"])
            self.scan_result.append([self.ui.label_sys_bitness.setText, f"64 Bit Bitness"])
        else:
            self.scan_result.append([self.ui.frame_sys_bitness.setStyleSheet,
                                     ".QFrame {image: url('" + GetRelPath(self, 'assets//images//32-bit.png') + "')}"])
            self.scan_result.append([self.ui.label_sys_bitness.setText, f"32 Bit Bitness"])
        self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetBitness : {e}")
        self.res_bad += 1


def GetBitlocker(self):
    try:
        if bitlocker.check_bitlocker_management_tools():  # TODO FIX
            self.scan_result.append([self.ui.label_sys_bitlocker.setText, f"Bitlocker Enabled"])
        else:
            self.scan_result.append([self.ui.label_sys_bitlocker.setText, f"Bitlocker Disabled"])
        self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetBitlocker : {e}")
        self.res_bad += 1


def GetVirtualization(self):
    try:
        out = subprocess.run(["powershell", 'Get-ComputerInfo -property HyperVisorPresent'],
                             capture_output=True,
                             text=True).stdout
        if "True" in out:
            self.scan_result.append([self.ui.label_sys_virt.setText, f"Virtualization Enabled"])
        elif "False" in out:
            self.scan_result.append([self.ui.label_sys_virt.setText, f"Virtualization Disabled"])
        else:
            self.scan_result.append([self.ui.label_sys_virt.setText, f"Unknown Virtualization"])
        self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetVirtualization : {e}")
        self.res_bad += 1


def RunCIA(self):
    print("\n\n\nЖОПА\n\n\n")
    try:
        for software in get_installed_software():
            if software['name'] != "" and software['version'] != "":
                self.soft_list.append(software)
        self.logger.debug(f"RunCIA : {len(self.soft_list)} soft")
    except Exception as e:
        self.logger.error(f"RunCIA : {e}")
        self.res_bad += 1
        return

    # check for zero list length
    if len(self.soft_list) == 0:
        self.logger.error(f"RunCIA : zero soft_list")
        self.res_bad += 1
        return

    # All apps list
    self.scan_result.append([FillInstalledAppsList, self, self.soft_list])

    self.logger.debug(f"Transforming softwares list to vulners.com format")
    for software in self.soft_list:
        self.soft_list_vulners.append(dict({"software": software['name'], "version": software['version']}))

    self.logger.debug(f"Connecting to vulners.com API")

    try:
        self.vulners_api = vulners.VulnersApi(api_key=self.vulners_key)
    except Exception as e:
        self.logger.error("RunCIA : Failed to connect Vulners Api : " + str(e))
        return

    self.logger.debug(f"Sending softwares list to vulners.com")
    try:
        if len(self.soft_list_vulners) > 500:
            for i in range(0, len(self.soft_list_vulners), 500):
                yield self.soft_list_vulners[i:i + 500]
            for chunk in self.soft_list_vulners:
                self.apps_report.update(self.vulners_api.software_audit(os="", version="", packages=chunk))
        else:
            self.apps_report = self.vulners_api.software_audit(os="", version="", packages=self.soft_list_vulners)
    except Exception as e:
        self.logger.error("RunCIA : Failed to get vulners.com report : " + str(e))
        return

    # Clear labels without CVE
    self.apps_report = [vuln for vuln in self.apps_report['vulnerabilities'] if vuln['id']]

    # Transorm to result format
    self.cve_list = []
    try:
        for item in self.apps_report:
            cve = {
                "cve": item["id"][0],
                "package": item["package"],
                "version": item["version"],
                "score": 0,
                "desc": "",
                "datePublished": "",
                "shortName": "",
                "cvss_metrics": [],
                "references": [],
            }
            self.cve_list.append(cve)
        self.apps_report = {"cve_list": self.cve_list}
    except Exception as e:
        self.logger.error("RunCIA : Failed to transorm to needed format : " + str(e))
        return

    self.logger.debug(f"RunCIA : Transormed to needed format : {self.apps_report}")

    #
    # Getting more info about CVEs
    #

    if len(self.apps_report["cve_list"]) == 0:
        pass
    else:
        try:
            with cf.ThreadPoolExecutor(max_workers=self.net_threads) as executor:
                futures = []
                for item in self.apps_report["cve_list"]:
                    futures.append(executor.submit(CIA_Get_CVE_Info, self=self, item=item))
                executor.shutdown(wait=True, cancel_futures=False)
        except Exception as e:
            self.logger.error("RunCIA : Failed to Getting more info about CVEs : " + str(e))
            return

    #
    # Done
    #

    self.logger.debug(f"RunCIA : Done")
    self.scan_result.append([Show_Report_CIA, self])


def CIA_Get_CVE_Info(self, item):
    cve_id = item["cve"]
    self.logger.debug(f"CIA_Get_CVE_Info : Processing {cve_id}")
    try:
        resp = httpx.get(f"https://cveawg.mitre.org/api/cve/{cve_id}", timeout=10).json()

        item["desc"] = resp["containers"]["cna"]["descriptions"][0]["value"] if \
            resp["containers"]["cna"]["descriptions"][0]["value"] else "No descriprion"

        if "metrics" in resp["containers"]["cna"] and "cvssV3_1" in \
                resp["containers"]["cna"]["metrics"][0]:
            item["score"] = resp["containers"]["cna"]["metrics"][0]["cvssV3_1"][
                "baseScore"]
        else:
            "-"

        if "assignerShortName" in resp["cveMetadata"]:
            item["shortName"] = resp["cveMetadata"]["assignerShortName"]
        else:
            item["shortName"] = "No shortname"

        if "metrics" in resp["containers"]["cna"] and "cvssV3_1" in \
                resp["containers"]["cna"]["metrics"][0]:
            item["cvss_metrics"] = resp["containers"]["cna"]["metrics"][0]
        else:
            "-"

            item["datePublished"] = resp["cveMetadata"]["datePublished"] if \
                resp["cveMetadata"]["datePublished"] else "No date"

        if "references" in resp["containers"]["cna"]:
            item["references"] = resp["containers"]["cna"]["references"]
        else:
            "No references"
    except Exception as e:
        self.logger.error(f"RunCIA : {cve_id} : Failed to get more info : {str(e)}")


def FillInstalledAppsList(self, data):
    name_max = max(len(item['name']) for item in data)
    ver_max = max(len(item['version']) for item in data)
    autor_max = max(len(item['publisher']) for item in data)

    self.all_app_list_model = QtGui.QStandardItemModel()
    self.ui.Software_listView_vuln.setModel(self.all_app_list_model)

    for item in data:
        list_item = QtGui.QStandardItem()
        list_item.setText(
            f"{item['name'].ljust(name_max - len(item['name']))}{item['version'].ljust(ver_max - len(item['version']))}{item['publisher'].ljust(autor_max - len(item['publisher']))}")
        self.all_app_list_model.appendRow(list_item)
