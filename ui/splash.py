try:
    import pyi_splash
except ModuleNotFoundError:
    pass


# The splash screen is controlled from within Python by the pyi_splash module,
# which can be imported at runtime. This module cannot be installed by a
# package manager because it is part of PyInstaller and is included as
# needed. This module must be imported within the Python program.

def SplashText(self):
    try:
        pyi_splash.update_text("Loading")
    except:
        pass
    self.logger.debug("SplashText : Text change")


def StopSplash(self):
    try:
        pyi_splash.close()
    except:
        pass
    self.logger.debug("StopSplash : Stop")
