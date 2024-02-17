import ctypes
import logging
import platform
import sys
from logging import StreamHandler, Formatter


def Setup_logger(app_version, file_handler):
    logger = logging.getLogger(__name__)
    std_handler = StreamHandler(sys.stdout)
    std_handler.setFormatter(Formatter("%(asctime)s %(levelname)s %(message)s"))
    file_handler.setFormatter(Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(std_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

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
