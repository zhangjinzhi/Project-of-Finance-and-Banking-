# coding=utf-8
import sys
import tushare as ts
import numpy as np
import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt
###########################################################
#动态散点图

# plt.axis([0, 100, 0, 1])
# plt.ion()
#
# for i in range(100):
#     y = np.random.random()
#     plt.scatter(i, y)
#     plt.pause(0.1)
##########################################################
reload(sys)
sys.setdefaultencoding('utf8')

# 打开数据库连接
db =MySQLdb.connect(host='127.0.0.1',user='root',passwd='zjz4818774',db='tusharedata',port=3306,charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()


# SQL 查询语句
# sql = "SELECT * FROM EMPLOYEE WHERE INCOME > '%d'" % (1000)
# sql = 'select * from PLICC_data'
sql1 = 'select date,open,high,close,low,volume,ma5,ma10,ma20,price_change from PLICC_data  order by date asc'
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

price_data = []
tag = []

line_num = 0
for row in rows:
    line_num += 1

    if line_num < 401:

        col = []
        for i in range(1,9):
           col.append(row[i])

        price_data.append(col)

        # if row[9] > 0 :
        #    tag.append(1)
        # else:
        #    tag.append(0)
        tag.append(row[3])


price_data = price_data[:-1]
# print price_data
tag  =  tag[1:]
# print tag

X = np.array(price_data)
Y = np.array(tag)
# print X
# print Y
###########################################
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR

from sklearn.preprocessing import StandardScaler
from numpy import *


x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2)
# f(x) = (x - means) / standard deviation
scaler = StandardScaler()
scaler.fit(x_train)
# standardization
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

# construct SVR model
#########################
clf_linear  = SVR(kernel='linear')
clf_poly    = SVR(kernel='poly', degree=3)
clf_sigmoid = SVR(kernel='sigmoid')
svr = clf_linear
#########################
# svr = SVR(kernel = 'rbf')

svr.fit(x_train, y_train)
y_predict = svr.predict(x_test)
# print y_test
# print y_predict
result = hstack((y_test.reshape(-1, 1), y_predict.reshape(-1, 1)))
print result
fp=open('predict_result.txt', 'w')
fp.write(str(result))
fp.close()
##################################
print svr.score(x_test, y_test)


import matplotlib.pyplot as plt

plt.autoscale(True, 'both', None)
#绘制方格
plt.rc('axes', grid=True)
plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
plt.plot( y_test,label='original close price')
plt.plot( y_predict,label='predicted close price')
plt.legend(loc='best')
#设置坐标标签

plt.xlabel('Time Interval')
# plt.ylabel('Close')
#将x坐标日期进行倾斜
plt.setp(plt.gca().get_xticklabels(), rotation=20, horizontalalignment='right')
plt.show()