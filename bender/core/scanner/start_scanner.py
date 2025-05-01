from loguru import logger

from bender.core.scanner.scanner import Scanner
from bender.core.scanner.scanner_signals import connect_scanner_signals
from bender.core.scanner.scanner_start_validator import start_scanner_validator
from bender.ui.animations import set_work_page_gif, stacked_widget_change_page


def start_scanner(self):
    self.ui.pushButton_start_scan.setEnabled(False)
    if start_scanner_validator(self):
        self.ui.pushButton_start_scan.setEnabled(True)
        return
    run_scanner_tasks(self)


def run_scanner_tasks(self):
    stacked_widget_change_page(self, 1, "up")

    #
    # Run ThreadPoolExecutor --> Put result in result page
    #

    # Set loading GIF to progress label
    set_work_page_gif(self)

    # Get ui values
    self.net_threads = self.ui.horizontalSlider_network_threads.value()
    self.data_workers = self.ui.horizontalSlider_data_threads.value()
    self.port_workers = self.ui.horizontalSlider_port_threads.value()
    self.vulners_key = self.ui.api_key.text().strip()

    # Create thread
    self.scanner = Scanner(self.net_threads, self.data_workers, self.port_workers, self.vulners_key)

    # Connect signals
    connect_scanner_signals(self)

    # Run scanner thread
    self.scanner.start()
    logger.debug("run_scanner_tasks : Thread started")
