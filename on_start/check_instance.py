import os
import sys

import wmi


def Check_Instance():
    if os.path.basename(sys.argv[0]) in [process.Name for process in wmi.WMI().Win32_Process()]:
        sys.exit(-1)
