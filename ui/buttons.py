import os
import sys
import webbrowser
from pathlib import Path

from PyQt6 import QtCore, QtTest
from PyQt6.QtCore import QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QFileDialog, QGraphicsOpacityEffect

from config.write_config import save_settings
from scanner.start_scanner import start_scanner
from tasks.start_tasks import run_start_tasks
from ui.animations import app_exit_anim, stacked_widget_change_page, elem_show_anim, elem_hide_anim, text_change_anim,     image_change_anim, show_err_message
from ui.styles import load_styles
from ui.tools import check_vulners_key_request, get_rel_path
from loguru import logger


def connect_buttons(self):

    self.splash.change_pbar(80, "Connecting buttons")

    #
    # Start page
    #

    self.ui.setting_btn.clicked.connect(lambda: (stacked_widget_change_page(self, 3)))

    self.ui.info_btn.clicked.connect(lambda: (stacked_widget_change_page(self, 6)))

    self.ui.reload_btn.clicked.connect(lambda: (restart_start_task(self)))

    self.ui.pushButton_start_scan.clicked.connect(lambda: (start_scanner(self)))

    #
    # Result page
    #

    self.ui.pushButton_save_log.clicked.connect(lambda: save_debug_log(self))
    self.ui.pushButton_save_report.clicked.connect(lambda: save_scan_results(self))

    #
    # Setting page
    #

    self.ui.setting_back_button.clicked.connect(
        lambda: (save_settings(self), (stacked_widget_change_page(self, 0))))

    self.ui.horizontalSlider_network_threads.valueChanged.connect(lambda: save_on_change(self))

    self.ui.horizontalSlider_data_threads.valueChanged.connect(lambda: save_on_change(self))

    self.ui.horizontalSlider_port_threads.valueChanged.connect(lambda: save_on_change(self))

    self.ui.qss_comboBox.currentIndexChanged.connect(lambda: apply_qss_theme(self))

    self.ui.save_log_pushButton.clicked.connect(lambda: save_debug_log(self))

    self.ui.check_key_pushButton.clicked.connect(lambda: check_vulners_key(self))

    #
    # Info page
    #

    self.ui.info_back_button.clicked.connect(lambda: stacked_widget_change_page(self, 0))
    self.ui.pushButton_repo.clicked.connect(lambda: webbrowser.open("https://github.com/trottling/Bender"))

    #
    # Errors page
    #

    self.ui.save_log_pushButton_2.clicked.connect(lambda: save_debug_log(self))

    self.ui.errors_exit.clicked.connect(lambda: (logger.debug("errors_exit : ******** EXIT ********"), sys.exit(-1)))

    self.ui.cve_info_back_button.clicked.connect(lambda: (stacked_widget_change_page(self, 2), clear_cve_info_page(self)))

    self.ui.next_work_btn.clicked.connect(lambda: stacked_widget_change_page(self, 2))

    self.ui.vuln_info_back_button.clicked.connect(lambda: stacked_widget_change_page(self, 2))

    self.ui.stackedWidget.currentChanged.connect(lambda: change_title(self))

    # self.ui.save_report_btn.clicked.connect(lambda: SaveReport(self))

    #
    # Toolbar
    #

    self.ui.pushButton_app_exit.clicked.connect(lambda: app_exit_anim(self))

    self.ui.pushButton_app_size.clicked.connect(lambda: resize_window(self))

    self.ui.pushButton_app_hide.clicked.connect(lambda: (self.ui.showMinimized(), logger.debug("pushButton_app_hide : ******** Minimized ********")))

    logger.debug(f"Connect_Buttons : Buttons connected")


def apply_qss_theme(self):
    # Fade out window
    fade_out = QPropertyAnimation(self.ui, b'windowOpacity', self)
    fade_out.setDuration(200)
    fade_out.setStartValue(1.0)
    fade_out.setEndValue(0.0)

    def set_theme():
        theme = self.ui.qss_comboBox.currentText()
        qss_path = get_rel_path(self, f"assets\\qss\\Material{theme}.qss")
        self.ui.setStyleSheet(open(qss_path, mode="r").read())
        logger.debug(f"AppleQSSTheme : {qss_path} : Styles loaded")

    def on_fade_out_finished():
        set_theme()
        fade_in = QPropertyAnimation(self.ui, b'windowOpacity', self)
        fade_in.setDuration(200)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.start()

    fade_out.finished.connect(on_fade_out_finished)
    fade_out.start()


def check_vulners_key(self):
    save_settings(self)
    if self.ui.api_key.text().strip() == "":
        logger.debug("Check_Vulners_Key : api key empty")
        webbrowser.open("https://github.com/trottling/Bender/blob/main/VULNERS-API-KEY-HELP.md")
        image_change_anim(self, self.ui.vulners_check_result, 'assets//images//fail.png')
        self.validate_vulners_key = False
        return
    if check_vulners_key_request(self):
        image_change_anim(self, self.ui.vulners_check_result, 'assets//images//apply.png')
        self.validate_vulners_key = True
    else:
        image_change_anim(self, self.ui.vulners_check_result, 'assets//images//fail.png')
        self.validate_vulners_key = False


