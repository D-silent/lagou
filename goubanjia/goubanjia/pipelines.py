# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem


def genid(item):
    text = '%s:%s' % (item.get('proxytype'), item.get('proxy'))
    return hashlib.sha1(text.encode('utf-8')).hexdigest()


def scan(item):
    for key in item.fields:
        if key not in item or not item[key]:
            return False
    return True


class UniquePipeline(object):

    def process_item(self, item, spider):
        item_id = genid(item)
        if item_id in self.all_ids:
            raise DropItem('item exists')

        self.all_ids.append(item_id)

        return item

    def open_spider(self, spider):
        self.all_ids = []


class IntegrityPipeline(object):

    def process_item(self, item, spider):
        if not scan(item):
            raise DropItem('item is incomplete')

        return item


class TextPipeline:

    def open_spider(self, spider):
        self.f = open('proxy.dat', 'w')

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        self.f.write(item['proxytype'] + '\t' + item['proxy'] + '\n')
        self.f.flush()
        return item


class MysqlPipeline:

    def __init__(self, user, passwd, db, host, port, charset):
        self.user = user
        self.passwd = passwd
        self.db = db
        self.host = host
        self.port = port
        self.charset = charset

    def open_spider(self, spider):
        self.conn = MySQLdb.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.passwd,
                database=self.db,
                charset=self.charset
                )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        sql = 'insert into proxy values(%s, %s, %s)'
        data = (item['proxytype'], item['proxy'], 'inactive')
        self.cursor.execute(sql, args=data)
        self.conn.commit()
        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
                user=crawler.settings.get('DB_USER'),
                passwd=crawler.settings.get('DB_PASSWD'),
                db=crawler.settings.get('DB_DB'),
                host=crawler.settings.get('DB_HOST'),
                port=crawler.settings.get('DB_PORT'),
                charset=crawler.settings.get('DB_CHARSET'),
                )
