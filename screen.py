import curses

class Screen(object):

    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        curses.use_default_colors()

        curses.init_pair(1, curses.COLOR_MAGENTA, -1)       
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_WHITE, -1)
        curses.init_pair(4, -1, -1)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_GREEN)

        
        self.magenta = curses.color_pair(1)     
        self.green = curses.color_pair(2)
        self.white = curses.color_pair(3)
        self.default = curses.color_pair(4)
        self.reverse = curses.A_REVERSE
        self.magenta_bg = curses.color_pair(5)

        self.init_windows()        

    def get_char(self):
        return self.body.getch()

    def init_windows(self):
        self.maxY, self.maxX = self.stdscr.getmaxyx()
        self.bodyMaxY = self.maxY - 2
        self.header = curses.newwin(1, self.maxX, 0, 0)
        self.body = curses.newwin(self.bodyMaxY, self.maxX, 1, 0)
        self.status = curses.newwin(1, self.maxX, self.maxY-1, 0)

    def put_header(self, string):
        string = string + " "*(self.maxX-len(string)-1)

        self.header.erase()
        self.header.addstr(0, 0, string[:self.maxX-2], self.magenta_bg)
        self.header.refresh()

    def put_status(self, string):
        self.status.erase()
        self.status.addstr(0, 0, string[:self.maxX-2], curses.A_REVERSE)
        self.status.refresh()

    def put_body_lines(self, lines):
        lines = lines[:self.bodyMaxY]
        self.body.erase()
        for line_number, line in enumerate(lines):
            cursor = 0
            for part in line:
                string = part[0][:max(0, self.maxX-cursor-2)]
                self.body.addstr(line_number, cursor , string, part[1])
                cursor += len(string)
                if string:
                    cursor += 1
            # self.body.addstr(line_number, 0 , line[0], style)
        self.refresh_body()

    def clear_status(self):
        self.put_status('')

    def refresh_body(self):
        self.body.refresh()

    def refresh(self):
        self.stdscr.refresh()

