import sys

from PyQt6.QtWidgets import QApplication

from OnAppStart.setup_logger import Setup_logger
from OnAppStart.check_appdir import CheckAppDir
from ui.user_interface import User_UI

app_version = "1.0.0"

# Setup logger
logger = Setup_logger(app_version)
# Check App folder
appdir = CheckAppDir(logger)

if __name__ == '__main__':
    # Run GUI
    app = QApplication(sys.argv)
    User_UI(app_version, logger)
    sys.exit(app.exec())
