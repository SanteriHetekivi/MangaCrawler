'''
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
'''
import sys, getopt

class Settings:
    verbose = False
    find = False
    site = False
    def parse(self):
        argv = sys.argv[1:]
        example = "manga-crawler.py -f <find-argument> -s <site>"
        try:
            opts, args = getopt.getopt(argv, "f:s:h:v", ["find=", "site=", "help"])
        except getopt.GetoptError:
            print(example)
            return False
        for opt, arg in opts:
            if opt == "-v":
                self.verbose = True
            elif opt in ("-h", "--help"):
                print(example)
                return False
            elif opt in ("-f", "--find"):
                self.find = arg
            elif opt in ("-s", "--site"):
                self.site = arg
        if self.verbose:
            print(self.site)
            print(self.find)
        if self.find == False or self.site == False:
            print(example)
            return False
        return True