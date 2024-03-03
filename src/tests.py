import math
import unittest

from src.logic.ai import AI
from src.logic.game_logic import GameLogic
from src.logic.static_methods import StaticMethods
from src.repository.board import Board


class StaticMethodsTests(unittest.TestCase):

    def test_validate_column(self):
        # Case 1: valid column
        board = Board()
        StaticMethods.validate_column(1, board)

        # Case 2: invalid column
        board = Board()
        board.make_moves("1111111")

        try:
            StaticMethods.validate_column(1, board)
            self.fail()
        except Exception as exc:
            self.assertEqual(str(exc), "Column is full!")

        # Case 3: invalid column

        board = Board()
        try:
            StaticMethods.validate_column("a", board)
            self.fail()
        except ValueError as exc:
            self.assertEqual(str(exc), "Input must be a number!")


class GameLogicTests(unittest.TestCase):
    def test_get_match_status(self):

        def str_list_to_matrix(array):

            result_array = []
            for string in array:
                arr = []
                for char in string:
                    arr.append(char)
                result_array.append(arr)
            return result_array

        # Case 1: Empty board -> "Unfinished"

        game_logic = GameLogic()

        self.assertEqual(game_logic.get_match_status, "Unfinished")

        # Case 2: Full board and no line -> "Draw"
        """
        XYXYXYY
        XYXYXYX
        YXYXYXY
        YXYXYXX
        XYXYXYY
        XYXYXYX
        """
        game_logic = GameLogic(Board())
        game_logic.make_moves("121221211212343443433434565665655656777777")

        self.assertEqual(game_logic.get_match_status, "Draw")

        # Case 3: player has _ line -> "The Player wins!"
        """



        YYY
        XXXX  Y
        XYXYXYX
        """
        game_logic = GameLogic(Board())
        game_logic.make_moves("6123456771122334")

        self.assertEqual(game_logic.get_match_status, "The Player wins!")

        # Case 4: AI has | line -> "The Computer wins!"

        game_logic = GameLogic(Board())
        game_logic.make_moves("2323232")

        self.assertEqual(game_logic.get_match_status, "The Computer wins!")

        # Case 5: player has \ line -> "The Player wins!"

        game_logic = GameLogic(Board())
        game_logic.make_moves("43322121121")

        self.assertEqual(game_logic.get_match_status, "The Computer wins!")

        # Case 6: AI has / line -> "The Computer wins!"

        game_logic = GameLogic(Board())
        game_logic.make_moves("7455676677")

        self.assertEqual(game_logic.get_match_status, "The Player wins!")

    def test_move_player(self):

        # Case 1: valid move
        game_logic = GameLogic(Board())
        game_logic.move_player(1, False)
        self.assertEqual(game_logic.get_board.get_cell_status(0, 0), "X")

        # Invalid moves are checked beforehand in the UI

    def test_move_ai(self):

        # Case 1: valid move
        game_logic = GameLogic(Board())
        game_logic.move_ai()
        self.assertEqual(game_logic.get_board.get_cell_status(0, 3), "Y")


