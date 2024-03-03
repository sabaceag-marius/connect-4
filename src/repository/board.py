from src.logic.static_methods import StaticMethods


class Board:
    """
       Bitboard

       .  .  .  .  .  .  .
       5 12 19 26 33 40 47
       4 11 18 25 32 39 46
       3 10 17 24 31 38 45
       2  9 16 23 30 37 44
       1  8 15 22 29 36 43
       0  7 14 21 28 35 42

       We represent the board using two bitstring of 49 bits.
       One for the board, and one for the AI. We get the player bitstring by doing a XOR between the two.
    """

    def __init__(self, nr_rows=6, nr_columns=7):

        self.__nr_rows = nr_rows
        self.__nr_columns = nr_columns

        # needed for the AI
        self.__sequence = ""
        self.__ai_bitstring = 0
        self.__board_bitstring = 0

    @property
    def get_nr_rows(self):
        return self.__nr_rows

    @property
    def get_nr_columns(self):
        return self.__nr_columns

    @property
    def get_sequence(self):
        return self.__sequence

    @property
    def get_board_bitstring(self):
        return self.__board_bitstring

    @property
    def get_ai_bitstring(self):
        return self.__ai_bitstring

    @property
    def get_player_bitstring(self):
        return self.__ai_bitstring ^ self.__board_bitstring

    def add_piece(self, col, isAI, realMove=None):
        """
        Function that adds a piece on the column 'col'.
        :param col: int between 0 and 6
        :param isAI: bool, True if the piece is added by the AI/second player, False otherwise
        :param realMove: bool, True if the move is a real move, False if the move is a simulation
        :return: None
        """
        if realMove is not None:
            self.__sequence += str(col)

        # Player move
        if not isAI:
            self.__board_bitstring |= self.__board_bitstring + (1 << (col * 7))
            return

        # Ai Move

        old_player_bitstring = self.get_player_bitstring
        self.__board_bitstring |= (self.__board_bitstring + (1 << (col * 7)))
        self.__ai_bitstring = self.__board_bitstring ^ old_player_bitstring

    def remove_piece(self, col):
        """
        Function that removes the last piece from the column 'col'.
        :param col: int between 0 and 6
        :return: None
        """
        self.__board_bitstring &= self.__board_bitstring - (
                1 << (self.__nr_rows - self.get_column_empty_cell(col) - 2 + col * 7))
        self.__ai_bitstring &= self.__board_bitstring

    def get_cell_status(self, row, col):
        """
        Function that returns the status of a cell. It can be empty, or it can contain a piece from the player or the AI.
        :param row: int
        :param col: int
        :return: str, representing the status of the cell (empty, X - player, Y - AI / second player)
        """
        mask_bitstring = self.__board_bitstring

        mask_bitstring = mask_bitstring >> col * (self.__nr_rows + 1)

        mask_bitstring = mask_bitstring >> row

        if not mask_bitstring & 1:
            return " "

        ai_bitstring = self.__ai_bitstring

        ai_bitstring = ai_bitstring >> col * (self.__nr_rows + 1)

        ai_bitstring = ai_bitstring >> row

        if ai_bitstring & 1:
            return "Y"
        return "X"

    def get_column_empty_cell(self, column):
        """
        Function that returns the row of the first empty cell in the column 'column'.
        :param column: int
        :return: int representing the row of the first empty cell in the column 'column' if the column is empty, or -1 otherwise.
        """
        if not self.is_column_not_full(column):
            return -1

        mask_bitstring = self.__board_bitstring
        mask_bitstring = mask_bitstring >> column * (self.__nr_rows + 1)

        position = 1
        while mask_bitstring & 1:
            mask_bitstring = mask_bitstring >> 1
            position += 1
        return self.__nr_rows - position

    def is_column_not_full(self, column):
        """
        Function that check if the column 'column' has empty cells.
        :param column: int
        :return: bool, True if the column 'column' has empty cells, False otherwise
        """
        return (self.__board_bitstring >> (self.__nr_rows + 1) * column) & ((1 << self.__nr_rows) - 1) != (
                1 << self.__nr_rows) - 1

    def __str__(self):
        board_str = ""

        for i in range(self.__nr_rows - 1, -1, -1):
            board_str += "#"
            for j in range(self.__nr_columns):
                cell = self.get_cell_status(i, j)
                board_str += cell
            board_str += "#\n"

        board_str += "#" * (self.__nr_columns + 2)

        return board_str

    def four_in_a_row(self, position):
        """
        Function that checks if there are four pieces in a row in the position 'position'.
        :param position: int, representing a 49 bit bitstring
        :return: bool, True if there are four pieces in a row, False otherwise
        """
        # Check _ line

        m = position & (position >> (self.__nr_rows + 1))

        if m & (m >> 2 * (self.__nr_rows + 1)):
            return True

        # Check | line

        m = position & (position >> 1)
        if m & (m >> 2):
            return True

        # Check \ line

        m = position & (position >> self.__nr_rows)
        if m & (m >> 2 * self.__nr_rows):
            return True

        # Check / line

        m = position & (position >> (self.__nr_rows + 2))
        if m & (m >> 2 * (self.__nr_rows + 2)):
            return True

        return False

    def count_three_in_a_row(self, position):
        """
        Function that counts the number of three in a row pieces in the position 'position'.
        :param position: int, representing a 49 bit bitstring
        :return: int representing the number of three in a row pieces in the position 'position'
        """
        # we need to check for four in a row, composed of 3 pieces from position, and 1 empty space
        # to do so we make a bitstring composed of three pieces in a row
        # we the normal position combine it (OR) with the opposite of the board bitstring
        # We transform this into a four in a row
        # And we take with AND the 3 in a row bitstring and count the bites

        # We do this for all possible lines
        empty_spaces_bitstring = ~self.get_board_bitstring
        position_and_empty_spaces = position | empty_spaces_bitstring

        counter = 0

        # Check | line

        two_in_a_row = position & (position >> 1)
        three_in_a_row = two_in_a_row & (position >> 2)

        two_in_a_row = position_and_empty_spaces & (position_and_empty_spaces >> 1)
        four_in_a_row = two_in_a_row & (two_in_a_row >> 2)

        counter += StaticMethods.count_bits(three_in_a_row & four_in_a_row)

        # Check - line

        two_in_a_row = position & (position >> (self.__nr_rows + 1))
        three_in_a_row = two_in_a_row & (position >> 2 * (self.__nr_rows + 1))

        two_in_a_row = position_and_empty_spaces & (position_and_empty_spaces >> (self.__nr_rows + 1))
        four_in_a_row = two_in_a_row & (two_in_a_row >> 2 * (self.__nr_rows + 1))

        # print(Utils.base10to2(three_in_a_row))

        counter += StaticMethods.count_bits(three_in_a_row & four_in_a_row)

        # Check the \ line

        two_in_a_row = position & (position >> self.__nr_rows)
        three_in_a_row = two_in_a_row & (position >> 2 * self.__nr_rows)

        two_in_a_row = position_and_empty_spaces & (position_and_empty_spaces >> self.__nr_rows)
        four_in_a_row = two_in_a_row & (two_in_a_row >> 2 * self.__nr_rows)

        counter += StaticMethods.count_bits(three_in_a_row & four_in_a_row)

        # Check the / line

        two_in_a_row = position & (position >> (self.__nr_rows + 2))
        three_in_a_row = two_in_a_row & (position >> 2 * (self.__nr_rows + 2))

        two_in_a_row = position_and_empty_spaces & (position_and_empty_spaces >> (self.__nr_rows + 2))
        four_in_a_row = two_in_a_row & (two_in_a_row >> 2 * (self.__nr_rows + 2))

        counter += StaticMethods.count_bits(three_in_a_row & four_in_a_row)

        return counter

    def make_moves(self, sequence, aiStarts=True):
        """
        Function that makes a sequence of moves. The first move is made by the player, the second by the AI, and so on.
        :param sequence: a string of digits between 1 and 7
        :param aiStarts: bool, True if the AI starts, False otherwise
        :return:
        """
        for i in range(len(sequence)):
            self.add_piece(int(sequence[i]) - 1, aiStarts)
            aiStarts = not aiStarts

        self.__sequence += sequence
