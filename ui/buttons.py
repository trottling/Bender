import os
import sys
import webbrowser
from pathlib import Path

from PyQt6 import QtCore, QtTest, QtGui
from PyQt6.QtCore import QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QFileDialog, QGraphicsOpacityEffect

from checkers.run_checker import Stop_Checker
from config.write_config import Save_Settings
from tasks.scanner_start_validator import StartScannerValidator
from tasks.scanner_tasks import Run_Scanner_Tasks
from tasks.start_tasks import Run_Start_Tasks
from ui.animations import App_Exit_Anim, StackedWidgetChangePage, ElemShowAnim, ElemHideAnim, TextChangeAnim, \
    ImageChangeAnim
from ui.styles import Load_Styles
from ui.tools import Check_Vulners_Key_Request, GetRelPath, ShowErrMessage


def Connect_Buttons(self):
    #
    # Start page
    #

    self.ui.setting_btn.clicked.connect(lambda: (StackedWidgetChangePage(self, 3)))

    self.ui.info_btn.clicked.connect(lambda: (StackedWidgetChangePage(self, 6)))

    self.ui.reload_btn.clicked.connect(lambda: (RestartStartTask(self)))

    self.ui.pushButton_start_scan.clicked.connect(lambda: (StartScanner(self)))

    #
    # Setting page
    #

    self.ui.setting_back_button.clicked.connect(
        lambda: (Save_Settings(self), (StackedWidgetChangePage(self, 0))))

    self.ui.horizontalSlider_network_threads.valueChanged.connect(lambda: MaxNetWorkersChanged(self))

    self.ui.horizontalSlider_data_threads.valueChanged.connect(lambda: MaxDataWorkersChanged(self))

    self.ui.qss_apply_pushButton.clicked.connect(lambda: ApplyQSSTheme(self))

    self.ui.qss_comboBox.currentIndexChanged.connect(lambda:
                                                     ChangeShowQSSInput(self))
    self.ui.qss_comboBox.currentIndexChanged.connect(lambda:
                                                     ChangeQSSDeleteBtn(self))

    self.ui.qss_file_pushButton.clicked.connect(lambda: OpenQSSFile(self))

    self.ui.qss_apply_file_pushButton.clicked.connect(lambda: ApplyCustomQSSTheme(self))

    self.ui.reset_qss_pushButton.clicked.connect(lambda: Load_Styles(self))

    self.ui.save_log_pushButton.clicked.connect(lambda: SaveDebugLog(self))

    self.ui.check_key_pushButton.clicked.connect(lambda: Check_Vulners_Key(self))

    #
    # Info page
    #

    self.ui.info_back_button.clicked.connect(lambda: StackedWidgetChangePage(self, 0))
    self.ui.pushButton_repo.clicked.connect(lambda: webbrowser.open("https://github.com/trottling/Bender"))

    #
    # Errors page
    #

    self.ui.save_log_pushButton_2.clicked.connect(lambda: SaveDebugLog(self))

    self.ui.errors_exit.clicked.connect(lambda: (self.logger.debug(
        "errors_exit : ******** EXIT ********"), sys.exit(-1)))

    self.ui.cve_info_back_button.clicked.connect(lambda: (StackedWidgetChangePage(self, 2), ClearCVEInfoPage(self)))

    self.ui.next_work_btn.clicked.connect(lambda: StackedWidgetChangePage(self, 2))

    self.ui.vuln_info_back_button.clicked.connect(lambda: StackedWidgetChangePage(self, 2))

    self.ui.delete_qss_pushButton.clicked.connect(lambda: DeleteQSSTheme(self))

    self.ui.stackedWidget.currentChanged.connect(lambda: ChangeTitle(self))

    # self.ui.save_report_btn.clicked.connect(lambda: SaveReport(self))

    #
    # Toolbar
    #

    self.ui.pushButton_app_exit.clicked.connect(lambda: App_Exit_Anim(self))

    self.ui.pushButton_app_size.clicked.connect(lambda: Resize_Window(self))

    self.ui.pushButton_app_hide.clicked.connect(lambda: (self.ui.showMinimized(), self.logger.debug(
        "pushButton_app_hide : ******** Minimized ********")))

    self.logger.debug(f"Connect_Buttons : Buttons connected")


def ChangeShowQSSInput(self):
    if self.ui.qss_comboBox.currentText() != "Custom" and self.qss_input_showed:
        HideQSSInput(self)
    elif self.ui.qss_comboBox.currentText() == "Custom" and not self.qss_input_showed:
        ShowQSSInput(self)


def HideQSSInput(self):
    self.qss_input_showed = False
    elem_list = [self.ui.qss_label_2, self.ui.qss_lineEdit, self.ui.delete_qss_pushButton,
                 self.ui.qss_apply_file_pushButton, self.ui.qss_file_pushButton]

    for elem in elem_list:
        elem.setGraphicsEffect(QGraphicsOpacityEffect().setOpacity(1.0))

        effect = QGraphicsOpacityEffect(elem)
        effect.setOpacity(1.0)
        elem.setGraphicsEffect(effect)

        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(150)
        anim.setStartValue(effect.opacity())
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        anim.start()
        elem.setEnabled(False)

    self.logger.debug("HideQSSInput : Hided")