class BoardTests(unittest.TestCase):

    def test_add_piece(self):
        # Case 1: player move
        board = Board()
        board.add_piece(0, False)
        self.assertEqual(board.get_cell_status(0, 0), "X")

        # Case 2: AI move
        board = Board()
        board.add_piece(0, True)
        self.assertEqual(board.get_cell_status(0, 0), "Y")

    def test_remove_piece(self):
        # Case 1: player move
        board = Board()
        board.add_piece(0, False)
        board.remove_piece(0)
        self.assertEqual(board.get_cell_status(0, 0), " ")

        # Case 2: AI move
        board = Board()
        board.add_piece(0, True)
        board.remove_piece(0)
        self.assertEqual(board.get_cell_status(0, 0), " ")

    def test_get_cell_status(self):
        # Case 1: empty cell
        board = Board()
        self.assertEqual(board.get_cell_status(0, 0), " ")

        # Case 2: player cell
        board = Board()
        board.add_piece(0, False)
        self.assertEqual(board.get_cell_status(0, 0), "X")

        # Case 3: AI cell
        board = Board()
        board.add_piece(0, True)
        self.assertEqual(board.get_cell_status(0, 0), "Y")

    def test_get_column_empty_cell(self):
        # Case 1: empty column
        board = Board()
        self.assertEqual(board.get_column_empty_cell(0), 5)

        # Case 2: non-empty column
        board = Board()
        board.add_piece(0, False)
        self.assertEqual(board.get_column_empty_cell(0), 4)

        # Case 3: full column
        board = Board()
        board.make_moves("1111111")
        self.assertEqual(board.get_column_empty_cell(0), -1)

    def test_is_column_not_full(self):
        # Case 1: empty column
        board = Board()
        self.assertTrue(board.is_column_not_full(0))

        # Case 2: non-empty column
        board = Board()
        board.add_piece(0, False)
        self.assertTrue(board.is_column_not_full(0))

        # Case 3: full column
        board = Board()
        board.make_moves("1111111")
        self.assertFalse(board.is_column_not_full(0))

    def test_count_three_in_a_row(self):
        # Case 1: no line
        board = Board()
        self.assertEqual(board.count_three_in_a_row(board.get_ai_bitstring), 0)

        # Case 2: | line
        board = Board()
        board.make_moves("232323")
        self.assertEqual(board.count_three_in_a_row(board.get_ai_bitstring), 1)


class AITests(unittest.TestCase):

    def test_make_move(self):
        # Case 1: empty board
        board = Board()
        ai = AI(board, 2)
        self.assertEqual(ai.make_move(), 3)

        # Case 2: non-empty board
        board = Board()
        ai = AI(board, 2)
        board.make_moves("1111111")
        self.assertEqual(ai.make_move(), 3)

        # Case 3: winning move for AI
        board = Board()
        ai = AI(board, 2)
        board.make_moves("12121")
        self.assertEqual(ai.make_move(), 0)

        # Case 4: winning move for player
        board = Board()
        ai = AI(board, 2)
        board.make_moves("121212")
        self.assertEqual(ai.make_move(), 0)

    def test_get_possible_moves(self):
        # Case 1: empty board
        board = Board()
        ai = AI(board)
        self.assertEqual(ai.get_possible_moves(), [0, 1, 2, 3, 4, 5, 6])

        # Case 2: non-empty board
        board = Board()
        ai = AI(board)
        board.make_moves("1111111")
        self.assertEqual(ai.get_possible_moves(), [1, 2, 3, 4, 5, 6])

    def test_get_winning_moves(self):
        # Case 1: no winning moves
        board = Board()
        ai = AI(board)
        self.assertEqual(ai.get_winning_moves(True), [])

        # Case 2: winning move
        board = Board()
        ai = AI(board)
        board.make_moves("12121")
        self.assertEqual(ai.get_winning_moves(True), [0])

    def test_is_terminal(self):
        # Case 1 - it's a draw
        board = Board()
        ai = AI(board)
        board.make_moves("121221211212343443433434565665655656777777")
        self.assertTrue(ai.is_terminal())

        # Case 2 - AI wins
        board = Board()
        ai = AI(board)
        board.make_moves("2323232")
        self.assertTrue(ai.is_terminal())

        # Case 3 - Player wins
        board = Board()
        ai = AI(board)
        board.make_moves("43322121121")
        self.assertTrue(ai.is_terminal())

        # Case 4 - not terminal
        board = Board()
        ai = AI(board)
        board.make_moves("4332212112")
        self.assertFalse(ai.is_terminal())

    def test_is_winning(self):
        # Case 1: no line
        board = Board()
        ai = AI(board)
        self.assertFalse(ai.is_winning(True))

        # Case 2: | line
        board = Board()
        ai = AI(board)
        board.make_moves("2323232")
        self.assertTrue(ai.is_winning(True))

        # Case 3: \ line
        board = Board()
        ai = AI(board)
        board.make_moves("43322121121")
        self.assertTrue(ai.is_winning(True))

        # Case 4: / line
        board = Board()
        ai = AI(board)
        board.make_moves("7455676677")
        self.assertTrue(ai.is_winning(False))


if __name__ == '__main__':
    unittest.main()
