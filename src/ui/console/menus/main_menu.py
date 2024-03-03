from src.ui.console.menu_cui import MenuCUI
from src.ui.console.menus.play_menu import PlayMenu
from src.ui.console.menus.tutorial_menu import TutorialMenu


class MainMenuCUI(MenuCUI):

    def __init__(self):
        super().__init__()
        self._commands = {
            "1": PlayMenu().run,
            "2": TutorialMenu().run
        }

    def display(self):
        print()
        print("MAIN MENU")
        print("1. PLAY")
        print("2. TUTORIAL")
        print("EXIT")
