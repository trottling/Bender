import darkdetect


def GetWindowsTheme(logger) -> str:
    if darkdetect.isDark():
        logger.
        print("Dark mode is enabled.")
    else:
        print("Dark mode is not enabled.")
