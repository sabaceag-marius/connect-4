import pygame
from pygame.font import Font

from src.ui.graphics.menugui import MenuGUI, Button
from src.ui.graphics.menus.play_menu import PlayMenu
from src.ui.graphics.menus.tutorial_menu import TutorialMenu


class MainMenuGUI(MenuGUI):

    def __init__(self):
        super().__init__()

        self._commands = {
            "1": PlayMenu().run,
        }

        self._buttons = [
            Button((.5, .1), self.screen.get_size(), "CONNECT 4", 94, self._colors["title_color"],
                   self._colors["background_color"],
                   self._colors["background_color"], ""),
            Button((.5, .5), self.screen.get_size(), " PLAY ", 48, self._colors["basic_text_color"],
                   self._colors["button_background"],
                   self._colors["button_background_hover"], "1"),
            Button((.5, .65), self.screen.get_size(), " EXIT ", 48, self._colors["basic_text_color"],
                   self._colors["button_background"],
                   self._colors["button_background_hover"], "exit")

        ]
