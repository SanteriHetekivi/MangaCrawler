from classes.MangaCrawler import MangaCrawler

crawler = MangaCrawler()
if crawler.run("mangafox"):
    print("DONE")
else:
    print("ERROR")
