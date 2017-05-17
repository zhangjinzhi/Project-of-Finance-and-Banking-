#coding=utf-8
import sys
import MySQLdb
import numpy as np
import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding('utf8')

# 打开数据库连接
db =MySQLdb.connect(host='127.0.0.1',user='root',passwd='zjz4818774',db='tusharedata',port=3306,charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()


# SQL 查询语句
# sql = "SELECT * FROM EMPLOYEE WHERE INCOME > '%d'" % (1000)
# sql = 'select * from PLICC_data'
sql1 = 'select date,open,high,close,low,price_change from PLICC_data  order by date asc'
sql2 = 'select date,open,high,close,low from PingAnInsurance  order by date asc'

try:
    cursor.execute(sql1)

    rows = cursor.fetchall()
    #获取连接对象的描述信息
    # desc = cursor.description
    # print 'cursor.description:',desc

    # #打印表头，就是字段名字
    # print "%s %3s" % (desc[0][0], desc[1][0])

    # for row in rows:
    #     print row

except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])

# 关闭数据库连接
db.close()

import csv
csvfile = file('stock_close.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerow(['date', 'close'])


fp=open('data.txt', 'w')

date = []
close_data = []

for row in rows:
    date.append(row[0])
    close_data.append(row[3])
    if row[5] > 0 :
        up_down = "\t"+"1"
    else:
        up_down = "\t"+"-1"

    fp.write((str(row[1:-1])+up_down).replace('(','').replace(')','').replace(',','')+'\n')

    writer.writerow([row[0],row[3]])

plt.autoscale(True, 'both', None)
#绘制方格
plt.rc('axes', grid=True)
plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
plt.plot(close_data)
#设置坐标标签
plt.xlabel('Date')
plt.ylabel('Close')
#将x坐标日期进行倾斜
plt.setp(plt.gca().get_xticklabels(), rotation=20, horizontalalignment='right')
plt.show()


fp.close()
csvfile.close()