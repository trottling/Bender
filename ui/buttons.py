import os

from PyQt6.QtWidgets import QFileDialog
from checkers.Check_Connected_Devices import RunCCD
from checkers.Check_Installed_Apps import RunCIA


def Connect_Buttons(self):
    self.ui.setting_btn.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(3), self.logger.debug(
        "setting_btn : self.stackedWidget.setCurrentIndex(3)")))

    self.ui.back_button.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(0), self.logger.debug(
        "setting_btn : self.stackedWidget.setCurrentIndex(0)")))

    self.ui.qss_apply_pushButton.clicked.connect(lambda: (
        self.ui.setStyleSheet(open(
            f"assets\\qss\\Material{'Light' if self.ui.qss_comboBox.currentText() == 'Default (Light)' else 'Dark'}.qss",
            mode="r").read()), self.logger.debug(
            f"qss_apply_pushButton : assets\\qss\\Material{'Light' if self.ui.qss_comboBox.currentText() == 'Default (Light)' else 'Dark'}.qss : Styles loaded")))

    self.ui.qss_comboBox.currentIndexChanged.connect(lambda:
                                                     ChangeShowQSSInput(self))

    self.ui.qss_file_pushButton.clicked.connect(lambda: OpenQSSFile(self))

    self.ui.qss_apply_file_pushButton.clicked.connect(lambda: ApplyQSSTheme(self))

    self.ui.save_log_pushButton.clicked.connect(lambda: SaveDebugLog(self))
    self.ui.save_log_pushButton_2.clicked.connect(lambda: SaveDebugLog(self))

    self.ui.CCD_btn.clicked.connect(lambda: RunCCD(self))
    self.ui.CIA_btn.clicked.connect(lambda: RunCIA(self))

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
    except:
        pass

    self.logger.debug(f"OpenQSSFile : File {qss_file}")

    if qss_file == "":
        return

    if os.path.isfile(str(qss_file[0])):
        self.ui.qss_lineEdit.setText(str(qss_file[0]))
        self.logger.debug(f"OpenQSSFile : qss_lineEdit set Text {str(qss_file[0])}")


def ApplyQSSTheme(self):
    path = self.ui.qss_lineEdit.text()

    self.logger.debug(f"ApplyQSSTheme : Apply Styles {path}")

    if not os.path.isfile(path):
        return

    self.ui.setStyleSheet(open(file=path, mode="r").read())
    self.ui.show()
    self.logger.debug(f"ApplyQSSTheme : {path} : Styles loaded")


def SaveDebugLog(self):
    log_file = None
    try:
        log_file = QFileDialog.getSaveFileName(self, caption='Save log file (.log)', directory="./",
                                               filter=".log",
                                               initialFilter=".log")
    except:
        pass

    if log_file == "":
        return

    log_file = log_file[0] + log_file[1]

    self.logger.debug(f"SaveDebugLog : Open file {log_file}")

    try:
        open(log_file, "x").write(open(self.appdir + "/" + "debug_log.txt", "r").read())
    except Exception as e:
        self.logger.debug(f"SaveDebugLog : error {e}")
        return
    self.logger.debug(f"SaveDebugLog : Log writed")
