def Hide_Elements(self):
    self.ui.qss_label_2.hide()
    self.ui.qss_lineEdit.hide()
    self.ui.qss_apply_file_pushButton.hide()
    self.ui.qss_file_pushButton.hide()
    self.ui.alert_msg.hide()
    self.ui.next_work_button.hide()
    self.ui.delete_qss_pushButton.hide()
    self.ui.label_windows_title.hide()
    self.ui.app_icon.hide()
    self.ui.label_no_cve.hide()

    if self.ui.db_comboBox.currentText() != "vulners.com (Recommended)":
        self.ui.label_vulners_key.hide()
        self.ui.api_key.hide()
        self.ui.check_key_pushButton.hide()
        self.ui.vulners_check_result.hide()
        self.ui.vulners_key_help.hide()

    self.logger.debug("Hide_Elements : Elements Hided")
