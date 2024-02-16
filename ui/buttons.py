import os

from PyQt6.QtWidgets import QFileDialog


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
    self.ui.label_thanks.move(675, 475)
    self.ui.label_list_thanks.move(625, 525)
    self.ui.qss_label_2.hide()
    self.ui.qss_lineEdit.hide()
    self.ui.qss_apply_file_pushButton.hide()
    self.ui.qss_file_pushButton.hide()
    self.logger.debug("HideQSSInput : Hided")


def ShowQSSInput(self):
    self.ui.label_thanks.move(675, 525)
    self.ui.label_list_thanks.move(625, 575)
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
