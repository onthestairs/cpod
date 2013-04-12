import curses

class Screen(object):

    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.init_windows()

    def get_char(self):
        return self.stdscr.getch()

    def init_windows(self):
        self.maxY, self.maxX = self.stdscr.getmaxyx()
        self.bodyMaxY = self.maxY - 2
        self.header = curses.newwin(1, self.maxX, 0, 0)
        self.body = curses.newwin(self.bodyMaxY, self.maxX, 1, 0)
        self.status = curses.newwin(1, self.maxX, self.maxY-1, 0)

        self.put_header('cpod')

    def put_header(self, string):
        self.header.erase()
        self.header.addstr(0, 0, string, curses.A_REVERSE)
        self.header.refresh()

    def put_status(self, string):
        self.status.erase()
        self.status.addstr(0, 0, string, curses.A_REVERSE)
        self.status.refresh()

    def put_body_lines(self, lines):
        lines = lines[:self.bodyMaxY]
        self.body.erase()
        for line_number, line in enumerate(lines):
            if line[1] == 'selected':
                style = curses.A_REVERSE
            else:
                style = curses.A_NORMAL
            self.body.addstr(line_number, 0 , line[0], style)
        self.body.refresh()


    def clear_status(self):
        self.put_status('')

    def refresh_body(self):
        self.body.refresh()