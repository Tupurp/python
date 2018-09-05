#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : export.py
# @Author: tupurp
# @Date  : 2018/9/5 15:29
# @Desc  : 查询数据库中经过base64编码的html文本中的图片链接地址

import pymysql
import base64
import re

#url正则
reg = r'src="(.*?\.[a-z]+)"'
#url保存文件路径
file="F:\\article.sql"
#成功日志路径
log="F:\\log.sql"
#计数sql
count_sql = '  SELECT \
        COUNT(ID)\
        FROM\
        S_ARTICLE\
        WHERE 1 = 1\
        AND CONTENT IS NOT NULL'


#打开数据库连接
host = input("请输入数据库地址，不要携带端口：")
user = input("请输入数据库用户名：")
passwd = input("请输入数据库密码：")
db = input("请输入要连接的数据库名称：")
port = input("请输入数据库端口：")
port = int(port)


db = pymysql.connect(host,user,passwd,db,port)

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

def query_content(total,page=0,limit=10):
    print('当前下载第%d页数据'%(page+1))

    with open(log, 'a', encoding='UTF-8') as f:
        f.write( '\n'+"第%d页数据查询：" % (page + 1) + '\n')
    start = page*limit
    query_sql = 'SELECT\
               SEQUENCE_ID,\
               CONTENT\
                FROM\
                S_ARTICLE\
                WHERE 1 = 1\
                AND CONTENT IS NOT NULL\
                ORDER BY CREATED_TIME\
                LIMIT %s,%s \
                 ' %(str(start),str(limit))
    cursor.execute(query_sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    size = len(results)
    for row in results:
        id = row[0]
        content = row[1]
        #base64解码
        content = base64.b64decode(content)
        content = str(content,'utf-8')
        #正则提取url
        pattern = re.compile(r'<img src="(.*?\.[a-z]+)"')
        src = re.findall(pattern,content)
        length = len(src)
        print("第%d页查询共有%d条资讯,本条资讯序列为%s,其正文共有%d条图片或视频链接"%(page+1,size,id,length))
        with open(log, 'a', encoding='UTF-8') as f:
            f.write("本条资讯序列为%s,其正文共有%d条图片或视频链接"%(id,length)+ '\n')
        if(length > 0):
            for img in src:
                pre = img[0:img.rfind('/', 1) + 1]
                end = img.replace(pre,' ')
                # 存入文件
                with open(file, 'a', encoding='UTF-8') as f:
                     f.write(pre+end+'\n')

    if start + limit>=total:
        return
    page = page+1
    query_content(total,page,limit)



try:
    # 执行SQL语句
    cursor.execute(count_sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    count = 0
    for row in results:
        count = row[0]
        # 打印结果
        print("共有%s条资讯数据" % \
              (count))
        with open(file, 'a', encoding='UTF-8') as f:
            f.write('#共有%s条资讯数据\n'%(count))

    query_content(count)

    print("数据下载完成")

except:
    print("Error: unable to fetch data")

# 关闭数据库连接
db.close()
