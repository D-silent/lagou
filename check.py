#!/usr/bin/env python3

import requests

import MySQLdb as mdb


class Checker:
    conn = mdb.connect('localhost', 'scrapy', 'scrapy', 'scrapy')
    cursor = conn.cursor()


    def get_proxies(self):
        sql = 'select * from proxy where proxytype="https"'
        self.cursor.execute(sql)
        return self.cursor.fetchall()


    def update_mysql(self, ip, status):
        sql = 'update proxy set status=%s where proxy=%s'
        data = (status, ip)
        self.cursor.execute(sql, args=data)
        self.conn.commit()


    def check(self, proxy):
        ip = proxy.split('/')[-1]
        test_url = 'https://www.lagou.com'
        proxies = {'https': proxy}
        timeout = 5
        try:
            requests.get(url=test_url, proxies=proxies, timeout=timeout)
        except:
            print('---------------------')
            self.update_mysql(ip, 'inactive')
        else:
            print(proxy)
            self.update_mysql(ip, 'active')


if __name__ == "__main__":
    checker = Checker()
    proxies = checker.get_proxies()
    print(len(proxies))
    for value in proxies:
        proxy = value[0] + '://' + value[1]
        checker.check(proxy)

