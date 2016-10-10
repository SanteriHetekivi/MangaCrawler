from classes.MangaCrawler import MangaCrawler
import sys

verbose = "-v" in sys.argv
crawler = MangaCrawler(verbose)
if crawler.run("mangafox"):
    print("DONE")
else:
    print("ERROR")
