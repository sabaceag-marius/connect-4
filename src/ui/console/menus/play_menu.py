from src.logic.game_logic import GameLogic
from src.ui.console.menu_cui import MenuCUI
from src.ui.console.game_cui import GamePVPUI
from src.ui.console.menus.play_computer_menu import PlayComputerMenu


class PlayMenu(MenuCUI):

    def __init__(self):
        super().__init__()

        self._commands = {
            "1": self.__ui_play_player,
            "2": self.__ui_play_computer,
        }

    def display(self):
        print()
        print("PLAY MENU")

        print("1. PLAYER VS PLAYER")
        print("2. PLAYER VS COMPUTER")
        print("EXIT")
        print()

    def __ui_play_player(self):
        self._exit_after_command = True
        GamePVPUI(GameLogic(), True).play()

    def __ui_play_computer(self):
        self._exit_after_command = True

        menu = PlayComputerMenu()
        menu.run()
