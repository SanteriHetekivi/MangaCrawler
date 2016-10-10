'''
  Made by Santeri Hetekivi.
  Licensed under Apache License 2.0.
  10/2016
'''
import os
import glob
import xml.etree.ElementTree as ET
import ntpath

class XML:
	def getFilename(self):
		directory  = os.path.dirname(os.path.abspath(__file__))
		path = directory+'/../data/*.xml'
		files = glob.glob(path)
		length = len(files)
		if length <= 0:
			print("No XML files in directory!")
			return 0
		elif length == 1:
			return files[0]
		else:
			fileno = -1
			while fileno < 0 or fileno >= length:
				no = 1
				print("Found XML files:")
				for filename in files:
					str = "%s) %s" % (no, ntpath.basename(filename))
					print(str)
					no += 1
				try:
				   fileno = int(input("Select file: "))
				except ValueError:
				   print("Give a number!")
				   fileno = -1
				fileno -= 1
			filename = files[fileno]
			return filename
	def getXMLRoot(self):
		filename = self.getFilename()
		if isinstance(filename, str):
			tree = ET.parse(filename)
			root = tree.getroot()
			return root
		else:
			return 0
