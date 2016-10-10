import xml.etree.ElementTree as ET
from .XML import XML
from .Manga import Manga

class MAL:

    mangas = []
    def __init__(self):
        print(self.parse())

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
                        self.getInfo(manga, "manga_mangadb_id"),
                        self.getInfo(manga, "manga_title"),
                        self.getInfo(manga, "my_status"),
                        self.getInfo(manga, "my_read_chapters")
                        )
                )
            return 1
        return 0
    def getInfo(self, manga, infoname):
        return  manga.find(infoname).text

    def getMangasByStatus(self, status):
        mangas_by_status = []
        for manga in self.mangas:
            if manga.status == status:
                mangas_by_status.append(manga)
        return mangas_by_status
