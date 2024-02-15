import ctypes
import platform
import sys


def CheckUserOs(logger):
    os_name = platform.system()
    os_release = platform.release()
    os_version = platform.version()
    logger.info("OS Name: " + os_name)
    logger.info("OS Release: " + os_release)
    logger.info("OS Version: " + os_version)
    if platform.system() != "Windows":
        logger.error("Unsupported operating system")
        sys.exit("Unsupported operating system")


def IsUserAdmin(logger):
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        logger.error(f"IsUserAdmin() : Admin check failed, assuming not an admin. : {e}")
        return False
