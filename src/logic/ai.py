import math
import random

from src.repository.board import Board


class AI:

    def __init__(self, board: Board, depth: int = 1):

        self.__board = board
        self.__depth = depth
        self.__3piece_weight = 10

    def set_depth(self, new_depth):
        """
        Function that sets the AI's depth to 'new_depth'
        :param new_depth: int
        :return:
        """
        self.__depth = new_depth

    def make_move(self) -> int:
        """
        Function that using minimax, chooses in which column to play.
        :return: int, representing the chosen column
        """
        return self.minimax(self.__depth, -math.inf, math.inf, True)[0]

    def minimax(self, depth, alpha, beta, maximizingPlayer):
        """
        Function that implements the minimax algorithm. It returns the best move and the score of the board.
        Optimisations: alpha-beta pruning,
        sorting the possible moves based on how close they are to the center of the board,
        not searching further if the current player has a winning move or if the current player loses instantly.

        :param depth: int representing the depth of the search
        :param alpha: int representing the alpha value of the alpha-beta pruning (lower bound)
        :param beta:  int representing the beta value of the alpha-beta pruning (upper bound)
        :param maximizingPlayer: bool, if True then the current player is the AI, otherwise the current player is a human.
        :return: tuple (int, int), representing the best move and the score of the board
        """
        remaining_moves = (self.__board.get_nr_rows * self.__board.get_nr_columns - len(self.__board.get_sequence))

        is_terminal = self.is_terminal()
        if depth == 0 or is_terminal:
            if is_terminal:

                # Game is over, no more valid moves
                if remaining_moves == 0:
                    return None, 0

                if self.is_winning(maximizingPlayer):
                    return None, 10000 * remaining_moves
                elif self.is_winning(not maximizingPlayer):
                    return None, -10000 * remaining_moves

            else:  # We reached max depth
                return None, self.score_board(maximizingPlayer)

        valid_locations = self.sort_possible_moves(self.get_possible_moves())

        # Catch draw
        if not valid_locations:
            return None, 0

        sign = 1 if maximizingPlayer else -1

        # If the current player has a winning move, choose it
        winning_moves = self.get_winning_moves(maximizingPlayer)
        if winning_moves:
            return random.choice(winning_moves), sign * 10000 * remaining_moves

        # Check for all positions where the current player doesn't lose instantly

        good_arr = []
        for col in valid_locations:

            self.__board.add_piece(col, maximizingPlayer)

            if not self.get_winning_moves(not maximizingPlayer):
                good_arr.append(col)

            self.__board.remove_piece(col)

        valid_locations = good_arr

        # If there are no position where the player doesn't lose instantly, there's no need in searching
        # for the best move, so choose any move

        if not valid_locations:
            return random.choice(self.get_possible_moves()), - sign * 10000 * (remaining_moves + 1)

        if maximizingPlayer:

            value = -10000 * (remaining_moves + 1)
            column = random.choice(valid_locations)

            for col in valid_locations:
                self.__board.add_piece(col, maximizingPlayer)

                new_score = self.minimax(depth - 1, alpha, beta, False)[1]
                self.__board.remove_piece(col)

                if new_score > value:
                    value = new_score
                    column = col

                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return column, value

        else:  # Minimizing player

            value = 10000 * (remaining_moves + 1)
            column = random.choice(valid_locations)

            for col in valid_locations:
                self.__board.add_piece(col, maximizingPlayer)

                new_score = self.minimax(depth - 1, alpha, beta, True)[1]
                self.__board.remove_piece(col)

                if new_score < value:
                    value = new_score
                    column = col

                beta = min(beta, value)
                if alpha >= beta:
                    break

            return column, value

    def get_possible_moves(self):
        """
        Function that generates all possible moves. A move on a column is possible if that column is not full
        :return: list containing the rows on which we can make a move
        """
        nr_columns = self.__board.get_nr_columns
        array = []
        for column in range(nr_columns):
            if self.__board.is_column_not_full(column):
                array.append(column)

        return array

    def sort_possible_moves(self, moves_array):
        """
        Function that sorts a list based on how close it is to the center of the board.
        :param moves_array: list with moves
        :return: the sorted list
        """

        return sorted(moves_array, key=lambda x: abs(x - self.__board.get_nr_columns // 2))

    def get_winning_moves(self, isAI):
        """
        Function that returns all the moves that will result in the win of the current player.
        :param isAI: bool, if True then the current player is the AI, otherwise the current player is a human.
        :return: lisit containing all winning moves
        """
        winning_moves = []

        possible_moves = self.get_possible_moves()

        for column in possible_moves:
            self.__board.add_piece(column, isAI)

            if self.is_winning(isAI):
                winning_moves.append(column)

            self.__board.remove_piece(column)

        return winning_moves

    def score_board(self, isAI):
        """
        Function that scores the current board based on how many three in a row pieces the current and opposite player have.
        :param isAI: bool, if True then the current player is the AI, otherwise the current player is a human.
        :return: int, representing the score of the board
        """
        if isAI:
            bitstring = self.__board.get_ai_bitstring
            opp_bitstring = self.__board.get_player_bitstring
        else:
            bitstring = self.__board.get_player_bitstring
            opp_bitstring = self.__board.get_ai_bitstring

        return (self.__3piece_weight * self.__board.count_three_in_a_row(bitstring)
                - self.__3piece_weight * self.__board.count_three_in_a_row(opp_bitstring))

    def is_terminal(self):
        """
        Function that checks if the board represents a finished game. A game is finished if someone won or
        there are no moves left.
        :return: bool, True if the board represents a finished game, False otherwise.
        """
        return not self.get_possible_moves() or self.is_winning(True) or self.is_winning(False)

    def is_winning(self, isAI):
        """
        Function that checks if the current player is winning.
        :param isAI: bool, if True then the current player is the AI, otherwise the current player is a human.
        :return: bool, True if the current player is winning, False otherwise
        """
        if isAI:
            return self.__board.four_in_a_row(self.__board.get_ai_bitstring)

        return self.__board.four_in_a_row(self.__board.get_player_bitstring)
