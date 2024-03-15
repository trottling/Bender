import concurrent.futures as cf
import hashlib
import platform
import shutil
import socket
import subprocess
from os import listdir
from os.path import join, isfile

import cpuinfo
import httpx
import psutil
import vulners
import wmi
from PyQt6 import QtTest, QtCore, QtGui
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QMovie
from getmac import get_mac_address
from portscan import PortScan
from windows_tools import windows_firewall, bitness, bitlocker, logical_disks, updates
from windows_tools.installed_software import get_installed_software

from ui.animations import StackedWidgetChangePage, ElemShowAnim, TextChangeAnim, ImageChangeAnim, ElemHideAnim
from ui.show_report import ReportApps, ReportDrivers, FillExtPorts, FillLocalPorts, FillKBList, ReportKB
from ui.tools import GetRelPath


def Run_Scanner_Tasks(self):
    StackedWidgetChangePage(self, 1)

    #
    # Run ThreadPoolExecutor --> Put result in result page
    #

    # Funcs calls results
    self.scan_result = [[LoadShodanReport, self]]

    # Custom waiting list
    self.done_scan_tasks_list = []

    # Funcs to call
    # Firts run long-time funcs
    self.scan_tasks_list = [CheckApps, CheckDrivers, CheckKB, GetLocalPorts,
                            GetExtPorts, GetWinIcon, GetWinVersions, GetCpu,
                            GetGpu, GetRam, GetRom, GetFirewall,
                            GetMac, GetLocalIP, GetExtIP, GetBitness,
                            GetBitlocker, GetVirtualization]

    # UI Input vars
    self.net_threads = self.ui.horizontalSlider_network_threads.value()
    self.data_workers = self.ui.horizontalSlider_data_threads.value()
    self.vulners_key = self.ui.api_key.text().strip()

    # Scan funcs vars
    self.apps_report = {}
    self.soft_list = []
    self.soft_list_vulners = []
    self.drivers_report = {}
    self.drivers_list = []
    self.drivers_list_hashed = []  # Sha256 and Sha1 hash
    self.drivers_vuln_list = []
    self.driver_db = None
    self.kb_list = []
    self.kb_scan_res = {}
    self.kb_report = {}

    # Info values
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

    ChangeWorkElems(self)


def ChangeWorkElems(self):
    TextChangeAnim(self, self.ui.label_work_progress, "Done")
    ElemHideAnim(self, self.ui.label_win_warn, dur=200)
    self.ui.image_work_progress.clear()
    ImageChangeAnim(self, self.ui.image_work_progress, r"assets\images\bender-medium.png")
    self.ui.label_scan_successful_len.setText(str(self.res_good))
    self.ui.label_scan_error_len.setText(str(self.res_bad))

    QtTest.QTest.qWait(1000)

    for elem in [self.ui.framel_scan_successful, self.ui.label_scan_successful,
                 self.ui.label_scan_successful_len, self.ui.frame_scan_error,
                 self.ui.label_scan_error, self.ui.label_scan_error_len,
                 self.ui.next_work_btn]:
        ElemShowAnim(self, elem)
        QtTest.QTest.qWait(50)

    QtTest.QTest.qWait(250)


def LoadShodanReport(self):
    try:
        ip = httpx.get(url="https://api.ipify.org", timeout=5).content.decode('utf8')
        self.ui.WebWidget.load(QUrl(f"https://www.shodan.io/host/{ip}"))
        self.logger.debug("LoadShodanReport : loaded")
        self.res_good += 1
    except Exception as e:
        self.logger.error(f"LoadShodanReport : {e}")
        self.res_bad += 1


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
        for drive in logical_disks.get_logical_disks():
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
        drives_list = []
        if bitlocker.check_bitlocker_management_tools():

            for drive in logical_disks.get_logical_disks():

                for line in subprocess.check_output(['manage-bde', '-status', drive]).decode(encoding='utf-8',
                                                                                             errors='ignore'):
                    if 'AES' or 'XEX' in line:
                        drives_list.append(drive)
                        break
            if len(drives_list) != 0:
                text = ", ".join([i.replace(":", "") for i in list(set(drives_list))])  # Remove ":" from drive name
                self.scan_result.append([self.ui.label_sys_bitlocker.setText,
                                         f"Bitlocker Enabled - {"Disks" if len(drives_list) > 1 else "Disk"} {text}"])
            else:
                self.scan_result.append([self.ui.label_sys_bitlocker.setText, f"Bitlocker Disabled"])
        else:
            self.scan_result.append([self.ui.label_sys_bitlocker.setText, f"Bitlocker Tools not found"])
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


