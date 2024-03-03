from src.ui.menu_ui import MenuUI


class MenuCUI(MenuUI):

    def get_user_input(self):
        return input(">").strip().lower()

    def display(self):
        return super().display()

    def handle_exceptions(self, exc: Exception):
        print(exc)
