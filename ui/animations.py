from PyQt6.QtCore import QPropertyAnimation


def ChangePBarValue(self, val: int):
    self.logger.debug(f"ChangePBarValue : Animation from {self.ui.progressBar.value()} to {val}")
    animation = QPropertyAnimation(self.ui.progressBar, b"value", self)
    animation.setDuration(1000)
    animation.setStartValue(self.ui.progressBar.value())
    animation.setEndValue(val)
    animation.start()


def Hide_element(self, func, element):
    pass


def App_Open_Anim(self):
    self.logger.debug(f"App_Open_Anim : Animation")

    self.ui.setWindowOpacity(0)
    self.ui.show()
    animation = QPropertyAnimation(self.ui, b'windowOpacity', self)
    animation.setDuration(500)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.start()

    self.stackedWidget.setCurrentIndex(0)
    self.logger.debug(f"Load_UI : UI showed")


def App_Exit_Anim(self):
    self.logger.debug(f"App_Close_Anim : Animation")

    animation = QPropertyAnimation(self.ui, b'windowOpacity', self)
    animation.finished.connect(self.close)
    animation.setDuration(500)
    animation.setStartValue(1.0)
    animation.setEndValue(0.0)
    animation.start()
