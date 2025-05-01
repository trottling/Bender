import os
import sys
import wmi
from loguru import logger


def check_instance():
    # Check for double running
    exe_path = os.path.abspath(sys.argv[0]).lower()
    count = 0
    for process in wmi.WMI().Win32_Process():
        try:
            proc_path = (process.ExecutablePath or '').lower()
            if proc_path == exe_path:
                count += 1
        except Exception as e:
            logger.error(f"[Check_Instance] WMI process error: {e}")
            continue
    if count > 1:
        logger.critical("[Check_Instance] Another instance detected. Exiting.")
        sys.exit(-1)
    logger.info("Instance check passed: no duplicate running.")