def GetApps(self):
    try:
        for software in get_installed_software():
            if software['name'] != "" and software['version'] != "":
                self.soft_list.append(software)

        self.logger.debug(f"GetApps : {len(self.soft_list)} soft")

        # check for zero list length
        if len(self.soft_list) > 0:
            self.res_good += 1
            return False
        else:
            self.res_bad += 1
            return True

    except Exception as e:
        self.logger.error(f"GetApps : {e}")
        self.res_bad += 1
        return True


def ConnectVulnersSoft(self):
    try:
        self.vulners_api_soft = vulners.VulnersApi(api_key=self.vulners_key)
        self.res_good += 1
        return False
    except Exception as e:
        self.logger.error(f"ConnectVulnersSoft : {e}")
        self.res_bad += 1
        return True


def SendAppsVulners(self):
    try:
        if len(self.soft_list) > 500:
            while True:

                try:
                    self.soft_list_vulners = [next(self.soft_list) for _ in range(500)]
                except StopIteration:
                    self.apps_report.update(self.vulners_api_soft.software_audit(os="", version="", packages=[
                        {"software": software['name'], "version": software['version']} for software in
                        self.soft_list_vulners]))
                    break

                self.apps_report.update(self.vulners_api_soft.software_audit(os="", version="", packages=[
                    {"software": software['name'], "version": software['version']} for software in
                    self.soft_list_vulners]))
        else:
            self.apps_report = self.vulners_api_soft.software_audit(os="", version="", packages=[
                {"software": software['name'], "version": software['version']} for software in self.soft_list])
        self.res_good += 1
        return False
    except Exception as e:
        self.logger.error(f"SendAppsVulners : Failed to get vulners.com report : {e}")
        self.res_bad += 1
        return True


def ProcessAppsResponse(self):
    self.cve_list_apps = []

    try:
        for item in [vuln for vuln in self.apps_report['vulnerabilities'] if vuln['id']]:
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
            self.cve_list_apps.append(cve)
        self.apps_report = {"cve_list": self.cve_list_apps}
    except Exception as e:
        self.logger.error(f"ProcessAppsResponse : Failed to transorm to needed format : {e}")
        self.res_bad += 1
        return True

    # Getting more info about CVEs
    if len(self.apps_report["cve_list"]) > 0:
        try:
            with cf.ThreadPoolExecutor(max_workers=self.net_threads) as executor:
                futures = []
                for item in self.apps_report["cve_list"]:
                    futures.append(executor.submit(GetCveInfo, self=self, item=item))
                executor.shutdown(wait=True, cancel_futures=False)
        except Exception as e:
            self.logger.error(f"ProcessAppsResponse : Failed to Getting more info about CVEs : {e}")
            self.res_bad += 1
            return True

    self.res_good += 1
    return False


def GetCveInfo(self, item):
    cve_id = item["cve"]
    self.logger.debug(f"GetCveInfo : Processing {cve_id}")

    try:
        self.mitre_resp = httpx.get(f"https://cveawg.mitre.org/api/cve/{cve_id}", timeout=10).json()
    except Exception as e:
        self.logger.error(f"GetCveInfo : {cve_id} : {e}")

    try:
        item["desc"] = self.mitre_resp["containers"]["cna"]["descriptions"][0]["value"]
    except KeyError:
        item["desc"] = "No descriprion"

    try:
        item["score"] = self.mitre_resp["containers"]["cna"]["metrics"][0]["cvssV3_1"]["baseScore"]
    except KeyError:
        item["score"] = "-"

    try:
        item["shortName"] = self.mitre_resp["cveMetadata"]["assignerShortName"]
    except KeyError:
        item["shortName"] = "No shortname"

    try:
        item["cvss_metrics"] = self.mitre_resp["containers"]["cna"]["metrics"][0]
    except KeyError:
        item["cvss_metrics"] = "-"

    try:
        item["datePublished"] = self.mitre_resp["cveMetadata"]["datePublished"]
    except KeyError:
        item["datePublished"] = "No date"

    try:
        item["references"] = self.mitre_resp["containers"]["cna"]["references"]
    except KeyError:
        item["references"] = "No references"


def CheckApps(self):
    if GetApps(self):
        self.res_bad += 1
        return

    # Fill all apps list
    self.scan_result.append([FillAllAppsList, self, self.soft_list])

    # Connect to Vulners api via his lib
    if ConnectVulnersSoft(self):
        self.res_bad += 1
        return

    # Sending softwares list to Vulners api via his lib
    if SendAppsVulners(self):
        self.res_bad += 1
        return

    # Transorm to result format
    if ProcessAppsResponse(self):
        self.res_bad += 1
        return

    self.scan_result.append([ReportApps, self])
    self.res_good += 1


