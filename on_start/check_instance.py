import sys
import wmi


def Check_Instance():
    if sys.argv[0] in wmi.WMI().Win32_Process():
        sys.exit(-1)


