from .MAL import MAL
from .Manga import Manga
from .MangaCrawler import MangaCrawler
from .MangaFox import MangaFox
from .MangaSite import MangaSite
from .Settings import Settings
from .XML import XML


def main():
    settings = Settings()
    settings.from_sys_parameters()
    crawler = MangaCrawler()
    crawler.run(settings)
