import feedparser

class Feed(object):

    def __init__(self, url):
        self.url = url
        self._items = None
        self._name = None

    def populate(self):
        d = feedparser.parse(self.url)
        self._name = d.feed.title
        self._items = d.entries

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