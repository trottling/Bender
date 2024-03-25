from PyQt6.QtGui import QPixmap

from ui.animations import ChangeWorkElems
from ui.show_report import *


def ConnectScannerSignals(self):
    self.scanner.finish_signal.connect(lambda: ChangeWorkElems(self))
    self.scanner.stat_signal.connect(lambda res: UpdateWorkPageStat(self, res))
    self.scanner.label_System_image_setStyleSheet_signal.connect(lambda item: self.ui.label_System_image.setPixmap(QPixmap(GetRelPath(self, r"assets\\images\\" + item))))
    self.scanner.label_System_name_setText_signal.connect(lambda item: self.ui.label_System_name.setText(item))
    self.scanner.label_System_ver_setText_signal.connect(lambda item: self.ui.label_System_ver.setText(item))
    self.scanner.label_Hardware_cpu_setText_signal.connect(lambda item: self.ui.label_Hardware_cpu.setText(item))
    self.scanner.label_Hardware_gpu_setText_signal.connect(lambda item: self.ui.label_Hardware_gpu.setText(item))
    self.scanner.label_Hardware_ram_setText_signal.connect(lambda item: self.ui.label_Hardware_ram.setText(item))
    self.scanner.label_Hardware_rom_setText_signal.connect(lambda item: self.ui.label_Hardware_rom.setText(item))
    self.scanner.label_Network_rules_setText_signal.connect(lambda item: self.ui.label_Network_rules.setText(item))
    self.scanner.label_network_mac_setText_signal.connect(lambda item: self.ui.label_network_mac.setText(item))
    self.scanner.label_Network_local_ip_setText_signal.connect(lambda item: self.ui.label_Network_local_ip.setText(item))
    self.scanner.label_Network_ext_ip_setText_signal.connect(lambda item: self.ui.label_Network_ext_ip.setText(item))
    self.scanner.frame_sys_bitness_setStyleSheet_signal.connect(lambda item: self.ui.frame_sys_bitness.setPixmap(QPixmap(GetRelPath(self, item))))
    self.scanner.label_sys_bitness_setText_signal.connect(lambda item: self.ui.label_sys_bitness.setText(item))
    self.scanner.label_sys_bitlocker_setText_signal.connect(lambda item: self.ui.label_sys_bitlocker.setText(item))
    self.scanner.label_sys_virt_setText_signal.connect(lambda item: self.ui.label_sys_virt.setText(item))
    self.scanner.FillAllAppsList_signal.connect(lambda item: FillAllAppsList(self, item))
    self.scanner.ReportApps_signal.connect(lambda item: ReportApps(self, item))
    self.scanner.FillLocalPorts_signal.connect(lambda item: FillLocalPorts(self, item))
    self.scanner.FillExtPorts_signal.connect(lambda item: FillExtPorts(self, item))
    self.scanner.FillDriversList_signal.connect(lambda item: FillDriversList(self, item))
    self.scanner.ReportDrivers_signal.connect(lambda item: ReportDrivers(self, item))
    self.scanner.FillKBList_signal.connect(lambda data_inst, data_miss: FillKBList(self, data_inst, data_miss))
    self.scanner.ReportKB_signal.connect(lambda item: ReportKB(self, item))
    self.scanner.UpdateWorkPageStat_signal.connect(lambda item: UpdateWorkPageStat(self, item))
