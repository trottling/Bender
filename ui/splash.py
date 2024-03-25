from PyQt6 import uic, QtTest
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QSplashScreen, QGraphicsOpacityEffect

from ui.tools import GetRelPath


class SplashScreen(QSplashScreen):
    def __init__(self, ):
        super(QSplashScreen, self).__init__()
        self.info_label = None
        self.progressBar = None

        uic.loadUi(GetRelPath(self, "assets/ui/splash.ui"), self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("Bender | Loading...")
        self.setPixmap(QPixmap(GetRelPath(self, "assets/images/splash.png")))

        self.effect = QGraphicsOpacityEffect(self.info_label)
        self.effect.setOpacity(1.0)
        self.info_label.setGraphicsEffect(self.effect)

    def ChangePbar(self, percent: int, text: str):
        self.PercAnim(percent)
        self.TextAnim(text)
        QtTest.QTest.qWait(150)

    def PercAnim(self, percent: int):
        animation = QPropertyAnimation(self.progressBar, b"value", self)
        animation.setDuration(200)
        animation.setStartValue(self.progressBar.value())
        animation.setEndValue(percent)
        animation.start()

    def TextAnim(self, text: str):
        # Hide
        anim = QPropertyAnimation(self.effect, b"opacity", self)
        anim.setDuration(100)
        anim.setStartValue(self.effect.opacity())
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        anim.start()
        QtTest.QTest.qWait(100)

        # Change Text
        self.info_label.setText(text)

        # Show
        anim = QPropertyAnimation(self.effect, b"opacity", self)
        anim.setDuration(100)
        anim.setStartValue(self.effect.opacity())
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        anim.start()
