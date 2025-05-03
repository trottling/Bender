from datetime import datetime

from PyQt6.QtCore import QThread, pyqtSignal

from bender.core.scanner.scanner_funcs import *


class Scanner(QThread):
    log_signal = pyqtSignal(str)
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

    def __init__(self, net_threads, data_workers, port_workers, vulners_key):
        super().__init__(parent=None)
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
        
        self.scan_tasks = [
            (check_apps, "Проверка приложений"),
            (check_drivers, "Проверка драйверов"),
            (check_kb, "Проверка обновлений Windows"),
            (get_local_ports, "Сканирование локальных портов"),
            (get_ext_ports, "Сканирование внешних портов"),
            (get_win_icon, "Получение информации о системе"),
            (get_win_versions, "Определение версии Windows"),
            (get_cpu, "Получение информации о процессоре"),
            (get_gpu, "Получение информации о видеокарте"),
            (get_ram, "Проверка оперативной памяти"),
            (get_rom, "Проверка жестких дисков"),
            (get_firewall, "Проверка брандмауэра"),
            (get_mac, "Получение MAC-адреса"),
            (get_local_ip, "Получение локального IP"),
            (get_ext_ip, "Получение внешнего IP"),
            (get_bitness, "Определение разрядности системы"),
            (get_bitlocker, "Проверка BitLocker"),
            (get_virtualization, "Проверка виртуализации")
        ]
    
    def log_message(self, message, emoji=""):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {emoji} {message}"
        self.log_signal.emit(formatted_message)
        logger.info(f"Scanner: log message: {formatted_message}")
    
    def run(self):
        self.log_message("Начало сканирования системы", "🚀")
        
        with cf.ThreadPoolExecutor(max_workers=len(self.scan_tasks)) as executor:
            futures = []
            for task, description in self.scan_tasks:
                self.log_message(f"Запуск: {description}", "🔍")
                futures.append(executor.submit(task, self))
                        
            executor.shutdown(wait=True)
        
        self.log_message("Сканирование успешно завершено", "🎉")
        self.finish_signal.emit()
        self.stop()

    def stop(self):
        logger.debug("ScanThread: Thread stopped")
        self.quit()