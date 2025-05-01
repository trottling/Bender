from bender.core.config.read_config import load_settings
from bender.core.start_tasks import run_start_tasks
from bender.ui.animations import app_open_anim
from bender.ui.buttons import connect_buttons
from bender.ui.hide_elements import hide_elements
from bender.ui.images import load_images_and_icons
from bender.ui.prepare_window import prepare_window
from bender.ui.styles import load_styles
from bender.core.ports_loader import get_ports_dict


def start_app(self) -> None:
    self.splash.change_pbar(10, "Loading UI...")
    prepare_window(self)

    self.splash.change_pbar(20, "Loading settings...")
    load_settings(self)

    self.splash.change_pbar(30, "Updating ports dictionary...")
    self.port_dict = get_ports_dict('tcp', app_dir=self.app_dir)

    self.splash.change_pbar(40, "Hiding elements...")
    hide_elements(self)

    self.splash.change_pbar(50, "Connecting buttons...")
    connect_buttons(self)

    self.splash.change_pbar(60, "Loading images and icons...")
    load_images_and_icons(self)

    self.splash.change_pbar(80, "Loading styles...")
    load_styles(self)

    self.splash.change_pbar(90, "Showing UI...")
    app_open_anim(self)

    self.splash.change_pbar(100, "Running start tasks...")
    run_start_tasks(self)
