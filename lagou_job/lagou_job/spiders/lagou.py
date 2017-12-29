import scrapy
from lagou_job.items import LagouJobItem
import MySQLdb as mdb


class Lagou(scrapy.Spider):
    name = 'lagou'
    conn = mdb.connect('localhost', 'scrapy', 'scrapy', 'scrapy')
    cursor = conn.cursor()
    sql = 'select * from url where status="no"'

    def get_one_url(self):
        self.cursor.execute(sql)
        return cursor.fetchone()

    def start_requests(self):
        while True:
            url = self.get_one_url()
            if url:
                url = url[0]
                print(url)
                yield scrapy.Request(url=url, callback=self.parse)
            else:
                break

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
