class FunctionCall:

    def __init__(self, name, *params):
        self.__function_name = name
        self.__params = params

    def call(self):
        """
        Function that calls the function with the given parameters.
        :return:
        """
        return self.__function_name(*self.__params)

    def __call__(self, *args, **kwargs):
        return self.call()


class UndoError(Exception):
    pass


class UndoServices:
    def __init__(self):
        self.__history = []

    def record(self, func: FunctionCall):
        """
        Function that records a function call in the history list.
        :param func: FunctionCall
        :return: None
        """
        self.__history.append(func)

    def undo(self):
        """
        Function that undoes the last operation. It calls the last operation from the history list and then pops it.
        :return: None
        """
        if len(self.__history) < 2:
            raise UndoError("No more undos")

        func = self.__history.pop()
        func()

        if not self.__history:
            raise UndoError("No more undos")

        func = self.__history.pop()
        func()
