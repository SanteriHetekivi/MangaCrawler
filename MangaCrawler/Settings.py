"""
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
"""
import getopt
import sys


class Settings:
    def __init__(self, find=None, site=None, verbose=False, min_chapters=0, azure_account_key=None,
                 manga_xml_file=None, output_file=None):
        self.verbose = verbose
        self.find = find
        self.site = site
        self.min_chapters = min_chapters
        self.azure_account_key = azure_account_key
        self.manga_xml_file = manga_xml_file
        self.output_file = output_file

    def from_sys_parameters(self):
        argv = sys.argv[1:]
        example = "MangaCrawler -f <find-argument> -s <site>"
        try:
            opts, args = getopt.getopt(argv, "f:s:c:a:m:o:h:v",
                                       ["find=", "site=", "min-chapters=", "azure-account-key=",
                                        "manga-xml-file=", "output-file=", "help"])
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
            elif opt in ("-c", "--min-chapters"):
                try:
                    self.min_chapters = int(arg)
                except ValueError:
                    self.min_chapters = 0
            elif opt in ("-a", "--azure-account-key"):
                self.azure_account_key = arg
            elif opt in ("-m", "--manga-xml-file"):
                self.manga_xml_file = arg
            elif opt in ("-o", "--output-file"):
                self.output_file = arg
        if self.find is False or self.site is False or (self.find == "updated" and not self.azure_account_key):
            print(example)
            return False
        print(self.azure_account_key)
        return True
