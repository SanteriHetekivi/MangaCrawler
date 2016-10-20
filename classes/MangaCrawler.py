'''
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
'''
from .MAL import MAL
from .Conf import Conf
from .Settings import Settings
from .MangaFox import MangaFox

import time
import csv
import os


class MangaCrawler:
    mangas = []
    supportedSites = ["mangafox"]
    def __init__(self):
        self.config = Conf().config
        self.settings = Settings()
        self.settings.parse()
        self.mangaSite = self.get_manga_site()

    def getManga(self, statuses=[]):
        self.mal = MAL()
        self.mangas = []
        lenght = len(statuses)
        if lenght <= 0:
            self.mangas = self.mal.mangas
        else:
            for status in statuses:
                self.mangas += self.mal.getMangasByStatus(status)
        self.mangas.sort(key=lambda x: x.chapters)

    def run(self):
        if not self.mangaSite:
            return False
        find = self.settings.find
        if find == "new":
            return self.find_new()
        elif find == "updated":
            return self.find_updated()
        else:
            print("Find type not supported!")
            return False

    def find_new(self):
        self.getManga(["Completed", "Reading", "Dropped", "On-Hold"])
        rows = [["Name", "Chapters", "MangaFox"]]
        new_mangas = self.mangaSite.get_new_mangas(self.mangas)
        print(new_mangas)
        if new_mangas:
            rows += new_mangas
            return self.write_csv(rows)
        return False

    def find_updated(self):
        self.getManga(["On-Hold", "Plan to Read"])
        print(len(self.mangas))
        rows = [["Name", "Read Chapters", "New Chapters", "MangaFox", "MAL"]]
        for manga in self.mangas:
            row = self.mangaSite.get_updated_manga(manga)
            if row:
                rows.append(row)
                if self.settings.verbose:
                    print(row)
        return self.write_csv(rows)

    def get_manga_site(self):
        if not self.settings.site:
            return False
        site = self.settings.site.lower()
        if site == "mangafox":
            return MangaFox()
        else:
            return False

    def write_csv(self, rows):
        directory  = os.path.dirname(os.path.abspath(__file__))
        filename = "new_chapters_%s.csv" % (int(time.time()))
        path = directory+'/../data/'+filename
        with open(path, 'w',encoding='utf8',newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=",",
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in rows:
                csvwriter.writerow(row)
            csvfile.close()
            return True
