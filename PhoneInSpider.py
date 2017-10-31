#coding:utf-8
import sys
import urllib2
import sqlite3
import json
import time
import re


class SQLITETool:
    def __init__(self,databaseName):
        self.databaseName = databaseName
        self.create_db()

    def create_db(self):
        conn = sqlite3.connect(self.databaseName)
        conn.close();

    def execute_table(self,sql):
        conn = sqlite3.connect(self.databaseName);
        cursor = conn.cursor();
        try:
            cursor.execute(sql)
        except Exception, e:
            print(Exception,":",e)
        finally:
            conn.commit()
            cursor.close()
            conn.close()


class PhoneInfoSpider:
    def __init__(self,databaseName,phoneSections):
        self.phoneSections = phoneSections
        self.sqlTool = SQLITETool(databaseName)

    def phoneInfoHandler(self,jsonData):
            mobile = jsonData['Mobile'];
            corp = jsonData['Corp'];
            province = jsonData['Province'];
            city = jsonData['City'];
            try:
                sql = 'insert into phone_info_table (mobile, corp, province, city) values(\'{0}\',\'{1}\',\'{2}\',\'{3}\')'.format(mobile,corp,province,city);
                self.sqlTool.execute_table(sql)
            except Exception,e:
                print(Exception,":",e)

    def requestPhoneInfo(self,phoneNum):
        print(phoneNum);
        try:
            #因为有20次/min的ip限制，所以sleep  3s
            time.sleep(3);
            response = urllib2.urlopen('http://v.showji.com/Locating/showji.com2016234999234.aspx?m={0}&output=json&callback=querycallback&timestamp=1484546664567'.format(phoneNum))
            resStr = response.read()
            jsonStr = re.search(r'querycallback\((.*?)\);',resStr,re.S).group(1)
            jsonData = json.loads(jsonStr)
            self.phoneInfoHandler(jsonData)
        except Exception,e:
            print(Exception,":",e)

    def requestAllSections(self):
        #last用于接上次异常退出前的号码
        last = 0
        #自动生成手机号码，后四位补0
        for head in self.phoneSections:
            for i in range(last,10000):
                middle = str(i).zfill(4)
                phoneNum = head+middle+"0000"
                self.requestPhoneInfo(phoneNum)
            last = 0

if __name__ == '__main__':
    reload(sys);
    sys.setdefaultencoding('utf-8');

    #要爬的号码段
    yys = ['134','135','136','137','138','139','150','151','152','133','153','180','181','189','177','173','149','182','183','184','178', '157','158','159','187','188','147','130','131','132','155','156','185','186','145','176'];
    spider = PhoneInfoSpider('phone.db',yys)
    sql = 'CREATE TABLE phone_info_table (mobile varchar(11) primary key,corp varchar(32),province varchar(16), city varchar(32));'
    spider.sqlTool.execute_table(sql)
    spider.requestAllSections()
