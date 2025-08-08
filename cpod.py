import curses

import player
import screen

class Cpod(object):

    def __init__(self, feeds):
        self.feeds = feeds
        self.player = player.probePlayer()()
        self.name_index = 0
        self.playing = False
        self.mode = 'feeds'
        self.item_offset = 0

    def run(self, stdscr):
        self.stdscr = stdscr

        self.screen = screen.Screen(self.stdscr)

        self.screen.put_header('cpod v0.1')
        self.screen.put_status('Loading...')


        for feed in self.feeds:
            feed.populate()

        self.screen.clear_status()

        self.draw_feeds()

        #self.screen.refresh()

        while True:
            try:
                character = self.screen.get_char()
                if self.process_char(character) == -1:
                   break
            except KeyboardInterrupt:
                break

    @property
    def feed_names(self):
        return [feed.name for feed in self.feeds]

    def draw_feeds(self):
        lines = []
        names = self.feed_names
        if self.name_index-1 > self.screen.bodyMaxY:
            names = names[self.name_index+1-self.screen.bodyMaxY:self.name_index+1]
        for index, name in enumerate(names):
            if index == self.name_index:
                parts = [(name, self.screen.reverse)]
                lines.append(parts)
            else:
                parts = [(name, self.screen.default)]
                lines.append(parts)
        self.screen.put_body_lines(lines)

    def draw_items(self):
        feed = self.feeds[self.name_index]
        items = feed.items

        if self.item_index > self.item_offset + self.screen.bodyMaxY - 1:
            self.item_offset = self.item_index - self.screen.bodyMaxY + 1
        if self.item_index < self.item_offset:
            self.item_offset = self.item_index

        items = items[self.item_offset:self.item_offset+self.screen.bodyMaxY]

        lines = []
        for index, item in enumerate(items):
            parts = [(item.title, self.screen.default),
                     (item.duration, self.screen.magenta)]
            title = item.title
            if index+self.item_offset == self.item_index:
                parts = [(item.title, self.screen.reverse),
                         (item.date, self.screen.green),
                         (item.duration, self.screen.magenta)]
                lines.append(parts)
            else:
                parts = [(item.title, self.screen.default),
                         (item.date, self.screen.green),
                         (item.duration, self.screen.magenta)]
                lines.append(parts)

        self.screen.put_body_lines(lines)

    def select_feed(self, index):
        number_of_feeds = len(self.feeds)
        self.name_index = index % number_of_feeds

    def select_item(self, index):
        feed = self.feeds[self.name_index]
        number_of_items = len(feed.items)
        self.item_index = index % number_of_items

    def play(self):
        self.playing_item = self.feeds[self.name_index].items[self.item_index]
        url = self.playing_item.play_url
        self.now_playing_status()
        self.playing = True
        self.player.play(url)

    def toggle_pause(self):
        self.player.pause()
        self.playing = not self.playing

        if self.playing:
            self.now_playing_status()
        else:
            self.paused_status()       

    def now_playing_status(self):
        self.screen.put_status('PLAYING: {0}'.format(self.playing_string))

    def paused_status(self):
        self.screen.put_status('PAUSED: {0}'.format(self.playing_string))

    @property
    def playing_string(self):
        return '{0} - {1}'.format(self.playing_item.feed.name, self.playing_item.title)

    def process_char(self, character):

        if character == curses.KEY_UP or character == ord('k'):
            if self.mode == 'feeds':
                self.select_feed(self.name_index-1)
                self.draw_feeds()
            else:
                self.select_item(self.item_index-1)
                self.draw_items()

        if character == curses.KEY_DOWN or character == ord('j'):
            if self.mode == 'feeds':
                self.select_feed(self.name_index+1)
                self.draw_feeds()
            else:
                self.select_item(self.item_index+1)
                self.draw_items()

        if character == curses.KEY_RIGHT or character == ord('l'):
            if self.mode == 'feeds':
                self.mode = 'items'
                self.item_index = 0
                self.draw_items()
            else:
                self.play()

        if character == curses.KEY_LEFT or character == ord('h'):
            self.mode = 'feeds'
            self.draw_feeds()

        if character == ord('p'):
            self.toggle_pause()

        if character == ord('='):
            self.player.volumeUp()

        if character == ord('-'):
            self.player.volumeDown()

        if character == ord('o'):
            self.player.seekForward()

        if character == ord('i'):
            self.player.seekBackward()

        if character == ord('q'):
            return -1

        if character == curses.KEY_RESIZE:
            self.screen.init_windows()
            self.screen.put_header('cpod v0.1')
            self.draw_items()
        
