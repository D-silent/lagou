from random import choice
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import MySQLdb as mdb


class RandomUserAgentMiddleware(UserAgentMiddleware):
    agents = open("agent.dat").readlines()

    def process_request(self, request, spider):
        agent = choice(self.agents).strip()
        request.headers["User-Agent"] = agent
        request.headers["Connection"] = "close"

    def process_response(self, request, response, spider):
        if response.status != 200:
            agent = choice(self.agents).strip()
            request.headers["User-Agent"] = agent
            return request
        return response


class ProxyMiddleware:
    conn = mdb.connect('localhost', 'scrapy', 'scrapy', 'scrapy')
    cursor = conn.cursor()

    def get_proxy(self):
        cursor.execute('select * from proxy where status="active"')
        proxies = cursor.fetchall()
        proxy = choice(proxies)

        return proxy[0] + "://" + proxy[1]

    def process_request(self, request, spider):
        request.meta['proxy'] = self.get_proxy()
        request.meta['download_timeout'] = 3

    def process_response(self, request, response, spider):
        if response.status != 200 and response.status != 301:
            url = response.url
            sql = 'update url set status="no" where page=%s'
            self.cursor.execute(sql, args=(url,))
            self.conn.commit()

        return response
