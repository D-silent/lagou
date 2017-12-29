# -*- coding: utf-8 -*-
import scrapy
from goubanjia.items import ProxyItem


class GoubanjiaspiderSpider(scrapy.Spider):
    name = 'proxy'
    start_urls = [
            'http://goubanjia.com/free/index%d.shtml' % page
                for page in range(1, 600)
            ]

    def parse(self, response):
        trs = response.xpath('//tr')
        for tr in trs[1:]:
            tds = tr.xpath('td')
            proxylist = tds[0].xpath('div/text() | span/text()').extract()
            ip = "".join(proxylist[:-1])
            port = tds[0].xpath('span/@class').extract()[-1].split()[-1]
            realport = ""
            for c in port:
                realport += str("ABCDEFGHIZ".find(c))
            realport = int(realport) >> 3
            proxytype = tds[2].xpath('a/text()').extract_first()
            proxy = "%s:%d" % (ip, realport)

            yield ProxyItem(proxytype=proxytype, proxy=proxy)
