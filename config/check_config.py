import os


def CheckConfigFile(self):
    if not os.path.isfile(self.config_path) or open(self.config_path, "r").read() == "" or open(self.config_path,
                                                                                                "r").read() is None:
        open(self.config_path, "w").close()
        self.logger.debug(f"CheckConfigFile : {self.config_path} : config created")
        self.config.read(self.config_path)
        if not self.config.has_section('main'):
            self.config.add_section('main')
        self.logger.debug(f"CheckConfigFile : main : add section")
        return False
    else:
        self.logger.debug(f"CheckConfigFile : {self.config_path} : config exist")
        return True
