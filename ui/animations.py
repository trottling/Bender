import sys

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QGraphicsOpacityEffect

from ui.tools import GetRelPath


def App_Open_Anim(self):
    self.logger.debug(f"App_Open_Anim : Animation")

    if self.window_size_full:
        self.ui.showMaximized()
        self.logger.debug("App_Open_Anim : showMaximized")

    self.ui.setWindowOpacity(0)
    self.ui.show()
    animation = QPropertyAnimation(self.ui, b'windowOpacity', self)
    animation.setDuration(250)
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
    animation.setDuration(250)
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


def ElemShowAnim(self, elem, show=True):
    self.logger.debug("ElemShowAnim : Show")

    elem.setGraphicsEffect(QGraphicsOpacityEffect())
    if show:
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


def ElemHideAnim(self, elem, hide=True):
    self.logger.debug("ElemHideAnim : Hide")

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
        lambda: elem.setGraphicsEffect(None))
    if hide:
        anim.finished.connect(
            lambda: elem.hide())

    anim.start()


def ImageChangeAnim(self, elem, image, elem_type, elem_style):
    #
    # Move opacity from 1 to 0 --> Change Image  -->  Move opacity from 0 to 1 | total 250 ms
    # Part 1
    #

    self.logger.debug("ImageChangeAnim : Change Image")

    elem.setGraphicsEffect(QGraphicsOpacityEffect().setOpacity(1.0))

    effect = QGraphicsOpacityEffect(elem)
    effect.setOpacity(1.0)
    elem.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity", self)
    anim.setDuration(175)
    anim.setStartValue(effect.opacity())
    anim.setEndValue(0.0)
    anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    anim.finished.connect(
        lambda: ImageChangeAnimShow(self, elem, image, elem_type, elem_style))

    anim.start()


def ImageChangeAnimShow(self, elem, image, elem_type, elem_style):
    #
    # Part 2
    #

    try:
        elem.setStyleSheet(
            "." + elem_type + "{" + elem_style + ": url('" + GetRelPath(self, image) + "')}")
    except Exception as e:
        self.logger.error(f"ImageChangeAnimShow : {e}")
        return

    elem.setGraphicsEffect(QGraphicsOpacityEffect().setOpacity(0.0))

    effect = QGraphicsOpacityEffect(elem)
    effect.setOpacity(0.0)
    elem.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity", self)
    anim.setDuration(175)
    anim.setStartValue(effect.opacity())
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.OutQuad)
    anim.start()
    self.logger.debug("ImageChangeAnimShow : Image Changed")


def TextChangeAnim(self, elem, text):
    #
    # Move opacity from 1 to 0 --> Change text  -->  Move opacity from 0 to 1 | total 250 ms
    # Part 1
    #

    self.logger.debug("TextChangeAnim : Change Text")

    elem.setGraphicsEffect(QGraphicsOpacityEffect().setOpacity(1.0))

    effect = QGraphicsOpacityEffect(elem)
    effect.setOpacity(1.0)
    elem.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity", self)
    anim.setDuration(175)
    anim.setStartValue(effect.opacity())
    anim.setEndValue(0.0)
    anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    anim.finished.connect(
        lambda: TextChangeAnimShow(self, elem, text))

    anim.start()


def TextChangeAnimShow(self, elem, text):
    #
    # Part 2
    #

    try:
        elem.setText(text)
    except Exception as e:
        self.logger.error(f"ImageChangeAnimShow : {e}")
        return

    elem.setGraphicsEffect(QGraphicsOpacityEffect().setOpacity(0.0))

    effect = QGraphicsOpacityEffect(elem)
    effect.setOpacity(0.0)
    elem.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity", self)
    anim.setDuration(175)
    anim.setStartValue(effect.opacity())
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.OutQuad)
    anim.start()
    self.logger.debug("TextChangeAnimShow : Text Changed")
