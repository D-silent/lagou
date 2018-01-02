# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib
from scrapy.exceptions import DropItem


def genid(item):
    text = '%s:%s:%s:%s:%s:%s' % (item.get('jobid'), item.get('jobname'),
            item.get('salary'), item.get('address'), item.get('experience'),
            item.get('edureq'))
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


class TextPipeline(object):

    def process_item(self, item, spider):
        op = ['jobid', 'jobname', 'salary', 'address', 'experience', 'edureq']
        for k in op:
            v = item[k]
            self.file.write('%s: %s\n' % (k, v))
        self.file.write('\n')

        return item

    def open_spider(self, spider):
        self.file = open('item.txt', 'a')
