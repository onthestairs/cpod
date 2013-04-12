import curses

from feed import Feed
import cpod


urls = ['http://www.guardian.co.uk/football/series/footballweekly/podcast.xml',
        'http://downloads.bbc.co.uk/podcasts/radio4/iot/rss.xml']

feeds = [Feed(url) for url in urls]

cpod = cpod.Cpod(feeds)
curses.wrapper(cpod.run)