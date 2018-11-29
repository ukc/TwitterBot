import tarfile
import json
import gzip
import os

class DataLoader(object):
	
	def __init__(self):
		self.DIR = "../data/"
		self.FILE = "database.txt"

	def load_data(self):
		tar_filename = self.DIR + "json.gold.tar.gz"
		tar_filepath = tarfile.open(tar_filename)
		text_file_filepath = open(self.DIR + self.FILE,"a+")
		for ith_file in tar_filepath.getmembers():
			tar_filepath.extract(ith_file, path=self.DIR)
			temp_file = self.DIR + ith_file.name
			with gzip.open(temp_file, "rb") as filepath:
				lines = filepath.readlines()
				for line in lines:
					json_decode = json.loads(line.decode("utf-8"))
					text_file_filepath.write(json_decode["text"].encode("utf-8"))
					text_file_filepath.write("\n")
			os.remove(temp_file)
		text_file_filepath.close()
		tar_filepath.close()

data_loader = DataLoader()
data_loader.load_data()
