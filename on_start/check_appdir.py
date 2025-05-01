import os
from logging.handlers import RotatingFileHandler
from loguru import logger


def CheckAppDir():
    appdata_path = os.getenv('APPDATA')
    app_folder = os.path.join(appdata_path, "Windows-Vulnerability-Scanner")

    try:
        os.makedirs(app_folder, exist_ok=True)
        logger.info(f"App folder checked/created: {app_folder}")
    except Exception as e:
        logger.error(f"[CheckAppDir] Failed to create app folder: {e}")

    style_folder = os.path.join(app_folder, "saved_qss")
    try:
        os.makedirs(style_folder, exist_ok=True)
        logger.info(f"Style folder checked/created: {style_folder}")
    except Exception as e:
        logger.error(f"[CheckAppDir] Failed to create style folder: {e}")

    log_file = os.path.join(app_folder, "debug_log.txt")

    # If the log file exists, remove it (will be recreated in check config func)
    if os.path.isfile(log_file):
        try:
            os.remove(log_file)
            logger.info(f"Old log file removed: {log_file}")
        except PermissionError as e:
            logger.error(f"[CheckAppDir] PermissionError when removing log file: {e}")
        except Exception as e:
            logger.error(f"[CheckAppDir] Error when removing log file: {e}")
    try:
        file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=3)
        logger.debug(f"RotatingFileHandler created for: {log_file}")
        return app_folder, file_handler
    except Exception as e:
        logger.error(f"[CheckAppDir] Failed to create RotatingFileHandler: {e}")
        return app_folder, None
