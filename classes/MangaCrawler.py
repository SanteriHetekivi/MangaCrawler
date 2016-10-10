from .MAL import MAL
from contextlib import closing
import urllib
import re
from urllib.parse import quote
import urllib.request
import time
import csv
import os
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup

class MangaCrawler:

    def __init__(self):
        self.mal = MAL()
        on_hold = self.mal.getMangasByStatus("On-Hold")
        plan_to_read = self.mal.getMangasByStatus("Plan to Read")
        mangas = on_hold + plan_to_read
        mangas.sort(key=lambda x: x.chapters)
        rows = []
        rows.append(["Name","Read Chapters","New Chapters","MangaFox", "MAL"])
        for manga in mangas:
            mangafox_url = self.getMangaFoxAddress(manga)
            if mangafox_url:
                row = self.parseMangaFox(manga, mangafox_url)
                if row:
                    rows.append(row)
                    print(row)
        directory  = os.path.dirname(os.path.abspath(__file__))
        filename = "new_chapters_%s.csv" % (int(time.time()))
        path = directory+'/../data/'+filename
        with open(path, 'w',encoding='utf8',newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=",",
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in rows:
                csvwriter.writerow(row)
            csvfile.close()
    def getMangaFoxAddress(self, manga):
        name = manga.name
        name = quote(name)
        url = 'https://www.google.fi/search?sclient=psy-ab&client=ubuntu&hs=k5b&channel=fs&biw=1366&bih=648&noj=1&q=mangafox+'+name
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        print(url)
        try:
            with urllib.request.urlopen(req) as htmlfile:
                soup = BeautifulSoup(htmlfile.read(), "lxml")
                mangafox_url = soup.h3.a["href"].replace("/url?q=", "")
                parts = mangafox_url.split("/")
                mangafox_url = "";
                stop_next = 0
                for part in parts:
                    mangafox_url += part+"/"
                    if part=="manga":
                        stop_next = 1
                    elif stop_next:
                        break
                return mangafox_url
        except urllib.error.HTTPError as err:
            return 0

    def parseMangaFox(self, manga, url):
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
