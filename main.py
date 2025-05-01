import sys

from PyQt6.QtWidgets import QApplication

from on_start.check_appdir import check_app_dir
from on_start.check_instance import check_instance
from on_start.setup_logger import setup_logger
from ui.splash import SplashScreen
from ui.user_interface import UserUI

app_version = "2.2.3"

if __name__ == '__main__':
    # Check Instance
    check_instance()

    # Start splash
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()

    # Check App folder
    appdir, file_handler = check_app_dir()

    # Setup logger
    logger = setup_logger(app_version, file_handler, appdir)

    # Run GUI
    UserUI(app_version, logger, appdir, splash)
    sys.exit(app.exec())
