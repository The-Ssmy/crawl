# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ZlsproPipeline(object):
    def process_item(self, item, spider):
        conn = spider.conn
        conn.lpush('movieData', item)
        return item
