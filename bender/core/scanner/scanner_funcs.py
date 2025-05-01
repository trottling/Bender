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
from getmac import get_mac_address
from portscan import PortScan
from windows_tools import windows_firewall, bitness, bitlocker, logical_disks, updates
from windows_tools.installed_software import get_installed_software
from loguru import logger


def get_win_icon(self):
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
        logger.error(f"GetWinIcon: {e}")
        self.stat_signal.emit("bad")


def get_win_versions(self):
    try:
        self.label_System_name_setText_signal.emit(f"{platform.system()} {platform.release()}")
        self.label_System_ver_setText_signal.emit(platform.version())
        self.stat_signal.emit("good")
    except Exception as e:
        logger.error(f"GetWinVersions: {e}")
        self.stat_signal.emit("bad")


def get_cpu(self):
    try:
        self.label_Hardware_cpu_setText_signal.emit(cpuinfo.get_cpu_info()['brand_raw'])
        self.stat_signal.emit("good")
    except Exception as e:
        logger.error(f"GetCpu: {e}")
        self.stat_signal.emit("bad")


def get_gpu(self):
    try:
        self.label_Hardware_gpu_setText_signal.emit(str(wmi.WMI().Win32_VideoController()[0].wmi_property('Name').value))
        self.stat_signal.emit("good")
    except Exception as e:
        logger.error(f"GetGpu: {e}")
        self.stat_signal.emit("bad")


def get_ram(self):
    try:
        self.label_Hardware_ram_setText_signal.emit(f"{round(psutil.virtual_memory().total / 1073741824)} Gb RAM")
        self.stat_signal.emit("good")
    except Exception as e:
        logger.error(f"GetRam: {e}")
        self.stat_signal.emit("bad")


def get_rom(self):
    try:
        space = 0.0
        for drive in logical_disks.get_logical_disks():
            total, _, _ = shutil.disk_usage(drive)
            space += total
        self.label_Hardware_rom_setText_signal.emit(f"{space // (2 ** 30)} Gb ROM")
        self.stat_signal.emit("good")
    except Exception as e:
        logger.error(f"GetRom: {e}")
        self.stat_signal.emit("bad")


def get_firewall(self):
    try:
        if windows_firewall.is_firewall_active():
            fwlen = len(subprocess.run(["powershell", "Get-NetFirewallRule"], capture_output=True, text=True, startupinfo=self.si).stdout.split("\n\n"))
            self.label_Network_rules_setText_signal.emit(f"{fwlen} Firewall rules" if fwlen > 0 else "Firewall Active")
        else:
            self.label_Network_rules_setText_signal.emit("Firewall Inactive")
            self.stat_signal.emit("good")
    except Exception as e:
        logger.error(f"GetFirewall: {e}")
        self.stat_signal.emit("bad")


def get_mac(self):
    try:
        self.label_network_mac_setText_signal.emit(f"{str(get_mac_address())} - Mac adress")
        self.stat_signal.emit("good")
    except Exception as e:
        logger.error(f"GetMac: {e}")
        self.stat_signal.emit("bad")


def get_local_ip(self):
    try:
        self.label_Network_local_ip_setText_signal.emit(f"{socket.gethostbyname(socket.gethostname())} - Local IP")
        self.stat_signal.emit("good")
    except Exception as e:
        logger.error(f"GetLocalIP: {e}")
        self.stat_signal.emit("bad")


