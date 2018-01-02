import MySQLdb as mdb


class CheckMiddleware:
    conn = mdb.connect('localhost', 'scrapy', 'scrapy', 'scrapy')
    cursor = conn.cursor()
    cursor.execute('select * from proxy')
    proxies = cursor.fetchall()
    length = len(proxies)
    num = 0

    def process_request(self, request, spider):
        proxy = self.proxies[self.num]
        self.num += 1
        self.num %= self.length
        request.meta['proxy'] = proxy[0] + "://" + proxy[1]
        request.meta['download_timeout'] = 3

    def process_response(self, request, response, spider):
        ip = request.meta['proxy'].split('/')[-1]
        sql = 'update proxy set status=%s where proxy=%s'
        if response.status == 200:
            data = ('active', ip)
        else:
            data = ('inactive', ip)
        self.cursor.execute(sql, args=data)
        self.conn.commit()
        print(request.meta['proxy'], response.status)

        return response
