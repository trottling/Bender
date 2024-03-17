from configparser import ConfigParser

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow

from ui.side_grips import SideGrip
from ui.start_app import Start_App


class User_UI(QMainWindow):
    _gripSize = 16  # Corner grips size

    def __init__(self, app_version, logger, appdir) -> None:
        super().__init__()

        self.app_version = app_version
        self.logger = logger
        self.appdir = appdir

        self.ui = None

        # UI vars
        self.app_theme = None
        self.check_thread = None
        self.config_path = self.appdir + "\\" + "config.ini"
        self.config = ConfigParser()
        self.isSliderTimerStart = False
        self.start_tasks_running = False
        self.qss_input_showed = False
        self.result_list_model = None
        self.update_msg_show = False
        self.rel_path_dict = {}
        self.net_threads = 0
        self.data_workers = 0
        self.vulners_key = None

        # Validating vars
        self.validate_vulners_key = False
        self.start_tasks_running = False
        self.validate_os_sup_status = False
        self.validate_user_admin = False
        self.validate_net_status = False
        self.validate_vulners_status = False
        self.validate_vulners_key = False
        self.validate_loldrivers_status = False

        # Scanner vars
        self.res_good = 0
        self.res_bad = 0
        self.scan_th = None

        # Window actions
        self.window_size_full = False
        self.window_offset = None
        self.screen_width = 0
        self.screen_height = 0
        self.screen_width_cut = 0
        self.screen_height_cut = 0
        self.sideGrips = [
            SideGrip(self, QtCore.Qt.Edge.LeftEdge),
            SideGrip(self, QtCore.Qt.Edge.TopEdge),
            SideGrip(self, QtCore.Qt.Edge.RightEdge),
            SideGrip(self, QtCore.Qt.Edge.BottomEdge),
        ]
        # corner grips should be "on top" of everything, otherwise the side grips
        # will take precedence on mouse events, so we are adding them *after*;
        # alternatively, widget.raise_() can be used
        self.cornerGrips = [QtWidgets.QSizeGrip(self) for _ in range(4)]
        Start_App(self)

    #
    # Window move
    #

    def mousePressEvent(self, event):  # TODO Set to windows title insane all window
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
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
                                  -self.gripSize, -self.gripSize)

        # top left
        self.cornerGrips[0].setGeometry(QtCore.QRect(outRect.topLeft(), inRect.topLeft()))
        # top right
        self.cornerGrips[1].setGeometry(QtCore.QRect(outRect.topRight(), inRect.topRight()).normalized())
        # bottom right
        self.cornerGrips[2].setGeometry(QtCore.QRect(inRect.bottomRight(), outRect.bottomRight()))
        # bottom left
        self.cornerGrips[3].setGeometry(QtCore.QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        # left edge
        self.sideGrips[0].setGeometry(0, inRect.top(), self.gripSize, inRect.height())
        # top edge
        self.sideGrips[1].setGeometry(inRect.left(), 0, inRect.width(), self.gripSize)
        # right edge
        self.sideGrips[2].setGeometry(inRect.left() + inRect.width(), inRect.top(), self.gripSize, inRect.height())
        # bottom edge
        self.sideGrips[3].setGeometry(self.gripSize, inRect.top() + inRect.height(), inRect.width(), self.gripSize)

    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)
        self.updateGrips()
