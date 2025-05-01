import os
import sys
import ctypes

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

from bender.core.on_run.check_appdir import check_app_dir
from bender.core.on_run.check_instance import check_instance
from bender.core.on_run.check_admin import check_admin
from bender.ui.splash import SplashScreen
from bender.ui.user_interface import UserUI

app_version = "2.2.3"

if __name__ == '__main__':
    # Check admin rights and relaunch if needed
    if  check_admin():
        logger.warning('App is not running as administrator. Relaunching with admin rights...')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join([f'"{arg}"' for arg in sys.argv]), None, 1)
        sys.exit(0)

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
