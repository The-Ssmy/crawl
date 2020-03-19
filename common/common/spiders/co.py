# -*- coding: utf-8 -*-
import scrapy


class CoSpider(scrapy.Spider):
    name = 'co'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://wenku.baidu.com/view/9d61bf1eb94ae45c3b3567ec102de2bd9605deb6.html']

    def parse(self, response):
        p_list = response.xpath('//*[@id="pageNo-1"]/div/div/div/div/div/p')
        print(p_list)
