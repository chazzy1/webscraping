# -*- coding: utf-8 -*-

class WriteItemPipeline(object):

	def __init__(self):
		self.filename = 'test1.txt'

	def open_spider(self, spider):
		self.file = open(self.filename, 'w')

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		line = '\t'.join(str(item.values())) + '\n'
		line = item["link"] + '\t' + str(item["nav_levels"])
		self.file.write(line)
		print(item)
		return item
