from configparser import ConfigParser
import os

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow

from bender.ui.side_grips import SideGrip
from bender.ui.start_app import start_app


class UserUI(QMainWindow):
    _grip_size = 16  # Corner grips size

    def __init__(self, app_version, app_dir, splash) -> None:
        super().__init__()

        self.app_version = app_version
        self.app_dir = app_dir
        self.splash = splash

        self.ui = None

        # UI vars
        self.app_theme = None
        self.check_thread = None
        self.config_path = os.path.join(self.app_dir, "config.ini")
        self.config = ConfigParser()
        self.is_slider_timer_start = False
        self.start_tasks_running = False
        self.qss_input_showed = False
        self.result_list_model = None
        self.update_msg_show = False
        self.rel_path_dict = {}
        self.net_threads = 0
        self.data_workers = 0
        self.port_workers = 0
        self.vulners_key = None

        # Validating vars
        self.validate_vulners_key = False
        self.start_tasks_running = False
        self.validate_os_sup_status = False
        self.validate_user_admin = False
        self.validate_net_status = False
        self.validate_vulners_status = False
        self.validate_loldrivers_status = False

        # Scanner vars
        self.res_good = 0
        self.res_bad = 0
        self.scan_th = None
        self.port_dict = {}

        # Window actions
        self.window_size_full = False
        self.window_offset = None
        self.screen_width = 0
        self.screen_height = 0
        self.screen_width_cut = 0
        self.screen_height_cut = 0
        self.side_grips = [
            SideGrip(self, QtCore.Qt.Edge.LeftEdge),
            SideGrip(self, QtCore.Qt.Edge.TopEdge),
            SideGrip(self, QtCore.Qt.Edge.RightEdge),
            SideGrip(self, QtCore.Qt.Edge.BottomEdge),
        ]
        # corner grips should be "on top" of everything, otherwise the side grips
        # will take precedence on mouse events, so we are adding them *after*;
        # alternatively, widget.raise_() can be used
        self.corner_grips = [QtWidgets.QSizeGrip(self) for _ in range(4)]

        # Run app
        start_app(self)

    #
    # Window move
    #

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.window_offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.window_offset is not None and event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.window_offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.window_offset = None
        super().mouseReleaseEvent(event)

    #
    # Window resize - stackoverflow.com/questions/62807295
    #

    @property
    def grip_size(self):
        return self._grip_size

    def set_grip_size(self, size):
        if size == self._grip_size:
            return
        self._grip_size = max(2, size)
        self.update_grips()

    def update_grips(self):
        self.setContentsMargins(*[self.grip_size] * 4)

        out_rect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        in_rect = out_rect.adjusted(self.grip_size, self.grip_size,
                                  -self.grip_size, -self.grip_size)

        # top left
        self.corner_grips[0].setGeometry(QtCore.QRect(out_rect.topLeft(), in_rect.topLeft()))
        # top right
        self.corner_grips[1].setGeometry(QtCore.QRect(out_rect.topRight(), in_rect.topRight()).normalized())
        # bottom right
        self.corner_grips[2].setGeometry(QtCore.QRect(in_rect.bottomRight(), out_rect.bottomRight()))
        # bottom left
        self.corner_grips[3].setGeometry(QtCore.QRect(out_rect.bottomLeft(), in_rect.bottomLeft()).normalized())

        # left edge
        self.side_grips[0].setGeometry(0, in_rect.top(), self.grip_size, in_rect.height())
        # top edge
        self.side_grips[1].setGeometry(in_rect.left(), 0, in_rect.width(), self.grip_size)
        # right edge
        self.side_grips[2].setGeometry(in_rect.left() + in_rect.width(), in_rect.top(), self.grip_size, in_rect.height())
        # bottom edge
        self.side_grips[3].setGeometry(self.grip_size, in_rect.top() + in_rect.height(), in_rect.width(), self.grip_size)

    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)
        self.update_grips()
