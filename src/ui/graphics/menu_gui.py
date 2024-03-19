import sys

import pygame

from src.ui.menu_ui import MenuUI


class MenuGUI(MenuUI):

    def __init__(self):
        super().__init__()

        pygame.display.set_caption("Connect4")

        if pygame.display.get_surface() is None:
            self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.get_surface()
        self.__BASE_WIDTH = 800
        self._BASE_HEIGHT = 600
        self._scale = 1
        self._buttons = []

        self._colors = {
            "button_background": (23, 103, 230),
            "button_background_hover": (66, 135, 245),
            "basic_text_color": (255, 255, 255),
            "checked_text_color": (9, 171, 19),
            "unchecked_text_color": (186, 17, 48),
            "background_color": (30, 30, 30),
            "title_color": (186, 17, 48),
            "board": (23, 103, 230),
            "red_piece": (255, 5, 51),
            "yellow_piece": (255, 226, 5),
            "preview_piece": (117, 117, 117)
        }

    def get_user_input(self):

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                self.update_assets_size()

            if event.type == pygame.MOUSEBUTTONUP:

                mouse_pos = pygame.mouse.get_pos()
                for button in self._buttons:

                    if button.pos_inside_button(mouse_pos):
                        return button.get_return

        return ""

    def display(self):
        self.update_assets_size()

        self.screen.fill(self._colors["background_color"])

        mouse_pos = pygame.mouse.get_pos()
        for button in self._buttons:
            button.update(self.screen, button.pos_inside_button(mouse_pos))

    def handle_exceptions(self, exc: Exception):
        pass

    def update_assets_size(self):
        self._scale = self.screen.get_size()[1] / self._BASE_HEIGHT  # Scale based on the height
        for button in self._buttons:
            button.scale(self._scale, self.screen.get_size())


class Button:
    def __init__(self, relative_pos, screen_size, text_input, relative_text_size, text_color, base_color,
                 hovering_color, return_value):

        self.__relative_pos = relative_pos

        self.__x_pos = self.__relative_pos[0] * screen_size[0]
        self.__y_pos = self.__relative_pos[1] * screen_size[1]

        self.__relative_text_size = relative_text_size
        self.__font = pygame.font.Font("ui/graphics/font.ttf", relative_text_size)
        self.__base_color, self.hovering_color, self._text_color = base_color, hovering_color, text_color
        self.__text_input = text_input
        self.__text = self.__font.render(self.__text_input, True, self._text_color, self.__base_color)

        self.__rect = self.__text.get_rect(center=(self.__x_pos, self.__y_pos))
        self.__text_rect = self.__text.get_rect(center=(self.__x_pos, self.__y_pos))

        self.__return_value = return_value

    @property
    def get_return(self):
        return self.__return_value

    def scale(self, scale, screen_size):
        self.__x_pos = self.__relative_pos[0] * screen_size[0]
        self.__y_pos = self.__relative_pos[1] * screen_size[1]

        self.__font = pygame.font.Font("ui/graphics/font.ttf", int(self.__relative_text_size * scale))
        self.__text = self.__font.render(self.__text_input, True, self._text_color, self.__base_color)

        self.__rect = self.__text.get_rect(center=(self.__x_pos, self.__y_pos))
        self.__text_rect = self.__text.get_rect(center=(self.__x_pos, self.__y_pos))

    def update(self, screen, isHovered: bool):

        if isHovered:
            self.__text = self.__font.render(self.__text_input, True, self._text_color, self.hovering_color)
        else:
            self.__text = self.__font.render(self.__text_input, True, self._text_color, self.__base_color)

        screen.blit(self.__text, self.__text_rect)

    def pos_inside_button(self, pos: tuple):
        return self.__rect.collidepoint(pos)


class CheckButton(Button):
    def __init__(self, relative_pos, screen_size, text_input, relative_text_size, text_color, base_color,
                 hovering_color, return_value, check_color, uncheck_color):
        self.__check_color = check_color
        self.__uncheck_color = uncheck_color
        text_color = self.__check_color
        super().__init__(relative_pos, screen_size, text_input, relative_text_size, text_color, base_color,
                         hovering_color, return_value)

    @property
    def get_return(self):
        if self._text_color == self.__check_color:
            self._text_color = self.__uncheck_color
        else:
            self._text_color = self.__check_color

        return super().get_return
