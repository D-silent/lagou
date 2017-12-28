import scrapy
from lagou_job.items import LagouJobItem


class Lagou(scrapy.Spider):
    name = 'lagou'

    def start_requests(self):
        url_mode = "https://www.lagou.com/jobs/%d.html"
        for page in range(1, 11):
            url = url_mode % page
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jobid = response.url.split('/')[-1].split('.')[0]
        jobname = response.xpath('//div[@class="job-name"]/@title')
        jobname = jobname.extract_first()
        p = response.xpath('//dd[@class="job_request"]/p[1]')
        salary = p.xpath('span[1]/text()').extract_first().strip()
        address = p.xpath('span[2]/text()').extract_first()
        address = address.split('/')[1].strip()
        experience = p.xpath('span[3]/text()').extract_first()
        experience = experience.split('/')[0].strip()
        edureq = p.xpath('span[4]/text()').extract_first()
        edureq = edureq.split('/')[0].strip()

        yield LagouJobItem(
                jobid=jobid,
                jobname=jobname,
                salary=salary,
                address=address,
                experience=experience,
                edureq=edureq,
                )
