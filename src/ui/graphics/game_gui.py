import sys

import pygame

from src.logic.game_logic import GameLogic
from src.logic.static_methods import StaticMethods
from src.logic.undo_services import UndoServices
from src.ui.graphics.menugui import MenuGUI, Button


class GameGUI(MenuGUI):

    def __init__(self, game_logic: GameLogic, first_player_turn):
        super().__init__()

        self._game_logic = game_logic
        self._first_player_turn = first_player_turn

        self._cell_size = self._scale * 70

        self._board_rect = pygame.Rect(int(.1 * self.screen.get_size()[0]),
                                       int(.05 * self.screen.get_size()[1]), int(7 * self._cell_size),
                                       int(6 * self._cell_size))
        self._board_rect.center = int(.5 * self.screen.get_size()[0]), int(.5 * self.screen.get_size()[1])

        self._buttons = [Button((0, 0), self.screen.get_size(), " EXIT ", 48, self._colors["basic_text_color"],
                                self._colors["button_background"],
                                self._colors["button_background_hover"], "exit")]

    def update_assets_size(self):
        super().update_assets_size()

        screen_size = self.screen.get_size()

        self._cell_size = self._scale * 75

        self._board_rect = pygame.Rect(int(.1 * screen_size[0]), int(.1 * screen_size[1]), int(7 * self._cell_size),
                                       int(6 * self._cell_size))

        self._board_rect.center = int(.5 * screen_size[0]), int(.5 * screen_size[1])

    def get_user_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                self.update_assets_size()

            if event.type == pygame.MOUSEBUTTONUP:

                # Buttons
                mouse_pos = pygame.mouse.get_pos()
                for button in self._buttons:

                    if button.pos_inside_button(mouse_pos):
                        return button.get_return

                # Columns
                mouse_pos = pygame.mouse.get_pos()
                for i in range(7):
                    rect = pygame.Rect(i * self._cell_size + self._board_rect.left, self._board_rect.top,
                                       self._cell_size,
                                       self._board_rect.height)
                    if rect.collidepoint(mouse_pos):
                        return i + 1

        return ""

    def display(self):
        super().display()  # Display buttons

        self.display_board()

        # Show preview piece
        board = self._game_logic.get_board
        nr_columns = board.get_nr_columns
        board_pos = self._board_rect.topleft
        cell_border = self._scale * 10
        mouse_pos = pygame.mouse.get_pos()
        for j in range(nr_columns):
            rect = pygame.Rect(j * self._cell_size + self._board_rect.left, self._board_rect.top, self._cell_size,
                               self._board_rect.height)

            if rect.collidepoint(mouse_pos):

                i = board.get_column_empty_cell(j)

                if i == -1:
                    continue

                rect = pygame.Rect(board_pos[0] + j * self._cell_size + cell_border // 2,
                                   board_pos[1] + i * self._cell_size + cell_border // 2,
                                   (self._cell_size - cell_border), (self._cell_size - cell_border))

                pygame.draw.ellipse(self.screen, self._colors["preview_piece"], rect)

        pygame.display.update()

    def display_end(self, match_status: str):
        print(self._game_logic.get_board.get_sequence)
        while True:
            self.screen.fill(self._colors["background_color"])
            self.display_board()

            # Display the match status
            font = pygame.font.Font("ui/graphics/font.ttf", int(72 * self._scale))
            text = font.render(match_status, True, self._colors["basic_text_color"])
            rect = text.get_rect(center=(0.5 * self.screen.get_size()[0], 0.055 * self.screen.get_size()[1]))
            self.screen.blit(text, rect)

            font = pygame.font.Font("ui/graphics/font.ttf", int(48 * self._scale))
            text = font.render("PRESS ANY KEY TO CONTINUE", True, self._colors["basic_text_color"])
            rect = text.get_rect(center=(0.5 * self.screen.get_size()[0], 0.5 * self.screen.get_size()[1]))
            self.screen.blit(text, rect)

            pygame.display.update()
            # Listen for some events

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                    self.update_assets_size()

                if event.type == pygame.KEYDOWN:
                    return

    def handle_exceptions(self, exc: Exception):
        print(exc)

    def play(self):
        pass

    def display_board(self):
        # Show board (blue rect)
        pygame.draw.rect(self.screen, self._colors["board"], self._board_rect)

        # Show pieces (circles)
        board = self._game_logic.get_board
        nr_rows = board.get_nr_rows
        nr_columns = board.get_nr_columns

        board_pos = self._board_rect.topleft

        cell_border = self._scale * 10

        for i in range(nr_rows):
            for j in range(nr_columns):

                cell = board.get_cell_status(i, j)

                rect = pygame.Rect(board_pos[0] + j * self._cell_size + cell_border // 2,
                                   board_pos[1] + (nr_rows - 1 - i) * self._cell_size + cell_border // 2,
                                   (self._cell_size - cell_border), (self._cell_size - cell_border))

                if cell == "X":  # Player pieces
                    pygame.draw.ellipse(self.screen, self._colors["red_piece"], rect)
                elif cell == "Y":  # AI pieces
                    pygame.draw.ellipse(self.screen, self._colors["yellow_piece"], rect)
                else:  # Empty cell
                    pygame.draw.ellipse(self.screen, self._colors["background_color"], rect)


