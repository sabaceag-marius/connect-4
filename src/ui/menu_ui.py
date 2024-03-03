class MenuUI:

    def __init__(self):
        self._commands = {}
        self._exit_after_command = False

    def run(self):

        while True:

            self.display()

            user_input = self.get_user_input()

            if user_input == "":
                continue
            if user_input == "exit":
                break

            if user_input in self._commands.keys():
                try:
                    self._commands[user_input]()
                    if self._exit_after_command:
                        return
                except Exception as exc:
                    self.handle_exceptions(exc)

    def get_user_input(self):
        return NotImplementedError("This class serves as a base class")

    def display(self):
        return NotImplementedError("This class serves as a base class")

    def handle_exceptions(self, exc: Exception):
        pass