def change_title(self):
    if self.ui.stackedWidget.currentIndex() != 0:
        if not self.ui.label_windows_title.isVisible():
            elem_show_anim(self, self.ui.label_windows_title)
            elem_show_anim(self, self.ui.app_icon)
    else:
        elem_hide_anim(self, self.ui.label_windows_title)
        elem_hide_anim(self, self.ui.app_icon)


def clear_cve_info_page(self):
    QTimer.singleShot(250, lambda: (self.ui.cve_desc_plainTextEdit.clear(),
                                    self.ui.plainTextEdit_references.clear(),
                                    self.ui.plainTextEdit_cvss_3.clear(),
                                    ))


def save_on_change(self):
    self.ui.label_data_threads_value.setText(str(self.ui.horizontalSlider_data_threads.value()))
    self.ui.label_network_threads_value.setText(str(self.ui.horizontalSlider_network_threads.value()))
    self.ui.label_port_threads.setText(str(self.ui.horizontalSlider_port_threads.value()))

    if not self.isSliderTimerStart:
        self.isSliderTimerStart = True
        QTimer.singleShot(2500, lambda: (save_settings(self), change_slider_lock(self)))


def change_slider_lock(self):
    self.isSliderTimerStart = False


def save_report(self):
    report_file = None
    try:
        report_file = QFileDialog.getSaveFileName(self, caption='Save log file (.txt)', directory="./", filter=".txt", initialFilter=".txt")
    except Exception as e:
        logger.debug(f"SaveReport: {e}")
    if report_file == "":
        return
    report_file = report_file[0] + report_file[1]
    logger.debug(f"SaveReport: Open file {report_file}")
    logger.debug(f"SaveReport: Report written")


def write_dict_recursive(self, f, d, indent=0):
    for key, value in d.items():
        if isinstance(value, dict):
            f.write("  " * indent + str(key) + ": \n")
            write_dict_recursive(self, f, value, indent + 1)
            f.write("  " * indent + "")
        else:
            f.write("  " * indent + str(key) + ": " + str(value) + "\n")


def resize_window(self):
    if not self.window_size_full:
        self.ui.showMaximized()
        logger.debug("Resize_Window : showMaximized")
        self.window_size_full = True
        save_settings(self)
    else:
        if self.screen_width_cut != 0 and self.screen_height_cut != 0:
            self.ui.resize(self.screen_width_cut, self.screen_height_cut)
            logger.debug(f"Resize_Window : Resized {self.screen_width_cut} x {self.screen_height_cut}")
        else:
            self.ui.resize(800, 600)
            logger.debug(f"Resize_Window : Resized 800 x 600")
        self.ui.move(int((self.screen_width - self.ui.size().width()) / 2), int((self.screen_height - self.ui.size().height()) / 2))
        self.window_size_full = False
        save_settings(self)


def restart_start_task(self):
    if self.start_tasks_running:
        show_err_message(self, "The operability test is already running")
    else:
        #
        # Total 175 ms
        #
        for image, label in zip(self.start_processing_elems, self.start_processing_labels):
            elem_hide_anim(self, image, dur=40)
            QtTest.QTest.qWait(40)
            text_change_anim(self, label, "Processing...")
            image.clear()
            gif = QMovie(get_rel_path(self, r"assets\gifs\loading.gif"))
            gif.setFormat(b"gif")
            gif.setScaledSize(QtCore.QSize(22, 22))
            image.setMovie(gif)
            gif.start()
            elem_show_anim(self, image, dur=40)
            QtTest.QTest.qWait(40)

        run_start_tasks(self)


def save_scan_results(self):
    try:
        res_file = QFileDialog.getSaveFileName(self, caption='Save image (.png)', directory="./", filter=".png")
    except Exception as e:
        logger.error(f"SaveScanResults : {e}")
        return

    if res_file == "" or None:
        return

    res_file = res_file[0] + res_file[1]

    logger.debug(f"SaveScanResults : Open file {res_file}")

    self.ui.pushButton_save_log.hide()
    self.ui.pushButton_save_report.hide()
    self.ui.logo_3.show()
    self.ui.app_name_2.show()
    self.ui.app_desc_2.show()
    self.ui.app_link_label.show()

    try:
        image = self.ui.scrollAreaWidgetContents.grab(self.ui.scrollAreaWidgetContents.rect())
        image.save(res_file)
        logger.debug(f"SaveScanResults : Image writed")
    except Exception as e:
        logger.error(f"SaveScanResults : error {e}")

    self.ui.pushButton_save_log.show()
    self.ui.pushButton_save_report.show()
    self.ui.logo_3.hide()
    self.ui.app_name_2.hide()
    self.ui.app_desc_2.hide()
    self.ui.app_link_label.hide()
