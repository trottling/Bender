from PyQt6 import uic, QtGui
from PyQt6.QtWidgets import QMainWindow


class User_UI(QMainWindow):
    def __init__(self, app_version: str, logger) -> None:
        super().__init__()
        self.app_version = app_version
        self.logger = logger
        self.ui = None
        Load_UI(self)


def Load_UI(self) -> None:
    self.logger.debug(r"Load_UI : Loading UI : .\ui\app.ui")

    # Load UI file
    self.ui = uic.loadUi(r"assets\ui\app.ui", self)
    self.logger.debug(f"Load_UI : UI loaded")

    # Icon
    self.ui.setWindowIcon(QtGui.QIcon(r"assets\icons\bender.ico"))
    self.logger.debug(f"Load_UI : Icon seted")

    # Title
    self.ui.setWindowTitle(f" Windows Vulnerability Scanner")
    self.logger.debug(f"Load_UI : Title seted")

    # Logo
    self.ui.logo.setStyleSheet(r".QFrame {border-image: url('assets//images//bender.png')}")
    self.ui.logo_2.setStyleSheet(r".QFrame {border-image: url('assets//images//bender.png')}")
    self.ui.git_frame.setStyleSheet(r".QFrame {image: url('assets//images//github.png')}")
    self.logger.debug(f"Load_UI : Logo seted")

    # Buttons icons
    self.ui.setting_btn.setStyleSheet(r".QPushButton {image: url('assets//images//settings.png')}")
    self.ui.back_button.setStyleSheet(r".QPushButton {image: url('assets//images//back.png')}")
    self.ui.lang_apply_pushButton.setStyleSheet(r".QPushButton {image: url('assets//images//apply.png')}")
    self.ui.font_apply_pushButton.setStyleSheet(r".QPushButton {image: url('assets//images//apply.png')}")
    self.ui.reset_font_pushButton.setStyleSheet(r".QPushButton {image: url('assets//images//reset.png')}")
    self.ui.qss_apply_pushButton.setStyleSheet(r".QPushButton {image: url('assets//images//apply.png')}")
    self.ui.select_qss_pushButton.setStyleSheet(r".QPushButton {image: url('assets//images//open_file.png')}")
    self.ui.reset_qss_pushButton.setStyleSheet(r".QPushButton {image: url('assets//images//reset.png')}")
    self.logger.debug(f"Load_UI : Buttons icons seted")

    # Connect buttons
    self.ui.setting_btn.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(3), self.logger.debug(
        "setting_btn : self.stackedWidget.setCurrentIndex(3)")))
    self.ui.back_button.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(0), self.logger.debug(
        "setting_btn : self.stackedWidget.setCurrentIndex(0)")))
    self.ui.font_apply_pushButton.clicked.connect(
        lambda: (self.ui.setFont(self.fontComboBox.currentText()), self.logger.debug(
            f"font_apply_pushButton : setFont {str(self.fontComboBox.currentText())}")))
    self.logger.debug(f"Load_UI : Buttons connected")

    # App version
    self.ui.app_ver.setText(f"ver {self.app_version}")
    self.logger.debug(f"Load_UI : App version seted")

    # Load styles
    self.ui.setStyleSheet(open(file=r"assets\qss\MaterialDark.qss", mode="r").read())
    self.logger.debug(f"Load_UI : Styles loaded")

    # Show UI
    self.stackedWidget.setCurrentIndex(0)
    self.ui.show()
    self.logger.debug(f"Load_UI : UI showed")
