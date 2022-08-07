import curses

from .text import TextBit
from .printer import WindowPrinter


class SelectionArrow:
    def __init__(self, window, symbol="▶︎", line=1, col=0):
        self.window = window
        self.symbol = symbol
        self.line = line
        self.col = col
        self.selection = 0

    def move(self, lines):
        self.line += lines
        self.selection += lines

    def draw(self):
        self.window.addstr(self.line, self.col, self.symbol)


class SelectionDropdown:
    def __init__(self, window, choices, line=1, col=0):
        self.window = window
        self.line_pos = line
        self.choices = choices
        self.arrow = SelectionArrow(window, line=line, col=max(col - 3, 0))
        self.printer = WindowPrinter(window)
        self.printer.line = line
        self.selection_made = False

    def move_up(self):
        if self.arrow.selection == 0:
            return
        self.arrow.move(-1)

    def move_down(self):
        if self.arrow.selection == len(self.choices) - 1:
            return
        self.arrow.move(1)

    def select(self):
        self.selection_made = True
        selection = self.arrow.selection
        choice = self.choices[selection]
        return choice

    def draw(self):
        self.printer.line = self.line_pos
        for x, choice in enumerate(self.choices):
            indent = 4
            if x == self.arrow.selection:
                indent += 1
                choice = TextBit(choice).bold()
            self.printer.print(choice, indent=indent)
        self.arrow.draw()
        self.window.refresh()

    def on_keypress(self, char_pressed):
        # quit loop on Q pressed or ESC pressed:
        if char_pressed == ord("q") or char_pressed == 27:
            return True

        if char_pressed == curses.KEY_UP:
            self.move_up()
        elif char_pressed == curses.KEY_DOWN:
            self.move_down()
        elif char_pressed == 10:  # Enter key
            self.select()

    def run(self):
        while not self.selection_made:
            self.draw()
            done = self.on_keypress(self.window.getch())
            if done:
                return
        return self.select()
