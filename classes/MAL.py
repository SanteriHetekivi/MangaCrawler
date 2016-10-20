'''
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
'''
import xml.etree.ElementTree as ET
from .XML import XML
from .Manga import Manga


class MAL:

    mangas = []
    statuses = {"Reading": 1, "Completed": 2, "On-Hold": 3, "Dropped": 4, "Plan to Read": 6}

    def __init__(self):
        self.parse()

    def printNames(self):
        self.printNames(self.mangas)

    def printNames(self, _mangas):
        for manga in _mangas:
            print("%s %s %s" % (manga.name, manga.status, manga.chapters))

    def parse(self):
        self.XML = XML()
        root = self.XML.getXMLRoot()
        if root:
            for manga in root.iter('manga'):
                self.mangas.append(
                    Manga(
                        self.getInfos(manga, ["manga_mangadb_id", "series_animedb_id"]),
                        self.getInfos(manga, ["manga_title", "series_title"]),
                        self.getInfo(manga, "my_status"),
                        self.getInfo(manga, "my_read_chapters"),
                        self.getInfo(manga, "series_synonyms")
                        )
                )
            return True
        return False

    def getInfos(self, manga, infonames):
        for infoname in infonames:
            value = self.getInfo(manga, infoname)
            if value:
                return value
        return ""

    def getInfo(self, manga, infoname):
        field = manga.find(infoname)
        if field is not None:
            return field.text
        else:
            return ""

    def getMangasByStatus(self, status):
        mangas_by_status = []
        if status in self.statuses:
            number = self.statuses[status]
        else:
            number = False
        for manga in self.mangas:
            if manga.status == status:
                mangas_by_status.append(manga)
            elif number and str(manga.status) == str(number):
                mangas_by_status.append(manga)
        return mangas_by_status
