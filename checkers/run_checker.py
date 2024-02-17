from PyQt6.QtCore import QThread, pyqtSignal
from checkers.Check_Connected_Devices import RunCCD
from checkers.Check_Installed_Apps import RunCIA
from ui.tools import Report_Error


class CheckerThread(QThread):
    log_signal = pyqtSignal(str)
    result_signal = pyqtSignal(object)
    pbar_signal = pyqtSignal(int)
    err_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(object)

    def __init__(self, checker, logger):
        QThread.__init__(self)
        super().__init__()
        self.checker = checker
        self.logger = logger

    def run(self):
        self.logger.debug(f"CheckerThread : {self.checker}")
        if self.checker == "RunCCD":
            RunCCD(self)
        elif self.checker == "RunCIA":
            RunCIA(self)

    def stop(self):
        self.terminate()


def Run_Checker(self, checker):
    try:
        self.ui.stackedWidget.setCurrentIndex(1)
        self.checker_thread = CheckerThread(checker, self.logger)
        self.checker_thread.log_signal.connect(lambda log: self.ui.work_log.appendPlainText(log))
        self.checker_thread.err_signal.connect(lambda err: (Report_Error(self, err), self.checker_thread.stop()))
        self.checker_thread.pbar_signal.connect(lambda num: self.ui.progressBar.setValue(num))
        self.checker_thread.start()
    except Exception as e:
        Report_Error(self, f"Run_Checker : {e}")
