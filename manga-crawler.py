'''
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
'''
from classes.MangaCrawler import MangaCrawler
import sys

verbose = "-v" in sys.argv
crawler = MangaCrawler(verbose)
if crawler.run("mangafox"):
    print("DONE")
else:
    print("ERROR")
