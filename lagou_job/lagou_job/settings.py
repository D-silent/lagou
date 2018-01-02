BOT_NAME = 'lagou_job'
SPIDER_MODULES = ['lagou_job.spiders']
NEWSPIDER_MODULE = 'lagou_job.spiders'
ROBOTSTXT_OBEY = False
#  DOWNLOAD_DELAY = 4
#  USER_AGENT = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'

DOWNLOADER_MIDDLEWARES = {
        'lagou_job.middlewares.RandomUserAgentMiddleware': 543,
        'lagou_job.middlewares.ProxyMiddleware': 544,
}

ITEM_PIPELINES = {
        'lagou_job.pipelines.UniquePipeline': 300,
        'lagou_job.pipelines.IntegrityPipeline': 301,
        'lagou_job.pipelines.TextPipeline': 302,
}
