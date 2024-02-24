import hashlib
import json
from os import listdir
from os.path import isfile, join

import httpx


def RunCCD(self):
    self.drivers_list = []
    self.drivers_list_hashed = []  # Sha256 hash
    self.drivers_path = r"c:\windows\system32\drivers"
    self.report = None

    self.logger.debug("RunCCD : Started")
    self.log_signal.emit("Check drivers started..." + "\n")

    #
    # getting drivers
    #

    try:
        for driver in [f for f in listdir(self.drivers_path) if isfile(join(self.drivers_path, f))]:
            self.drivers_list.append(driver)
    except Exception as e:
        self.err_signal.emit("RunCCD : Error getting installed apps : " + str(e))

    #
    # check for zero list length
    #

    if len(self.drivers_list) == 0:
        self.err_signal.emit("ERROR : Could not find any driver to check")

    #
    #  log info
    #

    self.logger.debug(f"RunCCD : Driver list : {len(self.drivers_list)} softwares")
    self.log_signal.emit(f"Found {len(self.drivers_list)} drivers\n")
    self.pbar_signal.emit(15)

    #
    #  hash drivers name
    #
    self.drivers_list_hashed.append(["3a95cc82173032b82a0ffc7d2e438df64c13bc16b4574214c9fe3be37250925e", ""])
    self.log_signal.emit(f"Hashing drivers\n")
    self.logger.debug(f"RunCCD : Hashing drivers")
    for driver in self.drivers_list:
        with open(f"{self.drivers_path}\\{driver}", "rb") as f:
            self.drivers_list_hashed.append([hashlib.sha256(f.read()).hexdigest(), hashlib.sha1(f.read()).hexdigest()])
    self.pbar_signal.emit(30)

    #
    #  loading loldrivers.io database
    #

    self.log_signal.emit(f"Loading loldrivers.io database\n")
    try:
        self.driver_db = httpx.get("https://www.loldrivers.io/api/drivers.json", timeout=10).json()
    except Exception as e:
        self.err_signal.emit("RunCCD : Failed to loading loldrivers.io database : " + str(e))
        return
    self.pbar_signal.emit(50)

    #
    #  log info
    #

    self.log_signal.emit(f"{len(self.driver_db)} drivers in database\n")
    self.logger.debug(f"RunCCD : {len(self.driver_db)} drivers in database")

    #
    #  Inspection drivers in database and add to report
    #

    self.log_signal.emit(f"Inspection drivers in database\n")
    vuln_list = []
    for drv_hash in self.drivers_list_hashed:
        for date in self.driver_db:
            for item in date["KnownVulnerableSamples"]:
                if 'SHA256' in item and drv_hash[0] == item['SHA256'] or 'SHA1' in item and drv_hash[1] == item['SHA1']:
                    vuln_driver_data = {
                        "shortName": item["Filename"] if "Filename" in item else item["OriginalFilename"],
                        "version": item["FileVersion"] if "FileVersion" in item and item[
                            "FileVersion"].strip() != "" else "No File Version",
                        "datePublished": item[
                            "CreationTimestamp"] if "CreationTimestamp" in item else "No Date Published",
                        "desc": f"{item["Company"] if "Company" in item and item["Company"].strip() != "" else "No Company"} : {item["Description"] if "Description" in item and item["Description"].strip() != "" else "No Description"} : {item["Product"] if "Description" in item and item["Product"].strip() != "" else "No Product"} : {item["Copyright"] if "Copyright" in item else "No Copyright"}",
                        "ImportedFunctions": item[
                            "ImportedFunctions"] if "ImportedFunctions" in item else ["No Imported Functions"],
                        "hash": f"SHA256 : {item['SHA256']}" if 'SHA256' in item else f"SHA1 : {item['SHA1']}",
                    }
                    Recursive_save(self, date, vuln_driver_data)
                    vuln_list.append(vuln_driver_data)

    self.report = {"driver_list": vuln_list}

    #
    # Log results
    #

    self.log_signal.emit(
        f"Found {len(self.report["driver_list"])} vulnerable drivers\n")
    self.logger.debug(
        f"RunCCD : Found {len(self.report["driver_list"])} vulnerable drivers")
    self.pbar_signal.emit(75)

    #
    #  Done
    #

    self.log_signal.emit("Done : Click Next button to see scan results")
    self.logger.debug(f"RunCCD : Done")
    self.pbar_signal.emit(100)
    self.result_signal.emit(json.dumps(self.report))


def Recursive_save(self, source_dict, target_dict, prefix=""):
    for key, value in source_dict.items():
        if isinstance(value, dict):
            Recursive_save(self, value, target_dict, prefix + key + ".")
        else:
            target_dict[prefix + key] = value
