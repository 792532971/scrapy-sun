# -*- coding: utf-8 -*-
import pymysql
from twisted.enterprise import adbapi
import datetime
import logging
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class SunPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipeline(object):
    def __init__(self, pool):
        self.pool = pool

    @classmethod
    def from_settings(cls, settings):
        # 获取settings文件中的配置
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )

        pool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(pool)

    def process_item(self, item, spider):

        query = self.pool.runInteraction(self.do_insert, item)

        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """
                insert into sun(num, title, href, guanli, status, faqiren, date_time)
                values (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (
        item["num"], item["title"], item['href'], item['guanli'], item['status'], item['faqiren'], item['date_time']))


class MysqlPipeline(object):
    # open_spider()和close_spider()：只在爬虫被打开和关闭时，执行一次。
    def open_spider(self, spider):
        self.connect = pymysql.connect(
            host='localhost',
            user='root',
            port=3306,
            passwd='root',
            db='test',
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        insert_sql = "INSERT INTO sun(num, title, href, guanli, status, faqiren, date_time, content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(insert_sql, (
            item["num"], item["title"], item['href'], item['guanli'], item['status'], item['faqiren'],
            item['date_time'], item['content']))
        self.connect.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()


