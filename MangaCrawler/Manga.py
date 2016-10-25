"""
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
"""


class Manga:
    malUrlStart = "https://myanimelist.net/manga/"

    def __init__(self, _id, _name, my_status, _my_read_chapters, _synonyms=""):
        try:
            self.id = int(_id)
        except ValueError:
            self.id = -1
        self.url = self.mal_url()
        self.name = _name
        self.status = my_status
        if _synonyms:
            self.synonyms = _synonyms.split('; ')
        else:
            self.synonyms = []
        try:
            self.chapters = int(_my_read_chapters)
        except ValueError:
            self.chapters = -1

    def mal_url(self):
        return "%s%s" % (self.malUrlStart, self.id)
