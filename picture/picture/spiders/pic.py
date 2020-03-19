# -*- coding: utf-8 -*-
import scrapy
from picture.items import PictureItem


class PicSpider(scrapy.Spider):
    name = 'pic'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://sc.chinaz.com/tupian/rentiyishu.html']

    def parse(self, response):

        div_list = response.xpath('//*[@id="container"]/div')
        for div in div_list:
            img_src = div.xpath("./div/a/img/@src2").extract_first()
            item = PictureItem()
            item["img_src"] = img_src

            yield item
            print(img_src)
        # pass

