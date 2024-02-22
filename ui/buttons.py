import os
import platform
import sys
from pathlib import Path

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QFileDialog

from OnAppStart.setup_logger import Check_Admin
from checkers.run_checker import Run_Checker
from checkers.run_checker import Stop_Checker
from ui.animations import App_Exit_Anim, StackedWidgetChangePage, ElemShowAnim, ElemHideAnim
from ui.styles import Load_Styles
from ui.tools import Save_Settings, Check_Vulners_Key_Request


def Connect_Buttons(self):
    self.ui.setting_btn.clicked.connect(lambda: (StackedWidgetChangePage(self, 3)))

    self.ui.info_btn.clicked.connect(lambda: (StackedWidgetChangePage(self, 6)))

    self.ui.cve_info_back_button.clicked.connect(lambda: (StackedWidgetChangePage(self, 2), ClearCVEInfoPage(self)))

    self.ui.setting_back_button.clicked.connect(
        lambda: (Save_Settings(self), (StackedWidgetChangePage(self, 0))))

    self.ui.info_back_button.clicked.connect(lambda: StackedWidgetChangePage(self, 0))

    self.ui.back_work_button.clicked.connect(
        lambda: (StackedWidgetChangePage(self, 0), Stop_Checker(self)))

    self.ui.next_work_button.clicked.connect(lambda: StackedWidgetChangePage(self, 2))

    self.ui.back_result_button.clicked.connect(lambda: StackedWidgetChangePage(self, 1))

    self.ui.next_result_button.clicked.connect(lambda: StackedWidgetChangePage(self, 0))

    self.ui.horizontalSlider_network_threads.valueChanged.connect(lambda: MaxNetWorkersChanged(self))

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

    self.ui.errors_exit.clicked.connect(lambda: (self.logger.debug(
        "errors_exit : EXIT"), sys.exit(-1)))

    self.ui.check_key_pushButton.clicked.connect(lambda: Check_Vulners_Key(self))

    self.ui.delete_qss_pushButton.clicked.connect(lambda: DeleteQSSTheme(self))

    self.ui.pushButton_app_exit.clicked.connect(lambda: App_Exit_Anim(self))

    self.ui.stackedWidget.currentChanged.connect(lambda: ChangeTitle(self))

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
    ElemHideAnim(self, self.ui.qss_label_2)
    ElemHideAnim(self, self.ui.qss_lineEdit)
    ElemHideAnim(self, self.ui.delete_qss_pushButton)
    ElemHideAnim(self, self.ui.qss_apply_file_pushButton)
    ElemHideAnim(self, self.ui.qss_file_pushButton)
    self.logger.debug("HideQSSInput : Hided")


def ShowQSSInput(self):
    ElemShowAnim(self, self.ui.qss_label_2)
    ElemShowAnim(self, self.ui.qss_lineEdit)
    ElemShowAnim(self, self.ui.qss_apply_file_pushButton)
    ElemShowAnim(self, self.ui.qss_file_pushButton)
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
    if path.strip() == "":
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
    ElemHideAnim(self, self.ui.vulners_check_result)
    Save_Settings(self)
    if self.ui.api_key.text().strip() == "":
        self.logger.debug("Check_Vulners_Key : api key empty")
        self.ui.vulners_check_result.setStyleSheet(r".QFrame {image: url('assets//images//fail.png')}")
        ElemShowAnim(self, self.ui.vulners_check_result)
        return
    if Check_Vulners_Key_Request(self):
        self.ui.vulners_check_result.setStyleSheet(r".QFrame {image: url('assets//images//apply.png')}")
    else:
        self.ui.vulners_check_result.setStyleSheet(r".QFrame {image: url('assets//images//fail.png')}")

    ElemShowAnim(self, self.ui.vulners_check_result)


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
        ElemShowAnim(self, self.ui.delete_qss_pushButton)
    else:
        ElemHideAnim(self, self.ui.delete_qss_pushButton)


