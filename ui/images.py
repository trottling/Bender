from ui.tools import GetRelPath


def Load_Images_And_Icons(self):
    # Logo
    self.ui.logo.setStyleSheet(
        ".QFrame {border-image: url('" + GetRelPath(self, 'assets//images//bender.png') + "')}")
    self.ui.logo_2.setStyleSheet(
        ".QFrame {border-image: url('" + GetRelPath(self, 'assets//images//bender.png') + "')}")
    self.ui.logo_3.setStyleSheet(
        ".QFrame {border-image: url('" + GetRelPath(self, 'assets//images//bender.png') + "')}")
    self.ui.git_frame.setStyleSheet(
        r".QFrame {image: url('" + GetRelPath(self, 'assets//images//github.png') + "')}")
    self.logger.debug(f"Load_Images_And_Icons : Logos seted")

    # Buttons icons

    # Toolbar
    self.ui.pushButton_app_exit.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//exit.png') + "')}")
    self.ui.pushButton_app_hide.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//minimize.png') + "')}")
    self.ui.app_icon.setStyleSheet(
        r".QFrame {image: url('" + GetRelPath(self, 'assets//images//bender-small.png') + "')}")

    # Settings
    self.ui.setting_back_button.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//back.png') + "')}")
    self.ui.lang_apply_pushButton.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//apply.png') + "')}")
    self.ui.qss_apply_pushButton.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//apply.png') + "')}")
    self.ui.reset_qss_pushButton.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//reset.png') + "')}")
    self.ui.qss_apply_file_pushButton.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//add.png') + "')}")
    self.ui.qss_file_pushButton.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//qss-file.png') + "')}")
    self.ui.check_key_pushButton.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//check.png') + "')}")
    self.ui.delete_qss_pushButton.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//delete.png') + "')}")
    self.ui.vulners_key_help.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//help.png') + "')}")

    # Pages

    # Start page
    self.ui.setting_btn.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//settings.png') + "')}")
    self.ui.info_btn.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//info.png') + "')}")

    # Work log page
    self.ui.back_work_button.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//back.png') + "')}")
    self.ui.next_work_button.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//next.png') + "')}")

    # Work result page
    self.ui.back_result_button.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//back.png') + "')}")
    self.ui.next_result_button.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//fail.png') + "')}")

    # Info page
    self.ui.info_back_button.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//back.png') + "')}")

    # CVE info page
    self.ui.cve_info_back_button.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//back.png') + "')}")

    # Vuln info page
    self.ui.vuln_info_back_button.setStyleSheet(
        r".QPushButton {image: url('" + GetRelPath(self, 'assets//images//back.png') + "')}")

    self.logger.debug(f"Load_Images_And_Icons : Buttons icons seted")
