BOT_NAME = 'goubanjia'
SPIDER_MODULES = ['goubanjia.spiders']
NEWSPIDER_MODULE = 'goubanjia.spiders'
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True

#  SPIDER_MIDDLEWARES = {
  #  'goubanjia.middlewares.GoubanjiaSpiderMiddleware': 543,
#  }

DOWNLOADER_MIDDLEWARES = {
    'goubanjia.middlewares.RandomUserAgentMiddleware': 543,
}

ITEM_PIPELINES = {
    'goubanjia.pipelines.UniquePipeline': 300,
    'goubanjia.pipelines.IntegrityPipeline': 301,
    'goubanjia.pipelines.TextPipeline': 303,
    'goubanjia.pipelines.MysqlPipeline': 302,
}

DB_USER = 'scrapy'
DB_PASSWD = 'scrapy'
DB_DB = 'scrapy'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_CHARSET = 'utf8'
