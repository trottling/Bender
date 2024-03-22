from PyQt6.QtCore import QThread, pyqtSignal

from tasks.scanner_funcs import *


class Scanner(QThread):
    stat_signal = pyqtSignal(str)
    finish_signal = pyqtSignal()
    label_System_image_setStyleSheet_signal = pyqtSignal(str)
    label_System_name_setText_signal = pyqtSignal(str)
    label_System_ver_setText_signal = pyqtSignal(str)
    label_Hardware_cpu_setText_signal = pyqtSignal(str)
    label_Hardware_gpu_setText_signal = pyqtSignal(str)
    label_Hardware_ram_setText_signal = pyqtSignal(str)
    label_Hardware_rom_setText_signal = pyqtSignal(str)
    label_Network_rules_setText_signal = pyqtSignal(str)
    label_network_mac_setText_signal = pyqtSignal(str)
    label_Network_local_ip_setText_signal = pyqtSignal(str)
    label_Network_ext_ip_setText_signal = pyqtSignal(str)
    frame_sys_bitness_setStyleSheet_signal = pyqtSignal(str)
    label_sys_bitness_setText_signal = pyqtSignal(str)
    label_sys_bitlocker_setText_signal = pyqtSignal(str)
    label_sys_virt_setText_signal = pyqtSignal(str)
    FillAllAppsList_signal = pyqtSignal(list)
    ReportApps_signal = pyqtSignal(dict)
    FillLocalPorts_signal = pyqtSignal(list)
    FillExtPorts_signal = pyqtSignal(list)
    FillDriversList_signal = pyqtSignal(list)
    ReportDrivers_signal = pyqtSignal(dict)
    FillKBList_signal = pyqtSignal((list, dict))
    ReportKB_signal = pyqtSignal(dict)
    UpdateWorkPageStat_signal = pyqtSignal(str)

    def __init__(self, logger, net_threads, data_workers, port_workers, vulners_key):
        super().__init__(parent=None)

        self.logger = logger
        self.net_threads = net_threads
        self.data_workers = data_workers
        self.port_workers = port_workers
        self.vulners_key = vulners_key

        # Hide console at calling
        self.si = subprocess.STARTUPINFO()
        self.si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.si.wShowWindow = subprocess.SW_HIDE

        self.kb_list = []
        self.kb_scan_res = {}
        self.kb_report = {}
        self.drivers_vuln_list = []
        self.drivers_list = []
        self.drivers_list_hashed = []
        self.soft_list = []
        self.apps_report = {}
        self.cve_list_kb = []
        self.scan_thread = None
        self.scan_tasks_list = [CheckApps, CheckApps, CheckDrivers, CheckKB, GetLocalPorts,
                                GetExtPorts, GetWinIcon, GetWinVersions, GetCpu,
                                GetGpu, GetRam, GetRom, GetFirewall,
                                GetMac, GetLocalIP, GetExtIP, GetBitness,
                                GetBitlocker, GetVirtualization]

    def run(self):
        # Run funcs
        with cf.ThreadPoolExecutor(max_workers=len(self.scan_tasks_list)) as self.sc_pool:
            [self.sc_pool.submit(task, self) for task in self.scan_tasks_list]
            self.sc_pool.shutdown(wait=True, cancel_futures=False)
        self.finish_signal.emit()
        self.stop()

    def stop(self):
        self.logger.debug("ScanThread : Thread stoped")
        self.quit()
