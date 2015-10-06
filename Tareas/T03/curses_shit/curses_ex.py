import curses

_PAD_WIDTH = 400
_PAD_HEIGHT = 10000
_TEXTBOX_WIDTH = 50
_TEXTBOX_HEIGHT = 3


class Selector:

    def __init__(self, options):
        self.options = options

    def select(self):
        self.initialize()
        self.create_pad(height=_PAD_HEIGHT, width=_PAD_WIDTH)

        windows = self.create_options()
        picked = self.select_option(windows)

        self.terminate()

        return picked

    def initialize(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(1)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.stdscr.bkgd(curses.color_pair(2))
        self.stdscr.refresh()

    def terminate(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def create_pad(self, height, width):
        self.pad = curses.newpad(height, width)
        self.pad.box()

    def create_options(self):
        maxy, maxx = self.stdscr.getmaxyx()
        windows = []
        i = 1
        for option in self.options:
            pad = self.pad.derwin(_TEXTBOX_HEIGHT,
                                  _TEXTBOX_WIDTH,
                                  i,
                                  _PAD_WIDTH // 2 - _TEXTBOX_WIDTH // 2)
            windows.append(pad)
            i += _TEXTBOX_HEIGHT

        for j in range(len(windows)):
            windows[j].box()
            windows[j].addstr(1, 4, '({0}) - {1}'.format(j, self.options[j]))
        return windows

    def center_view(self, window):
        cy, cx = window.getbegyx()
        maxy, maxx = self.stdscr.getmaxyx()
        self.pad.refresh(cy, cx, 1, maxx // 2 - _TEXTBOX_WIDTH // 2, maxy - 1, maxx - 1)
        return cy, cx

    def select_option(self, windows):
        topy, topx = self.center_view(windows[0])

        current_selected = 0
        last = 1
        top_textbox = windows[0]

        while True:
            windows[current_selected].bkgd(curses.color_pair(1))
            windows[last].bkgd(curses.color_pair(2))

            maxy, maxx = self.stdscr.getmaxyx()
            cy, cx = windows[current_selected].getbegyx()

            if ((topy + maxy - _TEXTBOX_HEIGHT) <= cy):
                top_textbox = windows[current_selected]

            if topy >= cy + _TEXTBOX_HEIGHT:
                top_textbox = windows[current_selected]

            if last != current_selected:
                last = current_selected

            topy, topx = self.center_view(top_textbox)

            char = self.stdscr.getch()
            if char == curses.KEY_DOWN:
                if current_selected < len(windows) - 1:
                    current_selected += 1
                else:
                    current_selected = 0
            elif char == curses.KEY_UP:
                if current_selected > 0:
                    current_selected -= 1
                else:
                    current_selected = len(windows) - 1
            elif char in [81, 113]:
                break
            elif char in [curses.KEY_ENTER, 10]:
                return int(current_selected)
        return -1


if __name__ == '__main__':
    opciones = list('Opción %d' % i for i in range(15))

    seleccion = Selector(opciones).select()
    if seleccion == -1:
        print(seleccion, 'Adiós')
    else:
        print(seleccion, opciones[seleccion])
