'''
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
'''
from MangaCrawler import *

settings = Settings()
settings.from_sys_parameters()
crawler = MangaCrawler()
crawler.run(settings)
