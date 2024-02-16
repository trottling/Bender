from PyQt6 import uic, QtGui


def Prepare_Window(self):
    self.logger.debug(r"Prepare_Window : Loading UI : .\ui\app.ui")

    # Load UI file
    self.ui = uic.loadUi(r"assets\ui\app.ui", self)
    self.logger.debug(f"Prepare_Window : UI loaded")

    # Icon
    self.ui.setWindowIcon(QtGui.QIcon(r"assets\icons\bender.ico"))
    self.logger.debug(f"Prepare_Window : Icon seted")

    # Title
    self.ui.setWindowTitle("Windows Vulnerability Scanner")
    self.logger.debug(f"Prepare_Window : Title seted")

    # App version
    self.ui.app_ver.setText(f"ver {self.app_version}")
    self.logger.debug(f"Prepare_Window : App version seted")

    # Hide elements
    self.ui.qss_label_2.hide()
    self.ui.qss_lineEdit.hide()
    self.ui.qss_apply_file_pushButton.hide()
    self.ui.qss_file_pushButton.hide()
    self.logger.debug("Prepare_Window : Elements Hided")