class GamePVCUI(GameGUI):

    def __init__(self, game_logic: GameLogic, first_player_turn):
        super().__init__(game_logic, first_player_turn)

        self.__undo_services = UndoServices()
        self._game_logic.set_undo_services(self.__undo_services)

        self._buttons = [Button((0.75, 0.938), self.screen.get_size(), " EXIT ", 48, self._colors["basic_text_color"],
                                self._colors["button_background"],
                                self._colors["button_background_hover"], "exit"),
                         Button((0.25, 0.938), self.screen.get_size(), " UNDO ", 48, self._colors["basic_text_color"],
                                self._colors["button_background"],
                                self._colors["button_background_hover"], "undo")
                         ]

    def play(self):

        match_status = self._game_logic.get_match_status

        while match_status == "Unfinished":

            if self._first_player_turn:
                self.display()

                user_input = self.get_user_input()

                if user_input == "":
                    continue

                if user_input == "exit":
                    return

                try:

                    if user_input == "undo":
                        self.__undo_services.undo()
                        continue
                    else:
                        StaticMethods.validate_column(user_input, self._game_logic.get_board)
                        self._game_logic.move_player(user_input, False)

                except Exception as exc:
                    self.handle_exceptions(exc)
                    continue

            else:
                self._game_logic.move_ai()

            self._first_player_turn = not self._first_player_turn
            match_status = self._game_logic.get_match_status

        self.display_end(match_status)


class GamePVPUI(GameGUI):
    def __init__(self, game_logic: GameLogic, first_player_turn):
        super().__init__(game_logic, first_player_turn)

        self._buttons = [Button((0.5, 0.938), self.screen.get_size(), " EXIT ", 48, self._colors["basic_text_color"],
                                self._colors["button_background"],
                                self._colors["button_background_hover"], "exit")]

    def play(self):

        match_status = self._game_logic.get_match_status

        while match_status == "Unfinished":
            self.display()

            user_input = self.get_user_input()

            if user_input == "":
                continue

            if user_input == "exit":
                return

            try:
                StaticMethods.validate_column(user_input, self._game_logic.get_board)
                self._game_logic.move_player(user_input, not self._first_player_turn)

            except Exception as exc:
                self.handle_exceptions(exc)
                continue

            self._first_player_turn = not self._first_player_turn
            match_status = self._game_logic.get_match_status

        self.display_end(match_status)

    def display_end(self, match_status: str):

        if match_status == "The Player wins!":
            match_status = "Player 1 wins!"
        elif match_status == "The Computer wins!":
            match_status = "Player 2 wins!"

        super().display_end(match_status)
