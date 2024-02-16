import logging
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from OnAppStart.check_run_environment import IsUserAdmin


def Setup_logger(app_version, config):
    logger = logging.getLogger(__name__)
    std_handler = StreamHandler(sys.stdout)
    logger.addHandler(std_handler)

    if config['debug']:
        logger.setLevel(logging.DEBUG)

    if config['debug_file'] is not None:
        try:
            file_handler = RotatingFileHandler(config['debug_file'], maxBytes=1024 * 1024)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error(f"Unable to create log file for debug : {config['debug_file']} : {e}")

    logger.debug(f"Python {sys.version}")
    logger.debug(f"Application version: {app_version}")
    logger.debug(f"Run args : {config}")
    logger.debug(f"Run as Admin : {IsUserAdmin(logger)}")

    return logger
