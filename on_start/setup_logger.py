from loguru import logger
import ctypes
import platform
import sys


def Setup_logger(app_version, file_handler, appdir):
    logger.remove()
    logger.add(sys.stdout, format="{time} {level} {message}", level="DEBUG")
    if file_handler is not None:
        logger.add(file_handler.baseFilename, rotation="1 MB", retention=3, level="DEBUG", format="{time} {level} {message}")
    logger.info(f"Log path :  {appdir}/debug_log.txt")
    logger.info(f"Python {sys.version}")
    logger.info(f"Application version: {app_version}")
    logger.info(f"Run as Admin : {Check_Admin(logger)}")
    logger.info("OS Name: " + platform.system())
    logger.info("OS Release: " + platform.release())
    logger.info("OS Version: " + platform.version())
    return logger


def Check_Admin(logger):
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        logger.error(f"IsUserAdmin() : Admin check failed, assuming not an admin. : {e}")
        return False
