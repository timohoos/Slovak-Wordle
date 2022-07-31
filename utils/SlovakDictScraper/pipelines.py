# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re
import os.path
import toml
import psycopg2
from psycopg2 import Error


class SlovakDictScraperPipeline(object):

    def open_spider(self, spider):
        settings = (toml.load(os.path.dirname(__file__) + "/../../settings.toml"))

        try:
            self.connection = psycopg2.connect(user=settings["database"]["user"],
                                    password=settings["database"]["password"],
                                    host=settings["database"]["host"],
                                    port=settings["database"]["port"],
                                    database=settings["database"]["database"])
            self.cursor = self.connection.cursor()

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def close_spider(self, spider):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def process_item(self, item, spider):
        for idx in item:
            if re.search("^[^-().’! ]*$", item[idx]) and len(item[idx]) == 5:
                self.cursor.execute("insert into words (word) values(%s)", (item[idx],))


        self.connection.commit()
        return item
