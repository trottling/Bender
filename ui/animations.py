from PyQt6.QtCore import QPropertyAnimation


def ChangePBarValue(self, val: int):
    self.logger.debug(f"ChangePBarValue : Animation from {self.ui.progressBar.value()} to {val}")
    animation = QPropertyAnimation(self.ui.progressBar, b"value", self)
    animation.setDuration(1000)
    animation.setStartValue(self.ui.progressBar.value())
    animation.setEndValue(val)
    animation.start()
