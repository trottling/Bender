import sys

from PyQt6.QtWidgets import QApplication

from on_start.check_appdir import CheckAppDir
from on_start.check_instance import Check_Instance
from on_start.setup_logger import Setup_logger
from ui.classes import User_UI

app_version = "2.0.0"

# Check Instance
Check_Instance()
# Check App folder
appdir, file_handler = CheckAppDir()
# Setup logger
logger = Setup_logger(app_version, file_handler, appdir)

if __name__ == '__main__':
    # Run GUI
    app = QApplication(sys.argv)
    User_UI(app_version, logger, appdir)
    sys.exit(app.exec())
