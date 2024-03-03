from src.logic.game_logic import GameLogic
from src.ui.graphics.game_gui import GamePVCUI
from src.ui.graphics.menugui import MenuGUI, Button, CheckButton
from src.ui.menu_ui import MenuUI


class PlayComputerMenu(MenuGUI):
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

        self._buttons = [
            Button((.5, .1), self.screen.get_size(), "PLAY COMPUTER", 94, self._colors["title_color"],
                   self._colors["background_color"],
                   self._colors["background_color"], ""),
            Button((.5, .3), self.screen.get_size(), "CHOOSE THE COMPUTER'S DIFFICULTY:", 48, self._colors["basic_text_color"],
                   self._colors["background_color"],
                   self._colors["background_color"], ""),
            Button((.2, .5), self.screen.get_size(), " EASY ", 48, self._colors["basic_text_color"],
                   self._colors["button_background"], self._colors["button_background_hover"], "1"),
            Button((.5, .5), self.screen.get_size(), " MEDIUM ", 48, self._colors["basic_text_color"],
                   self._colors["button_background"], self._colors["button_background_hover"], "2"),
            Button((.8, .5), self.screen.get_size(), " HARD ", 48, self._colors["basic_text_color"],
                   self._colors["button_background"], self._colors["button_background_hover"], "3"),
            CheckButton((.5, .65), self.screen.get_size(), " YOU START ", 48,
                        self._colors["basic_text_color"],
                        self._colors["button_background"], self._colors["button_background_hover"], "4",
                        self._colors["checked_text_color"], self._colors["unchecked_text_color"]),
            Button((.5, .80), self.screen.get_size(), " EXIT ", 48, self._colors["basic_text_color"],
                   self._colors["button_background"], self._colors["button_background_hover"], "exit"),
        ]

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
