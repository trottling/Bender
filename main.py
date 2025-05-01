import os
import sys

from loguru import logger

appdata_path = os.getenv('APPDATA')
app_folder = os.path.join(appdata_path, "Windows-Vulnerability-Scanner")
os.makedirs(app_folder, exist_ok=True)
log_file = os.path.join(app_folder, "debug_log.txt")

logger.remove()
log_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {module}:{function}:{line} - {message}"
logger.add(sys.stdout, format=log_format, level="DEBUG", colorize=True, catch=True, backtrace=True, diagnose=True)
logger.add(log_file, rotation="20 MB", retention=3, level="DEBUG", format=log_format, catch=True, backtrace=True, diagnose=True)
logger.info(f"Log path :  {log_file}")
logger.info(f"Python {sys.version}")
logger.info("Application version: 2.2.3")

from PyQt6.QtWidgets import QApplication

from on_start.check_appdir import check_app_dir
from on_start.check_instance import check_instance
from ui.splash import SplashScreen
from ui.user_interface import UserUI

app_version = "2.3.0"

if __name__ == '__main__':
    # Check Instance
    check_instance()

    # Start splash
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()

    # Check App folder
    app_dir, file_handler = check_app_dir()

    # Run GUI
    UserUI(app_version, app_dir, splash)
    sys.exit(app.exec())