def FillAllAppsList(self, data):
    try:
        self.all_app_list_model = QtGui.QStandardItemModel()
        self.ui.Software_listView_all.setModel(self.all_app_list_model)
        for item in data:
            list_item = QtGui.QStandardItem()
            list_item.setText(
                str(item['name'][:40]).capitalize() + f"{"..." if len(item['name']) > 40 else ""}" + "\t" + str(
                    item['version'][:15]))
            self.all_app_list_model.appendRow(list_item)

        self.res_good += 1
    except Exception as e:
        self.logger.error(f"FillAllAppsList : {e}")
        self.res_bad += 1


def GetLocalPorts(self):
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        self.LocalPorts = PortScan(ip_str=local_ip, port_str="1-49151",
                                   thread_num=1000, show_refused=False,
                                   wait_time=3, stop_after_count=True).run()

        self.scan_result.append([FillLocalPorts, self])

        self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetLocalPorts : {e}")
        self.res_bad += 1


def GetExtPorts(self):
    try:

        ext_ip = httpx.get(url="https://api.ipify.org", timeout=5).content.decode('utf8')
        self.ExtPorts = PortScan(ip_str=ext_ip, port_str="1-49151",
                                 thread_num=1000, show_refused=False,
                                 wait_time=3, stop_after_count=True).run()

        self.scan_result.append([FillExtPorts, self])
        self.res_good += 1
    except Exception as e:
        self.logger.error(f"GetExtPorts : {e}")
        self.res_bad += 1


def GetDrivers(self):
    try:
        # getting drivers
        for driver in [f for f in listdir(r"c:\windows\system32\drivers") if
                       isfile(join(r"c:\windows\system32\drivers", f))]:
            self.drivers_list.append(driver)

        self.logger.debug(f"GetDrivers : {len(self.drivers_list)} drivers")

        # check for zero list length
        if len(self.drivers_list) == 0:
            self.res_bad += 1
            return True

        self.res_good += 1
        return False
    except Exception as e:
        self.logger.error(f"GetDrivers : {e}")
        self.res_bad += 1
        return True


def HashDrivers(self):
    try:
        for driver in self.drivers_list:
            # [sha256, sha1]
            drivers_path = r"c:\windows\system32\drivers"
            with open(f"{drivers_path}\\{driver}", "rb") as f:
                self.drivers_list_hashed.append(
                    [hashlib.sha256(f.read()).hexdigest(), hashlib.sha1(f.read()).hexdigest()])
        self.res_good += 1
        return False
    except Exception as e:
        self.logger.error(f"HashDrivers : {e}")
        self.res_bad += 1
        return True


def GetDriversDB(self):
    try:
        self.driver_db = httpx.get("https://www.loldrivers.io/api/drivers.json", timeout=10).json()
        self.logger.debug(f"GetDriversDB : {len(self.driver_db)} drivers in database")

        if len(self.driver_db) == 0:
            self.res_bad += 1
            return True

        self.res_good += 1
        return False

    except Exception as e:
        self.logger.error(f"GetDriversDB : {e}")
        self.res_bad += 1
        return True


def ScanDrivers(self):
    try:
        with cf.ThreadPoolExecutor(max_workers=self.data_workers) as executor:
            futures = []
            for drv_hash in self.drivers_list_hashed:
                futures.append(executor.submit(ProcessDriver, self=self, drv_hash=drv_hash))
            executor.shutdown(wait=True, cancel_futures=False)

        self.res_good += 1
        return False
    except Exception as e:
        self.logger.error(f"ScanDrivers : {e}")
        self.res_bad += 1
        return True


def RecursiveSaveDict(self, source_dict, target_dict, prefix=""):
    for key, value in source_dict.items():
        if isinstance(value, dict):
            RecursiveSaveDict(self, value, target_dict, prefix + key + ".")
        else:
            target_dict[prefix + key] = value


def ProcessDriver(self, drv_hash):
    for date in self.driver_db:
        for item in date["KnownVulnerableSamples"]:
            if 'SHA256' in item and drv_hash[0] == item['SHA256'] or 'SHA1' in item and drv_hash[1] == item['SHA1']:

                try:
                    shortName = item["Filename"]
                except KeyError:
                    try:
                        shortName = item["OriginalFilename"]
                    except KeyError:
                        shortName = "Unknown Short Name"

                try:
                    version = item["FileVersion"]
                except KeyError:
                    version = "No File Version"

                try:
                    datePublished = item["CreationTimestamp"]
                except KeyError:
                    datePublished = "No Date Published"

                try:
                    Company = item["Company"]
                except KeyError:
                    Company = "No Company"

                try:
                    Desc = item["Description"]
                except KeyError:
                    Desc = "No Description"

                try:
                    Product = item["Product"]
                except KeyError:
                    Product = "No Product"

                try:
                    Copyright = item["Copyright"]
                except KeyError:
                    Copyright = "No Copyright"

                try:
                    ImportedFunctions = item["ImportedFunctions"]
                except KeyError:
                    ImportedFunctions = ["No Imported Functions"]

                try:
                    drhash = f"SHA256 : {item['SHA256']}"
                except KeyError:
                    drhash = f"SHA1 : {item['SHA1']}"

                vuln_driver_data = {
                    "shortName": shortName,
                    "version": version,
                    "datePublished": datePublished,
                    "desc": f"{Company} : {Desc} : {Product} : {Copyright}",
                    "ImportedFunctions": ImportedFunctions,
                    "hash": drhash
                }
                RecursiveSaveDict(self, date, vuln_driver_data)
                self.drivers_vuln_list.append(vuln_driver_data)


