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
from PyQt6.QtCore import QUrl
from getmac import get_mac_address
from portscan import PortScan
from windows_tools import windows_firewall, bitness, bitlocker, logical_disks, updates
from windows_tools.installed_software import get_installed_software

from ui.animations import UpdateWorkPageStat


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

        self.label_System_image_setStyleSheet_signal.emit(win_icon)

        self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetWinIcon : {e}")
        self.stat_signal.emit("bad")


def GetWinVersions(self):
    try:
        self.label_System_name_setText_signal.emit(f"{platform.system()} {platform.release()}")
        self.label_System_ver_setText_signal.emit(platform.version())
        self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetWinVersions : {e}")
        self.stat_signal.emit("bad")


def GetCpu(self):
    try:
        self.label_Hardware_cpu_setText_signal.emit(cpuinfo.get_cpu_info()['brand_raw'])
        self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetCpu : {e}")
        self.stat_signal.emit("bad")


def GetGpu(self):
    try:
        self.label_Hardware_gpu_setText_signal.emit(str(wmi.WMI().Win32_VideoController()[0].wmi_property('Name').value))
        self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetGpu : {e}")
        self.stat_signal.emit("bad")


def GetRam(self):
    try:
        self.label_Hardware_ram_setText_signal.emit(f"{round(psutil.virtual_memory().total / 1073741824)} Gb RAM")
        self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetRam : {e}")
        self.stat_signal.emit("bad")


def GetRom(self):
    try:
        space = 0.0
        for drive in logical_disks.get_logical_disks():
            total, _, _ = shutil.disk_usage(drive)
            space += total
        self.label_Hardware_rom_setText_signal.emit(f"{space // (2 ** 30)} Gb ROM")
        self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetRom : {e}")
        self.stat_signal.emit("bad")


def GetFirewall(self):
    try:
        if windows_firewall.is_firewall_active():
            fwlen = len(subprocess.run(["powershell", "Get-NetFirewallRule"], capture_output=True, text=True, startupinfo=self.si).stdout.split("\n\n"))
            self.label_Network_rules_setText_signal.emit(f"{fwlen} Firewall rules" if fwlen > 0 else "Firewall Active")
        else:
            self.label_Network_rules_setText_signal.emit("Firewall Inactive")
            self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetFirewall : {e}")
        self.stat_signal.emit("bad")


def GetMac(self):
    try:
        self.label_network_mac_setText_signal.emit(f"{str(get_mac_address())} - Mac adress")
        self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetMac : {e}")
        self.stat_signal.emit("bad")


def GetLocalIP(self):
    try:
        self.label_Network_local_ip_setText_signal.emit(f"{socket.gethostbyname(socket.gethostname())} - Local IP")
        self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetLocalIP : {e}")
        self.stat_signal.emit("bad")


