from src.logic.game_logic import GameLogic
from src.logic.static_methods import StaticMethods


class GameUI:

    def __init__(self, game_logic: GameLogic, first_player_starts: bool):
        self._game_logic = game_logic
        self._first_player_turn = first_player_starts

    def play(self):
        pass

    def display(self):
        return NotImplementedError("This class serves as a base class")

    def display_end(self, match_status: str):
        return NotImplementedError("This class serves as a base class")

    def get_user_input(self):
        return NotImplementedError("This class serves as a base class")

    def handle_exceptions(self, exc: Exception):
        return NotImplementedError("This class serves as a base class")

