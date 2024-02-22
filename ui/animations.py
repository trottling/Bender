import sys

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QGraphicsOpacityEffect


def App_Open_Anim(self):
    self.logger.debug(f"App_Open_Anim : Animation")

    self.ui.setWindowOpacity(0)
    self.ui.show()
    animation = QPropertyAnimation(self.ui, b'windowOpacity', self)
    animation.setDuration(500)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.start()

    self.ui.stackedWidget.setCurrentIndex(0)
    self.logger.debug(f"Load_UI : UI showed")


def App_Exit_Anim(self):
    self.logger.debug(f"App_Close_Anim : Animation")

    animation = QPropertyAnimation(self.ui, b'windowOpacity', self)
    animation.finished.connect(lambda: ((self.logger.debug(
        "App_Exit_Anim : ******* EXIT *******"), sys.exit(0))))
    animation.setDuration(500)
    animation.setStartValue(1.0)
    animation.setEndValue(0.0)
    animation.start()


def ChangePBarValue(self, val: int):
    self.logger.debug(f"ChangePBarValue : Animation to {val}%")
    animation = QPropertyAnimation(self.ui.progressBar, b"value", self)
    animation.setDuration(1000)
    animation.setStartValue(self.ui.progressBar.value())
    animation.setEndValue(val)
    animation.start()


def StackedWidgetChangePage(self, page_to: int):
    self.logger.debug(f"StackedWidgetAnimation : move to {page_to}")
    current_widget = self.ui.stackedWidget.currentWidget()

    effect = QGraphicsOpacityEffect(current_widget)
    effect.setOpacity(1.0)
    current_widget.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity", self)
    anim.setDuration(250)
    anim.setStartValue(effect.opacity())
    anim.setEndValue(0.0)
    anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    anim.finished.connect(
        lambda: (self.ui.stackedWidget.setCurrentIndex(page_to), current_widget.setGraphicsEffect(None)))

    anim.start()


def ElemShowAnim(self, elem):
    self.logger.debug(f"ElemShowAnim : Show {elem}")

    elem.setGraphicsEffect(QGraphicsOpacityEffect())
    elem.show()

    effect = QGraphicsOpacityEffect(elem)
    elem.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity", self)
    anim.setDuration(250)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    anim.finished.connect(lambda: elem.setGraphicsEffect(None))

    anim.start()


def ElemHideAnim(self, elem):
    self.logger.debug(f"ElemHideAnim : Show {elem}")

    elem.setGraphicsEffect(QGraphicsOpacityEffect().setOpacity(1.0))

    effect = QGraphicsOpacityEffect(elem)
    effect.setOpacity(1.0)
    elem.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity", self)
    anim.setDuration(250)
    anim.setStartValue(effect.opacity())
    anim.setEndValue(0.0)
    anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    anim.finished.connect(
        lambda: (elem.setGraphicsEffect(None), elem.hide()))

    anim.start()
