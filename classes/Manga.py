class Manga:
    malUrlStart = "https://myanimelist.net/manga/"
    def __init__(self, _id, _name, my_status, _my_read_chapters):
        try:
           self.id = int(_id)
        except ValueError:
           self.id = -1
        self.url = self.malUrl()
        self.name = _name
        self.status = my_status
        try:
           self.chapters = int(_my_read_chapters)
        except ValueError:
           self.chapters = -1
    def malUrl(self):
        return "%s%s" % (self.malUrlStart, self.id)