def ShowQSSInput(self):
    self.qss_input_showed = True
    elem_list = [self.ui.qss_label_2, self.ui.qss_lineEdit, self.ui.delete_qss_pushButton,
                 self.ui.qss_apply_file_pushButton, self.ui.qss_file_pushButton]

    for elem in elem_list:
        elem.setGraphicsEffect(QGraphicsOpacityEffect().setOpacity(0.0))

        effect = QGraphicsOpacityEffect(elem)
        effect.setOpacity(0.0)
        elem.setGraphicsEffect(effect)

        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(150)
        anim.setStartValue(effect.opacity())
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        anim.start()
        elem.setEnabled(True)

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
    try:
        log_file = QFileDialog.getSaveFileName(self, caption='Save log file (.log)', directory="./",
                                               filter=".log",
                                               initialFilter=".log")
    except Exception as e:
        self.logger.debug(f"SaveDebugLog : {e}")
        return

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
        self.ui.setStyleSheet(open(GetRelPath(self,
                                              f"assets\\qss\\Material{'Light' if self.ui.qss_comboBox.currentText() == 'Default (Light)' else 'Dark'}.qss"),
                                   mode="r").read())
        self.logger.debug(
            f"AppleQSSTheme : assets\\qss\\Material{'Light' if self.ui.qss_comboBox.currentText() == 'Default (Light)' else 'Dark'}.qss : Default Styles loaded")

    elif self.ui.qss_comboBox.currentText() != "Custom":
        try:
            self.ui.setStyleSheet(open(GetRelPath(self,
                                                  f"{self.appdir}\\saved_qss\\{self.ui.qss_comboBox.currentText()}"),
                                       mode="r").read())
            self.logger.debug(
                f"AppleQSSTheme : {self.appdir}\\saved_qss\\{self.ui.qss_comboBox.currentText()} : User Styles loaded")
        except Exception as e:
            self.logger.error(
                f"AppleQSSTheme : {self.appdir}\\saved_qss\\{self.ui.qss_comboBox.currentText()} : User Styles not loaded : {e}")


def Check_Vulners_Key(self):
    Save_Settings(self)
    if self.ui.api_key.text().strip() == "":
        self.logger.debug("Check_Vulners_Key : api key empty")
        webbrowser.open("https://vulners.com/docs/apikey/")
        ImageChangeAnim(self, self.ui.vulners_check_result, 'assets//images//fail.png')
        self.validate_vulners_key = False
        return
    if Check_Vulners_Key_Request(self):
        ImageChangeAnim(self, self.ui.vulners_check_result, 'assets//images//apply.png')
        self.validate_vulners_key = True
    else:
        ImageChangeAnim(self, self.ui.vulners_check_result, 'assets//images//fail.png')
        self.validate_vulners_key = False


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
                                    self.ui.plainTextEdit_cvss_3.clear(),
                                    ))


def MaxNetWorkersChanged(self):
    value = str(self.ui.horizontalSlider_network_threads.value())
    self.ui.label_network_threads_value.setText(value)
    if not self.isSliderTimerStart:
        self.isSliderTimerStart = True
        QTimer.singleShot(2500, lambda: (Save_Settings(self), ChangeSliderLock(self)))


def MaxDataWorkersChanged(self):
    value = str(self.ui.horizontalSlider_data_threads.value())
    self.ui.label_data_threads_value.setText(value)
    if not self.isSliderTimerStart:
        self.isSliderTimerStart = True
        QTimer.singleShot(2500, lambda: (Save_Settings(self), ChangeSliderLock(self)))


def ChangeSliderLock(self):
    self.isSliderTimerStart = False


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

    self.logger.debug(f"SaveReport : Report writed")


def Write_dict_recursive(self, f, d, indent=0):
    for key, value in d.items():
        if isinstance(value, dict):
            f.write("  " * indent + str(key) + ": \n")
            Write_dict_recursive(self, f, value, indent + 1)
            f.write("  " * indent + "")
        else:
            f.write("  " * indent + str(key) + ": " + str(value) + "\n")


def Resize_Window(self):
    if not self.window_size_full:
        self.ui.showMaximized()
        self.logger.debug("Resize_Window : showMaximized")
        self.window_size_full = True
        Save_Settings(self)
    else:
        if self.screen_width_cut != 0 and self.screen_height_cut != 0:
            self.ui.resize(self.screen_width_cut, self.screen_height_cut)
            self.logger.debug(f"Resize_Window : Resized {self.screen_width_cut} x {self.screen_height_cut}")
        else:
            self.ui.resize(800, 600)
            self.logger.debug(f"Resize_Window : Resized 800 x 600")
        self.ui.move(int((self.screen_width - self.ui.size().width()) / 2),
                     int((self.screen_height - self.ui.size().height()) / 2))
        self.window_size_full = False
        Save_Settings(self)


def RestartStartTask(self):
    if self.start_tasks_running:
        ShowErrMessage(self, "The operability test is already running")
    else:
        #
        # Total 175 ms
        #
        for image, label in zip(self.start_processing_elems, self.start_processing_labels):
            ElemHideAnim(self, image, dur=40)
            QtTest.QTest.qWait(40)
            TextChangeAnim(self, label, "Processing...")
            image.clear()
            gif = QMovie(GetRelPath(self, r"assets\gifs\loading.gif"))
            gif.setFormat(b"gif")
            gif.setScaledSize(QtCore.QSize(22, 22))
            image.setMovie(gif)
            gif.start()
            ElemShowAnim(self, image, dur=40)
            QtTest.QTest.qWait(40)

        Run_Start_Tasks(self)


def StartScanner(self):
    if StartScannerValidator(self):
        return
    Run_Scanner_Tasks(self)
