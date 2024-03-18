from config.read_config import Load_Settings
from tasks.start_tasks import Run_Start_Tasks
from ui.animations import App_Open_Anim
from ui.buttons import Connect_Buttons
from ui.hide_elements import Hide_Elements
from ui.images import Load_Images_And_Icons
from ui.prepare_window import Prepare_Window
from ui.styles import Load_Styles


def Start_App(self) -> None:

    # Anywhere shit
    Prepare_Window(self)

    # Load settings
    Load_Settings(self)

    # Hide elements
    Hide_Elements(self)

    # Connect buttons
    Connect_Buttons(self)

    # Load images and Icons
    Load_Images_And_Icons(self)

    # Load styles
    Load_Styles(self)

    # Show UI
    App_Open_Anim(self)

    # Run start tasks
    Run_Start_Tasks(self)