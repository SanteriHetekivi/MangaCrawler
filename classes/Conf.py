'''
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
'''
import configparser
import os
class Conf:
    config = None
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.filename())
    def filename(self):
        directory  = os.path.dirname(os.path.abspath(__file__))
        return directory+"/../config.ini"
