import concurrent.futures
import json

import httpx
import vulners
from windows_tools.installed_software import get_installed_software


def RunCIA(self):
    self.raw_soft_list = []
    self.soft_list = []
    self.soft_list_vulners = []
    self.soft_list_vulmon = []
    self.report = None

    self.logger.debug(f"RunCIA : Started : Check by {self.db}")
    self.log_signal.emit("Check installed apps started..." + "\n")

    #
    # getting installed apps
    #

    try:
        for software in get_installed_software():
            if software['name'] != "" and software['version'] != "":
                self.soft_list.append(software)
    except Exception as e:
        self.err_signal.emit("RunCIA : Error getting installed apps : " + str(e))

    #
    # check for zero list length
    #

    if len(self.soft_list) == 0:
        self.err_signal.emit("ERROR : Could not find any software to check")

    self.logger.debug(f"RunCIA : Soft list : {len(self.soft_list)} softwares")
    self.log_signal.emit(f"Found {len(self.soft_list)} softwares\n")
    self.pbar_signal.emit(15)

    #
    # Check softwares by selected DB
    #

    match self.db:
        case "vulners.com (Recommended)":
            Check_By_Vulners(self)

    #
    # Getting more info about CVEs
    #

    if len(self.report["cve_list"]) == 0:
        self.log_signal.emit("No CVEs to getting more\n")
    else:
        self.log_signal.emit("Getting more info about CVEs\n")
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.net_threads) as executor:
                futures = []
                for item in self.report["cve_list"]:
                    futures.append(executor.submit(CIA_Get_CVE_Info, self=self, item=item))
                executor.shutdown(wait=True, cancel_futures=False)
        except Exception as e:
            self.err_signal.emit("RunCIA : Failed to Getting more info about CVEs : " + str(e))
            return

    #
    # Done
    #

    self.log_signal.emit("Done : Click Next button to see scan results")
    self.logger.debug(f"RunCIA : Done")
    self.pbar_signal.emit(100)
    self.result_signal.emit(json.dumps(self.report))


def Check_By_Vulners(self):
    if len(self.soft_list) > 500:
        self.soft_list = self.soft_list[:500]
        self.log_signal.emit(f"Software list is too bigger : {len(self.soft_list)} : Cut lenght to 500\n")
        self.logger.debug(f"Software list is too bigger : {len(self.soft_list)} : Cut lenght to 500\n")

    self.log_signal.emit(f"Transforming softwares list to vulners.com format\n")
    for software in self.soft_list:
        self.soft_list_vulners.append(dict({"software": software['name'], "version": software['version']}))

    self.pbar_signal.emit(30)

    self.log_signal.emit(f"Connecting to vulners.com API\n")
    try:
        self.vulners_api = vulners.VulnersApi(api_key=self.api_key)
        self.pbar_signal.emit(45)
    except Exception as e:
        self.err_signal.emit("RunCIA : Failed to connect Vulners Api : " + str(e))
        return

    self.log_signal.emit(f"Sending softwares list to vulners.com\n")
    try:
        self.report = self.vulners_api.software_audit(os="", version="", packages=self.soft_list_vulners)
        self.pbar_signal.emit(60)
    except Exception as e:
        self.err_signal.emit("RunCIA : Failed to get vulners.com report : " + str(e))
        return

    #
    # Log results
    #

    try:
        self.log_signal.emit(
            f"Found {len([vuln for vuln in self.report['vulnerabilities'] if vuln['id']])} CVEs\n")
        self.logger.debug(
            f"RunCIA : Found {len([vuln for vuln in self.report['vulnerabilities'] if vuln['id']])} CVEs : {self.report}")
        self.pbar_signal.emit(75)
    except Exception as e:
        self.err_signal.emit("RunCIA : Failed read vulners.com report : " + str(e))
        return

    #
    # Clear labels without CVE
    #

    self.report = [vuln for vuln in self.report['vulnerabilities'] if vuln['id']]
    self.logger.debug(f"RunCIA : Cleared labels without CVE : {self.report}")
    self.pbar_signal.emit(85)

    #
    # Transorm to result format
    #

    self.cve_list = []
    try:
        for item in self.report:
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
        self.report = {"cve_list": self.cve_list}
    except Exception as e:
        self.err_signal.emit("RunCIA : Failed to transorm to needed format : " + str(e))
        return

    self.logger.debug(f"RunCIA : Transormed to needed format : {self.report}")


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
        self.log_signal.emit(f"RunCIA : {cve_id} : Failed to get more info : {str(e)}")
        self.logger.error(f"RunCIA : {cve_id} : Failed to get more info : {str(e)}")
