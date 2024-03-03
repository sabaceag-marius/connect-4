from src.ui.graphics.menugui import MenuGUI, Button


class TutorialMenu(MenuGUI):

    def __init__(self):
        super().__init__()

        self._buttons = {

            Button((.5, .5), self.screen.get_size(), "  Take turns dropping the checkers into the slots, attempting to make a horizontal, vertical, or diagonal line of 4 checkers of your color. ", 24, self._colors["basic_text_color"],
                   self._colors["background_color"], self._colors["background_color"], ""),

            Button((.5, .80), self.screen.get_size(), " EXIT ", 48, self._colors["basic_text_color"],
                   self._colors["button_background"], self._colors["button_background_hover"], "exit"),
        }
