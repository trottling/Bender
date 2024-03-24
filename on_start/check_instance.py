import os
import sys

import wmi


def Check_Instance():
    # Check for double running

    # Proc name == file name (if it's .exe file)
    name = os.path.basename(sys.argv[0])
    count = 0

    if name in [process.Name for process in wmi.WMI().Win32_Process()]:
        count = count + 1

    if count > 1:
        sys.exit(-1)
