import os
import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QFileDialog
from checkers.run_checker import Run_Checker
from ui.animations import App_Exit_Anim
from ui.styles import Load_Styles
from pathlib import Path

from ui.tools import Save_Settings, Check_Vulners_Key_Request
from checkers.run_checker import Stop_Checker


def Connect_Buttons(self):
    self.ui.setting_btn.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(3), self.logger.debug(
        "setting_btn : self.stackedWidget.setCurrentIndex(3)")))

    self.ui.setting_back_button.clicked.connect(
        lambda: (Save_Settings(self), self.stackedWidget.setCurrentIndex(0), self.logger.debug(
            "setting_back_button : self.stackedWidget.setCurrentIndex(0)")))

    self.ui.back_work_button.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(0), self.logger.debug(
        "back_work_button : self.stackedWidget.setCurrentIndex(0)"), Stop_Checker(self), self.logger.debug(
        "back_work_button : Checker stopped")))

    self.ui.next_work_button.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(2), self.logger.debug(
        "next_work_button : self.stackedWidget.setCurrentIndex(2)")))

    self.ui.back_result_button.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(1), self.logger.debug(
        "back_result_button : self.stackedWidget.setCurrentIndex(1)")))

    self.ui.next_result_button.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(0), self.logger.debug(
        "next_result_button : self.stackedWidget.setCurrentIndex(0)")))

    self.ui.qss_apply_pushButton.clicked.connect(lambda: ApplyQSSTheme(self))

    self.ui.qss_comboBox.currentIndexChanged.connect(lambda:
                                                     ChangeShowQSSInput(self))
    self.ui.qss_comboBox.currentIndexChanged.connect(lambda:
                                                     ChangeQSSDeleteBtn(self))

    self.ui.qss_file_pushButton.clicked.connect(lambda: OpenQSSFile(self))

    self.ui.qss_apply_file_pushButton.clicked.connect(lambda: ApplyCustomQSSTheme(self))

    self.ui.reset_qss_pushButton.clicked.connect(lambda: Load_Styles(self))

    self.ui.save_log_pushButton.clicked.connect(lambda: SaveDebugLog(self))

    self.ui.save_log_pushButton_2.clicked.connect(lambda: SaveDebugLog(self))

    self.ui.errors_exit.clicked.connect(lambda: sys.exit(-1))

    self.ui.check_key_pushButton.clicked.connect(lambda: Check_Vulners_Key(self))

    self.ui.delete_qss_pushButton.clicked.connect(lambda: DeleteQSSTheme(self))

    self.ui.pushButton_app_exit.clicked.connect(lambda: (App_Exit_Anim(self)))

    self.ui.pushButton_app_hide.clicked.connect(lambda: (self.ui.showMinimized(), self.logger.debug(
        "pushButton_app_hide : Minimized")))

    self.ui.CCD_btn.clicked.connect(lambda: Run_Checker(self, "RunCCD"))
    self.ui.CIA_btn.clicked.connect(lambda: Run_Checker(self, "RunCIA"))

    self.logger.debug(f"Connect_Buttons : Buttons connected")


def ChangeShowQSSInput(self):
    if self.ui.qss_comboBox.currentText() != "Custom":
        HideQSSInput(self)
        self.logger.debug(
            f"ChangeShowQSSInput : {self.ui.qss_comboBox.currentText()} : Selected theme is not Custom")
        return
    else:
        self.logger.debug("ChangeShowQSSInput : Selected theme is Custom")
        ShowQSSInput(self)


def HideQSSInput(self):
    self.ui.qss_label_2.hide()
    self.ui.qss_lineEdit.hide()
    self.ui.delete_qss_pushButton.hide()
    self.ui.qss_apply_file_pushButton.hide()
    self.ui.qss_file_pushButton.hide()
    self.logger.debug("HideQSSInput : Hided")


def ShowQSSInput(self):
    self.ui.qss_label_2.show()
    self.ui.qss_lineEdit.show()
    self.ui.qss_apply_file_pushButton.show()
    self.ui.qss_file_pushButton.show()
    self.logger.debug("ShowQSSInput : Showed")


def OpenQSSFile(self):
    self.logger.debug("OpenQSSFile : Open file")
    qss_file = None
    try:
        qss_file = QFileDialog.getOpenFileName(self, caption='Open file', directory='./',
                                               filter="QSS Style files (*.qss)")
    except Exception as e:
        self.logger.debug(f"OpenQSSFile : {e}")

    self.logger.debug(f"OpenQSSFile : File {qss_file}")

    if qss_file == "":
        return

    if os.path.isfile(str(qss_file[0])):
        self.ui.qss_lineEdit.setText(str(qss_file[0]))
        self.logger.debug(f"OpenQSSFile : qss_lineEdit set Text {str(qss_file[0])}")


