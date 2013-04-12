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
        self.link = item.link
        self.feed = feed

    @property 
    def play_url(self):
        return self.link

    @property
    def duration(self):
        return self.item.get('itunes_duration', None)