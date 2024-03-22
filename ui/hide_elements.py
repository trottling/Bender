from ui.buttons import HideQSSInput


def Hide_Elements(self):

    self.splash.ChangePbar(70, "Hide Elements")

    # Global
    self.ui.label_windows_title.hide()
    self.ui.app_icon.hide()

    # Start page
    self.ui.alert_msg.hide()

    # Settings page
    self.ui.delete_qss_pushButton.hide()

    # Work progress page
    self.ui.next_work_btn.hide()

    # Work result page
    self.ui.logo_3.hide()
    self.ui.app_name_2.hide()
    self.ui.app_desc_2.hide()
    self.ui.app_link_label.hide()

    HideQSSInput(self)

    self.logger.debug("Hide_Elements : Elements Hided")
