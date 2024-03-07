from ui.animations import ElemHideAnim
from ui.buttons import HideQSSInput


def Hide_Elements(self):
    self.ui.alert_msg.hide()
    self.ui.delete_qss_pushButton.hide()
    self.ui.label_windows_title.hide()
    self.ui.app_icon.hide()

    HideQSSInput(self)

    ElemHideAnim(self, self.ui.next_work_btn, hide=False)  # Just set opacity to 0
    self.ui.next_work_btn.setEnabled(False)  # And make inactive

    self.logger.debug("Hide_Elements : Elements Hided")
