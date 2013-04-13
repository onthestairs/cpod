import time
import datetime

import feedparser

class Feed(object):

    def __init__(self, url):
        self.url = url
        self._items = None
        self._name = None

    def populate(self):
        d = feedparser.parse(self.url)
        self._name = d.feed.title
        self._items = [Item(entry, self) for entry in d.entries]

    @property
    def items(self):
        if not self._items:
            self.populate()
        return self._items

    def refresh(self):
        self.populate()

    @property
    def name(self):
        if not self._name:
            self.populate()
        return self._name

    @property
    def display_name(self):
        return self.name


class Item(object):

    def __init__(self, item, feed):
        self.item = item
        self.title = item.title
        self.feed = feed

    @property 
    def play_url(self):
        if 'mp3' in self.item.guid and self.item.guidislink:
            return self.item.guid
        else:
            return self.item.link

    @property
    def duration(self):
        return self.item.get('itunes_duration', None)

    @property
    def date(self):
        t = time.mktime(self.item.published_parsed)
        dt = datetime.datetime.fromtimestamp(t)
        return dt.strftime('%d %b %Y')