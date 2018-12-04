from argparse import ArgumentParser
from lxml import html
from lxml.cssselect import CSSSelector
import requests
import urllib
import favicon
import os

class BookmarksLoader():
    def __init__(self):
        # initialize parser for arguments
        parser = self.build_parser()
        options = parser.parse_args()
        self.filename = options.filename.split('.')[0]
        self.target = options.filename
        self.run()
    def build_parser(self):
        # build parser for loading the filename
        parser = ArgumentParser()
        parser.add_argument('-f', type=str, dest='filename', help='filename', metavar='FILENAME', required=True)
        return parser
    def load_bookmarks(self):
        HtmlFile = open(self.target, 'r', encoding='utf-8').read()
        DOMtree = html.fromstring(HtmlFile)
        linksSelector = CSSSelector("dt a")
        res = linksSelector(DOMtree)
        links = [result.get("href") for result in res]
        return links

    def download_favicons(self, links):
        # download all favicons from the links if they don't exist yet
        if not os.path.exists(self.filename):
            os.makedirs(self.filename)
            for i, link in enumerate(links):
                try:
                    icon = favicon.get(link)[0]
                    response = requests.get(icon.url, stream=True)
                    path = (self.filename+'/'+ str(i) +'.{}').format(icon.format)
                    print(path)
                    with open(path, 'wb') as image:
                        for chunk in response.iter_content(1024):
                            image.write(chunk)
                except Exception as e:
                    print(link, e)
            print("download complete")
        else:
            print("favicons already downloaded!")

    def create_bookmarkticon(self):
        files = os.listdir(self.filename)
        for file in files:
            if file.endswith(".png") or file.endswith(".ico"):
                
        # img = Image.open("paddington.png")
        # # Resize smoothly down to 64x64 pixels
        # imgSmall = img.resize((64,64),resample=Image.BILINEAR)
        # # Scale back up using NEAREST to original size
        # result = imgSmall.resize(img.size, Image.NEAREST)
        # # Save
        # result.save(self.filename + '.png')

    def run(self):
        links = self.load_bookmarks()
        self.download_favicons(links)
        self.create_bookmarkticon()

if __name__ == "__main__":
    bookmarksLoader = BookmarksLoader()
