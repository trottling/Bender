from tasks.scanner import Scanner
from tasks.scanner_funcs import LoadShodanReport
from tasks.scanner_signals import ConnectScannerSignals
from tasks.scanner_start_validator import StartScannerValidator
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

    # Get UI values
    self.net_threads = self.ui.horizontalSlider_network_threads.value()
    self.data_workers = self.ui.horizontalSlider_data_threads.value()
    self.vulners_key = self.ui.api_key.text().strip()
    self.port_workers = self.ui.horizontalSlider_port_threads.value()

    # Create thread
    self.scanner = Scanner(self.logger, self.net_threads, self.data_workers, self.vulners_key, self.port_workers)

    # Connect signals
    ConnectScannerSignals(self)

    # Run scanner thread
    self.scanner.start()
    self.logger.debug("Run_Scanner_Tasks : Thread started")

    # Run other funcs
    LoadShodanReport(self)
