from src.logic.game_logic import GameLogic
from src.ui.console.menu_cui import MenuCUI
from src.ui.console.game_cui import GamePVCUI


class PlayComputerMenu(MenuCUI):
    def __init__(self):
        super().__init__()

        self._commands = {
            "1": self.__ui_play_easy_computer,
            "2": self.__ui_play_medium_computer,
            "3": self.__ui_play_hard_computer,
            "4": self.__ui_toggle_player_starts_first,
        }

        self.__game_logic = GameLogic()
        self.__player_starts_first = True

    def display(self):
        print()
        print("PLAY COMPUTER MENU")
        print("1. EASY")
        print("2. MEDIUM")
        print("3. HARD")
        print(f"4. PLAYER STARTS FIRST - {self.__player_starts_first}")
        print("EXIT")
        print()

    def __ui_play_easy_computer(self):
        self._exit_after_command = True  # To go to the main menu after finishing a game
        self.__game_logic.set_ai_depth(1)

        GamePVCUI(self.__game_logic, self.__player_starts_first).play()

    def __ui_play_medium_computer(self):
        self._exit_after_command = True  # To go to the main menu after finishing a game
        self.__game_logic.set_ai_depth(6)

        GamePVCUI(self.__game_logic, self.__player_starts_first).play()

    def __ui_play_hard_computer(self):
        self._exit_after_command = True  # To go to the main menu after finishing a game
        self.__game_logic.set_ai_depth(11)

        GamePVCUI(self.__game_logic, self.__player_starts_first).play()

    def __ui_toggle_player_starts_first(self):
        self.__player_starts_first = not self.__player_starts_first
