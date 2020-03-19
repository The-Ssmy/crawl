# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class NewspiderPipeline(object):
    def process_item(self, item, spider):

        if item.__class__.__name__ == "Detail_Item":
            content = item["content"]
            num = item["num"]
            print(item)
        else:
            title = item["title"]
            num = item["num"]
            print(item)

        return item


