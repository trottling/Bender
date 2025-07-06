import os
import sys
from PyQt6 import uic
import importlib.util
import platform

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

class HardwareModuleController:
    supported_os = ["Windows", "Linux"]  # список поддерживаемых ОС

    def __init__(self):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = resource_path(os.path.join(module_dir, 'module.ui'))
        result_ui_path = resource_path(os.path.join(module_dir, 'result.ui'))
        self.ui = uic.loadUi(ui_path)
        self.result_ui = uic.loadUi(result_ui_path)
        logic_path = os.path.join(module_dir, 'hardware.py')
        spec = importlib.util.spec_from_file_location('hardware_logic', logic_path)
        self.logic = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.logic)
        self.last_result = {}
        self.os_supported = self.is_os_supported()
        if not self.os_supported:
            self.ui.setDisabled(True)

    def is_os_supported(self):
        current_os = platform.system()
        return current_os in self.supported_os

    def get_params(self):
        params = {}
        for name, widget in self.ui.__dict__.items():
            if name.endswith('CheckBox'):
                params[name] = widget.isChecked()
            # Можно добавить обработку других типов виджетов
        return params

    def run(self, log_func=None):
        if not self.os_supported:
            if log_func:
                log_func(f"Module not supported on this OS: {platform.system()}", "❌")
            return {"error": f"Module not supported on this OS: {platform.system()}"}
        params = self.get_params()
        result = self.logic.run(params, log_func=log_func)
        self.last_result = result
        return result

    def get_last_result(self):
        return self.last_result 