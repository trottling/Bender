import os
from logging.handlers import RotatingFileHandler


def CheckAppDir():
    appdata_path = os.getenv('APPDATA')
    app_folder = os.path.join(appdata_path + "\\" + "Windows-Vulnerability-Scanner")

    if not os.path.exists(app_folder):
        os.mkdir(app_folder)

    style_folder = app_folder + "\\" + "saved_qss"

    if not os.path.exists(style_folder):
        os.mkdir(style_folder)

    log_file = app_folder + "\\" + "debug_log.txt"

    #
    # If log file doesn't exist, he will be create in check config func
    #

    if os.path.isfile(log_file):
        try:
            os.remove(log_file)
        except PermissionError:
            pass
    try:
        file_handler = RotatingFileHandler(log_file, maxBytes=0)
        return app_folder, file_handler
    except Exception:
        return app_folder, None
