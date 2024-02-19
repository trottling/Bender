from PyQt6.QtCore import QThread, pyqtSignal
from checkers.Check_Connected_Devices import RunCCD
from checkers.Check_Installed_Apps import RunCIA
from ui.tools import Report_Error
from checkers.validate import Validate_before_check
from ui.show_report import Show_Report


class CheckerThread(QThread):
    log_signal = pyqtSignal(str)
    result_signal = pyqtSignal(object)
    pbar_signal = pyqtSignal(int)
    err_signal = pyqtSignal(str)

    def __init__(self, checker, logger, db, api_key):
        QThread.__init__(self)
        super().__init__()
        self.checker = checker
        self.logger = logger
        self.db = db
        self.api_key = api_key
        self.report = None

    def run(self):
        self.logger.debug(f"CheckerThread : Run checker : {self.checker}")
        match self.checker:
            case "RunCCD":
                RunCCD(self)
            case "RunCIA":
                RunCIA(self)

    def stop(self):
        self.terminate()


def Run_Checker(self, checker):
    # Clear log widget
    self.ui.work_log.setPlainText("")

    if Validate_before_check(self):
        return
    try:
        self.ui.stackedWidget.setCurrentIndex(1)
        self.checker_thread = CheckerThread(checker, self.logger, self.ui.db_comboBox.currentText(),
                                            self.ui.api_key.text())
        self.checker_thread.log_signal.connect(lambda log: self.ui.work_log.appendPlainText(log))
        self.checker_thread.err_signal.connect(lambda err: (Report_Error(self, err), self.checker_thread.stop()))
        self.checker_thread.pbar_signal.connect(lambda num: self.ui.progressBar.setValue(num))
        self.checker_thread.result_signal.connect(lambda rep: (Stop_Checker(self), Show_Report(self)))
        self.checker_thread.start()
        self.logger.debug("Run_Checker : Thread started")
    except Exception as e:
        Report_Error(self, f"Run_Checker : {e}")


def Stop_Checker(self):
    self.checker_thread.stop()
    self.logger.debug("Stop_Checker : checker_thread : Thread stopped")
