import pygame
from src.ui.console.menus.main_menu import MainMenuCUI
from src.ui.graphics.menus.main_menu import MainMenuGUI

if __name__ == '__main__':

    console_mode = False

    if console_mode:

        menu = MainMenuCUI()
        menu.run()

    else:
        pygame.init()
        menu = MainMenuGUI()
        menu.run()
        pygame.quit()
