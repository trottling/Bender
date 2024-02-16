import ctypes
import logging
import platform
import sys
import time
from logging import StreamHandler
from logging.handlers import RotatingFileHandler


def Setup_logger(app_version):
    logger = logging.getLogger(__name__)
    std_handler = StreamHandler(sys.stdout)
    logger.addHandler(std_handler)
    logger.setLevel(logging.DEBUG)

    logger.debug(time.strftime("%Y-%m-%d | %H:%M:%S", time.localtime()))
    logger.debug(f"Python {sys.version}")
    logger.debug(f"Application version: {app_version}")
    logger.debug(f"Run as Admin : {Check_Admin(logger)}")
    logger.debug("OS Name: " + platform.system())
    logger.debug("OS Release: " + platform.release())
    logger.debug("OS Version: " + platform.version())

    return logger


def Check_Admin(logger):
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        logger.error(f"IsUserAdmin() : Admin check failed, assuming not an admin. : {e}")
        return False
