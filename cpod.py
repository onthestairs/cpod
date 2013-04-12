import curses

import player
import screen

class Cpod(object):

    def __init__(self, feeds):
        self.feeds = feeds
        self.player = player.probePlayer()()

    def run(self, stdscr):
        self.stdscr = stdscr

        self.screen = screen.Screen(self.stdscr)

        self.screen.put_status('Loading...')

        self.name_index = 0

        self.screen.clear_status()

        self.mode = 'feeds'

        self.draw_feeds()

        while True:
            character = self.screen.get_char()
            self.process_char(character)
    
    @property
    def feed_names(self):
        return [feed.name for feed in self.feeds]

    def draw_feeds(self):
        lines = []
        for index, name in enumerate(self.feed_names):
            name = name.encode('utf-8')
            if index == self.name_index:
                lines.append((name, 'selected'))
            else:
                lines.append((name, 'normal'))
        self.screen.put_body_lines(lines)

    def draw_items(self):
        feed = self.feeds[self.name_index]
        lines = []
        for index, item in enumerate(feed.items):
            title = item.title.encode('utf-8')
            if index == self.item_index:
                lines.append((title, 'selected'))
            else:
                lines.append((title, 'normal'))
        self.screen.put_body_lines(lines)

    def select_feed(self, index):
        number_of_feeds = len(self.feeds)
        self.name_index = index % number_of_feeds

    def select_item(self, index):
        feed = self.feeds[self.name_index]
        number_of_items = len(feed.items)
        self.item_index = index % number_of_items

    def play(self):
        url = self.feeds[self.name_index].items[self.item_index].link
        feed_name = self.feeds[self.name_index].name
        item_name = self.feeds[self.name_index].items[self.item_index].title
        self.screen.put_status('NOW PLAYING: {0} - {1}'.format(feed_name, item_name))
        self.player.play(url)

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

        
