#!/usr/bin/python

# -*- coding: UTF-8 -*-


import urllib
import urllib2
import re
import MySQLdb
import json


class crawl1:
    def getHtml(self,url=None):

        user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
        header={"User-Agent":user_agent}
        request=urllib2.Request(url,headers=header)
        response=urllib2.urlopen(request)
        html=response.read()
        return html

    def getContent(self,html,reg):
        content=re.findall(html, reg, re.S)
        return content


    def connectDB(self):
        host="192.168.85.21"
        dbName="test1"
        user="root"
        password="123456"
        db=MySQLdb.connect(host,user,password,dbName,charset='utf8')
        return db
        cursorDB=db.cursor()
        return cursorDB


    def creatTable(self,createTableName):
        createTableSql="CREATE TABLE IF NOT EXISTS "+ createTableName+"(time VARCHAR(40),title VARCHAR(100),text  VARCHAR(40),clicks VARCHAR(10))"
        DB_create=self.connectDB()
        cursor_create=DB_create.cursor()
        cursor_create.execute(createTableSql)
        DB_create.close()
        print 'creat table '+createTableName+' successfully'
        return createTableName

    def inserttable(self,insertTable,insertTime,insertTitle,insertText,insertClicks):
        insertContentSql="INSERT INTO "+insertTable+"(time,title,text,clicks)VALUES(%s,%s,%s,%s)"
#         insertContentSql="INSERT INTO "+insertTable+"(time,title,text,clicks)VALUES("+insertTime+" , "+insertTitle+" , "+insertText+" , "+insertClicks+")"


        DB_insert=self.connectDB()
        cursor_insert=DB_insert.cursor()
        cursor_insert.execute(insertContentSql,(insertTime,insertTitle,insertText,insertClicks))
        DB_insert.commit()
        DB_insert.close()
        print 'inert contents to  '+insertTable+' successfully'



url = "http://baoliao.hb.qq.com/api/report/NewIndexReportsList/cityid/18/num/20/pageno/1?callback=jQuery183019859437816181613_1440723895018&_=1440723895472"



reg_jason = r'.*?jQuery.*?\((.*)\)'
reg_time=r'.*?"create_time":"(.*?)"'
reg_title=r'.*?"title":"(.*?)".*?'
reg_text=r'.*?"content":"(.*?)".*?'
reg_clicks=r'.*?"counter_clicks":"(.*?)"'


crawl = crawl1()
html = crawl.getHtml(url)
html_jason=re.findall(reg_jason, html, re.S)

html_need = json.loads(html_jason[0])

print len(html_need)
print len(html_need['data']['list'])




table=crawl.creatTable('htk')
for i in range(len(html_need['data']['list'])):
    creatTime=html_need['data']['list'][i]['create_time']
    title=html_need['data']['list'][i]['title']
    content=html_need['data']['list'][i]['content']
    clicks=html_need['data']['list'][i]['counter_clicks']
    crawl.inserttable(table,creatTime,title,content,clicks)