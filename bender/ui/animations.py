import sys

from PyQt6 import QtTest, QtCore
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QTimer, QRect
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from loguru import logger

from bender.ui.tools import get_rel_path


def app_open_anim(self):
    logger.debug(f"app_open_anim : Animation")

    if self.window_size_full:
        self.ui.showMaximized()
        logger.debug("app_open_anim : showMaximized")

    self.ui.setWindowOpacity(0.0)
    self.ui.show()
    self.splash.finish(self.ui)
    animation = QPropertyAnimation(self.ui, b'windowOpacity', self)
    animation.setDuration(250)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.start()

    self.ui.stackedWidget.setCurrentIndex(0)
    logger.debug(f"app_open_anim : UI showed")


def app_exit_anim(self):
    logger.debug(f"App_Close_Anim : Animation")

    animation = QPropertyAnimation(self.ui, b'windowOpacity', self)
    animation.finished.connect(lambda: (logger.debug("App_Exit_Anim : ******* EXIT *******"), sys.exit(0)))
    animation.setDuration(250)
    animation.setStartValue(1.0)
    animation.setEndValue(0.0)
    animation.start()


# Slide animation for QStackedWidget
_slide_animations = []  # Global list to keep references

def stacked_widget_change_page(stacked_widget, new_index, direction='left', duration=450):
    current_index = stacked_widget.currentIndex()
    if current_index == new_index:
        return

    current_widget = stacked_widget.widget(current_index)
    next_widget = stacked_widget.widget(new_index)
    width = stacked_widget.frameRect().width()
    height = stacked_widget.frameRect().height()

    # Direction offsets
    if direction == 'left':
        offset_x, offset_y = width, 0
    elif direction == 'right':
        offset_x, offset_y = -width, 0
    elif direction == 'up':
        offset_x, offset_y = 0, height
    elif direction == 'down':
        offset_x, offset_y = 0, -height
    else:
        offset_x, offset_y = width, 0  # default left

    # Prepare the next widget
    next_widget.setGeometry(QRect(offset_x, offset_y, width, height))
    next_widget.show()

    # Animations
    anim_current = QPropertyAnimation(current_widget, b"geometry")
    anim_current.setDuration(duration)
    anim_current.setStartValue(QRect(0, 0, width, height))
    anim_current.setEndValue(QRect(-offset_x, -offset_y, width, height))
    anim_current.setEasingCurve(QEasingCurve.Type.InOutQuad)

    anim_next = QPropertyAnimation(next_widget, b"geometry")
    anim_next.setDuration(duration)
    anim_next.setStartValue(QRect(offset_x, offset_y, width, height))
    anim_next.setEndValue(QRect(0, 0, width, height))
    anim_next.setEasingCurve(QEasingCurve.Type.InOutQuad)

    # Keep references
    _slide_animations.append(anim_current)
    _slide_animations.append(anim_next)

    def on_finished():
        stacked_widget.setCurrentIndex(new_index)
        current_widget.hide()
        _slide_animations.clear()

    anim_next.finished.connect(on_finished)
    anim_current.start()
    anim_next.start()

def elem_show_anim(self, elem, show=True, dur=250):
    logger.debug("ElemShowAnim : Show")

    elem.setGraphicsEffect(QGraphicsOpacityEffect())
    if show:
        elem.show()

    effect = QGraphicsOpacityEffect(elem)
    elem.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity", self)
    anim.setDuration(dur)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    anim.finished.connect(lambda: effect.setEnabled(False))

    anim.start()


def elem_hide_anim(self, elem, hide=True, dur=250):
    logger.debug("ElemHideAnim : Hide")

    elem.setGraphicsEffect(QGraphicsOpacityEffect().setOpacity(1.0))

    effect = QGraphicsOpacityEffect(elem)
    effect.setOpacity(1.0)
    elem.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity", self)
    anim.setDuration(dur)
    anim.setStartValue(effect.opacity())
    anim.setEndValue(0.0)
    anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    anim.finished.connect(lambda: effect.setEnabled(False))
    if hide:
        anim.finished.connect(lambda: elem.hide())

    anim.start()


