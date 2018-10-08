# -*- coding: utf-8 -*-
import csv
import os

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


class WriteNewsItemPipeline(object):
    def __init__(self):
        self.current_dir = os.getcwd()
        self.data_dir = os.path.join(self.current_dir, 'data')
        self.filename_title = 'titles.txt'
        self.file_title = None
        self.csvwriter_title = None

        self.filename_content = 'contents.txt'
        self.file_content = None
        self.csvwriter_content = None

    def open_spider(self, spider):
        self.file_title = open(os.path.join(self.data_dir, self.filename_title), 'w', encoding='utf-8')
        self.csvwriter_title = csv.writer(self.file_title)

        self.file_content = open(os.path.join(self.data_dir, self.filename_content), 'w', encoding='utf-8')
        self.csvwriter_content = csv.writer(self.file_content)

    def close_spider(self, spider):
        self.file_title.close()
        self.file_content.close()

    def process_item(self, item, spider):

        self.csvwriter_title.writerow([item['levels'], item['link'], item['release_date'], item.get('title', None)])
        self.csvwriter_content.writerow([item['link'], item.get('content', None)])

        return item