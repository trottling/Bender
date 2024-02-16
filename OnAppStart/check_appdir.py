import os
from logging import StreamHandler
from logging.handlers import RotatingFileHandler


def CheckAppDir(logger):
    appdata_path = os.getenv('APPDATA')
    app_folder = os.path.join(appdata_path + "\\" + "Windows-Vulnerability-Scanner")

    logger.debug(f"CheckAppDir : app_folder : {app_folder}")

    if not os.path.exists(app_folder):
        os.mkdir(app_folder)
        logger.debug(f"CheckAppDir : {app_folder} has been created")
    else:
        logger.debug(f"CheckAppDir : {app_folder} already exists")

    style_folder = app_folder + "\\" + "saved_qss"

    if not os.path.exists(style_folder):
        os.mkdir(style_folder)
        logger.debug(f"CheckAppDir : {style_folder} has been created")
    else:
        logger.debug(f"CheckAppDir : {style_folder} already exists")

    log_file = app_folder + "\\" + "debug_log.txt"
    try:
        file_handler = RotatingFileHandler(log_file, maxBytes=0)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.error(f"Unable to create log file for debug : {log_file} : {e}")
