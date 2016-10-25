"""
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
"""
from .MangaSite import MangaSite
import urllib
import re
import urllib.request
import urllib.parse

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
import time


class MangaFox(MangaSite):
    genres = ["Action", "Adult", "Adventure", "Comedy", "Doujinshi", "Drama", "Ecchi", "Fantasy", "Gender Bender",
              "Harem", "Historical", "Horror", "Josei", "Martial+Arts", "Mature", "Mecha", "Mystery", "One+Shot",
              "Psychological", "Romance", "School+Life", "Sci-fi", "Seinen", "Shoujo", "Shoujo+Ai", "Shounen",
              "Shounen+Ai", "Slice+of+Life", "Smut", "Sports", "Supernatural", "Tragedy", "Webtoons", "Yaoi", "Yuri"]

    def __init__(self, verbose=False):
        super().__init__(verbose)

    def get_updated_manga(self, manga, min_chapters=0, azure_account_key=None):
        if azure_account_key:
            self.azure_account_key = azure_account_key
        self.min_chapters = min_chapters
        url = self.get_manga_site_address("mangafox", "manga", manga)
        if not url:
            return False
        if self.verbose:
            print(url)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as html_file:
                soup = BeautifulSoup(html_file.read(), "lxml")
                volumes = soup.findAll("h3", {"class": "volume"})
                if len(volumes) <= 0:
                    return 0
                volume = volumes[0]
                chapter_name = volume.span.text
                numbers = re.findall('\d+\.\d+|\d+', chapter_name)
                length = len(numbers)
                if length <= 0:
                    return False
                chapters = numbers[length - 1]
                numbers = re.findall('\d+', chapters)
                length = len(numbers)
                if length <= 0:
                    return False
                try:
                    chapters = int(numbers[0])
                except ValueError:
                    return False
                new_chapters = chapters - manga.chapters
                if new_chapters <= min_chapters:
                    return False
                row = [manga.name.replace(",", " "), manga.chapters, new_chapters, url, manga.url]
                return row
        except urllib.error.HTTPError as err:
            return False

    def get_new_mangas(self, mangas, min_chapters=0):
        self.min_chapters = min_chapters
        page = 1
        self.set_manga_names(mangas)
        mangas = []
        new = False
        while True:
            url = self.get_url(page)
            start = int(round(time.time()))
            new_mangas = self.get_new_mangas_from_url(url)
            if new_mangas:
                if new_mangas[0] != new:
                    new = new_mangas[0]
                else:
                    break
                mangas += new_mangas
            elif not new_mangas:
                break
            page += 1
            end = int(round(time.time()))
            diff_time = end - start
            sleep_time = (6 - diff_time) if (6 - diff_time) > 0 else 0
            time.sleep(sleep_time)
        return mangas

    def make_genres_to_url(self):
        url = ""
        for genre in self.genres:
            if self.included and genre in self.included:
                url += "genres%5B{0}%5D=1&".format(genre)
            elif self.excluded and genre in self.excluded:
                url += "genres%5B{0}%5D=2&".format(genre)
            else:
                url += "genres%5B{0}%5D=0&".format(genre)
        return url

    def parse_url(self, page):
        url = "http://mangafox.me/search.php?" + self.make_genres_to_url()
        url += "is_completed=&advopts=1&sort=rating&order=za&page=%s" % page
        return url

    def get_new_mangas_from_url(self, url):
        if not url:
            return False
        if self.verbose:
            print(url)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        rows = []
        try:
            with urllib.request.urlopen(req) as htmlfile:
                soup = BeautifulSoup(htmlfile.read(), "lxml")
                tables = soup.findAll("table", {"id": "listing"})
                if len(tables) > 0:
                    trs = tables[0].findChildren(['tr'])
                    for tr in trs:
                        cells = tr.findChildren('td')
                        if len(cells) == 5:
                            links = cells[0].findChildren(['a'])
                            if len(links) > 0:
                                link = links[0]
                                manga_name = link.text
                                if not self.in_names(manga_name):
                                    chapters = int(cells[3].text)
                                    manga_name = manga_name.replace(",", " ")
                                    if chapters >= self.min_chapters:
                                        if link.has_attr('href'):
                                            manga_url = link["href"]
                                        else:
                                            manga_url = ""
                                        google_url = 'https://www.google.fi/search?q=myanimelist.net+' + \
                                                     urllib.parse.quote_plus(manga_name) + '+manga'
                                        row = [manga_name, chapters, manga_url, google_url]
                                        rows.append(row)
                                        if self.verbose:
                                            print(row)
        except urllib.error.HTTPError as err:
            return False
        return rows
