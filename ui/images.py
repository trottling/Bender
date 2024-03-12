from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QMovie

from ui.tools import GetRelPath


def Load_Images_And_Icons(self):
    #
    # Logo
    #
    self.ui.logo.setStyleSheet(
        ".QFrame {border-image: url('" + GetRelPath(self, 'assets//images//bender.png') + "')}")
    self.ui.logo_2.setStyleSheet(
        ".QFrame {border-image: url('" + GetRelPath(self, 'assets//images//bender.png') + "')}")
    self.ui.git_frame.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//github.png') + "')}")

    self.logger.debug(f"Load_Images_And_Icons : Logos seted")

    # Set start page system data icons to processing GIF

    for elem in self.start_processing_elems:
        gif = QMovie(GetRelPath(self, r"assets\gifs\loading.gif"))
        gif.setFormat(b"gif")
        gif.setScaledSize(QtCore.QSize(22, 22))
        elem.setMovie(gif)
        gif.start()

    self.logger.debug(f"Load_Images_And_Icons : Loading GIF seted")

    #
    # Buttons icons
    #

    # Toolbar
    self.ui.pushButton_app_exit.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//exit.png') + "')}")
    self.ui.pushButton_app_size.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//resize.png') + "')}")
    self.ui.pushButton_app_hide.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//minimize.png') + "')}")
    self.ui.app_icon.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//bender-small.png') + "')}")

    #
    # Pages
    #

    # Start page
    self.ui.setting_btn.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//settings.png') + "')}")
    self.ui.info_btn.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//info.png') + "')}")
    self.ui.reload_btn.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//reload.png') + "')}")

    # Pbar page
    self.ui.next_work_btn.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//next.png') + "')}")
    self.ui.framel_scan_successful.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//apply.png') + "')}")
    self.ui.frame_scan_error.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//fail.png') + "')}")

    # Work result page
    self.ui.frame_Hardware_cpu.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//pc_cpu.png') + "')}")
    self.ui.frame_Hardware_gpu.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//gpu.png') + "')}")
    self.ui.frame_Hardware_ram.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//ram.png') + "')}")
    self.ui.frame_Hardware_rom.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//ssd.png') + "')}")
    self.ui.frame_net_firewall.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//firewall.png') + "')}")
    self.ui.frame_net_mac.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//mac.png') + "')}")
    self.ui.frame_net_local_ip.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//internal.png') + "')}")
    self.ui.frame_ext_local_ip.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//external.png') + "')}")
    self.ui.frame_sys_bitlocker.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//bitlocker.png') + "')}")
    self.ui.frame_sys_virt.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//virtualization.png') + "')}")
    self.ui.frame_sys_bitness.setStyleSheet(
        ".QFrame {image: url('" + GetRelPath(self, 'assets//images//help.png') + "')}")

    # Info page
    self.ui.info_back_button.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//back.png') + "')}")
    self.ui.pushButton_repo.setIcon(QtGui.QIcon(GetRelPath(self, r"assets\images\trottling.png")))
    self.ui.pushButton_repo.setIconSize(QtCore.QSize(40, 40))

    # Settings
    self.ui.setting_back_button.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//back.png') + "')}")
    self.ui.lang_apply_pushButton.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//apply.png') + "')}")
    self.ui.qss_apply_pushButton.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//apply.png') + "')}")
    self.ui.reset_qss_pushButton.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//reset.png') + "')}")
    self.ui.qss_apply_file_pushButton.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//add.png') + "')}")
    self.ui.qss_file_pushButton.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//qss-file.png') + "')}")
    self.ui.check_key_pushButton.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//check.png') + "')}")
    self.ui.delete_qss_pushButton.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//delete.png') + "')}")

    # CVE info page
    self.ui.cve_info_back_button.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//back.png') + "')}")

    # Vuln info page
    self.ui.vuln_info_back_button.setStyleSheet(
        ".QPushButton {image: url('" + GetRelPath(self, 'assets//images//back.png') + "')}")

    self.logger.debug(f"Load_Images_And_Icons : Buttons icons seted")
