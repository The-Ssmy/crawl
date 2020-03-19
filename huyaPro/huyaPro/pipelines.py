# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import redis

class HuyaproPipeline(object):
    fp = None

    def open_spider(self, spider):
        print("开始")
        self.fp = open("./data.txt", "w", encoding="utf-8")

    def process_item(self, item, spider):
        title = item["title"]
        name = item["name"]
        heat = item["heat"]
        list1 = []
        # print(content)
        for i in range(len(name)):
            self.fp.write(title[i] + " "*(50-(2*len(title[i]))) + name[i] + " "*(80 - 50 - (2*len(name[i]))) + heat[i] + "\n")

        return item   # 返回给下一个优先级的pipeline

    def close_spider(self, spider):
        print("结束")
        self.fp.close()



class mysqlHuyaproPipeline(object):

    conn = None
    cursor = None
    def open_spider(self, spider):
        self.conn = pymysql.Connect(host="127.0.0.1", port=3306, user="root", password="ssmy", db="spider", charset="utf8")
        print(self.conn)

    def process_item(self, item, spider):
        title = item["title"]
        name = item["name"]
        heat = item["heat"]
        for i in range(len(name)):
            sql = 'insert into huya values(0, "{}", "{}", "{}")'.format(title[i], name[i], heat[i])
            self.cursor = self.conn.cursor()
            try:
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(e)
                self.conn.rollback()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

class redisHuyaproPipeline(object):

    conn = None
    def open_spider(self, spider):
        self.conn = redis.Redis(host="127.0.0.1", port=6379, charset="utf8")
        print(self.conn)

    def process_item(self, item, spider):
        title = item["title"]
        name = item["name"]
        heat = item["heat"]
        # print(type(item))
        # for i in item:
        # #     # print(item[i])
        #     print(item[i])
        self.conn.lpush("huyaList", str(item))

        return item

    def close_spider(self, spider):
        self.conn.close()



