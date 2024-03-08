from ui.buttons import HideQSSInput


def Hide_Elements(self):
    self.ui.alert_msg.hide()
    self.ui.delete_qss_pushButton.hide()
    self.ui.label_windows_title.hide()
    self.ui.app_icon.hide()
    self.ui.next_work_btn.hide()
    self.ui.image_work_progress.hide()
    self.ui.label_work_progress.hide()

    HideQSSInput(self)

    self.logger.debug("Hide_Elements : Elements Hided")