def get_ext_ip(self):
    try:
        self.label_Network_ext_ip_setText_signal.emit(f"{httpx.get(url="https://api.ipify.org", timeout=5).content.decode('utf8')} - External IP")
        self.stat_signal.emit("good")
    except Exception as e:
        logger.error(f"GetExtIP: {e}")
        self.stat_signal.emit("bad")


def get_bitness(self):
    try:
        if bitness.is_64bit():
            self.frame_sys_bitness_setStyleSheet_signal.emit('assets//images//64-bit.png')
            self.label_sys_bitness_setText_signal.emit(f"64 Bit Bitness")
        else:
            self.frame_sys_bitness_setStyleSheet_signal.emit('assets//images//32-bit.png')
            self.label_sys_bitness_setText_signal.emit(f"32 Bit Bitness")
        self.stat_signal.emit("good")
    except Exception as e:
        logger.error(f"GetBitness: {e}")
        self.stat_signal.emit("bad")


def get_bitlocker(self):
    try:
        drives_list = []
        if bitlocker.check_bitlocker_management_tools():
            for drive in logical_disks.get_logical_disks():
                for line in subprocess.check_output(['manage-bde', '-status', drive], startupinfo=self.si).decode(encoding='utf-8', errors='ignore').splitlines():
                    if 'AES' in line or 'XEX' in line:
                        drives_list.append(drive)
                        break
            if len(drives_list) != 0:
                text = ", ".join([i.replace(":", "") for i in list(set(drives_list))])
                self.label_sys_bitlocker_setText_signal.emit(f"Bitlocker Enabled - {'Disks' if len(drives_list) > 1 else 'Disk'} {text}")
            else:
                self.label_sys_bitlocker_setText_signal.emit(f"Bitlocker Disabled")
        else:
            self.label_sys_bitlocker_setText_signal.emit(["self.ui.label_sys_bitlocker.setText", f"Bitlocker Tools not found"])
        self.stat_signal.emit("good")
    except Exception as e:
        logger.error(f"GetBitlocker: {e}")
        self.stat_signal.emit("bad")


def get_virtualization(self):
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
        logger.error(f"GetVirtualization: {e}")
        self.stat_signal.emit("bad")


def get_apps(self):
    try:
        for software in get_installed_software():
            if software['name'] != "" and software['version'] != "":
                self.soft_list.append(software)
        logger.info(f"GetApps: found {len(self.soft_list)} applications")
        if len(self.soft_list) > 0:
            self.stat_signal.emit("good")
            return False
        else:
            logger.warning("GetApps: application list is empty")
            self.stat_signal.emit("bad")
            return True
    except Exception as e:
        logger.error(f"GetApps: {e}")
        self.stat_signal.emit("bad")
        return True


def connect_vulners_soft(self):
    try:
        self.vulners_api_soft = vulners.VulnersApi(api_key=self.vulners_key)
        self.stat_signal.emit("good")
        return False
    except Exception as e:
        logger.error(f"ConnectVulnersSoft: {e}")
        self.stat_signal.emit("bad")
        return True


def cut_list_by_chunks(self, lst, chunk_max):
    # Делит список на чанки по chunk_max элементов
    res = [lst[i:i + chunk_max] for i in range(0, len(lst), chunk_max)]
    logger.debug(f"CutListByChunks: {len(lst)} items / {chunk_max} chunk size --> {len(res)} chunks")
    return res


def send_apps_vulners(self):
    try:
        if len(self.soft_list) > 500:
            self.soft_list = self.soft_list[:500]
        self.apps_report = self.vulners_api_soft.software_audit(os="", version="", packages=[{ "software": software['name'], "version": software['version'] } for software in self.soft_list])
        self.stat_signal.emit("good")
        return False
    except Exception as e:
        logger.error(f"SendAppsVulners: Failed to get vulners.com report: {e}")
        self.stat_signal.emit("bad")
        return True


def process_apps_response(self):
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
        self.apps_report = { "cve_list": self.cve_list_apps }
    except Exception as e:
        logger.error(f"ProcessAppsResponse: Failed to transorm to needed format: {e}")
        self.stat_signal.emit("bad")
        return True

    # Getting more info about CVEs
    if len(self.apps_report["cve_list"]) > 0:
        try:
            with cf.ThreadPoolExecutor(max_workers=self.net_threads) as executor:
                futures = []
                for item in self.apps_report["cve_list"]:
                    futures.append(executor.submit(get_cve_info, self=self, item=item))
                executor.shutdown(wait=True, cancel_futures=False)
        except Exception as e:
            logger.error(f"ProcessAppsResponse: Failed to Getting more info about CVEs: {e}")
            self.stat_signal.emit("bad")
            return True

    self.stat_signal.emit("good")
    return False


def get_cve_info(self, item):
    cve_id = item["cve"]
    logger.debug(f"GetCveInfo: Processing {cve_id}")

    try:
        self.mitre_resp = httpx.get(f"https://cveawg.mitre.org/api/cve/{cve_id}", timeout=10).json()
    except Exception as e:
        logger.error(f"GetCveInfo: {cve_id}: {e}")

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


def check_apps(self):
    if get_apps(self):
        self.stat_signal.emit("bad")
        return

    # Fill all app lists
    self.FillAllAppsList_signal.emit(self.soft_list)

    # Connect to Vulners api via his lib
    if connect_vulners_soft(self):
        self.stat_signal.emit("bad")
        return

    # Sending pieces of a software list to Vulners api via his lib
    if send_apps_vulners(self):
        self.stat_signal.emit("bad")
        return

    # Transorm to result format
    if process_apps_response(self):
        self.stat_signal.emit("bad")
        return

    self.ReportApps_signal.emit(self.apps_report)
    self.stat_signal.emit("good")


def get_local_ports(self):
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        self.LocalPorts = PortScan(ip_str=local_ip, port_str="1-1000",
                                   thread_num=self.port_workers, show_refused=False,
                                   wait_time=2, stop_after_count=True).run()

        self.FillLocalPorts_signal.emit(self.LocalPorts)

        self.stat_signal.emit("good")
    except Exception as e:
        logger.error(f"GetLocalPorts: {e}")
        self.stat_signal.emit("bad")


def get_ext_ports(self):
    try:
        ext_ip = httpx.get(url="https://api.ipify.org", timeout=5).content.decode('utf8')
        self.ExtPorts = PortScan(ip_str=ext_ip, port_str="1-1000",
                                 thread_num=self.port_workers, show_refused=False,
                                 wait_time=3, stop_after_count=True).run()

        self.FillExtPorts_signal.emit(self.ExtPorts)
        self.stat_signal.emit("good")
    except Exception as e:
        logger.error(f"GetExtPorts: {e}")
        self.stat_signal.emit("bad")


def get_drivers(self):
    try:
        for driver in [f for f in listdir(r"c:\windows\system32\drivers") if isfile(join(r"c:\windows\system32\drivers", f))]:
            self.drivers_list.append(driver)
        logger.info(f"GetDrivers: found {len(self.drivers_list)} drivers")
        if len(self.drivers_list) == 0:
            logger.warning("GetDrivers: driver list is empty")
            self.stat_signal.emit("bad")
            return True
        self.stat_signal.emit("good")
        return False
    except Exception as e:
        logger.error(f"GetDrivers: {e}")
        self.stat_signal.emit("bad")
        return True


def hash_drivers(self):
    try:
        for driver in self.drivers_list:
            drivers_path = r"c:\windows\system32\drivers"
            file_path = f"{drivers_path}\\{driver}"
            with open(file_path, "rb") as f:
                data = f.read()
                self.drivers_list_hashed.append([
                    hashlib.sha256(data).hexdigest(),
                    hashlib.sha1(data).hexdigest()
                    ])
        self.stat_signal.emit("good")
        return False
    except Exception as e:
        logger.error(f"HashDrivers: {e}")
        self.stat_signal.emit("bad")
        return True


def get_drivers_db(self):
    try:
        self.driver_db = httpx.get("https://www.loldrivers.io/api/drivers.json", timeout=10).json()
        logger.info(f"GetDriversDB: received {len(self.driver_db)} drivers from database")
        if len(self.driver_db) == 0:
            logger.warning("GetDriversDB: database is empty")
            self.stat_signal.emit("bad")
            return True
        self.stat_signal.emit("good")
        return False
    except Exception as e:
        logger.error(f"GetDriversDB: {e}")
        self.stat_signal.emit("bad")
        return True


def scan_drivers(self):
    try:
        with cf.ThreadPoolExecutor(max_workers=self.data_workers) as executor:
            futures = []
            for drv_hash in self.drivers_list_hashed:
                futures.append(executor.submit(process_driver, self=self, drv_hash=drv_hash))
            executor.shutdown(wait=True, cancel_futures=False)

        self.stat_signal.emit("good")
        return False
    except Exception as e:
        logger.error(f"ScanDrivers: {e}")
        self.stat_signal.emit("bad")
        return True


def recursive_save_dict(self, source_dict, target_dict, prefix = ""):
    for key, value in source_dict.items():
        if isinstance(value, dict):
            recursive_save_dict(self, value, target_dict, prefix + key + ".")
        else:
            target_dict[prefix + key] = value


def process_driver(self, drv_hash):
    for date in self.driver_db:
        for item in date["KnownVulnerableSamples"]:
            if 'SHA256' in item and drv_hash[0] == item['SHA256'] or 'SHA1' in item and drv_hash[1] == item['SHA1']:

                try:
                    short_name = item["Filename"]
                except KeyError:
                    try:
                        short_name = item["OriginalFilename"]
                    except KeyError:
                        short_name = "Unknown Short Name"

                try:
                    version = item["FileVersion"]
                except KeyError:
                    version = "No File Version"

                try:
                    date_published = item["CreationTimestamp"]
                except KeyError:
                    date_published = "No Date Published"

                try:
                    company = item["company"]
                except KeyError:
                    company = "No company"

                try:
                    desc = item["Description"]
                except KeyError:
                    desc = "No Description"

                try:
                    product = item["product"]
                except KeyError:
                    product = "No product"

                try:
                    item_copyright = item["copyright"]
                except KeyError:
                    item_copyright = "No copyright"

                try:
                    imported_functions = item["imported_functions"]
                except KeyError:
                    imported_functions = ["No Imported Functions"]

                try:
                    drhash = f"SHA256 : {item['SHA256']}"
                except KeyError:
                    drhash = f"SHA1 : {item['SHA1']}"

                vuln_driver_data = {
                    "short_name": short_name,
                    "version": version,
                    "date_published": date_published,
                    "desc": f"{company} : {desc} : {product} : {item_copyright}",
                    "imported_functions": imported_functions,
                    "hash": drhash
                    }
                recursive_save_dict(self, date, vuln_driver_data)
                self.drivers_vuln_list.append(vuln_driver_data)


def check_drivers(self):
    if get_drivers(self):
        self.stat_signal.emit("bad")
        return

    self.FillDriversList_signal.emit(self.drivers_list)

    if hash_drivers(self):
        self.stat_signal.emit("bad")
        return

    if get_drivers_db(self):
        self.stat_signal.emit("bad")
        return

    if scan_drivers(self):
        self.stat_signal.emit("bad")
        return

    self.drivers_report = { "driver_list": self.drivers_vuln_list }
    self.ReportDrivers_signal.emit(self.drivers_report)
    self.stat_signal.emit("good")


def connect_vulners_kb(self):
    try:
        self.vulners_api_kb = vulners.VulnersApi(api_key=self.vulners_key)
        self.stat_signal.emit("good")
        return False
    except Exception as e:
        logger.error(f"ConnectVulnersKB: {e}")
        self.stat_signal.emit("bad")
        return True


def get_kb(self):
    try:
        self.kb_list = updates.get_windows_updates(filter_duplicates=True)
        logger.debug(f"GetKB: {len(self.kb_list)} KB")
        if len(self.kb_list) == 0:
            self.stat_signal.emit("bad")
            return True

        self.stat_signal.emit("good")
        return False
    except Exception as e:
        logger.error(f"ConnectVulnersKB: {e}")
        self.stat_signal.emit("bad")
        return True


def send_kb_vulners(self):
    try:
        # List with deleted KBs without KB ID
        kb = [item['kb'] for item in self.kb_list if item['kb'] not in ("", None) and "KB" in item['kb']]
        if len(kb) > 500:
            kb = kb[:500]
        self.kb_scan_res = self.vulners_api_kb.kb_audit(os=f"{platform.system()} {platform.release()}", kb_list=kb)
        self.stat_signal.emit("good")
        return False
    except Exception as e:
        logger.error(f"SendKBVulners: {e}")
        self.stat_signal.emit("bad")
        return True


def process_kb_response(self):
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
        self.kb_report = { "cve_list": self.cve_list_kb }
    except Exception as e:
        logger.error(f"ProcessKBResponse: Failed to transorm to needed format: {e}")
        self.stat_signal.emit("bad")
        return True

    # Getting more info about CVEs
    if len(self.kb_report["cve_list"]) > 0:
        try:
            with cf.ThreadPoolExecutor(max_workers=self.net_threads) as executor:
                futures = []
                for item in self.kb_report["cve_list"]:
                    futures.append(executor.submit(get_cve_info, self, item))
                executor.shutdown(wait=True, cancel_futures=False)
        except Exception as e:
            logger.error(f"ProcessKBResponse: Failed to Getting more info about CVEs: {e}")
            self.stat_signal.emit("bad")
            return True

    self.stat_signal.emit("good")
    return False


def check_kb(self):
    # Another API connection call is needed to ensure that the API wrapper is received at the right time

    if connect_vulners_kb(self):
        self.stat_signal.emit("bad")
        return

    if get_kb(self):
        self.stat_signal.emit("bad")
        return

    if send_kb_vulners(self):
        self.stat_signal.emit("bad")
        return

    self.FillKBList_signal.emit(self.kb_list, self.kb_scan_res)

    if process_kb_response(self):
        self.stat_signal.emit("bad")
        return

    self.stat_signal.emit("good")
    self.ReportKB_signal.emit(self.kb_report)
