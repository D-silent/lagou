#!/usr/bin/env python3


import queue
import threading
from lxml import etree
from random import choice
from urllib import request
import MySQLdb as mdb


#  创建锁对象
threadLock = threading.Lock()
#  代理ip池
#  proxies = open('proxy.dat').readlines()
#  用户代理池
agents = open('agent.dat').readlines()
#  创建队列
q_queue = queue.Queue()
conn = mdb.connect('localhost', 'scrapy', 'scrapy', 'scrapy')
cursor = conn.cursor()
sql = 'select * from proxy where proxytype=%s and status=%s'
data = ('https', 'active')
cursor.execute(sql, args=data)
proxies = cursor.fetchall()


def parse(tree):
    """
    页面解析
    """
    #  职位名
    jobname = tree.xpath('//div[@class="job-name"]/@title')[0]
    #  用于抽取职位信息
    p = tree.xpath('//dd[@class="job_request"]/p[1]')[0]
    #  薪水范围
    salary = p.xpath('span[1]/text()')[0].strip()
    #  工作城市
    addr = p.xpath('span[2]/text()')[0].split('/')[1].strip()
    #  经验要求
    exprience = p.xpath('span[3]/text()')[0].split('/')[0].strip()
    #  学历要求
    edureq = p.xpath('span[4]/text()')[0].split('/')[0].strip()

    return jobname, salary, addr, exprience, edureq

def crawl():
    """
    爬虫程序
    """
    count = 0
    flag = True
    while not q_queue.empty():
        #  获取一个url
        url = q_queue.get()
        #  设置请求头
        headers = {
                'User-Agent': choice(agents).strip(),
                "Connection": "close",#"keep-alive",
                "Host": "www.lagou.com",
                'Origin':'https://www.lagou.com',
                'Referer':'https://www.lagou.com',
                "Upgrade-Insecure-Requests": "1",
                }
        #  使用代理ip
        if flag:
            ip = choice(proxies)
            ip = ip[0] + '://' + ip[1]
            proxy = {'https': ip}
            flag = False
        count += 1
        if count > 4:
            count = 0
            flag = True

        try:
            """
            使用代理ip和设置好的请求头获取url页面
            """
            proxy_handler = request.ProxyHandler(proxy)
            opener = request.build_opener(proxy_handler)
            request.install_opener(opener)
            req = request.Request(url=url, headers=headers)
            res = request.urlopen(req)
        except Exception as e:
            print(e)
            print("urlopen")
            q_queue.put(url)
            continue

        try:
            #  url页面的html文本
            content = res.read().decode('utf-8')
            #  构建解析树
            tree = etree.HTML(content)

            try:
                jobname, salary, addr, exprience, edureq = parse(tree)
                print(jobname)
            except Exception as e:
                print(e)
                print("parse")
                q_queue.put(url)
                continue
            #  加锁
            threadLock.acquire()
            #  解锁
            threadLock.release()
        except Exception as e:
            print(e)
            print("read")
            q_queue.put(url)
            continue

if __name__=="__main__":
    #  将url加入队列
    for page in range(3,4000000):
        url = "https://www.lagou.com/jobs/%d.html" % page
        q_queue.put(url)

    t=threading.Thread(target=crawl,)
    t.start()
    t.join()
