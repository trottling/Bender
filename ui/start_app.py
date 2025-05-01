from config.read_config import load_settings
from tasks.start_tasks import run_start_tasks
from ui.animations import app_open_anim
from ui.buttons import connect_buttons
from ui.hide_elements import hide_elements
from ui.images import load_images_and_icons
from ui.prepare_window import prepare_window
from ui.styles import load_styles


def start_app(self) -> None:
    # Anywhere shit
    prepare_window(self)

    # Load settings
    load_settings(self)

    # Hide elements
    hide_elements(self)

    # Connect buttons
    connect_buttons(self)

    # Load images and Icons
    load_images_and_icons(self)

    # Load styles
    load_styles(self)

    # Show UI
    app_open_anim(self)

    # Run start tasks
    run_start_tasks(self)
