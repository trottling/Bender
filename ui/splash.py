from PyQt6 import uic, QtTest
from PyQt6.QtCore import Qt, QPropertyAnimation
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QSplashScreen

from ui.tools import GetRelPath


class SplashScreen(QSplashScreen):
    def __init__(self, ):
        super(QSplashScreen, self).__init__()
        self.progressBar = None

        uic.loadUi(GetRelPath(self, "assets/ui/splash.ui"), self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("Bender | Loading...")
        self.setPixmap(QPixmap(GetRelPath(self, "assets/images/splash.png")))

    def ChangePbar(self, percent: int, text: str):
        self.PercAnim(percent)
        self.progressBar.setFormat(text)
        QtTest.QTest.qWait(200)

    def PercAnim(self, percent: int):
        animation = QPropertyAnimation(self.progressBar, b"value", self)
        animation.setDuration(200)
        animation.setStartValue(self.progressBar.value())
        animation.setEndValue(percent)
        animation.start()
