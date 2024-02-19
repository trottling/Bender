from PyQt6.QtCore import QTimer


def Validate_before_check(self):
    if self.ui.db_comboBox.currentText() == "vulners.com (Recommended)":
        if self.ui.api_key.text().strip() == "":
            ShowErrMessage(self, "Vulners.com API key is empty")
            return True
        if not self.isVulnersKeyValid:
            ShowErrMessage(self, "Check and validate vulners.com API key in settings before start")
            return True
        self.logger.debug("Validate_before_check : All normal")
        return False


def ShowErrMessage(self, msg):
    if not self.ui.alert_msg.isVisible():
        self.ui.alert_msg.show()
        self.ui.alert_msg.setText(msg)
        self.logger.debug(f"ShowErrMessage : {msg}")
        QTimer.singleShot(5000, lambda: self.ui.alert_msg.hide())
