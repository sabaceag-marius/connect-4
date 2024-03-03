from src.logic.ai import AI
from src.logic.undo_services import FunctionCall, UndoServices
from src.repository.board import Board


class GameLogic:

    def __init__(self, board: Board = None, undo_services: UndoServices = None):
        self.__board = Board()

        self.__ai = AI(self.__board, 1)

        if board is not None:
            self.__board = board

        self.__undo_services = undo_services

    @property
    def get_board(self):
        return self.__board

    def set_undo_services(self, new_undo_services):
        self.__undo_services = new_undo_services

    def move_player(self, column, secondPlayer: bool):
        """
        Function that puts a piece on the column 'column'.
        :param secondPlayer: bool
        :param column: an int between 1 and 7
        :return: None
        """
        column = int(column)
        column -= 1
        self.__board.add_piece(column, secondPlayer, True)

        # RECORD OPERATION FOR UNDO
        if self.__undo_services is not None:
            undo = FunctionCall(self.__board.remove_piece, column)
            self.__undo_services.record(undo)

    def move_ai(self):
        """
        Function that puts a piece on the column chosen by the AI.
        :return: None
        """
        column = self.__ai.make_move()
        self.__board.add_piece(column, True, True)

        # RECORD OPERATION FOR UNDO
        if self.__undo_services is not None:
            undo = FunctionCall(self.__board.remove_piece, column)
            self.__undo_services.record(undo)

    def set_ai_depth(self, ai_difficulty: int):
        """
        Function that sets the AI's depth
        :param ai_difficulty: int
        :return: None
        """
        self.__ai.set_depth(ai_difficulty)

    def make_moves(self, moves: str):
        """
        Function that makes a sequence of moves.
        :param moves: a string of digits between 1 and 7
        :return: None
        """
        self.__board.make_moves(moves)

    @property
    def get_match_status(self):
        """
        Function that returns the match status.
        :return: "The Player wins!", if the player has 4 pieces in a row,
                 "The Computer wins!", if the AI has 4 pieces in a row,
                 "Draw", if no one won and there are no moves left,
                 "Unfinished" otherwise
        """
        # Check if the player won
        if self.__board.four_in_a_row(self.__board.get_player_bitstring):
            return "The Player wins!"

        # Check if the computer won
        if self.__board.four_in_a_row(self.__board.get_ai_bitstring):
            return "The Computer wins!"

        # Check if it is a draw
        if len(self.__board.get_sequence) == self.__board.get_nr_columns * self.__board.get_nr_rows:
            return "Draw"

        return "Unfinished"
