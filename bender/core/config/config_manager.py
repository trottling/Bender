import os
import json

def get_config_path(self):
    return self.config_path

DEFAULT_CONFIG = {
    "selected_modules": [],
    "modules_params": {},
    "threads": 2,
    "lang": "ru",
    "theme": "dark"
}

def load_config(self):
    config_path = get_config_path(self)
    if not os.path.exists(config_path):
        save_config(self, DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(self, config):
    config_path = get_config_path(self)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2) 