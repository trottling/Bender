from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QMovie, QPixmap
from loguru import logger

from bender.ui.tools import get_rel_path


def load_images_and_icons(self):

    #
    # Logo
    #
    self.ui.logo.setStyleSheet(".QFrame {border-image: url('" + get_rel_path(self, 'assets//images//bender.png') + "')}")
    self.ui.logo_2.setStyleSheet(".QFrame {border-image: url('" + get_rel_path(self, 'assets//images//bender.png') + "')}")
    self.ui.logo_3.setStyleSheet(".QFrame {border-image: url('" + get_rel_path(self, 'assets//images//bender.png') + "')}")
    self.ui.git_frame.setStyleSheet(".QFrame {border-image: url('" + get_rel_path(self, 'assets//images//github.png') + "')}")

    logger.debug(f"load_images_and_icons : Logos seted")

    # Set start page system data icons to processing GIF

    for elem in self.start_processing_elems:
        gif = QMovie(get_rel_path(self, r"assets\gifs\loading.gif"))
        gif.setFormat(b"gif")
        gif.setScaledSize(QtCore.QSize(22, 22))
        elem.setMovie(gif)
        gif.start()

    logger.debug(f"load_images_and_icons : Loading GIF seted")

    #
    # Buttons icons
    #

    # Toolbar
    self.ui.pushButton_app_exit.setStyleSheet(".QPushButton {image: url('" + get_rel_path(self, 'assets//images//exit.png') + "')}")
    self.ui.pushButton_app_size.setStyleSheet(".QPushButton {image: url('" + get_rel_path(self, 'assets//images//resize.png') + "')}")
    self.ui.pushButton_app_hide.setStyleSheet(".QPushButton {image: url('" + get_rel_path(self, 'assets//images//minimize.png') + "')}")
    self.ui.app_icon.setStyleSheet(".QFrame {border-image: url('" + get_rel_path(self, 'assets//images//bender-small.png') + "')}")

    #
    # Pages
    #

    # Start page
    self.ui.setting_btn.setStyleSheet(".QPushButton {image: url('" + get_rel_path(self, 'assets//images//settings.png') + "')}")
    self.ui.info_btn.setStyleSheet(".QPushButton {image: url('" + get_rel_path(self, 'assets//images//info.png') + "')}")
    self.ui.reload_btn.setStyleSheet(".QPushButton {image: url('" + get_rel_path(self, 'assets//images//reload.png') + "')}")

    # Pbar page
    self.ui.next_work_btn.setStyleSheet(".QPushButton {image: url('" + get_rel_path(self, 'assets//images//next.png') + "')}")

    # Work result page
    self.ui.frame_Hardware_cpu.setStyleSheet(".QFrame {image: url('" + get_rel_path(self, 'assets//images//pc_cpu.png') + "')}")
    self.ui.frame_Hardware_gpu.setStyleSheet(".QFrame {image: url('" + get_rel_path(self, 'assets//images//gpu.png') + "')}")
    self.ui.frame_Hardware_ram.setStyleSheet(".QFrame {image: url('" + get_rel_path(self, 'assets//images//ram.png') + "')}")
    self.ui.frame_Hardware_rom.setStyleSheet(".QFrame {image: url('" + get_rel_path(self, 'assets//images//ssd.png') + "')}")
    self.ui.frame_net_firewall.setStyleSheet(".QFrame {image: url('" + get_rel_path(self, 'assets//images//firewall.png') + "')}")
    self.ui.frame_net_mac.setStyleSheet(".QFrame {image: url('" + get_rel_path(self, 'assets//images//mac.png') + "')}")
    self.ui.frame_net_local_ip.setStyleSheet(".QFrame {image: url('" + get_rel_path(self, 'assets//images//internal.png') + "')}")
    self.ui.frame_ext_local_ip.setStyleSheet(".QFrame {image: url('" + get_rel_path(self, 'assets//images//external.png') + "')}")
    self.ui.frame_sys_bitlocker.setStyleSheet(".QFrame {image: url('" + get_rel_path(self, 'assets//images//bitlocker.png') + "')}")
    self.ui.frame_sys_virt.setStyleSheet(".QFrame {image: url('" + get_rel_path(self, 'assets//images//virtualization.png') + "')}")
    self.ui.frame_sys_bitness.setPixmap(QPixmap(get_rel_path(self, 'assets//images//help.png')))

    # Info page
    self.ui.info_back_button.setStyleSheet(".QPushButton {image: url('" + get_rel_path(self, 'assets//images//back.png') + "')}")
    self.ui.pushButton_repo.setIcon(QtGui.QIcon(get_rel_path(self, r"assets\images\trottling.png")))
    self.ui.pushButton_repo.setIconSize(QtCore.QSize(40, 40))

    # Settings
    self.ui.setting_back_button.setStyleSheet(".QPushButton {image: url('" + get_rel_path(self, 'assets//images//back.png') + "')}")
    self.ui.check_key_pushButton.setStyleSheet(".QPushButton {image: url('" + get_rel_path(self, 'assets//images//check.png') + "')}")

    # CVE info page
    self.ui.cve_info_back_button.setStyleSheet(".QPushButton {image: url('" + get_rel_path(self, 'assets//images//back.png') + "')}")

    # Vuln info page
    self.ui.vuln_info_back_button.setStyleSheet(".QPushButton {image: url('" + get_rel_path(self, 'assets//images//back.png') + "')}")

    logger.debug(f"load_images_and_icons : Buttons icons seted")