def CheckDrivers(self):
    if GetDrivers(self):
        self.res_bad += 1
        return

    self.scan_result.append([FillDriversList, self])

    if HashDrivers(self):
        self.res_bad += 1
        return

    if GetDriversDB(self):
        self.res_bad += 1
        return

    if ScanDrivers(self):
        self.res_bad += 1
        return

    self.drivers_report = {"driver_list": self.drivers_vuln_list}

    self.scan_result.append([ReportDrivers, self])


def FillDriversList(self):
    try:
        self.Drivers_list_model = QtGui.QStandardItemModel()
        self.ui.Drivers_listView_all.setModel(self.Drivers_list_model)
        for item in self.drivers_list:
            list_item = QtGui.QStandardItem()
            list_item.setText(item)
            self.Drivers_list_model.appendRow(list_item)

        self.res_good += 1
    except Exception as e:
        self.logger.error(f"FillExtPorts : {e}")
        self.res_bad += 1


def ConnectVulnersKB(self):
    try:
        self.vulners_api_kb = vulners.VulnersApi(api_key=self.vulners_key)
        self.res_good += 1
        return False
    except Exception as e:
        self.logger.error(f"ConnectVulnersKB : {e}")
        self.res_bad += 1
        return True


def GetKB(self):
    try:
        self.kb_list = updates.get_windows_updates(filter_duplicates=True)
        self.logger.debug(f"GetKB : {len(self.kb_list)} KB")
        if len(self.kb_list) == 0:
            self.res_bad += 1
            return True

        self.res_good += 1
        return False
    except Exception as e:
        self.logger.error(f"ConnectVulnersKB : {e}")
        self.res_bad += 1
        return True


def SendKBVulners(self):
    try:
        # List with deleted KBs without KB ID
        kb = [item['kb'] for item in self.kb_list if item['kb'] not in ("", None) and "KB" in item['kb']]
        self.logger.debug(f"SendKBVulners : {kb}")
        self.kb_scan_res = self.vulners_api_kb.kb_audit(os=f"{platform.system()} {platform.release()}",
                                                        kb_list=kb)
        self.res_good += 1
        return False
    except Exception as e:
        self.logger.error(f"SendKBVulners : {e}")
        self.res_bad += 1
        return True


def ProcessKBResponse(self):
    self.cve_list_kb = []

    try:
        for item in self.kb_scan_res["cvelist"]:
            cve = {
                "cve": item,
                "score": 0,
                "desc": "",
                "datePublished": "",
                "shortName": "",
                "cvss_metrics": [],
                "references": [],
            }
            self.cve_list_kb.append(cve)
        self.kb_report = {"cve_list": self.cve_list_kb}
    except Exception as e:
        self.logger.error(f"ProcessKBResponse : Failed to transorm to needed format : {e}")
        self.res_bad += 1
        return True

    # Getting more info about CVEs
    if len(self.kb_report["cve_list"]) > 0:
        try:
            with cf.ThreadPoolExecutor(max_workers=self.net_threads) as executor:
                futures = []
                for item in self.kb_report["cve_list"]:
                    futures.append(executor.submit(GetCveInfo, self=self, item=item))
                executor.shutdown(wait=True, cancel_futures=False)
        except Exception as e:
            self.logger.error(f"ProcessKBResponse : Failed to Getting more info about CVEs : {e}")
            self.res_bad += 1
            return True

    self.res_good += 1
    return False


def CheckKB(self):
    # Another API connection call is needed to ensure that the API wrapper is received at the right time

    if ConnectVulnersKB(self):
        self.res_bad += 1
        return

    if GetKB(self):
        self.res_bad += 1
        return

    self.scan_result.append([FillKBList, self])

    if SendKBVulners(self):
        self.res_bad += 1
        return

    if ProcessKBResponse(self):
        self.res_bad += 1
        return

    self.res_good += 1
    self.scan_result.append([ReportKB, self])
