from PySide6 import QtGui, QtUiTools
from PySide6.QtWidgets import QMainWindow


class User_UI(QMainWindow):
    def __init__(self, app_version: str, logger) -> None:
        super().__init__()
        self.app_version = app_version
        self.logger = logger
        self.ui = None
        Load_UI(self)


def Load_UI(self) -> None:
    self.logger.info(f"Load_UI: Loading UI : {r"..\assets\ui\app.ui"}")
    self.ui = QtUiTools.QUiLoader().load(r"..\assets\ui\app.ui")
    self.ui.setWindowIcon(QtGui.QIcon(r"..\assets\icons\bender.ico"))
    self.ui.setWindowTitle(f" Windows Vulnerability Scanner")
    self.ui.show()
    self.logger.debug(f"Load_UI: UI loaded")
