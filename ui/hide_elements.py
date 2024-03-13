from ui.buttons import HideQSSInput


def Hide_Elements(self):
    self.ui.alert_msg.hide()
    self.ui.delete_qss_pushButton.hide()
    self.ui.label_windows_title.hide()
    self.ui.app_icon.hide()

    # Work progress page
    self.ui.next_work_btn.hide()
    self.ui.framel_scan_successful.hide()
    self.ui.label_scan_successful.hide()
    self.ui.label_scan_successful_len.hide()
    self.ui.frame_scan_error.hide()
    self.ui.label_scan_error.hide()
    self.ui.label_scan_error_len.hide()

    # Work result page
    self.ui.logo_3.hide()
    self.ui.app_name_2.hide()
    self.ui.app_desc_2.hide()
    self.ui.app_link_label.hide()

    HideQSSInput(self)

    self.logger.debug("Hide_Elements : Elements Hided")