def GetExtIP(self):
    try:
        self.label_Network_ext_ip_setText_signal.emit(f"{httpx.get(url="https://api.ipify.org", timeout=5).content.decode('utf8')} - External IP")
        self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetExtIP : {e}")
        self.stat_signal.emit("bad")


def GetBitness(self):
    try:
        if bitness.is_64bit():
            self.frame_sys_bitness_setStyleSheet_signal.emit('assets//images//64-bit.png')
            self.label_sys_bitness_setText_signal.emit(f"64 Bit Bitness")
        else:
            self.frame_sys_bitness_setStyleSheet_signal.emit('assets//images//32-bit.png')
            self.label_sys_bitness_setText_signal.emit(f"32 Bit Bitness")
        self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetBitness : {e}")
        self.stat_signal.emit("bad")


def GetBitlocker(self):
    try:
        drives_list = []
        if bitlocker.check_bitlocker_management_tools():

            for drive in logical_disks.get_logical_disks():

                for line in subprocess.check_output(['manage-bde', '-status', drive], startupinfo=self.si).decode(encoding='utf-8', errors='ignore'):
                    if 'AES' or 'XEX' in line:
                        drives_list.append(drive)
                        break
            if len(drives_list) != 0:
                # Remove ":" from drive name
                text = ", ".join([i.replace(":", "") for i in list(set(drives_list))])
                self.label_sys_bitlocker_setText_signal.emit(f"Bitlocker Enabled - {"Disks" if len(drives_list) > 1 else "Disk"} {text}")
            else:
                self.label_sys_bitlocker_setText_signal.emit(f"Bitlocker Disabled")
        else:
            self.label_sys_bitlocker_setText_signal.emit(["self.ui.label_sys_bitlocker.setText", f"Bitlocker Tools not found"])
        self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetBitlocker : {e}")
        self.stat_signal.emit("bad")


def GetVirtualization(self):
    try:
        out = subprocess.run(args=["powershell", 'Get-ComputerInfo -property HyperVisorPresent'],
                             capture_output=True,
                             text=True,
                             startupinfo=self.si).stdout
        if "True" in out:
            self.label_sys_virt_setText_signal.emit(f"Virtualization Enabled")
        elif "False" in out:
            self.label_sys_virt_setText_signal.emit(f"Virtualization Disabled")
        else:
            self.label_sys_virt_setText_signal.emit(f"Unknown Virtualization")
        self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetVirtualization : {e}")
        self.stat_signal.emit("bad")


def GetApps(self):
    try:
        for software in get_installed_software():
            if software['name'] != "" and software['version'] != "":
                self.soft_list.append(software)

        self.logger.debug(f"GetApps : {len(self.soft_list)} soft")

        # check for zero list length
        if len(self.soft_list) > 0:
            self.stat_signal.emit("good")
            return False
        else:
            self.stat_signal.emit("bad")
            return True

    except Exception as e:
        self.logger.error(f"GetApps : {e}")
        self.stat_signal.emit("bad")
        return True


def ConnectVulnersSoft(self):
    try:
        self.vulners_api_soft = vulners.VulnersApi(api_key=self.vulners_key)
        self.stat_signal.emit("good")
        return False
    except Exception as e:
        self.logger.error(f"ConnectVulnersSoft : {e}")
        self.stat_signal.emit("bad")
        return True


def CutListByChunks(self, lst, chunk_max):
    res = [lst[chunk_max * k:chunk_max * (k + 1)] for k in range(chunk_max)]
    self.logger.debug(f"CutListByChunks : {len(lst)} items / {chunk_max} chunk size --> {len(res)} chunks")
    return res


def SendAppsVulners(self):
    try:
        if len(self.soft_list) > 500:
            for chunc in CutListByChunks(self, self.soft_list, 500):
                self.apps_report.update(self.vulners_api_soft.software_audit(os="", version="", packages=[{"software": software['name'], "version": software['version']} for software in chunc]))
        else:
            self.apps_report = self.vulners_api_soft.software_audit(os="", version="", packages=[{"software": software['name'], "version": software['version']} for software in self.soft_list])
        self.stat_signal.emit("good")
        return False
    except Exception as e:
        self.logger.error(f"SendAppsVulners : Failed to get vulners.com report : {e}")
        self.stat_signal.emit("bad")
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
        self.stat_signal.emit("bad")
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
            self.stat_signal.emit("bad")
            return True

    self.stat_signal.emit("good")
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
        self.stat_signal.emit("bad")
        return

    # Fill all apps list
    self.FillAllAppsList_signal.emit(self.soft_list)

    # Connect to Vulners api via his lib
    if ConnectVulnersSoft(self):
        self.stat_signal.emit("bad")
        return

    # Sending pieces of software list to Vulners api via his lib
    if SendAppsVulners(self):
        self.stat_signal.emit("bad")
        return

    # Transorm to result format
    if ProcessAppsResponse(self):
        self.stat_signal.emit("bad")
        return

    self.ReportApps_signal.emit(self.apps_report)
    self.stat_signal.emit("good")


def GetLocalPorts(self):
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        self.LocalPorts = PortScan(ip_str=local_ip, port_str=self.port_range,
                                   thread_num=self.port_workers, show_refused=False,
                                   wait_time=2, stop_after_count=True).run()

        self.FillLocalPorts_signal.emit(self.LocalPorts)

        self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetLocalPorts : {e}")
        self.stat_signal.emit("bad")


def GetExtPorts(self):
    try:

        ext_ip = httpx.get(url="https://api.ipify.org", timeout=5).content.decode('utf8')
        self.ExtPorts = PortScan(ip_str=ext_ip, port_str=self.port_range,
                                 thread_num=self.port_workers, show_refused=False,
                                 wait_time=3, stop_after_count=True).run()

        self.FillExtPorts_signal.emit(self.ExtPorts)
        self.stat_signal.emit("good")
    except Exception as e:
        self.logger.error(f"GetExtPorts : {e}")
        self.stat_signal.emit("bad")


def GetDrivers(self):
    try:
        # getting drivers
        for driver in [f for f in listdir(r"c:\windows\system32\drivers") if isfile(join(r"c:\windows\system32\drivers", f))]:
            self.drivers_list.append(driver)

        self.logger.debug(f"GetDrivers : {len(self.drivers_list)} drivers")

        # check for zero list length
        if len(self.drivers_list) == 0:
            self.stat_signal.emit("bad")
            return True

        self.stat_signal.emit("good")
        return False
    except Exception as e:
        self.logger.error(f"GetDrivers : {e}")
        self.stat_signal.emit("bad")
        return True


def HashDrivers(self):
    try:
        for driver in self.drivers_list:
            # [sha256, sha1]
            drivers_path = r"c:\windows\system32\drivers"
            with open(f"{drivers_path}\\{driver}", "rb") as f:
                self.drivers_list_hashed.append([hashlib.sha256(f.read()).hexdigest(), hashlib.sha1(f.read()).hexdigest()])
        self.stat_signal.emit("good")
        return False
    except Exception as e:
        self.logger.error(f"HashDrivers : {e}")
        self.stat_signal.emit("bad")
        return True


def GetDriversDB(self):
    try:
        self.driver_db = httpx.get("https://www.loldrivers.io/api/drivers.json", timeout=10).json()
        self.logger.debug(f"GetDriversDB : {len(self.driver_db)} drivers in database")

        if len(self.driver_db) == 0:
            self.stat_signal.emit("bad")
            return True

        self.stat_signal.emit("good")
        return False

    except Exception as e:
        self.logger.error(f"GetDriversDB : {e}")
        self.stat_signal.emit("bad")
        return True


def ScanDrivers(self):
    try:
        with cf.ThreadPoolExecutor(max_workers=self.data_workers) as executor:
            futures = []
            for drv_hash in self.drivers_list_hashed:
                futures.append(executor.submit(ProcessDriver, self=self, drv_hash=drv_hash))
            executor.shutdown(wait=True, cancel_futures=False)

        self.stat_signal.emit("good")
        return False
    except Exception as e:
        self.logger.error(f"ScanDrivers : {e}")
        self.stat_signal.emit("bad")
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
        self.stat_signal.emit("bad")
        return

    self.FillDriversList_signal.emit(self.drivers_list)

    if HashDrivers(self):
        self.stat_signal.emit("bad")
        return

    if GetDriversDB(self):
        self.stat_signal.emit("bad")
        return

    if ScanDrivers(self):
        self.stat_signal.emit("bad")
        return

    self.drivers_report = {"driver_list": self.drivers_vuln_list}

    self.ReportDrivers_signal.emit(self.drivers_report)


def ConnectVulnersKB(self):
    try:
        self.vulners_api_kb = vulners.VulnersApi(api_key=self.vulners_key)
        self.stat_signal.emit("good")
        return False
    except Exception as e:
        self.logger.error(f"ConnectVulnersKB : {e}")
        self.stat_signal.emit("bad")
        return True


def GetKB(self):
    try:
        self.kb_list = updates.get_windows_updates(filter_duplicates=True)
        self.logger.debug(f"GetKB : {len(self.kb_list)} KB")
        if len(self.kb_list) == 0:
            self.stat_signal.emit("bad")
            return True

        self.stat_signal.emit("good")
        return False
    except Exception as e:
        self.logger.error(f"ConnectVulnersKB : {e}")
        self.stat_signal.emit("bad")
        return True


def SendKBVulners(self):
    try:
        # List with deleted KBs without KB ID
        kb = [item['kb'] for item in self.kb_list if item['kb'] not in ("", None) and "KB" in item['kb']]
        if len(kb) > 500:
            for chunk in CutListByChunks(self, kb, 500):
                self.kb_scan_res.update(self.vulners_api_kb.kb_audit(os=f"{platform.system()} {platform.release()}", kb_list=chunk))
        else:
            self.kb_scan_res = self.vulners_api_kb.kb_audit(os=f"{platform.system()} {platform.release()}", kb_list=kb)
        self.stat_signal.emit("good")
        return False
    except Exception as e:
        self.logger.error(f"SendKBVulners : {e}")
        self.stat_signal.emit("bad")
        return True


def ProcessKBResponse(self):
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
        self.stat_signal.emit("bad")
        return True

    # Getting more info about CVEs
    if len(self.kb_report["cve_list"]) > 0:
        try:
            with cf.ThreadPoolExecutor(max_workers=self.net_threads) as executor:
                futures = []
                for item in self.kb_report["cve_list"]:
                    futures.append(executor.submit(self.GetCveInfo, self, item))
                executor.shutdown(wait=True, cancel_futures=False)
        except Exception as e:
            self.logger.error(f"ProcessKBResponse : Failed to Getting more info about CVEs : {e}")
            self.stat_signal.emit("bad")
            return True

    self.stat_signal.emit("good")
    return False


def CheckKB(self):
    # Another API connection call is needed to ensure that the API wrapper is received at the right time

    if ConnectVulnersKB(self):
        self.stat_signal.emit("bad")
        return

    if GetKB(self):
        self.stat_signal.emit("bad")
        return

    self.FillKBList_signal.emit(self.kb_list)

    if SendKBVulners(self):
        self.stat_signal.emit("bad")
        return

    if ProcessKBResponse(self):
        self.stat_signal.emit("bad")
        return

    self.stat_signal.emit("good")
    self.ReportKB_signal.emit(self.kb_report)


def LoadShodanReport(self):
    try:
        ip = httpx.get(url="https://api.ipify.org", timeout=5).content.decode('utf8')
        self.ui.WebWidget.load(QUrl(f"https://www.shodan.io/host/{ip}"))
        self.logger.debug("LoadShodanReport : loaded")
        UpdateWorkPageStat(self, "good")
    except Exception as e:
        self.logger.error(f"LoadShodanReport : {e}")
        UpdateWorkPageStat(self, "bad")
