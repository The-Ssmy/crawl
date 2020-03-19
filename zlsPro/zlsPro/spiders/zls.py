# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from redis import Redis
from zlsPro.items import ZlsproItem

class ZlsSpider(CrawlSpider):
    conn = Redis(host="127.0.0.1", port=6379)
    name = 'zls'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.4567tv.tv/index.php/vod/show/class/%E7%88%B1%E6%83%85/id/1.html']

    rules = (
        Rule(LinkExtractor(allow=r'/page/\d+\.html'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        li_list = response.xpath('/html/body/div[1]/div/div/div/div[2]/ul/li')
        for li in li_list:
            name = li.xpath('./div/a/@title').extract_first()
            detail_url = "https://www.4567tv.tv" + li.xpath('./div/a/@href').extract_first()
            item = ZlsproItem()
            item["name"] = name
            # 可以将爬取过的详情页的URL记录起来
            # ex == 0:数据插入失败   ex == 1:数据插入成功
            ex = self.conn.sadd("movie_detail_urls", detail_url)
            if ex == 1:
                print("有更新")
                yield scrapy.Request(detail_url, callback=self.parse_detail, meta={"item":item})
            else:
                print("暂无数据更新")

    def parse_detail(self, response):
        desc = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[5]/span[2]/text()').extract_first()
        item = response.meta["item"]
        item["desc"] = desc
        # print(item)

        yield item












