'''
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
'''
from .MAL import MAL
from .Conf import Conf
from contextlib import closing
import urllib
from py_bing_search import PyBingWebSearch
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
    mangas = []
    supportedSites = ["mangafox"]
    def __init__(self, verbose):
        self.verbose = verbose
        conf = Conf()
        self.config = conf.config

    def getManga(self):
        self.mal = MAL()
        on_hold = self.mal.getMangasByStatus("On-Hold")
        plan_to_read = self.mal.getMangasByStatus("Plan to Read")
        self.mangas = on_hold + plan_to_read
        self.mangas.sort(key=lambda x: x.chapters)

    def run(self, mangasite):
        mangasite = mangasite.lower()
        if mangasite not in self.supportedSites:
            return 0
        self.getManga()
        rows = []
        rows.append(["Name","Read Chapters","New Chapters","MangaFox", "MAL"])
        for manga in self.mangas:
            mangaSiteUrl = self.getMangaSiteAddress(mangasite, "manga", manga)
            if mangaSiteUrl:
                if mangasite == "mangafox":
                    row = self.parseMangaFox(manga, mangaSiteUrl)
                else:
                    return 0
                if row:
                    rows.append(row)
                    if self.verbose:
                        print(row)
        return self.writeCSV(rows)

    def writeCSV(self, rows):
        directory  = os.path.dirname(os.path.abspath(__file__))
        filename = "new_chapters_%s.csv" % (int(time.time()))
        path = directory+'/../data/'+filename
        with open(path, 'w',encoding='utf8',newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=",",
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in rows:
                csvwriter.writerow(row)
            csvfile.close()
            return 1
        return 0

    def getMangaSiteAddress(self, site, urlPart, manga):
        name = manga.name
        search_term = "%s %s %s %s" % (site, name, urlPart, "-forum")
        if self.verbose:
            print(search_term)
        api_key = self.config["DEFAULT"]["azure_account_key"];
        bing_web = PyBingWebSearch(api_key, search_term, web_only=False) # web_only is optional, but should be true to use your web only quota instead of your all purpose quota
        results = bing_web.search(limit=1, format='json')
        length = len(results)
        if length > 0 and site in results[0].url and urlPart in results[0].url:
            mangaSiteUrl = results[0].url
            parts = mangaSiteUrl.split("/")
            mangaSiteUrl = "";
            stop_next = 0
            for part in parts:
                mangaSiteUrl += part+"/"
                if part==urlPart:
                    stop_next = 1
                elif stop_next:
                    break
            return mangaSiteUrl
        else:
            return 0

    def parseMangaFox(self, manga, url):
        if self.verbose:
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
