from config.check_config import CheckConfigFile


def Save_Settings(self):
    CheckConfigFile(self)
    try:
        self.logger.debug(f"Save_Settings : main : app_theme : {self.ui.qss_comboBox.currentText()}")
        self.logger.debug(
            f"Save_Settings : main : vulners_api_key : {" * IS NOT EMPTY *" if self.ui.api_key.text().strip() != "" or None else "EMPTY"}")
        self.logger.debug(
            f"Save_Settings : main : net_workers : {str(self.ui.horizontalSlider_network_threads.value())}")
        self.logger.debug(f"Save_Settings : main : data_workers : {str(self.ui.horizontalSlider_data_threads.value())}")
        self.logger.debug(f"Save_Settings : main : window_size_full : {self.window_size_full}")

        self.config.set('main', "app_theme", self.ui.qss_comboBox.currentText())
        self.config.set('main', "vulners_api_key", self.ui.api_key.text().strip())
        self.config.set('main', "net_workers", str(self.ui.horizontalSlider_network_threads.value()))
        self.config.set('main', "data_workers", str(self.ui.horizontalSlider_data_threads.value()))
        self.config.set('main', "window_size_full", "0" if self.window_size_full else "1")

        with open(self.config_path, 'w') as f:
            self.config.write(f)
            self.logger.debug("Save_Settings : Settings saved")
    except Exception as e:
        self.logger.error(f"Save_Settings : {e}")
