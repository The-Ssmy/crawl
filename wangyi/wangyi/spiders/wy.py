# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from wangyi.items import WangyiItem
import time

class WySpider(scrapy.Spider):
    name = 'wy'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://news.163.com/']
    model_urls = []
    bro = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

    def parse(self, response):
        # 解析出五个板块对应的url
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        model_index = [7, 8]
        for index in model_index:
            # li依次表示的是五个版块对应的li标签
            li = li_list[index]
            model_url = li.xpath('./a/@href').extract_first()
            # print(model_url)
            self.url = model_url
            print(self.url, model_url)
            self.model_urls.append(model_url)
            # 对每一个板块的url进行手动请求的发送
            if self.model_urls[-1] == "http://news.163.com/uav/":
                yield scrapy.Request(self.model_urls[-1], callback=self.parse_model)
            else:
                yield scrapy.Request(self.model_urls[-1], callback=self.parse_model2)

    # 解析每一个版块对应页面数据中的新闻标题和新闻详情页的URL
    def parse_model(self, response):

            div_list = response.xpath("/html/body/div[1]/div[3]/div[2]/div[2]/div[1]/div[1]/div/ul/li/div/div")

            for div in div_list:
                title = div.xpath("./div/h3/a/text()").extract()

                print(title)
                detail_url = div.xpath("./div[1]/h3/a/@href").extract()
                print(detail_url)
                item = WangyiItem()
                item["title"] = title
                item["content"] = detail_url

                yield item

    def parse_model2(self, response):

            div_list = response.xpath("/html/body/div/div[3]/div[4]/div[1]/div/div/ul/li/div/div")

            for div in div_list:
                title = div.xpath("./a/img/@alt").extract()
                print("*********************************************************************")
                print(title)
                detail_url = div.xpath("./a/img/@src").extract()
                print("----------------------------------------------------------")
                print(detail_url)
                item = WangyiItem()
                item["title"] = title
                item["content"] = detail_url

                yield item

            # yield scrapy.Request(str(detail_url), callback=self.parse_new_detail, meta={"item":item})

    # def parse_new_detail(self, response):
    #     item = response.meta["item"]
    #     content = response.xpath("/html/body/div[3]/div[2]/div[2]/h2/div[2]/div/p/text()").extract()
    #     print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #     print(content)
    #     item["content"] = content
    #     yield item

    # 该方法只会在整个程序结束的时候执行一次
    def closed(self, spider):
        self.bro.quit()






