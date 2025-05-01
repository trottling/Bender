from PyQt6 import uic, QtTest
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QSplashScreen, QGraphicsOpacityEffect

from ui.tools import get_rel_path


class SplashScreen(QSplashScreen):
    def __init__(self, ):
        super(QSplashScreen, self).__init__()
        self.info_label = None
        self.progress_bar = None

        uic.loadUi(get_rel_path(self, "assets/ui/splash.ui"), self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("Bender | Loading...")
        self.setPixmap(QPixmap(get_rel_path(self, "assets/images/splash.png")))

        # Проверяем, что info_label и progress_bar существуют
        if hasattr(self, 'info_label') and self.info_label is not None:
            self.effect = QGraphicsOpacityEffect(self.info_label)
            self.effect.setOpacity(1.0)
            self.info_label.setGraphicsEffect(self.effect)
        else:
            self.effect = QGraphicsOpacityEffect()
            self.effect.setOpacity(1.0)

    def change_pbar(self, percent: int, text: str):
        if self.progress_bar is not None:
            self.perc_anim(percent)
        if self.info_label is not None:
            self.text_anim(text)
        QtTest.QTest.qWait(150)

    def perc_anim(self, percent: int):
        if self.progress_bar is not None:
            animation = QPropertyAnimation(self.progress_bar, b"value", self)
            animation.setDuration(200)
            animation.setStartValue(self.progress_bar.value())
            animation.setEndValue(percent)
            animation.start()

    def text_anim(self, text: str):
        if self.info_label is None:
            return
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
