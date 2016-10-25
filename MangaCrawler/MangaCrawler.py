"""
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
"""
import csv
import os
import time

from .MAL import MAL
from .MangaFox import MangaFox
from .Settings import Settings


class MangaCrawler:
    all_manga = []
    supportedSites = ["mangafox"]

    def __init__(self):
        self.mal = MAL()
        self.settings = Settings()
        self.manga_site = None

    def run(self, settings):
        if not isinstance(settings, Settings):
            return False
        self.settings = settings
        self.manga_site = self.get_manga_site()
        if not self.manga_site:
            return False
        find = self.settings.find
        if find == "new":
            return self.find_new()
        elif find == "updated":
            return self.find_updated()
        else:
            print("Find type not supported!")
            return False

    def get_manga(self, statuses=None):
        if statuses is None:
            statuses = []
        self.all_manga = []
        self.mal = MAL()
        self.mal.parse(self.settings.manga_xml_file)
        length = len(statuses)
        if length <= 0:
            self.all_manga = self.mal.mangas
        else:
            for status in statuses:
                self.all_manga += self.mal.get_mangas_by_status(status)
        self.all_manga.sort(key=lambda x: x.chapters)

    def find_new(self):
        self.get_manga(["Completed", "Reading", "Dropped", "On-Hold"])
        rows = [["Name", "Chapters", "MangaFox", "Google"]]
        new_mangas = self.manga_site.get_new_mangas(self.all_manga, self.settings.min_chapters)
        if new_mangas:
            rows += new_mangas
            return self.write_csv(rows)
        return False

    def find_updated(self):
        self.get_manga(["On-Hold", "Plan to Read"])
        print(len(self.all_manga))
        rows = [["Name", "Read Chapters", "New Chapters", "MangaFox", "MAL"]]
        for manga in self.all_manga:
            row = self.manga_site.get_updated_manga(manga, self.settings.min_chapters, self.settings.azure_account_key)
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
            return MangaFox(self.settings.verbose)
        else:
            return False

    def write_csv(self, rows):
        directory = os.getcwd()
        if not self.settings.output_file or not isinstance(self.settings.output_file, str):
            filename = "new_chapters_%s.csv" % (int(time.time()))
        else:
            filename = self.settings.output_file
        if self.settings.verbose:
            print(filename)
        path = directory + '/' + filename
        with open(path, 'w', encoding='utf8', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=",",
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in rows:
                csv_writer.writerow(row)
            csvfile.close()
            return True
