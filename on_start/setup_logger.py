from loguru import logger
import ctypes
import platform
import sys


def setup_logger(app_version, file_handler, appdir):
    logger.remove()
    log_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {module}:{function}:{line} - {message}"
    logger.add(sys.stdout, format=log_format, level="DEBUG")
    if file_handler is not None:
        logger.add(file_handler.baseFilename, rotation="20 MB", retention=3, level="DEBUG", format=log_format)
    logger.info(f"Log path :  {appdir}/debug_log.txt")
    logger.info(f"Python {sys.version}")
    logger.info(f"Application version: {app_version}")
    logger.info(f"Run as Admin : {check_admin(logger)}")
    logger.info("OS Name: " + platform.system())
    logger.info("OS Release: " + platform.release())
    logger.info("OS Version: " + platform.version())
    return logger


def check_admin(log):
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        log.error(f"IsUserAdmin() : Admin check failed, assuming not an admin. : {e}")
        return False
