from src.logic.game_logic import GameLogic
from src.logic.undo_services import UndoServices
from src.ui.game_ui import GameUI
from src.logic.static_methods import StaticMethods


class GameCUI:

    def __init__(self, game_logic: GameLogic, first_player_starts: bool):
        self._game_logic = game_logic
        self._first_player_turn = first_player_starts

    def display(self):
        print()
        print(self._game_logic.get_board)

    def display_end(self, match_status: str):
        print(self._game_logic.get_board)
        print(match_status)

    def get_user_input(self):
        return input("Please choose a column: ").lower().strip()

    def handle_exceptions(self, exc: Exception):
        print(exc)


class GamePVPUI(GameCUI):  # Player vs Player

    def display(self):
        super().display()
        print("EXIT")

    def display_end(self, match_status: str):
        print(self._game_logic.get_board)

        if match_status == "The Player wins!":
            match_status = "Player 1 wins!"
        elif match_status == "The Computer wins!":
            match_status = "Player 2 wins!"

        print(match_status)

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


class GamePVCUI(GameCUI):  # Player vs Computer

    def __init__(self, game_logic: GameLogic, first_player_starts: bool):
        super().__init__(game_logic, first_player_starts)

        self.__undo_services = UndoServices()
        self._game_logic.set_undo_services(self.__undo_services)

    def display(self):
        super().display()
        print("EXIT")
        print("UNDO")

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
