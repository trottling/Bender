from config.check_config import CheckConfigFile


def Save_Settings(self):
    CheckConfigFile(self)
    try:

        self.config.set('main', "app_theme", self.ui.qss_comboBox.currentText())
        self.config.set('main', "vulners_api_key", self.ui.api_key.text().strip())
        self.config.set('main', "net_workers", str(self.ui.horizontalSlider_network_threads.value()))
        self.config.set('main', "data_workers", str(self.ui.horizontalSlider_data_threads.value()))

        with open(self.config_path, 'w') as f:
            self.config.write(f)
            self.logger.debug("Save_Settings : Settings saved")
    except Exception as e:
        self.logger.error(f"Save_Settings : {e}")
