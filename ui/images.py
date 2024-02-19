def Load_Images_And_Icons(self):
    # Logo
    self.ui.logo.setStyleSheet(r".QFrame {border-image: url('assets//images//bender.png')}")
    self.ui.logo_2.setStyleSheet(r".QFrame {border-image: url('assets//images//bender.png')}")
    self.ui.git_frame.setStyleSheet(r".QFrame {image: url('assets//images//github.png')}")
    self.logger.debug(f"Load_Images_And_Icons : Logos seted")

    # Buttons icons

    # Settings
    self.ui.setting_btn.setStyleSheet(r".QPushButton {image: url('assets//images//settings.png')}")
    self.ui.setting_back_button.setStyleSheet(r".QPushButton {image: url('assets//images//back.png')}")
    self.ui.lang_apply_pushButton.setStyleSheet(r".QPushButton {image: url('assets//images//apply.png')}")
    self.ui.qss_apply_pushButton.setStyleSheet(r".QPushButton {image: url('assets//images//apply.png')}")
    self.ui.reset_qss_pushButton.setStyleSheet(r".QPushButton {image: url('assets//images//reset.png')}")
    self.ui.qss_apply_file_pushButton.setStyleSheet(r".QPushButton {image: url('assets//images//apply.png')}")
    self.ui.qss_file_pushButton.setStyleSheet(r".QPushButton {image: url('assets//images//qss-file.png')}")
    self.ui.check_key_pushButton.setStyleSheet(r".QPushButton {image: url('assets//images//check.png')}")

    # Pages

    # Work log page
    self.ui.back_work_button.setStyleSheet(r".QPushButton {image: url('assets//images//back.png')}")
    self.ui.next_work_button.setStyleSheet(r".QPushButton {image: url('assets//images//next.png')}")

    # Work result page
    self.ui.back_result_button.setStyleSheet(r".QPushButton {image: url('assets//images//back.png')}")
    self.ui.next_result_button.setStyleSheet(r".QPushButton {image: url('assets//images//next.png')}")

    self.logger.debug(f"Load_Images_And_Icons : Buttons icons seted")
