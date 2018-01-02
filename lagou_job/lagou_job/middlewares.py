from random import choice
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import MySQLdb as mdb


class RandomUserAgentMiddleware(UserAgentMiddleware):
    agents = open("agent.dat").readlines()

    def process_request(self, request, spider):
        agent = choice(self.agents).strip()
        request.headers["User-Agent"] = agent
        #  request.headers["Connection"] = "close"

    def process_response(self, request, response, spider):
        if response.status != 200:
            agent = choice(self.agents).strip()
            request.headers["User-Agent"] = agent
            return request
        return response


class ProxyMiddleware:
    conn = mdb.connect('localhost', 'scrapy', 'scrapy', 'scrapy')
    cursor = conn.cursor()
    flag = True
    count = 0
    sql = 'select * from proxy where proxytype=%s and status=%s'
    data = ('https', 'active')
    cursor.execute(sql, args=data)
    proxies = cursor.fetchall()

    def get_proxy(self):
        proxy = choice(self.proxies)

        return proxy[0] + "://" + proxy[1]

    def process_request(self, request, spider):
        if self.flag:
            self.proxy = self.get_proxy()
            self.flag = False
        self.count += 1
        if self.count > 4:
            count = 0
            self.flag = True
        request.meta['proxy'] = self.proxy
        request.meta['download_timeout'] = 30

    def process_response(self, request, response, spider):
        url = response.url
        sql = 'update url set status=%s where page=%s'
        if response.status != 200 and response.status != 301:
            self.cursor.execute(sql, args=("no", url))
            self.conn.commit()
        elif response.status == 301:
            del_sql = 'delete from url where page=%s'
            self.cursor.execute(del_sql, args=(url, ))
            self.conn.commit()
        else:
            self.cursor.execute(sql, args=("yes", url))
            self.conn.commit()
            return response
