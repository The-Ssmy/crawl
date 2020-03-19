# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class PicturePipeline(object):
#     def process_item(self, item, spider):
#         return item

from scrapy.pipelines.images import ImagesPipeline
import scrapy

class PicturePipeline(ImagesPipeline):
    # 是用来对媒体资源进行请求的（数据下载），参数item就是接收到的爬虫类提交的item对象
    def get_media_requests(self, item, info):
        yield scrapy.Request(item["img_src"])

    # 指名数据存储的路径
    def file_path(self, request, response=None, info=None):
        return request.url.split("/")[-1]

    # 将item传递给下一个即将被执行那个的管道类
    def item_completed(self, results, item, info):
        return item