def ChangeTitle(self):
    if self.ui.stackedWidget.currentIndex() != 0:
        if not self.ui.label_windows_title.isVisible():
            ElemShowAnim(self, self.ui.label_windows_title)
            ElemShowAnim(self, self.ui.app_icon)
    else:
        ElemHideAnim(self, self.ui.label_windows_title)
        ElemHideAnim(self, self.ui.app_icon)


def ClearCVEInfoPage(self):
    QTimer.singleShot(250, lambda: (self.ui.cve_desc_plainTextEdit.clear(),
                                    self.ui.plainTextEdit_references.clear(),
                                    self.ui.plainTextEdit_cvss_3.clear()))


def SaveReport(self):
    report_file = None
    try:
        report_file = QFileDialog.getSaveFileName(self, caption='Save log file (.txt)', directory="./",
                                                  filter=".txt",
                                                  initialFilter=".txt")
    except Exception as e:
        self.logger.debug(f"SaveReport : {e}")

    if report_file == "":
        return

    report_file = report_file[0] + report_file[1]

    self.logger.debug(f"SaveReport : Open file {report_file}")

    try:
        with open(report_file, "w") as f:
            f.write(r"""
              ____                    _                       __          __ _             _                       __      __      _                           _      _  _  _  _             _____
             |  _ \                  | |                      \ \        / /(_)           | |                      \ \    / /     | |                         | |    (_)| |(_)| |           / ____|
             | |_) |  ___  _ __    __| |  ___  _ __   ______   \ \  /\  / /  _  _ __    __| |  ___ __      __ ___   \ \  / /_   _ | | _ __    ___  _ __  __ _ | |__   _ | | _ | |_  _   _  | (___    ___  __ _  _ __   _ __    ___  _ __
             |  _ <  / _ \| '_ \  / _` | / _ \| '__| |______|   \ \/  \/ /  | || '_ \  / _` | / _ \\ \ /\ / // __|   \ \/ /| | | || || '_ \  / _ \| '__|/ _` || '_ \ | || || || __|| | | |  \___ \  / __|/ _` || '_ \ | '_ \  / _ \| '__|
             | |_) ||  __/| | | || (_| ||  __/| |                \  /\  /   | || | | || (_| || (_) |\ V  V / \__ \    \  / | |_| || || | | ||  __/| |  | (_| || |_) || || || || |_ | |_| |  ____) || (__| (_| || | | || | | ||  __/| |
             |____/  \___||_| |_| \__,_| \___||_|                 \/  \/    |_||_| |_| \__,_| \___/  \_/\_/  |___/     \/   \__,_||_||_| |_| \___||_|   \__,_||_.__/ |_||_||_| \__| \__, | |_____/  \___|\__,_||_| |_||_| |_| \___||_|
                                                                                                                                                                         __/ |
                                                                                                                                                                        |___/

            Autor - @trottling
            Github - github.com/trottling/Bender
            """)
            f.write(f"Python {sys.version}")
            f.write(f"Application version: {self.app_version}")
            f.write(f"Run as Admin : {Check_Admin(self.logger)}")
            f.write("OS Name: " + platform.system())
            f.write("OS Release: " + platform.release())
            f.write("OS Version: " + platform.version())
            f.write("\n\n\n\n\n")

            for item in self.report["cve_list"]:
                f.write("cve: " + item["cve"])
                f.write("package: " + item["package"])
                f.write("version: " + item["version"])
                f.write("score: " + item["score"])
                f.write("desc: " + item["desc"])
                f.write("published: " + item["datePublished"])
                f.write("shortName: " + item["shortName"])
                f.write("references: " + item["references"])
                f.write("\n\n\n\n\n")
    except Exception as e:
        self.logger.error(f"SaveReport : error {e}")
        return
    self.logger.debug(f"SaveReport : Report writed")


def MaxNetWorkersChanged(self):
    value = str(self.ui.horizontalSlider_network_threads.value())
    self.ui.label_network_threads_value.setText(value)
    if not self.isSliderTimerStart:
        self.isSliderTimerStart = True
        QTimer.singleShot(2500, lambda: (Save_Settings(self)))
        self.isSliderTimerStart = False
