# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class WangyiPipeline(object):
    conn = None
    cursor = None

    def open_spider(self, spider):
        # print("开始")
        self.conn = pymysql.Connect(host="127.0.0.1", port=3306, user="root", password="ssmy", db="spider",
                                    charset="utf8")
        print(self.conn)

    def process_item(self, item, spider):

        sql = 'insert into wangyi values(0, "{}", "{}")'.format(item["title"], item["content"])
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        # print("结束")
        self.cursor.close()
        self.conn.close()
    # pass