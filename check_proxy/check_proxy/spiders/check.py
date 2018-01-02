# -*- coding: utf-8 -*-
import scrapy


class CheckSpider(scrapy.Spider):
    name = 'check'
    start_urls = ['http://www.goubanjia.com/']

    def parse(self, response):
        yield dict(text="check ok!")

        for url in response.xpath('//a/@href').extract():
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse)
