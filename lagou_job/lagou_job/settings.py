BOT_NAME = 'lagou_job'
SPIDER_MODULES = ['lagou_job.spiders']
NEWSPIDER_MODULE = 'lagou_job.spiders'
ROBOTSTXT_OBEY = False
#  DOWNLOAD_DELAY = 12

DOWNLOADER_MIDDLEWARES = {
        'lagou_job.middlewares.RandomUserAgentMiddleware': 543,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
        'lagou_job.middlewares.ProxyMiddleware': 544,
}

ITEM_PIPELINES = {
        'lagou_job.pipelines.UniquePipeline': 300,
        'lagou_job.pipelines.IntegrityPipeline': 301,
        'lagou_job.pipelines.TextPipeline': 302,
}