def image_change_anim(self, elem, image):
    #
    # Move opacity from 1 to 0 --> Change Image --> Move opacity from 0 to 1 | total 250 ms
    # Part 1
    #

    logger.debug("ImageChangeAnim : Change Image")

    elem.setGraphicsEffect(QGraphicsOpacityEffect().setOpacity(1.0))

    effect = QGraphicsOpacityEffect(elem)
    effect.setOpacity(1.0)
    elem.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity", self)
    anim.setDuration(175)
    anim.setStartValue(effect.opacity())
    anim.setEndValue(0.0)
    anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    anim.finished.connect(lambda: image_change_anim_show(self, elem, image))

    anim.start()


def image_change_anim_show(self, elem, image):
    #
    # Part 2
    #

    try:
        pixmap = QPixmap(get_rel_path(self, image))
        elem.setPixmap(pixmap)
    except Exception as e:
        logger.error(f"ImageChangeAnimShow : {e}")
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
    anim.finished.connect(lambda: effect.setEnabled(False))
    anim.start()
    logger.debug("ImageChangeAnimShow : Image Changed")


def text_change_anim(self, elem, text):
    #
    # Move opacity from 1 to 0 --> Change text --> Move opacity from 0 to 1 | total 250 ms
    # Part 1
    #

    logger.debug("TextChangeAnim : Change Text")

    elem.setGraphicsEffect(QGraphicsOpacityEffect().setOpacity(1.0))

    effect = QGraphicsOpacityEffect(elem)
    effect.setOpacity(1.0)
    elem.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity", self)
    anim.setDuration(175)
    anim.setStartValue(effect.opacity())
    anim.setEndValue(0.0)
    anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    anim.finished.connect(lambda: text_change_anim_show(self, elem, text))

    anim.start()


def text_change_anim_show(self, elem, text):
    #
    # Part 2
    #

    try:
        elem.setText(text)
    except Exception as e:
        logger.error(f"ImageChangeAnimShow : {e}")
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
    anim.finished.connect(lambda: effect.setEnabled(False))
    anim.start()
    logger.debug("TextChangeAnimShow : Text Changed")


def show_err_message(self, msg):
    if not self.ui.alert_msg.isVisible():
        self.ui.alert_msg.setText(str(msg))
        logger.debug(f"ShowErrMessage: {msg}")
        elem_show_anim(self, self.ui.alert_msg)
        QTimer.singleShot(5000, lambda: elem_hide_anim(self, self.ui.alert_msg))


# noinspection PyArgumentList
def set_work_page_gif(self):
    QtTest.QTest.qWait(500)
    gif = QMovie(get_rel_path(self, r"assets\gifs\loading.gif"))
    gif.setFormat(b"gif")
    gif.setScaledSize(QtCore.QSize(45, 45))
    self.ui.image_work_progress.setMovie(gif)
    gif.start()
    elem_show_anim(self, self.ui.image_work_progress, dur=200)
    elem_show_anim(self, self.ui.label_work_progress, dur=200)
    QtTest.QTest.qWait(500)


def change_work_elems(self):
    text_change_anim(self, self.ui.label_work_progress, "Done")
    self.ui.image_work_progress.clear()
    image_change_anim(self, self.ui.image_work_progress, r"assets\images\bender-medium.png")
    elem_hide_anim(self, self.ui.label_win_warn)

    QtTest.QTest.qWait(1000)

    elem_show_anim(self, self.ui.next_work_btn)


def update_work_page_stat(self, stat):
    if stat == "good":
        self.res_good += 1
        text_change_anim(self, self.ui.label_scan_successful_len, str(self.res_good))
    if stat == "bad":
        self.res_bad += 1
        text_change_anim(self, self.ui.label_scan_error_len, str(self.res_bad))
