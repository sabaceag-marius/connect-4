import pygame

from src.logic.game_logic import GameLogic
from src.ui.graphics.game_gui import GamePVPUI
from src.ui.graphics.menu_gui import MenuGUI, Button
from src.ui.graphics.menus.play_computer_menu import PlayComputerMenu


class PlayMenu(MenuGUI):

    def __init__(self):
        super().__init__()

        self._commands = {
            "1": self.__ui_play_player,
            "2": self.__ui_play_computer,
        }

        self._buttons = [
            Button((.5, .1), self.screen.get_size(), "PLAY", 94, self._colors["title_color"],
                   self._colors["background_color"],
                   self._colors["background_color"], ""),
            Button((.5, .5), self.screen.get_size(), " VERSUS PLAYER ", 48, self._colors["basic_text_color"],
                   self._colors["button_background"],
                   self._colors["button_background_hover"], "1"),
            Button((.5, .65), self.screen.get_size(), " VERSUS COMPUTER ", 48, self._colors["basic_text_color"],
                   self._colors["button_background"],
                   self._colors["button_background_hover"], "2"),
            Button((.5, .8), self.screen.get_size(), " EXIT ", 48, self._colors["basic_text_color"],
                   self._colors["button_background"],
                   self._colors["button_background_hover"], "exit")]

    def __ui_play_player(self):
        self._exit_after_command = True
        GamePVPUI(GameLogic(), True).play()

    def __ui_play_computer(self):
        self._exit_after_command = True

        PlayComputerMenu().run()
