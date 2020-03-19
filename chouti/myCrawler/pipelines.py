# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# 管道类 专门用作于持久化存储
class MycrawlerPipeline(object):
    fp = None

    def open_spider(self, spider):
        print("开始时调用一次")
        self.fp = open("./data.txt", "w", encoding="utf-8")

    def process_item(self, item, spider):
        content = item["content"]
        # print(content)
        for i in content:
            self.fp.write(i + "\n")
        return item

    def close_spider(self, spider):
        print("结束是调用")
        self.fp.close()








