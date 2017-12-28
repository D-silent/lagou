# -*- coding: utf-8 -*-
import scrapy


class GoubanjiaspiderSpider(scrapy.Spider):
    name = 'proxy'
    start_urls = [
            'http://goubanjia.com/free/gngn/index%d.shtml' % page
                for page in range(1, 203)
            ]

    def parse(self, response):
        print(response.url)
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
            proxy = "%s://%s:%d\n" % (proxytype, ip, realport)

            yield dict(proxy=proxy)
