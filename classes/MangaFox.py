'''
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
'''
from .MangaSite import MangaSite
import urllib
import re
import urllib.request
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup

class MangaFox(MangaSite):
    def __init__(self):
        super().__init__()

    def getUpdatedManga(self, manga):
        url = self.getMangaSiteAddress("mangafox", "manga", manga)
        if not url:
            return False
        if self.settings.verbose:
            print(url)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as htmlfile:
                soup = BeautifulSoup(htmlfile.read(), "lxml")
                volumes = soup.findAll("h3", { "class" : "volume" })
                if len(volumes) <= 0:
                    return 0
                volume = volumes[0]
                chaptername = volume.span.text;
                numbers = re.findall('\d+\.\d+|\d+', chaptername)
                length = len(numbers)
                if length <= 0:
                    return 0
                chapters = numbers[length-1]
                numbers = re.findall('\d+', chapters)
                length = len(numbers)
                if length <= 0:
                    return 0
                try:
                    chapters = int(numbers[0])
                except ValueError:
                    return 0
                new_chapers = chapters-manga.chapters
                if new_chapers < 5:
                    return 0
                row = [manga.name.replace(",", " "), manga.chapters, new_chapers, url, manga.url]
                return row
        except urllib.error.HTTPError as err:
            return 0

