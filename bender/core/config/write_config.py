from loguru import logger

from bender.core.config.check_config import check_config_file


def save_settings(self):
    check_config_file(self)
    try:
        logger.debug(f"save_settings : main : app_theme : {self.ui.qss_comboBox.currentText()}")
        logger.debug(f"save_settings : main : vulners_api_key : {f' * IS NOT EMPTY * : {len(self.ui.api_key.text().strip())} letters' if self.ui.api_key.text().strip() != '' or None else 'EMPTY'}")
        logger.debug(f"save_settings : main : net_workers : {str(self.ui.horizontalSlider_network_threads.value())}")
        logger.debug(f"save_settings : main : data_workers : {str(self.ui.horizontalSlider_data_threads.value())}")
        logger.debug(f"save_settings : main : port_workers : {str(self.ui.horizontalSlider_port_threads.value())}")
        logger.debug(f"save_settings : main : window_size_full : {self.window_size_full}")

        self.config.set('main', "app_theme", self.ui.qss_comboBox.currentText())
        self.config.set('main', "vulners_api_key", self.ui.api_key.text().strip())
        self.config.set('main', "net_workers", str(self.ui.horizontalSlider_network_threads.value()))
        self.config.set('main', "data_workers", str(self.ui.horizontalSlider_data_threads.value()))
        self.config.set('main', "port_workers", str(self.ui.horizontalSlider_port_threads.value()))
        self.config.set('main', "window_size_full", "0" if self.window_size_full else "1")

        with open(self.config_path, 'w') as f:
            self.config.write(f)
            logger.debug("save_settings : Settings saved")
    except Exception as e:
        logger.error(f"save_settings : {e}")
