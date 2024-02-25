from PyQt6.QtCore import QThread, pyqtSignal
from checkers.check_drivers import RunCCD
from checkers.check_installed_apps import RunCIA
from ui.animations import ChangePBarValue, StackedWidgetChangePage
from ui.tools import Report_Error, ClearResult
from checkers.validate import Validate_before_check
from ui.show_report import Show_Report_CIA, Show_Report_CCD


class CheckerThread(QThread):
    log_signal = pyqtSignal(str)
    result_signal = pyqtSignal(str)
    pbar_signal = pyqtSignal(int)
    err_signal = pyqtSignal(str)

    def __init__(self, checker, logger, db, api_key, net_threads, data_threads):
        QThread.__init__(self)
        super().__init__()
        self.checker = checker
        self.logger = logger
        self.db = db
        self.api_key = api_key
        self.net_threads = net_threads
        self.data_threads = data_threads
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
    ClearResult(self)
    self.checker = checker

    if Validate_before_check(self):
        return
    try:
        StackedWidgetChangePage(self, 1)
        self.checker_thread = CheckerThread(checker, self.logger, self.ui.db_comboBox.currentText(),
                                            self.ui.api_key.text(), self.ui.horizontalSlider_network_threads.value(),
                                            self.ui.horizontalSlider_data_threads.value())
        self.checker_thread.log_signal.connect(lambda log: self.ui.work_log.appendPlainText(log))
        self.checker_thread.err_signal.connect(lambda err: (Report_Error(self, err), self.checker_thread.stop()))
        self.checker_thread.pbar_signal.connect(lambda value: ChangePBarValue(self, value))
        self.checker_thread.result_signal.connect(lambda rep: ShowReport(self, rep, checker))
        self.checker_thread.start()
        self.logger.debug("Run_Checker : Thread started")
    except Exception as e:
        Report_Error(self, f"Run_Checker : {e}")


def Stop_Checker(self):
    self.checker_thread.stop()
    self.logger.debug("Stop_Checker : Thread stopped")


def ShowReport(self, rep, checker):
    Stop_Checker(self)

    match checker:
        case "RunCCD":
            Show_Report_CCD(self, rep)
        case "RunCIA":
            Show_Report_CIA(self, rep)
