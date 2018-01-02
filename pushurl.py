#!/usr/bin/env python3


import MySQLdb as mdb


if __name__ == "__main__":
    conn = mdb.connect('localhost', 'scrapy', 'scrapy', 'scrapy')
    cursor = conn.cursor()
    sql_mode = 'insert into url values'
    for i in range(20):
        sql = sql_mode
        for page in range(i * 200000 + 1, (i + 1) * 200000 + 1):
            sql += '("https://www.lagou.com/jobs/%d.html", "no"),' % page
        sql = sql[:-1]
        cursor.execute(sql)
        conn.commit()
        print(i)

