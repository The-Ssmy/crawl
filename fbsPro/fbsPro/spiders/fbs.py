# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from fbsPro.items import FbsproItem

class FbsSpider(RedisCrawlSpider):
    name = 'fbs'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['http://www.xxx.com/']
    redis_key = "fbsQueue"
    rules = (
        Rule(LinkExtractor(allow=r'type=4&page=\d+'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):

        tr_list = response.xpath('//*[@id="morelist"]/div/table[2]//tr/td/table//tr')
        for tr in tr_list:
            title = tr.xpath('./td[2]/a[2]/text()').extract_first()
            status = tr.xpath('./td[3]/span/text()').extract_first()
            item = FbsproItem()
            item["title"] = title
            item["status"] = status

            yield item












