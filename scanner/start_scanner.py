from scanner.scanner import Scanner
from scanner.scanner_signals import ConnectScannerSignals
from scanner.scanner_start_validator import StartScannerValidator
from ui.animations import StackedWidgetChangePage, SetWorkPageGIF


def StartScanner(self):
    self.ui.pushButton_start_scan.setEnabled(False)
    if StartScannerValidator(self):
        self.ui.pushButton_start_scan.setEnabled(True)
        return
    Run_Scanner_Tasks(self)


def Run_Scanner_Tasks(self):
    StackedWidgetChangePage(self, 1)

    #
    # Run ThreadPoolExecutor --> Put result in result page
    #

    # Set loading gif to progress label
    SetWorkPageGIF(self)

    # Get ui values
    self.net_threads = self.ui.horizontalSlider_network_threads.value()
    self.data_workers = self.ui.horizontalSlider_data_threads.value()
    self.port_workers = self.ui.horizontalSlider_port_threads.value()
    self.vulners_key = self.ui.api_key.text().strip()

    # Create thread
    self.scanner = Scanner(self.logger, self.net_threads, self.data_workers, self.port_workers, self.vulners_key)

    # Connect signals
    ConnectScannerSignals(self)

    # Run scanner thread
    self.scanner.start()
    self.logger.debug("Run_Scanner_Tasks : Thread started")
