from config.check_config import CheckConfigFile


def Load_Settings(self):
    if CheckConfigFile(self):
        try:
            self.config.read(self.config_path)

            self.logger.debug(f"Load_Settings : app_theme : {self.config.get('main', "app_theme")}")
            self.app_theme = self.config.get('main', "app_theme")

            net_workers = int(self.config.get('main', "net_workers"))
            self.logger.debug(f"Load_Settings : net_workers : {net_workers}")
            if net_workers not in (None, ""):
                self.ui.horizontalSlider_network_threads.setValue(net_workers)
            self.ui.label_network_threads_value.setText(str(net_workers))

            data_workers = int(self.config.get('main', "data_workers"))
            self.logger.debug(f"Load_Settings : data_workers : {data_workers}")
            if data_workers not in (None, ""):
                self.ui.horizontalSlider_data_threads.setValue(int(data_workers))
            self.ui.label_data_threads_value.setText(str(data_workers))

            vulners_api_key = self.config.get("main", "vulners_api_key")
            if vulners_api_key not in (None, ""):
                self.logger.debug(f"Load_Settings : vulners_api_key : * IS NOT EMPTY *")
                self.ui.api_key.setText(str(vulners_api_key))
            else:
                self.logger.debug(f"Load_Settings : vulners_api_key : * EMPTY *")

            port_workers = int(self.config.get('main', "port_workers"))
            self.logger.debug(f"Load_Settings : port_workers : {port_workers}")
            if port_workers not in (None, ""):
                self.ui.horizontalSlider_port_threads.setValue(int(port_workers))
            self.ui.label_port_threads.setText(str(port_workers))

            port_range = self.config.get("main", "port_range")
            if port_range not in (None, ""):
                self.ui.api_key.setText(str(port_range))
            self.logger.debug(f"Load_Settings : port_range : {str(port_range)}")

            self.window_size_full = True if self.config.get("main", "window_size_full") == "0" else False

            self.logger.debug("Load_Settings : Settings loaded")

        except Exception as e:
            self.logger.error(f"Load_Settings : {e}")
