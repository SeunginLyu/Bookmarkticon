from argparse import ArgumentParser
from lxml import html
from lxml.cssselect import CSSSelector
import requests
import urllib
import favicon
import random
import hashlib
import os
from PIL import Image

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
        filtered = []
        for file in files:
            if file.endswith(".png") or file.endswith(".ico"):
                filtered.append(file)

        # selects 40 images with fixed seed created via md5 hashing
        a = hashlib.md5(self.filename.encode('utf-8'))
        b = a.hexdigest()
        seed = int(b, 16)
        random.seed(seed)
        imgs = random.sample(filtered, 64)

        # paste 40 imgs together
        res = Image.new("RGBA", (3200, 3200))
        for index, path in enumerate(imgs):
            complete_path = os.path.expanduser(self.filename + '/' + path)
            try:
                img = Image.open(complete_path).convert("RGBA").resize((400,400))
            except:
                img = Image.new("RGBA", (400,400))
                print(complete_path)
            x = index % 8 * 400
            y = index // 8 * 400
            w, h = img.size
            res.paste(img, (x, y, x + w, y + h))
        res.save(self.filename+'original.png')

        # pixelate the favicon collage
        imgSmall = res.resize((32,32),resample=Image.BILINEAR)
        # Scale back up using NEAREST to original size
        result = imgSmall.resize(res.size, Image.NEAREST)
        # Save
        result.save(self.filename + '.png')
        print("image saved")

    def run(self):
        links = self.load_bookmarks()
        self.download_favicons(links)
        self.create_bookmarkticon()

if __name__ == "__main__":
    bookmarksLoader = BookmarksLoader()
