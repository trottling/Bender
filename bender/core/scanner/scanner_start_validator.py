from loguru import logger

from bender.ui.animations import show_err_message


def start_scanner_validator(self):
    # True - is there any mistake

    try:

        if self.start_tasks_running:
            show_err_message(self, "Wait until operability test is done")
            return True

        if not self.validate_os_sup_status:
            show_err_message(self, "OS not supported")
            return True

        if not self.validate_user_admin:
            show_err_message(self, "Rerun app as Admin to avoid errors")
            return True

        if not self.validate_net_status:
            show_err_message(self, "No network connection, try restart operability test")
            return True

        if not self.validate_vulners_status:
            show_err_message(self, "Vulners.com Unavailable, try run scanner later")
            return True

        if not self.validate_vulners_key:
            show_err_message(self,
                           "Vulners.com key invalid or empty, fix it in settings. <a href='https://github.com/trottling/Bender/blob/main/VULNERS-API-KEY-HELP.md'>Click for help</a>")
            return True

        if not self.validate_loldrivers_status:
            show_err_message(self, "Loldrivers.io Unavailable, try run scanner later")
            return True

        logger.debug("start_scanner_validator: All checks passed")

    except Exception as e:
        logger.error(f"start_scanner_validator: {e}")
        show_err_message(self, str(e))
        return True

    return False
