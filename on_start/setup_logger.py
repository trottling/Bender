from loguru import logger
import ctypes
import platform
import sys


def check_admin(log=None):
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        if log:
            log.error(f"IsUserAdmin() : Admin check failed, assuming not an admin. : {e}")
        return False
