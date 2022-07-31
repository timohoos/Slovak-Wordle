# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re


class SlovakDictScraperPipeline(object):

    def open_spider(self, spider):
        self.file = open('slovakdict.txt', 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        for idx in item:
            if re.search("^[^-().’! ]*$", item[idx]) and len(item[idx]) == 5:
                self.file.write(f"{item[idx]}\n")

        return item
