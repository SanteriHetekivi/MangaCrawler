"""
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
"""
import re

from py_bing_search import PyBingWebSearch
from unidecode import unidecode


class MangaSite:
    genres = []
    included = False
    excluded = False
    manga_names = []
    min_chapters = 0
    azure_account_key = None

    def __init__(self, verbose=False):
        self.verbose = verbose

    def get_manga_site_address(self, site, url_part, manga, azure_account_key=None):
        if azure_account_key:
            self.azure_account_key = azure_account_key
        name = unidecode(manga.name)
        search_term = "%s %s %s %s" % (site, self.trim(name), url_part, "-forum")
        if self.verbose:
            print(search_term)
        api_key = self.azure_account_key
        if not api_key:
            return False
        bing_web = PyBingWebSearch(api_key, search_term, web_only=False)
        results = bing_web.search(limit=1, format='json')
        length = len(results)
        if length > 0 and site in results[0].url and url_part in results[0].url:
            manga_site_url = results[0].url
            parts = manga_site_url.split("/")
            manga_site_url = ""
            stop_next = 0
            for part in parts:
                manga_site_url += part + "/"
                if part == url_part:
                    stop_next = 1
                elif stop_next:
                    break
            return manga_site_url
        else:
            return False

    def get_updated_manga(self, manga, min_chapters=0):
        return False

    def get_new_mangas(self, mangas, min_chapters=0):
        return False

    def get_genres(self, question):
        genres = self.genres
        for key, genre in enumerate(genres):
            print("%s) %s" % (key, genre))
        input_srt = input(question)
        keys = [int(s) for s in input_srt.split() if s.isdigit()]
        genres = [i for j, i in enumerate(genres) if j in keys]
        if self.verbose:
            print(genres)
        return genres

    def get_excluded_genres(self):
        self.excluded = self.get_genres("Give excluded genres:")

    def get_included_genres(self):
        self.included = self.get_genres("Give included genres:")

    def get_url(self, page):
        if self.excluded is False and self.included is False:
            self.get_included_genres()
            self.get_excluded_genres()
        return self.parse_url(page)

    def parse_url(self, page):
        return False

    def set_manga_names(self, mangas):
        names = []
        for manga in mangas:
            names.append(self.trim(manga.name))
            for synonym in manga.synonyms:
                names.append(self.trim(synonym))
        self.manga_names = names

    @staticmethod
    def trim(string):
        return unidecode(re.sub(r'\W+', '', re.sub(r'\([^)]*\)', '', string.lower()).strip()))

    def in_names(self, name):
        name = self.trim(name)
        # for manga_name in self.manga_names:
        # if manga_name in name or name in manga_name:
        # return True
        return name in self.manga_names
