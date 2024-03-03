class StaticMethods:

    @staticmethod
    def validate_column(column_input, board):
        """
        Function that validates 'column_input' in relation with 'board'
        :param column_input: an int between 1 and the number of columns of the board
        :param board: a matrix made out of ' ', 'x' and 'y'
        :return: None, if 'column_input' is valid, exception otherwise
        :raises:
                ValueError with message "Input must be a number!" if 'column_input' is not an integer number.
                ValueError with message f"The column must be between 1 and {board.get_nr_columns}!",
            if column_input is an int, but not between 1 and the number of columns of the board.
                Exception with message "Column is full!", if the column equal to 'column_input' doesn't have any ' '
            character.
        """

        try:

            column_input = int(column_input)

            if not (1 <= column_input <= 7):
                raise ValueError("The column must be between 1 and 7!")

            if not board.is_column_not_full(column_input - 1):
                raise Exception("Column is full!")

        except ValueError:
            raise ValueError("Input must be a number!")

    @staticmethod
    def count_bits(num):
        """
        Function that counts the number of bits in a number.
        :param num: int
        :return: int representing the number of bits
        """
        counter = 0

        while num:
            if num & 1 == 1:
                counter += 1
            num = num >> 1

        return counter