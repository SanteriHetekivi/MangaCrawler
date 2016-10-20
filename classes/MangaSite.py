'''
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
'''
from py_bing_search import PyBingWebSearch
from .Conf import Conf
from .Settings import Settings
import re

class MangaSite:
    genres = []
    included = False
    excluded = False
    manga_names = []

    def __init__(self):
        self.config = Conf().config
        self.settings = Settings()
        self.settings.parse()

    def getMangaSiteAddress(self, site, urlPart, manga):
        name = manga.name
        search_term = "%s %s %s %s" % (site, name, urlPart, "-forum")
        if self.settings.verbose:
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

    def get_updated_manga(self, manga):
        return False

    def get_new_mangas(self, mangas):
        return False

    def get_genres(self, question):
        genres = self.genres
        for key, genre in enumerate(genres):
            print("%s) %s" % (key, genre))
        str = input(question)
        keys = [int(s) for s in str.split() if s.isdigit()]
        genres = [i for j, i in enumerate(genres) if j in keys]
        if self.settings.verbose:
            print(genres)
        return genres

    def get_excluded_genres(self):
        self.excluded = self.get_genres("Give excluded genres:")

    def get_included_genres(self):
        self.included = self.get_genres("Give included genres:")

    def get_url(self, page):
        if self.excluded==False and self.included ==False:
            self.get_included_genres()
            self.get_excluded_genres()
        return self.parse_url(page)

    def parse_url(self, page):
        return False

    def set_manga_names(self, mangas):
        names = []
        for manga in mangas:
            names.append(self.trim(manga.name))
        self.manga_names = names

    def trim(self, str):
        return re.sub(r'\W+', '', str.lower().strip())

    def in_names(self, name):
        name = self.trim(name)
        for manga_name in self.manga_names:
            if manga_name in name or name in manga_name:
                return True
        return False



