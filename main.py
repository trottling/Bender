import sys

from PySide6.QtWidgets import QApplication

from OnAppStart.setup_logger import Setup_logger
from OnAppStart.setup_args import Setup_args
from OnAppStart.check_run_environment import CheckUserOs
from ui.user_interface import User_UI

app_version = "1.0.0"

# Setup args
config = Setup_args()
# Setup logger
logger = Setup_logger(app_version, config)
# Check environment
CheckUserOs(logger)

if __name__ == '__main__':
    # Run GUI
    app = QApplication(sys.argv)
    window = User_UI(app_version, logger)
    app.exec()
