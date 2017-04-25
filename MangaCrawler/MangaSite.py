"""
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
"""
import re

import http.client, urllib.request, urllib.parse, urllib.error, base64
from unidecode import unidecode
import json


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

        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': api_key,
        }

        params = urllib.parse.urlencode({
            'q': search_term,
            'count': '1',
            'offset': '0',
            'mkt': 'en-us',
            'safesearch': 'Moderate',
        })

        try:
            conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
            conn.request("GET", "/bing/v5.0/search?%s" % params, "{body}", headers)
            response = conn.getresponse()
            string = response.read().decode('utf-8')
            data = json.loads(string)
            results = data["webPages"]["value"]
            conn.close()
            length = len(results)
            if length > 0 and site in results[0]["displayUrl"] and url_part in results[0]["displayUrl"]:
                manga_site_url = results[0]["displayUrl"]
                parts = manga_site_url.split("/")
                manga_site_url = ""
                stop_next = 0
                for part in parts:
                    manga_site_url += part + "/"
                    if part == url_part:
                        stop_next = 1
                    elif stop_next:
                        break
                return "%s%s" % ("http://", manga_site_url)
            else:
                return False
        except Exception as e:
            print(e)
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
