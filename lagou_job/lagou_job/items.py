import scrapy


class LagouJobItem(scrapy.Item):
    jobid = scrapy.Field()
    jobname = scrapy.Field()
    salary = scrapy.Field()
    address = scrapy.Field()
    experience = scrapy.Field()
    edureq = scrapy.Field()
