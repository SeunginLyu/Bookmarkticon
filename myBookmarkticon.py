from argparse import ArgumentParser
from lxml import html
from lxml.cssselect import CSSSelector
import requests
import urllib

class BookmarksLoader():
    def __init__(self):
        # initialize parser for arguments
        parser = self.build_parser()
        options = parser.parse_args()
        self.filename = options.filename
        self.run()
    def build_parser(self):
        # build parser for loading the filename
        parser = ArgumentParser()
        parser.add_argument('-f', type=str, dest='filename', help='filename', metavar='FILENAME', required=True)
        return parser
    def load_bookmarks(self):
        HtmlFile = open(self.filename, 'r', encoding='utf-8').read()
        DOMtree = html.fromstring(HtmlFile)
        linksSelector = CSSSelector("dt a")
        res = linksSelector(DOMtree)
        links = [result.get("href") for result in res]
        return links

    def download_favicons(self):
        return null
    def create_bookmarkticon(self):
        return null

    def run(self):
        links = self.load_bookmarks()


if __name__ == "__main__":
    bookmarksLoader = BookmarksLoader()
