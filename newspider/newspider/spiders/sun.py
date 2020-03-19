# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from newspider.items import NewspiderItem, Detail_Item

class SunSpider(CrawlSpider):
    name = 'sun'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=']
    # 实例化了一个链接提取器对象
    # 作用：根据指定规则（allow=“正则表达式”）进行制定连接的提取
    link = LinkExtractor(allow=r"type=4&page=\d+")
    # 获取新闻详情页连接
    lin_detail = LinkExtractor(allow=r'question/\d+/\d+\.shtml')
    rules = (
        # 作用：将link取到的所有连接进行请求发送
        Rule(link, callback='parse_item', follow=False),
        Rule(lin_detail, callback='parse_detail', follow=False),
    )

    def parse_item(self, response):
        # xpath 表达式中不能出现tbody标签
        tr_list = response.xpath('//*[@id="morelist"]/div/table[2]//tr/td/table//tr')
        # print(len(tr_list))
        for tr in tr_list:
            title = tr.xpath('./td[2]/a[2]/text()').extract_first()
            num = tr.xpath('./td[1]/text()').extract_first()
            item = NewspiderItem()
            item["title"] = title
            item["num"] = num

            yield item

    def parse_detail(self, response):
        content = response.xpath('/html/body/div[9]/table[2]/tbody/tr[1]/td/text()').extract_first()
        num = response.xpath('/html/body/div[9]/table[1]//tr/td[2]/span[2]/text()').extract_first()
        num = num.split(":")[1]
        # print(num)
        item = Detail_Item()
        item["num"] = num
        item["content"] = content

        yield item



