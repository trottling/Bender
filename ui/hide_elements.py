from loguru import logger


def hide_elements(self):

    self.splash.change_pbar(70, "Hide Elements")

    # Global
    self.ui.label_windows_title.hide()
    self.ui.app_icon.hide()

    # Start page
    self.ui.alert_msg.hide()

    # Work progress page
    self.ui.next_work_btn.hide()

    # Work result page
    self.ui.logo_3.hide()
    self.ui.app_name_2.hide()
    self.ui.app_desc_2.hide()
    self.ui.app_link_label.hide()

    logger.debug("hide_elements : Elements Hided")
