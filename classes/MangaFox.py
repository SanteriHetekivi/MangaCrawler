'''
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
'''
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
              "Shounen+Ai", "Slice+of+Life", "Smut", "Sports", "Supernatural", "Tragedy", "Webtoons","Yaoi", "Yuri"]
    def __init__(self):
        super().__init__()


    def get_updated_manga(self, manga):
        url = self.getMangaSiteAddress("mangafox", "manga", manga)
        if not url:
            return False
        if self.settings.verbose:
            print(url)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as htmlfile:
                soup = BeautifulSoup(htmlfile.read(), "lxml")
                volumes = soup.findAll("h3", { "class" : "volume" })
                if len(volumes) <= 0:
                    return 0
                volume = volumes[0]
                chaptername = volume.span.text;
                numbers = re.findall('\d+\.\d+|\d+', chaptername)
                length = len(numbers)
                if length <= 0:
                    return False
                chapters = numbers[length-1]
                numbers = re.findall('\d+', chapters)
                length = len(numbers)
                if length <= 0:
                    return False
                try:
                    chapters = int(numbers[0])
                except ValueError:
                    return False
                new_chapers = chapters-manga.chapters
                if new_chapers <= self.settings.min_chapters:
                    return False
                row = [manga.name.replace(",", " "), manga.chapters, new_chapers, url, manga.url]
                return row
        except urllib.error.HTTPError as err:
            return False

    def get_new_mangas(self, mangas):
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
            elif new_mangas == False:
                break
            page += 1
            end = int(round(time.time()))
            diff_time = end - start
            time.sleep(6-diff_time)
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
        url = "http://mangafox.me/search.php?"+self.make_genres_to_url()
        url += "is_completed=&advopts=1&sort=rating&order=za&page=%s" % (page)
        return url

    def get_new_mangas_from_url(self, url):
        if not url:
            return False
        if self.settings.verbose:
            print(url)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        rows = []
        try:
            with urllib.request.urlopen(req) as htmlfile:
                soup = BeautifulSoup(htmlfile.read(), "lxml")
                tables = soup.findAll("table", { "id" : "listing" })
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
                                    if chapters >= self.settings.min_chapters:
                                        if link.has_attr('href'):
                                            manga_url = link["href"]
                                        else:
                                            manga_url = ""
                                        google_url='https://www.google.fi/search?q=myanimelist.net'+urllib.parse.quote_plus(manga_name)+'+manga'
                                        row = [manga_name, chapters, manga_url, google_url]
                                        rows.append(row)
                                        if self.settings.verbose:
                                            print(row)
        except urllib.error.HTTPError as err:
            return False
        return rows





