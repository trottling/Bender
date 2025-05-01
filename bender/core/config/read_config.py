from loguru import logger

from bender.core.config.check_config import check_config_file


def load_settings(self):

    self.splash.change_pbar(60, "Loading settings")

    if check_config_file(self):
        try:
            self.config.read(self.config_path)

            logger.debug(f"load_settings : app_theme : {self.config.get('main', 'app_theme')}")
            self.app_theme = self.config.get('main', 'app_theme')
            # Set theme in comboBox
            index = self.ui.qss_comboBox.findText(self.app_theme)
            if index != -1:
                self.ui.qss_comboBox.setCurrentIndex(index)

            net_workers = int(self.config.get('main', "net_workers"))
            logger.debug(f"load_settings : net_workers : {net_workers}")
            if net_workers not in (None, ""):
                self.ui.horizontalSlider_network_threads.setValue(net_workers)
            self.ui.label_network_threads_value.setText(str(net_workers))

            data_workers = int(self.config.get('main', "data_workers"))
            logger.debug(f"load_settings : data_workers : {data_workers}")
            if data_workers not in (None, ""):
                self.ui.horizontalSlider_data_threads.setValue(int(data_workers))
            self.ui.label_data_threads_value.setText(str(data_workers))

            port_workers = int(self.config.get('main', "port_workers"))
            logger.debug(f"load_settings : port_workers : {port_workers}")
            if port_workers not in (None, ""):
                self.ui.horizontalSlider_port_threads.setValue(int(port_workers))
            self.ui.label_port_threads.setText(str(port_workers))

            vulners_api_key = self.config.get("main", "vulners_api_key")
            if vulners_api_key not in (None, ""):
                logger.debug(f"load_settings : vulners_api_key : * IS NOT EMPTY * : {len(str(vulners_api_key))} letters")
                self.ui.api_key.setText(str(vulners_api_key))
            else:
                logger.debug(f"load_settings : vulners_api_key : * EMPTY *")

            self.window_size_full = True if self.config.get("main", "window_size_full") == "0" else False

            logger.debug("load_settings : Settings loaded")

        except Exception as e:
            logger.error(f"load_settings : {e}")
