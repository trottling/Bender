from ui.animations import ShowErrMessage


def StartScannerValidator(self):
    # True - is there any mistake

    try:

        if self.start_tasks_running:
            ShowErrMessage(self, "Wait until operability test is done")
            return True

        if not self.validate_os_sup_status:
            ShowErrMessage(self, "OS not supported")
            return True

        if not self.validate_user_admin:
            ShowErrMessage(self, "Rerun app as Admin to avoid errors")
            return True

        if not self.validate_net_status:
            ShowErrMessage(self, "No network connection, try restart operability test")
            return True

        if not self.validate_vulners_status:
            ShowErrMessage(self, "Vulners.com Unavailable, try run scanner later")
            return True

        if not self.validate_vulners_key:
            ShowErrMessage(self, "Vulners.com key invalid or empty, fix it in settings. <a href='https://github.com/trottling/Bender/blob/main/VULNERS-API-KEY-HELP.md'>Click for help</a>")
            return True

        if not self.validate_loldrivers_status:
            ShowErrMessage(self, "Loldrivers.io Unavailable, try run scanner later")
            return True

        self.logger.debug("StartScannerValidator : All normal")

    except Exception as e:
        self.logger.error(f"StartScannerValidator : {e}")
        ShowErrMessage(self, str(e))
        return True

    return False
