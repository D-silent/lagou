import scrapy
from lagou_job.items import LagouJobItem
import MySQLdb as mdb


class Lagou(scrapy.Spider):
    name = 'lagou'
    conn = mdb.connect('localhost', 'scrapy', 'scrapy', 'scrapy')
    cursor = conn.cursor()

    def get_all_url(self):
        sql = 'select * from url where status="no"'
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def start_requests(self):
        urls = self.get_all_url()
        for url in urls:
            url = url[0]
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jobid = response.url.split('/')[-1].split('.')[0]
        jobname = response.xpath('//div[@class="job-name"]/@title')
        jobname = jobname.extract_first()
        p = response.xpath('//dd[@class="job_request"]/p[1]')
        salary = p.xpath('span[1]/text()').extract_first()
        if salary:
            salary = salary.strip()
        address = p.xpath('span[2]/text()').extract_first()
        if address:
            address = address.split('/')[1].strip()
        experience = p.xpath('span[3]/text()').extract_first()
        if experience:
            experience = experience.split('/')[0].strip()
        edureq = p.xpath('span[4]/text()').extract_first()
        if edureq:
            edureq = edureq.split('/')[0].strip()

        yield LagouJobItem(
                jobid=jobid,
                jobname=jobname,
                salary=salary,
                address=address,
                experience=experience,
                edureq=edureq,
                )
