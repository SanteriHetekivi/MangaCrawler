'''
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
'''
from py_bing_search import PyBingWebSearch
from .Conf import Conf
from .Settings import Settings

class MangaSite:
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
    def getUpdatedManga(self, manga):
        return False