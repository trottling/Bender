import os
from loguru import logger


def check_config_file(self):
    config_exists = os.path.isfile(self.config_path)
    is_empty = True
    if config_exists:
        try:
            with open(self.config_path, "r") as f:
                content = f.read()
                is_empty = (content.strip() == "")
        except Exception as e:
            logger.error(f"check_config_file: error reading config: {e}")
            is_empty = True
    if not config_exists or is_empty:
        try:
            with open(self.config_path, "w") as f:
                pass
            logger.info(f"check_config_file: {self.config_path} created")
        except Exception as e:
            logger.error(f"check_config_file: error creating config: {e}")
        self.config.read(self.config_path)
        if not self.config.has_section('main'):
            self.config.add_section('main')
        logger.info(f"check_config_file: 'main' section added")
        return False
    else:
        logger.info(f"check_config_file: {self.config_path} exists")
        return True
