# -*- coding: utf-8 -*-
import scrapy
from myCrawler.items import MycrawlerItem

class SsmySpider(scrapy.Spider):
    # 爬虫文件的名称：爬虫源文件的唯一标识
    name = 'ssmy'

    # 允许的域名：举个例子下面列表中的第二个就无法请求 但是一般会进行屏蔽这一行代码
    # allowed_domains = ['www.baidu.com']

    # 起始的URL列表：列表中的列表元素会被scrapy自动的进行请求发送
    start_urls = ['https://dig.chouti.com/']

    # 解析数据 + 管道的持久化存储
    def parse(self, response):
        # data_list = []
        div_list = response.xpath("/html/body/main/div/div/div[1]/div/div[2]/div[1]")

        """
        /html/body/main/div/div/div[1]/div/div[2]/div[1]
        /html/body/main/div/div/div[1]/div/div[2]/div[1]/div[1]/div
        /html/body/main/div/div/div[1]/div/div[2]/div[1]/div[4]/div
        /html/body/main/div/div/div[1]/div/div[2]/div[1]/div[3]/div/div/div[1]/a
        """

        # print(div_list)
        for div in div_list:
            # 注意：xpath返回的列表中的列表元素是selector对象，我们要解析获取的字符串的数据是存储在该对象中的，必须经过一个 extract()的操作才可以将该对象中存储的字符串的的数据获取
            content = div.xpath("./div/div/div/div[1]/a/text()").extract()
            item = MycrawlerItem()
            item["content"] = content
            # xpath返回的列表元素有多个, 想要将每一个列表元素对应的字符串取出该如何操作
            print(content)
            print(item)

            yield item