def ApplyCustomQSSTheme(self):
    path = self.ui.qss_lineEdit.text()
    if path.strip() is "":
        return
    Save_Settings(self)
    self.logger.debug(f"ApplyCustomQSSTheme : Apply Styles {path}")

    if not os.path.isfile(path):
        return

    self.ui.setStyleSheet(open(file=path, mode="r").read())
    self.ui.show()
    self.logger.debug(f"ApplyCustomQSSTheme : {path} : Styles loaded")
    open(file=f"{self.appdir}\\saved_qss\\{Path(path).name}", mode="w").write(open(file=path, mode="r").read())
    self.ui.qss_comboBox.addItem(Path(path).name)
    self.ui.qss_comboBox.setCurrentText(Path(path).name)
    self.logger.debug(f"ApplyCustomQSSTheme : {self.appdir}\\saved_qss\\{Path(path).name} : Theme saved")


def SaveDebugLog(self):
    log_file = None
    try:
        log_file = QFileDialog.getSaveFileName(self, caption='Save log file (.log)', directory="./",
                                               filter=".log",
                                               initialFilter=".log")
    except Exception as e:
        self.logger.debug(f"SaveDebugLog : {e}")

    if log_file == "":
        return

    log_file = log_file[0] + log_file[1]

    self.logger.debug(f"SaveDebugLog : Open file {log_file}")

    try:
        open(log_file, "x").write(open(self.appdir + "/" + "debug_log.txt", "r").read())
    except Exception as e:
        self.logger.error(f"SaveDebugLog : error {e}")
        return
    self.logger.debug(f"SaveDebugLog : Log writed")


def ApplyQSSTheme(self):
    Save_Settings(self)
    if self.ui.qss_comboBox.currentText() == 'Default (Light)' or self.ui.qss_comboBox.currentText() == 'Default (Dark)':
        self.ui.setStyleSheet(open(
            f"assets\\qss\\Material{'Light' if self.ui.qss_comboBox.currentText() == 'Default (Light)' else 'Dark'}.qss",
            mode="r").read())
        self.logger.debug(
            f"AppleQSSTheme : assets\\qss\\Material{'Light' if self.ui.qss_comboBox.currentText() == 'Default (Light)' else 'Dark'}.qss : Default Styles loaded")

    elif self.ui.qss_comboBox.currentText() != "Custom":
        try:
            self.ui.setStyleSheet(open(
                f"{self.appdir}\\saved_qss\\{self.ui.qss_comboBox.currentText()}",
                mode="r").read())
            self.logger.debug(
                f"AppleQSSTheme : {self.appdir}\\saved_qss\\{self.ui.qss_comboBox.currentText()} : User Styles loaded")
        except Exception as e:
            self.logger.error(
                f"AppleQSSTheme : {self.appdir}\\saved_qss\\{self.ui.qss_comboBox.currentText()} : User Styles not loaded : {e}")


def Check_Vulners_Key(self):
    self.ui.vulners_check_result.hide()
    Save_Settings(self)
    if self.ui.api_key.text().strip() == "":
        self.logger.debug("Check_Vulners_Key : api key empty")
        self.ui.vulners_check_result.setStyleSheet(r".QFrame {image: url('assets//images//fail.png')}")
        self.ui.vulners_check_result.show()
        return
    if Check_Vulners_Key_Request(self):
        self.ui.vulners_check_result.setStyleSheet(r".QFrame {image: url('assets//images//apply.png')}")
    else:
        self.ui.vulners_check_result.setStyleSheet(r".QFrame {image: url('assets//images//fail.png')}")

    self.ui.vulners_check_result.show()


def DeleteQSSTheme(self):
    themeToDelete = self.ui.qss_comboBox.currentText()
    self.logger.debug(f"DeleteQSSTheme : theme To Delete : {themeToDelete}")
    if themeToDelete in ("Custom", "Default (Light)", "Default (Dark)"):
        return
    try:
        os.remove(f"{self.user_themes_path}{themeToDelete}")
        self.ui.qss_comboBox.removeItem(self.ui.qss_comboBox.currentIndex())
        self.ui.qss_comboBox.setCurrentText(self.default_theme)
        ApplyQSSTheme(self)
    except Exception as e:
        self.logger.error(f"DeleteQSSTheme : {themeToDelete} : {e}")


def ChangeQSSDeleteBtn(self):
    if self.ui.qss_comboBox.currentText() not in ("Custom", "Default (Light)", "Default (Dark)"):
        self.ui.delete_qss_pushButton.show()
        self.logger.debug("ChangeQSSDeleteBtn : show")
    else:
        self.ui.delete_qss_pushButton.hide()
        self.logger.debug("ChangeQSSDeleteBtn : hide")
