from PyQt6.QtGui import QPixmap
from bender.ui.animations import *
from bender.ui.show_report import *
from bender.ui.tools import get_rel_path


def connect_scanner_signals(self):
    # Connect finish signal
    self.scanner.finish_signal.connect(lambda: change_work_elems(self))
    
    # Connect log signal for progress updates
    self.scanner.log_signal.connect(lambda msg: textbrowser_append_anim(self, self.ui.scan_progress_textBrowser, msg))
    
    # Connect all UI update signals
    self.scanner.label_System_image_setStyleSheet_signal.connect(
        lambda item: self.ui.label_System_image.setPixmap(QPixmap(get_rel_path(self, r"assets\\images\\" + item))))
    self.scanner.label_System_name_setText_signal.connect(
        lambda item: self.ui.label_System_name.setText(item))
    self.scanner.label_System_ver_setText_signal.connect(
        lambda item: self.ui.label_System_ver.setText(item))
    self.scanner.label_Hardware_cpu_setText_signal.connect(
        lambda item: self.ui.label_Hardware_cpu.setText(item))
    self.scanner.label_Hardware_gpu_setText_signal.connect(
        lambda item: self.ui.label_Hardware_gpu.setText(item))
    self.scanner.label_Hardware_ram_setText_signal.connect(
        lambda item: self.ui.label_Hardware_ram.setText(item))
    self.scanner.label_Hardware_rom_setText_signal.connect(
        lambda item: self.ui.label_Hardware_rom.setText(item))
    self.scanner.label_Network_rules_setText_signal.connect(
        lambda item: self.ui.label_Network_rules.setText(item))
    self.scanner.label_network_mac_setText_signal.connect(
        lambda item: self.ui.label_network_mac.setText(item))
    self.scanner.label_Network_local_ip_setText_signal.connect(
        lambda item: self.ui.label_Network_local_ip.setText(item))
    self.scanner.label_Network_ext_ip_setText_signal.connect(
        lambda item: self.ui.label_Network_ext_ip.setText(item))
    self.scanner.frame_sys_bitness_setStyleSheet_signal.connect(
        lambda item: self.ui.frame_sys_bitness.setPixmap(QPixmap(get_rel_path(self, item))))
    self.scanner.label_sys_bitness_setText_signal.connect(
        lambda item: self.ui.label_sys_bitness.setText(item))
    self.scanner.label_sys_bitlocker_setText_signal.connect(
        lambda item: self.ui.label_sys_bitlocker.setText(item))
    self.scanner.label_sys_virt_setText_signal.connect(
        lambda item: self.ui.label_sys_virt.setText(item))
    
    # Connect data signals
    self.scanner.FillAllAppsList_signal.connect(
        lambda item: fill_all_apps_list(self, item))
    self.scanner.ReportApps_signal.connect(
        lambda item: report_apps(self, item))
    self.scanner.FillLocalPorts_signal.connect(
        lambda item: fill_local_ports(self, item))
    self.scanner.FillExtPorts_signal.connect(
        lambda item: fill_ext_ports(self, item))
    self.scanner.FillDriversList_signal.connect(
        lambda item: fill_drivers_list(self, item))
    self.scanner.ReportDrivers_signal.connect(
        lambda item: report_drivers(self, item))
    self.scanner.FillKBList_signal.connect(
        lambda data_inst, data_miss: fill_kb_list(self, data_inst, data_miss))
    self.scanner.ReportKB_signal.connect(
        lambda item: report_kb(self, item))
    
    # Auto-scroll text browser to bottom when new log message arrives
    self.scanner.log_signal.connect(
        lambda _: self.ui.scan_progress_textBrowser.verticalScrollBar().setValue(
            self.ui.scan_progress_textBrowser.verticalScrollBar().maximum()
        )
    )