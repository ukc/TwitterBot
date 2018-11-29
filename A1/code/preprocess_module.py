import re

class Preprocess(object):
	def __init__(self):
		self.DIR = "../data/"
		self.RAW_FILE = "database.txt"
		self.NEW_FILE = "working_data.txt"

	#removing newlines and urls
	def remove_unnecessary(self):
		raw_file = open(self.DIR+self.RAW_FILE,"r")
		temp_file = open(self.DIR+self.NEW_FILE,"w")
		lines = raw_file.readlines()
		for line in lines:
			if(line == "\n"):
				continue
			else:
				line = re.sub('http\S+','', line, flags=re.MULTILINE)			
				if(line != "\n"):
					try:
						line.encode(encoding='utf-8').decode('ascii')			
					except UnicodeDecodeError:
						continue
					else:
						temp_file.write(line)
		raw_file.close()
		temp_file.close()

				
preprocess = Preprocess()
preprocess.remove_unnecessary()
