# -*- coding: utf-8 -*-
import scrapy
from huyaPro.items import HuyaproItem

class HuyaSpider(scrapy.Spider):
    name = 'huya'
    # allowed_domains = ['ojwdojwd']
    start_urls = ['https://www.huya.com/g/lol/']
    url = "https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId=1&tagAll=0&page={}"

    def parse(self, response):
        div_list = response.xpath('//*[@id="js-live-list"]/li')

        all_data = []
        for div in div_list:
            title = div.xpath("./a[2]/text()").extract()
            name = div.xpath("./span/span[1]/i/text()").extract()
            heat = div.xpath("./span/span[2]/i[2]/text()").extract()
            dic = {
                "title":title,
                "name":name,
                "heat":heat
            }
            all_data.append(dic)
            item = HuyaproItem()
            item["title"] = title
            item["name"] = name
            item["heat"] = heat

            yield item
        # 手动请求的发送
        for page in range(2, 5):
            new_url = self.url.format(page)
            # 发送的是GET请求
            # 请求传参 让request将一个数据值（字典）传递给回调函数
            yield scrapy.Request(url=new_url, callback=self.parse_other, meta={"item":item})

        return all_data

    # 所有的解析方法都必须模拟parse进行定义：必须有和parse同样的参数
    def parse_other(self, response):
        # 接受请求传参的数据
        item = response.meta["item"]
        print(response.text)

        yield item

